
import pandas as pd
import numpy as np

# Given Relative Risk Ratios (RRR) for different ethnic groups
ethnic_group_rr = {
    'White': [1.0, 1.0, 1.0],  # Reference
    'Black': [1.43, 1.19, 1.05],
    'Asian': [0.34, 0.99, 0.46],
    'Other': [2.05, 1.13, 1.08],
    'missing': [0.77, 0.72, 0.89],
}

# Given Relative Risk Ratios (RRR) for different maternal age groups
maternal_age_rr = {
    '<20': [2.60, 0.57, 2.89],
    '20-29': [1.43, 0.85, 1.61],
    '30-39': [1.0, 1.0, 1.0],  # Reference
    '40+': [1.44, 1.09, 1.14],
    'missing': [2.13, 1.24, 1.50],
}

# Reference probabilities for each condition, including the probability for no error
reference_probabilities = [0.1, 0.15, 0.2]

# Calculate joint probabilities for each combination of ethnic group and maternal age group
joint_probabilities = {}

for ethgroup, eth_rr_values in ethnic_group_rr.items():
    for agecat, age_rr_values in maternal_age_rr.items():
        joint_probabilities[(ethgroup, agecat)] = []
        for t in range(len(reference_probabilities)):
            eth_prob = 1 - np.exp(-eth_rr_values[t] * 1)  # t = 1 for all
            age_prob = 1 - np.exp(-age_rr_values[t] * 1)  # t = 1 for all
            joint_prob = reference_probabilities[t] * eth_prob * age_prob
            joint_probabilities[(ethgroup, agecat)].append(joint_prob)

# Calculate the fourth term (1 - sum of the first three terms) for each combination
for key, probs in joint_probabilities.items():
    fourth_term = 1 - sum(probs)
    probs.append(fourth_term)  # Append the fourth term to the list

# Print the updated joint probabilities
for key, probs in joint_probabilities.items():
    print(key, probs)

# Print the calculated joint probabilities
for (ethgroup, agecat), prob_values in joint_probabilities.items():
    print(f'Ethnic Group: {ethgroup}, Maternal Age Category: {agecat}')
    for t, prob in enumerate(prob_values):
        print(f'Probability at condition {t+1}: {prob:.4f}')
    print()


# Define the known sample sizes for each combination of ethnic group and maternal age category
# The actual count is suppressed for the version shared on github. The numbers would not add up. Actual count from gold standard data is included in my own code. 
joint_total_samples = {
    ('White', '<20'): 400,
    ('White', '20-29'): 6000,
    ('White', '30-39'): 4000,
    ('White', '40+'): 120,
    ('White', 'missing'): 0,
    ('Black', '<20'): 20,
    ('Black', '20-29'): 70,
    ('Black', '30-39'): 40,
    ('Black', '40+'): 0,
    ('Black', 'missing'): 0,
    ('Asian', '<20'): 10,
    ('Asian', '20-29'): 60,
    ('Asian', '30-39'): 40,
    ('Asian', '40+'): 10,
    ('Asian', 'missing'): 0,
    ('Other', '<20'): 10,
    ('Other', '20-29'): 30,
    ('Other', '30-39'): 30,
    ('Other', '40+'): 10,
    ('Other', 'missing'): 0,
    ('missing', '<20'): 140,
    ('missing', '20-29'): 970,
    ('missing', '30-39'): 370,
    ('missing', '40+'): 20,
    ('missing', 'missing'): 730,
}

# Initialize a dictionary to store the simulated sample sizes
simulated_total_samples = {}

np.random.seed(43)

# Simulate known sample sizes based on joint probabilities
for key, joint_probs in joint_probabilities.items():
    expected_sample_size = np.array(joint_probs) * joint_total_samples[key]
    simulated_sample_size = np.random.multinomial(joint_total_samples[key], joint_probs)
    simulated_total_samples[key] = simulated_sample_size

for key, sample_size in simulated_total_samples.items():
    print(f'Ethnic Group: {key[0]}, Maternal Age Category: {key[1]}')
    print(f'Simulated Sample Size: {sample_size}')
    print()

# Convert the simulated_total_samples into a DataFrame
simulated_df = pd.DataFrame(simulated_total_samples).T
simulated_df['All'] = simulated_df.sum(axis=1)

simulated_df = simulated_df.reset_index()
# Create the cross-tabulation
cross_tab = pd.crosstab(index=simulated_df['level_0'], columns=simulated_df['level_1'], values = simulated_df['All'], aggfunc = 'sum', margins = True, margins_name = 'All')

# load uncorrupted
uncorrupted_df = pd.read_csv('6June_batch\\6June_batch\\accepted_sample_4.csv') 
cross_tab2 = pd.crosstab(index=[uncorrupted_df['ethgroup']],columns= uncorrupted_df['maternal_agecat'], margins= True)

# Initialize dictionaries to store the error counts
error_counts = {}
# Iterate through the simulated sample sizes
for key, sample_size in simulated_total_samples.items():
    ethgroup, maternal_agecat = key
    surname_error_count = sample_size[0]
    first_name_error_count = sample_size[1]
    g0_surname_error_count = sample_size[2]
    no_error_count = sample_size[3]
    # Create a unique key for the group
    group_key = f"ethgroup == '{ethgroup}' & maternal_agecat == '{maternal_agecat}'"
    # Split the error counts into three fields
    error_counts[group_key] = {
        "g1surname_error == 1 & g1firstname_error != 1 & g0surname_error != 1": {
            "g1surname_error": surname_error_count,
        },
        "g1firstname_error == 1 & g1surname_error != 1 & g0surname_error != 1": {
            "g1firstname_error": first_name_error_count,
        },
        "g0surname_error == 1 & g1surname_error != 1 & g1firstname_error != 1": {
            "g0surname_error": g0_surname_error_count,
        },
        "g1firstname_error != 1 & g1surname_error != 1 & g0surname_error != 1": {
            "no_error": no_error_count,
        },
    }

# Print the split error counts for each group
for group, errors in error_counts.items():
    print(group)
    print(errors)
    print()

# Initialize lists to store the error information
list_1 = []  # Group key and error type
list_2 = []  # Error count

# Iterate through the error counts
for group, errors in error_counts.items():
    for error_type, count in errors.items():
        list_1.append(f"{group} & {error_type}")
        list_2.append(count)

# Remove the keys from list_2
list_2 = [item for error_count in list_2 for item in error_count.values()]

# Print the lists
for i in range(len(list_1)):
    print(list_1[i])
    print(list_2[i])
    print()

pairs = list(zip(list_1, list_2))

# Sort the pairs based on the values in list2 in ascending order
sorted_pairs = sorted(pairs, key=lambda x: x[1])

# Extract the sorted values back into list1 and list2
list_1, list_2 = zip(*sorted_pairs)


from multi_sample_data import multi_sample_data6_new

df = pd.read_csv('corrupted\\new_corrupted\\20231027_file5_scen2_corrupted_clean.csv')

sampled_df = multi_sample_data6_new(df, list_1, list_2, seed = 5001)


ethgroup_order = ["White", "Black", "Asian", "Other", "missing"]
matcat_order = ["<20", "20-29", "30-39", "40+", "missing"]
sampled_df['ethgroup'] = pd.Categorical(sampled_df['ethgroup'], categories=ethgroup_order, ordered=True)
sampled_df['maternal_agecat'] = pd.Categorical(sampled_df['maternal_agecat'], categories=matcat_order, ordered=True)
sampled_df['pattern'] = sampled_df[['g1surname_error', 'g1firstname_error', 'g0surname_error']].apply(lambda x: ''.join(map(str, x)), axis=1)
cross_tab3 = pd.crosstab(index=[sampled_df['ethgroup'], sampled_df['maternal_agecat']], columns=sampled_df['pattern'], margins= True)


# checking 
def error_count(group):
    total_count = len(group)
    error_count = group.sum()
    return error_count, total_count


ethnic_count_data = sampled_df.groupby(['ethgroup']).agg({
    'g1surname_error': error_count,
    'g1firstname_error': error_count,
    'g0surname_error': error_count
}).reset_index()

maternal_count_data = sampled_df.groupby(['maternal_agecat']).agg({
    'g1surname_error': error_count,
    'g1firstname_error': error_count,
    'g0surname_error': error_count
}).reset_index()



def error_rate(group):
    total_count = len(group)
    error_count = group.sum()
    return (error_count / total_count) * 100

ethnic_error_rate = sampled_df.groupby(['ethgroup']).agg({
    'g1surname_error': error_rate,
    'g1firstname_error': error_rate,
    'g0surname_error': error_rate
}).reset_index()

maternal_error_rate = sampled_df.groupby(['maternal_agecat']).agg({
    'g1surname_error': error_rate,
    'g1firstname_error': error_rate,
    'g0surname_error': error_rate
}).reset_index()

sampled_df.to_csv('corrupted\\scen2\\20231027_data5.csv')