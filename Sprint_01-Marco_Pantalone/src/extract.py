from typing import Dict
import requests 
from pandas import DataFrame, read_csv, to_datetime
import os
def get_public_holidays(public_holidays_url: str, year: str) -> DataFrame:
    # Get the public holidays for the given year for Brazil.
    url = f"{public_holidays_url}/{year}/BR"
    
    with requests.Session() as session:  # Use a session to manage connections    
        try:
            response = session.get(url) # Make a GET request to the URL
            response.raise_for_status()  # Raises an exception for HTTP errors
        except requests.exceptions.RequestException as e: # Store any request exceptions as a variable
            raise SystemExit(f"Request failed: {e}") # Exit the program with stored error message
    
    # Alternative compact way to handle the response and convert it to a DataFrame
    # holidays_df = (
    # DataFrame(response.json())
    # .drop(columns=["types", "counties"], errors="ignore")
    # .assign(date=lambda df: to_datetime(df["date"]))
    # )
        
    
    # Store the response in a variable
    holidays_data = response.json()
    # Convert the JSON data to a DataFrame
    holidays_df = DataFrame(holidays_data)
    
    # Remove unwanted columns 
    holidays_df = holidays_df.drop(columns=["types", "counties"], errors="ignore")
    
    # Convert the 'date' column to datetime
    holidays_df["date"] = to_datetime(holidays_df["date"])
    
    return holidays_df




def extract(
    csv_folder: str, csv_table_mapping: Dict[str, str], public_holidays_url: str
) -> Dict[str, DataFrame]:
    """Extract the data from the csv files and load them into the dataframes.
    Args:
        csv_folder (str): The path to the csv's folder.
        csv_table_mapping (Dict[str, str]): The mapping of the csv file names to the
        table names.
        public_holidays_url (str): pyteThe url to the public holidays.
    Returns:
        Dict[str, DataFrame]: A dictionary with keys as the table names and values as
        the dataframes.
    """
    dataframes = {
        table_name: read_csv(f"{csv_folder}/{csv_file}")
        for csv_file, table_name in csv_table_mapping.items()
    }

    holidays = get_public_holidays(public_holidays_url, "2017")

    dataframes["public_holidays"] = holidays

    return dataframes

def dag_get_public_holidays(public_holidays_url: str, year: str, **kwargs):
    ti = kwargs['ti']
    df = get_public_holidays(public_holidays_url, year)
    output_dir = "/tmp/airflow_data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"public_holidays_{year}.parquet")
    df.to_parquet(output_path, index=False)
    ti.xcom_push(key="holidays_path", value=output_path)

def dag_extract(csv_folder: str, csv_table_mapping: Dict[str, str], public_holidays_url: str, **kwargs):
    """
    Airflow-compatible extract function that stores DataFrames to Parquet
    and returns their file paths via XCom.
    """
    dataframes = extract(csv_folder, csv_table_mapping, public_holidays_url)
    output_dir = "/tmp/extracted_data"
    os.makedirs(output_dir, exist_ok=True)

    file_paths = {}
    for table_name, df in dataframes.items():
        path = f"{output_dir}/{table_name}.parquet"
        df.to_parquet(path, index=False)
        file_paths[table_name] = path

    kwargs["ti"].xcom_push(key="extracted_paths", value=file_paths)

