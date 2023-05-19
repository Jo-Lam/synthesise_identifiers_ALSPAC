# synthesise_names

Task: Create High Fidelity Synthetic Dataset for ALSPAC
Real ALSPAC Data is only accessible in Secure Research Environments, fake example data used to develop code. (fake_testing.csv)

Considerations: 
1) Retain Name-Ethnicity Association
2) Retain Name-Frequency Order
3) Retain Name Cardinality
4) Avoid any identical synthetic names with original

To Tackle Considerations:
1) Replace Names from Data Source with the same ethnic group
2) Rank names by frequency
3 & 4) Use 1:1 replacement method, across first names and surnames

For example:
"John" (White, Male, Rank 1 most Frequent in Data) in ALSAPC surnames or first names will be replaced with 
"Peter" (White, Male,Rank 1 most Frequent in Data Source)

Fake Names Data Source:
1) Surnames: 1996-2018 Census Surnames with freqeuncies (gender-free)
2) Firstnames: 1996-2018 Baby Birth Name with frequencies, by gender

Problems, using 1:1 replacement method:
1) Both of the above data source doesn't have ethnicity information
2) In data source, deduplicate names, by ethnicity and gender
3) In gold-standard data, deduplicate such that there is no duplication across gender or race


Solution & Steps:
0) Download and Clean the Data Sources (census_name.R)
1) Prescribe Ethnicity base on only first name and only last name: Name Prism (Name_Prism.py)
- Getting ethnicity from names using Name Prism API
- Race (US) from Name Prism (https://name-prism.com/about)
- Request API at https://name-prism.com/api
Repeat for both Data Sources

2) Load data, create dictionary, create synthesised names. (replacing_names.R)
export to .csv

3) summarise synthetic names, compare cardinality (number of factors) to original names (replacing_names.R)
Done.






