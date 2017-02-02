import os

home_dir = '/gpfs2/well/ratcliff'
appsdir = '/apps/well'
qsub_exe = '/gpfs0/mgmt/sge/6.2u5/bin/lx26-amd64/qsub'

base_dir = os.path.join(home_dir, 'pipeline')

# pipeline_dir = os.path.join(base_dir, 'src')
tools_dir = os.path.join(base_dir, 'tools')
ref_beds_dir = os.path.join(base_dir, 'ref_beds')

GATK_dir = os.path.join(tools_dir, 'GATK')
Strelka_dir = os.path.join(tools_dir, 'strelka')
Virmid_dir = os.path.join(tools_dir, 'Virmid')
EBCall_dir = os.path.join(tools_dir, 'EBCall')
VarScan_dir = os.path.join(tools_dir, 'VarScan')
CaVEMan_dir = os.path.join(tools_dir, 'CaVEMan')

java_exe = os.path.join(appsdir, 'java', 'jdk1.8.0_latest', 'bin', 'java')
samtools_dir = os.path.join(appsdir, 'samtools', '1.3', 'bin')
R_dir = os.path.join(appsdir, 'R', '3.3.0', 'bin')

samtools_exe = os.path.join(samtools_dir, 'samtools')
