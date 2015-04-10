#in an experiments folder,
rm sim_analysis/misc
../../../simulation_analysis/metrics_ranking_misc.R sim_analysis/metrics_complete -o sim_analysis/clairvoyant_ranks
echo "Clairvoyant ranks" >> sim_analysis/misc
cat sim_analysis/clairvoyant_ranks|column -s' ' -t  >> sim_analysis/misc
cat sim_analysis/misc | less -#2 -N -S
