#!/usr/bin/bash

cd resources/gtk/
glib-compile-resources daty.gresource.xml
cd ../../
python __init__.py
