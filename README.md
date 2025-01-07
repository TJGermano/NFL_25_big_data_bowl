# Motion Classification
# 2025 NFL Big Data Bowl 
## Introduction
This repository contains the scripts and analysis for my NFL motion analysis project. The goal is to take a different look at pre-snap motion in the NFL. By categorizing and analyzing motion types, we can uncover trends that connect pre-snap motion to post-snap outcomes. This analysis provides a simple, data-driven method to evaluate pre-snap motion and its role in modern football strategies.

## Data
The raw data used in this project is sourced from the Kaggle NFL Big Data Bowl. Below is the link to the dataset:

(https://www.kaggle.com/competitions/nfl-big-data-bowl-2025/data)

## Usage
To use the scripts in this repository, download the datasets from Kaggle and place them in the data directory.

## Scripts

### Step 1: Initial Data Processing
The first step in the analysis involves processing the raw player_play dataset to identify plays with motion and categorize them by motion type. This is achieved using the scripts/process_motion_data.py script. Below is a summary of the operations performed in this step:

#### Operations Performed:

- Load the player_play.csv dataset.

- Generate a unique identifier for each play (gameId + playId).

- Identify plays with motion based on specific columns (inMotionAtBallSnap, shiftSinceLineset, motionSinceLineset).

#### Categorize plays into motion types:

- Target: Plays where the motion player was the target receiver.

- Rusher: Plays where the motion player had a rushing attempt.

- Decoy: Plays where the player was in motion at the ball snap but was neither a target nor rusher.

- Diagnostic: Plays where the player was involved in a shift or motion prior to the ball snap.

- Deduplicate the dataset to ensure each play is categorized only once.

#### Export two key outputs:

- de-dupped-motion-plays.csv: Deduplicated dataset of motion plays categorized by type.

- motion-players.csv: Full dataset of plays with motion.

The full script for this step is located in scripts/process_motion_data.py.

### Step 2: Lead Blocker Analysis

The second step involves analyzing each play to identify potential lead blockers among motion players. This script must be run individually for each week's tracking data. The analysis is performed using the scripts/analyze_lead_blockers.py script.

#### Operations Performed:

- Load weekly tracking data (e.g., tracking_week_9.csv), motion-players.csv, and player_play.csv.

- For each play, identify:

-- The motion player involved.

-- The ball carrier (if present).

-- Whether the motion player acts as a lead blocker by staying ahead of the ball carrier within a defined cone and direction tolerance.

--Calculate intersections between the motion player's path and the ball carrier's path to detect lead blocker behavior.

- Export results to a CSV file summarizing the analysis for the week.

#### Outputs:

- outputs/lead_blocker_analysis_week_X.csv: Contains results for each play, including whether a lead blocker was detected.

- Statistics summarizing the percentage of plays with a lead blocker.

#### Example Usage:

- Ensure weekly tracking data (e.g., tracking_week_9.csv) is in the data directory.

- Run the analysis script for the desired week:

- python scripts/analyze_lead_blockers.py

- Review the output in the outputs/ folder.

### Step 3: Merge Lead Blocker Results

The third step involves combining the weekly lead blocker results into a single dataset for comprehensive analysis. This is achieved using the scripts/merge_lead_blocker_results.py script.

#### Operations Performed:

- Read all weekly lead_blocker_analysis_week_X.csv files in the outputs folder.

- Concatenate the data into a single DataFrame.

- Add a column to track the source file for each row.

- Export the merged results to a CSV file.

#### Outputs:

outputs/merged_lead_blocker_results.csv: Contains the combined results of lead blocker analysis for all weeks.

#### Example Usage:

- Ensure all weekly lead_blocker_analysis_week_X.csv files are in the outputs folder.

- Run the merging script:

--python scripts/merge_lead_blocker_results.py

- Review the combined results in the outputs/merged_lead_blocker_results.csv file.

### Step 4: Merge Lead Blocker and Motion Data

The fourth step merges the lead blocker results with the motion data to create a comprehensive dataset. This is achieved using the scripts/merge_motion_and_lead_blockers.py script.

#### Operations Performed:

- Load the merged lead blocker file (lead_blocker_master.csv).

- Load the motion data file (motion-players.csv).

- Perform a left merge on gameId, playId, and nflId to associate lead blocker results with motion players.

- Handle edge cases where nflId is not available in the lead blocker file:

- Ensure only the correct motion player is assigned a lead blocker result.

- Filter results based on motion categories (e.g., only "decoy" players can be lead blockers).

- Export the merged dataset to a CSV file.

#### Outputs:

- outputs/motion_players_lead_blocker_master_shift.csv: Comprehensive dataset combining motion and lead blocker results.

#### Example Usage:

- Ensure the merged lead blocker file (lead_blocker_master.csv) and motion data file (motion-players.csv) are in the outputs folder.

- Run the merging script:

- python scripts/merge_motion_and_lead_blockers.py

- Review the results in the outputs/motion_players_lead_blocker_master_shift.csv file.

### Step 5: Generate Motion Categories Table

The fifth step generates a single table that integrates all motion categories, including updates for lead blockers detected. This step ensures that each play has a unique identifier and is categorized correctly. This is achieved using the scripts/generate_motion_categories_table.py script.

#### Operations Performed:

- Load the comprehensive merged dataset (motion_players_lead_blocker_master_shift.csv).

- Update the motion_category column to "blocker motion" for plays where lead blockers are detected.

- Create a unique identifier for each play (gameId + playId).

- Filter the dataset to retain only relevant columns (gameId, playId, motion_category, result, unique_play_id).

- Export the resulting table to a CSV file.

#### Outputs:

- outputs/motion_data_with_lead_blocker_unique_id.csv: A comprehensive dataset with unique identifiers and updated motion categories.

#### Example Usage:

- Ensure the merged dataset (motion_players_lead_blocker_master_shift.csv) is in the outputs folder.

- Run the script to generate the motion categories table:

- python scripts/generate_motion_categories_table.py

- Review the resulting table in the outputs/motion_data_with_lead_blocker_unique_id.csv file.

### Step 6: Recalculate Using New Motion Categories

The sixth step involves recalculating the dataset to prioritize motion categories and ensure deduplication based on the new motion types. This is achieved using the scripts/recalculate_motion_categories.py script.

#### Operations Performed:

- Load the dataset with unique identifiers (motion_data_with_unique_id.csv).

- Assign a priority order to motion categories:

- Target: Highest priority.

- Rusher.

- Blocker.

- Decoy.

- Diagnostic: Lowest priority.

- Sort the data by unique_play_id and priority to determine the highest-priority motion category for each play.

- Deduplicate the dataset by keeping only the highest-priority motion category for each unique play.

- Export the recalculated dataset to a CSV file.

#### Outputs:

- outputs/deduplicated_motion_data.csv: A recalculated and deduplicated dataset with prioritized motion categories.

#### Example Usage:

- Ensure the dataset with unique identifiers (motion_data_with_unique_id.csv) is in the outputs folder.

- Run the recalculation script:

- python scripts/recalculate_motion_categories.py

- Review the resulting table in the outputs/deduplicated_motion_data.csv file.

### Step 7: Analyze Lead Blocker and Motion Data

The seventh step analyzes the merged lead blocker and motion dataset for trends and insights. This is achieved using the scripts/analyze_motion_and_lead_blockers.py script.

#### Operations Performed:

- Load the comprehensive merged dataset (motion_players_with_lead_blocker_master.csv).

- Add a count of motion players for each gameId and playId.

- Group data by teamAbbr, motion_category, and motion_player_count.

- Calculate counts of plays with and without lead blockers for each group.

- Export the summarized results to a CSV file.

#### Outputs:

- Summary of lead blocker and motion trends by team and motion type.

- Insights into the impact of motion player counts on lead blocking.

#### Example Usage:

- Ensure the comprehensive merged dataset (motion_players_with_lead_blocker_master.csv) is in the outputs folder.

- Run the analysis script:

- python scripts/analyze_motion_and_lead_blockers.py

- Review the summarized results in the console or export them to a CSV file for further analysis.

### Step 8: Visualization - Motion Type Distribution

The eighth step generates pie charts to visualize the distribution of a specific motion type, such as blocker motion. This is achieved using the charts/visualize_motion_type_distribution.py script.

#### Operations Performed:

- Load the recalculated dataset (deduplicated_motion_data.csv).

- Count the occurrences of a specific motion type (e.g., blocker motion).

- Calculate percentages for the specific motion type as a proportion of:

- Total plays.

- Total motion plays.

- Generate pie charts to visualize the data:

- One pie chart shows the specific motion type as a percentage of total plays.

- Another pie chart shows the specific motion type as a percentage of motion plays.

- The script allows users to specify different motion types for visualization by changing the motion_category in the script.

#### Outputs:

- Two pie charts:

- Specific motion type as a percentage of total plays.

- Specific motion type as a percentage of motion plays.

#### Example Usage:

- Ensure the recalculated dataset (deduplicated_motion_data.csv) is in the outputs folder.

- Run the visualization script:

- python charts/visualize_motion_type_distribution.py

- Review the generated pie charts and modify the motion_category in the script to visualize other motion types.

### Step 9: Detailed Pie Chart Visualization for Blocker Motion

This step creates detailed pie charts comparing blocker motion to total and motion plays. It builds upon the motion type distribution visualization and includes additional results printing.

#### Operations Performed:

- Load the deduplicated data (deduplicated_motion_dataLB.csv).

- Count blocker motion plays and total motion plays.

- Calculate percentages for blocker motion as:

- A percentage of total plays.

- A percentage of motion plays.

- Generate two pie charts for the above metrics.

#### Outputs:

- Two pie charts:

- Blocker motion as a percentage of total plays.

- Blocker motion as a percentage of motion plays.

- Detailed printed results for blocker motion statistics.

#### Example Usage:

- Ensure the recalculated dataset (deduplicated_motion_dataLB.csv) is in the outputs folder.

- Run the script:

- python charts/detailed_pie_chart_blocker_motion.py

- Review the charts and printed results in the console.

## Generated Data
- outputs/de-dupped-motion-plays.csv: Contains deduplicated motion play data with the following columns:
-- unique_play: Unique identifier for each play.
-- motion_category: Categorized motion type (target, rusher, decoy, diagnostic, blocker motion).
-- has_motion: Boolean indicating whether the play involved motion.
- outputs/motion-players.csv: Contains detailed information on all plays with motion, including raw motion flags and categories.
- outputs/lead_blocker_analysis_week_X.csv: Results for weekly lead blocker analysis.
- outputs/merged_lead_blocker_results.csv: Combined lead blocker analysis for all weeks.
- outputs/motion_players_lead_blocker_master_shift.csv: Comprehensive dataset merging motion data and lead blocker results.
- outputs/motion_data_with_lead_blocker_unique_id.csv: Comprehensive dataset with unique identifiers and updated motion categories.
- outputs/deduplicated_motion_data.csv: A recalculated and deduplicated dataset with prioritized motion categories.
- outputs/deduplicated_motion_dataLB.csv: A specialized deduplicated dataset used for blocker motion analysis and visualization.

## Visualization Scripts
- scripts/visualize_motion_vs_nonmotion.py: Generates a pie chart comparing motion vs. non-motion plays.
- scripts/visualize_motion_type_distribution.py: Generates visualizations of specific motion types as percentages of total and motion plays. You can modify the motion_category to analyze other types.
- scripts/detailed_pie_chart_blocker_motion.py: Creates detailed pie charts specifically for blocker motion analysis, comparing it to total plays and motion plays.

# License
This project is licensed under the MIT License. See the LICENSE file for more details.

# Contact
For any questions or feedback, feel free to open an issue in this repository or contact me directly.














