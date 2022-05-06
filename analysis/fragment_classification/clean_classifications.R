#!/usr/bin/env Rscript

# Author : Kenneth Schackart <schackartk1@gmail.com>
# Date   : 2022-02-03
# Purpose: Clean the combined classification file

# Imports -------------------------------------------------------------------

## Library calls ------------------------------------------------------------

suppressMessages(suppressWarnings(library(dplyr)))
library(magrittr)
library(readr)
library(stringr)
suppressMessages(suppressWarnings(library(tidyr)))

# Argument Parsing ----------------------------------------------------------

#' Parse Arguments
#'
#' Parse command line arguments using argparse.
#'
#' @return args
get_args <- function() {
  parser <-
    argparse::ArgumentParser(description = "Clean combined classifications")
  
  parser$add_argument("file",
                      help = "Combined classifications",
                      metavar = "FILE")
  parser$add_argument(
    "-t",
    "--taxonomy",
    help = "Taxonomy information file",
    metavar = "FILE",
    type = "character",
    default = "data/refseq_info/taxonomy.csv"
  )
  parser$add_argument(
    "-k",
    "--key",
    help = "Classification key",
    metavar = "FILE",
    type = "character",
    default = "src/data_analysis/class_key.txt"
  )
  parser$add_argument(
    "-o",
    "--outdir",
    help = "Output directory",
    metavar = "DIR",
    type = "character",
    default = "out"
  )
  
  
  args <- parser$parse_args()
  
  if (file.access(args$file) == -1) {
    stop(str_glue("Specified file '{args$file}' cannot be accessed."))
  }
  
  if (file.access(args$taxonomy) == -1) {
    stop(str_glue("Specified --taxonomy file '{args$key}' cannot be accessed."))
  }
  
  if (file.access(args$key) == -1) {
    stop(str_glue("Specified --key file '{args$key}' cannot be accessed."))
  }
  
  return(args)
  
}

# Main ----------------------------------------------------------------------

#' Main Function
#'
#' @return
main <- function() {
  args <- get_args()
  file_name <- args$file
  out_dir <- args$outdir
  key_file <- args$key
  
  raw_df <- read_csv(file_name, show_col_types = FALSE)
  
  taxonomy_df <- read_csv(args$taxonomy, show_col_types = FALSE)
  
  viral_classes <- readLines(key_file)[1] %>%
    str_split(",")
  viral_classes <- viral_classes[[1]]
  
  nonviral_classes <- readLines(key_file)[2] %>%
    str_split(",")
  nonviral_classes <- nonviral_classes[[1]]
  
  if (!dir.exists(out_dir)) {
    dir.create(out_dir)
  }
  
  class_df <- raw_df %>%
    complete_classifications() %>%
    standardize_classifications(viral_classes, nonviral_classes) %>%
    stylize_classifiers() %>%
    add_taxonomy(taxonomy_df)
  
  out_file <-  file.path(out_dir, "cleaned_combined.csv")
  
  write.csv(class_df, out_file, row.names = FALSE)
  
  print(str_glue("Done. Wrote file to '{out_file}'"))
}


# Functions -----------------------------------------------------------------

#' Complete cases
#'
#' For tools that only return predicted viruses, fill in negative
#' classification.
#'
#' @param df
#'
#' @return df
complete_classifications <- function(df, viral, nonviral) {
  df %>%
    mutate(rec_len_act = str_c(record, "--", length, "--", actual)) %>%
    select(-record, -length, -actual) %>%
    complete(rec_len_act, tool,  fill = list(prediction = "non-viral")) %>%
    separate(rec_len_act,
             into = c("record", "length", "actual"),
             sep = "--")
}


#' Standardize classifications
#'
#' Make classification classes consistent and binary.
#'
#' @param df
#' @param viral character vector of viral classification names
#' @param nonviral character vector of nonviral classification names
#'
#' @return df
standardize_classifications <- function(df, viral, nonviral) {
  df %>%
    mutate(
      predict_class = case_when(
        prediction %in% viral ~ "viral",
        prediction %in% nonviral ~ "non-viral"
      ),
      actual_class = case_when(actual == "viral" ~ "viral",
                               actual != "viral" ~ "non-viral")
    ) %>%
    mutate(
      predict_class = as.factor(predict_class),
      actual_class = as.factor(actual_class),
      length = factor(length, levels = c("500", "1000", "3000", "5000"))
    )
  
}


#' Stylize classifiers
#'
#' Update names of the classifiers to be properly stylized.
#'
#' @param df
#'
#' @return df
stylize_classifiers <- function(df) {
  df %>%
    mutate(
      tool = case_when(
        tool == "dvf" ~ "DeepVirFinder",
        tool == "metaphinder" ~ "MetaPhinder",
        tool == "seeker" ~ "Seeker",
        tool == "vibrant" ~ "VIBRANT",
        tool == "viralverify" ~ "viralVerify",
        tool == "virfinder" ~ "VirFinder",
        tool == "virsorter" ~ "VirSorter",
        tool == "virsorter2" ~ "VirSorter2"
      )
    ) %>%
    mutate(tool = as.factor(tool))
}


#' Add taxonomy
#'
#' Add columns detailing taxonomic information
#'
#' @param df
#' @param taxonomy_df Dataframe of taxonomy
#'
#' @return df
add_taxonomy <- function(df, taxonomy_df) {
  # Drop kingdom, same values as actual
  taxonomy_df <- taxonomy_df %>%
    select(-kingdom) %>%
    unique()
  
  # Sequence IDs are in a longer string, extract them out
  seqid_pattern <- "^frag_[:digit:]*_(.*)$"
  
  # Join taxonomy and classification dataframes
  df %>%
    mutate(seq_id = str_match(record, seqid_pattern)[, 2]) %>%
    left_join(taxonomy_df, by = "seq_id")
}

# Call Main -----------------------------------------------------------------
if (!interactive()) {
  main()
}
