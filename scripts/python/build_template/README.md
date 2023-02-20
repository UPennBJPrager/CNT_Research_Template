This folder is designed to be a template that will help a user in the creation of their own build file. This allows the user to package their code in a way that allows for simple library imports and sharing with collaborators.

To use:
=======
- Place a folder containing the code you wish to include in the library in your src folder. Sub-folders provide different parts of the namespace.
- Update the pyproject.toml to include your information, including changing the project name to match the folder in src.
- Run python3 -m build in the top directory (containing the src folder, readme, license, etc.)
-- If you encounter an issue, make sure you have build installed 'pip install build'

This will produce a dist folder in the top directory with a .whl and .tar.gz file for your library.
