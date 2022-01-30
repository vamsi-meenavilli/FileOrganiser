import argparse
import os
import shutil

class Organiser():
    def __init__(self):
        self.InitializeArgParser()
        self.GetPath()
        self.GetFileStructure()
        self.OrganiseFiles()

        return

    def InitializeArgParser(self):
        self.arg_parser = argparse.ArgumentParser(description = 'This program groups the files by extension.')
        self.arg_parser.add_argument(
            '--p',
            '--path',
            dest = 'path',
            help = 'Path of the directory to be Grouped.',
            required = True
        )

        return

    def GetPath(self):
        self.path = self.arg_parser.parse_args().path

        return

    def GetFileStructure(self):
        self.files = dict()

        for root, dirs, files in os.walk(self.path):
            self.files[root] = files

        return

    def OrganiseFiles(self):
        for root in self.files:
            self.GroupFiles(root = root, files = self.files.get(root).get('files'))

        return

    def GroupFiles(self, root, files):
        grouped_by_extensions = self.GroupByExtensions(files)
        unique_extensions = grouped_by_extensions.keys()
        self.CreateDirs(root, unique_extensions)
        self.MoveFiles(root, grouped_by_extensions)

        return

    def GroupByExtensions(self, files):
        grouped_by_extensions = dict()

        for file in files:
            extension = file.split('.')[-1]

            if extension in dict:
                grouped_by_extensions[extension] = [file]
            else:
                grouped_by_extensions[extension].append(file)

        return grouped_by_extensions

    def CreateDirs(self, root, unique_extensions):
        os.chdir(root)

        for extension in unique_extensions:
            os.mkdir(extension)

        return

    def MoveFiles(self, root, grouped_by_extensions):
        os.chdir(root)

        for extension in grouped_by_extensions:
            for file in grouped_by_extensions[extension]:
                source = os.path.relpath(os.path.join(file))
                destination = os.path.realpath(os.path.join(extension + '/' + file))
                shutil.move(source, destination)


if __name__ == '__main__':
    Organiser()
