#in an experiments folder,
rm sim_analysis/misc
rm sim_analysis/clairvoyant_ranks
rm sim_analysis/clairvoyant_rank_among_sjbf
rm sim_analysis/clairvoyant_rank_among_fcbf

../../../simulation_analysis/metrics_ranking_misc.R sim_analysis/metrics_complete -o sim_analysis

echo "Clairvoyant ranks" >> sim_analysis/misc
cat sim_analysis/clairvoyant_ranks|column -s' ' -t  >> sim_analysis/misc

echo "Clairvoyant rank AMONG SJBF" >> sim_analysis/misc
cat sim_analysis/clairvoyant_rank_sjbf|column -s' ' -t  >> sim_analysis/misc

echo "Clairvoyant rank AMONG FCBF" >> sim_analysis/misc
cat sim_analysis/clairvoyant_rank_fcbf|column -s' ' -t  >> sim_analysis/misc

echo "Summary" >> sim_analysis/misc
cat sim_analysis/table_intro|column -s' ' -t  >> sim_analysis/misc

cat sim_analysis/misc | less -#2 -N -S
