import pandas as pd
import datetime as dt

class BirthdaySelector:
    def __init__(self, csv_path: str):
        self.birthdays = pd.read_csv(csv_path)
        self.today = dt.datetime.now()

    def get_birthdays(self):
        return self.birthdays[
            (self.birthdays["month"] == self.today.month) &
            (self.birthdays["day"] == self.today.day)
        ]
