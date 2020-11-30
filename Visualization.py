import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
#from sklearn.model_selection import train_test_split
#from sklearn import metrics
#%matplotlib inline
pd.options.display.float_format = "{:,.2f}".format

df = pd.read_csv('https://raw.githubusercontent.com/DivyanshSrivastava04/IDS-Project/main/Dataset.csv?token=ANPGBX7V2H3MCI4P55HSCAK7ZOPTM')

#no data for west bengal so we will drop the column of west bengal
del df['West Bengal1']

#now we need to handle missing value
#we will split database into two parts 

df_1 = df.iloc[:6,:]
df_2 = df.iloc[6:,:]

#appyling interpolation method to fill nan values in dataset1
df_1.interpolate(method='pchip' , limit_direction ='forward', inplace=True )

df_1

#now we need to do some computation to fill missing values in dataset2 with help of dataset1
for index in range(1, 6):
    #print(index)
    for col in df.columns[2:]:
        #print(col)
        
        n_today = df_1.iloc[index][col]
        n_yesterday = df_1.iloc[index-1][col]
        difference = n_today - n_yesterday
        percentage = (100 * difference ) / n_yesterday
        
        #print (percentage)
        df_2.loc[df.index[index+5], col] = percentage
        
df_2

for columnName in df_1.columns[2:]:
    df_1.plot.bar(y = columnName)
    
for columnName in df_2.columns[2:]:
    df_2.plot.line(y = columnName)
    
    
#simple compuatations 

#maximum growth of states 
for col in df_1.columns[2:]:
    maxi = df_1[col].max()
    maxi_per = df_2[col].max()
    #print(col,'max growth is {:0.2f}'.format(maxi), 'max % growth is {:0.2f}\n'.format(maxi_per))

NDPgrowth = []
    
#avg growth of states 
for col in df_1.columns[2:]:
    maxi = df_1[col].mean()
    maxi_per = df_2[col].mean()
    NDPgrowth.append((col, maxi_per))
    #print(col,'mean growth is {:0.2f}'.format(maxi), 'mean % growth is {:0.2f}\n'.format(maxi_per))

NDPgrowth.sort(key=lambda x: x[1])

x1 = [i[0] for i in NDPgrowth[5:]]
y1 = [i[1] for i in NDPgrowth[5:]]

x2 = [i[0] for i in NDPgrowth[-5:]]
y2 = [i[1] for i in NDPgrowth[-5:]]

plt.subplots(figsize=(6, 6))
plt.barh(x1, y1, color='red')

plt.barh(x2, y2, color='g')

#del df_1['Item Description']
#del df_1['All_India NDP']

#piechart of statewise contribution in NDP of India
fig, axes = plt.subplots(2, 3, figsize=(30, 20))

for i, (idx, row) in enumerate(df_1.set_index('Duration').iterrows()):
    ax = axes[i // 3, i % 3]
    row = row[row.gt(row.sum() * .01)]
    ax.pie(row, labels=row.index, startangle=30)
    ax.set_title(idx)

fig.subplots_adjust(wspace=.2)
