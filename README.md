# Synthesising Names
This repo is a code repository for my paper: Generating synthetic identifiers to support development and evaluation of data linkage methods.
Please feel free to get in touch with me at joseph.lam.18@ucl.ac.uk

This includes:
1) process of creating a synthetic ALSPAC dataset
2) process of corrupting and selecting relevant synthetic data
3) process of data linkage using Splink
4) code for comparing linked data using synthetic data, compared to original linkage in ALSPAC. 

For detailed description of the methods, please refer to the manuscript (to be published).

## Creating High Fidelity Synthetic Dataset for ALSPAC
- Real ALSPAC Data is only accessible in Secure Research Environments, fake example data used to demonstrate code. (fake_testing.csv)
- As synthesised data is of high fidelity, and includes personally identifiable information, the original ALSPAC identifiers is not shared here.
- Enquiry to the dataset is welcomed to contact ALSPAC team at University of Bristol.


### Synethsising Names for this study - Considerations: 
1) Retain Name-Gender & Name-Ethnicity Association
2) Retain Name-Frequency Order
3) Retain Name Cardinality
4) Avoid any identical synthetic names with original

### To Tackle Considerations:
1) Replace Names from Data Source belonging to the same ethnic group and gender
2) Rank names by frequency
3 & 4) Use 1:1 replacement method, across first names and surnames

For example:
"John" (White, Male, Rank 1 most frequent in data) in ALSAPC surnames or first names will be replaced with 
"Peter" (White, Male,Rank 1 most frequent in data source)

### Fake Names Data Source:
1) Surnames: 1996-2018 Census Surnames with freqeuncies 
list created by predecessor at UCL (hao_output.csv)
Comparable methods: see [this]([url](https://eprints.lse.ac.uk/115497/1/WP_342.pdf)) 
3) Firstnames: 1996-2021 Baby Birth Name with frequencies, by gender
accessed: https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/datasets/babynamesinenglandandwalesfrom1996

### Problems of using 1:1 replacement method:
1) Both of the above data source doesn't have ethnicity information
2) In data source, deduplicate names, by ethnicity and gender
3) For 1:1 replacement to work, we have to make sure that there is no duplication across gender or ethnicity

## Solution to above problems & Steps:
0) Download and Clean the Data Sources - preprocessing (0_census_name.R), seperate name lists by gender
1) Prescribe Ethnicity base on only first name and only last name: Name Prism (1_Name_Prism.py)
- Getting ethnicity from names using Name Prism API
- Race (US) from Name Prism (https://name-prism.com/about)
- Request API at https://name-prism.com/api - contact the Name Prism team for API key access.
Repeat for both Data Sources
Be considerate and limit request numbers & frequency!

2) summarise synthetic names, compare cardinality (number of factors) to original names 
replace shared names across gender/ethnicity depends on count (retain option with higher cardinality)

3) Load data, create dictionary, create synthesised identifiers and attributes (without names)
Use of R Package Synthpop (https://www.synthpop.org.uk/get-started.html) - (2_synthesise_data.R)
- problem: not all synthesised data would match combination of ethnicity/maternal_age category
- Solution: Reject Sampling - create multiple copies

Describing the synthesised datasets - (3_describe_syn_sample.r)
Inspect distribution of ethnicity /maternal age category fits with original data.

4) create synthesised names (4_replacing_names.R)
This file also combines the synthesised names with the dataset, matching by ethnicity and gender where possible.

This marks the completion of creating synthetic identifiers and attribute varaibles, for 200 copies.
For my paper, I have used first 5 copies of these 200 synthetic data as gold standard. 

![Flowchart Synthetic Data work v2](https://github.com/Jo-Lam/synthesise_identifiers_ALSPAC/assets/56257474/14928f62-a283-4d67-8739-caf7dbead3ef) (Figure 2 from my paper)

For each gold-standard dataset, it will be corrupted based on 4 scenarios, creating 4 copies of corrupted synthetic dataset that has different level of fidelity compared to the gold standard synthetic data.

## Data Corruption 
Each corruption process is split into 2 steps:
1) create corrupted dataset
2) select relevant number of records (N matching the original sample for my purpose)
Corrupted synthetic datasets are then linked with gold standard synthesised dataset, and evaluated against the linkage between ARCADAIA and CHDB in ALSPAC. 

Corruption Scenarios:
![image](https://github.com/Jo-Lam/synthesise_identifiers_ALSPAC/assets/56257474/75b0008a-6ffa-4930-9c14-7bff5faaf5c6)

Error-Attribute relationship
1) Known error-attribute relationship (7_corrupt_known_scen1.py)
2) Error-attribute relationship estimated based on relative risk (6_corrupt_rr_scen2.py)
3) Independent error-attribute relationship (5_corrupt_independent_scen3_4.py)
4) Independent error-attribute relationship (5_corrupt_independent_scen3_4.py)

Drawing relavent samples from corrupted data to induce error co-occurring patterns, and error-attribute dependency
- Scen 1: 8_Drawing_corrupted_data_scen1.py
- Scen 2: 9_Drawing_corrupted_data_scen2.py
- Scen 3: 10_Drawing_corrupted_data_scen3.py
- Scen 4: 11_Drawing_corrupted_data_secn4_nopatt.py

Inspect Data:  12_inspect_drawn_samples.py

## Data linkage
Now that for each gold standard synthetic dataset, we have 4 scenarios of corrupted data, we can perform linkages between each corrupted data with the gold standard synthetic data, and compare the linkage quality metrics with the original linkage between  ALSPAC waves. Three data linkage settings were explored:
- deterministic
- probabilistic with Jaro-Winkler Similarity Scores
- probabilistic with Jaro-Winkler Similarity Scores and Term Frequency Adjustment

(13_data_linkage.py)

## Compare findings
False matches and miss matches at each scenario is summarised and compared (14_compare_linkages.py, 15_combine_outputs.py).
against original linkage in ALSPAC, which is not described here.

For results and further description of the methodology, please read my paper and the appendix materials. (links to be added)

