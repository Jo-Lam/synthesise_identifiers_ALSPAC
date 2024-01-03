from cmath import nan
from queue import Empty
import numpy as np
import functools
import random
import pandas as pd

from corrupt.geco_corrupt import CorruptValueQuerty, position_mod_uniform


@functools.lru_cache(maxsize=None)
def get_given_name_alternatives_lookup():
    in_path = "out_data/wikidata/processed/alt_name_lookups/given_name_lookup.parquet"
    df = pd.read_parquet(in_path).set_index("original_name")
    return df.to_dict(orient="index")


@functools.lru_cache(maxsize=None)
def get_family_name_alternatives_lookup():
    in_path = "out_data/wikidata/processed/alt_name_lookups/family_name_lookup.parquet"
    df = pd.read_parquet(in_path).set_index("original_name")
    return df.to_dict(orient="index")


def full_name_gen_uncorrupted_record(master_record, record_to_modify={}):
    record_to_modify["full_name"] = master_record["humanLabel"][0]
    return record_to_modify

def first_name_gen_uncorrupted_record(master_record, record_to_modify={}):
    record_to_modify["given_nameLabel"] = master_record["given_nameLabel"][0]
    return record_to_modify

def last_name_gen_uncorrupted_record(master_record, record_to_modify={}):
    record_to_modify["family_nameLabel"] = master_record["family_nameLabel"][0]
    return record_to_modify

def full_name_alternative(formatted_master_record, record_to_modify={}):
    """Choose an alternative full name if one exists"""

    options = formatted_master_record["full_name_arr"]
    if options is None:
        record_to_modify["full_name"] = None
    elif len(options) == 1:
        record_to_modify["full_name"] = options[0]
    else:
        record_to_modify["full_name"] = np.random.choice(options).lower()
    return record_to_modify


def each_name_alternatives(formatted_master_record, record_to_modify={}):
    """Choose a full name if one exists"""

    options = str(formatted_master_record["full_name_arr"])

    if options is None:
        record_to_modify["full_name"] = None
        return record_to_modify

    full_name = options[0]

    names = full_name.split(" ")

    given_name_alt_lookup = get_given_name_alternatives_lookup()
    family_name_alt_lookup = get_family_name_alternatives_lookup()

    output_names = []
    for n in names:
        n = n.lower()
        if n in given_name_alt_lookup:
            name_dict = given_name_alt_lookup[n]
            alt_names = name_dict["alt_name_arr"]
            weights = name_dict["alt_name_weight_arr"]
            output_names.append(np.random.choice(alt_names, p=weights))

        elif n in family_name_alt_lookup:
            name_dict = family_name_alt_lookup[n]
            alt_names = name_dict["alt_name_arr"]
            weights = name_dict["alt_name_weight_arr"]
            output_names.append(np.random.choice(alt_names, p=weights))

        else:
            output_names.append(n)

    record_to_modify["full_name"] = " ".join(output_names).lower()

    return record_to_modify


def full_name_typo(formatted_master_record, record_to_modify={}):

    options = formatted_master_record["full_name_arr"]

    if options is None:
        record_to_modify["full_name"] = None
        return record_to_modify

    full_name = options[0]

    querty_corruptor = CorruptValueQuerty(
        position_function=position_mod_uniform, row_prob=0.5, col_prob=0.5
    )

    record_to_modify["full_name"] = querty_corruptor.corrupt_value(full_name)

    return record_to_modify

def name_inversion(formatted_master_record, record_to_modify):

    given = formatted_master_record["given_nameLabel"]
    family = formatted_master_record["family_nameLabel"]

    if len(given) > 0 and len(family) > 0:
        full_name = family[0] + " " + given[0]
    record_to_modify["full_name"] = full_name.lower()

    return record_to_modify

# Version 1
def full_name_null(formatted_master_record, record_to_modify={}):

    new_name = formatted_master_record["full_name_arr"][0].split(" ")

    try:
        first = new_name.pop(0)
    except IndexError:
        first = None
    try:
        last = new_name.pop()
    except IndexError:
        last = None

    # Erase middle names with probability 0.5
    new_name = [n for n in new_name if random.uniform(0, 1) > 0.5]

    # Erase first or last name with prob null prob

    if random.uniform(0, 1) > 1 / 2:
        first = None
    if random.uniform(0, 1) > 1 / 2:
        last = None

    new_name = [first] + new_name + [last]

    new_name = [n for n in new_name if n is not None]
    if len(new_name) > 0:
        record_to_modify["full_name"] = " ".join(new_name)
    else:
        record_to_modify["full_name"] = None
    return record_to_modify


# error: Multiple First/Last Names, remove parts of their names.
import re

def full_name_null2(formatted_master_record, record_to_modify={}):

    new_name = re.split(r'[\s-]+', formatted_master_record["full_name_arr"])
    if len(new_name) >= 3:
        for i in range(len(new_name),0, -1):
            new_name.pop(random.randint(0,i-1))
            record_to_modify["full_name"] = " ".join(new_name)
            break
    elif len(new_name) == 2:
        if random.uniform(0, 1) == 0:
            new_name.pop(0)
            record_to_modify["full_name"] = new_name
        elif random.uniform(0, 1) == 1:
            new_name.pop(1)
            record_to_modify["full_name"] = new_name
    elif len(new_name) == 1 or len(new_name) == 0:
        record_to_modify["full_name"] == None
    return record_to_modify


"""
# error: Swapped first and surname
def swapped_name_error(formatted_master_record, record_to_modify={}):
 
   options = formatted_master_record["full_name"]

    if options is None:
        record_to_modify["full_name"] = None
        return record_to_modify

    full_name = options[0]

    names = full_name.split(" ")

    output_names = []
    for n in names:
    n = n.lower()
        if n[1] == n[2]:
            pass
        elif n[1] != n[2]
            output_names.append(n)
    
    record_to_modify["full_name"] = " ".join(output_names[::-1]).lower()
    return record_to_modify

"""

    
def last_name_random_wiki(formatted_master_record, record_to_modify={}):
    
    options = formatted_master_record["full_name_arr"]

    if options is None:
        record_to_modify["full_name"] = None
        return record_to_modify

    full_name = options[0]

    names = full_name.split(" ")

    output_names = []
    for n in names:
        n = n.lower()
        n[0] = random.choice(formatted_master_record["humanLabel"])

        output_names.append(n)

    record_to_modify["full_name"] = " ".join(output_names).lower()

    return record_to_modify


def first_name_alternatives(formatted_master_record, record_to_modify={}):
    """ choose alternative first names"""
    
    given = formatted_master_record["given_nameLabel"]
    
    if given is None:
        record_to_modify["given_nameLabel"] = None
        return record_to_modify
    

    given_name_alt_lookup = get_given_name_alternatives_lookup()
    
    output_names = []
    for n in given:
        n = n.lower()
        if n in given_name_alt_lookup:
            name_dict = given_name_alt_lookup[n]
            alt_names = name_dict["alt_name_arr"]
            weights = name_dict["alt_name_weight_arr"]
            output_names.append(np.random.choice(alt_names, p=weights))
            
        else:
            output_names.append(n)

    record_to_modify["given_nameLabel"] = " ".join(output_names).lower()

    return record_to_modify

def first_name_insertion(formatted_master_record, record_to_modify):
    """insertion of extra term in first name"""
    given = formatted_master_record["given_nameLabel"][0]

    if given is None:
        record_to_modify["given_nameLabel"] = None
        return record_to_modify
    
    if len(given) == 1:
        given_extra = given[0] + " " + random.choice(formatted_master_record["given_nameLabel"])
        record_to_modify["given_nameLabel"] = given_extra.lower()
    elif given is None:
        record_to_modify["given_nameLabel"] = None
        return record_to_modify
    elif len(given) == 2:
        given_extra = given[0] + " " + given[1] + " " + random.choice(formatted_master_record["given_nameLabel"])
        record_to_modify["given_nameLabel"] = given_extra.lower()
    elif len(given) == 3:
        given_extra = given[0] + " " + given[1] + " " + given[2] + random.choice(formatted_master_record["given_nameLabel"])
        record_to_modify["given_nameLabel"] = given_extra.lower()

    return record_to_modify

def first_name_deletion(formatted_master_record, record_to_modify):
    """deletion of extra term in first name"""
    if len(formatted_master_record["given_nameLabel"][0]) == 1:
        record_to_modify["given_nameLabel"] = formatted_master_record["given_nameLabel"][0]
        
    new_name = formatted_master_record["given_nameLabel"][0].split(" ")
    # new_name = new_name.split("-") # remove hyphens in first name
    
    try:
        first_term_removed = new_name.pop(0)
    except IndexError:
        first_term_removed = None
    try:
        second_term_removed = new_name.pop(1)
    except IndexError:
        second_term_removed = None
    try:
        third_term_removed = new_name.pop(2)
    except IndexError:
        third_term_removed = None
        
    # count number of terms, and condition on it
    if len(new_name) >= 4:
        new_name = third_term_removed
        record_to_modify["given_nameLabel"] = new_name
    elif len(new_name) == 3:
        new_name = second_term_removed
        record_to_modify["given_nameLabel"] = new_name
    elif len(new_name) == 2:
        new_name = first_term_removed
        record_to_modify["given_nameLabel"] = new_name
    elif len(new_name) == 1:
        record_to_modify["given_nameLabel"] = new_name

       
    return record_to_modify



def last_name_insertion(formatted_master_record, record_to_modify):
    """insert extra term in surname"""
    
    options = formatted_master_record["family_nameLabel"]
    
    if options is None:
        record_to_modify["family_nameLabel"] = None
        return record_to_modify
    
    lastname_orig = options[0]
    extra = options[0]
    
    for n in extra:
        n = n.lower()
        n[-1] = random.choice(formatted_master_record["family_nameLabel"])
    
    record_to_modify["family_nameLabel"] = lastname_orig.lower() + " " + extra[0]
                                                
    return record_to_modify


def last_name_deletion(formatted_master_record, record_to_modify):
    """deletion of extra term in surname"""
    if len(formatted_master_record["family_nameLabel"][0]) == 1:
        record_to_modify["family_nameLabel"] = formatted_master_record["family_nameLabel"][0]
        
    new_name = formatted_master_record["family_nameLabel"][0].split(" ")
    new_name = new_name.split("-") # do not remove hyphens in last name
    
    try:
        first_term_removed = new_name.pop(0)
    except IndexError:
        first_term_removed = None
    try:
        second_term_removed = new_name.pop(1)
    except IndexError:
        second_term_removed = None
    try:
        third_term_removed = new_name.pop(2)
    except IndexError:
        third_term_removed = None
        
    # count number of terms, and condition on it
    if len(new_name) >= 4:
        new_name = third_term_removed
        record_to_modify["family_nameLabel"] = new_name
    elif len(new_name) == 3:
        new_name = second_term_removed
        record_to_modify["family_nameLabel"] = new_name
    elif len(new_name) == 2 and random.uniform(0, 1) >= 0.6:
        new_name = first_term_removed
        record_to_modify["family_nameLabel"] = new_name
    elif len(new_name) == 2 and random.uniform(0, 1) < 0.6:
        new_name = second_term_removed
        record_to_modify["family_nameLabel"] = new_name

       
    return record_to_modify


def first_name_typo(formatted_master_record, record_to_modify={}):

    options = formatted_master_record["given_nameLabel"]

    if options is None:
        record_to_modify["given_nameLabel"] = None
        return record_to_modify

    first_name = options[0]

    querty_corruptor = CorruptValueQuerty(
        position_function=position_mod_uniform, row_prob=0.5, col_prob=0.5
    )

    record_to_modify["given_nameLabel"] = querty_corruptor.corrupt_value(first_name)

    return record_to_modify

def last_name_typo(formatted_master_record, record_to_modify={}):

    options = formatted_master_record["family_nameLabel"]

    if options is None:
        record_to_modify["family_nameLabel"] = None
        return record_to_modify

    last_name = options[0]

    querty_corruptor = CorruptValueQuerty(
        position_function=position_mod_uniform, row_prob=0.5, col_prob=0.5
    )

    record_to_modify["family_nameLabel"] = querty_corruptor.corrupt_value(last_name)

    return record_to_modify

######################################
# FOR ALSPAC 
######################################

def alspac_G1_first_name_gen_uncorrupted_record(formatted_master_record, record_to_modify={}):
    record_to_modify["syn_g1_firstname"] = formatted_master_record["syn_g1_firstname"] 
    return record_to_modify

def alspac_G1_surname_gen_uncorrupted_record(formatted_master_record, record_to_modify={}):
    record_to_modify["syn_g1_surname"] = formatted_master_record["syn_g1_surname"] 
    return record_to_modify

def alspac_G0_surname_gen_uncorrupted_record(formatted_master_record, record_to_modify={}):
    record_to_modify["syn_g0_surname"] = formatted_master_record["syn_g0_surname"] 
    return record_to_modify

# Random first name (Random non-diminutive first name)
def alspac_first_name_random(formatted_master_record, record_to_modify={}):
    
    orig_firstname = formatted_master_record['syn_g1_firstname']
    first_name_alt_lookup = get_given_name_alternatives_lookup()
    new_firstname = random.choice(list(first_name_alt_lookup.keys()))

    if new_firstname == orig_firstname or new_firstname.startswith("q1") == True or new_firstname.startswith("q2") == True or new_firstname.startswith("q3") == True or new_firstname.startswith("q4") == True or new_firstname.startswith("q5") == True or new_firstname.startswith("q6") == True or new_firstname.startswith("q7") == True or new_firstname.startswith("q8") == True or new_firstname.startswith("q9") == True:
        new_firstname = random.choice(list(first_name_alt_lookup.keys()))
        

    if orig_firstname is None or str(orig_firstname).lower()=="nan":
        record_to_modify["syn_g1_firstname"] = None
        record_to_modify["random_first_corrupt"] = 2
        return record_to_modify

    record_to_modify["syn_g1_firstname"] = new_firstname
    record_to_modify["random_first_corrupt"] = 1
    return record_to_modify


#random G1 last name - married/devorced


def alspac_G1_surname_random(formatted_master_record, record_to_modify={}):
    
    orig_surname = formatted_master_record['syn_g1_surname']
    family_name_alt_lookup = get_family_name_alternatives_lookup()
    new_surname = random.choice(list(family_name_alt_lookup.keys()))
    while new_surname == orig_surname or new_surname.startswith("q1") == True or new_surname.startswith("q2") == True or new_surname.startswith("q3") == True or new_surname.startswith("q4") == True or new_surname.startswith("q5") == True or new_surname.startswith("q6") == True or new_surname.startswith("q7") == True or new_surname.startswith("q8") == True or new_surname.startswith("q9") == True:
        new_surname = random.choice(list(family_name_alt_lookup.keys()))
        if new_surname != orig_surname:
            continue

    if orig_surname is None or str(orig_surname).lower()=="nan":
        record_to_modify["syn_g1_surname"] = None
        record_to_modify["G1_last_name_random_corrupt"] = 2
        return record_to_modify

    record_to_modify["syn_g1_surname"] = new_surname
    record_to_modify["G1_last_name_random_corrupt"] = 1
    return record_to_modify


def alspac_G1_surname_random(formatted_master_record, record_to_modify={}):
    
    orig_surname = formatted_master_record['syn_g1_surname']
    family_name_alt_lookup = get_family_name_alternatives_lookup()
    new_surname = random.choice(list(family_name_alt_lookup.keys()))
    while new_surname == orig_surname or new_surname.startswith("q1") == True or new_surname.startswith("q2") == True or new_surname.startswith("q3") == True or new_surname.startswith("q4") == True or new_surname.startswith("q5") == True or new_surname.startswith("q6") == True or new_surname.startswith("q7") == True or new_surname.startswith("q8") == True or new_surname.startswith("q9") == True:
        new_surname = random.choice(list(family_name_alt_lookup.keys()))
        if new_surname != orig_surname:
            continue

    if orig_surname is None or str(orig_surname).lower()=="nan":
        record_to_modify["syn_g1_surname"] = None
        record_to_modify["G1_last_name_random_corrupt"] = 2
        return record_to_modify

    record_to_modify["syn_g1_surname"] = new_surname
    record_to_modify["G1_last_name_random_corrupt"] = 1
    return record_to_modify

#random G0 last name - married/devorced
def alspac_G0_surname_random(formatted_master_record, record_to_modify={}):
    
    orig_surname = formatted_master_record['syn_g0_surname']
    family_name_alt_lookup = get_family_name_alternatives_lookup()
    new_surname = random.choice(list(family_name_alt_lookup.keys()))

    while new_surname == orig_surname or new_surname.startswith("q1") == True or new_surname.startswith("q2") == True or new_surname.startswith("q3") == True or new_surname.startswith("q4") == True or new_surname.startswith("q5") == True or new_surname.startswith("q6") == True or new_surname.startswith("q7") == True or new_surname.startswith("q8") == True or new_surname.startswith("q9") == True:
        new_surname = random.choice(list(family_name_alt_lookup.keys()))
        if new_surname != orig_surname:
            continue

    if orig_surname is None or str(orig_surname).lower()=='nan':
        record_to_modify["syn_g0_surname"] = None
        record_to_modify["G0_last_name_random_corrupt"] = 2
        return record_to_modify

    record_to_modify["syn_g0_surname"] = new_surname
    record_to_modify["G0_last_name_random_corrupt"] = 1
    return record_to_modify

#alspac alternative first names

def alspac_first_name_alternatives(formatted_master_record, record_to_modify={}):
    """ choose alternative first names"""
    
    given = formatted_master_record["syn_g1_firstname"]
    
    if given is None or given == "" or str(given).lower() == "nan":
        record_to_modify["syn_g1_firstname"] = None
        record_to_modify["first_name_variants_corrupt"] = 2
        return record_to_modify
    

    given_name_alt_lookup = get_given_name_alternatives_lookup()
    
    output_names = []

    if str(given).lower() in given_name_alt_lookup:
        name_dict = given_name_alt_lookup[str(given).lower()]
        alt_names = name_dict["alt_name_arr"]
        weights = name_dict["alt_name_weight_arr"]
        output_names.append(np.random.choice(alt_names, p=weights))
        record_to_modify["syn_g1_firstname"] = str(output_names[0])
        record_to_modify["first_name_variants_corrupt"] = 1 
    else:
        if record_to_modify["syn_g1_firstname"] != given:
            record_to_modify["syn_g1_firstname"] = record_to_modify["syn_g1_firstname"]
            record_to_modify["first_name_variants_corrupt"] = 2
        
        else:
            output_names.append(given)
            record_to_modify["syn_g1_firstname"] = given
            record_to_modify["first_name_variants_corrupt"] = 2


    return record_to_modify

def alspac_first_name_insertion(formatted_master_record, record_to_modify):
    """insertion of extra term in first name"""
    given = str(formatted_master_record['syn_g1_firstname'])
    first_name_alt_lookup = get_given_name_alternatives_lookup()
    new_firstname = str(random.choice(list(first_name_alt_lookup.keys())))
    if new_firstname.startswith("q1") == True or new_firstname.startswith("q2") == True or new_firstname.startswith("q3") == True or new_firstname.startswith("q4") == True or new_firstname.startswith("q5") == True or new_firstname.startswith("q6") == True or new_firstname.startswith("q7") == True or new_firstname.startswith("q8") == True or new_firstname.startswith("q9") == True:
        new_firstname = str(random.choice(list(first_name_alt_lookup.keys())))

    if given is None or given == "" or str(given).lower() == "nan": 
       record_to_modify["syn_g1_firstname"] = None
       record_to_modify["first_name_insertion_corrupt"] = 2
       return record_to_modify
    else:
        record_to_modify["syn_g1_firstname"] = given + " " + new_firstname
        record_to_modify["first_name_insertion_corrupt"] = 1
        return record_to_modify

def alspac_first_name_deletion(formatted_master_record, record_to_modify):
    orig_firstname = formatted_master_record['syn_g1_firstname']
    """deletion of extra term in first name"""
    num_of_terms = str(orig_firstname).count(" ")  
    if num_of_terms == 0 or str(orig_firstname).lower() == "nan":
        record_to_modify["first_name_deletion_corrupt"] = 2 
        if record_to_modify["syn_g1_firstname"] != orig_firstname:
            record_to_modify["syn_g1_firstname"] = record_to_modify["syn_g1_firstname"]
        else:
            record_to_modify["syn_g1_firstname"] = orig_firstname 
        return record_to_modify
        
    
    # new_name = new_name.split("-") # remove hyphens in first name
    new_name = orig_firstname.split(" ")
    if num_of_terms == 1:
        first_term = new_name.pop(0)
        second_term = new_name.pop(0)
    elif num_of_terms == 2:
        first_term = new_name.pop(0)
        second_term = new_name.pop(0)
        third_term = new_name.pop(0)
    elif num_of_terms >= 3:
        first_term = new_name.pop(0)
        second_term = new_name.pop(0)
        third_term = new_name.pop(0)
        forth_term = new_name.pop(0)


    # count number of terms, and condition on it
    if num_of_terms >= 3:
        if random.randint(1,4)==1:
            new_name = second_term.lower() + " " + third_term.lower() + " " + forth_term.lower()
            record_to_modify["syn_g1_firstname"] = str(new_name)
        elif random.randint(1,4)==2:
            new_name = first_term.lower() + " " + third_term.lower() + " " + forth_term.lower()
            record_to_modify["syn_g1_firstname"] = str(new_name)
        elif random.randint(1,4)==3:
            new_name = first_term.lower() + " " + second_term.lower() + " " + forth_term.lower()
            record_to_modify["syn_g1_firstname"] = str(new_name)
        elif random.randint(1,4)==4:
            new_name = first_term.lower() + " " + second_term.lower() + " " + third_term.lower()
            record_to_modify["syn_g1_firstname"] = str(new_name)
    elif num_of_terms == 2:
        if random.randint(1,3)==1:
            new_name = second_term.lower() + " " + third_term.lower()
            record_to_modify["syn_g1_firstname"] = str(new_name)
        elif random.randint(1,3)==2:
            new_name = first_term.lower() + " " + third_term.lower()
            record_to_modify["syn_g1_firstname"] = str(new_name)
        elif random.randint(1,3)==3:
            new_name = second_term.lower() + " " + third_term.lower()
            record_to_modify["syn_g1_firstname"] = str(new_name)
    elif num_of_terms == 1:
        if random.randint(1,2)==1:
            new_name = first_term
            record_to_modify["syn_g1_firstname"] = str(new_name)
        elif random.randint(1,2)==2:
            new_name = second_term
            record_to_modify["syn_g1_firstname"] = str(new_name)
    
    record_to_modify["first_name_deletion_corrupt"] = 1
    return record_to_modify


def alspac_G1_last_name_insertion(formatted_master_record, record_to_modify):
    """insert extra term in surname"""
    
    options = str(formatted_master_record['syn_g1_surname'])
    
    lastname_orig = options
    family_name_alt_lookup = get_family_name_alternatives_lookup()
    new_surname = str(random.choice(list(family_name_alt_lookup.keys())))
    while new_surname.startswith("q1") == True or new_surname.startswith("q2") == True or new_surname.startswith("q3") == True or new_surname.startswith("q4") == True or new_surname.startswith("q5") == True or new_surname.startswith("q6") == True or new_surname.startswith("q7") == True or new_surname.startswith("q8") == True or new_surname.startswith("q9") == True:
        new_surname = str(random.choice(list(family_name_alt_lookup.keys())))

    if options is None or options == "" or options.lower() == "nan":
        record_to_modify["syn_g1_surname"] = new_surname
    else:
        record_to_modify["syn_g1_surname"] = lastname_orig.lower() + " " + new_surname.lower()
    
    record_to_modify["G1_last_name_insertion_corrupt"] = 1
    return record_to_modify


def alspac_G1_last_name_deletion(formatted_master_record, record_to_modify):
    """deletion of extra term in surname"""

    orig_lastname = formatted_master_record['syn_g1_surname']
    num_of_terms = str(orig_lastname).count(" ")
    if num_of_terms == 0 or str(orig_lastname).lower() == "nan":
        record_to_modify["G1_last_name_deletion_corrupt"] = 2
        record_to_modify["syn_g1_surname"] = orig_lastname
        return record_to_modify 
        
    
    # new_name = new_name.split("-") # remove hyphens in first name
    new_name = orig_lastname.split(" ")
    if num_of_terms == 1:
        first_term = new_name.pop(0)
        second_term = new_name.pop(0)
    elif num_of_terms == 2:
        first_term = new_name.pop(0)
        second_term = new_name.pop(0)
        third_term = new_name.pop(0)
    elif num_of_terms >= 3:
        first_term = new_name.pop(0)
        second_term = new_name.pop(0)
        third_term = new_name.pop(0)
        forth_term = new_name.pop(0)


    # count number of terms, and condition on it
    if num_of_terms >= 3:
        if random.randint(1,4)==1:
            new_name = second_term.lower() + " " + third_term.lower() + " " + forth_term.lower()
            record_to_modify["syn_g1_surname"] = str(new_name)
        elif random.randint(1,4)==2:
            new_name = first_term.lower() + " " + third_term.lower() + " " + forth_term.lower()
            record_to_modify["syn_g1_surname"] = str(new_name)
        elif random.randint(1,4)==3:
            new_name = first_term.lower() + " " + second_term.lower() + " " + forth_term.lower()
            record_to_modify["syn_g1_surname"] = str(new_name)
        elif random.randint(1,4)==4:
            new_name = first_term.lower() + " " + second_term.lower() + " " + third_term.lower()
            record_to_modify["syn_g1_surname"] = str(new_name)
    elif num_of_terms == 2:
        if random.randint(1,3)==1:
            new_name = second_term.lower() + " " + third_term.lower()
            record_to_modify["syn_g1_surname"] = str(new_name)
        elif random.randint(1,3)==2:
            new_name = first_term.lower() + " " + third_term.lower()
            record_to_modify["syn_g1_surname"] = str(new_name)
        elif random.randint(1,3)==3:
            new_name = first_term.lower() + " " + second_term.lower()
            record_to_modify["syn_g1_surname"] = str(new_name)
    elif num_of_terms == 1:
        if random.randint(1,2)==1:
            new_name = first_term
            record_to_modify["syn_g1_surname"] = str(new_name)
        elif random.randint(1,2)==2:
            new_name = second_term
            record_to_modify["syn_g1_surname"] = str(new_name)

    record_to_modify["G1_last_name_deletion_corrupt"] = 1
    return record_to_modify

def alspac_G0_last_name_insertion(formatted_master_record, record_to_modify):
    """insert extra term in surname"""
    
    options = str(formatted_master_record["syn_g0_surname"])

    
    lastname_orig = options
    family_name_alt_lookup = get_family_name_alternatives_lookup()
    new_surname = str(random.choice(list(family_name_alt_lookup.keys())))
    while new_surname.startswith("q1") == True or new_surname.startswith("q2") == True or new_surname.startswith("q3") == True or new_surname.startswith("q4") == True or new_surname.startswith("q5") == True or new_surname.startswith("q6") == True or new_surname.startswith("q7") == True or new_surname.startswith("q8") == True or new_surname.startswith("q9") == True:
        new_surname = str(random.choice(list(family_name_alt_lookup.keys())))

    if options is None or options == "" or options.lower() == "nan":
        record_to_modify["syn_g0_surname"] = new_surname
    else:
        record_to_modify["syn_g0_surname"] = lastname_orig.lower() + " " + new_surname.lower()                                              
    record_to_modify["G0_last_name_insertion_corrupt"] = 1
    return record_to_modify


def alspac_G0_last_name_deletion(formatted_master_record, record_to_modify):
    """deletion of extra term in surname"""

    orig_lastname = formatted_master_record['syn_g0_surname']
    num_of_terms = str(orig_lastname).count(" ")
    if num_of_terms == 0 or str(orig_lastname).lower() == "nan":
        record_to_modify["G0_last_name_deletion_corrupt"] = 2
        record_to_modify["syn_g0_surname"] = orig_lastname
        return record_to_modify
        
    
    # new_name = new_name.split("-") # remove hyphens in first name
    new_name = orig_lastname.split(" ")
    if num_of_terms == 1:
        first_term = new_name.pop(0)
        second_term = new_name.pop(0)
    elif num_of_terms == 2:
        first_term = new_name.pop(0)
        second_term = new_name.pop(0)
        third_term = new_name.pop(0)
    elif num_of_terms >= 3:
        first_term = new_name.pop(0)
        second_term = new_name.pop(0)
        third_term = new_name.pop(0)
        forth_term = new_name.pop(0)


    # count number of terms, and condition on it
    if num_of_terms >= 3:
        if random.randint(1,4)==1:
            new_name = second_term.lower() + " " + third_term.lower() + " " + forth_term.lower()
            record_to_modify["syn_g0_surname"] = str(new_name)
        elif random.randint(1,4)==2:
            new_name = first_term.lower() + " " + third_term.lower() + " " + forth_term.lower()
            record_to_modify["syn_g0_surname"] = str(new_name)
        elif random.randint(1,4)==3:
            new_name = first_term.lower() + " " + second_term.lower() + " " +  forth_term.lower()
            record_to_modify["syn_g0_surname"] = str(new_name)
        elif random.randint(1,4)==4:
            new_name = first_term.lower() + " " + second_term.lower() + " " + third_term.lower() 
            record_to_modify["syn_g0_surname"] = str(new_name)
    elif num_of_terms == 2:
        if random.randint(1,3)==1:
            new_name = second_term.lower() + " " + third_term.lower()
            record_to_modify["syn_g0_surname"] = str(new_name)
        elif random.randint(1,3)==2:
            new_name = first_term.lower() + " " + third_term.lower()
            record_to_modify["syn_g0_surname"] = str(new_name)
        elif random.randint(1,3)==3:
            new_name = first_term.lower() + " " + second_term.lower()
            record_to_modify["syn_g0_surname"] = str(new_name)
    elif num_of_terms == 1:
        if random.randint(1,2)==1:
            new_name = first_term
            record_to_modify["syn_g0_surname"] = str(new_name)
        elif random.randint(1,2)==2:
            new_name = second_term
            record_to_modify["syn_g0_surname"] = str(new_name)

    record_to_modify["G0_last_name_deletion_corrupt"] = 1
    return record_to_modify


def alspac_first_name_typo(formatted_master_record, record_to_modify={}):

    options = str(formatted_master_record["syn_g1_firstname"])

    if options is None or options == "" or options.lower() == "nan":
        record_to_modify["first_name_typo_corrupt"] = 2
        record_to_modify["syn_g1_firstname"] = None
        return record_to_modify

    first_name = options

    querty_corruptor = CorruptValueQuerty(
        position_function=position_mod_uniform, row_prob=0.5, col_prob=0.5
    )

    record_to_modify["syn_g1_firstname"] = querty_corruptor.corrupt_value(first_name)
    record_to_modify["first_name_typo_corrupt"] = 1
    return record_to_modify

def alspac_G1_last_name_typo(formatted_master_record, record_to_modify={}):

    options = str(formatted_master_record["syn_g1_surname"])

    if options is None or options == "" or options.lower() == "nan":
        record_to_modify["syn_g1_surname"] = None
        return record_to_modify

    last_name = options

    querty_corruptor = CorruptValueQuerty(
        position_function=position_mod_uniform, row_prob=0.5, col_prob=0.5
    )

    record_to_modify["syn_g1_surname"] = querty_corruptor.corrupt_value(last_name)

    return record_to_modify

def alspac_G0_last_name_typo(formatted_master_record, record_to_modify={}):

    options = str(formatted_master_record["syn_g0_surname"])

    if options is None or options == "":
        record_to_modify["syn_g0_surname"] = None
        return record_to_modify

    last_name = options

    querty_corruptor = CorruptValueQuerty(
        position_function=position_mod_uniform, row_prob=0.5, col_prob=0.5
    )

    record_to_modify["syn_g0_surname"] = querty_corruptor.corrupt_value(last_name)

    return record_to_modify

def alspac_name_inversion(formatted_master_record, record_to_modify):

    given = str(formatted_master_record["syn_g1_firstname"])
    family = str(formatted_master_record["syn_g1_surname"])

    if len(given) > 0 and len(family) > 0:
       record_to_modify["syn_g1_firstname"] = family
       record_to_modify["syn_g1_surname"] = given
    return record_to_modify