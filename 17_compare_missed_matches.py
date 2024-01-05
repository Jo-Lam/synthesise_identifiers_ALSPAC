# combine exported into 1 file - format for graphs

import os
import pandas as pd

# Set the path to the top-level folder containing the CSV files

top_folder_path = "C:\\Users\\uctvjla\\OneDrive - University College London\\Desktop\\splink\\splink_synthetic_data-main\\linkage_outputs"

# Create an empty DataFrame to store the merged data
merged_df = pd.DataFrame()

# Iterate through all files in the top-level folder and its subfolders
for root, dirs, files in os.walk(top_folder_path):
    # Exclude folders with the name "archive"
    dirs[:] = [d for d in dirs if d.lower() != 'archive']
    for file in files:
        # Check if the file is a CSV file and contains the text "false_match" in its name
        if file.endswith('.csv') and 'miss_match' in file:
            file_path = os.path.join(root, file)
            # Read the CSV file into a DataFrame
            current_df = pd.read_csv(file_path)
            # Append the current DataFrame to the merged DataFrame
            merged_df = merged_df.append(current_df, ignore_index=True)

# Export the merged DataFrame to a new CSV file
output_csv_path = "C:\\Users\\uctvjla\\OneDrive - University College London\\Desktop\\splink\\splink_synthetic_data-main\\linkage_outputs\\merged_miss_match_data.csv"
merged_df.to_csv(output_csv_path, index=False)

print(f"Merged DataFrame exported to {output_csv_path}")


