#!/usr/bin/env Rscript

# Author : Kenneth Schackart <schackartk1@gmail.com>
# Date   : 2022-02-03
# Purpose: Get taxnomy using taxonomizr

# Imports -------------------------------------------------------------------

## Library calls ------------------------------------------------------------

suppressMessages(suppressWarnings(library(dplyr)))
library(magrittr)
library(readr)
library(stringr)
library(taxonomizr)

# Argument Parsing ----------------------------------------------------------

#' Parse Arguments
#'
#' Parse command line arguments using argparse.
#'
#' @return args
get_args <- function() {
  parser <-
    argparse::ArgumentParser(description = "Get taxonomy using taxonomizr")
  
  parser$add_argument("file",
                      help = "File with taxid column",
                      metavar = "FILE")
  parser$add_argument("-o",
                      "--outdir",
                      help = "Output directory",
                      metavar = "DIR",
                      type = "character",
                      default = "out")
  parser$add_argument("-d",
		      "--db",
		      help = "taxonomizr database",
		      metavar = "DB",
		      type = "character",
		      default = "data/taxonomizr/accession_taxa.sql")
  
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
  db <- args$db
  
  if (file.access(file_name) == -1) {
    stop(str_glue("Specified file '{file_name}' cannot be accessed."))
  } else {
    ids <- read_csv(file_name, show_col_types = FALSE)
  }

  if (file.access(db) == -1) {
    stop(str_glue("Specified database '{db}' cannot be accessed."))
  }
  
  if (!dir.exists(out_dir)) {
    dir.create(out_dir)
  }
  
  out_file <-  file.path(out_dir, "taxonomy.csv")
  
  taxonomy <- ids$taxid %>%
    getTaxonomy(db) %>%
    as_tibble() %>%
    bind_cols(ids, .)
  
  write.csv(taxonomy, out_file, row.names = FALSE)
  
  print(str_glue("Done. Wrote file to '{out_file}'"))
}

# Call Main -----------------------------------------------------------------
if (!interactive()) {
  main()
}
