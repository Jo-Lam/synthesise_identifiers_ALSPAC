# summarise data setssss
#
# 1. load all dataset
# 2. check if no duplicate in [seed]
# 3. loop table over them
# 4. change date formatting in all
rm(list=ls())

# setwd("/DesktopSettings/Desktop/splink/sdv/")

# load file names
file_names <- list.files(pattern = "^accepted_sample_.*\\.csv$")

# Create an empty list to store the data frames
data_list <- list()

# 1) Loop through the file names and read each file using read.csv()
for(i in 1:length(file_names)) {
  data_list[[i]] <- read.csv(file_names[i])
}


# 2) Loop through the data frames in data_frames and modify the G1dob variable
for(i in 1:length(data_list)) {
  data_list[[i]]$G1dob <- as.Date(as.numeric(data_list[[i]]$G1dob), origin = '1970-1-1')
}



# Initialize vector to store compiled values
compiled_values <- vector(length = length(file_names))
dataset_flags <- vector(length = length(file_names))

# Loop over datasets and compile values to view the seed of each dataset
for (i in seq_along(file_names)) {
  # Read dataset into R
  current_dataset <- read.csv(paste0(file_names[i]))
  
  # Extract unique value
  unique_val <- unique(current_dataset$seed)
  
  # Compile value into single cell
  single_cell_val <- paste(unique_val, collapse = ", ")
  
  # Store compiled value in vector
  compiled_values[i] <- single_cell_val
  
  # Check for duplicate values and flag dataset name if duplicated
  if (sum(compiled_values == single_cell_val) > 1) {
    dataset_flags[i] <- "DUPLICATE"
  } else {
    dataset_flags[i] <- "UNIQUE"
  }
  
  #remove current_dataset
  rm(current_dataset)
}


# Check for duplicated values
duplicated_values <- duplicated(compiled_values)

# Create a list of which values are duplicates
# this creates a list to show where, which seed occurred
duplicate_list <- split(seq_along(compiled_values), compiled_values)


# Create new data_list to include only non-duplicate seeds
# Create list of unique datasets
unique_dataset_names <- file_names[which(dataset_flags == "UNIQUE")]

# Create an empty list to store the data frames
unique_data_list <- list()

# 1) Loop through the file names and read each file using read.csv()
for(i in 1:length(unique_dataset_names)) {
  unique_data_list[[i]] <- read.csv(unique_dataset_names[i])
}


# Define a function to create a cross-tabulation and calculate proportions
tabulate_prop_race_maternal <- function(df) {
  # Create a cross-tabulation using the table() function
  tab <- table(df$race, df$maternal_age)
  
  # Calculate proportions using prop.table()
  prop_tab <- prop.table(tab, margin = 1)
  
  # Return the proportion table
  return(prop_tab)
}

tabulate_race_maternal <- function(df) {
  # Create a cross-tabulation using the table() function
  tab <- table(df$race, df$maternal_age)

  # Return the proportion table
  return(tab)
}

# Use lapply() to apply the function to each data frame in data_frames
tab <- lapply(unique_data_list, tabulate_race_maternal)
tab

prop <- lapply(unique_data_list, tabulate_prop_race_maternal)
prop

gold <- read.csv("fake_testing.csv")
gold <- data.frame(gold)

#compare in other ways






