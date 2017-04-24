
# Notes ----

notes <- '
12G     Default configuration for each tool (Virmid failed).
257G	1_2017-02-14: first 124 configurations tested (some of them default).
'

library(VariantAnnotation)

# Functions ----

supportedPrograms <- c("MuTect2","Strelka","EBCall","VarScan","CaVEMan") # Virmid

# Identify supported program sub-folders within a benchmark run folder
scanPrograms <- function(dir){
    programDirs <- dir(
        dir, paste(sprintf("(%s)", supportedPrograms), collapse="|")
    )
    if (length(programDirs) < 1) stop("No program sub-folder detected.")
    return(programDirs)
}

# Identify configurations sub-folders within a program folder
scanConfigs <- function(dir){
    configDirs <- dir(dir, "config_")
    if (length(configDirs) < 1) stop("No configuration sub-folder detected.")
    return(configDirs)
}

# Settings ----

benchmarkDir <- "/gpfs2/well/ratcliff/data/kevin/somatic_benchmark/1_2017-02-14"
MuTect2.vcf <- "output.vcf"
benchmark.config <- "benchmark_config.txt"

Mutect2.d.config <- c(
    "--initial_normal_lod" = 0.5,
    "--initial_tumor_lod" = 4.0,
    "--max_alt_allele_in_normal_fraction" = 0.03,
    "--max_alt_alleles_in_normal_count" = 1,
    "--max_alt_alleles_in_normal_qscore_sum" = 20,
    "--normal_lod" = 2.2,
    "--tumor_lod" = 6.3
)

# Processing ----

# Identify all programs present in benchmark run
programDirs <- scanPrograms(benchmarkDir)

# MuTect2 # TODO: loop through each supported program
# Identify all configurations
configDirs <- scanConfigs(file.path(benchmarkDir, "MuTect2"))
cConfig <- configDirs[1] # Current configuration # TODO: loop through each configuration
# Define path to VCF file with variant calls
vcfFile <- file.path(benchmarkDir, "MuTect2", cConfig, MuTect2.vcf)
# Define path to declared configuration
configFile <- file.path(benchmarkDir, "MuTect2", cConfig, benchmark.config)
# Import data from VCF
vcfData <- readVcf(vcfFile)
# Import declared configuration parameters (named vector)
tmp <- read.table(configFile, col.names = c("flag", cConfig))
configInfo <- Mutect2.d.config # set default
configInfo[tmp$flag] <- tmp$config_1 # update declared parameters

countTotal <- nrow(vcfData)
countPass <- sum(rowRanges(vcfData)$FILTER == "PASS")
propPass <- countPass / countTotal

table(info(vcfData)$DB) # T/F count of dbSNP membership



rowRanges(vcfData)
