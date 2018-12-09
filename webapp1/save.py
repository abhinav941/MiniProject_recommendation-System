import pandas as pd
df = pd.read_csv('new_movie.csv',names=['id','language','name','content','image','date','status','rating','vote_count','genre1'])
df.drop(['id'],axis=1,inplace=True)
for _ in range(191):
    x=int(input())
    df.drop(df.index[x],inplace=True)

df.to_csv('new_movie.csv')


