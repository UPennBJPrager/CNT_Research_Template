import os
import sys

def main(path,recursive=True):
    """
    Import a path to sys.path. Will search recursively by default.
    This allows users to use most of this repository without needing to 
    install various packages to their environment path.

    Parameters
    ----------
    path : str
        Relative or absolute path to the parent directory to import.
    recursive : bool, optional
        Import recursively down from path. The default is True.

    Returns
    -------
    None.

    """
    
    for idir in os.walk(path):
        if '__pycache' not in idir[0]:
            if idir[0] not in sys.path:
                sys.path.append(idir[0])
                
    if __name__ == '__main__':
        main(argv[1])