# Drawing Corrupted Data
import pandas as pd
import numpy as np
# 1) import data
#df = pd.read_csv('2023_02_17_synthesised corrupted to draw.csv')

"""df = pd.DataFrame({'random_id':[1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4],
'a':['1','0','0','0','1','0','0','0','1','0','0','1','1','1','1','0','1','1','0','0'],
'b':['0','0','0','1','0','1','0','0','1','1','0','1','1','1','1','0','1','1','0','0'],
'c':['0','1','1','1','1','0','1','1','1','0','0','1','1','1','1','0','1','1','0','0']})"""

# 1) import data
df = pd.read_csv("corrupted_alspac_1000_record_each.csv")

# testing df
# df = pd.read_csv("corrupted_testing_2_copy.csv")

# 2) create binary variables
df2 = df.assign(
    g1surname_error = 0,
    g1firstname_error = 0,
    g0surname_error = 0,
#    g1firstname_missing = 0
)

# recode NAN to "Missing" in maternal age cat
df2['maternal_agecat'] = df2['maternal_agecat'].fillna('missing')
df2['imddecile'] = df2['imddecile'].fillna('missing')

df2.loc[(df2['ethgroup'] == "Missing"), "ethgroup"] = "missing"


# correcting
# G1 forename
df2.loc[(df2['first_name_variants_corrupt'] == "1") & (df2['first_name_typo_corrupt'] == "1"), "first_name_typo_corrupt"] = 2
df2.loc[(df2['first_name_variants_corrupt'] == "1") & (df2['first_name_insertion_corrupt'] == "1"), "first_name_insertion_corrupt"] = 2
df2.loc[(df2['first_name_variants_corrupt'] == "1") & (df2['first_name_deletion_corrupt'] == "1"), "first_name_deletion_corrupt"] = 2
df2.loc[(df2['first_name_variants_corrupt'] == "1") & (df2['random_first_corrupt'] == "1"), "random_first_corrupt"] = 2

df2.loc[(df2['first_name_typo_corrupt'] == "1") & (df2['first_name_insertion_corrupt'] == "1"), "first_name_insertion_corrupt"] = 2
df2.loc[(df2['first_name_typo_corrupt'] == "1") & (df2['first_name_deletion_corrupt'] == "1"), "first_name_deletion_corrupt"] = 2
df2.loc[(df2['first_name_typo_corrupt'] == "1") & (df2['random_first_corrupt'] == "1"), "random_first_corrupt"] = 2

df2.loc[(df2['first_name_insertion_corrupt'] == "1") & (df2['first_name_deletion_corrupt'] == "1"), "first_name_deletion_corrupt"] = 2
df2.loc[(df2['first_name_insertion_corrupt'] == "1") & (df2['random_first_corrupt'] == "1"), "random_first_corrupt"] = 2

df2.loc[(df2['first_name_deletion_corrupt'] == "1") & (df2['random_first_corrupt'] == "1"), "random_first_corrupt"] = 2

# G0 surname
df2.loc[(df2['G0_last_name_random_corrupt'] == "1") & (df2['G0_last_name_deletion_corrupt'] == "1"), "G0_last_name_deletion_corrupt"] = 2
df2.loc[(df2['G0_last_name_random_corrupt'] == "1") & (df2['G0_last_name_insertion_corrupt'] == "1"), "G0_last_name_insertion_corrupt"] = 2

df2.loc[(df2['G0_last_name_deletion_corrupt'] == "1") & (df2['G0_last_name_insertion_corrupt'] == "1"), "G0_last_name_insertion_corrupt"] = 2

# G1 surname
df2.loc[(df2['G1_last_name_random_corrupt'] == "1") & (df2['G1_last_name_deletion_corrupt'] == "1"), "G1_last_name_deletion_corrupt"] = 2
df2.loc[(df2['G1_last_name_random_corrupt'] == "1") & (df2['G1_last_name_insertion_corrupt'] == "1"), "G1_last_name_insertion_corrupt"] = 2

df2.loc[(df2['G1_last_name_deletion_corrupt'] == "1") & (df2['G1_last_name_insertion_corrupt'] == "1"), "G1_last_name_insertion_corrupt"] = 2

# 3) populate binary variables
df2['g1surname_error'] = np.where((df2["G1_last_name_deletion_corrupt"] == '1') , 1, df2['g1surname_error'])
df2['g1surname_error'] = np.where((df2["G1_last_name_insertion_corrupt"] == '1') , 1, df2['g1surname_error'])
df2['g1surname_error'] = np.where((df2["G1_last_name_random_corrupt"] == '1') , 1, df2['g1surname_error'])


df2['g0surname_error'] = np.where((df2['G0_last_name_deletion_corrupt'] == "1") , 1, df2['g0surname_error'])
df2['g0surname_error'] = np.where((df2['G0_last_name_insertion_corrupt'] == "1") , 1, df2['g0surname_error'])
df2['g0surname_error'] = np.where((df2['G0_last_name_random_corrupt'] == "1") , 1, df2['g0surname_error'])


df2['g1firstname_error'] = np.where((df2['random_first_corrupt'] == "1") , 1, df2['g1firstname_error']) 
df2['g1firstname_error'] = np.where((df2['first_name_deletion_corrupt'] == "1") , 1, df2['g1firstname_error']) 
df2['g1firstname_error'] = np.where((df2['first_name_insertion_corrupt'] == "1") , 1, df2['g1firstname_error']) 
df2['g1firstname_error'] = np.where((df2['first_name_typo_corrupt'] == "1") , 1, df2['g1firstname_error']) 
df2['g1firstname_error'] = np.where((df2['first_name_variants_corrupt'] == "1") , 1, df2['g1firstname_error']) 


# create error type combines first name insertion or deletion
df2.loc[(df2["first_name_insertion_corrupt"] == "1"), 'first_name_insdel'] = 1
df2.loc[(df2["first_name_deletion_corrupt"] == "1"), 'first_name_insdel'] = 1
df2.loc[(df2["first_name_insdel"] == np.nan), 'first_name_insdel'] = 0

df2 = df2.assign(first_name_insert_delete= 0)
df2.loc[(df2['first_name_insdel'] == 1), 'first_name_insert_delete'] = 1
del df2['first_name_insdel']

# Draw data - scenario 3 - error num.

from multi_sample_data import multi_sample_data
"""
def multi_sample_data(df, conditions_list, sample_sizes):
    # Create a copy of the original dataframe to work with
    df_copy = df.copy()
    sampled_df = pd.DataFrame()
    for conditions, sample_size in zip(conditions_list, sample_sizes):

        # Iterate through the list of conditions and filter the dataframe
        for condition in conditions:
            df_copy = df_copy.query(condition)
        # Get a random sample of unique ids using the sample() function and set the random_state for reproducibility
        sample_ids = df_copy["random_id"].sample(sample_size, random_state=1).unique()

        # Use the sample_ids to filter the dataframe and keep only the rows with the unique ids
        sample_df = df_copy[df_copy["random_id"].isin(sample_ids)]
        sampled_df = pd.concat([sampled_df,sample_df],ignore_index=True)
        
        # drop the selected rows
        df_copy = df_copy[~df_copy["random_id"].isin(sample_ids)]
    return sampled_df
"""
# conditions_list = [["a == '1'"],["b == '1'"], ["c == '1'"]]

conditions_list = [["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Black' & maternal_agecat == '40+'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Other' & maternal_agecat == '40+'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Other' & maternal_agecat == '<20'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Black' & maternal_agecat == '<20'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '40+'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Asian' & maternal_agecat == '<20'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Asian' & maternal_agecat == '20-29'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Black' & maternal_agecat == '30-39'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '<20'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '20-29'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '30-39'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Asian' & maternal_agecat == '30-39'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '20-29'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '<20'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == 'missing'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '30-39'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Black' & maternal_agecat == '20-29'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '40+'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Other' & maternal_agecat == '30-39'"],["g0surname_error != 1  & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Other' & maternal_agecat == '20-29'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Other' & maternal_agecat == '30-39'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Other' & maternal_agecat == '20-29'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Asian' & maternal_agecat == '30-39'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Black' & maternal_agecat == '30-39'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Asian' & maternal_agecat == '20-29'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '<20'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'Asian' & maternal_agecat == '<20'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Black' & maternal_agecat == '20-29'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Asian' & maternal_agecat == '<20'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '30-39'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '20-29'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == 'missing'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '20-29'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '<20'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '40+'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '30-39'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '40+'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'Black' & maternal_agecat == '<20'"],["G0_last_name_random_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Black' & maternal_agecat == '<20'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'missing' & maternal_agecat == '40+'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'Other' & maternal_agecat == '20-29'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'Asian' & maternal_agecat == '30-39'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'White' & maternal_agecat == '40+'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'Black' & maternal_agecat == '30-39'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'missing' & maternal_agecat == '<20'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'Asian' & maternal_agecat == '20-29'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'missing' & maternal_agecat == '30-39'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'White' & maternal_agecat == '20-29'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'missing' & maternal_agecat == 'missing'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'missing' & maternal_agecat == '20-29'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'White' & maternal_agecat == '30-39'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'White' & maternal_agecat == '<20'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'Black' & maternal_agecat == '20-29'"],["first_name_variants_corrupt == '1'  & g1surname_error != 1 & g0surname_error != 1 & ethgroup == 'Other' & maternal_agecat == '30-39'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Black' & maternal_agecat == '30-39'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Other' & maternal_agecat == '20-29'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Black' & maternal_agecat == '20-29'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '40+'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Asian' & maternal_agecat == '30-39'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '<20'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '30-39'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == 'missing'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Other' & maternal_agecat == '30-39'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '20-29'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '30-39'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '20-29'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '<20'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '40+'"],["G1_last_name_random_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'Asian' & maternal_agecat == '20-29'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'Other' & maternal_agecat == '20-29'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'Asian' & maternal_agecat == '30-39'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'Other' & maternal_agecat == '30-39'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'Black' & maternal_agecat == '30-39'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'Black' & maternal_agecat == '20-29'"],["first_name_insert_delete == 1 & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'Black' & maternal_agecat == '20-29'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'missing' & maternal_agecat == '30-39'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'White' & maternal_agecat == '40+'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'Asian' & maternal_agecat == '20-29'"],["first_name_insert_delete == 1 & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'Asian' & maternal_agecat == '20-29'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'missing' & maternal_agecat == '20-29'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'missing' & maternal_agecat == 'missing'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'White' & maternal_agecat == '30-39'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'White' & maternal_agecat == '20-29'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'White' & maternal_agecat == '<20'"],["first_name_typo_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'missing' & maternal_agecat == '<20'"],["first_name_insert_delete == 1 & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'White' & maternal_agecat == '<20'"],["first_name_insert_delete == 1 & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'White' & maternal_agecat == '40+'"],["random_first_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'White' & maternal_agecat == '40+'"],["G0_last_name_deletion_corrupt == '1' & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '40+'"],["first_name_insert_delete == 1 & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'missing' & maternal_agecat == 'missing'"],["first_name_insert_delete == 1 & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'White' & maternal_agecat == '20-29'"],["first_name_insert_delete == 1 & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'White' & maternal_agecat == '30-39'"],["first_name_insert_delete == 1 & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'missing' & maternal_agecat == '20-29'"],["first_name_insert_delete == 1 & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'missing' & maternal_agecat == '<20'"],["random_first_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'missing' & maternal_agecat == '<20'"],["G0_last_name_deletion_corrupt == '1' & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '<20'"],["first_name_insert_delete == 1 & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'missing' & maternal_agecat == '30-39'"],["random_first_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'missing' & maternal_agecat == '30-39'"],["G0_last_name_deletion_corrupt == '1' & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '30-39'"],["random_first_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'White' & maternal_agecat == '20-29'"],["random_first_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'White' & maternal_agecat == '30-39'"],["random_first_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'missing' & maternal_agecat == 'missing'"],["random_first_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'missing' & maternal_agecat == '20-29'"],["random_first_corrupt == '1' & g1surname_error != 1 & g0surname_error != 1  & ethgroup == 'White' & maternal_agecat == '<20'"],["G0_last_name_deletion_corrupt == '1' & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '<20'"],["G0_last_name_deletion_corrupt == '1' & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '20-29'"],["G0_last_name_deletion_corrupt == '1' & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == 'missing'"],["G0_last_name_deletion_corrupt == '1' & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '20-29'"],["G0_last_name_deletion_corrupt == '1' & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '30-39'"],["G0_last_name_insertion_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == 'missing'"],["G1_last_name_deletion_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '30-39'"],["G0_last_name_insertion_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '30-39'"],["G0_last_name_insertion_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '20-29'"],["G0_last_name_insertion_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '30-39'"],["G0_last_name_insertion_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '20-29'"],["G1_last_name_deletion_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '<20'"],["G0_last_name_insertion_corrupt == '1'  & g1surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '<20'"],["G1_last_name_deletion_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '20-29'"],["G1_last_name_deletion_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '30-39'"],["G1_last_name_deletion_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '20-29'"],["G1_last_name_insertion_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == 'missing'"],["G1_last_name_deletion_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == 'missing'"],["G1_last_name_insertion_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '20-29'"],["G1_last_name_insertion_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'missing' & maternal_agecat == '20-29'"],["G1_last_name_insertion_corrupt == '1' & g0surname_error != 1 & g1firstname_error != 1 & ethgroup == 'White' & maternal_agecat == '30-39'"]]


# sample_sizes = [1,1,1]
sample_sizes = [2,2,3,6,16,5,48,38,114,730,3027,28,4372,253,594,229,39,94,29,25,7,6,6,8,10,52,1,8,1,617,891,121,148,23,19,46,3,1,1,2,3,3,10,4,12,5,24,456,62,76,315,26,4,3,3,2,3,7,2,8,16,41,2,297,205,49,17,1,3,1,1,1,1,1,1,5,2,1,1,15,12,61,87,5,2,3,1,1,1,6,44,30,7,1,1,1,2,2,2,38,26,5,6,2,2,5,4,28,19,3,1,1,19,13,3,1,1,2,7,9,1,1,7,1,4]

# sample_sizes = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,4,4,4,4,5,5,5,5,5,6,6,6,6,7,7,7,7,7,8,8,8,9,10,10,12,12,13,15,16,17,19,19,19,23,24,26,26,28,30,38,41,44,46,49,52,61,62,76,87,121,148,205,297,315,456,617,891]

sampled_df_cond3, df_copy = multi_sample_data(df2, conditions_list, sample_sizes)
print(sampled_df_cond3)

sampled_df_cond3.to_csv('May_drawing_test_2023.csv', encoding = "utf-8-sig")
df_copy.to_csv('0205_unused_df_2023.csv', encoding = "utf-8-sig")
# sampled_df_cond3.to_csv('2023_02_20_synthesised corrupted data.csv', encoding = "utf-8-sig")