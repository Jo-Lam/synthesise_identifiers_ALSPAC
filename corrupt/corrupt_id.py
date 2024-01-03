def gen_uncorrupted_id(formatted_master_record, record_to_modify={}):

    record_to_modify["random_id"] = formatted_master_record["random_id"]

    return record_to_modify

def gen_uncorrupted_unique_id(formatted_master_record, record_to_modify={}):

    record_to_modify["unique_id"] = formatted_master_record["unique_id"]

    return record_to_modify