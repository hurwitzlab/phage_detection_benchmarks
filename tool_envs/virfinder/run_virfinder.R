#!/usr/bin/env Rscript

# Author : Kenneth Schackart <schackartk1@gmail.com>
# Date   : 2021-11-16
# Purpose: Predict with VirFinder

# Imports -------------------------------------------------------------------

## Library calls ------------------------------------------------------------

library(magrittr)
library(VirFinder)

# Argument Parsing ----------------------------------------------------------

#' Parse Arguments
#'
#' Parse command line arguments using argparse.
#'
#' @return args
get_args <- function() {
  parser <- argparse::ArgumentParser(description = "Predict with VirFinder")
  
  parser$add_argument("files",
                      help = "A positional argument",
                      metavar = "FILE",
                      nargs="+")
  parser$add_argument("-o",
                      "--outdir",
                      help = "Output directory",
                      metavar = "DIR",
                      type = "character",
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
  out_dir <- args$outdir

  if (!dir.exists(out_dir)) {
    dir.create(out_dir)
  }
  
  for (file in args$files) {

    file_name <- basename(file)
    split_name <- strsplit(file_name, "\\.")[[1]]
    base <- split_name[1]
    ext <- split_name[2]

    preds <- VF.pred(file)

    out_file <- file.path(out_dir, paste(base, "_vf_preds.", ext, sep=""))
    write.table(preds, out_file, row.names=F, col.names=T, sep="\t")
  }
}

# Call Main -----------------------------------------------------------------
if (!interactive()) {
  main()
}

