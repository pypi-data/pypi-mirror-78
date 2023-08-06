""" This module defines all exergi functions within the AWS.postgreSQL module"""

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
    
    # Returns an error if a parameter is not listed in the initialization file
    else:
        raise Exception(f'Section {section} not found in the {filePath} file')
    return db_cred

def checkPostgreSQLConnection(db_cred: dict):
    """A function that checks connection settings and version of postgreSQL
    
    Arguments:
        - db_cred        - Connection parameters from config file
    Returns:
        - return_str     - Results of connection check 
    """

    import psycopg2

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
        return_str = f"{dsn_para}\n\nYou are connected to - {record}"

    except (Exception, psycopg2.Error) as error:
        return_str = f"Error while connecting to PostgreSQL, {error}"
    finally:
        # Closing database connection.
            if(conn):
                cursor.close()
                conn.close()
                return_str = return_str + "\n\nPostgreSQL connection is closed"
    return return_str
                
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
    connection = None
    
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
                        print(f"Warning! '{col}' has multiple dtypes in schema. Using most popular dtype for conversion")
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
                            df[col] = pd.to_datetime(df[col],infer_datetime_format=True,utc=True,errors="coerce")
                    
                    # Date conversion
                    elif dtype == 'date':
                        if data_dtype == np.dtype('O'):
                            df[col] = pd.to_datetime(df[col],infer_datetime_format=True,utc=True,errors="coerce")

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
                        raise(Exception(f"Data conversion '{dtype}' not implemented. Please contact package administrator"))
        else:
            print("WARNING. No data type conversion was executed")
        
        # Remove Timezone info from datetime tags
        for col in df.select_dtypes(include='datetime64[ns, UTC]').columns:
            df[col] = df[col].dt.tz_localize(None)
        
        # Post rename
        if post_rename:
            df = df.rename(columns=post_rename)
        
        success_bool = True
        return_str = f"Query executed without errors in {time.time()-start:.3f} [s]. Resulting DataFrame shape = {df.shape}"
        
    except Exception as e:
        
        if raise_error:
            raise(e)
        else:
            tb = traceback.format_exc(e)
        df = pd.DataFrame()
        success_bool = False
        return_str = f"Failed to execute query ({tb})"

    finally:
            if(connection):
                cursor.close()
                connection.close()

    return df,success_bool,return_str

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
    connection = None
    
    # Format Query
    df_meta_query = f"""
        SELECT table_name,column_name,data_type,is_nullable FROM 
        information_schema.columns WHERE table_name LIKE '{like_str}%'"""

    try:
        # Import Data
        connection = psycopg2.connect(**db_cred)
        cursor = connection.cursor()
        df_meta = pd.read_sql(df_meta_query,connection).drop_duplicates()

    except Exception as error:
        raise(error)   
    finally:
            if(connection):
                cursor.close()
                connection.close()    
    return df_meta
