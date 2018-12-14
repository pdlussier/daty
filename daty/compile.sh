#!/usr/bin/bash

cd data/gtk/
glib-compile-resources daty.gresource.xml
cd ../../
python __init__.py
