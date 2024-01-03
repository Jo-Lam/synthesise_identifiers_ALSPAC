# summarise data setssss
#
# 1. load all dataset
# 2. check if no duplicate in [seed]
# 3. loop table over them
# 4. change date formatting in all
rm(list=ls())

# setwd("")

file_names <- list.files(pattern = "^accepted_sample_.*\\.csv$")

# Create an empty list to store the data frames
data_list <- list()

# 1) Loop through the file names and read each file using read.csv()
for(i in 1:length(file_names)) {
  data_list[[i]] <- read.csv(file_names[i])
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

# all unique data
rm(list=ls())

##### tidy up dates#####
file_names <- list.files(pattern = "^accepted_sample_.*\\.csv$")

# Create an empty list to store the data frames
data_list <- list()
for(i in 1:length(file_names)) {
  data_list[[i]] <- read.csv(file_names[i])
}


# Define a function to create a cross-tabulation and calculate proportions
tabulate_prop_race_maternal <- function(df) {
  # Create a cross-tabulation using the table() function
  tab <- addmargins(table(as.factor(df$ethgroup), as.factor(df$maternal_agecat), useNA = "always"))
  
  # Calculate proportions using prop.table()
  prop_tab <- prop.table(tab, margin = 1)
  
  # Return the proportion table
  return(prop_tab)
}

tabulate_race_maternal <- function(df) {
  # Create a cross-tabulation using the table() function
  tab <- addmargins(table(as.factor(df$ethgroup), as.factor(df$maternal_agecat), useNA = "always"))

  # Return the proportion table
  return(tab)
}

# Use lapply() to apply the function to each data frame in data_frames
tab <- lapply(data_list, tabulate_race_maternal)
tab

prop <- lapply(data_list, tabulate_prop_race_maternal)
prop

############# The section below is run only to quality assure synthetic data - Not Necessary for names generation ###################

# load and compare gold standard
gold <- read.csv("fake_testing.csv")
gold <- data.frame(gold)
gold$ethgroup <- as.factor(gold$ethgroup)
gold$maternal_agecat <- as.factor(gold$maternal_agecat)
gold_dist_nototal <- table(gold$ethgroup, gold$maternal_agecat, useNA = "always")
gold_dist <- addmargins(gold_dist_nototal)
gold_prop <- prop.table(gold_dist, margin = 1)

# difference in proportion
prop_diff <- list()
for (i in 1:length(prop)){
  prop_diff[[i]] <- round(gold_prop - prop[[i]], 4)
  
}
prop_diff_percent <- list()
for (i in 1: length(prop_diff)){
  prop_diff_percent[[i]] <- prop_diff[[i]] * 100
}

avg_diff <- matrix(0, nrow = 5, ncol = 5)
ci_avg_diff <- matrix(0, nrow = 5, ncol = 5) 

for (i in 1:5){
  for (j in 1:5){
    sum_value <- 0
    squared_sum <- 0
    
    for (k in 1:200){
      value <- prop_diff_percent[[k]][i,j]
      sum_value <- sum_value + value
      squared_sum <- squared_sum + value^2
    }
    
    mean_value <- sum_value / 200
    variance <- (squared_sum - sum_value^2/200) / 199
    standard_deviation <- sqrt(variance)
    standard_error <- standard_deviation/ sqrt(200)
    critical_value <- qnorm(( 1 + 0.95)/ 2)
    lower_bound <- mean_value - (critical_value * standard_error)
    upper_bound <- mean_value + (critical_value * standard_error)
    
    avg_diff[i,j] <- mean_value
    ci_avg_diff[i,j] <- paste0("[", round(lower_bound, 3), ", ", round(upper_bound, 3), "]")
  
  }
}
  

# present them together
for (i in 1:5){
  for (j in 1:5){
    cat("Average:", round(avg_diff[i,j], 3), "CI:", ci_avg_diff[i,j],"\n")
  }
}

# repeat for gender & ethnicity

tabulate_prop_race_gender <- function(df) {
  # Create a cross-tabulation using the table() function
  tab <- addmargins(table(as.factor(df$ethgroup), as.factor(df$g1_gender_arc)))
  
  # Calculate proportions using prop.table()
  prop_tab <- prop.table(tab, margin = 1)
  
  # Return the proportion table
  return(prop_tab)
}

prop_gend <-  lapply(data_list, tabulate_prop_race_gender)

# prop gold
gold$g1_gender_arc <- as.factor(gold$g1_gender_arc)
gold_gend_nototal <- table(gold$ethgroup, gold$g1_gender_arc)
gold_gend <- addmargins(gold_gend_nototal)
gold_prop_gend <- prop.table(gold_gend, margin = 1)


prop_diff_gend <- list()
for (i in 1:length(prop)){
  prop_diff_gend[[i]] <- round(gold_prop_gend - prop_gend[[i]], 4)
  
}
prop_gend_diff_percent <- list()
for (i in 1: length(prop_diff_gend)){
  prop_gend_diff_percent[[i]] <- prop_diff_gend[[i]] * 100
}

avg_diff_gend <- matrix(0, nrow = 5, ncol = 2)
ci_avg_diff_gend <- matrix(0, nrow = 5, ncol = 2) 

for (i in 1:5){
  for (j in 1:2){
    sum_value <- 0
    squared_sum <- 0
    
    for (k in 1:200){
      value <- prop_gend_diff_percent[[k]][i,j]
      sum_value <- sum_value + value
      squared_sum <- squared_sum + value^2
    }
    
    mean_value <- sum_value / 200
    variance <- (squared_sum - sum_value^2/200) / 199
    standard_deviation <- sqrt(variance)
    standard_error <- standard_deviation/ sqrt(200)
    critical_value <- qnorm(( 1 + 0.95)/ 2)
    lower_bound <- mean_value - (critical_value * standard_error)
    upper_bound <- mean_value + (critical_value * standard_error)
    
    avg_diff_gend[i,j] <- mean_value
    ci_avg_diff_gend[i,j] <- paste0("[", round(lower_bound, 3), ", ", round(upper_bound, 3), "]")
    
  }
}


# bar plot
# proportion in gold
barplot(gold_prop,names.arg = c("<20", "20-29","30-39","40+", "NA", "Total"), 
        xlab = "maternal age category", 
        ylab = "Ethnicity", 
        main = "cross-tab eth_mat", 
        col = c("yellow", "black", "orange", "blue", "white"))
legend("topright", c("Asian", "Black","Missing", "Other", "White"), cex = 1.2, fill = c("yellow", "black", "orange", "blue", "white"))


# proportion in data
for (i in 1:length(prop)){
  filename = paste0("barplot_", i, ".png")
  png(filename,
      width = 480,
      height = 600,
      units = "px",
      pointsize = 12,
      bg = "grey")
  barplot(prop[[i]], names.arg = c("<20", "20-29","30-39","40+", "NA"), 
          xlab = "maternal age category", 
          ylab = "Ethnicity", 
          main = "cross-tab eth_mat", 
          col = c("yellow", "black", "orange", "blue", "white"))
  legend("topright", c("Asian", "Black","Missing", "Other", "White"), cex = 1.2, fill = c("yellow", "black", "orange", "blue", "white"))
  dev.off()
}

# difference in proportion
for (i in 1:length(prop_diff)){
  barplot(prop_diff[[i]], names.arg = c("<20", "20-29","30-39","40+", "NA", "Sum"), 
          xlab = "maternal age category", 
          ylab = "Ethnicity", 
          main = paste0("cross-tab eth_mat number ", i),
          col = c("yellow", "black", "orange", "blue", "white"))
  legend("topright", c("Asian", "Black","Missing", "Other", "White"), cex = 1.2, fill = c("yellow", "black", "orange", "blue", "white"))
}

barplot(avg_diff,names.arg = c("<20", "20-29","30-39","40+", "NA"), 
        xlab = "maternal age category", 
        ylab = "Ethnicity", 
        main = "cross-tab eth_mat", 
        col = c("yellow", "black", "orange", "blue", "white"))
legend("topright", c("Asian", "Black","Missing", "Other", "White"), cex = 1.2, fill = c("yellow", "black", "orange", "blue", "white"))



# overlay: par(new=T)
# barplot(gold_dist,names.arg = c("<20", "20-29","30-39","40+", "NA"), 
#         xlab = "maternal age category", 
#         ylab = "Ethnicity", 
#         main = "cross-tab eth_mat", 
#         col = c("yellow", "black", "orange", "blue", "white"))
# legend("topright", c("Asian", "Black","Missing", "Other", "White"), cex = 1.2, fill = c("yellow", "black", "orange", "blue", "white"))


# 1) Loop through the file names and read each file using read.csv(), update date formats
#for(i in 1:length(file_names)) {
#  data_list[[i]] <- read.csv(file_names[i])
#  data_list[[i]]$g1_dob_arc1 <- as.Date(as.numeric(data_list[[i]]$g1_dob_arc1), origin = '1970-1-1')
#  write.csv(data_list[[i]], file = paste0("accepted_sample_",i,".csv"))
# }
# this code has been creating problems. Should add condition for ifNA replace
# try in data_list[[1]] first.
#####################
      
      

