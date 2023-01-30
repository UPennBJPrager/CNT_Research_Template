import numpy as np

def sample_array(m=8,n=4):
    """
    Create a dummy array to pass as pulled data.

    Parameters
    ----------
    m : TYPE, optional
        Number of rows. The default is 8.
    n : TYPE, optional
        Number of columns. The default is 4.

    Returns
    -------
    Dummy array.

    """
    return np.arange(m*n).reshape((m,n))