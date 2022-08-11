#!/bin/bash
cd $1
exec youtube-dl -f 140 $2
exec youtube-dl --skip-download --print-json -f 140 $2 >> audio/log.json