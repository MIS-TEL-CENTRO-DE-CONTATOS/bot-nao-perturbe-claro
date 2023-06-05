import os
import pandas as pd

from dotenv import load_dotenv
from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()


class importFile:
    def __init__(self, archive):
        # Variaveis do banco
        server = os.getenv('SQL_SERVER')
        database = os.getenv('SQL_DATABASE')
        user_id = os.getenv('SQL_USER')
        password = os.getenv('SQL_PASSWORD')
        driver = 'ODBC Driver 17 for SQL Server'

        database_con = f'mssql://{user_id}:{password}@{server}/{database}?driver={driver}'
        # print(database_con)
        engine = create_engine(database_con, echo=False)
        Session = sessionmaker(bind=engine)
        con = engine.connect()

        try:
            con.execute(
                text(f"EXEC RENTABILIZACAO_PBI.dbo.PRC_CLARO_IMPORT_DIARIO_NP '{archive}'"))

            print(
                f"{datetime.today().strftime('%d/%m/%Y %H:%M:%S')} - Processo de importação iniciado com sucesso.")
        except Exception as e:
            print(f'Processo de importação falhou: {e}')

        con.close()
