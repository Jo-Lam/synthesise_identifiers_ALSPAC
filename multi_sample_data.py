# 
import pandas as pd 
import numpy as np

def multi_sample_data(df, conditions_list, sample_sizes):
    # Create a copy of the original dataframe to work with
    np.random.seed(0)
    sampled_df = pd.DataFrame()
    df_copy = df.copy()
    unused_ids = pd.Series(df_copy['random_id'].unique())
    for conditions, sample_size in zip(conditions_list, sample_sizes):

        # create copy of each df
        df_copy_temp = df_copy.copy()
        
        # Iterate through the list of conditions and filter the dataframe
        for condition in conditions:
            df_copy_temp = df_copy_temp.query(condition)
            print(condition)

            # check if the filtered_dataframe is empty
        if df_copy_temp.empty:
            print("There is no data that fulfils this")
            continue

        # Get a random sample of unique ids using the sample() function and set the random_state for reproducibility
        # sample_ids = df_copy["random_id"].sample(sample_size, random_state=1).unique()
        sample_ids = np.random.choice(df_copy_temp["random_id"], sample_size, replace = False)
        if len(sample_ids) != sample_size:
            print(len(sample_ids))
            print(sample_size)

        # Use the sample_ids to filter the dataframe and keep only the rows with the unique ids
        sample_df = df_copy_temp[df_copy_temp["random_id"].isin(sample_ids)]
        sample_df = sample_df.drop_duplicates(subset = ["random_id"])

        # Check if the sample has the expected number of rows, and resample if necessary
        """while sample_df.shape[0] < sample_size:
            remaining_ids = unused_ids[~unused_ids.isin(sample_ids)]
            additional_ids = remaining_ids.sample(sample_size - sample_df.shape[0], random_state=1).unique()
            additional_df = df_copy[df_copy["random_id"].isin(additional_ids)]
            sample_df = pd.concat([sample_df, additional_df], ignore_index=True)
            sample_ids = np.concatenate([sample_ids, additional_ids])"""
        sampled_df = pd.concat([sampled_df,sample_df],ignore_index=True)
        
        # Update the list of unused ids
        unused_ids = unused_ids[~unused_ids.isin(sample_ids)]

        # drop the selected rows
        df_copy = df_copy[~df_copy["random_id"].isin(sample_ids)]
    return sampled_df, df_copy

""" 
logic
label the synthetic/corrupted record with type of error induced, whether singular or combination of errors
List format [inversion error, dob error]


During each step:
1. Compare corrupted with record a step before corrupted (e.g., gold, or other, if multiple corruption in the same field)
2. From each step, mark if an corruption occured (binary, whether identical to previous step)
3. Master tracker tally the count of error [if composite error]





"""