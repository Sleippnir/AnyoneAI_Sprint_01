from typing import Dict
import logging
from pandas import DataFrame
from sqlalchemy.engine.base import Engine
from time import sleep

# Configure logging to log errors to a file
# (just used to it, not necessary for base functionality)
# logging.basicConfig(
    
#     filename="database_load.log", 
#     level=logging.ERROR, 
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )
        
def load(data_frames: Dict[str, DataFrame], database: Engine):
    errors = {}  # Store error messages

    for table_name, df in data_frames.items():
        try:
            df.to_sql(name=table_name, con=database, if_exists="replace", index=False)
        except Exception as e:
            error_msg = f"{e}"
            logging.error(f"Failed to load table {table_name}: {error_msg}")
            errors[table_name] = error_msg


    # Print errors if any exist
    if errors:
        print("The following errors occurred during data loading:")
        for table, msg in errors.items():
            print(f"{table}: {msg}")
        sleep(15)
    return  errors