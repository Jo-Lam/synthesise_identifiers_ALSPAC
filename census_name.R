# Read First Names Lists

rm(list = ls())
library("readxl")

male_names <- read_excel('N:/Downloads/babynames1996to2021.xlsx', sheet = "1")
female_names <- read_excel('N:/Downloads/babynames1996to2021.xlsx', sheet = "2")

# drop first 6 columns

male_names <- male_names[-c(1:6),]
female_names <- female_names[-c(1:6),]

# rename
names(male_names) <- NULL
names(male_names) <- male_names[1,]
male_names <- male_names[-c(1),]

names(female_names) <- NULL
names(female_names) <- female_names[1,]
female_names <- female_names[-c(1),]

# replace [x] with NA

male_names <- replace(male_names, male_names == "[x]", NA)
female_names <- replace(female_names, female_names == "[x]", NA)

# keep only count information
male_names_count <- male_names[, c(1, seq(3, ncol(male_names), by = 2))]
female_names_count <- female_names[, c(1, seq(3, ncol(female_names), by = 2))]

# data type to numeric
columns_to_convert <- names(male_names_count[,2:27])

male_names_count[columns_to_convert] <- lapply(male_names_count[columns_to_convert], as.numeric)
female_names_count[columns_to_convert] <- lapply(female_names_count[columns_to_convert], as.numeric)

# row total

male_names_count$total <- rowSums(male_names_count[,2:27], na.rm = TRUE)
female_names_count$total <- rowSums(female_names_count[,2:27], na.rm = TRUE)

# export

write.csv(male_names_count, "male_names.csv")
write.csv(female_names_count, "female_names.csv")
