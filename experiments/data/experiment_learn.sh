#!/bin/bash

FOLDERS="CTC-SP2 KTH-SP2 SDSC-SP2"

for f in $FOLDERS;
do
  cd $f
  make metrics_learn
  echo "$f" >> ../analysis/learned_best_rmsbsld
  cat sim_analysis/learned_best_rmsbsld >> ../analysis/learned_best_rmsbsld
  cd ..
done


