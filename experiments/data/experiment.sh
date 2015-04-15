#!/bin/bash

#for f in  CTC-SP2 KTH-SP2 SDSC-SP2 SDSC-BLUE ;
for f in  CTC-SP2 KTH-SP2 SDSC-SP2 ;
do
  cd $f
  make metrics_misc
  echo "$f" >> ../analysis/best_test_performances
  echo "$f" >> ../analysis/bestperformances
  cat sim_analysis/misc >> ../analysis/bestperformances
  cat sim_analysis_after50/misc >> ../analysis/best_test_performances
  cd ..
done
