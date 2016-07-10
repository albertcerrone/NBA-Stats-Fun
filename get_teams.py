# -*- coding: utf-8 -*-

from nba_py.constants import *
import pandas as pd
import requests
import time


# This script is stand-alone.  No accompanying scripts are required.
# What does it do?  Basically, it scrapes stats.nba.com for every
# single game played by every team that ever played in the NBA.  Each
# team's games are saved to a .csv file written to the working directory.
# We also consolidate all of these files into a single "master" file
# called all_games.csv.


if __name__ == "__main__":

    # Dan Vatterott included this in his scraping script.
    # Without it, I encountered plenty of connection issues.
    # It was apparently borrowed from Py-Goldsberry:
    #      https://github.com/bradleyfay/py-Goldsberry
    header_data = { # this is pulled from the py goldsberry library
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'en-US,en;q=0.8',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'\
                ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 '\
                'Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'\
                ',image/webp,*/*;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive'
            }
    
    iterator = 0
    
    # iterate through teams
    for team in TEAMS.keys():
        
        # get all games for team
        try:
            season = requests.get('http://stats.nba.com/stats/teamgamelog/?Season=ALL&TeamID=%s&SeasonType=Regular+Season'\
    		         %(str(TEAMS[team]['id'])), headers=header_data)
        except:
            # This was a fix suggested by Dan Vatterott.
            # Apparently, the NBA gets unhappy with too many requests 
    		# (thinking a DOS attack perhaps?), so we wait a few seconds.
            time.sleep(5)
            season = requests.get('http://stats.nba.com/stats/teamgamelog/?Season=ALL&TeamID=%s&SeasonType=Regular+Season'\
    		                      %(str(TEAMS[team]['id'])), headers=header_data)
            
        # get headers
        columns = season.json()['resultSets'][0]['headers']
        # get raw data
        data = season.json()['resultSets'][0]['rowSet']
        #convert to Pandas data frame
        df = pd.DataFrame(data,columns=columns)
        
        # add some columns
        df['nickname'] = TEAMS[team]['name'] 
        df['team_hq'] = TEAMS[team]['city']     
        
        # write to csv
        df.to_csv(team+'.csv',index=False)
        
        # append to master dataframe
        if iterator == 0:    
            master = df
        else:
            master = master.append(df)
        
        iterator += 1
    
    # write to csv
    master.to_csv('all_games.csv', index=False)
    