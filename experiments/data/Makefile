#___________SIMULATION_ANALYSIS__:
#simulation_analysis: simu_stretch simu_metrics
FILES=KTH-SP2/sim_analysis/metrics_complete  CTC-SP2/sim_analysis/metrics_complete SDSC-SP2/sim_analysis/metrics_complete SDSC-BLUE/sim_analysis/metrics_complete
FILES2=SDSC-BLUE/sim_analysis/metrics_complete CTC-SP2/sim_analysis/metrics_complete SDSC-SP2/sim_analysis/metrics_complete KTH-SP2/sim_analysis/metrics_complete
FILES3=KTH-SP2/sim_analysis/metrics_complete SDSC-BLUE/sim_analysis/metrics_complete SDSC-SP2/sim_analysis/metrics_complete CTC-SP2/sim_analysis/metrics_complete
FILES4=KTH-SP2/sim_analysis/metrics_complete CTC-SP2/sim_analysis/metrics_complete SDSC-BLUE/sim_analysis/metrics_complete SDSC-SP2/sim_analysis/metrics_complete

compare_traces:
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R  -o analysis/scatter_rankings_scheduler_predictor_KTH-SP2_CTC-SP2.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R SDSC-SP2/sim_analysis/metrics_complete CTC-SP2/sim_analysis/metrics_complete -o analysis/scatter_rankings_scheduler_predictor_SDSC-SP2_CTC-SP2.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R SDSC-BLUE/sim_analysis/metrics_complete CTC-SP2/sim_analysis/metrics_complete -o analysis/scatter_rankings_scheduler_predictor_SDSC-BLUE_CTC-SP2.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R SDSC-SP2/sim_analysis/metrics_complete KTH-SP2/sim_analysis/metrics_complete -o analysis/scatter_rankings_scheduler_predictor_SDSC-SP2_KTH-SP2.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R SDSC-BLUE/sim_analysis/metrics_complete KTH-SP2/sim_analysis/metrics_complete -o analysis/scatter_rankings_scheduler_predictor_SDSC-BLUE_KTH-SP2.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R SDSC-BLUE/sim_analysis/metrics_complete SDSC-SP2/sim_analysis/metrics_complete -o analysis/scatter_rankings_scheduler_predictor_SDSC-BLUE_SDSC-SP2.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_weight.R KTH-SP2/sim_analysis/metrics_complete CTC-SP2/sim_analysis/metrics_complete -o analysis/scatter_rankings_weight_KTH-SP2_CTC-SP2.pdf -r 2
	../../simulation_analysis/metrics_compare_rankings_scheduler_weight.R SDSC-SP2/sim_analysis/metrics_complete CTC-SP2/sim_analysis/metrics_complete -o analysis/scatter_rankings_weight_SDSC-SP2_CTC-SP2.pdf -r 2
	../../simulation_analysis/metrics_compare_rankings_scheduler_weight.R SDSC-BLUE/sim_analysis/metrics_complete CTC-SP2/sim_analysis/metrics_complete -o analysis/scatter_rankings_weight_SDSC-BLUE_CTC-SP2.pdf -r 2
	../../simulation_analysis/metrics_compare_rankings_scheduler_weight.R SDSC-SP2/sim_analysis/metrics_complete KTH-SP2/sim_analysis/metrics_complete -o analysis/scatter_rankings_weight_SDSC-SP2_KTH-SP2.pdf -r 2
	../../simulation_analysis/metrics_compare_rankings_scheduler_weight.R SDSC-BLUE/sim_analysis/metrics_complete KTH-SP2/sim_analysis/metrics_complete -o analysis/scatter_rankings_weight_SDSC-BLUE_KTH-SP2.pdf -r 2
	../../simulation_analysis/metrics_compare_rankings_scheduler_weight.R SDSC-BLUE/sim_analysis/metrics_complete SDSC-SP2/sim_analysis/metrics_complete -o analysis/scatter_rankings_weight_SDSC-BLUE_SDSC-SP2.pdf -r 2
	ranger analysis

cross_validate:
	mkdir analysis/cross_validation_sdscblue
	mkdir analysis/cross_validation_kthsp2
	mkdir analysis/cross_validation_ctcsp2
	mkdir analysis/cross_validation_sdscsp2
	../../simulation_analysis/metrics_selection_cross_validation.R $(FILES) -o analysis/cross_validation_sdscblue
	../../simulation_analysis/metrics_selection_cross_validation.R $(FILES2) -o analysis/cross_validation_kthsp2
	../../simulation_analysis/metrics_selection_cross_validation.R $(FILES3) -o analysis/cross_validation_ctcsp2
	../../simulation_analysis/metrics_selection_cross_validation.R $(FILES4) -o analysis/cross_validation_sdscsp2
	cat analysis/cross_validation_sdscblue/ranked_list|column -s' ' -t > analysis/cross_validation_sdscblue/rlist
	cat analysis/cross_validation_sdscblue/validation|column -s' ' -t > analysis/cross_validation_sdscblue/sel
	rm analysis/cross_validation_sdscblue/ranked_list
	rm analysis/cross_validation_sdscblue/validation
	cat analysis/cross_validation_kthsp2/ranked_list|column -s' ' -t > analysis/cross_validation_kthsp2/rlist
	cat analysis/cross_validation_kthsp2/validation|column -s' ' -t > analysis/cross_validation_kthsp2/sel
	rm analysis/cross_validation_kthsp2/ranked_list
	rm analysis/cross_validation_kthsp2/validation
	cat analysis/cross_validationctcsp2/ranked_list|column -s' ' -t > analysis/cross_validationctcsp2/rlist
	cat analysis/cross_validationctcsp2/validation|column -s' ' -t > analysis/cross_validationctcsp2/sel
	rm analysis/cross_validationctcsp2/ranked_list
	rm analysis/cross_validationctcsp2/validation
	cat analysis/cross_validation_sdscsp2/ranked_list|column -s' ' -t > analysis/cross_validation_sdscsp2/rlist
	cat analysis/cross_validation_sdscsp2/validation|column -s' ' -t > analysis/cross_validation_sdscsp2/sel
	rm analysis/cross_validation_sdscsp2/ranked_list
	rm analysis/cross_validation_sdscsp2/validation
	ranger analysis/

learn:
	./experiment_learn.sh

#_____________CLEANING___________:
clean:
	rm -rf analysis/*

#clean:
	#rm -rf $(DRY_PREDICTION_FOLDER)/* $(ANALYSIS_FOLDER)/* $(SWF_FOLDER)/* $(MEASUREMENTS_FOLDER)/* $(COEFFS_FOLDER)/* $(SIM_FOLDER)/* $(PRED_CPROFILE_FOLDER)/* $(SIM_CPROFILE_FOLDER)/* $(SIM_ANALYSIS_FOLDER)/*

