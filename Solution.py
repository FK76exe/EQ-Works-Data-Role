import pandas
import math
pandas.set_option('display.max_columns',None)

df = pandas.read_csv("data/DataSample.csv")

#QUESTION 1: CLEANUP DATA WITH IDENTICAL TIMESTAMP + GEOINFO

freq = df[' TimeSt'].value_counts()
indices = freq.index

def findFreq(row):
    return freq.loc[ row[' TimeSt'] ]

df['Freq'] = df.apply(lambda row: findFreq(row),axis = 1)
df = df[ df['Freq'] == 1 ]

df = df.drop(columns=['Freq'])
print(df)

print('-----------------------------------------------------')

#QUESTION 2: FIND CLOSEST POI FOR EACH REQUEST

poi = pandas.read_csv("data/POIList.csv")
names = list(poi['POIID'])
latitudes = list(poi[' Latitude'])
longitudes = list(poi['Longitude'])

def closest(row):
    x,y = row['Latitude'],row['Longitude']
    closestPOI = None
    closestDistance = None
    for z in range(len(names)):
        distance = math.sqrt( (x-latitudes[z])**2 + (y-longitudes[z])**2 )
        if closestDistance == None or distance < closestDistance:
            closestDistance = distance
            closestPOI = z
    return  [names[closestPOI],closestDistance]

df['closestPOI']= df.apply(lambda row: closest(row)[0],axis = 1)
df['POIdistance']= df.apply(lambda row: closest(row)[1],axis = 1)
print(df)

print('-----------------------------------------------------')

#QUESTION 3.1: AVERAGE/STD DEV OF DISTANCE B/W POI AND REQUEST

def std_dev(row,avg):
    return (row['POIdistance'] - avg)**2

POIs = df['closestPOI'].unique()
for P in POIs:
    print("Average Request Distance from {}: ".format(P),end=' ')
    x = df[ df['closestPOI'] == P ].copy()
    average = sum(x['POIdistance']) / len(x['POIdistance'])
    print(average)

    print("Standard Deviation of Request Distance from {}: ".format(P),end=' ')
    x['Dist-Avg Squared'] = x.apply(lambda row: std_dev(row,average),axis=1)
    stdDev = (sum(x['Dist-Avg Squared']) / len(x['POIdistance']))**0.5
    print(stdDev)

print('-----------------------------------------------------')

#QUESTION 3.2: AVERAGE/STD DEV OF DISTANCE B/W POI AND REQUEST
densities = []
for P in POIs:
    x = df[ df['closestPOI'] == P ]
    radius = max(x['POIdistance'])
    area = math.pi * (radius ** 2)
    densities.append([P,len(x)/area])
    print('Radius of {}: {}\nDensity of {} (requests/area): {}'.format(P,radius,P,len(x)/area))
    

print('-----------------------------------------------------')

#QUESTION 4A: MAP ON A SCALE OF -10 to 10

nums = [p[1] for p in densities]
avg = sum(nums) / len(nums) #acts as 0
rng = max(  abs(max(nums)-avg), abs(min(nums)-avg)  )

coeff = rng/10
print(coeff)
for P in densities:
    print("{} popularity from -10 -> 10: {}".format(P[0],(P[1]-avg)/coeff))

