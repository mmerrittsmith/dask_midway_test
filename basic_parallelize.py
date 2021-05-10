# basic_parallelize.py
import subprocess

def main():
	filenames = grab_DeS_GADM_codes()
	sbatch_scripts = [gen_sbatch_script(code_set, file_num) for file_num, code_set in enumerate(filenames)]
	for script_num, sbatch_script in enumerate(sbatch_scripts):
		with open('sbatch_holder/'+str(script_num)+'.sbatch', 'w+') as f:
			f.write(sbatch_script)
		subprocess.run(['sbatch', 'sbatch_holder/'+str(script_num)+'.sbatch'])

def grab_DeS_GADM_codes():
    with open('DeS_GADM_codes.txt', 'r+') as read_file:
        DeS_codes = read_file.read()
    DeS_codes = DeS_codes.split(', ')
    filenames = [filename_helper(code) for code in DeS_codes]
    return filenames


def filename_helper(code):
    block_path = '/project2/bettencourt/mnp/prclz/data/blocks/Africa/TZA/blocks_'+code+'.csv'
    summary_path = '/home/merrittsmith/block_summaries/TZA/'+code+'.geojson'
    return {'block path': block_path, 'summary_path': summary_path}


def gen_sbatch_script(code_set, job_num):
    # long-term I think it makes sense to integrate this dask stuff with block_summary 
    # but for now we'll access it via the CLI
    last_line = ' '.join(['python', '/home/merrittsmith/mnp-analysis/analytics2/utils/block_summary.py',
                    '--aoi_path', code_set['block path'],
                    '--landscan_path', '/project2/bettencourt/mnp/prclz/data/LandScan_Global_2018/raw_tif/ls_2018.tif',
                    '--buildings_dir', '/project2/bettencourt/mnp/prclz/data/buildings/Africa/TZA',
                    '--blocks_dir', '/project2/bettencourt/mnp/prclz/data/blocks/Africa/TZA',
                    '--gadm_dir', '/project2/bettencourt/mnp/prclz/data/GADM/TZA',
                    '--summary_out_path', code_set['summary_path']])
    sbatch_options =  ['--job-name=parallel_block_summary_test_'+str(job_num), '--output=DeS_parallel_summary.out', '--error=DeS_parallel_block_summary.err',
                      '--time=8:00:00', '--partition=broadwl', '--nodes=1', '--ntasks-per-node=1', '--mem-per-cpu=40000', 
                      '--mail-type=END', '--mail-user=merrittsmith@uchicago.edu']
    sbatch_options = '\n'.join(['#SBATCH' + option for option in sbatch_options])
    sbatch_script = '\n'.join(['#!/bin/bash', sbatch_options, last_line])

    return sbatch_script






if __name__ == '__main__':
	main()
