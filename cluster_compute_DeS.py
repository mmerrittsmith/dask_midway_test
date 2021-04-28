from dask_jobqueue import SLURMCluster
from dask.distributed import Client
import subprocess


def main():
	filenames = grab_DeS_GADM_codes()
	cluster = SLURMCluster(cores=24,
					   memory='40GB',
					   walltime='08:00:00',
					   log_directory='/home/merrittsmithdask_log',
					   local_directory='/home/merrittsmith/dask_out',
					   job_extra=['--partition=broadwl'])

	cluster.adapt(maximum_jobs=20)
	client = Client(cluster)
	client.map(filenames, run_block_summary)


def grab_DeS_GADM_codes():
	with open('grab_DeS_GADM_codes.txt', 'r+') as read_file:
		DeS_codes = read_file.read()
	DeS_codes = DeS_codes.split(', ')
	filenames = [filename_helper(code) for code in DeS_codes]
	return filenames


def filename_helper(code):
	block_path = '/project2/bettencourt/mnp/prclz/data/blocks/Africa/TZA/blocks_'+code+'.csv'
	summary_path = '/home/merrittsmith/block_summaries/TZA/'+code+'.geojson'
	return {'block path': block_path, 'summary_path': summary_path}


def run_block_summary(code_set):
	# long-term I think it makes sense to integrate this dask stuff with block_summary 
	# but for now we'll access it via the CLI
	subprocess.run(['python', '/home/merrittsmith/mnp-analysis/utils/block_summary.py',
	                '--aoi_path', code_set['block path'],
	                '--landscan_path', '/project2/bettencourt/mnp/prclz/data/LandScan_Global_2018/raw_tif/ls_2018.tif',
	                '--buildings_dir', '/project2/bettencourt/mnp/prclz/data/buildings/Africa/TZA',
	                '--blocks_dir', '/project2/bettencourt/mnp/prclz/data/blocks/Africa/TZA',
	                '--gadm_dir', '/project2/bettencourt/mnp/prclz/data/GADM/TZA',
	                '--summary_out_path', code_set['summary_path']],
	                check=True,
	                cwd='/home/merrittsmith')

if __name__ == '__main__':
	main()