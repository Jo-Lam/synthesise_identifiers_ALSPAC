
#summarize extracted data output

import pandas as pd
import glob

# Assuming all CSV files are in the same folder
files = glob.glob('corrupted\\scen0\\*.csv')  # Replace 'path_to_folder' with your directory

# Create an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Read each CSV file and combine into one DataFrame
for file in files:
    data = pd.read_csv(file)
    combined_data = combined_data.append(data)

# Grouping by 'ethgroup' and 'maternal_agecat' and calculating error rate
g1sur_error_rate_summary = combined_data.groupby(['ethgroup', 'maternal_agecat'])['g1surname_error'].mean()
g1fir_error_rate_summary = combined_data.groupby(['ethgroup', 'maternal_agecat'])['g1firstname_error'].mean()
g0sur_error_rate_summary = combined_data.groupby(['ethgroup', 'maternal_agecat'])['g0surname_error'].mean()
# Replace 'error_column' with the actual column name representing error rate in your data

cross_tab_g1sur = pd.crosstab(index=combined_data['ethgroup'], columns=combined_data['maternal_agecat'], values=combined_data['g1surname_error'], aggfunc='mean')
cross_tab_g1fir = pd.crosstab(index=combined_data['ethgroup'], columns=combined_data['maternal_agecat'], values=combined_data['g1firstname_error'], aggfunc='mean')
cross_tab_g0sur = pd.crosstab(index=combined_data['ethgroup'], columns=combined_data['maternal_agecat'], values=combined_data['g0surname_error'], aggfunc='mean')

# cross_tab_g1sur.to_csv('error_rates_cross_tab.csv', na_rep='N/A', index=True, header=True)

# Group by 'ethgroup'
g1sur_error_rate_summary_eth = combined_data.groupby(['ethgroup'])['g1surname_error'].mean()
g1fir_error_rate_summary_eth = combined_data.groupby(['ethgroup'])['g1firstname_error'].mean()
g0sur_error_rate_summary_eth = combined_data.groupby(['ethgroup'])['g0surname_error'].mean()


# Group by 'maternal_agecat'
g1sur_error_rate_summary_matcat = combined_data.groupby(['maternal_agecat'])['g1surname_error'].mean()
g1fir_error_rate_summary_matcat = combined_data.groupby(['maternal_agecat'])['g1firstname_error'].mean()
g0sur_error_rate_summary_matcat = combined_data.groupby(['maternal_agecat'])['g0surname_error'].mean()


print(g1sur_error_rate_summary)