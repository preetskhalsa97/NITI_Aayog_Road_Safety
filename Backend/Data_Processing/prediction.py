import pandas as pd


data = pd.read_excel('Data/cleaned_data.xlsx')

df = data[['deviceCode_location_wardName', 'day']]


def counts(area_name , day_name ):


    if (area_name == 'All'):

        list_all = []
        df2 = df['deviceCode_location_wardName'].unique()
        for j in range(df['deviceCode_location_wardName'].nunique()):
            list_all.append(counts(df2[j] , day_name))

        return list_all


    i=0
    c=0
    numbers=[]
    print(area_name)
    print(day_name)


    while (df.iloc[i][0] != area_name):
        if (i <= 142417):
            i=i+1
        else:
            return []

    print(i)
    while( area_name == df.iloc[i][0] ):

        while(day_name != df.iloc[i][1]):
            if (i <= 142417):
                i=i+1
            else:
                return numbers

        while(day_name == df.iloc[i][1]):
            c=c+1

            if (i <= 142417):
                i=i+1
            else:
                numbers.append(c)
                return numbers

        numbers.append(c)
        c=0

    return numbers


single_list=[]
final_list=[]
moving_avg = 0

days ='Sunday Monday Tuesday Wednesday Thursday Friday Saturday'.split()

# for area_name in (df['deviceCode_location_wardName'].unique()):
#     for day_name in days :
#         single_list= counts(area_name, day_name)
#         area_list.append(single_list)
#     final_list.append(area_list)
#     area_list=[]



area_list = counts('Hagadur', 'Thursday')

print(area_list)

for c in area_list:
    moving_avg = .4*moving_avg + .6*c

print(moving_avg)

# print(counts('All', 'Thursday'))