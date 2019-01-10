#!/usr/bin/bash

cd daty/resources
glib-compile-resources daty.gresource.xml #--generate-source --generate-header
cd ../../
