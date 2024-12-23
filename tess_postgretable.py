import pandas as pd
from sqlalchemy import create_engine

# Database connection details
db_name = 'postgres'
db_user = 'postgres'
db_password = 'harry1130'
db_host = 'sku.crgka6sy8spi.us-west-1.rds.amazonaws.com'
db_port = '5432'

# Create a connection to the PostgreSQL database
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

query_tables = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
df_tables = pd.read_sql(query_tables, engine)

# Display the table names
query_sku = 'SELECT * FROM public."SKU"'
df_sku = pd.read_sql(query_sku, engine)

# Display the data from the SKU table
print(df_sku)
print(df_sku)
