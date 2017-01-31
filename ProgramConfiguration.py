from SingleConfiguration import *
from LocalSettings import *


class PairedProgramConfiguration:
    """
    Parent class to store benchmark configurations for one program.
    """

    def __init__(self, params, out):
        """
        Initialise a Configuration object.
        :param params: Parameters to supply to the program.
        :param out: Program to use in this configuration.
        """
        self.configurations = []
        self.out = out
        self.add_configuration(params)

    def add_configuration(self, params):
        """
        Add a configuration.
        :param params: Dictionary of parameter flags and values.
        :return: None
        """
        config_index = len(self.configurations)+1
        self.configurations.append(SinglePairedConfiguration(params, config_index))

    def make_dir_structure(self, out):
        """
        Create the folder to store outputs of all configurations for this program.
        :param out: Root folder to store outputs of the benchmark.
        :return: None
        """
        self.make_output_dir(out)
        program_folder = os.path.join(out, self.out)
        self.make_config_dirs(program_folder)
        return None

    def make_output_dir(self, out):
        """
        :param out: Root folder to store outputs of the benchmark.
        :return:
        """
        program_folder = os.path.join(out, self.out)
        logging.info("Create program output folder: {0}".format(program_folder))
        os.mkdir(program_folder)
        return None

    def make_config_dirs(self, out):
        """
        Create a folder for each configuration under the folder for the corresponding program.
        :param out: Root folder to store outputs of the program.
        :return: None
        """
        for config in self.configurations:
            config.make_dir_structure(out)
        return None

    def submit_scripts(self, out):
        """
        Run all benchmark scripts.
        :param out: Root folder to store outputs of the benchmark.
        :return: None
        """
        program_folder = os.path.join(out, self.out)
        for config in self.configurations:
            config.submit_script(program_folder)
        return None


class Mutect2PairedConfiguration(PairedProgramConfiguration):
    """
    Configuration for the Mutect2 program.
    """
    def __init__(self, params, out):
        super().__init__(params, out)
        self.path2exe = os.path.join(GATK_dir, 'GenomeAnalysisTK.jar')

    def write_scripts(self, out, ref, file1, file2):
        """
        Write a script for each configuration.
        :param out: Root folder to store outputs of the program.
        :param ref: Path to reference genome Fasta file.
        :param file1: Input file for reference group (e.g. normal).
        :param file2: Input file for target group (e.g. tumour).
        :return: None
        """
        for config in self.configurations:
            program_folder = os.path.join(out, self.out)
            config.write_mutect2_script(program_folder, self.path2exe, ref, file1, file2)
        return None


class StrelkaPairedConfiguration(PairedProgramConfiguration):
    """
    Configuration for the Strelka program.
    Warning: may be renamed to StrelkaBwaPairedConfiguration if elaand and/or isaac are used in the future.
    """
    def __init__(self, params, out):
        super().__init__(params, out)
        self.path2exe = os.path.join(Strelka_dir, 'strelka_workflow-1.0.14', 'bin', 'configureStrelkaWorkflow.pl')
        self.template_config = os.path.join(
            Strelka_dir, 'strelka_workflow-1.0.14', 'etc', 'strelka_config_bwa_default.ini'
        )

    def write_scripts(self, out, ref, file1, file2):
        """
        Write a script for each configuration.
        :param out: Root folder to store outputs of the program.
        :param ref: Reference genome Fasta file.
        :param file1: Input file for reference group (e.g. normal).
        :param file2: Input file for target group (e.g. tumour).
        :return: None
        """
        for config in self.configurations:
            program_folder = os.path.join(out, self.out)
            config.write_strelka_script(program_folder, self.path2exe, ref, file1, file2, self.template_config)
        return None


class VirmidPairedConfiguration(PairedProgramConfiguration):
    """
    Configuration for the Virmid program.
    """
    def __init__(self, params, out):
        super().__init__(params, out)
        self.path2exe = os.path.join(Virmid_dir, 'virmid.jar')

    def write_scripts(self, out, ref, file1, file2):
        """
        Write a script for each configuration.
        :param out: Root folder to store outputs of the program.
        :param ref: Reference genome Fasta file.
        :param file1: Input file for reference group (e.g. normal).
        :param file2: Input file for target group (e.g. tumour).
        :return: None
        """
        for config in self.configurations:
            program_folder = os.path.join(out, self.out)
            config.write_virmid_script(program_folder, self.path2exe, ref, file1, file2)
        return None


class EBCallPairedConfiguration(PairedProgramConfiguration):
    """
    Configuration for the EBcall program.
    """
    def __init__(self, params, out):
        super().__init__(params, out)
        self.path2exe = os.path.join(EBCall_dir, 'ebCall_v2.sh')
        self.template_config = os.path.join(EBCall_dir, 'config.sh')
        self.normal_list = os.path.join(EBCall_dir, 'testdata', 'list_normal_sample.txt')

    def write_scripts(self, out, ref, file1, file2):
        """
        Write a script for each configuration.
        :param out: Root folder to store outputs of the program.
        :param ref: Reference genome Fasta file.
        :param file1: Input file for reference group (e.g. normal).
        :param file2: Input file for target group (e.g. tumour).
        :return: None
        """
        for config in self.configurations:
            program_folder = os.path.join(out, self.out)
            config.write_EBcall_script(
                program_folder, self.path2exe, ref, file1, file2, self.template_config, self.normal_list
            )
        return None