import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df= pd.read_csv('movies.csv', lineterminator='\n')
print(df.head())

print(df.shape)

print(df.info())

print(df['Genre'].head())

print(df.duplicated().sum())

print(df.describe())


'''
. Exploration Summary

. we have a dataframe consisting of 9827 rows and 9 columns.
. our dataset looks a bit tidy with no NaNs nor duplicated values.
. Release_Date column needs to be casted into date time and to extract only the year value.
. Overyiew, Original_Languege and Poster-Url wouldn't be so useful during analysis, so we'll drop them.
. there is noticable outliers in Popularity column
. Vote_Average bettter be categorised for proper analysis.
. Genre column has comma saperated values and white spaces that needs to be handled and casted into category. Exploration Summary
'''


df['Release_Date']=pd.to_datetime(df['Release_Date'])

print(df['Release_Date'].dtypes)


# want only year so now.
df['Release_Date']=df['Release_Date'].dt.year

print(df['Release_Date'].dtypes)
print(df.head())


#removing unwanted column - not in use
cols=["Overview","Original_Language","Poster_Url"]

df.drop(cols,axis=1,inplace=True)
print(df.head())

'''
categorizing vote_average column by labelling values in 4 parts: 
popular, average, below_avg, not_popular
'''

def catigorize_col(df, col, labels):
    edges = [df[col].describe()['min'],
             df[col].describe()['25%'],
             df[col].describe()['50%'],
             df[col].describe()['75%'],
             df[col].describe()['max']]
    df[col] = pd.cut(df[col], edges , labels = labels, duplicates = 'drop')
    return df

labels=["popular", "average", "below_avg", "not_popular"]
catigorize_col(df,"Vote_Average", labels)
print(df["Vote_Average"].unique())

print(df["Vote_Average"].head())
print(df.head())

print(df["Vote_Average"].value_counts())

df.dropna(inplace=True)
print(df.isna().sum())

#splitting genres to have only one genre per row for each movie

df["Genre"]=df["Genre"].str.split(", ")
df=df.explode("Genre").reset_index(drop=True)
print(df.head())

print("-------------------")

#casting columns into category
df["Genre"]=df["Genre"].astype('category')
print(df["Genre"].dtypes)

print(df.info())

print(df.nunique())

print(df.head())


#DATA VISUALIZATION

sns.set_style("whitegrid")

#SOLUTION1
print(df["Genre"].describe())
sns. catplot(y = "Genre", data = df, kind = 'count',
             order = df["Genre"]. value_counts().index,
             color = 'green')
plt.title("Genre Column Distribution")
plt.show()

#SOLUTION2
sns.catplot(y = "Vote_Average",data = df,kind = 'count',
            order = df["Vote_Average"].value_counts().index,
            color = 'blue')
plt.title("Votes Distribution")
plt.show()

#SOLUTION3
print(df[df["Popularity"]==df["Popularity"].max()])

#SOLUTION4
print(df[df["Popularity"]==df["Popularity"].min()])

#SOLUTION5
df["Release_Date"].hist()
plt.title("Release_Date Column Distribution")
plt.show()


#CONCLUSION

#Q1) WHAT IS THE MOST FREQUENT GENRE OF MOVIES RELEASED ON NETFLIX.
#ANSWER---> DRAMA 

#Q2) WHICH HAS THE HIGHEST VOTES IN VOTES AVG COLUMN.
#ANSWER--> BELOW_AVERAGE

#Q3) WHAT MOVIE GOT THE HIGHEST POPULARITY? WHAT'S IT'S GENRE?
#ANSWER--> Spider-Man: No Way Home,(Action, Adventure,Science Fiction)

#Q4) WHAT MOVIE GOT THE LOWEST POPULARITY? WHAT'S IT'S GENRE?
#ANSWER-->The United States vs. Billie Holiday(Music,Drama,History)

#Q5) WHICH YEAR HAS THE MOST FILMMED MOVIES?
#ANSWER--> 2020


df.to_excel("movies_updated.xlsx", index=False)




