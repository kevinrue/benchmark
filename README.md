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

* TAB-separated (`\t`)
  * Column 1 must be a program name in the following list:
    * `MuTect2`, `Strelka`, `Virmid`, `EBCall`, (soon: `VarScan`, `CaVEMan`)
  * Column 2 must a semicolon-separated (`;`) list of `flag=value` pairs
    that will be supplied to the program. The framework parses those
    pairs and reformats them to produce a valid call to the program.
    In particular, `flag` must be written exactly as it would be in
    a direct call to the program; short and long options must be
    prefixed with the adequate number of hyphens, for programs that use
    a configuration file with `flag=value` syntax, `flag` must not be
    prefixed by any hyphen (see example configuration files in this
    repository for reference).