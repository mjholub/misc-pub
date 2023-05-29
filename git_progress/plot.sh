#!/bin/bash

echo "Date,Additions,Deletions" >stats.csv
git log --pretty=format:"%ad" --date=short --numstat | awk 'NF==3 {plus+=$1; minus+=$2} NF==1 {print $1 "," plus "," -minus; plus=minus=0}' >>stats.csv
