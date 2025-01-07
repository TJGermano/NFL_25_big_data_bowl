import os
import pandas as pd

# Define the folder containing the weekly lead blocker analysis results
input_folder = "outputs"
output_file = "outputs/merged_lead_blocker_results.csv"

# Initialize an empty list to hold DataFrames
dataframes = []

# Iterate through files in the folder
for file in os.listdir(input_folder):
    if file.startswith("lead_blocker_analysis_week_") and file.endswith(".csv"):
        file_path = os.path.join(input_folder, file)
        print(f"Processing file: {file_path}")
        df = pd.read_csv(file_path)
        df['source_file'] = file  # Add a column to identify the source file
        dataframes.append(df)

# Concatenate all DataFrames
if dataframes:
    merged_df = pd.concat(dataframes, ignore_index=True)
    print(f"Merged {len(dataframes)} files. Saving to {output_file}.")
    merged_df.to_csv(output_file, index=False)
else:
    print("No lead blocker analysis files found.")

print("Merging complete.")
