
#modules used in this linear regression 
import pandas as pd 
import math 
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from scipy import linalg

#saving rating data as dataframe.
ratings_in_moviedata = pd.read_csv('./Yahoo-movie-data/data_movies.txt',sep="\t",names=['userid','criteria1','criteria2','criteria3','criteria4','overall','movieid','num'])
print(max(ratings_in_moviedata.overall))

