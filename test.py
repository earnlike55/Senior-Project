from time import time
from scipy.stats import expon
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
import warnings
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
from sklearn.metrics import f1_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import scale
import os.path
import json
import joblib
import pandas as pd
import numpy as np
from IPython import get_ipython
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def prepare_data(data, drop_na=True):
    ''' Drops unnecessary columns, Fill or Drop rows containing N/A, and pre-processes the columns.'''
    data = data.drop(columns=['Date', 'HomeTeam', 'AwayTeam'])
    data = data.drop(columns=['FTHG', 'FTAG'])
    data = data.drop(
        columns=['HT_goal_for', 'AT_goal_for', 'HT_goal_against', 'AT_goal_against'])
    # data = data.drop(columns=['HT_3_win_streak', 'HT_5_win_streak', 'HT_3_lose_Streak', 'HT_5_lose_Streak',
    #                          'AT_3_win_streak', 'AT_5_win_streak', 'AT_3_lose_Streak', 'AT_5_lose_Streak'])

    data = data.loc[data['HT_match_played'] == data['HT_match_played']]

    if drop_na:
        data = data.dropna()
    else:
        data.fillna(value=-99999, inplace=True)

    # Columns that are not normalized: (Ordinal, Categorical)
    # [FTR, HT_match_played, AT_match_played, HT_3_win_streak, HT_5_win_streak,
    # HT_3_lose_Streak, HT_5_lose_Streak, AT_3_win_streak, AT_5_win_streak, AT_3_lose_Streak, AT_5_lose_Streak]

    # Columns that are normalized: (Continuous variables)
    normalized_columns = ['HomeOVA', 'AwayOVA', 'OVA_diff']
    normalized_columns += ['HT_current_standing', 'AT_current_standing']
    normalized_columns += ['HT_goal_diff', 'HT_win_rate_season',
                           'AT_goal_diff', 'AT_win_rate_season']
    normalized_columns += ['HT_past_standing', 'HT_past_goal_diff', 'HT_past_win_rate',
                           'AT_past_standing', 'AT_past_goal_diff', 'AT_past_win_rate']
    normalized_columns += ['HT_5_win_rate', 'AT_5_win_rate',
                           'HT_win_rate_against', 'AT_win_rate_against']
    normalized_columns += ['current_standing_diff',
                           'win_rate_season_diff', 'goal_diff_diff']
    normalized_columns += ['past_standing_diff',
                           'past_goal_diff_diff', 'past_win_rate_diff']
    #normalized_columns += ['HT_goal_for', 'AT_goal_for', 'HT_goal_against', 'AT_goal_against']

    for column in normalized_columns:
        data[column] = scale(list(data[column]))
    return data








