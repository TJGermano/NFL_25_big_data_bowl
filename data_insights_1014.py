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

# Count records for each value in the 'inMotionAtBallSnap' column
in_motion_counts = player_play['inMotionAtBallSnap'].value_counts(dropna=False)
shiftSinceLineset= player_play['shiftSinceLineset'].value_counts(dropna=False)
motionSinceLineset= player_play['motionSinceLineset'].value_counts(dropna=False)


# List of columns you're interested in
steams_cols = ['gameId', 'playId', 'playDescription', 'quarter', 'down', 'yardsToGo',
               'possessionTeam', 'defensiveTeam', 'yardlineSide', 'yardlineNumber',
               'gameClock', 'preSnapHomeScore', 'preSnapVisitorScore', 'offenseFormation']

# Filter rows where 'offenseFormation' is NaN or null
null_offense_formation = plays[steams_cols][plays['offenseFormation'].isnull()]
# Filter rows where 'down' equals 4
fourth_down_plays = plays[steams_cols][plays['down'] == 4]

# Display the filtered result
print(fourth_down_plays)


# # Display the filtered rows
# print(null_offense_formation)
# Count of unique playIds grouped by each event type
unique_playId_counts_by_event = tw1.groupby('event')['playId'].nunique().reset_index()

# Rename the columns for clarity
unique_playId_counts_by_event.columns = ['event', 'unique_playId_count']

# print(unique_playId_counts_by_event)


# Display the result
# print(in_motion_counts)
# print(shiftSinceLineset)
# print(motionSinceLineset)
# print(games.columns)
# print(plays.columns)
# print(players.columns)
# print(player_play.columns)
print(plays['pff_passCoverage'].unique().tolist())
# print(plays['offenseFormation'].unique().tolist())
# print(plays['passResult'].unique().tolist())
# print(player_play['playId'].nunique())
# print(tw1['event'].unique())
# print(tw1['event'].value_counts(dropna=False))
# print(tw1['playId'].nunique())
# print(tw1[tw1['event'] == 'run']['playId'].nunique())
# print(tw1[tw1['event'] == 'pass_forward']['playId'].nunique())
# print(tw1[tw1['event'] != 'huddle_break_offense']['playId'].unique().tolist())
