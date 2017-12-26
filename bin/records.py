"""
module for logging historical values of possesions
"""
import datetime


class RecordsLog(object):
    def __init__(self, location, include_date=True):
        self.location = location
        self.include_date = include_date

    def new_record(self, *records):
        try:
            historical_records = open(self.location, 'r').readlines()
            records_file = open(self.location, 'w')
            records_file.writelines(historical_records)
        except FileNotFoundError:
            records_file = open(self.location, 'w')
        if self.include_date:
            records_file.write('{}|{}\n'.format(datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),
                                                '|'.join([str(x) for x in records])))
        else:
            records_file.write('|'.join([str(x) for x in records]) + '\n')
        records_file.close()
        return records_file.closed

    def read_records(self, *names):
        records = open(self.location, 'r').readlines()
        record1, record2, record3 = [], [], []
        if self.include_date:
            dates = []
        for i in records[:len(records)]:
            i = i.split('|')
            if self.include_date:
                dates.append(i[0])
            record1.append(i[1])
            record2.append(i[2])
            record3.append(i[3][:len(i[3]) - 1])
        return {'dates': dates,
                names[0]: record1,
                names[1]: record2,
                names[2]: record3}
