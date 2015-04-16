#!/bin/bash

#for f in  CTC-SP2 KTH-SP2 SDSC-SP2 SDSC-BLUE ;
for f in  CTC-SP2 KTH-SP2 SDSC-SP2 CEA-curie SDSC-BLUE Metacentrum2013;
do
  cd $f
  make metrics_misc
  #echo "$f" >> ../analysis/best_test_performances
  echo " " >> ../analysis/bestperformances
  echo " " >> ../analysis/bestperformances
  echo "#$f" >> ../analysis/bestperformances

  #echo " " >> ../analysis/best_test_performances
  #echo " " >> ../analysis/best_test_performances
  #echo "#$f" >> ../analysis/best_test_performances

  cat sim_analysis/misc >> ../analysis/bestperformances
  #cat sim_analysis_after50/misc >> ../analysis/best_test_performances
  cd ..
done
