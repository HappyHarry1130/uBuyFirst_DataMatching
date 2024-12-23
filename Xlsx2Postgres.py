import pandas as pd
from sqlalchemy import create_engine

excel_file_path = '1.xlsx'
df = pd.read_excel(excel_file_path, engine='openpyxl')

db_name = 'postgres'
db_user = 'postgres'
db_password = 'harry1130'
db_host = 'sku.crgka6sy8spi.us-west-1.rds.amazonaws.com'
db_port = '5432'

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')


table_name = 'SKU'
df.to_sql(table_name, engine, if_exists='replace', index=False)

print(f"Data from {excel_file_path} has been successfully inserted into the {table_name} table.")