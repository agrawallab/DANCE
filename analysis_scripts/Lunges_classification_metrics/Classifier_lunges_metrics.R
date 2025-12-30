# Load the libraries
library(ggplot2)
library(tidyverse)
library(dplyr)

# Set working directories
input_dir <- "~/Documents/DANCE/Modified tables"
output_dir <- "~/Documents/DANCE/modified tables"

# Ensure the output directory exists
if (!dir.exists(output_dir)) {
  dir.create(output_dir)
}

# Get a list of all CSV files in the input directory
csv_files <- list.files(input_dir, pattern = "*.csv", full.names = TRUE)

# Set up a single log file for all output
log_file_name <- paste0(output_dir, "/all_files_log.txt")

# Start logging output to a single log file
sink(log_file_name)

# Helper function to match vector lengths by padding with NAs or truncating
lengthen_vector <- function(vec, desired_length) {
  if (length(vec) < desired_length) {
    vec <- c(vec, rep(NA, desired_length - length(vec)))
  } else if (length(vec) > desired_length) {
    vec <- vec[1:desired_length]
  }
  return(vec)
}

# Function to calculate TP, FP, FN, Precision, Recall, F1
calculate_metrics <- function(ground_truth, predicted) {
  TP <- length(intersect(ground_truth, predicted))
  FP <- length(setdiff(predicted, ground_truth))
  FN <- length(setdiff(ground_truth, predicted))
  
  Precision <- TP / (TP + FP)
  Recall <- TP / (TP + FN)
  F1 <- 2 * (Precision * Recall) / (Precision + Recall)
  
  return(list(TP = TP, FP = FP, FN = FN, Precision = Precision, Recall = Recall, F1 = F1))
}

# Initialize a data frame to store TP, FP, FN for all files
all_metrics_df <- data.frame()

# Loop over each CSV file
for (file_path in csv_files) {
  
  # Load the data from the CSV file
  df <- read.csv(file_path)
  
  # Extracting the file base name for logging
  file_base_name <- tools::file_path_sans_ext(basename(file_path))
  
  # Print the file being processed
  print(paste("Processing file:", basename(file_path)))
  
  # Print column names to verify
  print(names(df))
  
  # Using dplyr's select with matches() to dynamically select columns
  fly1_gt <- df %>% select(matches("Groundtruth.*Fly.1"))
  fly2_gt <- df %>% select(matches("Groundtruth.*Fly.2"))
  
  fly1_dance <- df %>% select(matches("DANCE.*Fly.1"))
  fly2_dance <- df %>% select(matches("DANCE.*Fly.2"))
  
  fly1_cad <- df %>% select(matches("CADABRA.*Fly.1"))
  fly2_cad <- df %>% select(matches("CADABRA.*Fly.2"))
  
  fly1_div <- df %>% select(matches("Divider.*Fly.1"))
  fly2_div <- df %>% select(matches("Divider.*Fly.2"))
  
  # Check if any columns were found
  if (length(fly1_gt) == 0 || length(fly2_gt) == 0 ||
      length(fly1_dance) == 0 || length(fly2_dance) == 0 ||
      length(fly1_cad) == 0 || length(fly2_cad) == 0 ||
      length(fly1_div) == 0 || length(fly2_div) == 0) {
    print("Error: One or more required columns are missing in this file.")
    next
  }
  
  # Convert data frames to vectors
  fly1_gt <- unlist(fly1_gt)
  fly2_gt <- unlist(fly2_gt)
  
  fly1_dance <- unlist(fly1_dance)
  fly2_dance <- unlist(fly2_dance)
  
  fly1_cad <- unlist(fly1_cad)
  fly2_cad <- unlist(fly2_cad)
  
  fly1_div <- unlist(fly1_div)
  fly2_div <- unlist(fly2_div)
  
  # Determine the maximum length to ensure consistency
  max_length <- max(length(fly1_gt), length(fly2_gt), 
                    length(fly1_dance), length(fly2_dance), 
                    length(fly1_cad), length(fly2_cad), 
                    length(fly1_div), length(fly2_div))
  
  # Ensure all vectors have the same length
  fly1_gt <- lengthen_vector(fly1_gt, max_length)
  fly2_gt <- lengthen_vector(fly2_gt, max_length)
  
  fly1_dance <- lengthen_vector(fly1_dance, max_length)
  fly2_dance <- lengthen_vector(fly2_dance, max_length)
  
  fly1_cad <- lengthen_vector(fly1_cad, max_length)
  fly2_cad <- lengthen_vector(fly2_cad, max_length)
  
  fly1_div <- lengthen_vector(fly1_div, max_length)
  fly2_div <- lengthen_vector(fly2_div, max_length)
  
  # Merging fly1 and fly2 data into single columns
  merged_gt <- c(fly1_gt, fly2_gt)
  merged_dance <- c(fly1_dance, fly2_dance)
  merged_cad <- c(fly1_cad, fly2_cad)
  merged_div <- c(fly1_div, fly2_div)
  
  # Remove rows where all values are NA
  merged_df <- data.frame(
    Groundtruth = merged_gt,
    DANCE = merged_dance,
    CADABRA = merged_cad,
    Divider = merged_div
  )
  
  merged_df <- merged_df[rowSums(is.na(merged_df)) < ncol(merged_df), ]
  
  # Calculate metrics for each comparison
  metrics_dance <- calculate_metrics(merged_gt, merged_dance)
  metrics_cad <- calculate_metrics(merged_gt, merged_cad)
  metrics_div <- calculate_metrics(merged_gt, merged_div)
  
  # Combine the results into a data frame for this file
  results_df <- data.frame(
    Comparison = c("Groundtruth vs DANCE", "Groundtruth vs CADABRA", "Groundtruth vs Divider"),
    True_Positives = c(metrics_dance$TP, metrics_cad$TP, metrics_div$TP),
    False_Positives = c(metrics_dance$FP, metrics_cad$FP, metrics_div$FP),
    False_Negatives = c(metrics_dance$FN, metrics_cad$FN, metrics_div$FN),
    Precision = c(metrics_dance$Precision, metrics_cad$Precision, metrics_div$Precision),
    Recall = c(metrics_dance$Recall, metrics_cad$Recall, metrics_div$Recall),
    F1_Score = c(metrics_dance$F1, metrics_cad$F1, metrics_div$F1)
  )
  
  # Print the results data frame
  print(results_df)
  
  # Create a unique output file name based on the input file name
  output_file_name <- paste0(output_dir, "/", file_base_name, "_metrics_results.csv")
  
  # Write the results to a CSV file
  write.csv(results_df, output_file_name, row.names = FALSE)
  
  # Store TP, FP, FN values in a combined data frame for all files
  file_metrics_df <- data.frame(
    File = file_base_name,
    Comparison = c("Groundtruth vs DANCE", "Groundtruth vs CADABRA", "Groundtruth vs Divider"),
    TP = c(metrics_dance$TP, metrics_cad$TP, metrics_div$TP),
    FP = c(metrics_dance$FP, metrics_cad$FP, metrics_div$FP),
    FN = c(metrics_dance$FN, metrics_cad$FN, metrics_div$FN)
  )
  
  # Append the current file's metrics to the overall data frame
  all_metrics_df <- rbind(all_metrics_df, file_metrics_df)
}

# Save the combined TP, FP, FN data for all files
output_file_name_metrics <- paste0(output_dir, "/all_files_tp_fp_fn_metrics.csv")
write.csv(all_metrics_df, output_file_name_metrics, row.names = FALSE)

# Stop redirecting output and return to the console
sink()

# Calculating the overall precision, recall and F1 score for each model

# Read in the CSV file with TP, FP, FN values
metrics_df <- read.csv(output_file_name_metrics)

# Define a function to calculate overall metrics for a specific classifier
calculate_overall_metrics <- function(df, classifier) {
  filtered_df <- df %>%
    filter(Comparison == classifier)
  
  total_TP <- sum(filtered_df$TP)
  total_FP <- sum(filtered_df$FP)
  total_FN <- sum(filtered_df$FN)
  
  precision <- total_TP / (total_TP + total_FP)
  recall <- total_TP / (total_TP + total_FN)
  f1_score <- 2 * (precision * recall) / (precision + recall)
  
  return(data.frame(
    Classifier = classifier,
    Precision = precision,
    Recall = recall,
    F1_Score = f1_score
  ))
}

# Calculate metrics for each classifier
metrics_dance <- calculate_overall_metrics(metrics_df, "Groundtruth vs DANCE")
metrics_cadabra <- calculate_overall_metrics(metrics_df, "Groundtruth vs CADABRA")
metrics_divider <- calculate_overall_metrics(metrics_df, "Groundtruth vs Divider")

# Combine the results into a single data frame
overall_metrics <- bind_rows(metrics_dance, metrics_cadabra, metrics_divider)

# Print the overall metrics
print(overall_metrics)

# Optionally, save the overall metrics to a new CSV file
overall_metrics_output_file <- paste0(output_dir, "/overall_metrics.csv")
write.csv(overall_metrics, overall_metrics_output_file, row.names = FALSE)

# Print confirmation of saved file
cat("Overall metrics saved at:", overall_metrics_output_file, "\n")

# Optional: Print the lengths of the vectors for debugging purposes
print(length(merged_gt), length(merged_dance), length(merged_cad), length(merged_div))

