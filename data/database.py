from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql://postgres:postgres@10.25.53.161:5432/demo"

# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

today_date = datetime.now().strftime("%Y-%m-%d")

# Define the Log model
class Log(Base):
    __tablename__ = f'logs_{today_date}'
    
    id = Column(Integer, primary_key=True, index=True)
    error = Column(String, index=True)
    token = Column(String, index=True)
    error_details = Column(Text)
    created_at = Column(DateTime, default=func.now())  # Add the timestamp column

# Function to initialize the database
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False








# from sqlalchemy import create_engine
# from sqlalchemy.exc import OperationalError

# # Replace with the actual IP address and port of your PostgreSQL server
# DATABASE_URL = "postgresql://postgres:postgres@10.25.53.161:5432/demo"

# def test_connection():
#     engine = create_engine(DATABASE_URL)
#     try:
#         with engine.connect() as connection:
#             print("Connection to the database is successful!")
#     except OperationalError as e:
#         print(f"OperationalError: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     test_connection()

