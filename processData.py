#!/usr/bin/bash python3

import datetime
import sys
import csv
import os
import json

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
                        hour = int(time[0])
                        minute = int(time[1])
                        if hour != 12:
                            hour = hour + 12
                        start_end['start']['hour'] = hour
                        start_end['start']['min'] = minute

                    else:
                        time = tp[0].split(' ')[0]
                        time = time.split(':')
                        hour = int(time[0])
                        minute = int(time[1])
                        start_end['start']['hour'] = hour
                        start_end['start']['min'] = minute

                    # End Time

                    if tp[1].split(' ')[1] == 'PM':
                        time = tp[1].split(' ')[0]
                        time = time.split(':')
                        hour = int(time[0])
                        minute = int(time[1])
                        if hour != 12:
                            hour = hour + 12
                        start_end['end']['hour'] = hour
                        start_end['end']['min'] = minute

                    else:
                        time = tp[1].split(' ')[0]
                        time = time.split(':')
                        hour = int(time[0])
                        minute = int(time[1])
                        start_end['end']['hour'] = hour
                        start_end['end']['min'] = minute
                    
                    index_start = int((12*start_end['start']['hour']) + int((start_end['start']['min']/5)))
                    index_end = int((12*start_end['end']['hour']) + int((start_end['end']['min']/5)))

                    for i in range(index_start, index_end + 1):
                        translated[room][day][i] = 1
    return translated


def parse_occupancy():
    occ = {}
    lights = {}

    with open("LightRoomKey.csv") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            lights[row[0]] = row[1]

    for filename in os.listdir("occupancy_csv"):
        filename = filename.split(".")[0]
        if filename in lights:
            with open(os.path.join("occupancy_csv", filename + ".csv"), 'r') as f:
                csvreader = csv.reader(f)
                header = []
                header = next(csvreader)
                if filename not in occ:
                    occ[lights[filename]] = {}
                
                for row in csvreader:
                    row_data = {}
                    date = row[0].split(' ')[0]
                    new_date = date.split('/')
                    start_date = datetime.date(2021, 8, 23)
                    current_date = datetime.date(int(new_date[2]), int(new_date[0]), int(new_date[1]))
                    weekday = current_date.weekday()
                    if current_date < start_date:
                        continue
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
                    if day not in occ[lights[filename]]:
                        occ[lights[filename]][day] = []
                    
                    occ[lights[filename]][day].append(row_data)
                               
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
        
    return translated

def compare(schedule, occ):
    compared = {}
    averages = {}

    with open("LightRoomKey.csv") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            room = row[1]
            if room == "205" or room == "214" or room == "149": # 205 has too little data, 214 is empty file, 346 and 349 have no classes
                continue
            if room not in compared:
                compared[room] = {}
                averages[room] = {}
            for weekday in schedule[room].keys():
                if weekday not in compared[room]:
                    compared[room][weekday] = {}
                    averages[room][weekday] = [0 for i in range(288)]
                if weekday != "U": # room 143 has a class on Sunday's, should we try and incorporate Sunday's or ignore this instance
                    total_weekdays = len(occ[room][weekday].keys())
                    for date in occ[room][weekday].keys():
                        if date not in compared[room][weekday]:
                            compared[room][weekday][date] = [0 for i in range(288)]
                        for i in range(288):
                            averages[room][weekday][i] += occ[room][weekday][date][i]
                            if schedule[room][weekday][i] == 0 and occ[room][weekday][date][i] == 1:
                                compared[room][weekday][date][i] = 1
                    
                    for i in range(288):
                        averages[room][weekday][i] = averages[room][weekday][i]/total_weekdays
                        
    return [compared, averages]

def percentages(compared):
    percentages = {}
    
    with open("LightRoomKey.csv") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            room = row[1]
            sum = 0
            dateCount = 0
            if room == "205" or room == "214" or room == "149": # 205 has too little data, 214 is empty file, 346 and 349 have no classes
                continue
            if room not in percentages:
                percentages[room] = 0
            for weekday in compared[room].keys():
                if weekday != "U": # room 143 has a class on Sunday's, should we try and incorporate Sunday's or ignore this instance
                    for date in compared[room][weekday].keys():
                        for i in range(288):
                            sum += compared[room][weekday][date][i]
                            dateCount += 1
                    
            percentages[room] = sum / dateCount
    return percentages

def main():
    schedule = parse_schedule()
    with open("schedule.json", "w+") as f:
        f.write(json.dumps(schedule))
    occ = parse_occupancy()
    with open("occ.json", "w+") as f:
        f.write(json.dumps(occ))
    [compared, averages] = compare(schedule, occ)
    with open("compared.json", "w+") as f:
        f.write(json.dumps(compared))
    with open("averages.json", "w+") as f:
        f.write(json.dumps(averages))
    p = percentages(compared)
    with open("percentages.json", "w+") as f:
        f.write(json.dumps(p))
    with open("143_averages.json", "w+") as f:
        f.write(json.dumps(averages['143']))
    with open("143_schedule.json", "w+") as f:
        f.write(json.dumps(schedule['143']))

if __name__ == '__main__':
    main()

