# THIS ONLY APPLIES TO SCENARIO 3, WHERE WE ASSUMED CERTAIN PATTERNS TO BE PRESENT
# FOR SCENARIO 1 AND 2, WHERE WE ASSUMED A DIFFERENT PATTERN, A DIFFERENT CORRUPTION MECHANISM NEEDS TO BE USED!

import os
import pandas as pd
import itertools

path = os.getcwd()
directory = os.path.join(path, "6June_batch\\6June_batch") # path to folder with synthesised gold standard data



# create path and transform .csv gold to parquet
path2 = os.path.join(directory, "accepted_sample_5.csv")
df = pd.read_csv(path2)

#dob format as YYYY-MM-DD
from datetime import datetime, timedelta
def format_days_to_date(days):
    base_date = datetime(1970, 1, 1)
    target_date = base_date + timedelta(days=days)
    return target_date.strftime('%Y-%m-%d')

df['g1_dob_arc1'] = df['g1_dob_arc1'].apply(format_days_to_date) 

# This Block Introduces the corruption functions 


from corrupt.corrupt_name import (
    alspac_first_name_random,
    alspac_G1_surname_random, # 95% completely different 
    alspac_G0_surname_random, # 95% completely different 
    alspac_first_name_alternatives, # 73% alternatives
    alspac_first_name_insertion,
    alspac_first_name_deletion,
    alspac_G1_last_name_insertion,
    alspac_G1_last_name_deletion,
    alspac_G0_last_name_insertion,
    alspac_G0_last_name_deletion,
    alspac_first_name_typo, # 14% typo
)


corruption_functions = [
    # alspac_first_name_random, # 6% completely different
    alspac_G1_surname_random, # 95% completely different 
    # alspac_G0_surname_random, # 95% completely different 
    # alspac_first_name_alternatives, # 73% alternatives
    # alspac_first_name_insertion,
    # alspac_first_name_deletion,
    # alspac_G1_last_name_insertion,
    # alspac_G1_last_name_deletion,
    # alspac_G0_last_name_insertion,
    # alspac_G0_last_name_deletion,
    alspac_first_name_typo, # 14% typo
    # alspac_name_inversion]
]

#condition 1
corruption_functions = [
    # alspac_first_name_random, # 6% completely different
    alspac_G1_surname_random, # 95% completely different 
    alspac_G0_surname_random, # 95% completely different 
    alspac_first_name_alternatives, # 73% alternatives
    # alspac_first_name_insertion,
    # alspac_first_name_deletion,
    # alspac_G1_last_name_insertion,
    # alspac_G1_last_name_deletion,
    # alspac_G0_last_name_insertion,
    # alspac_G0_last_name_deletion,
    # alspac_first_name_typo, # 14% typo
    # alspac_name_inversion]
]

# Create a copy of the original DataFrame to keep the original data
corrupted_df = df.copy()
# Initialize an empty list to store DataFrames
corrupted_dfs = []

# Generate combinations of AT LEAST 2 corruption functions, fit conbination 1,3,4
for combo_length in range(2, len(corruption_functions) + 1):
    for combo in itertools.combinations(corruption_functions, combo_length):
        for index, row in corrupted_df.iterrows():
            # Apply the selected corruption functions to the row
            corrupted_row = row.copy()
            for corrupt_func in combo:
                corrupted_row = corrupt_func(row, corrupted_row)
            # Append the corrupted row to the list as a DataFrame
            corrupted_dfs.append(pd.DataFrame([corrupted_row]))

# Concatenate all DataFrames in the list to create the final DataFrame
corrupted_df = pd.concat(corrupted_dfs, ignore_index=True)
corrupted_df.fillna(0, inplace=True)
corrupted_df.to_csv('corrupted\\new_corrupted\\corrupt_combination1.csv')


#condition 2: 
corruption_functions = [
    alspac_G1_surname_random,
    alspac_first_name_typo,

]

corrupted_df = df.copy()

# Initialize an empty list to store DataFrames
corrupted_dfs = []

# Iterate through all possible combinations of corruption functions
for combo_length in range(1, len(corruption_functions) + 1):
    for combo in itertools.combinations(corruption_functions, combo_length):
        for index, row in corrupted_df.iterrows():
            # Apply the selected corruption functions to the row
            corrupted_row = row.copy()
            for corrupt_func in combo:
                corrupted_row = corrupt_func(row, corrupted_row)
            # Append the corrupted row to the list as a DataFrame
            corrupted_dfs.append(pd.DataFrame([corrupted_row]))

# Concatenate all DataFrames in the list to create the final DataFrame
corrupted_df = pd.concat(corrupted_dfs, ignore_index=True)
corrupted_df.fillna(0, inplace=True)
corrupted_df.to_csv('corrupted\\new_corrupted\\corrupt_combination2.csv')


#condition 3
corruption_functions = [
    alspac_first_name_random, # 6% completely different
    alspac_G1_surname_random, # 95% completely different 
    alspac_G0_surname_random, # 95% completely different 
    alspac_first_name_alternatives, # 73% alternatives
    alspac_first_name_insertion,
    alspac_first_name_deletion,
    alspac_G1_last_name_insertion,
    alspac_G1_last_name_deletion,
    alspac_G0_last_name_insertion,
    alspac_G0_last_name_deletion,
    # alspac_first_name_typo, # 14% typo
    # alspac_name_inversion]
]

# Create a copy of the original DataFrame to keep the original data
corrupted_df = df.copy()
# Initialize an empty list to store DataFrames
corrupted_dfs = []

# Generate combinations of ONLY 1 corruption functions
records = [record for index, record in corrupted_df.iterrows()]

# Create a list to store the combinations of records and corruption functions
corrupted_data = []

# Iterate through records and corruption functions to create combinations
for record in records:
    for corrupt_func in corruption_functions:
        # Apply the corruption function to the record
        corrupted_record = corrupt_func(record, record.copy())
        corrupted_data.append(corrupted_record)

# Create a DataFrame from the list of corrupted data
corrupted_df = pd.DataFrame(corrupted_data)
corrupted_df.fillna(0, inplace=True)
# Concatenate all DataFrames in the list to create the final DataFrame
corrupted_df.to_csv('corrupted\\new_corrupted\\corrupt_combination3.csv')


# Combine 4 csv to 1
file_paths = ['6June_batch\\6June_batch\\accepted_sample_5.csv','corrupted\\new_corrupted\\corrupt_combination1.csv', 'corrupted\\new_corrupted\\corrupt_combination2.csv','corrupted\\new_corrupted\\corrupt_combination3.csv']

appended_data = pd.DataFrame()

for file_path in file_paths:
    data = pd.read_csv(file_path)
    appended_data = appended_data.append(data, ignore_index=True)

appended_data.fillna(0, inplace=True)
appended_data.to_csv('corrupted\\new_corrupted\\20231027_file5_scen1_corrupted.csv', index=False)



