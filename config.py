from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ['USER']
pwd = os.environ['PASSWORD']
host = os.environ['HOST']
database = os.environ['DATABASE']
port = os.environ['PORT']

# Assuming you are using PostgreSQL
DATABASE_CONNECTION = f'postgresql://{user}:{pwd}@{host}:{port}/{database}'
