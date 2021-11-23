#!/usr/bin/env Rscript

# Author : Kenneth Schackart <schackartk1@gmail.com>
# Date   : 2021-11-16
# Purpose: Predict with VirFinder

# Imports -------------------------------------------------------------------

## Library calls ------------------------------------------------------------

suppressMessages(library(stringr))
suppressMessages(library(VirFinder))

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
  

  n_files <- 0

  for (file in args$files) {

    file_name <- basename(file)
    base <- strsplit(file_name, "\\.")[[1]][1]

    invisible(capture.output(preds <- VF.pred(file)))

    out_file <- file.path(out_dir, paste(base, "_vf_preds.csv", sep=""))
    write.table(preds, out_file, row.names=F, col.names=T, sep="\t")

    n_files <- n_files + 1
  }

  plu <- if(n_files > 1) "s" else ""
  print(str_glue("Done. Wrote {n_files} file{plu} to {out_dir}."))
 
}

# Call Main -----------------------------------------------------------------
if (!interactive()) {
  main()
}

