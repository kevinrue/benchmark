
import logging
import subprocess
import re

from LocalSettings import *

logging.basicConfig(level=logging.DEBUG)


class SinglePairedConfiguration:
    """
    A class to store a single configuration to benchmark a program.
    """

    config_filename = 'benchmark_config.txt'
    script_filename = 'benchmark_script.sh'
    job_stdout = 'stdout.log'
    job_stderr = 'stderr.log'
    n_cores = 4

    def __init__(self, params, index):
        """
        Constructor for the SinglePairedConfiguration class.
        :param params: Dictionary of flag:value pairs.
        :param index: Index of the configuration in the list of the program.
        """
        self.params = params
        self.index = index
        self.out = "config_{0}".format(index)

    def make_dir_structure(self, out):
        """
        :param out: Root folder to store outputs of the program.
        :return: None
        """
        config_folder = os.path.join(out, self.out)
        logging.info("Create configuration output folder: {0}".format(config_folder))
        os.mkdir(config_folder)
        self.write_config_file(config_folder)
        return None

    def write_config_file(self, out):
        """
        Write the configuration parameters in a file in the corresponding folder.
        :param out: Folder to store outputs of the configuration.
        :return: None
        """
        config_file = os.path.join(out, self.config_filename)
        logging.info("Create configuration log file: {0}".format(config_file))
        with open(config_file, 'w') as stream:
            for (k, v) in self.params.items():
                if v is None:
                    v = 'NA'
                stream.write("{0}\t{1}\n".format(k, v))
        return None

    def write_MuTect2_script(self, out, exe, ref, file1, file2):
        """
        Write a script to run the configuration using the Mutect2 program.
        :param out: Folder to store outputs of the program.
        :param exe: Path to executable of the program.
        :param ref: Reference genome Fasta file.
        :param file1: Input file for reference group (e.g. normal).
        :param file2: Input file for target group (e.g. tumour).
        :return: None
        """
        output_dir = os.path.join(out, self.out)
        script_file = os.path.join(output_dir, self.script_filename)
        logging.info("Create script file: {0}".format(script_file))
        output_vcf = os.path.join(out, self.out, 'output.vcf')
        output_filters = os.path.join(out, self.out, 'filters.txt')
        dbsnp = "--dbsnp {0}".format(os.path.join(ref_beds_dir, 'known.vcf'))
        cosmic = "--cosmic {0}".format(os.path.join(ref_beds_dir, 'Cosmic.vcf'))
        lexico = '-U ALLOW_SEQ_DICT_INCOMPATIBILITY'
        cmd = "{0} -Xmx25g -jar {1} -T MuTect2 -R {2} -I:tumor {3} -I:normal {4} {5} {6} -o {7} {8}".format(
            java_exe, exe, ref, file2, file1, dbsnp, cosmic, output_vcf, lexico
        )
        for key in self.params.keys():
            if self.params[key] is None:
                raise ValueError("MuTect2 does not support flags without value: {0}".format(key))
            cmd += " {0} {1}".format(key, self.params[key])
            self.write_prolog_script(script_file, output_dir)
        cmd += "\n"
        with open(script_file, 'a') as stream:
            stream.write(cmd)
            stream.write(
                "awk '$0 ~ /^[^#]/ {{nFilters = split($7,filters,\";\"); for (i = 0; i < nFilters; ++i) {{print filters[i+1]}} }}' {0} | sort | uniq -c > {1}".format(
                    output_vcf, output_filters
                )
            )
        self.make_script_executable(script_file)
        return None

    def write_Strelka_script(self, out, exe, ref, file1, file2, template):
        """
        Write a script to run the configuration using the Mutect2 program.
        :param out: Folder to store outputs of the program.
        :param exe: Path to executable of the program.
        :param ref: Reference genome Fasta file.
        :param file1: Input file for reference group (e.g. normal).
        :param file2: Input file for target group (e.g. tumour).
        :param template: Template Strelka configuration file.
        :return: None
        """
        script_file = os.path.join(out, self.out, self.script_filename)
        logging.info("Create script file: {0}".format(script_file))
        config_dir = os.path.join(out, self.out)
        config_file = os.path.join(config_dir, 'strelka_config.ini')
        output_basedir = 'analysis'
        output_fulldir = os.path.join(config_dir, output_basedir)
        cmd = "{0} --normal {1} --tumor {2} --ref {3} --config {4} --output-dir {5}\n".format(
            exe, file1, file2, ref, config_file, output_fulldir
        )
        self.write_prolog_script(script_file, config_dir)
        with open(script_file, 'a') as stream:
            stream.write("cp {0} {1}\n".format(template, config_file))
            for key in self.params.keys():
                if self.params[key] is None:
                    raise ValueError("Strelka does not support flags without value: {0}".format(key))
                stream.write("sed -i 's/^{0} = .*$/{0} = {1} # edited/' {2}\n".format(key, self.params[key], config_file))
            stream.write(cmd)
            stream.write("cd {0}\n".format(output_basedir))
            stream.write("make\n")
        self.make_script_executable(script_file)
        return None

    def write_Virmid_script(self, out, exe, ref, file1, file2):
        """
        Write a script to run the configuration using the Mutect2 program.
        :param out: Folder to store outputs of the program.
        :param exe: Path to executable of the program.
        :param ref: Reference genome Fasta file.
        :param file1: Input file for reference group (e.g. normal).
        :param file2: Input file for target group (e.g. tumour).
        :return: None
        """
        output_dir = os.path.join(out, self.out)
        script_file = os.path.join(output_dir, self.script_filename)
        logging.info("Create script file: {0}".format(script_file))
        cmd = "{0} -Xmx25g -jar {1} -R {2} -D {3} -N {4} -w {5}".format(
            java_exe, exe, ref, file2, file1, output_dir
        )
        for key in self.params.keys():
            if self.params[key] is None:
                raise ValueError("Virmid does not support flags without value: {0}".format(key))
            cmd += " {0} {1}".format(key, self.params[key])
            self.write_prolog_script(script_file, output_dir)
        cmd += "\n"
        with open(script_file, 'a') as stream:
            stream.write(cmd)
        self.make_script_executable(script_file)
        return None

    def write_EBCall_script(self, out, exe, ref, file1, file2, template, normal_list):
        """
        Write a script to run the configuration using the Mutect2 program.
        :param out: Folder to store outputs of the program.
        :param exe: Path to executable of the program.
        :param template: Template EBcall configuration script.
        :param normal_list: List of paths to .bam files for non-paired normal reference samples.
        :param ref: Reference genome Fasta file.
        :param file1: Input file for reference group (e.g. normal).
        :param file2: Input file for target group (e.g. tumour).
        :return: None
        """
        script_file = os.path.join(out, self.out, self.script_filename)
        logging.info("Create script file: {0}".format(script_file))
        config_dir = os.path.join(out, self.out)
        config_script = os.path.join(config_dir, 'EBcall_config.sh')
        output_dir = os.path.join(config_dir, 'analysis')
        cmd = "sh {0} {1} {2} {3} {4} {5}\n".format(
            exe, file2, file1, output_dir, normal_list, config_script,
        )
        self.write_prolog_script(script_file, config_dir)
        with open(script_file, 'a') as stream:
            stream.write("cp {0} {1}\n".format(template, config_script))
            stream.write("sed -i 's|^PATH_TO_REF=.*$|PATH_TO_REF={0} # edited|' {1}\n".format(ref, config_script))
            stream.write("sed -i 's|^PATH_TO_SAMTOOLS=.*$|PATH_TO_SAMTOOLS={0} # edited|' {1}\n".format(
                samtools_dir, config_script)
            )
            stream.write("sed -i 's|^PATH_TO_R=.*$|PATH_TO_R={0} # edited|' {1}\n".format(R_dir, config_script))
            for key in self.params.keys():
                if self.params[key] is None:
                    raise ValueError("EBCall does not support flags without value: {0}".format(key))
                stream.write("sed -i 's/^{0}=.*$/{0}={1} # edited/' {2}\n".format(key, self.params[key], config_script))
            stream.write(cmd)
        self.make_script_executable(script_file)
        return None

    def write_VarScan_script(self, out, exe, ref, file1, file2):
        """
        Write a script to run the configuration using the VarScan program.
        :param out: Folder to store outputs of the program.
        :param exe: Path to executable of the program.
        :param ref: Reference genome Fasta file.
        :param file1: Input file for reference group (e.g. normal).
        :param file2: Input file for target group (e.g. tumour).
        :return: None
        """
        output_dir = os.path.join(out, self.out)
        script_file = os.path.join(output_dir, self.script_filename)
        output_basename = os.path.join(output_dir, 'output')
        logging.info("Create script file: {0}".format(script_file))
        cmd_samtools = "{0} mpileup -f {1} {2} {3}".format(samtools_exe, ref, file1, file2)
        cmd_VarScan = "{0} -Xmx25g -jar {1} somatic {2} --mpileup 1".format(java_exe, exe, output_basename)
        for key in self.params.keys():
            if self.params[key] is None:
                raise ValueError("VarScan does not support flags without value: {0}".format(key))
            cmd_VarScan += " {0} {1}".format(key, self.params[key])
            self.write_prolog_script(script_file, output_dir)
        cmd = "{0} | {1}\n".format(cmd_samtools, cmd_VarScan)
        with open(script_file, 'a') as stream:
            stream.write(cmd)
        self.make_script_executable(script_file)
        return None

    def write_CaVEMan_scripts(self, out, exe, ref, file1, file2):
        """
        Write a script to run the configuration using the VarScan program.
        :param out: Folder to store outputs of the program.
        :param exe: Path to executable of the program.
        :param ref: Reference genome Fasta file.
        :param file1: Input file for reference group (e.g. normal).
        :param file2: Input file for target group (e.g. tumour).
        :return: None
        """
        output_dir = os.path.join(out, self.out)
        setup_script_file = os.path.join(output_dir, '01_setup_script.sh')
        split_script_file = os.path.join(output_dir, '02_split_script.sh')
        merge_split_script_file = os.path.join(output_dir, '03_merge_split_script.sh')
        Mstep_script_file = os.path.join(output_dir, '04_Mstep_script.sh')
        merge_script_file = os.path.join(output_dir, '05_merge_script.sh')
        Estep_script_file = os.path.join(output_dir, '06_Estep_script.sh')
        config_file = os.path.join(output_dir, 'caveman.cfg.ini')
        qsub_dir = os.path.join(output_dir, 'qsub')
        ref_fai = "{0}.fai".format(ref)
        with open(ref_fai) as stream:
            fai_entries = len(stream.readlines())
            logging.info("# fai_entries: {0}".format(fai_entries))
        self.write_setup_script(setup_script_file, exe, ref, file1, file2, config_file)
        return None

    def write_setup_script(self, script, exe, ref, file1, file2, config_file):
        """

        :param script:
        :param exe:
        :param ref:
        :param file1:
        :param file2:
        :param config_file:
        :return:
        """
        cmd_setup = "{0} setup -t {1} -n {2} -r {3} -f {4}".format(exe, file2, file1, ref, config_file)
        # Fail-safe: 'setup:-g' should have been added automatically if not specified in the config file
        # See BenchmarkConfiguration.select_program_config(...)
        if not 'setup:-g' in self.params.keys():
            raise ValueError('"setup:-g" not found in parameters. Please contact maintainer.')
        for key in self.params.keys():
            if key.startswith('setup:'):
                cmd_setup += " {0}".format(key.replace('setup:', ''))
                if not self.params[key] is None:
                    cmd_setup += " {0}".format(self.params[key])
        cmd_setup += "\n"
        with open(script, 'a') as stream:
            stream.write(cmd_setup)
        return None

    def write_CaVEMan_split_script(self, script, exe, config_file, qsub_dir):
        """

        :param script:
        :param exe:
        :param config_file:
        :param qsub_dir:
        :return:
        """
        stdout_file = os.path.join(qsub_dir, 'stdout.split.${SGE_TASK_ID}.log')
        stderr_file = os.path.join(qsub_dir, 'stderr.split.${SGE_TASK_ID}.log')
        cmd_split = "{0} split -i $SGE_TASK_ID -f {1}".format(exe, config_file)
        for key in self.params.keys():
            if key.startswith('split:'):
                cmd_split += " {0}".format(key.replace('split:', ''))
                if self.params[key] is None:
                    raise ValueError("CaVEMan split step does not support flags without value: {0}".format(key))
                cmd_split += " {0}".format(self.params[key])
        cmd_split += " 1>{0} 2>{1}\n".format(stdout_file, stderr_file)
        with open(script, 'w') as stream:
            stream.write("#!/bin/bash\n")
            stream.write(cmd_split)
        return None

    @staticmethod
    def write_prolog_script(script, out):
        """
        Write common prolog of benchmark scripts.
        :param script: Filename of the script file to write.
        :param out: Folder to store outputs of the configuration.
        :return: None
        """
        with open(script, 'w') as stream:
            stream.write("#!/bin/bash\n")
            stream.write("cd {0}\n".format(out))
        return None

    @staticmethod
    def make_script_executable(script):
        """
        Make script executable.
        :return:
        """
        subprocess.call(["chmod", "+x", script])
        return None

    def submit_script(self, out):
        """
        :param out: Folder to store outputs of the program.
        :return: None
        """
        output_dir = os.path.join(out, self.out)
        script = os.path.join(output_dir, self.script_filename)
        stdout_file = os.path.join(output_dir, self.job_stdout)
        stderr_file = os.path.join(output_dir, self.job_stderr)
        job_name = "{0}_{1}".format(os.path.basename(out), self.index)
        qsub_cmd_args = [
            'qsub',
            '-o', stdout_file,
            '-e', stderr_file,
            '-pe', 'shmem', str(self.n_cores),
            '-N', job_name,
            '-q', 'short.qc',
            script
        ]
        qsub_cmd_str = ' '.join(qsub_cmd_args)
        logging.info("Submit command: {0}".format(qsub_cmd_str))
        subprocess.call(qsub_cmd_args)
        return None

    def submit_CaVEMan_scripts(self, out):
        """
        :param out: Folder to store outputs of the program.
        :return: None
        """
        output_dir = os.path.join(out, self.out)
        setup_script_file = os.path.join(output_dir, '01_setup_script.sh')
        split_script_file = os.path.join(output_dir, '02_split_script.sh')
        merge_split_script_file = os.path.join(output_dir, '03_merge_split_script.sh')
        Mstep_script_file = os.path.join(output_dir, '04_Mstep_script.sh')
        merge_script_file = os.path.join(output_dir, '05_merge_script.sh')
        Estep_script_file = os.path.join(output_dir, '06_Estep_script.sh')
        qsub_dir = os.path.join(output_dir, 'qsub')
        pattern_job_id = re.compile('.* (\d+)\..*')
        setup_stdout, err = subprocess.Popen(
            [
                'qsub', '-o', os.path.join(qsub_dir, 'setup.out'),
                '-e', os.path.join(qsub_dir, 'setup.err'),
                '-N', "setup_{0}".format(self.index),
                '-q', 'short.qc',
                setup_script_file
            ],
            stdout=subprocess.PIPE).communicate()
        setup_job_id = pattern_job_id.match(setup_stdout.decode("utf-8")).group(1)
        logging.info("setup_{0} JOB_ID: {1}".format(self.index, setup_job_id))
        return None

# def parse_job_id():
#     cmd = 'sed \'s/.* \([0-9]\+\)\..*/\\1/\''
#     return