#in an experiments folder,
rm sim_analysis/metrics_complete_ranked*
echo AVGSTRETCH >sim_analysis/metrics_complete_ranked_avgstretch
echo RMSS       >sim_analysis/metrics_complete_ranked_RMSS
echo RMSBSLD    >sim_analysis/metrics_complete_ranked_RMSBSLD
../../../simulation_analysis/metrics_ranking_avgstretch.R sim_analysis/metrics_complete -o sim_analysis/metrics_complete_ranked_avgstretch
../../../simulation_analysis/metrics_ranking_rmss.R sim_analysis/metrics_complete -o sim_analysis/metrics_complete_ranked_RMSS
../../../simulation_analysis/metrics_ranking_rmsbsld.R sim_analysis/metrics_complete -o sim_analysis/metrics_complete_ranked_RMSBSLD
column -s' ' -t < sim_analysis/metrics_complete_ranked_avgstretch | less -#2 -N -S
column -s' ' -t < sim_analysis/metrics_complete_ranked_RMSS       | less -#2 -N -S
column -s' ' -t < sim_analysis/metrics_complete_ranked_RMSBSLD    | less -#2 -N -S
