# Calling libraries
library(tidyverse)
library(dplyr)

# Parse command-line arguments
# Usage: Rscript timestamps_to_frames.R /path/to/folder [filename.txt]
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript timestamps_to_frames.R <input_folder> [filename.txt]")
# The folder that contains your CADABRA .txt timestamp files
input_folder  <- args[1]
# Optional: specific filename for the single-file section (defaults to the original name)
single_file   <- if (length(args) >= 2) args[2] else "Lunges_dates_A2p07.txt"

setwd(input_folder)

# Read the file into a data frame, specifying the correct separator
lunges_data <- read.table(single_file, header = FALSE, skip = 3, fill = TRUE)

# Remove unnecessary columns (assuming the relevant data is in the second and third columns)
lunges_data <- lunges_data[, 1:2]
lunges_data = lunges_data[-c(1:2),]

# Rename the columns
colnames(lunges_data) <- c("Timestamps_Fly1", "Timestamps_Fly2")
class(lunges_data) 

# Convert columns to numeric (if they are not already)
lunges_data$Timestamps_Fly1 <- as.numeric(as.character(lunges_data$Timestamps_Fly1))
lunges_data$Timestamps_Fly2 <- as.numeric(as.character(lunges_data$Timestamps_Fly2))


# Convert timestamps to frames (30 fps)
lunges_data$Frames_Fly1 <- lunges_data$Timestamps_Fly1 * 30
lunges_data$Frames_Fly2 <- lunges_data$Timestamps_Fly2 * 30

# Extracting Frames data
frames_data = lunges_data[c(3,4)]

# Combine the two columns into one
df <- frames_data %>%
  pivot_longer(cols = c(Frames_Fly1, Frames_Fly2), names_to = "Fly", values_to = "Frames") %>%
  arrange(Frames)
 
# Create a new data frame with the modified values
df_modified <- df %>%
  mutate(Frames_plus1 = Frames + 1,
         Frames_minus1 = Frames - 1) %>%
  select(Fly, Frames_minus1, Frames, Frames_plus1) %>%
  pivot_longer(cols = c(Frames_minus1, Frames, Frames_plus1), names_to = "Type", values_to = "Frames") %>%
  arrange(Frames)

# Save the data frame to a CSV file
write.csv(df_modified, "lunges_A2_p07_frames.csv", row.names = FALSE)

##################################### In bulk ################################################

# The bulk section processes all .txt files in the same folder supplied above.
# To use a different folder for bulk processing, pass it as a third argument:
#   Rscript timestamps_to_frames.R /single/file/folder Lunges_dates.txt /bulk/folder
bulk_folder <- if (length(args) >= 3) args[3] else input_folder
setwd(bulk_folder)

# List all .txt files in the directory
file_list <- list.files(pattern = "*.txt")

# Loop over each file and process it
for (file_name in file_list) {
  
  # Read the file into a data frame, specifying the correct separator
  lunges_data <- read.table(file_name, header = FALSE, skip = 3, fill = TRUE)
  
  # Remove unnecessary columns (assuming the relevant data is in the first two columns)
  lunges_data <- lunges_data[, 1:2]
  lunges_data = lunges_data[-c(1:2),]
  
  # Rename the columns
  colnames(lunges_data) <- c("Timestamps_Fly1", "Timestamps_Fly2")
  
  # Convert columns to numeric (if they are not already)
  lunges_data$Timestamps_Fly1 <- as.numeric(as.character(lunges_data$Timestamps_Fly1))
  lunges_data$Timestamps_Fly2 <- as.numeric(as.character(lunges_data$Timestamps_Fly2))
  
  # Convert timestamps to frames (assuming 30 fps)
  lunges_data$Frames_Fly1 <- lunges_data$Timestamps_Fly1 * 30
  lunges_data$Frames_Fly2 <- lunges_data$Timestamps_Fly2 * 30
  
  # Extracting Frames data
  frames_data <- lunges_data[c("Frames_Fly1", "Frames_Fly2")]
  
  # Combine the two columns into one
  df <- frames_data %>%
    pivot_longer(cols = c(Frames_Fly1, Frames_Fly2), names_to = "Fly", values_to = "Frames") %>%
    arrange(Frames)
  
  # Create a new data frame with the modified values
  df_modified <- df %>%
    mutate(Frames_plus1 = Frames + 1,
           Frames_minus1 = Frames - 1) %>%
    select(Fly, Frames_minus1, Frames, Frames_plus1) %>%
    pivot_longer(cols = c(Frames_minus1, Frames, Frames_plus1), names_to = "Type", values_to = "Frames") %>%
    arrange(Frames)
  
  # Save the data frame to a CSV file with a new name
  output_file_name <- paste0("processed_", tools::file_path_sans_ext(file_name), ".csv")
  write.csv(df_modified, output_file_name, row.names = FALSE)
  
  # Print the name of the processed file
  print(paste("Processed file:", file_name))
}


