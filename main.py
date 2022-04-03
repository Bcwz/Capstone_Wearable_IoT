from datetime import datetime
import time
from Database.mongodb import mongoDatabase


while True:
    dateNow = datetime.now()
    mongoDatabase.insertDatabase(dateNow)
    time.sleep(5)
    