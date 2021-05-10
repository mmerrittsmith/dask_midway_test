#!/bin/bash
#SBATCH--job-name=parallel_block_summary_test_82
#SBATCH--output=DeS_parallel_summary.out
#SBATCH--error=DeS_parallel_block_summary.err
#SBATCH--time=8:00:00
#SBATCH--partition=broadwl
#SBATCH--nodes=1
#SBATCH--ntasks-per-node=1
#SBATCH--mem-per-cpu=40000
#SBATCH--mail-type=END
#SBATCH--mail-user=merrittsmith@uchicago.edu
python /home/merrittsmith/mnp-analysis/analytics2/utils/block_summary.py --aoi_path /project2/bettencourt/mnp/prclz/data/blocks/Africa/TZA/blocks_TZA.2.3.23_1.csv --landscan_path /project2/bettencourt/mnp/prclz/data/LandScan_Global_2018/raw_tif/ls_2018.tif --buildings_dir /project2/bettencourt/mnp/prclz/data/buildings/Africa/TZA --blocks_dir /project2/bettencourt/mnp/prclz/data/blocks/Africa/TZA --gadm_dir /project2/bettencourt/mnp/prclz/data/GADM/TZA --summary_out_path /home/merrittsmith/block_summaries/TZA/TZA.2.3.23_1.geojson