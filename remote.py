#!/usr/bin/bash

broadwayd :6345 & (sleep 3 && env GDK_BACKEND=broadway BROADWAY_DISPLAY=:6345 GTK_DEBUG=touchscreen daty)
