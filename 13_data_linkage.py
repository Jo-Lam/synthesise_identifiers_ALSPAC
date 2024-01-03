# Data Linkage - quick run


# formatting to splink
import os
import pandas as pd
import altair as alt
alt.renderers.enable('html')
# import data
import numpy as np
from splink.duckdb.linker import DuckDBLinker

# define which scenario and which dataset to be linked.
scen = 2
data_set = 1

#scen 1234
df = pd.read_csv(f"corrupted\\scen{scen}\\20231027_data{data_set}.csv") 

# for scen1, scen2 
df['unique_id'] = df['unique_id'] + 90000000


# import uncorrupted data.
directory = os.path.join(os.getcwd(), "June6batch\\June6batch")
file_name = f"accepted_sample_{data_set}.csv"
file_path = os.path.join(directory, file_name)
gold_df = pd.read_csv(file_path)


# formatting
# drop useless rows?
column_names = df.columns.tolist()
columns_to_keep = ['unique_id' , 'maternal_agecat', 'ethgroup', 'g1_gender_arc', 'imddecile', 'g1_dob_arc1', 'syn_g0_surname', 'syn_g1_surname', 'syn_g1_firstname'] 
df = df.loc[:, columns_to_keep]
# scen 0, 1
#df["g1_dob_arc1"] = pd.to_datetime(df["g1_dob_arc1"], unit = "D")

df["g1_dob_str"] = df["g1_dob_arc1"].astype(str)
df["g1_dob_str"] = df["g1_dob_str"].str[:10]
df["g1_dob_arc1"] = df["g1_dob_str"]
df.drop(columns = "g1_dob_str")

# inspect vars, code "missing" into nulls.
df['maternal_agecat'] = df['maternal_agecat'].replace('missing', np.nan)
df['ethgroup'] = df['ethgroup'].replace('missing', np.nan)
df['imddecile'] = df['imddecile'].replace('missing', np.nan)
df['syn_g1_firstname'] = df['syn_g1_firstname'].replace('missing', np.nan)
df['syn_g0_surname'] = df['syn_g0_surname'].replace('missing', np.nan)
df['syn_g1_surname'] = df['syn_g1_surname'].replace('missing', np.nan)

columns_to_keep = ['unique_id' , 'maternal_agecat', 'ethgroup', 'g1_gender_arc', 'imddecile', 'g1_dob_arc1', 'syn_g0_surname', 'syn_g1_surname', 'syn_g1_firstname'] 
df = df.loc[:, columns_to_keep]
df.head(5)

# create gold standard (with cluster), by keeping uncorrupted = True rows.
gold_df["g1_dob_arc1"] = pd.to_datetime(gold_df["g1_dob_arc1"], unit = "D")
#gold_df['g1_dob_arc1']=pd.to_datetime(gold_df['g1_dob_arc1'], format = '%d/%m/%Y') 

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

columns_to_keep = ['unique_id' , 'maternal_agecat', 'ethgroup', 'g1_gender_arc', 'imddecile', 'g1_dob_arc1', 'syn_g0_surname', 'syn_g1_surname', 'syn_g1_firstname'] 
gold_df = gold_df.loc[:, columns_to_keep]


# gold_df['g1_dob_arc1']=pd.to_datetime(df['g1_dob_arc1'].astype(str), format='%Y-%m-%d')

# deterministic
from splink.duckdb.blocking_rule_library import block_on
import splink.duckdb.comparison_template_library as ctl
import splink.duckdb.comparison_library as cl

# link_only - setting 1: basic comparison
settings_deterministic =  {
    "link_type": "link_only",
    "blocking_rules_to_generate_predictions": [
        block_on(["syn_g1_firstname", "syn_g1_surname", "syn_g0_surname", "g1_dob_arc1"]),
        block_on(["syn_g1_firstname", "syn_g0_surname", "g1_dob_arc1", "g1_gender_arc"]),
        block_on(["syn_g1_surname", "syn_g0_surname", "g1_dob_arc1", "g1_gender_arc"]),
        block_on(["syn_g1_firstname", "syn_g1_surname", "g1_dob_arc1", "g1_gender_arc"]),
        block_on(["syn_g1_firstname", "syn_g1_surname", "syn_g0_surname", "g1_gender_arc"]),
    ],  
    "comparisons": [],
    "retain_matching_columns":True,
    "retain_intermediate_calculation_columns":True,
    "additional_columns_to_retain": [
        "ethgroup",
        "imddecile",
        "maternal_agecat",
    ]
}

linker = DuckDBLinker(
    [gold_df, df],
    settings_dict= settings_deterministic,
    input_table_aliases=["df_left","df_right"]
)

df_predict = linker.deterministic_link()
df_predict.as_pandas_dataframe().head()
deterministic_scen1 = df_predict.as_pandas_dataframe()
deterministic_scen1.to_csv(f"linkage_outputs\\scen{scen}\\dataset{data_set}\\deterministic.csv")

# prob

# Define Comparisons - lower JW weights should not matter, try anyway. remove date 3 months.
import splink.duckdb.comparison_library as cl
import splink.duckdb.comparison_template_library as ctl
import splink.duckdb.comparison_level_library as cll

comparison_syn_g1_first_name = {
    "output_column_name": "syn_g1_firstname",
    "comparison_description": "G1 First name jaro winkler",
    "comparison_levels": [
        {
            "sql_condition": "syn_g1_firstname_l IS NULL OR syn_g1_firstname_r IS NULL",
            "label_for_charts": "Null",
            "is_null_level": True,
        },
        {
            "sql_condition": "syn_g1_firstname_l = syn_g1_firstname_r",
            "label_for_charts": "Exact match",
        },
        {
            "sql_condition": 'jaro_winkler_similarity("syn_g1_firstname_l", "syn_g1_firstname_r") >= 0.8',
            "label_for_charts": "Jaro_winkler_similarity 0.8",

        },
        {"sql_condition": "ELSE", "label_for_charts": "All other comparisons"},
    ],
}

comparison_syn_g0_surname = {
    "output_column_name": "syn_g0_surname",
    "comparison_description": "G0 surname jaro winkler",
    "comparison_levels": [
        {
            "sql_condition": "syn_g0_surname_l IS NULL OR syn_g0_surname_r IS NULL",
            "label_for_charts": "Null",
            "is_null_level": True,
        },
        {
            "sql_condition": "syn_g0_surname_l = syn_g0_surname_r",
            "label_for_charts": "Exact match",
        },
        {
            "sql_condition": 'jaro_winkler_similarity("syn_g0_surname_l", "syn_g0_surname_r") >= 0.8',
            "label_for_charts": "Jaro_winkler_similarity 0.8",

        },
        {"sql_condition": "ELSE", "label_for_charts": "All other comparisons"},
    ],
}

comparison_syn_g1_surname = {
    "output_column_name": "syn_g1_surname",
    "comparison_description": "G1 surname jaro winkler",
    "comparison_levels": [
        {
            "sql_condition": "syn_g1_surname_l IS NULL OR syn_g1_surname_r IS NULL",
            "label_for_charts": "Null",
            "is_null_level": True,
        },
        {
            "sql_condition": "syn_g1_surname_l = syn_g1_surname_r",
            "label_for_charts": "Exact match",
        },
        {
            "sql_condition": 'jaro_winkler_similarity("syn_g1_surname_l", "syn_g1_surname_r") >= 0.8',
            "label_for_charts": "Jaro_winkler_similarity 0.8",

        },
        {"sql_condition": "ELSE", "label_for_charts": "All other comparisons"},
    ],
}

comparison_date = {
    "output_column_name": "g1_dob_arc1",
    "comparison_description": "exact match vs anything else",
    "comparison_levels": [
        cll.null_level("g1_dob_arc1"),
        cll.exact_match_level("g1_dob_arc1", m_probability =  0.999),
        cll.else_level(m_probability = 0.001),
    ],
}

comparison_gender = {
    "output_column_name": "g1_gender_arc",
    "comparison_description": "exact match vs anything else",
    "comparison_levels": [
        cll.null_level("g1_gender_arc"),
        cll.exact_match_level("g1_gender_arc", m_probability =  0.999),
        cll.else_level(m_probability = 0.001),
    ],
}


settings_prob = {
    "link_type": "link_only",
    "probability_two_random_records_match": 1/13281,
    "blocking_rules_to_generate_predictions": [       
        block_on(["syn_g1_firstname"]),
        block_on(["syn_g1_surname"]),
        block_on(["syn_g0_surname"]),
        block_on(["g1_dob_arc1", "g1_gender_arc"]),
    ],  
    "comparisons":[
        comparison_syn_g1_first_name,
        comparison_syn_g1_surname,
        comparison_syn_g0_surname,
        comparison_date,
        comparison_gender,     
    ],
    "retain_matching_columns":True,
    "retain_intermediate_calculation_columns":True,
    "additional_columns_to_retain": [
        "ethgroup",
        "imddecile",
        "maternal_agecat",
    ]
}

linker = DuckDBLinker(
    [gold_df, df],
    settings_dict= settings_prob,
    input_table_aliases=["df_left","df_right"]
)

linker.estimate_u_using_random_sampling(max_pairs=2e7, seed = 1)
linker.estimate_m_from_label_column("unique_id")

# With threshold
threshold_values = [-7, -5, -3, 2, 3, 4, 6]
for v in threshold_values:
    results = linker.predict(threshold_match_weight = v)
    prob_linkage = results.as_pandas_dataframe()
    file_name = f"linkage_outputs//scen{scen}//dataset{data_set}//probabilistic_threshold_{v}.csv"
    prob_linkage.to_csv(file_name)


# Scenario 3
import splink.duckdb.comparison_library as cl
import splink.duckdb.comparison_template_library as ctl
import splink.duckdb.comparison_level_library as cll
# Define Comparisons 
tfcomparison_syn_g1_first_name = {
    "output_column_name": "syn_g1_firstname",
    "comparison_description": "G1 First name jaro winkler",
    "comparison_levels": [
        {
            "sql_condition": "syn_g1_firstname_l IS NULL OR syn_g1_firstname_r IS NULL",
            "label_for_charts": "Null",
            "is_null_level": True,
        },
        {
            "sql_condition": "syn_g1_firstname_l = syn_g1_firstname_r",
            "label_for_charts": "Exact match",
            "tf_adjustment_column": "syn_g1_firstname",
            "tf_adjustment_weight": 1.0,
            "tf_minimum_u_value": 0.001,
        },
        {
            "sql_condition": 'jaro_winkler_similarity("syn_g1_firstname_l", "syn_g1_firstname_r") >= 0.8',
            "label_for_charts": "Jaro_winkler_similarity 0.8",
            "tf_adjustment_column": "syn_g1_firstname",
            "tf_adjustment_weight": 0.5,
            "tf_minimum_u_value": 0.001,

        },
        {"sql_condition": "ELSE", "label_for_charts": "All other comparisons"},
    ],
}

tfcomparison_syn_g0_surname = {
    "output_column_name": "syn_g0_surname",
    "comparison_description": "G0 surname jaro winkler",
    "comparison_levels": [
        {
            "sql_condition": "syn_g0_surname_l IS NULL OR syn_g0_surname_r IS NULL",
            "label_for_charts": "Null",
            "is_null_level": True,
        },
        {
            "sql_condition": "syn_g0_surname_l = syn_g0_surname_r",
            "label_for_charts": "Exact match",
             "tf_adjustment_column": "syn_g0_surname",
            "tf_adjustment_weight": 1.0,
            "tf_minimum_u_value": 0.001,
        },
        {
            "sql_condition": 'jaro_winkler_similarity("syn_g0_surname_l", "syn_g0_surname_r") >= 0.8',
            "label_for_charts": "Jaro_winkler_similarity 0.8",
            "tf_adjustment_column": "syn_g0_surname",
            "tf_adjustment_weight": 0.5,
            "tf_minimum_u_value": 0.001,

        },
        {"sql_condition": "ELSE", "label_for_charts": "All other comparisons"},
    ],
}

tfcomparison_syn_g1_surname = {
    "output_column_name": "syn_g1_surname",
    "comparison_description": "G1 surname jaro winkler",
    "comparison_levels": [
        {
            "sql_condition": "syn_g1_surname_l IS NULL OR syn_g1_surname_r IS NULL",
            "label_for_charts": "Null",
            "is_null_level": True,
        },
        {
            "sql_condition": "syn_g1_surname_l = syn_g1_surname_r",
            "label_for_charts": "Exact match",
            "tf_adjustment_column": "syn_g1_surname",
            "tf_adjustment_weight": 1.0,
            "tf_minimum_u_value": 0.001,
        },
        {
            "sql_condition": 'jaro_winkler_similarity("syn_g1_surname_l", "syn_g1_surname_r") >= 0.8',
            "label_for_charts": "Jaro_winkler_similarity 0.8",     
            "tf_adjustment_column": "syn_g1_surname",
            "tf_adjustment_weight": 0.5,
            "tf_minimum_u_value": 0.001,

        },
        {"sql_condition": "ELSE", "label_for_charts": "All other comparisons"},
    ],
}

comparison_date = {
    "output_column_name": "g1_dob_arc1",
    "comparison_description": "exact match vs anything else",
    "comparison_levels": [
        cll.null_level("g1_dob_arc1"),
        cll.exact_match_level("g1_dob_arc1", m_probability =  0.999),
        cll.else_level(m_probability = 0.001),
    ],
}

comparison_gender = {
    "output_column_name": "g1_gender_arc",
    "comparison_description": "exact match vs anything else",
    "comparison_levels": [
        cll.null_level("g1_gender_arc"),
        cll.exact_match_level("g1_gender_arc", m_probability =  0.999),
        cll.else_level(m_probability = 0.001),
    ],
}


# Scenario 3,  probabilistic linkage with term frequency adjustment
from splink.duckdb.blocking_rule_library import block_on
settings_prob_tf = {
    "link_type": "link_only",
    "probability_two_random_records_match": 1/13281,
    "blocking_rules_to_generate_predictions":[     
        block_on(["syn_g1_firstname"]),
        block_on(["syn_g1_surname"]),
        block_on(["syn_g0_surname"]),
        block_on(["g1_dob_arc1", "g1_gender_arc"]),
    ],  
    "comparisons":[
        tfcomparison_syn_g1_first_name,
        tfcomparison_syn_g1_surname,
        tfcomparison_syn_g0_surname,
        comparison_date,
        comparison_gender,      
    ],
    "retain_matching_columns":True,
    "retain_intermediate_calculation_columns":True,
    "additional_columns_to_retain": [
        "ethgroup",
        "imddecile",
        "maternal_agecat",
    ]
}

linker = DuckDBLinker(
    [gold_df, df],
    settings_dict= settings_prob_tf,
    input_table_aliases=["df_left","df_right"]
)

linker.estimate_u_using_random_sampling(max_pairs=2e7, seed = 1)
linker.estimate_m_from_label_column("unique_id")

threshold_values = [-5, -2, -1 , -0.5, 2, 4, 5]
for v in threshold_values:
    results = linker.predict(threshold_match_weight = v)
    prob_linkage = results.as_pandas_dataframe()
    file_name = f"linkage_outputs\\scen{scen}\\dataset{data_set}\\tf_{v}.csv"
    prob_linkage.to_csv(file_name)