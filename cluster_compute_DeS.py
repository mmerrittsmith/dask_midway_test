from dask_jobqueue import SLURMCluster
from dask.distributed import Client, performance_report, LocalCluster
import subprocess
import logging
import bokeh


def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    filenames = grab_DeS_GADM_codes()
    c = LocalCluster()
    client = Client(c)
    # c.start_diagnostics_server()
    client.submit(run_block_summary, filenames)

    cluster = SLURMCluster(cores=24,
                           memory='40GB',
                           walltime='08:00:00',
                           log_directory='/home/merrittsmith/dask_log',
                           local_directory='/home/merrittsmith/dask_out',
                           job_extra=['--partition=broadwl', '--account=pi-bettencourt'])

    cluster.scale(8)
    client = Client(cluster)
    filenames = filenames[:2]
    with performance_report(filename='DeS_dask_report.html'):
       client.map(run_block_summary, filenames)
    print(cluster.job_script())

def grab_DeS_GADM_codes():
    with open('DeS_GADM_codes.txt', 'r+') as read_file:
        DeS_codes = read_file.read()
    DeS_codes = DeS_codes.split(', ')
    filenames = [filename_helper(code) for code in DeS_codes]
    return filenames


def filename_helper(code):
    block_path = '/project2/bettencourt/mnp/prclz/data/blocks/Africa/TZA/blocks_'+code+'.csv'
    summary_path = '/home/merrittsmith/block_summaries/TZA/'+code+'.geojson'
    return [block_path, summary_path]


def run_block_summary(code_set):
    # long-term I think it makes sense to integrate this dask stuff with block_summary 
    # but for now we'll access it via the CLI
    print(type(code_set))
    subprocess.run(['python', '/home/merrittsmith/mnp-analysis/analytics2/utils/block_summary.py',
                    '--aoi_path', code_set[0][0],
                    '--landscan_path', '/project2/bettencourt/mnp/prclz/data/LandScan_Global_2018/raw_tif/ls_2018.tif',
                    '--buildings_dir', '/project2/bettencourt/mnp/prclz/data/buildings/Africa/TZA',
                    '--blocks_dir', '/project2/bettencourt/mnp/prclz/data/blocks/Africa/TZA',
                    '--gadm_dir', '/project2/bettencourt/mnp/prclz/data/GADM/TZA',
                    '--summary_out_path', code_set[0][1]],
                    check=True,
                    cwd='/home/merrittsmith')

if __name__ == '__main__':
    main()
