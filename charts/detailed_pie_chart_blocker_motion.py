# Load the deduplicated data
deduped_data = pd.read_csv('deduplicated_motion_dataLB.csv')

# Constants
total_plays = 16124  # Given total number of plays

# Count blocker motion and total motion plays
blocker_motion_count = deduped_data[deduped_data['motion_category'] == 'blocker motion']['unique_play_id'].nunique()
total_motion_plays = deduped_data['unique_play_id'].nunique()

# Calculate percentages
percent_blocker_total_plays = round((blocker_motion_count / total_plays) * 100, 2)
percent_blocker_motion_plays = round((blocker_motion_count / total_motion_plays) * 100, 2)

# Prepare data for the pie charts
labels_total = ['Blocker Motion (Total Plays)', 'Other Plays']
sizes_total = [blocker_motion_count, total_plays - blocker_motion_count]
colors_total = ['#1f77b4', '#d3d3d3']

labels_motion = ['Blocker Motion (Motion Plays)', 'Other Motion Plays']
sizes_motion = [blocker_motion_count, total_motion_plays - blocker_motion_count]
colors_motion = ['#ff7f0e', '#d3d3d3']

# Create pie chart for total plays
fig, ax = plt.subplots(1, 2, figsize=(14, 7))

# Total Plays Pie Chart
ax[0].pie(
    sizes_total, labels=labels_total, autopct='%1.1f%%', startangle=90, colors=colors_total,
    textprops={'fontsize': 12}
)
ax[0].set_title('Blocker Motion as % of Total Plays', fontsize=14)

# Motion Plays Pie Chart
ax[1].pie(
    sizes_motion, labels=labels_motion, autopct='%1.1f%%', startangle=90, colors=colors_motion,
    textprops={'fontsize': 12}
)
ax[1].set_title('Blocker Motion as % of Motion Plays', fontsize=14)

# Show and save the chart
plt.tight_layout()
plt.show()

# Print results
print(f"Blocker Motion Plays: {blocker_motion_count}")
print(f"Total Plays: {total_plays}")
print(f"Total Motion Plays: {total_motion_plays}")
print(f"Blocker Motion as % of Total Plays: {percent_blocker_total_plays}%")
print(f"Blocker Motion as % of Motion Plays: {percent_blocker_motion_plays}%")
