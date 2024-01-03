# ALSPAC Synthpop Synthetic Data 
setwd() # set working directory
rm(list = ls())
library("synthpop")

# Load Raw Data
data <- data.frame(read.csv('fake_testing.csv')) # fake data for code development
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

# Only keep relevant variables 
data2 <- subset(data2, select = c(maternal_agecat, ethgroup, g1_gender_arc, imddecile, g1_dob_arc1))

# describe data
codebook.syn(data2)
summary(data2)
dim(data2)

# set the number of accepted samples to accept (start with 1) This is such that we can loop until right number is found
num_accepted_samples <- 200

# Generate Data, set seed
seed <- 20230531

synth_data <- syn(data2,
                  cont.na = list(race = 'Missing', maternal_agecat = 'NA'), # specify how missing is coded
                  predictor.matrix = NULL,
                  visit.seqeuence = c(3,5,1,2,4),
                  seed = seed,
                  drop.not.used = TRUE,
                  print.flag = FLASE) # do not need to print in terminal
                  
write.syn(synth_data, filename = 'syndata', filetype = 'csv')
synth_data <- data.frame(read.csv('syndata.csv'))
synth_data$seed <- seed # add seed information back in synthesised data
write.csv(synth_data, "syndata") # replace above

# define accepted sample number (stop at)
accepted_samples <- 0

# re-set start seed
seed <- 8765432

# Define Loop Counter, for record taking how many loops required to capture enough datasets
loop_counter <- 1
while (accepted_samples < num_accepted_samples){
  # gen new data using synthpop
  seed <- seed + 1
  print(paste("This is loop number:", loop_counter, " Random Seed Number:", seed, " Accepted Sample Count", accepted_samples))
  new_data <- syn(data2,
                  cont.na = list(race = 'Missing', maternal_agecat = 'NA'), 
                  predictor.matrix = NULL,
                  visit.seqeuence = c(3,5,1,2,4),
                  seed = seed,
                  drop.not.used = TRUE,
                  print.flag = FLASE)
  write.syn(new_data, filename = 'sample', filetype = 'csv')
  new_data <- data.frame(read.csv('sample.csv'))
  new_data$seed <- seed
  loop_counter <- loop_counter + 1
  
  counts <- table("race" = new_data$race, "mat_age" = new_data$maternal_age, useNA = 'always') # create count variable to count eth/mat_cat num
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
  
  # Conditions to meet
  if (Black_under20 >= 11 & 
      Black_above40 == 0 & 
      Asian_under20 >= 4 & 
      Asian_above40 <= 1 & 
      Other_under20 >= 2 & 
      Other_above40 >= 1){ 

    
    synth_data <- rbind(synth_data, new_data)
    accepted_samples <- accepted_samples + 1
    file_name <- paste0("accepted_sample_", accepted_samples, ".csv")
    write.csv(new_data, file_name, row.names = FALSE)
  }
}
