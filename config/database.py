import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = "../db/database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

print(database_url)

engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

# --------------------------------------Details------------------------------------
# | * importamos os para requerir todos las funciones del sistema operativo.        |
# | * importamos create_engine para crear un motor de base de datos.                |
# | * importamos sessionmaker para crear la session de nuestra conexión a nuesta db.|
# | * importamos declarative_base para poder ir trabajando nuestro orm desde ahí    |
# | * engine crea una instancia del resultado que devuelve create_engine            |
# | * session guarda la sesión creada a partir del motor.                           |
# ----------------------------------------------------------------------------------
