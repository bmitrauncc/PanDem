
from pathlib import Path
from typing import Set
import time
import csv
from operator import add

source_dir = Path('nssac-ncov-data-country-state/')

def processFiles(name):
    files = source_dir.glob('*.csv')  # check ext
    for file in files:
        with open(file, 'r') as readFile:
           for line in readFile:
               if name == line.split(',')[0]:  # check unique regions
                   yield (line.rstrip('\n'))



def writeCsvStats(stats, csvName, header = None):
    # use index for non epoch stamped values
    with open(csvName+'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for key in sorted(stats.keys()):
            writer.writerow(stats[key])



def cityStats(cityName):
    # creates csv func:2

    setTime: Set[int] = set()
    dictStats = {}
    # nameFiler = processFiles(cityName)
    for line in processFiles(cityName):
        listLine = line.split(',')
        date_time = listLine[2].split(" ")[0]  # to extract date from dateTime value
        pattern = '%Y-%m-%d'
        epoch = int(time.mktime(time.strptime(date_time, pattern))) 

        if epoch not in setTime:    #only unique dates 
            setTime.add(epoch)
            dictStats[epoch] = listLine[2:]
    header = ["Date", "Confirmed", "Deaths", "Recovered"]
    csvName = cityName+"CityStats"
    writeCsvStats(dictStats, csvName, header)
    


def allCityStats(cityName):
    dictStats = {}
    counterKey = 0
    # nameFiler = processFiles(cityName)
    for line in processFiles(cityName):
        # print (line)
        counterKey += 1
        listLine = line.split(',')
        # date_time = listLine[2].split(" ")
        # pattern = "%Y-%m-%d %h:%m:%s"
        # epoch = int(time.mktime(time.strptime(date_time, pattern)))     #maintian order of dateTime in csv
        dictStats[counterKey] = listLine[2:]
    # todo: :( order
    header = ["Date", "Confirmed", "Deaths", "Recovered"]
    csvName = cityName + "AllCityStats"
    writeCsvStats(dictStats, csvName, header)

def regionStats(regionName):
    # todo: move to processFiles
    dictStats = {}

    files = source_dir.glob('*.csv')  # check ext
    for file in files:

        with open(file, 'r') as readFile:
            # readFile.seek(0)
            sumStats = [0, 0, 0]
            lastTime = 0
            for line in readFile:
                listLine = line.split(',')
                if regionName == listLine[1]:  # check unique regions
                    stat =  map(int, (line.rstrip('\n').split(','))[3:])  #forming list of last 3 cols as ints
                    sumStats = list(map(add, sumStats, stat))

                    date_time = listLine[2].split(" ")[0]  # to extract date from dateTime value
                    pattern = '%Y-%m-%d'
                    epoch = int(time.mktime(time.strptime(date_time, pattern)))
                    if epoch > lastTime:
                        lastTime = listLine[2]
            sumStats.insert(0, lastTime)
            sumStats.insert(0, str(file)[-14:])
            dictStats[str(file)[-14:]] = sumStats
    header = ["Date", "Confirmed", "Deaths", "Recovered"]
    csvName = regionName + "RegionStats"
    writeCsvStats(dictStats, csvName, header)

#test
cityStats('India')
allCityStats('India')
regionStats('India')





