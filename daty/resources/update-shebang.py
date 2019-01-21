# -*- coding: utf-8 -*-

#    update-shebang
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


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
