
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
        self.write_prolog_script(script_file)
        cmd += "\n"
        with open(script_file, 'a') as stream:
            # stream.write("cd {0}\n".format(output_dir))
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
        self.write_prolog_script(script_file)
        with open(script_file, 'a') as stream:
            # stream.write("cd {0}\n".format(config_dir))
            stream.write("cp {0} {1}\n".format(template, config_file))
            for key in self.params.keys():
                if self.params[key] is None:
                    raise ValueError("Strelka does not support flags without value: {0}".format(key))
                stream.write("sed -i 's/^{0} = .*$/{0} = {1} # edited/' {2}\n".format(key, self.params[key], config_file))
            stream.write(cmd)
            stream.write("cd {0}\n".format(output_fulldir))
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
        cmd += "\n"
        self.write_prolog_script(script_file)
        with open(script_file, 'a') as stream:
            # stream.write("cd {0}\n".format(output_dir))
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
        self.write_prolog_script(script_file)
        with open(script_file, 'a') as stream:
            # stream.write("cd {0}\n".format(output_dir))
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
            self.write_prolog_script(script_file)
        cmd = "{0} | {1}\n".format(cmd_samtools, cmd_VarScan)
        with open(script_file, 'a') as stream:
            # stream.write("cd {0}\n".format(output_dir))
            stream.write(cmd)
        self.make_script_executable(script_file)
        return None

    def write_CaVEMan_scripts(
            self, out, exe, ref, file1, file2, qsub_base, config_file_base, setup_base, split_base, merge_splits_base):
        """
        Write a script to run the configuration using the VarScan program.
        """
        output_dir = os.path.join(out, self.out)
        setup_script_file = os.path.join(output_dir, setup_base)
        split_script_file = os.path.join(output_dir, split_base)
        merge_splits_script_file = os.path.join(output_dir, merge_splits_base)
        qsub_dir = os.path.join(output_dir, qsub_base)
        config_file = os.path.join(output_dir, config_file_base)
        logging.info("Create qsub output folder: {0}".format(qsub_dir))
        os.mkdir(qsub_dir)
        self.write_prolog_script(setup_script_file)
        self.write_setup_script(setup_script_file, exe, ref, file1, file2, config_file, output_dir)
        self.write_prolog_script(split_script_file)
        self.write_CaVEMan_split_script(split_script_file, exe, config_file, qsub_dir)
        self.write_prolog_script(merge_splits_script_file)
        self.write_CaVEMan_merge_splits_script(merge_splits_script_file, qsub_dir, output_dir)
        return None

    def write_setup_script(self, script, exe, ref, file1, file2, config_file, out):
        """
        Write a script to run the setup step of CaVEMan.
        :param script:
        :param exe:
        :param ref:
        :param file1:
        :param file2:
        :param config_file:
        :param out: Folder for outputs of configuration.
        :return:
        """
        output_folder = os.path.join(out, 'results')
        split_file = os.path.join(out, 'splitList')
        alg_bean_file = os.path.join(out, 'alg_bean')
        cmd_setup = "{0} setup -t {1} -n {2} -r {3} -c {4} -f {5} -l {6} -a {7}".format(
            exe, file2, file1, "{0}.fai".format(ref), config_file, output_folder, split_file, alg_bean_file
        )
        # Fail-safe: 'setup:-g' should have been added automatically if not specified in the config file
        # See BenchmarkConfiguration.select_program_config(...)
        if 'setup:-g' not in self.params.keys():
            raise ValueError('"setup:-g" not found in parameters. Please contact maintainer.')
        for key in self.params.keys():
            if key.startswith('setup:'):
                cmd_setup += " {0}".format(key.replace('setup:', ''))
                if not self.params[key] is None:
                    cmd_setup += " {0}".format(self.params[key])
        cmd_setup += "\n"
        with open(script, 'a') as stream:
            # CaVEMan wants all steps to be run in the same working directory as the Setup step
            # qsub jobs are launched from the $HOME directory
            stream.write("cd $HOME\n")
            stream.write(cmd_setup)
            stream.write("cd -\n")
        self.make_script_executable(script)
        return None

    def write_CaVEMan_split_script(self, script, exe, config_file, qsub_dir):
        """

        :param script:
        :param exe:
        :param config_file:
        :param qsub_dir:
        :return:
        """
        stdout_file = os.path.join(qsub_dir, 'out.split.${SGE_TASK_ID}')
        stderr_file = os.path.join(qsub_dir, 'err.split.${SGE_TASK_ID}')
        cmd_split = "{0} split -i $SGE_TASK_ID -f {1}".format(exe, config_file)
        for key in self.params.keys():
            if key.startswith('split:'):
                cmd_split += " {0}".format(key.replace('split:', ''))
                if self.params[key] is None:
                    raise ValueError("CaVEMan split step does not support flags without value: {0}".format(key))
                cmd_split += " {0}".format(self.params[key])
        cmd_split += " 1>{0} 2>{1}\n".format(stdout_file, stderr_file)
        with open(script, 'a') as stream:
            stream.write(cmd_split)
        self.make_script_executable(script)
        return None

    def write_CaVEMan_merge_splits_script(self, script, qsub_dir, out):
        """

        :param script:
        :param qsub_dir:
        :param out: Folder for outputs of configuration.
        :return:
        """
        split_file = os.path.join(out, 'splitList')
        tmp_split_files = "{0}.*".format(split_file)
        stdout_file = os.path.join(qsub_dir, 'out.merge-split.${SGE_TASK_ID}')
        stderr_file = os.path.join(qsub_dir, 'err.merge-split.${SGE_TASK_ID}')
        with open(script, 'a') as stream:
            stream.write("ls -1 {0} | xargs\n".format(tmp_split_files))
            stream.write("cat {0} > {1}\n".format(tmp_split_files, split_file))
            stream.write("rm {0}\n".format(tmp_split_files))
        self.make_script_executable(script)
        return None

    @staticmethod
    def write_prolog_script(script):
        """
        Write common prolog of benchmark scripts.
        :param script: Filename of the script file to write.
        :param out: Folder to store outputs of the configuration.
        :return: None
        """
        with open(script, 'w') as stream:
            stream.write("#!/bin/bash\n")
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

    def submit_CaVEMan_scripts(self, out, ref_fai, qsub_base, setup_base, split_base, merge_splits_base):
        """
        :param out: Folder to store outputs of the program.
        :return: None
        """
        output_dir = os.path.join(out, self.out)
        qsub_dir = os.path.join(output_dir, qsub_base)
        setup_script_file = os.path.join(output_dir, setup_base)
        split_script_file = os.path.join(output_dir, split_base)
        merge_splits_script_file = os.path.join(output_dir, merge_splits_base)
        logging.info("Submit command: {0}".format(setup_script_file))
        if ref_fai is None:
            raise ValueError("ref_fai not set! please contact maintainer.")
        with open(ref_fai) as stream:
            fai_entries = len(stream.readlines())
            logging.info("# fai_entries: {0}".format(fai_entries))
        # Setup
        subprocess.call([setup_script_file])
        pattern_job_id = re.compile('.* (\d+)[ .].*')
        # Split
        split_cmd_args = [
                'qsub',
                '-t', "1-{0}".format(fai_entries),
                '-o', os.path.join(qsub_dir, '02_split.out'),
                '-e', os.path.join(qsub_dir, '02_split.err'),
                '-N', "setup_{0}".format(self.index),
                '-q', 'short.qc',
                split_script_file
            ]
        logging.info("Submit command: {0}".format(' '.join(split_cmd_args)))
        setup_stdout, err = subprocess.Popen(split_cmd_args, stdout=subprocess.PIPE).communicate()
        setup_job_id = pattern_job_id.match(setup_stdout.decode("utf-8")).group(1)
        logging.info("split_{0} JOB_ID: {1}".format(self.index, setup_job_id))
        # Merge splits
        merge_splits_cmd_args = [
                'qsub',
                '-hold_jid_ad', setup_job_id, # hold until setup completed
                '-o', os.path.join(qsub_dir, '03_merge-splits.out'),
                '-e', os.path.join(qsub_dir, '03_merge-splits.err'),
                '-N', "setup_{0}".format(self.index),
                '-q', 'short.qc',
                split_script_file
            ]
        logging.info("Submit command: {0}".format(' '.join(merge_splits_cmd_args)))
        merge_splits_stdout, err = subprocess.Popen(merge_splits_cmd_args, stdout=subprocess.PIPE).communicate()
        setup_job_id = pattern_job_id.match(merge_splits_stdout.decode("utf-8")).group(1)
        logging.info("merge_splits_{0} JOB_ID: {1}".format(self.index, setup_job_id))
        return None

# def parse_job_id():
#     cmd = 'sed \'s/.* \([0-9]\+\)\..*/\\1/\''
#     return