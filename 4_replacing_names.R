# 1:1 Names Dictionary/Replacement

# Step 0: Consider First Names and Last Names together (separate Male and Female Names)
# Step 1: inspect if there are duplicated male/female names in data & dictionary
# Step 2: Remove duplicate names from the dictionary 
# (keep male names if duplicate (since less male names than female names))
# (remove surnames if present in firstnames combined list)
# Step 3: rank order names by frequency
# Step 4: replace terms in list by same order
# Step 5: inspect new name lists
rm(list=ls())
setwd("N:/DesktopSettings/Desktop/splink/LearningPython")

# load csvs 
surnames_list <- read.csv("hao_output.csv")
male_names <- read.csv("male_output_nameprism.csv")
female_names <- read.csv("female_output_nameprism.csv")

# load data

data <- read.csv("fake_testing.csv")
names(data)[names(data) == "ï..G0_surname"] <- "G0_surname"

# Step 0: Dedup male names and female names into a single column

# unique_male_names <- setdiff(male_names$Name, female_names$Name)
# remove male names from female list
unique_female_names <- setdiff(female_names$Name, male_names$Name) # 19,634 unique female first names

# replace unique_female_names as names
unique_female_list <- subset(female_names, Name %in% unique_female_names)

# combined first name list 
combine_dict_list <- c(male_names$Name, unique_female_names) # 36,411 unique first names

# dedup surnames
unique_surnames_list <- surnames_list[!duplicated(surnames_list$Name),] #8,395 deduplicated last names

# remove duplicated surnames from first name list
# unique_surnames_list <- setdiff(unique_surnames_list$Name, combine_dict_list) 
# 8,395 unique last names, matched, no need further remove

# replace surname_list if unique
# unique_surname_list <- subset(deduped_surnames_list, Name %in% unique_surnames)


### Remove existing terms in data from list ### 
## This is such that we won't be creating synthesised names that is identical to original data

existing_names <- c(data$G0_surname, data$G1_surname, data$G1_firstname)

unique_male_list <-  subset(male_names, Name %in% setdiff(male_names$Name, existing_names))

unique_female_list <- subset(unique_female_list, Name %in% setdiff(unique_female_list$Name, existing_names))

unique_surnames_list <- subset(unique_surnames_list, Name %in% setdiff(unique_surnames_list$Name, existing_names))

## clean data frames

rm(male_names, female_names, surnames_list)
rm(combine_dict_list, unique_female_names, existing_names)

# Step 2: CREATE RANKINGS in Dictionary

# create Rank for male, female, surnames, by ethnicity
# order sort by frequency, Most frequent == rank 1

unique_male_list$rank <- ave(unique_male_list$total, unique_male_list$race, FUN = function(x) rank(-x, ties.method = "random"))
sorted_male <- unique_male_list[order(unique_male_list$race,unique_male_list$rank, decreasing = FALSE), ]

unique_female_list$rank <- ave(unique_female_list$total, unique_female_list$race, FUN = function(x) rank(-x, ties.method = "random"))
sorted_female <- unique_female_list[order(unique_female_list$race,unique_female_list$rank, decreasing = FALSE), ]

unique_surnames_list$rank <- ave(unique_surnames_list$freq, unique_surnames_list$race, FUN = function(x) rank(-x, ties.method = "random"))
sorted_surnames <- unique_surnames_list[order(unique_surnames_list$race,unique_surnames_list$rank, decreasing = FALSE), ]

rm(unique_male_list, unique_female_list, unique_surnames_list)

# Step 3: CREATE RANKINGS in DATA
# separate name by Gender

# 2 problems of name generation
# 1) name-ethnicity relationship is not 1:1 (black people have white names, vice versa)
# White people with black names (rare) will be replaced with other black names (match ethnicity), but it might have less cross-ethnic fit.
# 2) name-gender relationship is not 1:1 (male have female names, vice versa)
# female with male names will be replaced with other male names (match gender), but it might have less cross-gender fit.
# How to determine which gender/ethnicity if multiple?
# for example: Joseph is a common White, Male name. My name is Joseph and I am not White.
# Consider the most frequent pattern: If name more common in male, consider it male. If name more common in White, consider it white
# caveat, this pattern is data specific --> within data pattern may not agree with population data pattern.
# for example, we are cleaning a dataset with known transgender population. 
# consider data linkage implications - name-gender & name-ethnic dependencies 


# combine names across surname columns
combined_surnames <- c(data$G0_surname, data$G1_surname)
combined_df <- data.frame(Name = combined_surnames, race = data$Race)

# calculate total frequency of surnames in each field by race
name_frequency_by_race <- aggregate(list(Frequency = combined_df$Name), by = combined_df[c("race", "Name")], FUN = length)

# Inspect frequency of surnames, regardless of race 
aggregated_surname_list <- aggregate(Frequency ~ Name, data = name_frequency_by_race, FUN = sum)

# identify duplicate names in list across race
duplicated_names <- name_frequency_by_race$Name[duplicated(name_frequency_by_race$Name)]
duplicated_df <- subset(name_frequency_by_race, Name %in% duplicated_names)

# Keep when the name is more frequent in that race 
sorted_df <- duplicated_df[order(duplicated_df$Name, duplicated_df$Frequency, decreasing = TRUE), ]
deduplicated_df <- sorted_df[!duplicated(sorted_df$Name), ]

# identify non-duplicate names in list
non_duplicated_names <- name_frequency_by_race$Name[!duplicated(name_frequency_by_race$Name)]
non_duplicated_names <- non_duplicated_names[!non_duplicated_names %in% duplicated_names]

# combine this with above.
merge_surname <- merge(aggregated_surname_list, deduplicated_df, by = "Name", all.x = TRUE)
merge_surname <- merge(merge_surname, name_frequency_by_race[!name_frequency_by_race$Name %in% duplicated_names, ],
                   by = "Name", all.x = TRUE)

merge_surname$race <- ifelse(is.na(merge_surname$race.x), merge_surname$race.y, merge_surname$race.x)
merge_surname <- subset(merge_surname, select = -c(race.x, race.y))
merge_surname <- subset(merge_surname, select = -c(Frequency.y, Frequency))
colnames(merge_surname)[2] <- "Frequency"

# rank by race
surname_ranked_frequency_by_race <- within(merge_surname, Rank <- ave(-Frequency, race, FUN = function(x) rank(x, ties.method = "random")))
surname_ranked_frequency_by_race <- surname_ranked_frequency_by_race[order(surname_ranked_frequency_by_race$race, surname_ranked_frequency_by_race$Rank), ]

################################################################################
# repeat the same with first name (gender & ethnicity)

## first name - gendered
firstname_df <- data.frame(Name = data$G1_firstname, race = data$Race, Gender = data$Gender)

# first name, by race and gender
fname_freq_by_race <- aggregate(list(Frequency = firstname_df$Name), by = firstname_df[c("Name","race","Gender")], FUN = length)

# first name, by race
fname_freq_by_race_2 <- aggregate(list(Frequency = firstname_df$Name), by = firstname_df[c("Name","race")], FUN = length)

# first name, by gender
fname_freq_by_race_3 <- aggregate(list(Frequency = firstname_df$Name), by = firstname_df[c("Name","Gender")], FUN = length)

# first name, overall freq
fname_freq_by_race_4 <- aggregate(list(Frequency = firstname_df$Name), by = firstname_df[c("Name")], FUN = length)

# decision: If dup over gender, use = more frequent
# decision: If dup over ethnicity, use = more frequent
# decision: freq, tallied independent of race/gender

# identify duplicate names in list across race
duplicated_names_first <- fname_freq_by_race_2$Name[duplicated(fname_freq_by_race_2$Name)]
duplicated_first_df <- subset(fname_freq_by_race_2, Name %in% duplicated_names_first)

# Keep when the name is more frequent in that race 
sorted_first_df <- duplicated_first_df[order(duplicated_first_df$Name, duplicated_first_df$Frequency, decreasing = TRUE), ]
deduplicated_first_df <- sorted_first_df[!duplicated(sorted_first_df$Name), ]

# identify non-duplicate names in list
non_duplicated_first_names <- fname_freq_by_race_2$Name[!duplicated(fname_freq_by_race_2$Name)]
non_duplicated_first_names <- non_duplicated_first_names[!non_duplicated_first_names %in% duplicated_names_first]

# identify duplicate names in list across gender
duplicated_names_first_gender <- fname_freq_by_race_3$Name[duplicated(fname_freq_by_race_3$Name)]
duplicated_first_gender_df <- subset(fname_freq_by_race_3, Name %in% duplicated_names_first_gender)

# Keep when the name is more frequent in that gender 
sorted_first_gender_df <- duplicated_first_gender_df[order(duplicated_first_gender_df$Name, duplicated_first_gender_df$Frequency, decreasing = TRUE), ]
deduplicated_first_gender_df <- sorted_first_gender_df[!duplicated(sorted_first_gender_df$Name), ]

# identify non-duplicate names in list
non_duplicated_first_names <- fname_freq_by_race$Name[!duplicated(fname_freq_by_race$Name)]
non_duplicated_first_names <- non_duplicated_first_names[!non_duplicated_first_names %in% duplicated_names_first]
non_duplicated_first_names <- non_duplicated_first_names[!non_duplicated_first_names %in% duplicated_names_first_gender]


# combine this with total freq (4)

# get Race if duplicate
merge_firstname <- merge(fname_freq_by_race_4, deduplicated_first_df, by = "Name", all.x = TRUE, suffixes = c("_racekeep", "_drop"))
merge_firstname <- subset(merge_firstname, select = -c(Frequency_drop))

# get Gender if duplicate
merge_firstname <- merge(merge_firstname, deduplicated_first_gender_df, by = "Name", all.x = TRUE, suffixes = c("_genderkeep", "_drop"))
merge_firstname <- subset(merge_firstname, select = -c(Frequency))
# get the rest (no duplicate)
# flag duplicated names at gender or race

duplicated_names_first_total <- c(duplicated_names_first_gender,duplicated_names_first)
  
merge_firstname <- merge(merge_firstname, fname_freq_by_race[!fname_freq_by_race$Name %in% duplicated_names_first_total, ],
                       by = "Name", all.x = TRUE, suffixes = c("_d", "_tokeep"))
merge_firstname <- subset(merge_firstname, select = -c(Frequency))


merge_firstname$race <- ifelse(is.na(merge_firstname$race_d), merge_firstname$race_tokeep, merge_firstname$race_d)
merge_firstname <- subset(merge_firstname, select = -c(race_d, race_tokeep))

merge_firstname$Gender <- ifelse(is.na(merge_firstname$Gender_d), merge_firstname$Gender_tokeep, merge_firstname$Gender_d)
merge_firstname <- subset(merge_firstname, select = -c(Gender_d, Gender_tokeep))

colnames(merge_firstname)[2] <- "Frequency"

# rank by race
firstname_ranked_frequency_by_race <- within(merge_firstname, Rank <- ave(-Frequency, race, FUN = function(x) rank(x, ties.method = "random")))
firstname_ranked_frequency_by_race <- firstname_ranked_frequency_by_race[order(firstname_ranked_frequency_by_race$race, firstname_ranked_frequency_by_race$Rank), ]

# clean data
# keep only these data frames
data_frame_names <- c("data", "firstname_ranked_frequency_by_race","surname_ranked_frequency_by_race", "sorted_female", "sorted_male", "sorted_surnames")
rm(list = setdiff(ls(), data_frame_names))

# remove unwanted dataframes
# rm(aggregated_surname_list, combined_df, deduplicated_df, deduplicated_first_df, deduplicated_first_gender_df, duplicated_df, duplicated_first_df
#   , duplicated_first_gender_df,firstname_df, fname_freq_by_race, fname_freq_by_race_2, fname_freq_by_race_3, fname_freq_by_race_4,
#   merge_firstname, merge_surname, name_frequency_by_race, sorted_df, sorted_first_df, sorted_first_gender_df)


# Step 4: Replace terms in the list with the same order, matching ethnicity and gender
# 4.1: clean "race" var in lists. (API = Asian, Hispanic/AIAN = Other, White, Black. Missing in data = White)
sorted_female$race <- replace(sorted_female$race, sorted_female$race  == "API", "Asian")
sorted_female$race <- replace(sorted_female$race, sorted_female$race  == "Hispanic", "Other")
sorted_female$race <- replace(sorted_female$race, sorted_female$race  == "AIAN", "Other")

sorted_male$race <- replace(sorted_male$race, sorted_male$race == "API", "Asian")
sorted_male$race <- replace(sorted_male$race, sorted_male$race == "Hispanic", "Other")
sorted_male$race <- replace(sorted_male$race, sorted_male$race == "AIAN", "Other")

sorted_surnames$race <- replace(sorted_surnames$race, sorted_surnames$race == "API", "Asian")
sorted_surnames$race <- replace(sorted_surnames$race, sorted_surnames$race == "Hispanic", "Other")
sorted_surnames$race <- replace(sorted_surnames$race, sorted_surnames$race == "AIAN", "Other")


# sequence of generating names does not matter. Repeating the concept to remind myself.
# I have cleaned the data such the more frequent groups (race/gender) will take precedent if name co-occurs
# this mean that white people with non-white names (rare) would be replaced with non-white names
# this mean that male with common female name would be replaced with a female name
# problem is: within sample pattern may not match with global pattern
# for example, if there are many more female Alex in sample
# all male Alex in the data will be given a random female name, say, Lily. 
# this name is not as gender-ambiguous as Alex, hence weaker name-gender association
# matching based on names and gender in more gendered names would be given an edge (interdependency..?)
# If we have name-gender frequency adjustment, then this would be positively recognised.


# name-frequency adjustment is based on existing names in data (cardinality of names within) 
# Or based on external name bank (distribution of names in (expected) population)

# Create a dictionary based on matching rank, race, and gender: first name
firstname_dictionary <- data.frame(
  fname_Rank = firstname_ranked_frequency_by_race$Rank,
  fname_Race = firstname_ranked_frequency_by_race$race,
  fname_Gender = firstname_ranked_frequency_by_race$Gender,
  G1_firstname = firstname_ranked_frequency_by_race$Name,
  firstname_syn_f = ifelse(firstname_ranked_frequency_by_race$Gender == "Female",
                       sorted_female$Name[match(paste(firstname_ranked_frequency_by_race$Rank, 
                                                      firstname_ranked_frequency_by_race$race), 
                                              paste(sorted_female$rank, 
                                                    sorted_female$race))],
                       NA),
  firstname_syn_m = ifelse(firstname_ranked_frequency_by_race$Gender == "Male",
                       sorted_male$Name[match(paste(firstname_ranked_frequency_by_race$Rank, 
                                                    firstname_ranked_frequency_by_race$race), 
                                            paste(sorted_male$rank, 
                                                  sorted_male$race))],
                       NA)
)

firstname_dictionary$firstname_syn <- ifelse(is.na(firstname_dictionary$firstname_syn_f), firstname_dictionary$firstname_syn_m, firstname_dictionary$firstname_syn_f)
firstname_dictionary <- subset(firstname_dictionary, select = -c(firstname_syn_f, firstname_syn_m))

# inspect if duplicated names occurred.
duplicated_firstnames <- firstname_dictionary$G1_firstnames[duplicated(firstname_dictionary$G1_firstnames) | duplicated(firstname_dictionary$G1_firstnames, fromLast = TRUE), ]

# Should expect NULL - but leave in to check if somehow an error happens.
# deduped_firstname_dict <- firstname_dictionary[!duplicated(firstname_dictionary$G1_firstname, fromLast = FALSE), ]

# Repeat for Surname
surname_dictionary <- data.frame(
  sname_Rank = surname_ranked_frequency_by_race$Rank,
  sname_Race = surname_ranked_frequency_by_race$race,
  surname_orig = surname_ranked_frequency_by_race$Name,
  surname_syn = sorted_surnames$Name[match(paste(surname_ranked_frequency_by_race$Rank, 
                                                 surname_ranked_frequency_by_race$race), 
                                           paste(sorted_surnames$rank, 
                                                 sorted_surnames$race))]
  
)



# Step 5: Inspect the new name lists
merge_data <- merge(data, firstname_dictionary, by = "G1_firstname")
merge_data <- subset(merge_data, select = -c(fname_Rank, fname_Race, fname_Gender))

merge_data <- merge(merge_data, surname_dictionary, by.x = "G0_surname", by.y = "surname_orig")
merge_data <- subset(merge_data, select = -c(sname_Rank, sname_Race))

merge_data <- merge(merge_data, surname_dictionary, by.x = "G1_surname", by.y = "surname_orig")
merge_data <- subset(merge_data, select = -c(sname_Rank, sname_Race))

# check if indeed is referring to column 6-8
colnames(merge_data)[6:8] <- c("Syn_G1_firstname","Syn_G0_surname","Syn_G1_surname")

syn_data <- subset(merge_data, select = -c(G1_surname,G0_surname, G1_firstname))

# cardinality
length(unique(merge_data$G1_surname))
length(unique(merge_data$G0_surname))
length(unique(merge_data$G1_firstname))

length(unique(merge_data$Syn_G1_surname))
length(unique(merge_data$Syn_G0_surname))
length(unique(merge_data$Syn_G1_firstname))

# Get the current date
current_date <- format(Sys.Date(), "%Y_%m_%d")

# Create the file name with the current date
file_name <- paste(current_date, "syndata.csv", sep = "_")

# Write data frame to the CSV file
write.csv(syn_data, file = file_name, row.names = TRUE)
