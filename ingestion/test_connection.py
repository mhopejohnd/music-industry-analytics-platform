from sqlalchemy import create_engine

USERNAME = "postgres"
PASSWORD = "Martina-Desiree4"
HOST = "localhost"
PORT = "5432"
DATABASE = "music_analytics"

engine = create_engine(
    f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

try:
    with engine.connect() as conn:
        print("Connected successfully!")
except Exception as e:
    print("Connection failed!")
    print(e)