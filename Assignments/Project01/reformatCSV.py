#DESCRIPTION:
#In this file NULL values were saved as \n
#this created errors when trying to copy over data so this is a quick and easy script to convert the original data
#into something that wouldn't error by turning all NULL values which were labeled as literally: \n
#into blanks

import csv

x = 0

#opens up the original csv file 'airportscopy.csv
#and then we open and create a newAirports.csv that will hold the new edited values without the "\N"'s
with open('/Users/parkerhagmaier/Desktop/AAAA/airportscopy.csv','r') as csvinput:
    with open('/Users/parkerhagmaier/Desktop/AAAA/newAirports.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        all = []
        row = next(reader)
        all.append(row)

        for row in reader:
            row.append(x)
            all.append(row)
            x+=1
        count = 0
        for i in range(len(all)):
            for x in range(13):
                if all[i][x] == '\\N':
                    all[i][x] = ''
                    if count < 5:
                        print('True')
                        count +=1
#print(all[6983])
        writer.writerows(all)
