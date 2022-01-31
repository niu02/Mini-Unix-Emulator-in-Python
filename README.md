# Mini-Unix-Emulator-in-Python
A class project to reproduce the Unix filesystem/terminal commands in Python.
The purpose of this project was to test our OOP skills. The brief instructed us to use objects and classes to implement a representation of a simple file system.
Classes we were to implement included 'File', 'PlainFile','Directory' and 'FileSystem'.

Methods included: 
- Printing the entire file system tree
- 'Chown' to modify file or directory owners (set to default if not specified)
- 'ls' to recursively print the content of a directory and all subdirectories (with indentation to represent position of file/directory in the tree structure)
- 'pwd' to return the current working directory
- 'ls' for the FileSsystem class, to only print from the current directory
- 'cd' to move directory
- 'create_file' and 'mkdir' to create files and directories within the working directory and ensure the file name doesn't already exist
- 'rm' to remove files, and directories only if it is empty
- 'find' to search for a file name in a file system and return the path of its first occurence but False if it is not found
- 'wc' with flags '-l' and '-L' to print character length of the longest file name in the current directory and number of files in the current directory, respectively
- 'ls' in FileSystem with flag '-l' to print full file listing with file permissions and owners
- 'chmod' to change file permissions using octal representation
