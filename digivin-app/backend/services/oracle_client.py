from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

class OracleClient:
    def __init__(self):
        self.username = os.getenv('ORACLE_DB_USERNAME')
        self.password = os.getenv('ORACLE_DB_PASSWORD')
        self.dsn = os.getenv('ORACLE_DB_DSN')
        self.engine = create_engine(f'oracle+cx_oracle://{self.username}:{self.password}@{self.dsn}')
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def close_session(self, session):
        session.close()