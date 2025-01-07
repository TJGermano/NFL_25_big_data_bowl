import pandas as pd

# Load datasets
player_play = pd.read_csv('../player_play.csv')

# Display general information about the dataset
print("Player Play DataFrame Info:")
print(player_play.info())
print("\nSample Rows:")
print(player_play.head())

# Create a unique identifier for each play
player_play['unique_play'] = player_play['gameId'].astype(str) + "_" + player_play['playId'].astype(str)

# Identify plays with motion
player_play['has_motion'] = (
    player_play['inMotionAtBallSnap'] |
    player_play['shiftSinceLineset'] |
    player_play['motionSinceLineset']
)

# Filter only plays with motion
plays_with_motion = player_play[player_play['has_motion']]

# Display information about plays with motion
print("\nPlays with Motion DataFrame Info:")
print(plays_with_motion.info())
print("\nSample Rows of Plays with Motion:")
print(plays_with_motion.head())

# Define a function to categorize plays according to priority
def categorize_motion(row):
    if row['wasTargettedReceiver'] == 1:
        return 'target'
    elif row['hadRushAttempt'] == 1:
        return 'rusher'
    elif row['inMotionAtBallSnap'] == 1:
        return 'decoy'
    elif row['shiftSinceLineset'] == 1 or row['motionSinceLineset'] == 1:
        return 'diagnostic'
    else:
        return 'none'

# Apply categorization
plays_with_motion['motion_category'] = plays_with_motion.apply(categorize_motion, axis=1)

# Deduplicate by unique_play, ensuring only one play is categorized
dedup_summary = plays_with_motion[['unique_play', 'motion_category']].drop_duplicates(subset='unique_play')

# Add a 'has_motion' column to the dedup_summary for completeness
dedup_summary['has_motion'] = True

# Debugging: Check for duplicates in unique_play
duplicates = dedup_summary['unique_play'].duplicated().sum()
print(f"\nNumber of duplicate unique_play entries in dedup_summary: {duplicates}")

# Debugging: Validate deduplication
unique_motion_plays = dedup_summary['unique_play'].nunique()
print(f"\nUnique plays in dedup_summary: {unique_motion_plays}")
print(f"Total rows in dedup_summary: {len(dedup_summary)}")

# Calculate totals
total_plays = player_play['unique_play'].nunique()
total_motion_plays = dedup_summary['unique_play'].nunique()
total_non_motion_plays = total_plays - total_motion_plays

# Count the number of plays per category
category_counts = dedup_summary['motion_category'].value_counts().to_dict()

# Print results
print(f"\nTotal plays: {total_plays}")
print(f"Total motion plays: {total_motion_plays}")
print(f"Total non-motion plays: {total_non_motion_plays}")
print(f"Motion category counts: {category_counts}")

# Print deduplicated summary info
print("\nDeduplicated Summary DataFrame Info:")
print(dedup_summary.info())
print("\nSample Rows of Deduplicated Summary:")
print(dedup_summary.head())

# Export dedup_summary as a CSV file
dedup_summary.to_csv('de-dupped-motion-plays.csv', index=False)
print("\n'dedup_summary' DataFrame saved to 'de-dupped-motion-plays.csv'")

# Export plays_with_motion as a CSV file
plays_with_motion.to_csv('motion-players.csv', index=False)
print("\n'plays_with_motion' DataFrame saved to 'motion-players.csv'")
