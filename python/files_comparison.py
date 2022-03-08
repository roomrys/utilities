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


class Directory():

    import os
    from color_print import ColorPrint

    color_printer = ColorPrint()

    def __init__(self, root=os.getcwd()) -> None:
        self.root = root
        self.color_printer.yellow(f'root = {self.root}')
        self.filesList = []
        self.foundFiles = False

    def find_all_files(self):
        self.color_printer.yellow(f'\nRunning {self.find_all_files.__name__}:')
        for path, subdirs, files in self.os.walk(self.root):
            # self.color_printer.cyan(self.os.path.relpath(path))
            # self.color_printer.green(subdirs)
            # self.color_printer.magenta(files)
            for name in files:
                self.filesList.append(self.os.path.join(self.os.path.relpath(path), name))
                # self.color_printer.blue(self.os.path.join(path, name))
        self.foundFiles = True

    def compare_Directory(self, another_Directory=None, another_Directory_path=None):
        if another_Directory_path is not None:
            another_Directory = Directory(another_Directory_path)
        
        try:
            if not isinstance(another_Directory, Directory):
                raise VariableIsNotInstance
            elif not (another_Directory.foundFiles and self.foundFiles):
                raise FilesNotYetRetrieved
        except VariableIsNotInstance:
            self.color_printer.red(f'{self.compare_Directory.__name__}: VariableIsNotInstance, stopping execution, returning None\n')
            return None
        except FilesNotYetRetrieved:
            self.color_printer.red(f'{self.compare_Directory.__name__}: FilesNotYetRetrieved, retrieving files, then continuing execution.\n')
            if not another_Directory.foundFiles:
                another_Directory.find_all_files()
            if not self.foundFiles:
                self.find_all_files()
        
        shortList, longList = (self.filesList, another_Directory.filesList) if (len(self.filesList) < len(another_Directory.filesList)) else (another_Directory.filesList, self.filesList)

        try:
            if not shortList:
                raise DirectoryIsEmpty
        except DirectoryIsEmpty:
            self.color_printer.red(f'{self.compare_Directory.__name__}: DirectoryIsEmpty, returning longer list without comparison.\n')
            return longList

        differingFilesList = []
        for fileL in longList:
            if fileL not in shortList:
                differingFilesList.append(self.os.path.abspath(fileL))
        
        for fileS in shortList:
            if fileS not in longList:
                differingFilesList.append(self.os.path.abspath(fileS))

        return differingFilesList

if __name__ == "__main__":
    path_to_compare_1 = 'C:\\Users\\liezl\\Documents\\Projects\\sleap'
    path_to_compare_2 = "C:\\Users\\liezl\\Documents\\sleap\\pr\\supervised_id\\sleap"

    dir_to_compare_1 = Directory(root=path_to_compare_1)

    differingFilesList = dir_to_compare_1.compare_Directory(another_Directory_path=path_to_compare_2)
    dir_to_compare_1.color_printer.yellow(f'differingFilesList =\n{differingFilesList}')


