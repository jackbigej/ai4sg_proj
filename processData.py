#!/usr/bin/bash python3

import sys
import csv

def parse_schedule():
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

        translated = {}

        for room in pd.keys():
            if room not in translated:
                translated[room] = {}
            for day in pd[room].keys():
                if day not in translated:
                    translated[room][day] = [0 for i in range(288)]

                for tp in pd[room][day]:
                    tp = tp.split(' - ')

                    start_end = {'start': {}, 'end':{}}
                    #Start Time
                    
                    if tp[0].split(' ')[1] == 'PM':
                        time = tp[0].split(' ')[0]
                        time = time.split(':')
                        if room == 'B011' and day == 'F':
                            print(time)
                        hour = int(time[0])
                        minute = int(time[1])
                        if hour != 12:
                            hour = hour + 12
                        start_end['start']['hour'] = hour
                        start_end['start']['min'] = minute

                        #print(hour, minute, tp[0].split(' ')[1])

                    else:
                        time = tp[0].split(' ')[0]
                        time = time.split(':')
                        if room == 'B011' and day == 'F':
                            print(time)
                        hour = int(time[0])
                        minute = int(time[1])
                        start_end['start']['hour'] = hour
                        start_end['start']['min'] = minute
                        #print(hour, minute, tp[0].split(' ')[1])


                    # End Time

                    if tp[1].split(' ')[1] == 'PM':
                        time = tp[1].split(' ')[0]
                        time = time.split(':')
                        if room == 'B011' and day == 'F':
                            print(time)
                        hour = int(time[0])
                        minute = int(time[1])
                        if hour != 12:
                            hour = hour + 12
                        start_end['end']['hour'] = hour
                        start_end['end']['min'] = minute
                        #print(hour, minute, tp[0].split(' ')[1])

                    else:
                        time = tp[1].split(' ')[0]
                        time = time.split(':')
                        if room == 'B011' and day == 'F':
                            print(time)
                        hour = int(time[0])
                        minute = int(time[1])
                        start_end['end']['hour'] = hour
                        start_end['end']['min'] = minute
                        #print(hour, minute, tp[0].split(' ')[1])

                    
                    
                    index_start = int((12*start_end['start']['hour']) + int((start_end['start']['min']/5)))
                    index_end = int((12*start_end['end']['hour']) + int((start_end['end']['min']/5)))

                    if room == 'B011' and day == 'F':
                        print(start_end)
                        print('Start:', index_start, 'End:', index_end)
                    for i in range(index_start, index_end + 1):
                        translated[room][day][i] = 1
                    #print(len(translated[room][day]))

        print(pd['B011']['F'])
        print(translated)


def parse_occupancy():
    pass


def main():
    parse_schedule()

if __name__ == '__main__':
    main()

