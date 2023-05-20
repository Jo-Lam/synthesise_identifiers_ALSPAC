# ALSPAC Synthpop Synthetic Data 
setwd() # set working directory
rm(list = ls())
library("synthpop")

# Load Raw Data
data <- data.frame(read.csv('uk_gold.csv')) # fake data for code development
dim(data)
codebook.syn(data)$tab

# Load original data - format as factors for Synthpop
data2 <- data
str(data2)
data2$maternal_age <- as.factor(data2$maternal_age)
data2$race <- as.factor(data2$race)
data2$imd <- as.factor(data2$imd)
data2$sex <- as.factor(data2$sex)
data2$G0dob <- as.Date(data2$G0dob, tryFormats = c("%d/%m/%Y"))
data2$G0dob <- as.numeric(data2$G0dob)
data2$G1dob <- as.Date(data2$G1dob, tryFormats = c("%d/%m/%Y"))
data2$G1dob <- as.numeric(data2$G1dob)
data2$G0surname <- as.factor(data2$G0surname)
data2$G1surname <- as.factor(data2$G1surname)
data2$G1forename <- as.factor(data2$G1forename)
data2 <-subset(data2,select = -c(nhsid))

#omit names
data2 <- subset(data2, select = -c(G0surname, G1surname, G1forename))

#true data no date of birth G0
data2 <- subset(data2, select = -c(G0dob))

# describe data
codebook.syn(data2)
summary(data2)
dim(data2)

# set the number of accepted samples (start with 0)
num_accepted_samples <- 0

# Generate Data, set seed
seed <- 20230507

synth_data <- syn(data2,
                  cont.na = list(race = 'Missing', maternal_agecat = 'NA'), # specify





# Define the desired counts for each value
desired_counts <- list(race = list("Black" >= 127, "Asian" >= 120, "Other" >= 90, "missing" >= 2173),
                       maternal_age = list("30-39" >= 4735, "40+" >= 137, "<20" >= 529, "NA" >= 670))


# desired_counts <- list(list(race = "White", maternal_age = "<20") = 362,
#                       list(race = "White", maternal_age = "40+") = 135,
#                       
#                       list(race = "Black", maternal_age = "<20") = 8,
#                       list(race = "Black", maternal_age = "20-29") = 56,
#                       list(race = "Black", maternal_age = "30-39") = 54,
#                       list(race = "Black", maternal_age = "40+") = 2,
#                       
#                       list(race = "Asian", maternal_age = "<20") = 7,
#                       list(race = "Asian", maternal_age = "20-29") = 68,
#                       list(race = "Asian", maternal_age = "30-39") = 40,
#                       list(race = "Asian", maternal_age = "40+") = 0,
#                       
#                       list(race = "Other", maternal_age = "<20") = 3,
#                       list(race = "Other", maternal_age = "20-29") = 37,
#                       list(race = "Other", maternal_age = "30-39") = 42,
#                       list(race = "Other", maternal_age = "40+") = 2,
#                       
#                       list(race = "missing", maternal_age = "<20") = 162,
#                       list(race = "missing", maternal_age = "40+") = 22,
#                       
#                       list(race = "missing", maternal_age = "NA") = 850)

# Set the number of accepted samples
num_accepted_samples <- 50

# Generate Synthetic Data
seed <- 20230503
# mysyn <- syn(data2,
#              # rules = rules.list, 
#              # rvalues =  rules.value.list,
#              cont.na = list(race = "missing"),
#              predictor.matrix = NULL,
#              visit.sequence = c(3, 5, 1, 2 , 4),
#              seed = seed,
#              drop.not.used = TRUE)

synth_data <- syn(data2,
                # rules = rules.list,
                # rvalues =  rules.value.list,
                cont.na = list(race = "missing"),
                predictor.matrix = NULL,
                visit.sequence = c(3, 5, 1, 2 , 4),
                seed = seed,
                drop.not.used = TRUE)

write.syn(synth_data, filename = 'syndata', filetype = 'csv')
synth_data <- data.frame(read.csv('syndata.csv'))
synth_data$seed <- seed
synth_data$G1dob <- as.Date(as.numeric(synth_data$G1dob), origin = '1970-1-1')
write.csv(synth_data, "syndata")



# Define a function to check if the counts meet the desired values
check_counts <- function(data, desired_counts) {
  # Loop over each variable and its desired counts
  for (var in names(desired_counts)) {
    for (val in names(desired_counts[[var]])) {
      # Count the number of observations with the current variable and value
      count <- sum(data[[var]] == val)
      # Check if the count is less than the desired count
      if (count < desired_counts[[var]][[val]]) {
        # If the count is less, return FALSE
        return(FALSE)
      }
    }
  }
  # If all counts are at least the desired values, return TRUE
  return(TRUE)
}

# Loop until we have the desired number of accepted samples
accepted_samples <- 0

# # Define a function to generate a synthetic dataset using CART in synthpop
# generate_data <- function(seed) {
#   # Set the random seed for this iteration
#   set.seed(seed)
#   # Generate a new synthetic dataset using CART in synthpop
#   new_data <- syn(data2,
#                   # rules = rules.list, 
#                   # rvalues =  rules.value.list,
#                   cont.na = list(race = "missing"),
#                   predictor.matrix = NULL,
#                   visit.sequence = c(3, 5, 1, 2 , 4),
#                   seed = seed,
#                   drop.not.used = TRUE)
# }
# 
# cl <- makeCluster(detectCores())
# 
# while (accepted_samples < num_accepted_samples) {
#   # Generate a list of random seeds for each iteration
#   seeds <- seq(20230503 + accepted_samples, 20230503 + accepted_samples + getDoParWorkers() - 1)
#   # Generate the synthetic datasets in parallel
#   new_data_list <- parLapply(cl, seeds, generate_data)
#   # Convert the list to a data frame
#   new_data <- do.call(rbind, new_data_list)
#   # Check if the counts meet the desired values
#   if (check_counts(new_data, desired_counts)) {
#     # If the counts meet the desired values, add the dataset to the output
#     synth_data <- rbind(synth_data, new_data)
#     # Increment the number of accepted samples
#     accepted_samples <- accepted_samples + 1
#     # Export the accepted sample as a CSV file with a name indicating its order
#     file_name <- paste0("accepted_sample_", accepted_samples, ".csv")
#     write.csv(new_data, file_name, row.names = FALSE)
#   }
# }
# 
# # Stop the parallel backend
# stopCluster(cl)
# 
# # View the final synthetic dataset
# head(synth_data)


loop_counter <- 1
# If no parallel implementation...
while (accepted_samples < num_accepted_samples) {
  # Generate a new synthetic dataset using CART in synthpop
  seed <- sample(1:100000, 1) # choose any integer value to use as a seed
  print(paste("This is loop number:",loop_counter, " Random seed Number: ", seed, " Accepted Sample Number Count: ", accepted_samples))
  new_data <- syn(data2,
               # rules = rules.list,
               # rvalues =  rules.value.list,
               cont.na = list(race = "missing", maternal_age = "NA"),
               predictor.matrix = NULL,
               visit.sequence = c(3, 5, 1, 2 , 4),
               seed = seed,
               drop.not.used = TRUE,
               print.flag = FALSE)
  write.syn(new_data, filename = 'sample', filetype = 'csv')
  new_data <- data.frame(read.csv('sample.csv'))
  new_data$seed <- seed
  new_data$G1dob <- as.Date(as.numeric(new_data$G1dob), origin = '1970-1-1')
  loop_counter <- loop_counter + 1
  
  counts <- table("race" = new_data$race, "mat_age"= new_data$maternal_age, useNA = "always")
  
  White_under20 <- counts[5]
  white_above40 <- counts[23]
  Black_under20 <- counts[2]
  Black_2029 <- counts[8]
  Black_3039 <- counts[14]
  Black_above40 <- counts[20]
  Asian_under20 <- counts[1]
  Asian_2029 <- counts[7]
  Asian_3039 <- counts[13]
  Asian_above40 <- counts[19]
  Other_under20 <- counts[4]
  Other_2029 <- counts[10]
  Other_3039 <- counts[16]
  Other_above40 <- counts[22]
  missing_under20 <- counts[3]
  missing_above40 <- counts[21]
  missingboth <- counts[27]
  
  
  if (#White_under20 >= 362 & 
      #white_above40 >= 135 & 
      Black_under20 >= 8 & 
      #Black_2029 >= 56 & 
      #Black_3039 >= 54 & 
      Black_above40 >= 2 & 
      #Asian_under20 >= 7 & 
      #Asian_2029 >= 68 & 
      #Asian_3039 >= 40 & 
      Asian_above40 == 0 & 
      #Other_under20 >= 3 & 
      #Other_2029 >= 37 & 
      #Other_3039 >=42 & 
      Other_above40 >= 2){ 
      #missing_under20 >= 162 & 
      #missing_above40 >=22 & 
      #missingboth >= 850
    
    synth_data <- rbind(synth_data, new_data)
    accepted_samples <- accepted_samples + 1
    file_name <- paste0("accepted_sample_", accepted_samples, ".csv")
    write.csv(new_data, file_name, row.names = FALSE)
  }
}
  
  

  
#   # Check if the counts meet the desired values
#   if (check_counts(new_data, desired_counts)) {
#     # If the counts meet the desired values, add the dataset to the output
#     synth_data <- rbind(synth_data, new_data)
#     # Increment the number of accepted samples
#     accepted_samples <- accepted_samples + 1
#     # Export the accepted sample as a CSV file with a name indicating its order
#     file_name <- paste0("accepted_sample_", accepted_samples, ".csv")
#     write.csv(new_data, file_name, row.names = FALSE)
#   }
# }

