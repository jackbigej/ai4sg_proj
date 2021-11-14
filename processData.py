#!/usr/bin/bash python3

import datetime
import sys
import csv
import os

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

                    else:
                        time = tp[0].split(' ')[0]
                        time = time.split(':')
                        if room == 'B011' and day == 'F':
                            print(time)
                        hour = int(time[0])
                        minute = int(time[1])
                        start_end['start']['hour'] = hour
                        start_end['start']['min'] = minute

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

                    else:
                        time = tp[1].split(' ')[0]
                        time = time.split(':')
                        if room == 'B011' and day == 'F':
                            print(time)
                        hour = int(time[0])
                        minute = int(time[1])
                        start_end['end']['hour'] = hour
                        start_end['end']['min'] = minute
                    
                    index_start = int((12*start_end['start']['hour']) + int((start_end['start']['min']/5)))
                    index_end = int((12*start_end['end']['hour']) + int((start_end['end']['min']/5)))

                    if room == 'B011' and day == 'F':
                        print(start_end)
                        print('Start:', index_start, 'End:', index_end)
                    for i in range(index_start, index_end + 1):
                        translated[room][day][i] = 1


def parse_occupancy():
    occ = {}

    for filename in os.listdir("occupancy_csv"):
        with open(os.path.join("occupancy_csv", filename), 'r') as f:
            csvreader = csv.reader(f)
            header = []
            header = next(csvreader)
            if filename not in occ:
                occ[filename] = {}
            
            for row in csvreader:
                row_data = {}
                date = row[0].split(' ')[0]
                new_date = date.split('/')
                weekday = datetime.date(int(new_date[2]), int(new_date[0]), int(new_date[1])).weekday()
                if weekday == 0:
                    day = 'M'
                elif weekday == 1:
                    day = 'T'
                elif weekday == 2:
                    day = 'W'
                elif weekday == 3:
                    day = 'R'
                elif weekday == 4:
                    day = 'F'
                else:
                    continue
                
                row_data['date'] = date
                time = row[0].split(' ')[1]
                row_data['time'] = time
                occupied = row[1]
                row_data['occupied'] = occupied
                if day not in occ[filename]:
                    occ[filename][day] = []
                
                occ[filename][day].append(row_data)
                               
    translated = {}

    for room in occ.keys():
        if room not in translated:
            translated[room] = {}
        for day in occ[room].keys():
            if day not in translated[room]:
                translated[room][day] = {}
            for date_dict in occ[room][day]:
                if date_dict['date'] not in translated[room][day]:
                    translated[room][day][date_dict['date']] = [0 for i in range(288)]
                    
                # Occupancy at 00:00 will be the same for 00:05, 00:10
                time = date_dict['time']
                time = time.split(':')
                hour = int(time[0])
                minute = int(time[1])
                index_start = int((12*hour) + int(minute)/5)
                occupied = date_dict['occupied']
                if occupied == '':
                    occupied = 0
                translated[room][day][date_dict['date']][index_start] = int(occupied)
                translated[room][day][date_dict['date']][index_start + 1] = int(occupied)
                translated[room][day][date_dict['date']][index_start + 2] = int(occupied)
        

    print('printing translated')
    print(translated)
    #print(translated['VAV_1027A.csv']['R']['10/21/2021'])        

def main():
    parse_schedule()
    parse_occupancy()

if __name__ == '__main__':
    main()

