import datetime as dt
import logging

log = logging.basicConfig(filename=f"../logging_/{dt.date.today()}.txt",
                          level=logging.INFO, filemode="w", encoding="utf-8")
