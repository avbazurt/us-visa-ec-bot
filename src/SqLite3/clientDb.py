import sqlite3, os, logging
from sqlite3 import Cursor, Connection
from threading import Semaphore

# Obtengo el Log
try:
    from src.PyLog import Log
    AppLog = Log(__name__)
except Exception as ex:
    AppLog = logging.getLogger(__name__)
    AppLog.setLevel(logging.DEBUG)
    stramHandler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')    
    stramHandler.setFormatter(formatter)
    AppLog.addHandler(stramHandler)

# Creo mi clase
class ClientSQLite():
    def __init__(self, filepath:str, log_level:int = logging.CRITICAL) -> None:
        # Seteo primero el log
        AppLog.setLevel(log_level)

        file = os.path.basename(filepath)
        AppLog.debug(f"Init ClientSQLite in base '{file}'")

        # Variables a utilizar
        self._path:str = filepath
        self._semaphore: Semaphore = Semaphore()

        self._conn:Connection = None
        self._cursor: Cursor = None

    def _connect(self) -> (bool, str):
        try:
            AppLog.debug(f"Begin client SQLite")
            self._conn = sqlite3.connect(self._path)
            self._cursor = self._conn.cursor()
            return (True, "")
        
        except sqlite3.Error as err:
            AppLog.error(err)     
            return (False, str(err))
        
        except Exception as ex:
            AppLog.error(ex, exc_info=True)
            return (False, str(ex))

    def _disconnect(self)-> (bool, str):
        # Cerrar la conexión y el cursor al finalizar
        AppLog.debug(f"Disconnect client SQLite")
        try:
            if (self._conn != None and self._cursor != None):
                self._conn.commit()
                self._cursor.close()
                self._conn.close()

            self._conn = None
            self._cursor = None

            return (True, "")

        except sqlite3.Error as err:
            AppLog.error(err)     
            return (False, str(err))

        except Exception as ex:
            AppLog.error(ex, exc_info=True)
            return (False, str(ex))

    def execute(self, query:str, parameters:set = None) -> dict:
        dataQuery:dict = {"status": False, "msg": "", "data":[]}

        try:
            with self._semaphore:
                #Primero intento conectarme
                status, msg = self._connect()
                if (not status):
                    dataQuery["msg"] = msg
                    dataQuery["status"] = False
                    return
                
                # Procedo a realizar el query
                if (parameters is None):
                    AppLog.debug(f"Execute '{query}'")
                    self._cursor.execute(query)

                else:
                    AppLog.debug(f"Execute '{query}' with parameters '{parameters}'")
                    self._cursor.execute(query, parameters)

                # Valido si devuelve algun query
                columns  = [description[0] for description in self._cursor.description]

                if (columns  is not None):
                    row = self._cursor.fetchone() 
                
                    while row:
                        list_row = list(row)

                        _dict = {}
                        for n in range(len(list_row)):
                            _dict[columns[n]] = list_row[n]

                        dataQuery["data"].append(_dict) 

                        row = self._cursor.fetchone()

                dataQuery["status"] = True 


        except sqlite3.Error as err:
            AppLog.error(err)
            dataQuery["msg"] = str(err)     
        
        except Exception as ex:
            AppLog.error(err, exc_info=True)     
            dataQuery["msg"] = str(err)   

        finally:
            self._disconnect()
            return dataQuery


