#!/usr/bin/env Rscript

# Author : Kenneth Schackart <schackartk1@gmail.com>
# Date   : 2022-01-25
# Purpose: Retrieve and join taxIDs

# Imports -------------------------------------------------------------------

## Library calls ------------------------------------------------------------

suppressWarnings(suppressMessages(library(dplyr)))
library(magrittr)
library(readr)
library(stringr)

# Argument Parsing ----------------------------------------------------------

#' Parse Arguments
#'
#' Parse command line arguments using argparse.
#'
#' @return args
get_args <- function() {
  parser <-
    argparse::ArgumentParser(description = "Retrieve and join taxIDs")
  
  parser$add_argument("summaries",
                      help = "RefSeq assembly information files",
                      metavar = "FILE",
                      nargs = "+")
  parser$add_argument(
    "-i",
    "--ids",
    help = "Extracted accession and seq IDs file",
    metavar = "FILE",
    required = TRUE
  )
  parser$add_argument(
    "-o",
    "--outdir",
    help = "Output directory",
    type = "character",
    metavar = "DIR",
    default = "out"
  )
  
  
  args <- parser$parse_args()
  
  return(args)
  
}

# Main ----------------------------------------------------------------------

#' Main Function
#'
#' @return
main <- function() {
  args <- get_args()
  ids_file <- args$ids
  out_dir <- args$outdir
  
  if (file.access(ids_file) == -1) {
    stop(str_glue("Specified file '{ids_file}' cannot be accessed."))
  } else {
    taxonomy_df <- read.csv(ids_file)
  }
  
  if (!dir.exists(out_dir)) {
    dir.create(out_dir)
  }
  
  out_file <-  file.path(out_dir, "tax_ids.csv")
  
  assembly_df <- tibble()

  for (file_name in args$summaries) {
    
    if (file.access(file_name) == -1) {
      stop(str_glue("Specified file '{file_name}' cannot be accessed."))
    } else {
      assembly_df <- assembly_df %>% rbind(read_tsv(file_name, show_col_types = FALSE))
    }
    
  }

  
  assembly_df <- assembly_df %>%
	    select(assembly_accession, taxid, species_taxid)
	
  joined_ids <- left_join(taxonomy_df, assembly_df, by = c("accession" =  "assembly_accession"))

  write.csv(joined_ids, out_file, row.names = FALSE)

  print(str_glue("Done. Wrote file to '{out_file}'"))
}

# Call Main -----------------------------------------------------------------
if (!interactive()) {
  main()
}
