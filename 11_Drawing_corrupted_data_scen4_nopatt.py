# Drawing Corrupted Data
import pandas as pd
import numpy as np
# import pyarrow.parquet as pq
import os
path = os.getcwd()
directory = os.path.join(path, "output\\2023-10-22")

# 1) import data

# testing df
# df = pd.read_csv("corrupted_testing_2_copy.csv")

"""
file_list = [f for f in os.listdir(directory) if f.endswith('.csv')]
all_data = []
for file_name in file_list:
    file_path = os.path.join(directory, file_name)
    df = pd.read_csv(file_path)
    all_data.append(df)

merged_df = pd.concat(all_data, ignore_index=True)
"""

merged_df = pd.read_csv('output\\independent\\data_1_independent.csv')

"""
file_list = [f for f in os.listdir(directory) if f.endswith('.parquet')]
all_data = []
for file_name in file_list:
    file_path = os.path.join(directory, file_name)
    table = pq.read_table(file_path)
    df = table.to_pandas()
    all_data.append(df)
"""

# inspect data
pd.set_option('display.max_columns', None)
merged_df.head(5)
pd.reset_option('display.max_columns')
column_names = merged_df.columns.tolist()
# 1) import data
#df = pd.read_csv('2023_02_17_synthesised corrupted to draw.csv')

"""df = pd.DataFrame({'random_id':[1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4],
'a':['1','0','0','0','1','0','0','0','1','0','0','1','1','1','1','0','1','1','0','0'],
'b':['0','0','0','1','0','1','0','0','1','1','0','1','1','1','1','0','1','1','0','0'],
'c':['0','1','1','1','1','0','1','1','1','0','0','1','1','1','1','0','1','1','0','0']})"""


# 2) create binary variables
df2 = merged_df.assign(
    g1surname_error = 0,
    g1firstname_error = 0,
    g0surname_error = 0,
#    g1firstname_missing = 0
)

# recode NAN to "Missing" in maternal age cat
df2['maternal_agecat'] = df2['maternal_agecat'].fillna('missing')
df2['imddecile'] = df2['imddecile'].fillna('missing')

df2.loc[(df2['ethgroup'] == "Missing"), "ethgroup"] = "missing"


df2['syn_g0_surname'] = df2['syn_g0_surname'].fillna('missing')
df2['g1_dob_arc1'] = df2['g1_dob_arc1'].fillna('missing')
df2['g1_gender_arc'] = df2['g1_gender_arc'].fillna('missing')
df2['syn_g1_surname'] = df2['syn_g1_surname'].fillna('missing')
df2['syn_g1_firstname'] = df2['syn_g1_firstname'].fillna('missing')


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

df2 = df2.assign(G1_fore_insdel= 0)
df2.loc[(df2['first_name_insdel'] == 1), 'G1_fore_insdel'] = 1
del df2['first_name_insdel']

# repeat same for all error
#G1 surname
df2 = df2.assign(G1_sur_del= 0)
df2.loc[(df2['G1_last_name_deletion_corrupt'] == "1"), 'G1_sur_del'] = 1
del df2['G1_last_name_deletion_corrupt']

df2 = df2.assign(G1_sur_ins= 0)
df2.loc[(df2['G1_last_name_insertion_corrupt'] == "1"), 'G1_sur_ins'] = 1
del df2['G1_last_name_insertion_corrupt']

df2 = df2.assign(G1_sur_rand= 0)
df2.loc[(df2['G1_last_name_random_corrupt'] == "1"), 'G1_sur_rand'] = 1
del df2['G1_last_name_random_corrupt']

#G1 forename
df2 = df2.assign(G1_fore_variant= 0)
df2.loc[(df2['first_name_variants_corrupt'] == "1"), 'G1_fore_variant'] = 1
del df2['first_name_variants_corrupt']

df2 = df2.assign(G1_fore_typo= 0)
df2.loc[(df2['first_name_typo_corrupt'] == "1"), 'G1_fore_typo'] = 1
del df2['first_name_typo_corrupt']

df2 = df2.assign(G1_fore_rand= 0)
df2.loc[(df2['random_first_corrupt'] == "1"), 'G1_fore_rand'] = 1
del df2['random_first_corrupt']

#G0 sur
df2 = df2.assign(G0_sur_del= 0)
df2.loc[(df2['G0_last_name_deletion_corrupt'] == "1"), 'G0_sur_del'] = 1
del df2['G0_last_name_deletion_corrupt']

df2 = df2.assign(G0_sur_ins= 0)
df2.loc[(df2['G0_last_name_insertion_corrupt'] == "1"), 'G0_sur_ins'] = 1
del df2['G0_last_name_insertion_corrupt']

df2 = df2.assign(G0_sur_rand= 0)
df2.loc[(df2['G0_last_name_random_corrupt'] == "1"), 'G0_sur_rand'] = 1
del df2['G0_last_name_random_corrupt']


# clean variables data types

result = df2.dtypes
# df2.value_counts("vars")

# describe corrupted variables
# from tabulate import tabulate
# print(tabulate(df2, showindex= False))




# Draw data - scenario 3 - error num.

from multi_sample_data import multi_sample_data6_new

# Simplest condition

conditions_list = ["g0surname_error == 1  & g1surname_error != 1 & g1firstname_error != 1","g0surname_error != 1  & g1surname_error == 1 & g1firstname_error != 1","g0surname_error != 1  & g1surname_error != 1 & g1firstname_error == 1", "g0surname_error != 1  & g1surname_error != 1 & g1firstname_error != 1"]
sample_sizes = [1992,1328, 664, 9297]

sampled_df = multi_sample_data6_new(df2, conditions_list, sample_sizes)
print(sampled_df)

ethgroup_order = ["White", "Black", "Asian", "Other", "missing"]
matcat_order = ["<20", "20-29", "30-39", "40+", "missing"]
sampled_df['pattern'] = sampled_df[['g1surname_error', 'g0surname_error', 'g1firstname_error']].apply(lambda x: ''.join(map(str, x)), axis=1)
sampled_df['ethgroup'] = pd.Categorical(sampled_df['ethgroup'], categories=ethgroup_order, ordered=True)
sampled_df['maternal_agecat'] = pd.Categorical(sampled_df['maternal_agecat'], categories=matcat_order, ordered=True)
cross_tab3 = pd.crosstab(index=[sampled_df['ethgroup'], sampled_df['maternal_agecat']], columns=sampled_df['pattern'])
sampled_df.to_csv('corrupted\\scen4\\20231027_data1.csv', encoding = "utf-8-sig")
