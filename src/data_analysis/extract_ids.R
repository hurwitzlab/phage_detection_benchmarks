#!/usr/bin/env Rscript

# Author : Kenneth Schackart <schackartk1@gmail.com>
# Date   : 2022-01-25
# Purpose: Extract Assembly Accession and Record IDs

# Imports -------------------------------------------------------------------

## Library calls ------------------------------------------------------------

suppressWarnings(suppressMessages(library(dplyr)))
library(magrittr)
library(stringr)

# Argument Parsing ----------------------------------------------------------

#' Parse Arguments
#'
#' Parse command line arguments using argparse.
#'
#' @return args
get_args <- function() {
  parser <-
    argparse::ArgumentParser(description = "Extract Assembly Accession and Record IDs")
  
  parser$add_argument("file",
                      help = "File resulting from grep '>' on genome files",
                      metavar = "FILE")
  parser$add_argument("-o",
                      "--outdir",
                      help = "Output directory",
                      metavar = "DIR",
                      type = "character",
                      default = "out")
  
  args <- parser$parse_args()
  
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
  
  if (file.access(file_name) == -1) {
    stop(str_glue("Specified file '{file_name}' cannot be accessed."))
  } else {
    ids <- readLines(file_name)
  }
  
  if (!dir.exists(out_dir)) {
    dir.create(out_dir)
  }
  
  out_file <-  file.path(out_dir, "extracted_ids.csv")
  
  expression <- paste0(
    "([[:alpha:]]+)/",
    # kingdom
    "([[:alpha:]]{3}_[[[:alnum:]]\\.]+)_.*",
    # accession
    ">([[[:alnum:]]_\\.]+)\\s.*"             # seq_id
  )
  
  taxonomy <- ids %>%
    str_match(expression) %>%
    as_tibble() %>%
    rename(
      original = "V1",
      kingdom = "V2",
      accession = "V3",
      seq_id = "V4"
    ) %>%
    select(-original)
  
  write.csv(taxonomy, out_file, row.names = FALSE)
  
  print(str_glue("Done. Wrote file to '{out_file}'"))
}

# Call Main -----------------------------------------------------------------
if (!interactive()) {
  main()
}
