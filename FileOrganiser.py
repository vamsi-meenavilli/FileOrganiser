import argparse
import os
import shutil


def GroupByExtensions(files):
    grouped_by_extensions = dict()

    for file in files:
        extension = file.split('.')[-1]

        if extension in grouped_by_extensions:
            grouped_by_extensions[extension].append(file)
        else:
            grouped_by_extensions[extension] = [file]

    return grouped_by_extensions


def CreateDirs(root, unique_extensions):
    os.chdir(root)

    for extension in unique_extensions:
        if os.path.isdir(os.path.join(root, extension)):
            print("Directory already exists for .{}'s".format(extension))
        else:
            os.mkdir(extension)
            print("Created directory for .{}'s".format(extension))

    return


def MoveFiles(root, grouped_by_extensions):
    os.chdir(root)

    for extension in grouped_by_extensions:
        for file in grouped_by_extensions[extension]:
            source = os.path.join(root, file)
            destination = os.path.join(root, extension, file)
            shutil.move(source, destination)
        print("Grouped all .{}'s".format(extension))


def GroupFiles(root, files):
    grouped_by_extensions = GroupByExtensions(files)
    unique_extensions = list(set(grouped_by_extensions.keys()))
    CreateDirs(root, unique_extensions)
    MoveFiles(root, grouped_by_extensions)

    return


class Organiser():
    def __init__(self):
        self.include_hidden_files = None
        self.arg_parser = None
        self.recursive = None
        self.path = None
        self.files = dict()
        self.InitializeArgParser()
        self.GetOptions()
        self.GetFiles()
        self.OrganiseFiles()

        return

    def InitializeArgParser(self):
        self.arg_parser = argparse.ArgumentParser(description = 'This program groups the files by extension.')
        self.arg_parser.add_argument(
            '-p',
            '--path',
            dest = 'path',
            help = 'Path of the directory to be Grouped.',
            required = True
        )
        self.arg_parser.add_argument(
            '-r',
            '--recursive',
            dest = 'recursive',
            help = "Groups inside nested files, by default its set to False.",
            required = False,
            default = False
        )
        self.arg_parser.add_argument(
            '--hidden',
            dest = 'hidden',
            help = "Includes hidden files, by default it's set to False.",
            required = False,
            default = False
        )

        return

    def GetOptions(self):
        self.path = self.arg_parser.parse_args().path
        self.recursive = self.arg_parser.parse_args().recursive
        self.include_hidden_files = self.arg_parser.parse_args().hidden

        return

    def GetFiles(self):
        self.files = dict()

        if self.recursive:
            for root, dirs, files in os.walk(self.path):
                self.files[root] = files
        else:
            self.files[self.path] = list()

            for file in os.listdir(self.path):
                if (
                    os.path.isfile(os.path.join(self.path, file))
                    and (
                        self.include_hidden_files
                        or not file.startswith('.')
                    )
                ):
                    self.files[self.path].append(file)

        return

    def OrganiseFiles(self):
        for root in self.files:
            GroupFiles(root = root, files = self.files.get(root))

        return


if __name__ == '__main__':
    Organiser()
