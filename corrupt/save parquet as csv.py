import pandas as pd
import os

OUT_BASE = "out_data"
WIKIDATA = "wikidata"
RAW = "raw"
PERSONS = "persons"
NAMES = "names"
PROCESSED = "processed"

# Transformed master data
TRANSFORMED = "transformed_master_data"
TRANSFORMED_MASTER_DATA = os.path.join(
    OUT_BASE,
    WIKIDATA,
    TRANSFORMED,
)

TRANSFORMED_MASTER_DATA_ONE_ROW_PER_PERSON = os.path.join(
    TRANSFORMED_MASTER_DATA, "one_row_per_person"
)

out_path = os.path.join(
    TRANSFORMED_MASTER_DATA_ONE_ROW_PER_PERSON, "transformed_master_data.parquet"
)

df = pd.read_parquet(out_path)

df.to_csv('transformed_master.csv')


# metadata = pq.read_metadata(out_path)
# metadata


# val df = spark.read.parquet(out_path).select(dod, full_names, sex_or_genderLabel, ethnicityLabel)

# con = duckdb.connect()

# sql = f"""
# select *
# from '{out_path}'
# limit 5
# """


# pd.options.display.max_columns = 1000
# df = con.execute(sql).df()
# df




# df = bn.import_example('sprinkler')
# df = bn.import_example()
# model = bn.structure_learning.fit(df)
# G = bn.plot(model)