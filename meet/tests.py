from django.test import TestCase
import time
import sqlite3

for _ in range(5):  # Try 5 times
    try:
        # your DB code here
        break
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            time.sleep(1)  # wait and retry
        else:
            raise
