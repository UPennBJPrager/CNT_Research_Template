# Add submodule repository tools to the current opath
import sys
sys.path.append('../../../CNT_research_tools/python/tools')

# User requested tools for preprocessing

def main(ieeg_obj,samp_freq):
    """
    Create a dictionary with feature selection for ieeg data. 

    Parameters
    ----------
    iieeg_obj : array or dataframe structure
        Placeholder until example workflow is available.
    features : list, optional
        Feature selection. Currently available:
            LL = Line Length,
            BP = Band Power
        The default is None. If None, all features. Case Sensitive.
    channels : list, optional
        Channels to analyze.
        The default is None. If None, all channels.

    Returns
    -------
    Dictionary with requested features.

    """

    return none

if __name__ == '__main__':
    
    main()