import csv
import sys

tsv_file = sys.argv[1]
csv_file = r"parks.csv"

with open(tsv_file, "r") as fin:
    datain = csv.reader(fin, delimiter = '\t')
    with open(csv_file, "w") as fout:
        dataout = csv.writer(fout)
        for row in datain :
            dataout.writerow(row)

csvFile = 'parks.csv'
xmlFile = sys.argv[2]

csv_Data = csv.reader(open(csvFile))
xmlData = open(xmlFile, 'w')
xmlData.write('<?xml version="1.0"?>' + "\n")
xmlData.write('<parks>' + "\n")
nrow = 0
for row in csv_Data:
    if nrow == 0:
        tags = row
        for i in range(len(tags)):
            tags[i] = tags[i].replace(' ', '_')
    else:
        xmlData.write('<park>' + "\n")
        for i in range(len(tags)):
            xmlData.write('    ' + '<' + tags[i] + '>'+ row[i] + '</' + tags[i] + '>' + "\n")
        xmlData.write('</park>' + "\n")
    nrow += 1

xmlData.write('</parks>' + "\n")
xmlData.close()