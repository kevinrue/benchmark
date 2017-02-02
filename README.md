# Benchmark

A framework to run multiple programs under multiple configurations.
Currently designed to benchmark somatic variant calling programs.

# Requirements

* Python (>= 3.0)

# Usage

    usage: benchmark_somatic_callers.py [-h] [-d]
                                        config.txt ./benchmark reference.fa
                                        normal.bam tumour.bam

    Benchmark a selection of software and configurations.

    positional arguments:
      ./config.txt     A file of programs and configurations to run. The file is
                     TAB-separated. Column 1 must be one of the following program
                     names: {Mutect2, Strelka}. Column 2 must be a semicolon-
                     separated list of --flag=value pairs. Those pairs are
                     subsequently adapted to the program command line format.
      ./benchmark    Overall output folder for the benchmark.
      ./reference.fa   Reference genome Fasta file.
      ./normal.bam     Input file for reference group (e.g. normal.bam).
      ./tumour.bam     Input file for target group (e.g. tumour.bam).

    optional arguments:
      -h, --help     show this help message and exit
      -d, --dry-run  Do not submit scripts as jobs.

# Configuration

The framework requires a configuration file in which each line defines
the configuration of one run for one program. The format of the
configuration file is as follows:

* TAB-separated (`\t`) file of two columns:
  1. A program name in the following (case-sensitive)
    list:
    * `MuTect2`, `Strelka`, `Virmid`, `EBCall`, `VarScan`
      (soon: `CaVEMan`)
  2. A semicolon-separated (`;`) list of `flag=value` pairs or
   `flag`-only toggles that will be supplied to the program.
    The framework parses those flags (and values), and formats them
    to produce a valid call to the program.
    In most cases, `flag` must be written exactly as it would be in
    a direct call to the program: short and long options must be
    prefixed with the adequate number of hyphens, for programs that use
    a configuration file with `flag=value` syntax, `flag` must not be
    prefixed by any hyphen (see example configuration files in this
    repository for reference).
    * **Special case**: the `CaVEMan` program is split in several steps
      with overlapping sets of flags. As a consequence, this framework
      requires flags to be prefixed by one of the following
      keywords to specify which of the steps should be given the
      information:
      * `setup`, `split`, `Mstep`, `Merge`, `Estep`


# Post-processing

Currently, only the VCF file produced by `MuTect2` is further processed
to obtain the count of each value in the VCF `FILTER` field.
