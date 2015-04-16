#in an experiments folder,
rm sim_analysis/misc
rm sim_analysis/table_intro
rm sim_analysis/clairvoyant_rank_sjbf
rm sim_analysis/clairvoyant_rank_fcfs
rm sim_analysis/learning_ranks_sjbf
rm sim_analysis/learning_ranks_fcfs

../../../simulation_analysis/metrics_ranking_misc.R sim_analysis/metrics_filtered -o sim_analysis

echo "#Global ranks of the Clairvoyant(x2), EASY FCFS and EASY++ algorithms">> sim_analysis/misc
cat sim_analysis/table_intro|column -s' ' -t  >> sim_analysis/misc

echo "#Global and Algo-wise ranks of the clairvoyants schedulers">> sim_analysis/misc
cat sim_analysis/clairvoyant_rank_sjbf|column -s' ' -t  >> sim_analysis/misc
cat sim_analysis/clairvoyant_rank_fcfs|column -s' ' -t  >> sim_analysis/misc

echo "#Global and Algo-wise maximal and minimal ranks of the predictive schedulers">> sim_analysis/misc
cat sim_analysis/learning_ranks_sjbf|column -s' ' -t  >> sim_analysis/misc
cat sim_analysis/learning_ranks_fcfs|column -s' ' -t  >> sim_analysis/misc

#cat sim_analysis/misc | less -#2 -N -S
