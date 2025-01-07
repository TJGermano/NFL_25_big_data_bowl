import pandas as pd

# Load the merged file
merged_file = 'motion_players_lead_blocker_master_shift.csv'
merged_data = pd.read_csv(merged_file)

# Update the motion_category to "blocker motion" where lead blockers are detected
merged_data['motion_category'] = merged_data.apply(
    lambda row: 'blocker motion' if 'Lead Blocker Detected' in str(row['result']) else row['motion_category'],
    axis=1
)

# Create a unique identifier for each play
merged_data['unique_play_id'] = merged_data['gameId'].astype(str) + "_" + merged_data['playId'].astype(str)

# Keep only the required columns
filtered_data = merged_data[['gameId', 'playId', 'motion_category', 'result', 'unique_play_id']]

# Export the full dataset to CSV
output_file = 'motion_data_with_lead_blocker_unique_id.csv'
filtered_data.to_csv(output_file, index=False)

print(f"Data with unique identifiers exported to {output_file}.")
