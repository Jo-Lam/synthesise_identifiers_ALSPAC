# synthesise_Data

Task A: Create High Fidelity Synthetic Dataset for ALSPAC
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
list created by predecessor at UCL
Comparable methods: see [this]([url](https://eprints.lse.ac.uk/115497/1/WP_342.pdf)) 
3) Firstnames: 1996-2021 Baby Birth Name with frequencies, by gender
accessed: https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/datasets/babynamesinenglandandwalesfrom1996

Problems, using 1:1 replacement method:
1) Both of the above data source doesn't have ethnicity information
2) In data source, deduplicate names, by ethnicity and gender
3) In gold-standard data, deduplicate such that there is no duplication across gender or race


Solution & Steps:
0) Download and Clean the Data Sources (0_census_name.R)
1) Prescribe Ethnicity base on only first name and only last name: Name Prism (1_Name_Prism.py)
- Getting ethnicity from names using Name Prism API
- Race (US) from Name Prism (https://name-prism.com/about)
- Request API at https://name-prism.com/api
Repeat for both Data Sources
Be considerate and limit request numbers!

2) summarise synthetic names, compare cardinality (number of factors) to original names (replacing_names.R)
Done.

Task B: Create Synthesised Data that replicates ALSPAC
- High Fidelity
- Share the same combination of ethnicity/maternal_age category
- Share the exact same N

Use of R Package Synthpop (https://www.synthpop.org.uk/get-started.html) - 3_synthesise_data.R
- problem: not all synthesised data would match combination of ethnicity/maternal_age category
- Solution: Reject Sampling - create 200 copies

Describe the synthesised datasets - 4_describe_syn_sample.r

Task C: Corruption of data 
Considerations
- field of error 
G0 Surname, G1 Surname, G1 Firstname
- types of error 
Surname: typo, insertion/deletion

3) Load data, create dictionary, create synthesised names. (replacing_names.R)
export to .csv













