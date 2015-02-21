""" Extract everything from the Koku SQL lite DB
"""

import sqlite3
import csv
import argparse
from datetime import (datetime, timedelta)

__author__ = 'peter@phyn3t.com'

sql = '''
select a.Z_PK, a.ZDATE, a.ZDEPOSIT, a.ZWITHDRAWAL, a.ZINFO, c.ZNAME
from ZFRTRANSACTION as a
LEFT JOIN Z_11TRANSACTIONS as b on a.Z_PK=b.Z_12TRANSACTIONS1
LEFT JOIN ZFRTAG as c on c.Z_PK=b.Z_11TAGS
'''

class Koku(object):
    """ Contains a single entry in a koku database
    """

    apple_time = datetime(2001, 1, 1)

    def __init__(self, row):
        self.date = self.get_date(row[1])
        self.value = self.get_value(row[2], row[3])
        self.description = row[4] if not row[4] is None else 'Unknown'
        self.category = row[5] if not row[5] is None else 'Unknown'

    def get_value(self, deposit, withdraw):
        """ Determine our transaction value
        """

        if deposit is not None and deposit != 0:
            return deposit
        return "-{}".format(withdraw)

    def to_csv(self):
        """ return list for csv module
        """

        return [self.date, self.value, self.description, self.category]

    def get_date(self, sec=None):
        """ return the transaction date
        """

        date = self.apple_time + timedelta(seconds=sec)

        return "{}-{}-{}".format(date.day, date.month, date.year)


def main():
    """ main duuu
    """

    parser = argparse.ArgumentParser(description='Convert Koku DB to csv')
    parser.add_argument('--database', help='Koku sqlite database path',
                        required=True)
    parser.add_argument('--output', help='Output csv file path',
                        required=True)
    args = parser.parse_args()

    conn = sqlite3.connect(args.database)
    cur = conn.cursor()
    cur.execute(sql)

    with open(args.output, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in cur:
            csvwriter.writerow(Koku(row).to_csv())


if __name__ == '__main__':
    main()
