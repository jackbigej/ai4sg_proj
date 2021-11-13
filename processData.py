#!/usr/bin/bash python3

import sys
import csv

def import_data():
    with open('FallClassSchedule.csv', 'r') as f:
        csvreader = csv.reader(f)

        header = []
        header = next(csvreader)

        pd = {}

        for row in csvreader:
            if str(row[1].split(' ')[0]) == '1144':
                room = str(row[1].split(' ')[1])
                if room not in pd:
                    pd[room] = {}
                for l in str(row[5]):
                    if l not in pd[room]:
                        pd[room][l] = []
                    pd[room][l].append(str(str(row[6]) + ' - ' + str(row[7])))
                    pd[room][l].sort()

        print(pd)


def main():
    import_data()

if __name__ == '__main__':
    main()

