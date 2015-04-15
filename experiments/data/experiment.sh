#!/bin/bash

for f in  CTC-SP2 KTH-SP2 SDSC-BLUE SDSC-SP2 ;
do
  cd $f
  make clean
  make filter
  make predict -j 2
  make prediction_analysis
  cd ..
done
