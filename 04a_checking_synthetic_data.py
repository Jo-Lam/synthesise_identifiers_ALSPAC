#checking accepted data

import pandas as pd
import os

# Define predefined values
ethgroup_values = ["Black", "White", "Asian", "Other", "Missing"]
maternal_agecat_values = ["<20", "20-29", "30-39", "40+", "NA"]

target_counts = {
    ("Black", "<20"): 11, 
    ("Black", "20-29"): 73,
    ("Black", "30-39"): 41,
    ("Black", "40+"): 0,
    #("Missing", "<20"): 156,
    #("White", "<20"): 388,   
    #("White", "20-29"): 6081,
    #("White", "30-39"): 4154,
    #("White", "40+"): 133,
    #("Missing", "20-29"):989,
    #("Asian", "<20"): 4,   
    #("Asian", "20-29"): 63,
    #("Asian", "30-39"): 37,
    #("Asian", "40+"): 1,
    #("Missing", "30-39"): 336,
    #("Other", "<20"): 2,   
    #("Other", "20-29"): 35,s
    #("Other", "30-39"): 36,
    ("Other", "40+"): 1,
    #("Missing", "40+"): 19,
    #("Missing", "NA"): 721
}


# Create an empty list to store matching CSV files
matching_files = []

# Directory containing the CSV files
csv_directory = '6June_batch\\6June_batch'

# Loop through CSV files in the directory
for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(csv_directory, filename)
        # Load the CSV into a DataFrame
        df = pd.read_csv(file_path)
        # Create a cross-tabulation of ethgroup and maternal_agecat
        cross_tab = pd.crosstab(df['ethgroup'], df['maternal_agecat'])
        # Check if the cross-tabulated counts match the predefined values
        match = True
        for (ethgroup, agecat), target_count in target_counts.items():
            actual_count = cross_tab.at[ethgroup, agecat]
            if actual_count < target_count:
                match = False
                break
        if match:
            matching_files.append(filename)
      
# Print the matching CSV files
if matching_files:
    print("Matching CSV files:")
    for file in matching_files:
        print(file)
else:
    print("No matching CSV files found.")


# compare errors 

import os
import pandas as pd

# Specify the folder containing the CSV files
folder_path = 'corrupted\\scen2'

# List all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Initialize an empty DataFrame
combined_df = pd.DataFrame()

# Load CSV files into the DataFrame
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    combined_df = combined_df.append(df, ignore_index=True)

# Tabulate ethgroup and g1surname_error percentages
ethgroup_percentages = combined_df['ethgroup'].value_counts(normalize=True) * 100
g1surname_error_percentages = combined_df['g1surname_error'].value_counts(normalize=True) * 100

# Display the results using tabulate
cross_tab = pd.crosstab(combined_df['ethgroup'], combined_df['g1surname_error'], margins=True, margins_name="Total", normalize="index") * 100
cross_tab

cross_tab2 = pd.crosstab(combined_df['maternal_agecat'], combined_df['g1surname_error'], margins=True, margins_name="Total", normalize="index") * 100
cross_tab2

# Display the results using tabulate
cross_tab = pd.crosstab(combined_df['ethgroup'], combined_df['g0surname_error'], margins=True, margins_name="Total", normalize="index") * 100
cross_tab

cross_tab2 = pd.crosstab(combined_df['maternal_agecat'], combined_df['g0surname_error'], margins=True, margins_name="Total", normalize="index") * 100
cross_tab2

# Display the results using tabulate
cross_tab = pd.crosstab(combined_df['ethgroup'], combined_df['g1firstname_error'], margins=True, margins_name="Total", normalize="index") * 100
cross_tab

cross_tab2 = pd.crosstab(combined_df['maternal_agecat'], combined_df['g1firstname_error'], margins=True, margins_name="Total", normalize="index") * 100
cross_tab2




