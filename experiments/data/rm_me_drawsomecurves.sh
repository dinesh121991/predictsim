#!/bin/bash

#for f in  CTC-SP2 KTH-SP2 SDSC-SP2 SDSC-BLUE ;
for f in  CTC-SP2 KTH-SP2 SDSC-SP2 CEA-curie SDSC-BLUE;
do
  cd $f

  rm analysis/*.pdf

  for h in simulations/*;
  do
    ../../../simulation_analysis/swf2vis_bsldCDF_KDE.R $h -o analysis/`basename $h`.pdf -r 2
  done

  #echo "$f" >> ../analysis/best_test_performances
  #echo "$f" >> ../analysis/bestperformances
  #cat sim_analysis/misc >> ../analysis/bestperformances
  #cat sim_analysis_after50/misc >> ../analysis/best_test_performances
  cd ..
done
