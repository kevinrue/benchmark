import os

home_dir = '/gpfs2/well/ratcliff'
appsdir='/apps/well'

base_dir = os.path.join(home_dir, 'pipeline')

# pipeline_dir = os.path.join(base_dir, 'src')
tools_dir = os.path.join(base_dir, 'tools')
ref_beds_dir = os.path.join(base_dir, 'ref_beds')

GATK_dir = os.path.join(tools_dir, 'GATK')
strelka_dir = os.path.join(tools_dir, 'strelka')

java_exe = os.path.join(appsdir, 'java', 'jdk1.8.0_latest', 'bin', 'java')