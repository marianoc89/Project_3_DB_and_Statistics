import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium import webdriver
import undetected_chromedriver as uc
from datetime import date
import random
import locale
import time
from datetime import datetime
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pymysql
import sqlalchemy as alch
from getpass import getpass
from scipy.stats import poisson
from scipy.stats import norm

def all_matches (df_a_his, df_b_his, df_c_his, df_d_his, df_e_his, df_f_his, df_g_his, df_h_his, df_i_his, df_j_his, df_k_his, df_l_his, df_m_his):
    #This function will pass all the different df created previously to combine them all into 1 dataset containing all the historical matches data
    df_match_1 = df_a_his['Match'].str.extract('(\D+) (\d+-\d+) (\D+) (\d+ \w+,\s\d{4})', expand=True)
    df_match_1['League'] = df_a_his['League']
    df_match_1.columns = ['Home', 'Resultado', 'Away', 'Fecha', 'League']
    df_match_1['Match Number'] = pd.Series(["1" for x in range(len(df_match_1.index))])

    df_match_2 = df_e_his['Match'].str.extract('(\D+) (\d+-\d+) (\D+) (\d+ \w+,\s\d{4})', expand=True)
    df_match_2['League'] = df_e_his['League']
    df_match_2.columns = ['Home', 'Resultado', 'Away', 'Fecha', 'League']
    df_match_2['Match Number'] = pd.Series(["2" for x in range(len(df_match_2.index))])

    df_match_3 = df_f_his['Match'].str.extract('(\D+) (\d+-\d+) (\D+) (\d+ \w+,\s\d{4})', expand=True)
    df_match_3['League'] = df_f_his['League']
    df_match_3.columns = ['Home', 'Resultado', 'Away', 'Fecha', 'League']
    df_match_3['Match Number'] = pd.Series(["3" for x in range(len(df_match_3.index))])

    df_match_4 = df_g_his['Match'].str.extract('(\D+) (\d+-\d+) (\D+) (\d+ \w+,\s\d{4})', expand=True)
    df_match_4['League'] = df_g_his['League']
    df_match_4.columns = ['Home', 'Resultado', 'Away', 'Fecha', 'League']
    df_match_4['Match Number'] = pd.Series(["4" for x in range(len(df_match_4.index))])

    df_match_5 = df_b_his['Match'].str.extract('(\D+) (\d+-\d+) (\D+) (\d+ \w+,\s\d{4})', expand=True)
    df_match_5['League'] = df_b_his['League']
    df_match_5.columns = ['Home', 'Resultado', 'Away', 'Fecha', 'League']
    df_match_5['Match Number'] = pd.Series(["5" for x in range(len(df_match_5.index))])

    df_match_6 = df_c_his['Match'].str.extract('(\D+) (\d+-\d+) (\D+) (\d+ \w+,\s\d{4})', expand=True)
    df_match_6['League'] = df_c_his['League']
    df_match_6.columns = ['Home', 'Resultado', 'Away', 'Fecha', 'League']
    df_match_6['Match Number'] = pd.Series(["6" for x in range(len(df_match_6.index))])

    df_match_7 = df_d_his['Match'].str.extract('(\D+) (\d+-\d+) (\D+) (\d+ \w+,\s\d{4})', expand=True)
    df_match_7['League'] = df_d_his['League']
    df_match_7.columns = ['Home', 'Resultado', 'Away', 'Fecha', 'League']
    df_match_7['Match Number'] = pd.Series(["7" for x in range(len(df_match_7.index))])

    df_match_8 = df_i_his['Match'].str.extract('(\D+) (\d+-\d+) (\D+) (\d+ \w+,\s\d{4})', expand=True)
    df_match_8['League'] = df_i_his['League']
    df_match_8.columns = ['Home', 'Resultado', 'Away', 'Fecha', 'League']
    df_match_8['Match Number'] = pd.Series(["8" for x in range(len(df_match_8.index))])

    df_match_9 = df_j_his['Match'].str.extract('(\D+) (\d+-\d+) (\D+) (\d+ \w+,\s\d{4})', expand=True)
    df_match_9['League'] = df_j_his['League']
    df_match_9.columns = ['Home', 'Resultado', 'Away', 'Fecha', 'League']
    df_match_9['Match Number'] = pd.Series(["9" for x in range(len(df_match_9.index))])

    df_match_10 = df_h_his['Match'].str.extract('(\D+) (\d+-\d+) (\D+) (\d+ \w+,\s\d{4})', expand=True)
    df_match_10['League'] = df_h_his['League']
    df_match_10.columns = ['Home', 'Resultado', 'Away', 'Fecha', 'League']
    df_match_10['Match Number'] = pd.Series(["10" for x in range(len(df_match_10.index))])

    df_match_11 = df_k_his['Match'].str.extract('(\D+) (\d+-\d+) (\D+) (\d+ \w+,\s\d{4})', expand=True)
    df_match_11['League'] = df_k_his['League']
    df_match_11.columns = ['Home', 'Resultado', 'Away', 'Fecha', 'League']
    df_match_11['Match Number'] = pd.Series(["11" for x in range(len(df_match_11.index))])

    df_match_12 = df_l_his['Match'].str.extract('(\D+) (\d+-\d+) (\D+) (\d+ \w+,\s\d{4})', expand=True)
    df_match_12['League'] = df_l_his['League']
    df_match_12.columns = ['Home', 'Resultado', 'Away', 'Fecha', 'League']
    df_match_12['Match Number'] = pd.Series(["12" for x in range(len(df_match_12.index))])

    df_match_13 = df_m_his['Match'].str.extract('(\D+) (\d+-\d+) (\D+) (\d+ \w+,\s\d{4})', expand=True)
    df_match_13['League'] = df_m_his['League']
    df_match_13.columns = ['Home', 'Resultado', 'Away', 'Fecha', 'League']
    df_match_13['Match Number'] = pd.Series(["13" for x in range(len(df_match_13.index))])

    def river_res(row):
        """Description: 
            This function determines the result of each match for River Plate based on the 'Resultado' and 'Home' columns.
            Arguments:
                row: A row from the DataFrame.
            Returns: 
                1 if River Plate won the match, 0 if it was a draw, or -1 if they lost.
        """
        resultado = row['Resultado'].split('-')
        home = row['Home']
        away = row['Away']
        
        if int(resultado[0]) > int(resultado[1]):
            if home == 'River Plate':
                return 'Victoria'
            elif away == 'River Plate':
                return 'Derrota'
        elif int(resultado[0]) < int(resultado[1]):
            if home == 'River Plate':
                return 'Derrota'
            elif away == 'River Plate':
                return 'Victoria'
        else:
            return 'Empate'
    
    #Concatenating all Df from each match into 1 and only df fro the historical matches and results
    df_all_matches = pd.concat([df_match_1, df_match_2, df_match_3,df_match_4, df_match_5, df_match_6, df_match_7,
                                df_match_8,df_match_9,df_match_10, df_match_11, df_match_12, df_match_13])
    
    df_all_matches['River_Resultado'] = df_all_matches.apply(lambda row: river_res(row), axis=1)
    #Replacing spanish months to english to stablish datetime dtype to all values
    month_dict = {'Ene': 'Jan', 'Feb': 'Feb', 'Mar': 'Mar', 'Abr': 'Apr', 'May': 'May', 'Jun': 'Jun',
                'Jul': 'Jul', 'Ago': 'Aug', 'Sep': 'Sep', 'Oct': 'Oct', 'Nov': 'Nov', 'Dic': 'Dec'}

    df_all_matches['Fecha'] = pd.to_datetime(df_all_matches['Fecha'].str.replace(r'(\d+ \w{3},) (\d{4})', r'\1\2', regex=True)
                                            .apply(lambda x: re.sub(r'\b\w{3}\b', lambda m: month_dict[m.group()], x)))
    df_all_matches['Match Number'] = df_all_matches['Match Number'].astype(int)
    return df_all_matches

def data_save(df, df_2, df_all_matches, df_arq, df_campo):
    """Description: 
                This function saves all 5 df in 5 different csv files.
        arguments:
            df: results table cleaned.
            df_2: table of the upcoming matches.
            df_all_matches: table with the data of all the historical matches for the upcoming games.
            df_arq: table with River Plate's goal keepers data
            df_campo: table with River Plate's field players data
        return: 
            5 final csv DataFrame with the cleaned data and the date of the creation at the end.
    """
    today = str(pd.to_datetime('today'))[:10].replace('-','')
    df.to_csv(f"C:/Users/maria/Desktop/Projects/Project_3_DB_and_Statistics/data/league_results_table_{today}.csv",encoding='ISO-8859-1', index=False)
    df_2.to_csv(f"C:/Users/maria/Desktop/Projects/Project_3_DB_and_Statistics/data/upcoming_matches_{today}.csv",encoding='ISO-8859-1', index=False)
    df_all_matches.to_csv(f"C:/Users/maria/Desktop/Projects/Project_3_DB_and_Statistics/data/historical_upcoming_{today}.csv",encoding='ISO-8859-1', index=False)
    df_arq.to_csv(f"C:/Users/maria/Desktop/Projects/Project_3_DB_and_Statistics/data/goal_keepers{today}.csv",encoding='ISO-8859-1', index=False)
    df_campo.to_csv(f"C:/Users/maria/Desktop/Projects/Project_3_DB_and_Statistics/data/field_players_{today}.csv",encoding='ISO-8859-1', index=False)
    return 'Files saved in folder'