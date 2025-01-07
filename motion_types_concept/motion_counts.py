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

# Total distinct playIds
distinct_playIds = player_play['playId'].nunique()

# Motion plays
motion_plays = player_play.groupby('playId')['inMotionAtBallSnap'].any().sum()
non_motion_plays = player_play.groupby('playId')['inMotionAtBallSnap'].all().sum()
mixed_motion_plays = distinct_playIds - (motion_plays + non_motion_plays)

# Shift Since Lineset
shifted_plays = player_play.groupby('playId')['shiftSinceLineset'].any().sum()
non_shifted_plays = player_play.groupby('playId')['shiftSinceLineset'].all().sum()
mixed_shifted_plays = distinct_playIds - (shifted_plays + non_shifted_plays)

# Motion Since Lineset
motion_since_lineset_plays = player_play.groupby('playId')['motionSinceLineset'].any().sum()
non_motion_since_lineset_plays = player_play.groupby('playId')['motionSinceLineset'].all().sum()
mixed_motion_since_lineset_plays = distinct_playIds - (motion_since_lineset_plays + non_motion_since_lineset_plays)

# Function to calculate percentage
def calculate_percentage(count, total):
    return (count / total) * 100

# Print the results
print("Total distinct playIds:", distinct_playIds)

# Motion results
print("\nDistinct playIds with motion (at least one player):", motion_plays, f"({calculate_percentage(motion_plays, distinct_playIds):.2f}%)")
print("Distinct playIds without motion (all players):", non_motion_plays, f"({calculate_percentage(non_motion_plays, distinct_playIds):.2f}%)")
print("Distinct playIds with mixed motion (some players in motion, some not):", mixed_motion_plays, f"({calculate_percentage(mixed_motion_plays, distinct_playIds):.2f}%)")

# Shift results
print("\nDistinct playIds with shift (at least one player):", shifted_plays, f"({calculate_percentage(shifted_plays, distinct_playIds):.2f}%)")
print("Distinct playIds without shift (all players):", non_shifted_plays, f"({calculate_percentage(non_shifted_plays, distinct_playIds):.2f}%)")
print("Distinct playIds with mixed shift (some players shifted, some not):", mixed_shifted_plays, f"({calculate_percentage(mixed_shifted_plays, distinct_playIds):.2f}%)")

# Motion since lineset results
print("\nDistinct playIds with motion since lineset (at least one player):", motion_since_lineset_plays, f"({calculate_percentage(motion_since_lineset_plays, distinct_playIds):.2f}%)")
print("Distinct playIds without motion since lineset (all players):", non_motion_since_lineset_plays, f"({calculate_percentage(non_motion_since_lineset_plays, distinct_playIds):.2f}%)")
print("Distinct playIds with mixed motion since lineset (some players in motion, some not):", mixed_motion_since_lineset_plays, f"({calculate_percentage(mixed_motion_since_lineset_plays, distinct_playIds):.2f}%)")
