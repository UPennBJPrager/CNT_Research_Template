# Add submodule repository tools to the current opath
import sys
sys.path.append('../../../CNT_research_tools/python/tools')

import getpass
import argparse
import check_data_repository as CDR
from get_iEEG_data import get_iEEG_data

def main():
    """
    Checks if data requested already exists in cache.
    If not, download requested data.
    If cached, return cached data.

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
    args = parser.parse_args()

    # Figure out expected filename based on parameters
    ifile = 'foo.bar'

    # Check if data exists
    if CDR.check_ieeg_data(ifile):
        endtime = args.start+args.duration
        DF,fs   = get_iEEG_data(args.user, args.password, args.dataset, args.start, args.duration)
        return DF,fs
    else:

        if not args.password:
            args.password = getpass.getpass()
        
        endtime = args.start+args.duration 
        DF,fs   = get_iEEG_data(args.user, args.password, args.dataset, args.start, endtime)
        return DF,fs

if __name__ == '__main__':
    
    DF,fs = main()