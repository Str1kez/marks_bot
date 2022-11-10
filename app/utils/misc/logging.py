import logging


logging.basicConfig(
    format="%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s",
    level=logging.INFO,
    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
)

exc_log = logging.getLogger("exception")
exc_log.setLevel(logging.ERROR)
exc_fh = logging.FileHandler("errors.log")
exc_formatter = logging.Formatter("%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s")
exc_fh.setFormatter(exc_formatter)
exc_log.addHandler(exc_fh)
