import pandas as pd
import requests
import json
import argparse




headers = {'content-type':'application/json'}









def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
        api_key = (config["api_key"])

        print(api_key)
    return config




#fheaders = login(username, password)

# Read the Excel file into a pandas DataFrame
# Function to check if dataset exists
def dataset_exists():
    print (fheaders)
    dataset_url = f"{dremio_url}/api/v3/catalog/by-path/{'/'.join(dataset_path)}/{dataset_name}"
    print(requests.get(dataset_url, headers=fheaders))
    response = requests.get(dataset_url, headers=fheaders)
    print ("dataset check " + str( response.status_code))
    if response.status_code in [200, 201]:
        print("Table exists!")
    return response.status_code == 200






def execute_sql(sql):
    query_url = f"{dremio_url}/api/v3/sql"
    payload = {"sql": sql}
    response = requests.post(query_url, headers=fheaders, json=payload)
    if response.status_code in [200, 201, 202]:
        print("SQL executed successfully!")
    else:
        print("Failed to execute SQL.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)



# Function to create the table
def create_table(columns):
    columns_def = ', '.join([f"{col} VARCHAR" for col in columns])
    sql = f"CREATE TABLE {'.'.join(dataset_path)}.{dataset_name} ({columns_def})"
    print(sql)
    execute_sql(sql)

def main(excel_file_path, dataset_name, config, dataset_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file_path)





    # Convert datetime columns to ISO format strings
    for col in df.select_dtypes(include=['datetime', 'datetimetz']):
        df[col] = df[col].apply(lambda x: x.isoformat() if pd.notnull(x) else None)

    # Convert DataFrame to JSON format suitable for Dremio
    #records = df.to_dict(orient='records')



    if not dataset_exists():
        create_table(df.columns)
        print("created table")

    # Generate SQL insert statements and execute them
    for index, row in df.iterrows():
        columns = ', '.join(row.index)
        values = ', '.join(f"'{str(value)}'" if pd.notnull(value) else 'NULL' for value in row.values)
        sql = f"INSERT INTO {'.'.join(dataset_path)}.{dataset_name} ({columns}) VALUES ({values})"
        ##print(sql)
        execute_sql(sql)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Insert Excel data into Dremio.')
    parser.add_argument('-c', '--config', type=str, required=True, help='Path to the config file.')
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the Excel file.')
    parser.add_argument('-t', '--table', type=str, required=True, help='Name of the dataset/table in Dremio.')
    parser.add_argument('-p', '--path', type=str, required=True,  help='Name of the path in Dremio.')
    args = parser.parse_args()
    config = load_config(args.config)
    api_key = (config["api_key"])
    dremio_url = (config["dremio_url"])
    dataset_v = args.path
    dataset_path = list(dataset_v.split(","))

    dataset_name = args.table
    excel_file_path = args.file
    print(excel_file_path)


    # Headers for Dremio API
    fheaders = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    main(excel_file_path, dataset_name, config, dataset_path)