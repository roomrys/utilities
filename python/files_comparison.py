import os

from numpy import not_equal
# This type of import requires files_comparison.py to be run in same directory as color_print
from color_print import ColorPrint

color_printer = ColorPrint()

class Error(Exception):
    """Base class for other exceptions"""
    pass

class VariableIsNotInstance(Error):
    """Raised when variable is not an instance of the desired class"""
    pass

class FilesNotYetRetrieved(Error):
    """Raised when Directory.filesFound is False"""
    pass

class DirectoryIsEmpty(Error):
    """Raised when Directy.filesList is empty and Directory.filesFound is True"""
    pass

class NoComparateDirectory(Error):
    """Raised when no comparate Directory was given"""
    pass

class Comparate():
    """Comparate Directory to by used in Comparison."""
    def __init__(self, first_directory, second_directory):
        self.Directory = first_directory

class Comparison():

    def __init__(self, first_Directory, second_Directory) -> None:
        try:
            if not (isinstance(first_Directory, Directory()) and isinstance(second_Directory, Directory())):
                raise VariableIsNotInstance
        except VariableIsNotInstance:
            color_printer.red(f'{self.__init__.__name__}: VariableIsNotInstance, stopping execution, returning None\n')
            return None

        self.comparate_Directory_1 = first_Directory
        self.comparate_Directory_2 = second_Directory


class Directory():

    def __init__(self, root=os.getcwd()) -> None:
        """Sets the root of the Directory. Initializes filesList to an empty list and foundFiles to False.

        Args:
            root (str, optional): The absolute path to the directory. Defaults to os.getcwd().
        """
        self.root = root
        color_printer.yellow(f'root = {self.root}')
        self.filesList = []
        self.foundFiles = False
        self.comparate = None
        self.missing_files = []

    def find_all_files(self):
        """Finds all files at Directory.root and any subfolders. 
        Stores files in list Document.filesList and sets Document.foundFiles to True.
        """
        color_printer.yellow(f'\nRunning {self.find_all_files.__name__}:')
        for path, _, files in os.walk(self.root):
            # color_printer.cyan(os.path.relpath(path))
            # color_printer.green(subdirs)
            # color_printer.magenta(files)
            for name in files:
                file_to_append = os.path.join(os.path.relpath(path, self.root), name)
                self.filesList.append(file_to_append)
                # color_printer.blue(os.path.join(path, name))
        self.foundFiles = True

    def compare_Directory(self, another_Directory=None, another_Directory_path=None):
        """Compares Directory(self).filesList to that of Directory(another_Directory).filesList.

        Args:
            another_Directory (Directory, optional): Comparate Directory whose filesList will be compared to self.filesList. Defaults to None.
            another_Directory_path (str, optional): Comparate directory path whose filesList will be compared to self.filesList. Defaults to None.

        Raises:
            VariableIsNotInstance: Raised when variable is not an instance of the desired class
            FilesNotYetRetrieved: Raised when Directory.filesFound is False
            DirectoryIsEmpty: Raised when Directy.filesList is empty and Directory.filesFound is True

        Returns:
            list: List of differing files between Directory(self) and Directory(another_Directory)
        """
        if another_Directory_path is not None:
            another_Directory = Directory(another_Directory_path)
        
        try:
            if (another_Directory is None) and (another_Directory_path is None):
                raise NoComparateDirectory
            if not isinstance(another_Directory, Directory):
                raise VariableIsNotInstance
            elif not (another_Directory.foundFiles and self.foundFiles):
                raise FilesNotYetRetrieved
        except VariableIsNotInstance:
            color_printer.red(f'{self.compare_Directory.__name__}: VariableIsNotInstance, stopping execution, returning None\n')
            return None
        except FilesNotYetRetrieved:
            color_printer.red(f'{self.compare_Directory.__name__}: FilesNotYetRetrieved, retrieving files, then continuing execution.\n')
            if not another_Directory.foundFiles:
                another_Directory.find_all_files()
            if not self.foundFiles:
                self.find_all_files()
        except NoComparateDirectory:
            color_printer.red(f'{self.compare_Directory.__name__}: NoComparateDirectory, stopping execution, returning None\n')
            return None

        self.comparate = another_Directory
        another_Directory.comparate = self

        self.find_missing_files()
        another_Directory.find_missing_files()

        return another_Directory

    def find_missing_files(self):
        """_summary_

        Args:
            files_list (list): List of files from which a missing files list will be populated.
            comparate_list (list): List of files which will be compared against files_list.

        Returns:
            list: List of files contained in files_list that are missing in comparate_list.
        """
        try:
            if self.comparate is None:
                raise NoComparateDirectory
        except NoComparateDirectory:
            color_printer.red(f'{self.compare_Directory.__name__}: NoComparateDirectory, stopping execution, returning None\n')
            return None
            

        self.missing_files = []
        for file in self.filesList:
            if file not in self.comparate.filesList:
                file_to_append = os.path.join(self.root, file)  # VARDEBUG
                self.missing_files.append(os.path.join(self.root, file))

    def write_missing_files_to_file(self):
        try:
            if self.comparate is None:
                raise NoComparateDirectory
        except NoComparateDirectory:
            color_printer.red(f'{self.compare_Directory.__name__}: NoComparateDirectory, stopping execution, returning None\n')
            return None

        path_to_name = self.root.split(':')[-1].replace('\\', '_')[1:]
        ext = '.txt'
        file_name = f'{os.path.basename(__file__).split(".")[0]}-{path_to_name}{ext}'
        base_dir = os.path.commonpath([self.root, self.comparate.root])
        
        file_to_write_to = open(file_name, "w")
        file_to_write_to.write(f'# {path_to_name}\n\n')
        file_to_write_to.write(f'# Base directory: {base_dir}\n')
        file_to_write_to.write(f'# Root directory containing files: {os.path.relpath(self.root, base_dir)}\n')
        file_to_write_to.write(f'# Root directory of comparate: {os.path.relpath(self.comparate.root, base_dir)}\n')
        file_to_write_to.write(f'# This file lists the files contained within the "root directory containing files"\n\
#   which are not contained in the "root directory of the comparate"\n\n')

        i = 0
        prev_head = os.path.dirname(self.missing_files[0])
        # given two file paths, want to compare whether base directory is same or different
        for file in self.missing_files:
            head, tail = os.path.split(file) # directory of file
            if prev_head != head:  # check if in new subfolder
                base_rel_path = os.path.dirname(os.path.relpath(file, self.root)) # path relative to base_path
                file_to_write_to.write(f'\n{base_rel_path}\n')
            file_to_write_to.write(f'{i}: {tail}\n')
            i += 1
            prev_head = head
        
        file_to_write_to.close()

        color_printer.yellow(f'Missing file names written to {file_name}')


def main(path1, path2):
    dir1 = Directory(root=path1)

    dir2 = dir1.compare_Directory(another_Directory_path=path2)

    color_printer.yellow(f'differingFilesList1 =\n{dir1.missing_files}')
    color_printer.cyan(f'differingFilesList2 =\n{dir2.missing_files}')

    dir1.write_missing_files_to_file()
    dir2.write_missing_files_to_file()


if __name__ == "__main__":
    path_to_compare_1 = 'C:\\Users\\liezl\\Documents\\Projects\\sleap'
    path_to_compare_2 = "C:\\Users\\liezl\\Documents\\sleap\\pr\\supervised_id\\sleap"
    main(path_to_compare_1, path_to_compare_2)


