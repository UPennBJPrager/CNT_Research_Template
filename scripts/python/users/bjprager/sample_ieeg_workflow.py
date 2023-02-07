import sys
import glob
import argparse

for dirs in glob.glob("../../pipeline/**"):
    if dirs not in sys.path:
        sys.path.append(dirs)
        
# User library import
import pipeline_datapull_ieeg as PDI
import dataframe_properties_check as DPC

def main():
    """
    Calls series of commands for a simple ieeg pipeline.

    Returns
    -------
    None.

    """
    
    # Command line options needed to obtain data.
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', required=True, help='username')
    parser.add_argument('-p', '--password', help='password (will be prompted if omitted)')
    parser.add_argument('--dataset', help='dataset name')
    parser.add_argument('--start', type=int, help='start offset in usec')
    parser.add_argument('--duration', type=int, help='number of usec to request')
    parser.add_argument('--local_path', default=None, type=str, help='Path to local data to ingest manually. Default=None.')
    parser.add_argument('--silent', dest='verbose', default=True, action='store_false', help='Silent Verbose Output. Default=False.')
    args = parser.parse_args()
    
    # Data ingestion
    DF,fs = PDI.main(args)
    
    # Data quality check
    quality_flag = DPC.main(DF,16,verbose=args.verbose)
    
    return DF,fs

if __name__ == '__main__':
    DF,fs = main()