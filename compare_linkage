# compare linkages and write on csv NEW - automate!

import pandas as pd
import os
import numpy as np

def filter_duplicates_probabilistic(df):
    # Sort the DataFrame by "match_weights" in descending order 
    df = df.sort_values(by=["unique_id_l", "match_weight"], ascending=[True, False])
    # Group by "unique_id" and keep the first row for each group
    df = df.groupby("unique_id_l").first().reset_index()
    return df


# scenario 0,1 uses independent data
scenarios = 0
data_set = 2
prob_threshold_values = ["-0.22", "0", "2", "3", "4", "5", "6"]
tf_thresehold_values = ["-3", "-2", "-1","-0.5", "1", "2", "4", "5", "6"]
collected_data = []
# for scenario in scenarios:
#    for data in data_set:

directory_path = f"linkage_outputs\\scen{scenarios}\\dataset{data_set}"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    if "deterministic" in filename:
        df = pd.read_csv(file_path)
        df['match'] = (df['unique_id_l'] == df['unique_id_r']).astype(int)
        filtered_df = df.drop_duplicates(subset='unique_id_l', keep='first')
        number_of_linkage = len(filtered_df)
        true_positive = len(filtered_df[filtered_df['match'] == 1])
        false_positive = len(filtered_df[filtered_df['match'] == 0])
        comparison_directory = os.path.join(os.getcwd(), f"output\\independent")
        gold_file_name = f"data_{data_set}_independent.csv"
        file_path = os.path.join(comparison_directory, gold_file_name)
        undrawn_df = pd.read_csv(file_path)
        undrawn_df['uncorrupted_record'] = undrawn_df['uncorrupted_record'].astype(bool)
        gold_df = undrawn_df[undrawn_df['uncorrupted_record']]
        columns_to_keep = ['cluster', 'unique_id' , 'maternal_agecat', 'ethgroup', 'g1_gender_arc', 'imddecile', 'g1_dob_arc1', 'syn_g0_surname', 'syn_g1_surname', 'syn_g1_firstname'] 
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
        filtered_df.rename(columns={'unique_id_l': 'unique_id'}, inplace = True)
        # combined Df
        merged_df = gold_df.merge(filtered_df, on = 'unique_id', how = 'left') 
        false_negative = len(set(merged_df['unique_id']) - set(filtered_df['unique_id']))
        true_negative = 0
        # metrics
        positive_predictive_value = true_positive/(true_positive + false_positive)
        sensitivity = true_positive/(true_positive + false_negative)
        # Rates
        false_match_rate = (1 - positive_predictive_value) * 100
        missed_match_rate = (1 - sensitivity) * 100
        collected_data.append({
            'Scenario': scenarios,
            'Data': data_set,
            'Threshold_value': 'deterministic',
            'Number of Linkage': number_of_linkage,
            'False Match Rate': false_match_rate,
            'Missed Match Rate': missed_match_rate
        })


for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    if "probabilistic" in filename:
            print(filename)
            df = pd.read_csv(file_path)
            df['match'] = (df['unique_id_l'] == df['unique_id_r']).astype(int)
            filtered_df = filter_duplicates_probabilistic(df)
            filtered_df.reset_index(drop=True, inplace=True)
            number_of_linkage = len(filtered_df)
            true_positive = len(filtered_df[filtered_df['match'] == 1])
            false_positive = len(filtered_df[filtered_df['match'] == 0])
            comparison_directory = os.path.join(os.getcwd(), f"output\\independent")
            gold_file_name = f"data_{data_set}_independent.csv"
            file_path = os.path.join(comparison_directory, gold_file_name)
            undrawn_df = pd.read_csv(file_path)
            undrawn_df['uncorrupted_record'] = undrawn_df['uncorrupted_record'].astype(bool)
            gold_df = undrawn_df[undrawn_df['uncorrupted_record']]
            columns_to_keep = ['cluster', 'unique_id' , 'maternal_agecat', 'ethgroup', 'g1_gender_arc', 'imddecile', 'g1_dob_arc1', 'syn_g0_surname', 'syn_g1_surname', 'syn_g1_firstname'] 
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
            filtered_df.rename(columns={'unique_id_l': 'unique_id'}, inplace = True)
            # combined Df
            merged_df = gold_df.merge(filtered_df, on = 'unique_id', how = 'left') 
            false_negative = len(set(merged_df['unique_id']) - set(filtered_df['unique_id']))
            true_negative = 0
            # metrics
            positive_predictive_value = true_positive/(true_positive + false_positive)
            sensitivity = true_positive/(true_positive + false_negative)
            # Rates
            false_match_rate = (1 - positive_predictive_value) * 100
            missed_match_rate = (1 - sensitivity) * 100
            collected_data.append({
                'Scenario': scenarios,
                'Data': data_set,
                'Threshold_value': filename,
                'Number of Linkage': number_of_linkage,
                'False Match Rate': false_match_rate,
                'Missed Match Rate': missed_match_rate
            })
                
for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    if "tf" in filename:
            print(filename)
            df = pd.read_csv(file_path)
            df['match'] = (df['unique_id_l'] == df['unique_id_r']).astype(int)
            filtered_df = filter_duplicates_probabilistic(df)
            filtered_df.reset_index(drop=True, inplace=True)
            number_of_linkage = len(filtered_df)
            true_positive = len(filtered_df[filtered_df['match'] == 1])
            false_positive = len(filtered_df[filtered_df['match'] == 0])
            comparison_directory = os.path.join(os.getcwd(), f"output\\independent")
            gold_file_name = f"data_{data_set}_independent.csv"
            file_path = os.path.join(comparison_directory, gold_file_name)
            undrawn_df = pd.read_csv(file_path)
            undrawn_df['uncorrupted_record'] = undrawn_df['uncorrupted_record'].astype(bool)
            gold_df = undrawn_df[undrawn_df['uncorrupted_record']]
            columns_to_keep = ['cluster', 'unique_id' , 'maternal_agecat', 'ethgroup', 'g1_gender_arc', 'imddecile', 'g1_dob_arc1', 'syn_g0_surname', 'syn_g1_surname', 'syn_g1_firstname'] 
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
            filtered_df.rename(columns={'unique_id_l': 'unique_id'}, inplace = True)
            # combined Df
            merged_df = gold_df.merge(filtered_df, on = 'unique_id', how = 'left') 
            false_negative = len(set(merged_df['unique_id']) - set(filtered_df['unique_id']))
            true_negative = 0
            # metrics
            positive_predictive_value = true_positive/(true_positive + false_positive)
            sensitivity = true_positive/(true_positive + false_negative)
            # Rates
            false_match_rate = (1 - positive_predictive_value) * 100
            missed_match_rate = (1 - sensitivity) * 100
            collected_data.append({
                'Scenario': scenarios,
                'Data': data_set,
                'Threshold_value': filename,
                'Number of Linkage': number_of_linkage,
                'False Match Rate': false_match_rate,
                'Missed Match Rate': missed_match_rate
            })


#print(f"For {filename}, the linkage output is: \n Number of linkages: {number_of_linkage} \n True positive: {true_positive} \n False Positive: {false_positive} \n False Negative: {false_negative} \n False Match Rate: {false_match_rate} \n Missed Match Rate: {missed_match_rate}")
            
# Create a DataFrame from the collected data
data_df = pd.DataFrame(collected_data)
data_df.to_csv(f"linkage_outputs\\scen0\\dataset{scenarios}\\20231120_dataset{scenarios}_comparison.csv")

