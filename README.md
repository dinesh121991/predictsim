Improving Backfilling by using Machine Learning to predict Running Times.
=========================================================================

This repository is home to the scheduling simulator, machine learning tools, and experimental results from the SC'15 submission "Improving Backfilling by using Machine Learning to predict Running Times".

Experimental Results
====================
The following files contain metrics for all the so-called heuristic triples, in the CSV format.

experiments/data/CEA-curie/sim_analysis/metrics_complete

experiments/data/KTH-SP2/sim_analysis/metrics_complete

experiments/data/CTC-SP2/sim_analysis/metrics_complete

experiments/data/SDSC-SP2/sim_analysis/metrics_complete

experiments/data/SDSC-BLUE/sim_analysis/metrics_complete

experiments/data/Metacentrum2013/sim_analysis/metrics_complete

Scheduling Simulator
====================
The Scheduling simulator used in this paper is a fork of the pyss open source scheduler. It found in the folder:
simulation/pyss/src

Machine Learning Algorithms
===========================
Implementations of the NAG algorithm for learning the model are located at:
simulation/pyss/src/predictors/

Replicating Experiments
=======================
in each log folder in experiments/data/, the following make targets are available:


Necessary R stuff:
install.packages("argparse","ggplot2","gridExtra")
