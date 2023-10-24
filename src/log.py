import logging, os
from logging import handlers


class log(logging.getLoggerClass()):
    def __init__(self, name: str, level: int = logging.NOTSET) -> None:
        super().__init__(name, level)

        # Creo el stream
        stramHandler = logging.StreamHandler()
        formatter = logging.Formatter(
                '%(asctime)s [%(levelname)-8s] Line %(lineno)-4s of %(filename)-20s: %(message)s')
        
        stramHandler.setFormatter(formatter)
        self.addHandler(stramHandler)

        # Creo el FileHandler
        folder = "log"

        if (not os.path.exists(folder)):
            os.mkdir(folder)

        fh = handlers.RotatingFileHandler(f"{folder}/app.log", maxBytes=(10485760*5), backupCount=5)
        fh.setFormatter(formatter)
        self.addHandler(fh)

        # Seteo el Level
        self.setLevel(level)
