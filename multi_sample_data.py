# 
import pandas as pd 

def multi_sample_data2(df, conditions_list, sample_sizes):
    sampled_df = pd.DataFrame()
    copy_df = df
    for condition, sample_size in zip(conditions_list, sample_sizes):
        condition_df = copy_df.query(condition)
        sampled_condition_df = condition_df.sample(n=sample_size, random_state = 1)
        sampled_df = pd.concat([sampled_df, sampled_condition_df])
        unique_ids_to_remove = sampled_condition_df['unique_id'].unique()
        copy_df = copy_df[~copy_df['unique_id'].isin(unique_ids_to_remove)]
    return sampled_df

""" 
logic
label the synthetic/corrupted record with type of error induced, whether singular or combination of errors
List format [inversion error, dob error]


During each step:
1. Compare corrupted with record a step before corrupted (e.g., gold, or other, if multiple corruption in the same field)
2. From each step, mark if an corruption occured (binary, whether identical to previous step)
3. Master tracker tally the count of error [if composite error]





"""
