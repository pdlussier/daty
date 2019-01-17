from os.path import join
from re import sub
from sys import argv

installdir = argv[1]

script = installdir + "\\bin\\daty-script.pyw"

pattern = "C:/msys64/mingw64/bin/python3w.exe"

repl = "\"" + installdir + "\\bin\\python3w.exe" + "\""

repl = sub("\\\\", "/", repl)

print(script)
print(pattern)
print(repl)

with open(script, 'r') as f:
    content = f.read()
    f.close()

content = sub(pattern, repl, content)

print(content)
with open(script, 'w') as f:
    f.write(content)
    f.close()
