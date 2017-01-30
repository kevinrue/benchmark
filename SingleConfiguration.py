
import logging
import os
import subprocess

from LocalSettings import ref_beds_dir

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
            for key in self.params.keys():
                stream.write("{0}\t{1}\n".format(key, self.params[key]))
        return None

    def write_mutect2_script(self, out, exe, ref, files1, files2):
        """
        Write a script to run the configuration using the Mutect2 program.
        :param out: Folder to store outputs of the program.
        :param exe: Path to executable of the program.
        :return: None
        """
        output_dir = os.path.join(out, self.out)
        script_file = os.path.join(output_dir, self.script_filename)
        logging.info("Create script file: {0}".format(script_file))
        output_vcf = os.path.join(out, self.out, 'output.vcf')
        dbsnp = "--dbsnp {0}".format(os.path.join(ref_beds_dir, 'known.vcf'))
        cosmic = "--cosmic {0}".format(os.path.join(ref_beds_dir, 'Cosmic.vcf'))
        cmd = "java -Xmx25g -jar {0} -T MuTect2 -R {1} -I:tumour {2} -I:normal {3} {4} {5} -o {6}\n".format(
            exe, ref, files2, files1, dbsnp, cosmic, output_vcf
        )
        for key in self.params.keys():
            cmd += " {0} {1}".format(key, self.params[key])
            self.write_prolog_script(script_file, output_dir)
        with open(script_file, 'a') as stream:
            stream.write(cmd)
        self.make_script_executable(script_file)
        return None

    def write_strelka_script(self, out, exe, ini, ref, files1, files2):
        """
        Write a script to run the configuration using the Mutect2 program.
        :param out: Folder to store outputs of the program.
        :param exe: Path to executable of the program.
        :return: None
        """
        script_file = os.path.join(out, self.out, 'script.sh')
        logging.info("Create script file: {0}".format(script_file))
        output_dir = os.path.join(out, self.out)
        cmd = "{0} --normal {1} --tumor {2} --ref {3} --config {4} --output-dir {5}\n".format(
            exe, files1, files2, ref, ini, output_dir
        )
        for key in self.params.keys():
            cmd += " {0} {1}".format(key, self.params[key])
        self.write_prolog_script(script_file, output_dir)
        with open(script_file, 'a') as stream:
            stream.write("cp {0} config.ini".format(ini))
            stream.write(cmd)
            stream.write("make\n")
        return None

    @staticmethod
    def write_prolog_script(script, out):
        """
        Write common prolog of benchmark scripts.
        :param script: Filename of the script file to write.
        :param out: Folder to store outputs of the configuration benchmark.
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
