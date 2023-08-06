""" This module defines all exergi functions within the AWS.RDS module"""

def config(filePath: str ='/home/ec2-user/SageMaker/.config/database.ini', 
    section: str = 'maximo')-> dict:
    """ The following config() function reads in the database.ini file and 
    returns the connection parameters as a dictionary. This function will be 
    imported in to the main python script. 
    
    This file was adapted from:
    http://www.postgresqltutorial.com/postgresql-python/connect/
    
    Arguments:
        - filePath      - Path to the "database.ini"-file required to initiate
                          connection.
        - section       - Section of "database.ini"-filefile where the 
                          connection-parameters are stored.
    Returns:
        - db_cred  - All connection parameters in the specified filePath   
                          and section
    """

    from configparser import ConfigParser

    parser = ConfigParser()     # Create a parser
    parser.read(filePath)       # Read config file
    db_cred = {}                # Get section, default to postgresql
    
    # Checks to see if section (postgresql) parser exists
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_cred[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filePath} file')
    return db_cred

def checkPostgreSQLConnection(db_cred: dict):
    """A function that checks connection settings and version of postgreSQL
    
    Arguments:
        - db_cred        - Connection parameters from config file or manually 
                           defined dictionary
    """
    
    import logging
    import psycopg2

    # Import logger from main script if already initiated
    logger = logging.getLogger(__name__)
    logger.info('Checking DB Connection')
    
    try:

        # Setup connection
        conn = psycopg2.connect(**db_cred)
        cursor = conn.cursor()
        
        # Print PostgreSQL Connection properties
        dsn_para = conn.get_dsn_parameters()
        
        # Print PostgreSQL version
        cursor.execute("SELECT version();")           
        record = cursor.fetchone()

        # Construct connection string
        logger.info(f"\tDSN Parameters:")
        for key in dsn_para: logger.info(f"\t\t{key:20} = {dsn_para[key]}")
        logger.info(f"\tConnection information:")
        logger.info(f"\t\t{record}")
        
    except (Exception, psycopg2.Error) as error:
        logger.info(f"Error while connecting to PostgreSQL, {error}")
    finally:
        # Closing database connection.
            if(conn):
                cursor.close()
                conn.close()
                logger.info("\tConnection is closed")

def importMetaData(db_cred: dict,like_str: str = "maximoworker_"):
    """Function for importing data base schema for every table with a table
    name starting with like_str 
    
    (SQL: ... WHERE table_name LIKE '{like_str}%)
    
    Arguments:
    - like_str - List all tables with table_name starting with this string. 
                (default: "maximoworker_")
    - db_cred  - Dictionary containing all login information either manually 
                entered or using the config function of the exergi-package.
    Returns
    - df_meta - DataFrame containing 
    """
        
    import psycopg2
    import pandas as pd
    import logging
    connection = None
    
    # Format Query
    df_meta_query = f"""
        SELECT table_name,column_name,data_type,is_nullable FROM 
        information_schema.columns WHERE table_name LIKE '{like_str}%'"""

    # Import logger from main script if already initiated
    logger = logging.getLogger(__name__)
    logger.info('Loading Meta Data:')

    try:
        # Import Data
        connection = psycopg2.connect(**db_cred)
        cursor = connection.cursor()
        df_meta = pd.read_sql(df_meta_query,connection).drop_duplicates()
        
        logger.info(f'\tOK! {df_meta.shape[0]} rows loaded from schema')
        
    except (Exception, psycopg2.Error) as error:
        logger.info(f"\tError while querying data, {error}")
    finally:
            if(connection):
                cursor.close()
                connection.close()    
                logger.info("\tConnection is closed")
    return df_meta

def importData(sql_query: str, db_cred: dict, df_meta = None, 
    post_rename: dict = {}, convert_dtypes: bool = True,
    raise_error: bool = True, remove_tz: bool = False):
    """A function that takes in a PostgreSQL query and outputs a pandas database 
    
    Arguments:
        - sql_query         - SQL-query to run
        - db_cred           - Connection parameters from config file
        - df_meta           - DataFrame with schema information from 
                              importMetaData function
        - post_rename       - Dictionary for renaming dictionaries after dtype 
                              conversion
        - convert_dtypes    - Flag if data types should be converted using the 
                              data base schema for the used table
        - remove_tz         - Flag if timezone info should be removed from 
                              datetime columns
    Returns:
        - df                - DataFrame with loaded data
    """

    import psycopg2
    import pandas as pd
    import numpy as np
    import traceback
    import time
    import logging
    connection = None
    
    # Import logger from main script if already initiated
    logger = logging.getLogger(__name__)
    logger.info('Loading Data:')

    try:
        
        start = time.time()

        # Get Data
        connection = psycopg2.connect(**db_cred)
        cursor = connection.cursor()
        df = pd.read_sql_query(sql_query, connection)
        
        if (df_meta is not None) & (convert_dtypes):

            for col,data_dtype in df.dtypes.iteritems():
                
                # Check schema
                df_meta_subset = df_meta.loc[df_meta.column_name==col,]
                
                if (df_meta_subset.empty == False):

                    # If there are more than one schema type present in df_meta
                    if df_meta_subset.data_type.nunique() > 1:
                        logger.warning(f"\t'{col}' has multiple dtypes in schema. Using most popular dtype for conversion")
                        dtype = df_meta_subset.data_type.value_counts().index[0]
                    else:
                        dtype = df_meta_subset.data_type.unique().item()

                    # Integer conversion
                    if dtype in ['integer','bigint']:
                        if data_dtype != np.dtype('int64'):
                            df[col] = df[col].astype(pd.Int64Dtype())    
                    
                    # String conversion
                    elif dtype in ['character varying','text']:
                        if data_dtype == np.dtype('O'):
                            df[col] = df[col].astype(pd.StringDtype()) 
                    
                    # DateTime conversion
                    elif dtype == 'timestamp with time zone':
                        if data_dtype == np.dtype('O'):
                            df[col] = pd.to_datetime(df[col],
                            infer_datetime_format=True,
                            utc=True,errors="coerce")
                    
                    # Date conversion
                    elif dtype == 'date':
                        if data_dtype == np.dtype('O'):
                            df[col] = pd.to_datetime(df[col],
                            infer_datetime_format=True,utc=True,
                            errors="coerce")

                    # Floats conversions
                    elif ((dtype == 'double precision') | (dtype == 'numeric')):
                        if data_dtype != np.dtype('float64'):
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                
                    # Boolean conversion
                    elif dtype == 'boolean':
                        if data_dtype != np.dtype('bool'):
                            df[col] = df[col].astype(bool)
                    
                    # Raise error if conversion hasn't been implemented 
                    else:
                        raise_str = f"""\tData conversion '{dtype}' not implemented. Please contact package administrator"""
                        logger.critical(raise_str)
                        raise(Exception(raise_str))
        else:
            logger.warning("\tNo data type conversion was executed")
        
        # Remove Timezone info from datetime tags
        for col in df.select_dtypes(include='datetime64[ns, UTC]').columns:
            df[col] = df[col].dt.tz_localize(None)
        
        # Post rename
        if post_rename:
            df = df.rename(columns=post_rename)
        
        # Output results to logger and return string
        success_bool = True
        return_str = "\tOK! Query executed in {:.3f} [s]. Shape = {}".format(
            time.time()-start,
            df.shape)
        logger.info(return_str)
        
    except:
        tb = traceback.format_exc()
        df = pd.DataFrame()
        success_bool = False
        return_str = f"\tFailed to execute query ({tb})"
        logger.critical(return_str)

    finally:
            if(connection):
                cursor.close()
                connection.close()
                logger.info("\tConnection is closed")

    return df,success_bool,return_str


