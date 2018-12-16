#!/usr/bin/bash

mkdir tmp
declare -a arr=(16 32 48 64 128 256)
for i in "${arr[@]}"; do
    convert daty-logo.svgz -scale "$i" tmp/"$i".png
done
convert tmp/16.png tmp/32.png tmp/48.png tmp/64.png tmp/128.png tmp/256.png daty.ico
rm -r tmp
