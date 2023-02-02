import getpass
import argparse
import check_data_repository as CDR

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
        
        # As of 020223, return dummy dataframe object of requested data. Ensure check once paths established
        import get_dummy_data as GDD
        tmp = GDD.ieeg()
        return tmp
    else:

        if not args.password:
            args.password = getpass.getpass()
        
        # As of 020223, return dummy dataframe object of requested data. Ensure check once paths established
        import get_dummy_data as GDD
        tmp = GDD.ieeg()
        return tmp


if __name__ == '__main__':
    
    DF = main()