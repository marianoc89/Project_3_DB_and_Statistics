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

def match_1_graph(df_match_1):
    # Calculate the average number of goals scored and conceded by each team in their recent matches
    boca_goals_scored = df_match_1.loc[df_match_1['Home'] == 'Boca Juniors', 'Resultado'].apply(lambda x: int(x.split('-')[0])).tolist() + df_match_1.loc[df_match_1['Away'] == 'Boca Juniors', 'Resultado'].apply(lambda x: int(x.split('-')[1])).tolist()
    river_goals_scored = df_match_1.loc[df_match_1['Home'] == 'River Plate', 'Resultado'].apply(lambda x: int(x.split('-')[0])).tolist() + df_match_1.loc[df_match_1['Away'] == 'River Plate', 'Resultado'].apply(lambda x: int(x.split('-')[1])).tolist() 

    # Use these averages as the parameters for the Poisson distribution
    boca_lambda = np.mean(boca_goals_scored)
    river_lambda = np.mean(river_goals_scored)

    #Poisson distribution to determine the probabiliy of River Winning over Boca
    river_win_prob = np.sum(poisson.pmf(k, river_lambda) * poisson.pmf(k, boca_lambda) for k in range(0, 15))
    boca_win_prob = np.sum(poisson.pmf(k, boca_lambda) * poisson.pmf(k, river_lambda) for k in range(0, 15))
    draw_prob = 1 - (river_win_prob + boca_win_prob)

    # Simulate 10,000 matches and store the results
    draws = []
    for i in range(10000):
        goals_river = poisson.rvs(river_lambda)
        goals_boca = poisson.rvs(boca_lambda)
        if goals_river == goals_boca:
            draws.append(1)
        else:
            draws.append(0)

    # Calculate the mean and standard deviation of the draws
    mean_draws = np.mean(draws)
    std_draws = np.std(draws)

    # define the data and parameters for the histograms
    river_mu = river_lambda
    boca_mu = boca_lambda
    draw_mu = mean_draws
    sigma_river = np.std(river_goals_scored)
    sigma_boca = np.std(boca_goals_scored)
    sigma_draw = std_draws
    n_reps = 10000

    # generate the random samples for each histogram
    river_samples = np.random.normal(river_mu, sigma_river, n_reps)
    boca_samples = np.random.normal(boca_mu, sigma_boca, n_reps)
    draw_samples = np.random.normal(draw_mu, sigma_draw, n_reps)

    # create the subplots and plot the histograms
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))


    axs[0].hist(river_samples, bins=30, density=True, alpha=0.6, color='blue')
    axs[0].axvline(river_mu, c="y", linewidth=2, label="Mean")
    axs[0].set_title('Probability of River Plate Winning')
    axs[0].set_xlabel('Probability')
    axs[0].set_ylabel('Density')


    axs[1].hist(boca_samples, bins=30, density=True, alpha=0.6, color='red')
    axs[1].axvline(boca_mu, c="y", linewidth=2, label="Mean")
    axs[1].set_title('Probability of Boca Juniors Winning')
    axs[1].set_xlabel('Probability')
    axs[1].set_ylabel('Density')


    axs[2].hist(draw_samples, bins=30, density=True, alpha=0.6, color='green')
    axs[2].axvline(draw_mu, c="y", linewidth=2, label="Mean")
    axs[2].set_title('Probability of a Draw')
    axs[2].set_xlabel('Probability')
    axs[2].set_ylabel('Density')

    for i, ax in enumerate(axs):
        if i == 0:
            data = river_samples
            mean = river_mu
            std = sigma_river
        elif i == 1:
            data = boca_samples
            mean = boca_mu
            std = sigma_boca
        else:
            data = draw_samples
            mean = draw_mu
            std = sigma_draw

        x = np.linspace(min(data), max(data), 100)
        gauss = 1/(std * np.sqrt(2*np.pi)) * np.exp(-(x - mean)**2/(2*std**2))
        ax.plot(x, gauss, color='red', linewidth=2)

    plt.tight_layout()
    plt.show()
    fig.figure.savefig("C:/Users/maria/Desktop/Projects/Project_3_DB_and_Statistics/images/match_1_graph.jpg", dpi=500)

def match_2_graph(df_match_2):
    # Calculate the average number of goals scored and conceded by each team in their recent matches
    talleres_goals_scored = df_match_2.loc[df_match_2['Home'] == 'Talleres (Córdoba)', 'Resultado'].apply(lambda x: int(x.split('-')[0])).tolist() + df_match_2.loc[df_match_2['Away'] == 'Talleres (Córdoba)', 'Resultado'].apply(lambda x: int(x.split('-')[1])).tolist()
    river_goals_scored_2 = df_match_2.loc[df_match_2['Home'] == 'River Plate', 'Resultado'].apply(lambda x: int(x.split('-')[0])).tolist() + df_match_2.loc[df_match_2['Away'] == 'River Plate', 'Resultado'].apply(lambda x: int(x.split('-')[1])).tolist() 

    # Use these averages as the parameters for the Poisson distribution
    talleres_lambda = np.mean(talleres_goals_scored)
    river_lambda_2 = np.mean(river_goals_scored_2)

    #Poisson distribution to determine the probabiliy of River Winning over Talleres
    river_win_prob_2 = np.sum(poisson.pmf(k, river_lambda_2) * poisson.pmf(k, talleres_lambda) for k in range(0, 15))
    talleres_win_prob = np.sum(poisson.pmf(k, talleres_lambda) * poisson.pmf(k, river_lambda_2) for k in range(0, 15))
    draw_prob = 1 - (river_win_prob_2 + talleres_win_prob)

    # Simulate 10,000 matches and store the results
    draws = []
    for i in range(10000):
        goals_river = poisson.rvs(river_lambda_2)
        goals_talleres = poisson.rvs(talleres_lambda)
        if goals_river == goals_talleres:
            draws.append(1)
        else:
            draws.append(0)

    # Calculate the mean and standard deviation of the draws
    mean_draws = np.mean(draws)
    std_draws = np.std(draws)

    # define the data and parameters for the histograms
    river_mu = river_lambda_2
    talleres_mu = talleres_lambda
    draw_mu = mean_draws
    sigma_river = np.std(river_goals_scored_2)
    sigma_talleres = np.std(talleres_goals_scored)
    sigma_draw = std_draws
    n_reps = 10000

    # generate the random samples for each histogram
    river_samples_2 = np.random.normal(river_mu, sigma_river, n_reps)
    talleres_samples = np.random.normal(talleres_mu, sigma_talleres, n_reps)
    draw_samples = np.random.normal(draw_mu, sigma_draw, n_reps)

    # create the subplots and plot the histograms
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))


    axs[0].hist(river_samples_2, bins=30, density=True, alpha=0.6, color='blue')
    axs[0].axvline(river_mu, c="y", linewidth=2, label="Mean")
    axs[0].set_title('Probability of River Plate Winning')
    axs[0].set_xlabel('Probability')
    axs[0].set_ylabel('Density')


    axs[1].hist(talleres_samples, bins=30, density=True, alpha=0.6, color='red')
    axs[1].axvline(talleres_mu, c="y", linewidth=2, label="Mean")
    axs[1].set_title('Probability of Talleres (Córdoba) Winning')
    axs[1].set_xlabel('Probability')
    axs[1].set_ylabel('Density')


    axs[2].hist(draw_samples, bins=30, density=True, alpha=0.6, color='green')
    axs[2].axvline(draw_mu, c="y", linewidth=2, label="Mean")
    axs[2].set_title('Probability of a Draw')
    axs[2].set_xlabel('Probability')
    axs[2].set_ylabel('Density')

    for i, ax in enumerate(axs):
        if i == 0:
            data = river_samples_2
            mean = river_mu
            std = sigma_river
        elif i == 1:
            data = talleres_samples
            mean = talleres_mu
            std = sigma_talleres
        else:
            data = draw_samples
            mean = draw_mu
            std = sigma_draw

        x = np.linspace(min(data), max(data), 100)
        gauss = 1/(std * np.sqrt(2*np.pi)) * np.exp(-(x - mean)**2/(2*std**2))
        ax.plot(x, gauss, color='red', linewidth=2)

    plt.tight_layout()
    plt.show()
    fig.figure.savefig("C:/Users/maria/Desktop/Projects/Project_3_DB_and_Statistics/images/match_2_graph.jpg", dpi=500)

def match_3_graph(df_match_3):
    # Calculate the average number of goals scored and conceded by each team in their recent matches
    platense_goals_scored = df_match_3.loc[df_match_3['Home'] == 'Platense', 'Resultado'].apply(lambda x: int(x.split('-')[0])).tolist() + df_match_3.loc[df_match_3['Away'] == 'Platense', 'Resultado'].apply(lambda x: int(x.split('-')[1])).tolist()
    river_goals_scored_3 = df_match_3.loc[df_match_3['Home'] == 'River Plate', 'Resultado'].apply(lambda x: int(x.split('-')[0])).tolist() + df_match_3.loc[df_match_3['Away'] == 'River Plate', 'Resultado'].apply(lambda x: int(x.split('-')[1])).tolist() 

    # Use these averages as the parameters for the Poisson distribution
    platense_lambda = np.mean(platense_goals_scored)
    river_lambda_3 = np.mean(river_goals_scored_3)

    #Poisson distribution to determine the probabiliy of River Winning over Platense
    river_win_prob_3 = np.sum(poisson.pmf(k, river_lambda_3) * poisson.pmf(k, platense_lambda) for k in range(0, 15))
    platense_win_prob = np.sum(poisson.pmf(k, platense_lambda) * poisson.pmf(k, river_lambda_3) for k in range(0, 15))
    draw_prob = 1 - (river_win_prob_2 + talleres_win_prob)

    # Simulate 10,000 matches and store the results
    draws = []
    for i in range(10000):
        goals_river = poisson.rvs(river_lambda_3)
        goals_platense = poisson.rvs(platense_lambda)
        if goals_river == goals_platense:
            draws.append(1)
        else:
            draws.append(0)

    # Calculate the mean and standard deviation of the draws
    mean_draws = np.mean(draws)
    std_draws = np.std(draws)

    # define the data and parameters for the histograms
    river_mu = river_lambda_3
    platense_mu = platense_lambda
    draw_mu = mean_draws
    sigma_river = np.std(river_goals_scored_3)
    sigma_platense = np.std(platense_goals_scored)
    sigma_draw = std_draws
    n_reps = 10000

    # generate the random samples for each histogram
    river_samples_3 = np.random.normal(river_mu, sigma_river, n_reps)
    platense_samples = np.random.normal(platense_mu, sigma_platense, n_reps)
    draw_samples = np.random.normal(draw_mu, sigma_draw, n_reps)

    # create the subplots and plot the histograms
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))


    axs[0].hist(river_samples_3, bins=30, density=True, alpha=0.6, color='blue')
    axs[0].axvline(river_mu, c="y", linewidth=2, label="Mean")
    axs[0].set_title('Probability of River Plate Winning')
    axs[0].set_xlabel('Probability')
    axs[0].set_ylabel('Density')


    axs[1].hist(platense_samples, bins=30, density=True, alpha=0.6, color='red')
    axs[1].axvline(platense_mu, c="y", linewidth=2, label="Mean")
    axs[1].set_title('Probability of Platense Winning')
    axs[1].set_xlabel('Probability')
    axs[1].set_ylabel('Density')


    axs[2].hist(draw_samples, bins=30, density=True, alpha=0.6, color='green')
    axs[2].axvline(draw_mu, c="y", linewidth=2, label="Mean")
    axs[2].set_title('Probability of a Draw')
    axs[2].set_xlabel('Probability')
    axs[2].set_ylabel('Density')

    for i, ax in enumerate(axs):
        if i == 0:
            data = river_samples_3
            mean = river_mu
            std = sigma_river
        elif i == 1:
            data = platense_samples
            mean = platense_mu
            std = sigma_platense
        else:
            data = draw_samples
            mean = draw_mu
            std = sigma_draw

        x = np.linspace(min(data), max(data), 100)
        gauss = 1/(std * np.sqrt(2*np.pi)) * np.exp(-(x - mean)**2/(2*std**2))
        ax.plot(x, gauss, color='red', linewidth=2)

    plt.tight_layout()
    plt.show()
    fig.figure.savefig("C:/Users/maria/Desktop/Projects/Project_3_DB_and_Statistics/images/match_3_graph.jpg", dpi=500)

def eficacie_graph (df_campo):
    # Calculate efficacy for each player
    df_campo['Porb_Gol'] = df_campo['Goles'] / df_campo['Tiros']

    # Sort by efficacy in descending order
    df_campo = df_campo.sort_values('Porb_Gol', ascending=False)
    df_campo_2 = df_campo[df_campo['Porb_Gol'] > 0]

    # Create horizontal bar chart
    eficacie_graph = plt.scatter(df_campo_2['Porb_Gol'],df_campo_2['Nombre'] , c=np.random.rand(11))

    # Add labels and title
    plt.xlabel('Probabilidad goles por Tiros')
    plt.ylabel('Jugador')
    plt.title('Eficacia de los jugadores')
    plt.tight_layout()
    plt.show()
    eficacie_graph.figure.savefig("C:/Users/maria/Desktop/Projects/Project_3_DB_and_Statistics/images/eficacie_graph.jpg", dpi=500)

def goals_age_graph (df_campo):
    # Creating a subdataset for players with Goals > 0
    df_campo_3 = df_campo[df_campo['Goles'] > 0]

    # Calculate mean values of age and goals
    age_mean = df_campo_3['Edad'].mean()
    goals_mean = df_campo_3['Goles'].mean()

    # Create scatter plot
    goals_age_graph = plt.scatter(df_campo_3['Edad'], df_campo_3['Goles'])

    # Add mean age and mean goals as vertical lines
    plt.axvline(x=age_mean, color='red', linestyle='--', label='Mean Age')
    plt.axhline(y=goals_mean, color='blue', linestyle='--', label='Mean Goals')

    # Add axis labels and title
    plt.xlabel('Age')
    plt.ylabel('Goals')
    plt.title('Age vs. Goals')
    plt.legend()
    plt.tight_layout()
    plt.show()
    goals_age_graph.figure.savefig("C:/Users/maria/Desktop/Projects/Project_3_DB_and_Statistics/images/goals_age_graph.jpg", dpi=500)

def faltas_graph (df_campo):
    #Creating colums for probabilities of fouls, yellow and red cards
    df_campo_4 = df_campo[df_campo['Faltas_cometidas'] > 0]
    df_campo_4['Prob_Falta'] = df_campo_4['Faltas_cometidas'] / df_campo_4['Apariciones']
    df_campo_4['Prob_Amarilla'] = df_campo_4['Tarjetas_amarillas'] / df_campo_4['Faltas_cometidas']
    df_campo_4['Prob_Roja'] = df_campo_4['Tarjetas_Rojas'] / df_campo_4['Faltas_cometidas']
    df_campo_5 = df_campo_4[['Nombre', 'Posición', 'Edad', 'Estatura (cm)', 'Peso (kg)', 'Prob_Falta', 'Prob_Amarilla', 'Prob_Roja']]
    df_campo_5 = df_campo_5.sort_values('Prob_Falta', ascending=False)

    # Create grouped bar chart
    c = ['blue', 'yellow', 'red']
    faltas_graph = df_campo_5.set_index('Nombre').plot(kind='bar', y=['Prob_Falta', 'Prob_Amarilla', 'Prob_Roja'], figsize=(10, 6), color=c)

    # Add labels and title
    plt.xlabel('Jugador')
    plt.ylabel('Probabilidad')
    plt.title('Probabilidades de faltas, amarillas y rojas por jugador')
    plt.tight_layout()
    plt.show()
    faltas_graph.figure.savefig("C:/Users/maria/Desktop/Projects/Project_3_DB_and_Statistics/images/faltas_graph.jpg", dpi=500)