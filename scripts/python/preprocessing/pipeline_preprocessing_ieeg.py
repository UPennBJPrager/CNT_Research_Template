# Add submodule repository tools to the current opath
import sys
sys.path.append('../../../CNT_research_tools/python/tools')

# User requested tools for feature selection
import clean_labels as CL

def main(ieeg_obj,preprocesses=None):
    """
    Create a dictionary with feature selection for ieeg data. 

    Parameters
    ----------
    iieeg_obj : array or dataframe structure
        Placeholder until example workflow is available.
    preprocesses : list, optional
        Preprocessing steps. Currently available:
            CL = Clean labels
        The default is None. If None, all preprocessing steps. Case Sensitive.
        Steps performed in order of provided list.
    channels : list, optional
        Channels to analyze.
        The default is None. If None, all channels.

    Returns
    -------
    Dictionary with requested features.

    """
    
    # Setup variables to go through functions in order
    if channels == None:
        preprocessing_steps = ['CL']
    else:
        preprocessing_steps = preprocesses
    
    # Loop over preprocessing steps
    for ival in preprocesses:
        if ival == 'CL':
            ieeg_obj = ieeg_obj.copy()
    return ieeg_obj

if __name__ == '__main__':
    
    main()