import pandas as pd

# Set display options for pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.2f}'.format)

# Load datasets
games = pd.read_csv('games.csv')
plays = pd.read_csv('plays.csv')
players = pd.read_csv('players.csv')
player_play = pd.read_csv('player_play.csv')
tw1 = pd.read_csv('tracking_week_1.csv')

# break down the data into different groups
quarterly_play_counts = plays.groupby('quarter')['playId'].nunique()
down_play_counts =  plays.groupby('down')['playId'].nunique()
pa_counts =  plays.groupby('playAction')['playId'].nunique()


print(quarterly_play_counts)
print(down_play_counts)
print(pa_counts)