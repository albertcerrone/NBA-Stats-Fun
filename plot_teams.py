# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    master = pd.read_csv('all_games.csv')

    # make our Seaborn plot pretty
    sns.set_style("whitegrid")
    
    # convert the dates to pandas datetimes and make them indices
    master = pd.read_csv('all_games.csv')
    master['GAME_DATE'] = pd.to_datetime(master['GAME_DATE'])
    master.set_index('GAME_DATE', inplace=True)
    
    # Create a violin plot using seaborn wherein x-axis is team and y-axis is
    # field goal percentage.
    ax = sns.violinplot(x=master['team_hq'], y=master['FG_PCT']*100, hue=master['WL'], \
                        split=True, scale='count', order=np.unique(master['team_hq']))
    ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
    plt.ylabel('Field Goal Percentage')    
    plt.ylim([0,100])
    plt.show()
