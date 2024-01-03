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
setwd()

# load csvs 
surnames_list <- read.csv("hao_output.csv")
male_names <- read.csv("male_output_nameprism.csv")
female_names <- read.csv("female_output_nameprism.csv")

# load data

data <- read.csv("fake_testing.csv")

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

existing_names <- c(data$g0_surname_1_arc1, data$g0_surname_1_arc2,data$g0_surname_1_arc3,data$g0_surname_1_arc4,data$g1_surname_1_arc1, data$g1_surname_1_arc2,data$g1_surname_1_arc3,data$g1_surname_1_arc4,data$g1_forename_1_arc1, data$g1_forename_1_arc2)

unique_male_list <-  subset(male_names, Name %in% setdiff(male_names$Name, existing_names))

unique_female_list <- subset(unique_female_list, Name %in% setdiff(unique_female_list$Name, existing_names))

unique_surnames_list <- subset(unique_surnames_list, Name %in% setdiff(unique_surnames_list$Name, existing_names))

## clean data frames

rm(male_names, female_names, surnames_list)
rm(combine_dict_list, unique_female_names, existing_names)

# Step 2: CREATE RANKINGS in Dictionary

# Race: missing as White as ALSPAC is white dominant
data$flag <- ifelse(data$ethgroup == "Missing", "ethnicity missing", "ethnicity not missing")
data$ethgroup <- ifelse(data$ethgroup == "Missing", "White", data$ethgroup)


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
combined_surnames <- c(data$g0_surname_1_arc1, data$g0_surname_1_arc2,data$g0_surname_1_arc3,data$g0_surname_1_arc4,data$g1_surname_1_arc1, data$g1_surname_1_arc2,data$g1_surname_1_arc3,data$g1_surname_1_arc4)
combined_df <- data.frame(Name = combined_surnames, race = data$ethgroup)
combined_df <- subset(combined_df, Name != "")

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
combined_firstnames <- c(data$g1_forename_1_arc1, data$g1_forename_1_arc2)
firstname_df <- data.frame(Name = combined_firstnames, race = data$ethgroup, Gender = data$g1_gender_arc)
firstname_df <- subset(firstname_df, Name != "")

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

# duplicated_names_first_total <- c(duplicated_names_first_gender,duplicated_names_first)
merge_firstname <- merge(merge_firstname, fname_freq_by_race_3[!fname_freq_by_race_3$Name %in% duplicated_names_first_gender, ],
                         by = "Name", all.x = TRUE, suffixes = c("_d", "_tokeep"))

merge_firstname$Gender <- ifelse(is.na(merge_firstname$Gender_d), merge_firstname$Gender_tokeep, merge_firstname$Gender_d)
merge_firstname <- subset(merge_firstname, select = -c(Gender_d, Gender_tokeep))

merge_firstname <- merge(merge_firstname, fname_freq_by_race_2[!fname_freq_by_race_2$Name %in% duplicated_names_first, ],
                         by = "Name", all.x = TRUE, suffixes = c("_d", "_tokeep"))
merge_firstname <- subset(merge_firstname, select = -c(Frequency_tokeep))


merge_firstname$race <- ifelse(is.na(merge_firstname$race_d), merge_firstname$race_tokeep, merge_firstname$race_d)
merge_firstname <- subset(merge_firstname, select = -c(race_d, race_tokeep))
merge_firstname <- subset(merge_firstname, select = -c(Frequency_d))

colnames(merge_firstname)[2] <- "Frequency"

# rank by race
firstname_ranked_frequency_by_race_gender <- within(merge_firstname, Rank <- ave(-Frequency, race, Gender, FUN = function(x) rank(x, ties.method = "random")))
firstname_ranked_frequency_by_race_gender <- firstname_ranked_frequency_by_race_gender[order(firstname_ranked_frequency_by_race_gender$race, firstname_ranked_frequency_by_race_gender$Gender,firstname_ranked_frequency_by_race_gender$Rank), ]

# clean data
# keep only these data frames
data_frame_names <- c("data", "firstname_ranked_frequency_by_race_gender","surname_ranked_frequency_by_race", "sorted_female", "sorted_male", "sorted_surnames")
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
  fname_Rank = firstname_ranked_frequency_by_race_gender$Rank,
  fname_Race = firstname_ranked_frequency_by_race_gender$race,
  fname_Gender = firstname_ranked_frequency_by_race_gender$Gender,
  G1_firstname = firstname_ranked_frequency_by_race_gender$Name,
  firstname_syn_f = ifelse(firstname_ranked_frequency_by_race_gender$Gender == "Female",
                           sorted_female$Name[match(paste(firstname_ranked_frequency_by_race_gender$Rank, 
                                                          firstname_ranked_frequency_by_race_gender$race), 
                                                    paste(sorted_female$rank, 
                                                          sorted_female$race))],
                           NA),
  firstname_syn_m = ifelse(firstname_ranked_frequency_by_race_gender$Gender == "Male",
                           sorted_male$Name[match(paste(firstname_ranked_frequency_by_race_gender$Rank, 
                                                        firstname_ranked_frequency_by_race_gender$race), 
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

# problem: did not have enough "other" race surnames, replace with white. from least common.
surname_unused_rank <- sorted_surnames[order(sorted_surnames$race, -sorted_surnames$rank), ]
surname_usused_white <- subset(surname_unused_rank, race == "White")
surname_usused_white_15 <- surname_usused_white[1:15,]
surname_dictionary$surname_syn <- ifelse(is.na(surname_dictionary$surname_syn), surname_usused_white_15$Name, surname_dictionary$surname_syn)

# Step 5: Inspect the new name lists
merge_data <- merge(data, firstname_dictionary, by.x = "g1_forename_1_arc1", by.y = "G1_firstname", all.x = TRUE)
# replace missing first names in original as "missing"
merge_data$firstname_syn <- ifelse(merge_data$g1_forename_1_arc1 == "", "", merge_data$firstname_syn)
names(merge_data)[names(merge_data) == "firstname_syn"] <- "syn_g1_forename_1"
merge_data <- subset(merge_data, select = -c(fname_Rank, fname_Race, fname_Gender))

merge_data <- merge(merge_data, firstname_dictionary, by.x = "g1_forename_1_arc2", by.y = "G1_firstname", all.x = TRUE)
names(merge_data)[names(merge_data) == "firstname_syn"] <- "syn_g1_forename_2"
merge_data$syn_g1_forename_2 <- ifelse(merge_data$g1_forename_1_arc2 == "", "", merge_data$syn_g1_forename_2)

merge_data <- subset(merge_data, select = -c(fname_Rank, fname_Race, fname_Gender))

# replace firstname 1 = firstname 2 if firstname 1 is missing
merge_data$syn_g1_forename_1 <- ifelse(is.na(merge_data$syn_g1_forename_1), merge_data$syn_g1_forename_2, merge_data$syn_g1_forename_1)
merge_data$syn_g1_forename_2 <- ifelse(merge_data$syn_g1_forename_1 == merge_data$syn_g1_forename_2, "", merge_data$syn_g1_forename_2)

# merge surnames, repeat for each of teh surname variable

merge_data <- merge(merge_data, surname_dictionary, by.x = "g0_surname_1_arc1", by.y = "surname_orig", all.x = TRUE)
merge_data <- subset(merge_data, select = -c(sname_Rank, sname_Race))
names(merge_data)[names(merge_data) == "surname_syn"] <- "syn_g0_surname_1"

merge_data <- merge(merge_data, surname_dictionary, by.x = "g0_surname_1_arc2", by.y = "surname_orig", all.x = TRUE)
merge_data <- subset(merge_data, select = -c(sname_Rank, sname_Race))
names(merge_data)[names(merge_data) == "surname_syn"] <- "syn_g0_surname_2"

merge_data <- merge(merge_data, surname_dictionary, by.x = "g0_surname_1_arc3", by.y = "surname_orig", all.x = TRUE)
merge_data <- subset(merge_data, select = -c(sname_Rank, sname_Race))
names(merge_data)[names(merge_data) == "surname_syn"] <- "syn_g0_surname_3"

merge_data <- merge(merge_data, surname_dictionary, by.x = "g0_surname_1_arc4", by.y = "surname_orig", all.x = TRUE)
merge_data <- subset(merge_data, select = -c(sname_Rank, sname_Race))
names(merge_data)[names(merge_data) == "surname_syn"] <- "syn_g0_surname_4"


merge_data <- merge(merge_data, surname_dictionary, by.x = "g1_surname_1_arc1", by.y = "surname_orig", all.x = TRUE)
merge_data <- subset(merge_data, select = -c(sname_Rank, sname_Race))
names(merge_data)[names(merge_data) == "surname_syn"] <- "syn_g1_surname_1"

merge_data <- merge(merge_data, surname_dictionary, by.x = "g1_surname_1_arc2", by.y = "surname_orig", all.x = TRUE)
merge_data <- subset(merge_data, select = -c(sname_Rank, sname_Race))
names(merge_data)[names(merge_data) == "surname_syn"] <- "syn_g1_surname_2"

merge_data <- merge(merge_data, surname_dictionary, by.x = "g1_surname_1_arc3", by.y = "surname_orig", all.x = TRUE)
merge_data <- subset(merge_data, select = -c(sname_Rank, sname_Race))
names(merge_data)[names(merge_data) == "surname_syn"] <- "syn_g1_surname_3"

merge_data <- merge(merge_data, surname_dictionary, by.x = "g1_surname_1_arc4", by.y = "surname_orig", all.x = TRUE)
merge_data <- subset(merge_data, select = -c(sname_Rank, sname_Race))
names(merge_data)[names(merge_data) == "surname_syn"] <- "syn_g1_surname_4"

# replace NAs with ""
merge_data$syn_g0_surname_1 <- ifelse(merge_data$g0_surname_1_arc1 == "", "", merge_data$syn_g0_surname_1)
merge_data$syn_g0_surname_2 <- ifelse(merge_data$g0_surname_1_arc2 == "", "", merge_data$syn_g0_surname_2)
merge_data$syn_g0_surname_3 <- ifelse(merge_data$g0_surname_1_arc3 == "", "", merge_data$syn_g0_surname_3)
merge_data$syn_g0_surname_4 <- ifelse(merge_data$g0_surname_1_arc4 == "", "", merge_data$syn_g0_surname_4)
merge_data$syn_g1_surname_1 <- ifelse(merge_data$g1_surname_1_arc1 == "", "", merge_data$syn_g1_surname_1)
merge_data$syn_g1_surname_2 <- ifelse(merge_data$g1_surname_1_arc2 == "", "", merge_data$syn_g1_surname_2)
merge_data$syn_g1_surname_3 <- ifelse(merge_data$g1_surname_1_arc3 == "", "", merge_data$syn_g1_surname_3)
merge_data$syn_g1_surname_4 <- ifelse(merge_data$g1_surname_1_arc4 == "", "", merge_data$syn_g1_surname_4)

# replace ethnicity as missing if originally coded as missing
merge_data$ethgroup <- ifelse(merge_data$flag == "ethnicity missing", "Missing", merge_data$ethgroup)
merge_data <- subset(merge_data, select = -c(flag))

# check if indeed is referring to column 6-8
# colnames(merge_data)[12:14] <- c("Syn_G1_firstname","Syn_G0_surname","Syn_G1_surname")

# concatonate name variables
merge_data$g0_surname_arc <- paste(merge_data$g0_surname_1_arc1, merge_data$g0_surname_1_arc2, merge_data$g0_surname_1_arc3, merge_data$g0_surname_1_arc4, sep = " ")
merge_data$g1_surname_arc <- paste(merge_data$g1_surname_1_arc1, merge_data$g1_surname_1_arc2, merge_data$g1_surname_1_arc3, merge_data$g1_surname_1_arc4, sep = " ")
merge_data$g1_firstname_arc <- paste(merge_data$g1_forename_1_arc1, merge_data$g1_forename_1_arc2, sep = " ")

merge_data$syn_g0_surname <- paste(merge_data$syn_g0_surname_1, merge_data$syn_g0_surname_2, merge_data$syn_g0_surname_3, merge_data$syn_g0_surname_4, sep = " ")
merge_data$syn_g1_surname <- paste(merge_data$syn_g1_surname_1, merge_data$syn_g1_surname_2, merge_data$syn_g1_surname_3, merge_data$syn_g1_surname_4, sep = " ")
merge_data$syn_g1_firstname <- paste(merge_data$syn_g1_forename_1, merge_data$syn_g1_forename_2, sep = " ")

# remove leading or trailing spaces 
merge_data$g0_surname_arc <- trimws(merge_data$g0_surname_arc)
merge_data$g1_surname_arc <- trimws(merge_data$g1_surname_arc)
merge_data$g1_firstname_arc <- trimws(merge_data$g1_firstname_arc)

merge_data$syn_g0_surname <- trimws(merge_data$syn_g0_surname)
merge_data$syn_g1_surname <- trimws(merge_data$syn_g1_surname)
merge_data$syn_g1_firstname <- trimws(merge_data$syn_g1_firstname)


# cardinality
length(unique(merge_data$g0_surname_arc))
length(unique(merge_data$g1_surname_arc))
length(unique(merge_data$g1_firstname_arc))

length(unique(merge_data$syn_g0_surname))
length(unique(merge_data$syn_g1_surname))
length(unique(merge_data$syn_g1_firstname))

# create syn_data subset
syn_data <- subset(merge_data, select = c(sid3002, maternal_agecat, ethgroup, g1_gender_arc, imddecile, g1_dob_arc1, g0_surname_arc, g1_surname_arc,g1_firstname_arc,syn_g0_surname,syn_g1_surname,syn_g1_firstname))

# Get the current date
current_date <- format(Sys.Date(), "%Y_%m_%d")

# Create the file name with the current date
file_name <- paste(current_date, "syn_data_withnames.csv", sep = "_")

# Write data frame to the CSV file
write.csv(merge_data, file = file_name, row.names = TRUE)


# add names to synthetic data

# loop over accepted samples
# need to maintain cardinality, meaning the same number of unique names need to be used

file_names <- list.files(pattern = "^accepted_sample_.*\\.csv$")

# Create an empty list to store the data frames
data_list <- list()

# 1) Loop through the file names and read each file using read.csv()
# 2) order both lists by race and gender, paste?
for(i in 1:length(file_names)) {
  data_list[[i]] <- read.csv(file_names[i])
  # data_list[[i]] <- data_list[[i]][order(sapply(data_list[[i]], function(x) c(data_list[[i]]$ethgroup, data_list[[i]]$gender_arc)))]
}

synth_names <- merge_data[, c("syn_g1_firstname", "syn_g1_surname", "syn_g0_surname", "ethgroup", "g1_gender_arc")]
synth_names <- synth_names[order(synth_names$ethgroup, synth_names$g1_gender_arc), ]
colnames(synth_names)[4:5] <- c("ethgroup_synname","gender_arc_synname")

# add synth names to data files. 
# order data by ethnicity and gender
# bind and paste syn names
# create flags to indicate ethnicity and gender mismatches
# drop excess vars
for (i in 1:length(file_names)){
  data_list[[i]] <- data_list[[i]][order(data_list[[i]]$ethgroup,data_list[[i]]$g1_gender_arc),]
  data_list[[i]] <- cbind(data_list[[i]], synth_names[, c("syn_g1_firstname", "syn_g1_surname", "syn_g0_surname", "ethgroup_synname","gender_arc_synname")])
  data_list[[i]]$flag_ethnicity_mismatch <- ifelse(data_list[[i]]$ethgroup != data_list[[i]]$ethgroup_synname & data_list[[i]]$g1_gender_arc == data_list[[i]]$gender_arc_synname, "ethnicity mismatch", "")
  data_list[[i]]$flag_gender_mismatch <- ifelse(data_list[[i]]$ethgroup == data_list[[i]]$ethgroup_synname & data_list[[i]]$g1_gender_arc != data_list[[i]]$gender_arc_synname, "gender mismatch", "")
  data_list[[i]] <- subset(data_list[[i]], select = -c(ethgroup_synname, gender_arc_synname))
}


# inspect if name-mismatch by gender/ethnicity is a problem.

# replace gender and ethnicity mismatch = 1 if not missing, = 0 if missing
for (i in 1:200){
  data_list[[i]]$flag_ethnicity_mismatch_num[data_list[[i]]$flag_ethnicity_mismatch != ""] <- 1
  data_list[[i]]$flag_ethnicity_mismatch_num[data_list[[i]]$flag_ethnicity_mismatch == ""] <- 0
  data_list[[i]]$flag_gender_mismatch_num[data_list[[i]]$flag_gender_mismatch != ""] <- 1
  data_list[[i]]$flag_gender_mismatch_num[data_list[[i]]$flag_gender_mismatch == ""] <- 0
}

# function to tabulate gender mismatch with gender
tabulate_gend_match <- function(df) {
  # Create a cross-tabulation using the table() function
  tab <- table(as.factor(df$g1_gender_arc), df$flag_gender_mismatch_num)
  # Return the proportion table
  return(tab)
}
# apply to all  dataset
tab <- lapply(data_list, tabulate_gend_match)

# function to tabulate ethncity mismatch with ethnicity
tabulate_eth_match <- function(df) {
  # Create a cross-tabulation using the table() function
  tab2 <- addmargins(table(as.factor(df$ethgroup), (df$flag_gender_mismatch_num)))
  # Return the proportion table
  return(tab2)
}
# apply to all dataset
tab2 <- lapply(data_list, tabulate_eth_match)

total_mismatch_gend <- c(male = 0, female = 0)
gender_count <- c(male = 0, female = 0)

for (i in 1:length(tab)){
  
  current_table <- tab[[i]]
  
  male_mismatches <- tab[[i]][4]
  female_mismatches <- tab[[i]][3]
  
  total_mismatch_gend["male"] <- total_mismatch_gend["male"] + male_mismatches
  total_mismatch_gend["female"] <- total_mismatch_gend["female"] + female_mismatches
  gender_count["male"] <- gender_count["male"] + tab[[i]][2] + tab[[i]][4]
  gender_count["female"] <- gender_count["female"] + tab[[i]][1] + tab[[i]][3]
}

avg_mismatch_gend <- total_mismatch_gend/gender_count



total_mismatch_eth <- c(Asian = 0, Black = 0, Missing = 0, Other = 0, White = 0)
ethnicity_count <- c(Asian = 0, Black = 0, Missing = 0, Other = 0, White = 0)

for (i in 1:length(tab2)){
  
  current_table <- tab2[[i]]
  
  if (!is.na(current_table[13])){
    Asian_mismatches <- current_table[7]
    Black_mismatches <- current_table[8]  
    Missing_mismatches <- current_table[9]
    Other_mismatches <- current_table[10]
    White_mismatches <- current_table[11]
    
    total_mismatch_eth["Asian"] <- total_mismatch_eth["Asian"] + Asian_mismatches
    total_mismatch_eth["Black"] <- total_mismatch_eth["Black"] + Black_mismatches
    total_mismatch_eth["Missing"] <- total_mismatch_eth["Missing"] + Missing_mismatches
    total_mismatch_eth["Other"] <- total_mismatch_eth["Other"] + Other_mismatches
    total_mismatch_eth["White"] <- total_mismatch_eth["White"] + White_mismatches
    
    ethnicity_count["Asian"] <- ethnicity_count["Asian"] + current_table[13]
    ethnicity_count["Black"] <- ethnicity_count["Black"] + current_table[14]
    ethnicity_count["Missing"] <- ethnicity_count["Missing"] + current_table[15]
    ethnicity_count["Other"] <- ethnicity_count["Other"] + current_table[16]
    ethnicity_count["White"] <- ethnicity_count["White"] + current_table[17]

  } else {
    Asian_mismatches <- total_mismatch_eth["Asian"] + 0
    Black_mismatches <- total_mismatch_eth["Asian"] + 0  
    Missing_mismatches <- total_mismatch_eth["Asian"] + 0
    Other_mismatches <- total_mismatch_eth["Asian"] + 0
    White_mismatches <- total_mismatch_eth["Asian"] + 0
    
    ethnicity_count["Asian"] <- ethnicity_count["Asian"] + current_table[7]
    ethnicity_count["Black"] <- ethnicity_count["Black"] + current_table[8]
    ethnicity_count["Missing"] <- ethnicity_count["Missing"] + current_table[9]
    ethnicity_count["Other"] <- ethnicity_count["Other"] + current_table[10]
    ethnicity_count["White"] <- ethnicity_count["White"] + current_table[11]
  }
}

avg_mismatch_eth <- total_mismatch_eth/ethnicity_count

# drop columns
for (i in 1:200){
  data_list <- lapply(data_list, function(i) i[, -c(10,11,12,13)])
}

# data_list[[i]] <- subset(data_list[[i]], select = c("maternal_agecat", "ethgroup", "g1_gender_arc", "imddecile", "g1_dob_arc1", "syn_g0_surname","syn_g1_surname","syn_g1_firstname","seed"))
# data_list[[i]] <- subset(data_list[[i]], -select = c("flag_ethnicity_mismatch", "flag_gender_mismatch"))

# create unique IDs
for (i in 1:200){
  data_list[[i]]$unique_id <- 1:nrow(data_list[[i]])
  data_list[[i]] <- data_list[[i]][, c("unique_id", names(data_list[[i]][-ncol(data_list[[i]])]))]
}

# save and replace
for(i in 1:length(file_names)) {
  write.csv(data_list[[i]], file = paste0("accepted_sample_",i,".csv"))
}
