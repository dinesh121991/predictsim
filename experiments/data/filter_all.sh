#!/bin/bash

FOLDERS="CTC-SP2 KTH-SP2 SDSC-SP2"
#FOLDERS="CTC-SP2 KTH-SP2 SDSC-SP2 SDSC-BLUE"

for f in $FOLDERS;
do
  cd $f
  rm sim_analysis/metrics_filtered
  make metrics_filter
  cd ..
done


