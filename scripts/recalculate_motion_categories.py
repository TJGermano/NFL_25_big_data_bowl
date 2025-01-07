import pandas as pd

# Load the data with unique identifiers
input_file = 'no_shift/motion_data_with_unique_id.csv'
data = pd.read_csv(input_file)

# Define the priority order
priority_order = {
    'target': 1,
    'rusher': 2,
    'blocker': 3,
    'decoy': 4,
    'diagnostic': 5
}

# Add a priority column based on the motion category
data['priority'] = data['motion_category'].map(priority_order)

# Sort the data by unique_play_id and priority (lower number = higher priority)
data_sorted = data.sort_values(by=['unique_play_id', 'priority'])

# Deduplicate by keeping the highest-priority motion category for each unique_play_id
deduped_data = data_sorted.drop_duplicates(subset=['unique_play_id'], keep='first')

# Count the total number of unique_play_ids and ensure it matches the deduplicated rows
unique_play_id_count = data['unique_play_id'].nunique()
deduped_count = deduped_data.shape[0]

print(f"Number of unique play IDs: {unique_play_id_count}")
print(f"Number of deduplicated rows: {deduped_count}")

# Count by motion category in the deduplicated data
motion_type_counts = deduped_data['motion_category'].value_counts()
print("\nMotion Type Counts:")
print(motion_type_counts)

# Save the deduplicated data to a new CSV
output_file = 'deduplicated_motion_data.csv'
deduped_data.to_csv(output_file, index=False)

print(f"\nDeduplicated data saved to {output_file}")
