import pandas as pd

# Load the files
lead_blocker_file = '../lead_blocker_master.csv'
motion_players_file = '../motion-players.csv'
# Read the CSV files
lead_blocker = pd.read_csv(lead_blocker_file)
motion_players = pd.read_csv(motion_players_file)

# Improved merge
# Ensure that the lead_blocker file contains only unique rows per gameId, playId, and the correct nflId of the lead blocker (if available)
if 'nflId' in lead_blocker.columns:
    merged_data = motion_players.merge(
        lead_blocker[['gameId', 'playId', 'nflId', 'result']],
        on=['gameId', 'playId', 'nflId'],  # Merge on nflId as well
        how='left'
    )
else:
    # Merge without nflId but ensure filtering afterward
    merged_data = motion_players.merge(
        lead_blocker[['gameId', 'playId', 'result']],
        on=['gameId', 'playId'],
        how='left'
    )
    # Filter: Apply logic to ensure that only the correct motion player gets the result
    merged_data['result'] = merged_data.apply(
        lambda row: row['result'] if row['motion_category'] == 'decoy' else None, axis=1
    )

# Save the corrected merged file
output_file = '../no_shift/motion_players_lead_blocker_master_shift.csv'
merged_data.to_csv(output_file, index=False)

print(f"Corrected merged data saved to {output_file}")
