import pandas as pd
import os
import numpy as np

def filter_duplicates_probabilistic(df):
    df = df.sort_values(by = ['unique_id_l', 'match_weight'], ascending = [True, False])
    df = df.groupby("unique_id_l").first().reset_index()
    return df

# scenario 0,1 uses independent data
scenarios = 1
data_set = 5

directory_path = f"linkage_outputs\\scen{scenarios}\\dataset{data_set}"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# file_name = "probabilistic_threshold_3.csv"
file_name = "tf_2.csv"

file_path = os.path.join(directory_path, file_name)
df = pd.read_csv(file_path)
df['match'] = (df['unique_id_l'] == df['unique_id_r']).astype(int)
filtered_df = filter_duplicates_probabilistic(df)
filtered_df.reset_index(drop=True, inplace=True)
filtered_df.rename(columns={'unique_id_l': 'unique_id'}, inplace = True)

false_positive_list = filtered_df[filtered_df['match'] == 0]

# If indepedent, run this block

comparison_directory = os.path.join(os.getcwd(), f"output\\independent")
gold_file_name = f"data_{data_set}_independent.csv"
file_path = os.path.join(comparison_directory, gold_file_name)
undrawn_df = pd.read_csv(file_path)
undrawn_df['uncorrupted_record'] = undrawn_df['uncorrupted_record'].astype(bool)
gold_df = undrawn_df[undrawn_df['uncorrupted_record']]
columns_to_keep = ['unique_id' , 'maternal_agecat', 'ethgroup', 'g1_gender_arc', 'imddecile', 'g1_dob_arc1', 'syn_g0_surname', 'syn_g1_surname', 'syn_g1_firstname'] 
gold_df = gold_df.loc[:, columns_to_keep]                
gold_df["g1_dob_str"] = gold_df["g1_dob_arc1"].astype(str)
gold_df["g1_dob_str"] = gold_df["g1_dob_str"].str[:10]
gold_df["g1_dob_arc1"] = gold_df["g1_dob_str"]
gold_df.drop(columns = "g1_dob_str")
gold_df['maternal_agecat'] = gold_df['maternal_agecat'].replace('', np.nan)
gold_df['ethgroup'] = gold_df['ethgroup'].replace('Missing', np.nan)
gold_df['imddecile'] = gold_df['imddecile'].replace('', np.nan)
gold_df['syn_g1_firstname'] = gold_df['syn_g1_firstname'].replace('missing', np.nan)
gold_df['syn_g0_surname'] = gold_df['syn_g0_surname'].replace('missing', np.nan)
gold_df['syn_g1_surname'] = gold_df['syn_g1_surname'].replace('missing', np.nan)
# merge with gold standard data to flag false negatives
"""
# If associated, run this block
comparison_directory = os.path.join(os.getcwd(), f"output\\associated")
gold_file_name = f"data_{data_set}_associated.csv"
file_path = os.path.join(comparison_directory, gold_file_name)
undrawn_df = pd.read_csv(file_path)
undrawn_df['uncorrupted_record'] = undrawn_df['uncorrupted_record'].astype(bool)
gold_df = undrawn_df[undrawn_df['uncorrupted_record']]
columns_to_keep = ['unique_id' , 'maternal_agecat', 'ethgroup', 'g1_gender_arc', 'imddecile', 'g1_dob_arc1', 'syn_g0_surname', 'syn_g1_surname', 'syn_g1_firstname'] 
gold_df = gold_df.loc[:, columns_to_keep]                
gold_df["g1_dob_str"] = gold_df["g1_dob_arc1"].astype(str)
gold_df["g1_dob_str"] = gold_df["g1_dob_str"].str[:10]
gold_df["g1_dob_arc1"] = gold_df["g1_dob_str"]
gold_df.drop(columns = "g1_dob_str")
gold_df['maternal_agecat'] = gold_df['maternal_agecat'].replace('', np.nan)
gold_df['ethgroup'] = gold_df['ethgroup'].replace('Missing', np.nan)
gold_df['imddecile'] = gold_df['imddecile'].replace('', np.nan)
gold_df['syn_g1_firstname'] = gold_df['syn_g1_firstname'].replace('missing', np.nan)
gold_df['syn_g0_surname'] = gold_df['syn_g0_surname'].replace('missing', np.nan)
gold_df['syn_g1_surname'] = gold_df['syn_g1_surname'].replace('missing', np.nan)
"""
# merge
merged_df = gold_df.merge(filtered_df, on = 'unique_id', how = 'left') 

gold_id = gold_df['unique_id']
linked_id = filtered_df['unique_id']
unlinked_id = list(set(gold_id) - set (linked_id))
missed = gold_df[gold_df['unique_id'].isin(unlinked_id)]
missed

# load in no threshold dataset

# nothresh_df = pd.read_csv(f"linkage_outputs\\scen{scenarios}\\dataset{data_set}\\20240104_probabilistic_nothreshold.csv") 
nothresh_df = pd.read_csv(f"linkage_outputs\\scen{scenarios}\\dataset{data_set}\\20240104_probabilistic_tf_nothreshold.csv") 

nothresh_df['match'] = (nothresh_df['unique_id_l'] == nothresh_df['unique_id_r']).astype(int)
nothresh_df = filter_duplicates_probabilistic(nothresh_df)
nothresh_df.reset_index(drop = True, inplace = True)

filtered_nothresh_df = nothresh_df[nothresh_df['unique_id_l'].isin(unlinked_id)]

filtered_nothresh_df['g1fore_match'] = (filtered_nothresh_df['syn_g1_firstname_l'] == filtered_nothresh_df['syn_g1_firstname_r']).astype(int)
filtered_nothresh_df['g0sur_match'] = (filtered_nothresh_df['syn_g0_surname_l'] == filtered_nothresh_df['syn_g0_surname_r']).astype(int)
filtered_nothresh_df['g1sur_match'] = (filtered_nothresh_df['syn_g1_surname_l'] == filtered_nothresh_df['syn_g1_surname_r']).astype(int)
filtered_nothresh_df['gender_match'] = (filtered_nothresh_df['g1_gender_arc_l'] == filtered_nothresh_df['g1_gender_arc_r']).astype(int)
filtered_nothresh_df['dob_match'] = (filtered_nothresh_df['g1_dob_arc1_l'] == filtered_nothresh_df['g1_dob_arc1_r']).astype(int)

cols = ['g1fore_match', 'g0sur_match', 'g1sur_match',  'gender_match', 'dob_match']
filtered_nothresh_df['pattern'] = filtered_nothresh_df[cols].apply(lambda row: ''.join(row.values.astype(str)),axis = 1)

result = pd.DataFrame({'Counts': filtered_nothresh_df["pattern"].value_counts(), 'Percent': (filtered_nothresh_df["pattern"].value_counts()/len(filtered_nothresh_df))})
result 

len(filtered_nothresh_df)