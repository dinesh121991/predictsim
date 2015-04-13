
import glob
import os.path, time
import os
import subprocess

class Maker:
	
	def __init__(self, verbose=False):
		self.verbose = verbose

	def listToGlob(self, l):
		if type(l) == list:
			return l[0] + '*' + l[1]
		else:# l is a string
			return l


	def ageOf(self, files):
		files = self.listToGlob(files)
		if type(files) == list:
			fs = []
			for fil in files:
				fs += glob.glob(fil)
		else:
			fs = glob.glob(files)
		if len(fs) == 0:
			return 0
		age = 0
		for f in fs:
			age = max(age, os.path.getmtime(f))
		return age


	def isNewer(self, source, dest):
		return self.ageOf(source) > self.ageOf(dest)


	def doTask(self, source, dest, command):
		print "[Maker]: Start of ", command
		list_of_task = []
		
		if type(source) == list:
			if type(dest) == list:
				# N to N
				sources = glob.glob(self.listToGlob(source))
				for s in sources:
					list_of_task.append( (s, dest[0] + s[len(source[0]):-len(source[1])] + dest[1], command) )
				
			else:
				# N to 1
				list_of_task.append( (source, dest, command) )
		else:
			if type(dest) == list:
				# 1 to N
				list_of_task.append( (source, dest, command) )
			else:
				# 1 to 1
				list_of_task.append( (source, dest, command) )
			
		
		#print list_of_task
		t_already_done=0
		t_done=0
	
		for task in list_of_task:
			src = task[0]
			dst = task[1]
			cmd = task[2]
			
			if( self.isNewer(src, dst) ):
				if self.verbose: print("[Maker]: Source ("+str(src)+") is newer than dest ("+str(dst)+").")
				
			
				os.environ["SOURCE"] = self.listToGlob(source)
				#os.environ["SOURCE_GLOB"] = " ".join(glob.glob(self.listToGlob(source)))
				os.environ["DEST"] = self.listToGlob(dest)
				
				os.environ["SOURCE_FILE"] = self.listToGlob(src)
				if type(src) != list:
					os.environ["SOURCE_FILE_SHORT"] = os.path.splitext(os.path.basename(src))[0]
					os.environ["SOURCE_FILE_BASE"] = os.path.basename(src)
				
				os.environ["DEST_FILE"] = self.listToGlob(dst)
				if type(dst) != list:
					os.environ["DEST_FILE_SHORT"] = os.path.splitext(os.path.basename(str(dst)))[0]
					os.environ["DEST_FILE_BASE"] = os.path.basename(str(dst))
				
				if self.verbose: print("[Maker]: Launching: "+str(cmd))
				print subprocess.check_output(cmd, shell=True)
				t_done += 1
			else:
				if self.verbose: print("[Maker]: Nothing to do for "+str(src)+" => "+str(dst)+")")
				t_already_done += 1
		print "[Maker]: \tAlready done:", t_already_done, "\tDone:", t_done




b = Maker(False)


b.doTask(
	source=["./", "/simulations/res_easy_prediction_backfill_scheduler_predictorclairvoyant_throw_an_error.swf.gz"], dest=["preliminary_expe/", ".clairvoyant.csv"],
	command="""../../simulation_analysis/swf2vis_metrics.R $SOURCE_FILE -o $DEST_FILE""")
b.doTask(
	source=["./", "/simulations/res_easy_prediction_backfill_scheduler_predictorreqtime_throw_an_error.swf.gz"], dest=["preliminary_expe/", ".reqtime.csv"],
	command="""../../simulation_analysis/swf2vis_metrics.R $SOURCE_FILE -o $DEST_FILE""")

b.doTask(
	source=["preliminary_expe/", ".csv"], dest="preliminary_expe/AAA_metrics",
	command="../data_manipulation/merge_to_metrics.sh $SOURCE > $DEST_FILE")

b.doTask(
	source="preliminary_expe/AAA_metrics", dest="preliminary_expe/AAA_metrics_complete",
	command="""perl -p -e  's|./(.*)/simulations|\1" |' $SOURCE_FILE | perl -p -e  's|"name"|"trace" "predictor"|' | perl -p -e  's|/res_easy_pred.*predictor(.*)_throw.*gz"|"\1" |' > $DEST_FILE""")





