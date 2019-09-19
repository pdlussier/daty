#!/usr/bin/env python3

from subprocess import check_output
from subprocess import CalledProcessError, STDOUT
from os import listdir as ls
from os.path import splitext
from shutil import rmtree as rm


b = lambda x: bytes(x, encoding='utf-8')

already_exists_error = "fatal: destination path 'update-dependencies' already exists and is not an empty directory.\n"

is_python_package = lambda x: True if x.endswith('json') and x.startswith('python3') else False

get_package_name = lambda x: splitext(x.split('python3-')[1])[0]

def sh(command, callback=None, exception_handler=None, callback_args=[], exception_handler_args=[], retries=5):
    i = 0
    while i < retries:
        try:
            command = command.split(" ")
            out = check_output(command, stderr=STDOUT)
            if callback:
                callback(*callback_args)
            return True
        except CalledProcessError as e:
            if exception_handler:
                exception_handler(e, *exception_handler_args)
            return True
        i += 1
        print(i)

clone = "git clone https://github.com/flatpak/flatpak-builder-tools update-dependencies"

def clone_exception_handler(exception):
    if exception.output == b(already_exists_error):
        print("repository already exists, pulling changes...")
        pull = "git -C ./update-dependencies pull"
        sh(pull)

sh(clone, clone_exception_handler)

for x in ls():
    if is_python_package(x):
        y = get_package_name(x)
        print("Updating {}".format(y))
        update = "./update-dependencies/pip/flatpak-pip-generator {}".format(y)
        sh(update)

print("Removing temporary directory...")
rm('update-dependencies')
