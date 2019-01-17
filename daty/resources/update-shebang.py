from os.path import join
from re import sub
from sys import argv

installdir = argv[1]

script = join(installdir, "bin", "daty-script.pyw")

pattern = "C:/msys64/mingw64/bin/python3w.exe"

python = join(installdir, "bin", "python3w.exe")

with open(script, 'w') as f:
    content = f.read()
    content = sub(pattern, python, content)
    f.write(content)
    f.close()
