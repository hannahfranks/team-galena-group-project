from ingest import db_connection, get_secret, get_table_names, extract_table_data, save_tables_as_parquet

#get the RDS secrets from aws secret manager
credentials = get_secret()

# connect to DB
conn = db_connection(credentials)

# get all the table names 
table_names = get_table_names(conn)

# Extract data from all the tables and return a dictionary of tables
tables_data = extract_table_data(table_names, conn)

# transform data to parquet and save to s3
data = save_tables_as_parquet(tables_data, "s3-ingestion-bucket-team-galena")