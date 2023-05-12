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

def argentina_table ():
    driver = webdriver.Chrome()
    url = "https://www.google.com/search?q=river+plate&oq=river+plate&aqs=chrome.0.0i271j46i39j46i175i199i512j0i512l2j69i60j69i65l2.1209j1j7&sourceid=chrome&ie=UTF-8#sie=t;/m/037d7f;2;/m/04hpk1;st;fp;1;;;"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    driver.find_element('xpath','//*[@id="W0wltc"]/div').click()
    #Si no abre la seccion de clasificacion directamente, hay que ejecutar esto para que seleccione la pestaña:
    #driver.find_element('xpath','//*[@id="sports-app"]/div/div[2]/div/div/div/ol/li[3]').click()
    data = driver.find_element('xpath','//*[@id="liveresults-sports-immersive__team-fullpage"]/div/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div/div[2]/div/table').text
    # Create a table containing the data and split it by '\n'
    table = np.array(data.split('\n'))
    #Defining which are the columns and then choosing and creating custom names for each column
    table[0:20] #columnas
    columns = ['Rank', 'Club', 'Partidos jugados', 'Victorias', 
        'Empates', 'Derrotas', 'Goles marcados', 
        'Goles en contra', 'Diferencia de goles', 'Puntos',
        'Ultimo partido', 'Ultimo partido -1', 'Ultimo partido -2', 'Ultimo partido -3', 'Ultimo partido -4']
    #Defining which are going to be the rows to be used
    rows = table[21:]
    #Create a Df from rows list which is split into 28 sublists with 8 items each list
    df = pd.DataFrame([rows[i:i+8] for i in range(0, len(rows), 8)])
    #Splitting column 2 that had all the numbers combined
    df[[2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7]] = df[2].str.split(' ', expand=True)
    #Ordering the columns properly
    df = df[[0.0,1.0,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,3.0,4.0,5.0,6.0,7.0]]
    #assigning final columns to the DF
    df.columns = columns

    cols_res= ['Rank','Partidos jugados', 'Victorias', 
        'Empates', 'Derrotas', 'Goles marcados', 
        'Goles en contra', 'Diferencia de goles', 'Puntos',]
    for i in cols_res:
        df[i] = df[i].astype(int)

    #Este DF contiene la informacion estadistica de los ultimos partidos de la "Primera Divison Argentina Teporada 2023" 
    # - Ultima fecha corrida: 5.03.23 (8pm)
    return df

def upcoming_matches ():
    driver2 = webdriver.Chrome()
    url2 = "https://www.espn.com.ar/futbol/equipo/calendario/_/id/16/liga/ARG.1"
    driver2.get(url2)
    html2 = driver2.page_source
    soup2 = BeautifulSoup(html2, 'lxml')
    driver2.find_element('xpath','//*[@id="onetrust-accept-btn-handler"]').click()
    #Solo 3 letras ya que hay 3 tablas unicamente, 1 por mes (Mayo, Junio, Julio)
    a = driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section/div/section/div[3]/div[1]').text
    b = driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section/div/section/div[3]/div[2]').text
    c = driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section/div/section/div[3]/div[3]').text
    #Puting the data scraped into diferent lists to then return a DF
    row_a = a.split('\n')[2:]
    row_a = [row_a[i:i+5] for i in range(0, len(row_a), 5)]
    row_b = b.split('\n')[2:]
    row_b = [row_b[i:i+5] for i in range(0, len(row_b), 5)]
    row_c = c.split('\n')[2:]
    row_c = [row_c[i:i+5] for i in range(0, len(row_c), 5)]
    #appending all data to a single table with the upcoming matches for River Plate
    table_calendar = []
    for i in row_a:
        table_calendar.append(i)
    for i in row_b:
        table_calendar.append(i)
    for i in row_c:
        table_calendar.append(i)
    #Creating DF with the information from the table
    df_2 = pd.DataFrame(table_calendar, columns=['Fecha','Home','vs','Away', 'Time - League'])
    #Adding a match number for index purpuses and table references
    df_2['Match Number'] = (df_2.index+1)
    #Replace Fecha format to a better one with year
    df_2['Fecha'] = df_2['Fecha'].str[6:]+' 2023'
    #Changing the data type to DateTime format
    df_2['Fecha'] = pd.to_datetime(df_2['Fecha'], format='%d de %b. %Y')
    return df_2

def historical_matches ():
    driver2 = webdriver.Chrome()
    url2 = "https://www.espn.com.ar/futbol/equipo/calendario/_/id/16/liga/ARG.1"
    driver2.get(url2)
    html2 = driver2.page_source
    soup2 = BeautifulSoup(html2, 'lxml')
    driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/section/div/section/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr/td[3]/span/a[2]').click()
    #Esta funcion entra al 1er partido de la 1er tabla y trae los ultimos resultados de estos equipos
    a_his = driver2.find_element('xpath','//*[@id="gamepackage-team-form-away"]/div/div').text
    row_a_his = a_his.split('\n')[1:]
    row_a_his = [row_a_his[i:i+2] for i in range(0, len(row_a_his), 2)]
    df_a_his = pd.DataFrame(row_a_his, columns=['Match','League'])
    driver2.execute_script("window.history.go(-1)")
    #Esta funcion entra al 2do partido de la 1er tabla y trae los ultimos resultados de estos equipos
    driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section/div/section/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[3]/span/a[2]').click()
    e_his = driver2.find_element('xpath','//*[@id="gamepackage-team-form-away"]/div/div').text
    row_e_his = e_his.split('\n')[1:]
    row_e_his = [row_e_his[i:i+2] for i in range(0, len(row_e_his), 2)]
    df_e_his = pd.DataFrame(row_e_his, columns=['Match','League'])
    driver2.execute_script("window.history.go(-1)")
    #Esta funcion entra al 3er partido de la 1er tabla y trae los ultimos resultados de estos equipos
    driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section/div/section/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[3]/td[3]/span/a[2]').click()
    f_his = driver2.find_element('xpath','//*[@id="gamepackage-team-form-away"]/div/div').text
    row_f_his = f_his.split('\n')[1:]
    row_f_his = [row_f_his[i:i+2] for i in range(0, len(row_f_his), 2)]
    df_f_his = pd.DataFrame(row_f_his, columns=['Match','League'])
    driver2.execute_script("window.history.go(-1)")
    #Esta funcion entra al 4to partido de la 1er tabla y trae los ultimos resultados de estos equipos
    driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/section/div/section/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[4]/td[3]/span/a[2]').click()
    g_his = driver2.find_element('xpath','//*[@id="gamepackage-team-form-away"]/div/div').text
    row_g_his = g_his.split('\n')[1:]
    row_g_his = [row_g_his[i:i+2] for i in range(0, len(row_g_his), 2)]
    df_g_his = pd.DataFrame(row_g_his, columns=['Match','League'])
    driver2.execute_script("window.history.go(-1)")
    
    #Esta funcion entra al 1er partido de la 2da tabla y trae los ultimos resultados de estos equipos
    driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/section/div/section/div[3]/div[2]/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/span/a[2]').click()
    b_his = driver2.find_element('xpath','//*[@id="gamepackage-team-form-away"]/div/div').text
    row_b_his = b_his.split('\n')[1:]
    row_b_his = [row_b_his[i:i+2] for i in range(0, len(row_b_his), 2)]
    df_b_his = pd.DataFrame(row_b_his, columns=['Match','League'])
    driver2.execute_script("window.history.go(-1)")
    #Esta funcion entra al 2do partido de la 2da tabla y trae los ultimos resultados de estos equipos
    driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/section/div/section/div[3]/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td[3]/span/a[2]').click()
    c_his = driver2.find_element('xpath','//*[@id="gamepackage-team-form-away"]/div/div').text
    row_c_his = c_his.split('\n')[1:]
    row_c_his = [row_c_his[i:i+2] for i in range(0, len(row_c_his), 2)]
    df_c_his = pd.DataFrame(row_c_his, columns=['Match','League'])
    driver2.execute_script("window.history.go(-1)")
    #Esta funcion entra al 3er partido de la 2da tabla y trae los ultimos resultados de estos equipos
    driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/section/div/section/div[3]/div[2]/div[2]/div/div[2]/table/tbody/tr[3]/td[3]/span/a[2]').click()
    d_his = driver2.find_element('xpath','//*[@id="gamepackage-team-form-away"]/div/div').text
    row_d_his = d_his.split('\n')[1:]
    row_d_his = [row_d_his[i:i+2] for i in range(0, len(row_d_his), 2)]
    df_d_his = pd.DataFrame(row_d_his, columns=['Match','League'])
    driver2.execute_script("window.history.go(-1)")

    #Esta funcion entra al 1er partido de la 3er tabla y trae los ultimos resultados de estos equipos
    driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/section/div/section/div[3]/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/span/a[2]').click()
    i_his = driver2.find_element('xpath','//*[@id="gamepackage-team-form-away"]/div/div').text
    row_i_his = i_his.split('\n')[1:]
    row_i_his = [row_i_his[i:i+2] for i in range(0, len(row_i_his), 2)]
    df_i_his = pd.DataFrame(row_i_his, columns=['Match','League'])
    driver2.execute_script("window.history.go(-1)")
    #Esta funcion entra al 2er partido de la 3er tabla y trae los ultimos resultados de estos equipos
    j_his = driver2.find_element('xpath','//*[@id="gamepackage-team-form-away"]/div/div').text
    row_j_his = j_his.split('\n')[1:]
    row_j_his = [row_j_his[i:i+2] for i in range(0, len(row_j_his), 2)]
    df_j_his = pd.DataFrame(row_j_his, columns=['Match','League'])
    driver2.execute_script("window.history.go(-1)")
    #Esta funcion entra al 3er partido de la 3er tabla y trae los ultimos resultados de estos equipos
    driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/section/div/section/div[3]/div[3]/div[2]/div/div[2]/table/tbody/tr[3]/td[3]/span/a[2]').click()
    h_his = driver2.find_element('xpath','//*[@id="gamepackage-team-form-away"]/div/div').text
    row_h_his = h_his.split('\n')[1:]
    row_h_his = [row_h_his[i:i+2] for i in range(0, len(row_h_his), 2)]
    df_h_his = pd.DataFrame(row_h_his, columns=['Match','League'])
    driver2.execute_script("window.history.go(-1)")
    #Esta funcion entra al 4to partido de la 3er tabla y trae los ultimos resultados de estos equipos
    driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/section/div/section/div[3]/div[3]/div[2]/div/div[2]/table/tbody/tr[4]/td[3]/span/a[2]').click()
    k_his = driver2.find_element('xpath','//*[@id="gamepackage-team-form-away"]/div/div').text
    row_k_his = k_his.split('\n')[1:]
    row_k_his = [row_k_his[i:i+2] for i in range(0, len(row_k_his), 2)]
    df_k_his = pd.DataFrame(row_k_his, columns=['Match','League'])
    driver2.execute_script("window.history.go(-1)")
    #Esta funcion entra al 5to partido de la 3er tabla y trae los ultimos resultados de estos equipos
    driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/section/div/section/div[3]/div[3]/div[2]/div/div[2]/table/tbody/tr[5]/td[3]/span/a[2]').click()
    l_his = driver2.find_element('xpath','//*[@id="gamepackage-team-form-away"]/div/div').text
    row_l_his = l_his.split('\n')[1:]
    row_l_his = [row_l_his[i:i+2] for i in range(0, len(row_l_his), 2)]
    df_l_his = pd.DataFrame(row_l_his, columns=['Match','League'])
    driver2.execute_script("window.history.go(-1)")
    #Esta funcion entra al 6to partido de la 3er tabla y trae los ultimos resultados de estos equipos
    driver2.find_element('xpath','//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/section/div/section/div[3]/div[3]/div[2]/div/div[2]/table/tbody/tr[6]/td[3]/span/a[2]').click()
    m_his = driver2.find_element('xpath','//*[@id="gamepackage-team-form-away"]/div/div').text
    row_m_his = m_his.split('\n')[1:]
    row_m_his = [row_m_his[i:i+2] for i in range(0, len(row_m_his), 2)]
    df_m_his = pd.DataFrame(row_m_his, columns=['Match','League'])
    return df_a_his, df_b_his, df_c_his, df_d_his, df_e_his, df_f_his, df_g_his, df_h_his, df_i_his, df_j_his, df_k_his, df_l_his, df_m_his

def players_data():
    driver3 = webdriver.Chrome()
    url3 = "https://www.espn.com.ar/futbol/equipo/plantel/_/id/16/arg.river_plate"
    driver3.get(url3)
    html3 = driver3.page_source
    soup3 = BeautifulSoup(html3, 'lxml')
    driver3.find_element('xpath','//*[@id="onetrust-close-btn-container"]/button').click()
    #Scraping table with goal keepers information
    table_arq = soup3.find_all('table')[0]
    df_arq = pd.read_html(table_arq.prettify())[0]
    df_arq.rename(columns={'POS': 'Posición', 'Est':'Estatura (cm)', 'P': 'Peso (kg)', 'NAC': 'Nacionalidad', 'Ap':'Apariciones',
                            'SUB': 'Apariciones_Sustituto', 'A': 'Atajadas', 'GA': 'Goles_Concedidos','A.1': 'Asistencias',
                            'FC': 'Faltas_cometidas', 'FS': 'Faltas_sufridas', 'TA': 'Tarjetas_amarillas', 
                            'TR': 'Tarjetas_Rojas'}, inplace=True)
    df_arq.drop(columns='Unnamed: 15', inplace=True)
    df_arq['Posición'] = df_arq['Posición'].str.replace('G', 'Arquero')
    df_arq['Estatura (cm)'] = df_arq['Estatura (cm)'].str.replace('.', '').str.replace('m', '').str.strip()
    df_arq['Peso (kg)'] = df_arq['Peso (kg)'].str.replace('kg', '').str.strip()
    cols = ['Estatura (cm)', 'Peso (kg)','Apariciones', 'Apariciones_Sustituto', 'Atajadas', 'Goles_Concedidos',
            'Asistencias','Faltas_cometidas', 'Faltas_sufridas','Tarjetas_amarillas', 'Tarjetas_Rojas']

    for i in cols:
        df_arq[i] = df_arq[i].str.replace('--', '0')
        df_arq[i] = df_arq[i].astype(int)
    
    #Scraping table with field players information
    table_campo = soup3.find_all('table')[1]
    df_campo = pd.read_html(table_campo.prettify())[0]
    df_campo.rename(columns={'POS': 'Posición', 'Est':'Estatura (cm)', 'P': 'Peso (kg)', 'NAC': 'Nacionalidad', 'Ap':'Apariciones',
                            'SUB': 'Apariciones_Sustituto', 'G': 'Goles','A': 'Asistencias', 'TT': 'Tiros', 'TM': 'Tiros_Meta',
                            'FC': 'Faltas_cometidas', 'FS': 'Faltas_sufridas', 'TA': 'Tarjetas_amarillas', 
                            'TR': 'Tarjetas_Rojas'}, inplace=True)
    df_campo['Posición'] = df_campo['Posición'].str.replace('D', 'Defensor')
    df_campo['Posición'] = df_campo['Posición'].str.replace('M', 'Mediocampo')
    df_campo['Posición'] = df_campo['Posición'].str.replace('A', 'Ataque')
    df_campo['Estatura (cm)'] = df_campo['Estatura (cm)'].str.replace('.', '').str.replace('m', '').str.strip()
    df_campo['Peso (kg)'] = df_campo['Peso (kg)'].str.replace('kg', '').str.strip()
    cols = ['Estatura (cm)', 'Peso (kg)','Apariciones', 'Apariciones_Sustituto', 'Goles',
        'Asistencias', 'Tiros', 'Tiros_Meta', 'Faltas_cometidas',
        'Faltas_sufridas', 'Tarjetas_amarillas', 'Tarjetas_Rojas']

    for i in cols:
        df_campo[i] = df_campo[i].str.replace('--', '0')
        df_campo[i] = df_campo[i].astype(int)
    return df_arq, df_campo