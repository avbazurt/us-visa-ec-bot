import os, logging
from .clientDb import ClientSQLite


# Obtengo el Log
try:
    from src.PyLog import Log
    AppLog = Log(__name__)
except Exception as ex:
    import logging
    AppLog = logging.getLogger(__name__)
    AppLog.setLevel(logging.DEBUG)
    stramHandler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')    
    stramHandler.setFormatter(formatter)
    AppLog.addHandler(stramHandler)

NAME_TABLE = "PARAMETROS"

class Parametros:
    def __init__(self, log_level:int = logging.CRITICAL) -> None:
        AppLog.setLevel(log_level)

        # Primero valido si existe la carpeta
        folder = "database"
        if (not os.path.exists(folder)):
            os.mkdir(folder)
            AppLog.warning(f"The Folder '{folder}' created")

        # Procedo a inicializar el SQLite3
        self.ClientSQLite = ClientSQLite(f"{folder}/app2.db")

        # Verfico si existe la tabla
        dataQuery:dict = self.ClientSQLite.execute(f"SELECT * FROM {NAME_TABLE}")
        if (not dataQuery["status"] and dataQuery["msg"] == f"no such table: {NAME_TABLE}"):
            AppLog.warning(f"La tabla {NAME_TABLE} no existe, se procede a crear")
            # Si llegamos a este punto intento crear la tabla
            query = f"""CREATE TABLE {NAME_TABLE} (
                        ID_SECUENCIAL INT AUTO_INCREMENT,
                        NOMBRE VARCHAR(100) PRIMARY KEY,
                        VALOR VARCHAR(100),
                        FECHA_REGISTRO DATETIME,
                        FECHA_MODIFICACION DATETIME,
                        OBSERVACION VARCHAR(100)
                    );
                    """
            self.ClientSQLite.execute(query)

    def __setitem__(self, key, value):
        self.ClientSQLite.execute(f"INSERT OR REPLACE INTO {NAME_TABLE} (NOMBRE, VALOR) VALUES (?, ?)", (key, value))

    def __getitem__(self, key):
        dataQuery:dict = self.ClientSQLite.execute(f"SELECT VALOR FROM {NAME_TABLE} WHERE NOMBRE = '{key}'")

        if (not dataQuery["status"]):
            AppLog.error(dataQuery["msg"])
            return None

        elif (len(dataQuery["data"])==0):
            return None    

        return dataQuery["data"][0]["VALOR"]

