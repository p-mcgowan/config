#!/bin/bash

touch ~/tmp/i-was-here
/usr/bin/gnome-terminal --working-directory="$*" /bin/bash -il
