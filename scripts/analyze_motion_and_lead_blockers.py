import pandas as pd

# Set display options for pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.2f}'.format)

# Load the merged file
merged_file = 'motion_players_with_lead_blocker_master.csv'
merged_data = pd.read_csv(merged_file)

# Add a count of motion players for each gameId and playId
merged_data['motion_player_count'] = merged_data.groupby(['gameId', 'playId'])['nflId'].transform('count')

# Count lead blocker results based on motion_category, teamAbbr, and motion_player_count
grouped_counts = merged_data.groupby(['teamAbbr', 'motion_category', 'motion_player_count']).agg(
    lead_blocker_count=('result', lambda x: x.str.contains('Lead Blocker Detected').sum()),  # Count lead blocker detected
    no_lead_blocker_count=('result', lambda x: (~x.str.contains('Lead Blocker Detected', na=False)).sum())  # Count everything else
).reset_index()

# Rename columns for clarity
grouped_counts.columns = ['teamAbbr', 'motion_category', 'motion_player_count', 'lead_blocker_count', 'no_lead_blocker_count']

# Print the counts
print(grouped_counts)
