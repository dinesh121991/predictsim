#___________SIMULATION_ANALYSIS__:
#simulation_analysis: simu_stretch simu_metrics
FILES=Metacentrum2013/sim_analysis/metrics_filtered CEA-curie/sim_analysis/metrics_filtered KTH-SP2/sim_analysis/metrics_filtered  CTC-SP2/sim_analysis/metrics_filtered SDSC-SP2/sim_analysis/metrics_filtered SDSC-BLUE/sim_analysis/metrics_filtered
FILES2=Metacentrum2013/sim_analysis/metrics_filtered CEA-curie/sim_analysis/metrics_filtered SDSC-BLUE/sim_analysis/metrics_filtered CTC-SP2/sim_analysis/metrics_filtered SDSC-SP2/sim_analysis/metrics_filtered KTH-SP2/sim_analysis/metrics_filtered
FILES3=Metacentrum2013/sim_analysis/metrics_filtered CEA-curie/sim_analysis/metrics_filtered KTH-SP2/sim_analysis/metrics_filtered SDSC-BLUE/sim_analysis/metrics_filtered SDSC-SP2/sim_analysis/metrics_filtered CTC-SP2/sim_analysis/metrics_filtered
FILES4=Metacentrum2013/sim_analysis/metrics_filtered CEA-curie/sim_analysis/metrics_filtered KTH-SP2/sim_analysis/metrics_filtered CTC-SP2/sim_analysis/metrics_filtered SDSC-BLUE/sim_analysis/metrics_filtered SDSC-SP2/sim_analysis/metrics_complete
FILES5=Metacentrum2013/sim_analysis/metrics_filtered KTH-SP2/sim_analysis/metrics_filtered CTC-SP2/sim_analysis/metrics_filtered SDSC-BLUE/sim_analysis/metrics_filtered SDSC-SP2/sim_analysis/metrics_complete CEA-curie/sim_analysis/metrics_filtered
FILES6=KTH-SP2/sim_analysis/metrics_filtered CTC-SP2/sim_analysis/metrics_filtered SDSC-BLUE/sim_analysis/metrics_filtered SDSC-SP2/sim_analysis/metrics_complete CEA-curie/sim_analysis/metrics_filtered Metacentrum2013/sim_analysis/metrics_filtered

compare_traces: filter
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	SDSC-BLUE/sim_analysis/metrics_filtered         KTH-SP2/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b1.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	SDSC-BLUE/sim_analysis/metrics_filtered         CTC-SP2/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b2.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	SDSC-BLUE/sim_analysis/metrics_filtered         Metacentrum2013/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b3.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	SDSC-BLUE/sim_analysis/metrics_filtered         CEA-curie/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b4.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	SDSC-BLUE/sim_analysis/metrics_filtered         SDSC-SP2/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b5.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	KTH-SP2/sim_analysis/metrics_filtered           CTC-SP2/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b6.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	KTH-SP2/sim_analysis/metrics_filtered           Metacentrum2013/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b7.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	KTH-SP2/sim_analysis/metrics_filtered           CEA-curie/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b8.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	KTH-SP2/sim_analysis/metrics_filtered           SDSC-SP2/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b9.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	CTC-SP2/sim_analysis/metrics_filtered           Metacentrum2013/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b10.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	CTC-SP2/sim_analysis/metrics_filtered           CEA-curie/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b11.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	CTC-SP2/sim_analysis/metrics_filtered           SDSC-SP2/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b12.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	Metacentrum2013/sim_analysis/metrics_filtered   CEA-curie/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b13.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	Metacentrum2013/sim_analysis/metrics_filtered   SDSC-SP2/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b14.pdf -r 1
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	CEA-curie/sim_analysis/metrics_filtered         SDSC-SP2/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b15.pdf -r 1

scatterplot:
	../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	KTH-SP2/sim_analysis/metrics_filtered           SDSC-SP2/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b9.pdf -r 1
	#../../simulation_analysis/metrics_compare_rankings_scheduler_predictor.R 	Metacentrum2013/sim_analysis/metrics_filtered   CEA-curie/sim_analysis/metrics_filtered  -o analysis/scatter_rankings_scheduler_predictor_a1_b13.pdf -r 1




	#ranger analysis

#mkdir cross_validation_sdscblue
#mkdir cross_validation_kthsp2
#mkdir cross_validation_ctcsp2
#mkdir cross_validation_sdscsp2

cross_validate: filter
	../../simulation_analysis/metrics_selection_cross_validation.R $(FILES) -o cross_validation_sdscblue
	../../simulation_analysis/metrics_selection_cross_validation.R $(FILES2) -o cross_validation_kthsp2
	../../simulation_analysis/metrics_selection_cross_validation.R $(FILES3) -o cross_validation_ctcsp2
	../../simulation_analysis/metrics_selection_cross_validation.R $(FILES4) -o cross_validation_sdscsp2
	../../simulation_analysis/metrics_selection_cross_validation.R $(FILES5) -o cross_validation_ceacurie
	../../simulation_analysis/metrics_selection_cross_validation.R $(FILES6) -o cross_validation_meta
	echo  "cross validating for SDSC BLUE"
	cat cross_validation_sdscblue/ranked_list|column -s' ' -t > cross_validation_sdscblue/rlist
	cat cross_validation_sdscblue/validation|column -s' ' -t > cross_validation_sdscblue/sel
	rm cross_validation_sdscblue/ranked_list
	rm cross_validation_sdscblue/validation
	echo  "cross validating for KTHSP2"
	cat cross_validation_kthsp2/ranked_list|column -s' ' -t > cross_validation_kthsp2/rlist
	cat cross_validation_kthsp2/validation|column -s' ' -t > cross_validation_kthsp2/sel
	rm cross_validation_kthsp2/ranked_list
	rm cross_validation_kthsp2/validation
	echo  "cross validating for CTCSP2"
	cat cross_validation_ctcsp2/ranked_list|column -s' ' -t > cross_validation_ctcsp2/rlist
	cat cross_validation_ctcsp2/validation|column -s' ' -t > cross_validation_ctcsp2/sel
	rm cross_validation_ctcsp2/ranked_list
	rm cross_validation_ctcsp2/validation
	echo  "cross validating for SDSCSP2"
	cat cross_validation_sdscsp2/ranked_list|column -s' ' -t > cross_validation_sdscsp2/rlist
	cat cross_validation_sdscsp2/validation|column -s' ' -t > cross_validation_sdscsp2/sel
	rm cross_validation_sdscsp2/ranked_list
	rm cross_validation_sdscsp2/validation
	echo  "cross validating for CEACURIE"
	cat cross_validation_ceacurie/ranked_list|column -s' ' -t > cross_validation_ceacurie/rlist
	cat cross_validation_ceacurie/validation|column -s' ' -t > cross_validation_ceacurie/sel
	rm cross_validation_ceacurie/ranked_list
	rm cross_validation_ceacurie/validation
	echo  "cross validating for METACENTRUM"
	cat cross_validation_meta/ranked_list|column -s' ' -t > cross_validation_meta/rlist
	cat cross_validation_meta/validation|column -s' ' -t > cross_validation_meta/sel
	rm cross_validation_meta/ranked_list
	rm cross_validation_meta/validation
	./cross_validate_join.sh

learn: filter
	./experiment_learn.sh

evaluate: filter
	./experiment.sh

filter:
	./filter_all.sh

#_____________CLEANING___________:
clean:
	rm -rf analysis/*
	./cleaneasy.sh

#clean:
	#rm -rf $(DRY_PREDICTION_FOLDER)/* $(ANALYSIS_FOLDER)/* $(SWF_FOLDER)/* $(MEASUREMENTS_FOLDER)/* $(COEFFS_FOLDER)/* $(SIM_FOLDER)/* $(PRED_CPROFILE_FOLDER)/* $(SIM_CPROFILE_FOLDER)/* $(SIM_ANALYSIS_FOLDER)/*

