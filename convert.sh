#!/bin/bash
cd $1
exec youtube-dl --print-json -f 140 $2