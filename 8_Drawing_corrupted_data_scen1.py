# Drawing Corrupted Data

# Draw data - scenario 3 - error num.
import pandas as pd
from multi_sample_data import multi_sample_data6_new2
df2 = pd.read_csv('corrupted\\new_corrupted\\20231027_file5_corrupted_clean.csv')

df2['pattern'] = df2[['g1surname_error', 'g0surname_error', 'g1firstname_error']].apply(lambda x: ''.join(map(str, x)), axis=1)
cross_tab1 = pd.crosstab(index=[df2['ethgroup'], df2['maternal_agecat']], columns=df2['pattern'])

uncorrupted_df = pd.read_csv('6June_batch\\6June_batch\\accepted_sample_4.csv') 
uncorrupted_df['maternal_agecat'].fillna("Missing", inplace = True)

cross_tab = pd.crosstab(index=[uncorrupted_df['ethgroup']],columns= uncorrupted_df['maternal_agecat'], margins= True)


condition_list = ["G0_sur_rand  == 1 & G1_sur_rand == 1 & G1_fore_variant  == 1  & ethgroup == 'White' & maternal_agecat == '<20'","G0_sur_rand  == 1 & G1_sur_rand == 1 & G1_fore_variant  == 1& ethgroup == 'Black'& maternal_agecat == '20-29'","G0_sur_rand  == 1 & G1_sur_rand == 1 & G1_fore_variant  == 1& ethgroup == 'Other'& maternal_agecat == '30-39'","G0_sur_rand  == 1 & G1_sur_rand == 1 & G1_fore_variant  == 1& ethgroup == 'missing'& maternal_agecat == '20-29'","G0_sur_rand  == 1 & G1_sur_rand == 1 & G1_fore_variant  == 1& ethgroup == 'missing'& maternal_agecat == '30-39'","G0_sur_rand  == 1 & G1_sur_rand == 1 & G1_fore_variant  == 1& ethgroup == 'missing'& maternal_agecat == 'missing'","G1_sur_rand== 1 & G1_fore_typo== 1 & g0surname_error != 1& ethgroup == 'Other'& maternal_agecat == '20-29'","G1_sur_rand== 1 & G1_fore_typo== 1 & g0surname_error != 1& ethgroup == 'missing'& maternal_agecat == '<20'","G1_sur_rand== 1 & G1_fore_typo== 1 & g0surname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '40+'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'Asian'& maternal_agecat == '20-29'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'Other'& maternal_agecat == '20-29'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'Other'& maternal_agecat == '30-39'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '40+'","G0_sur_rand == 1 & G1_fore_variant == 1 & g1surname_error != 1& ethgroup == 'missing'& maternal_agecat == '<20'","G0_sur_rand == 1 & G1_fore_variant == 1 & g1surname_error != 1& ethgroup == 'missing'& maternal_agecat == '40+'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Asian'& maternal_agecat == '40+'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Other'& maternal_agecat == '40+'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'Black'& maternal_agecat == '20-29'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'Black'& maternal_agecat == '30-39'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'Asian'& maternal_agecat == '20-29'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '40+'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Other'& maternal_agecat == '30-39'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Other'& maternal_agecat == '40+'","G1_sur_rand== 1 & G1_fore_typo== 1 & g0surname_error != 1& ethgroup == 'missing'& maternal_agecat == '20-29'","G0_sur_rand == 1 & G1_fore_variant == 1 & g1surname_error != 1& ethgroup == 'Black'& maternal_agecat == '20-29'","G0_sur_rand == 1 & G1_fore_variant == 1 & g1surname_error != 1& ethgroup == 'Asian'& maternal_agecat == '30-39'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Other'& maternal_agecat == '<20'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'Other'& maternal_agecat == '30-39'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '30-39'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Black'& maternal_agecat == '<20'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Asian'& maternal_agecat == '30-39'","G1_fore_variant == 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'Other'& maternal_agecat == '30-39'","G1_sur_rand== 1 & G1_fore_typo== 1 & g0surname_error != 1& ethgroup == 'White'& maternal_agecat == '40+'","G0_sur_rand == 1 & G1_fore_variant == 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '40+'","G0_sur_rand == 1 & G1_fore_variant == 1 & g1surname_error != 1& ethgroup == 'missing'& maternal_agecat == '30-39'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Asian'& maternal_agecat == '<20'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '40+'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'Other'& maternal_agecat == '20-29'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '40+'","G1_fore_variant == 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'Other'& maternal_agecat == '20-29'","G1_fore_variant == 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'missing'& maternal_agecat == '40+'","G1_sur_rand== 1 & G1_fore_typo== 1 & g0surname_error != 1& ethgroup == 'missing'& maternal_agecat == 'missing'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'Black'& maternal_agecat == '20-29'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'Black'& maternal_agecat == '30-39'","G0_sur_rand == 1 & G1_fore_variant == 1 & g1surname_error != 1& ethgroup == 'Other'& maternal_agecat == '30-39'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Asian'& maternal_agecat == '20-29'","G1_fore_typo== 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'Asian'& maternal_agecat == '30-39'","G1_sur_rand== 1 & G1_fore_typo== 1 & g0surname_error != 1& ethgroup == 'White'& maternal_agecat == '<20'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '<20'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == 'missing'","G0_sur_del == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '20-29'","G0_sur_ins == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '20-29'","G1_fore_typo== 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'missing'& maternal_agecat == '30-39'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '30-39'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Other'& maternal_agecat == '20-29'","G1_fore_typo== 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'Black'& maternal_agecat == '30-39'","G1_fore_variant == 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'missing'& maternal_agecat == '<20'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Black'& maternal_agecat == '20-29'","G1_fore_typo== 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'Asian'& maternal_agecat == '20-29'","G1_sur_del == 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Black'& maternal_agecat == '30-39'","G1_fore_typo== 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'Black'& maternal_agecat == '20-29'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Black'& maternal_agecat == '<20'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '<20'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '40+'","G1_fore_typo== 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'missing'& maternal_agecat == '20-29'","G1_fore_typo== 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'missing'& maternal_agecat == 'missing'","G0_sur_rand == 1 & G1_fore_variant == 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '<20'","G1_fore_variant == 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '<20'","G0_sur_rand == 1 & G1_fore_variant == 1 & g1surname_error != 1& ethgroup == 'missing'& maternal_agecat == 'missing'","G1_sur_ins == 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '40+'","G1_fore_variant == 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '40+'","G0_sur_rand  == 1 & G1_sur_rand == 1 & G1_fore_variant  == 1& ethgroup == 'White'& maternal_agecat == '30-39'","G1_sur_rand== 1 & G1_fore_variant== 1 & g0surname_error != 1& ethgroup == 'White'& maternal_agecat == '30-39'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '20-29'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '<20'","G0_sur_del == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '30-39'","G1_fore_variant == 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'missing'& maternal_agecat == '30-39'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Other'& maternal_agecat == '20-29'","G0_sur_rand  == 1 & G1_sur_rand == 1 & G1_fore_variant  == 1& ethgroup == 'White'& maternal_agecat == '20-29'","G0_sur_rand == 1 & G1_fore_variant == 1 & g1surname_error != 1& ethgroup == 'missing'& maternal_agecat == '20-29'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Black'& maternal_agecat == '30-39'","G1_sur_rand== 1 & G1_fore_variant== 1 & g0surname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '<20'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Other'& maternal_agecat == '30-39'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '20-29'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '30-39'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Asian'& maternal_agecat == '30-39'","G0_sur_del == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","G0_sur_ins == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","G1_fore_rand == 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '30-39'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '30-39'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == 'missing'","G1_fore_insdel== 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","G1_fore_insdel== 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '30-39'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '<20'","G1_fore_rand == 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","G1_fore_variant == 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'missing'& maternal_agecat == '20-29'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Black'& maternal_agecat == '20-29'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'Asian'& maternal_agecat == '20-29'","G1_fore_typo== 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '30-39'","G1_fore_variant == 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'missing'& maternal_agecat == 'missing'","G0_sur_rand == 1 & G1_fore_variant == 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '30-39'","G1_fore_typo== 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '<20'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '40+'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == 'missing'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '30-39'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '<20'","G0_sur_rand == 1 & G1_fore_variant == 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '20-29'","G1_sur_rand== 1 & g0surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","G0_sur_rand== 1 & G1_sur_rand== 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '<20'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '30-39'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '30-39'","G1_fore_variant == 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","G1_fore_variant == 1 & g0surname_error != 1 & g1surname_error != 1& ethgroup == 'White'& maternal_agecat == '30-39'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == 'missing'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'missing'& maternal_agecat == '20-29'","G0_sur_rand == 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '30-39'","g0surname_error != 1 & g1surname_error != 1 & g1firstname_error != 1& ethgroup == 'White'& maternal_agecat == '20-29'"]
sample_sizes = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,7,7,8,8,8,9,9,10,10,10,11,11,12,12,12,14,15,17,17,18,18,18,21,22,22,22,23,23,25,27,27,28,30,30,30,38,44,45,45,46,47,48,50,51,53,56,66,76,88,97,101,105,122,129,130,151,155,197,274,354,385,396,488,722,853,3017,4114]

sampled_df = multi_sample_data6_new2(df2, condition_list, sample_sizes, seed = 5001)


ethgroup_order = ["White", "Black", "Asian", "Other", "missing"]
matcat_order = ["<20", "20-29", "30-39", "40+", "missing"]

# Convert ethgroup to a categorical variable with the desired order
sampled_df['ethgroup'] = pd.Categorical(sampled_df['ethgroup'], categories=ethgroup_order, ordered=True)
sampled_df['maternal_agecat'] = pd.Categorical(sampled_df['maternal_agecat'], categories=matcat_order, ordered=True)
cross_tab3 = pd.crosstab(index=[sampled_df['ethgroup'], sampled_df['maternal_agecat']], columns=sampled_df['pattern'])


# if sampled_df < 13281, append from uncorrupted.
unused_id = uncorrupted_df[~uncorrupted_df['unique_id'].isin(sampled_df['unique_id'])]
unused_id = unused_id.assign(
    g1surname_error = 0,
    g1firstname_error = 0,
    g0surname_error = 0,
#    g1firstname_missing = 0
)

# append
appended_df = pd.concat([sampled_df, unused_id])
appended_df.fillna(0,inplace = True)

ethgroup_order = ["White", "Black", "Asian", "Other", "missing"]
matcat_order = ["<20", "20-29", "30-39", "40+", "missing"]

# Convert ethgroup to a categorical variable with the desired order
appended_df['ethgroup'] = pd.Categorical(appended_df['ethgroup'], categories=ethgroup_order, ordered=True)
appended_df['maternal_agecat'] = pd.Categorical(appended_df['maternal_agecat'], categories=matcat_order, ordered=True)
appended_df['maternal_agecat'].fillna("missing", inplace = True)
appended_df['ethgroup'].fillna("missing", inplace = True)

appended_df['pattern'] = appended_df[['g1surname_error', 'g0surname_error', 'g1firstname_error']].apply(lambda x: ''.join(map(str, x)), axis=1)
cross_tab4 = pd.crosstab(index=[appended_df['ethgroup'], appended_df['maternal_agecat']], columns=appended_df['pattern'], margins= True)


sampled_df = appended_df
# evaluate.


def error_rate(group):
    total_count = len(group)
    error_count = group.sum()
    return (error_count / total_count) * 100

def error_count(group):
    total_count = len(group)
    error_count = group.sum()
    return error_count, total_count

# Group the DataFrame by 'ethgroup' and 'maternal_agecat' and calculate error rates
grouped_data = sampled_df.groupby(['ethgroup', 'maternal_agecat']).agg({
    'g1surname_error': error_rate,
    'g1firstname_error': error_rate,
    'g0surname_error': error_rate
}).reset_index()

# Group the DataFrame by 'ethgroup' and 'maternal_agecat' and calculate error rates
grouped_count_data = sampled_df.groupby(['ethgroup', 'maternal_agecat']).agg({
    'g1surname_error': error_count,
    'g1firstname_error': error_count,
    'g0surname_error': error_count
}).reset_index()


# Group the DataFrame by 'maternal_agecat' and calculate error rates
error_rates_maternal_agecat = sampled_df.groupby('maternal_agecat').agg({
    'g1surname_error': error_rate,
    'g1firstname_error': error_rate,
    'g0surname_error': error_rate
}).reset_index()

# Rename the columns for clarity
error_rates_maternal_agecat.rename(columns={
    'g1surname_error': 'g1surname_error_rate',
    'g1firstname_error': 'g1firstname_error_rate',
    'g0surname_error': 'g0surname_error_rate'
}, inplace=True)

# Print the resulting DataFrame with error rates for maternal_agecat
print(error_rates_maternal_agecat)

# Group the DataFrame by 'ethgroup' and calculate error rates
error_rates_ethgroup = sampled_df.groupby('ethgroup').agg({
    'g1surname_error': error_rate,
    'g1firstname_error': error_rate,
    'g0surname_error': error_rate
}).reset_index()


error_rates_ethgroup = sampled_df.groupby('ethgroup').agg({
    'g1surname_error': error_rate,
    'g1firstname_error': error_rate,
    'g0surname_error': error_rate
}).reset_index()

# Rename the columns for clarity
error_rates_ethgroup.rename(columns={
    'g1surname_error': 'g1surname_error_rate',
    'g1firstname_error': 'g1firstname_error_rate',
    'g0surname_error': 'g0surname_error_rate'
}, inplace=True)

# Print the resulting DataFrame with error rates for ethgroup
print(error_rates_ethgroup)



error_count_ethgroup = sampled_df.groupby('ethgroup').agg({
    'g1surname_error': error_count,
    'g1firstname_error': error_count,
    'g0surname_error': error_count
}).reset_index()

error_count_ethgroup = sampled_df.groupby('ethgroup').agg({
    'g1surname_error': error_count,
    'g1firstname_error': error_count,
    'g0surname_error': error_count
}).reset_index()

sampled_df.to_csv('corrupted\\scen1\\20231027_data5.csv', encoding = "utf-8-sig") # use same naming structure for each dataset.