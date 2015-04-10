#in an experiments folder,
mkdir sim_analysis/plots/
rm sim_analysis/plots/*.pdf
../../../simulation_analysis/metrics_ranking_draw_bestcurve.R sim_analysis/metrics_complete -o sim_analysis/metrics_complete_ranked_RMSBSLD -o sim_analysis/plots -r 2
