#!/usr/bin/Rscript


################WORKING DIRECTORY MAGIC##########
##################DO NOT ALTER###################
initial.options <- commandArgs(trailingOnly = FALSE)
file.arg.name <- "--file="
script.name <- sub(file.arg.name, "", initial.options[grep(file.arg.name, initial.options)])
script.basename <- dirname(script.name)
execution_wd=getwd()
setwd(script.basename)
base_script_wd=getwd()
###################END BLOCK#####################

##############COMMON REQUIREMENTS################
##################DO NOT ALTER###################
#Parser file with all the parser types.
source('Rscript/parser.R')
###################END BLOCK#####################


##############SCRIPT PARAMETERS##################
#############MODIFY AS REQUIRED##################

#Path file for setting up the location of your R files.
#you can alternatively set rfold='/path/to/your/files', but its less modular.
source('Rscript/path.R')

#description and epilog for the console help output.
#e.g. description="This scripts does this and that."
#e.g. epilog="use with caution. refer to www.site.com .."
description='This tool will plot system utilization for the whole log file.'
epilog='You can input multiple swf files, they will be cat.'


#External parser function: for usual options.
#e.g. parser=parser_swf(description,epilog)
parser=parser_swf_minimal(description,epilog)


#additional argparse entries for this particular script.
#e.g. parser$add_argument('-s','--sum', dest='accumulate', action='store_const', const=sum, default=max,help='sum the integers (default: find the max)')

#files you want to source from the rfold folder for this Rscript
#e.g. c('common.R','histogram.R')
userfiles=c('common.R')
###################END BLOCK#####################


###SOURCING, CONTEXT CLEANING, ARG RETRIEVE######
##################DO NOT ALTER###################
#code insertion.
rm(list=setdiff(ls(),c("parser","rfold","userfiles","execution_wd","base_script_wd")))
args=parser$parse_args()
#Verbosity management.
source('Rscript/verbosity.R')
verb<-verbosity_function_maker(args$verbosity)
verb(args,"Parameters to the script")

setwd(rfold)
rfold_wd=getwd()
for (filename in userfiles) {
  source(filename)
}


setwd(base_script_wd)
rm(parser,rfold,userfiles)
###################END BLOCK#####################


#####################OUTPUT_MANAGEMENT###########
################MODIFY IF NEEDED####################
###################END BLOCK#####################


#############BEGIN YOUR RSCRIPT HERE.############
#here is your working directory :)
setwd(execution_wd)
#You have access to:
#set_output(device='pdf',filename='tmp.pdf',ratio=1)
#use it if you really want to change the output type on your way.
#pause_output(pause=TRUE) for x11
#use it to pause for output.
#args for retrieving your arguments.


#type stuff here.

if(length(args$swf_filenames) != 1) {
	print("only 1 file a t time is supported")
	exit(1)
}

if(args$output == "") {
	print("outptut directory should be precise")
	quit("no")
}


doit <- function(data, swf_filename, output_file)
{
	name       =c()
	len        =c()
	avgft      =c()
	maxft      =c()
	RMSFT      =c()
	avgstretch =c()
	maxstretch =c()
	RMSS       =c()
	avgbsld    =c()
	maxbsld    =c()
	RMSBSLD    =c()

	data$ft=data$wait_time+data$run_time
	data$stretch=data$ft/data$run_time
	data$bsld=pmax(1,data$ft/pmax(10,data$run_time))
	n=nrow(data)

	name=append(name,swf_filename)
	len=append(len,nrow(data))
	avgft=append(avgft, sum(as.numeric(data$ft))/nrow(data))
	maxft=append(maxft, max(data$ft))
	RMSFT=append(RMSFT, sqrt(sum(as.numeric(data$ft)*as.numeric(data$ft))/n))
	avgstretch=append(avgstretch, sum(data$stretch)/nrow(data))
	maxstretch=append(maxstretch, max(data$stretch))
	RMSS=append(RMSS, sqrt(sum(as.numeric(data$stretch)*as.numeric(data$stretch))/n))
	avgbsld=append(avgbsld, sum(data$bsld)/nrow(data))
	maxbsld=append(maxbsld, max(data$bsld))
	RMSBSLD=append(RMSBSLD, sqrt(sum(as.numeric(data$bsld)*as.numeric(data$bsld))/n))


	df=data.frame(name=name,
		length=len,
		avgft=avgft,
		maxft=maxft,
		RMSFT=RMSFT,
		avgstretch=avgstretch,
		maxstretch=maxstretch,
		RMSS=RMSS,
		avgbsld=avgbsld,
		maxbsld=maxbsld,
		RMSBSLD=RMSBSLD)
	df=df[with(df,order(avgstretch,RMSBSLD)),]
	write.table(df,output_file, sep="   ",row.names=FALSE)
}

i = 1
swf_filename=args$swf_filenames[i]

csvfile = substr(basename(swf_filename), 0, nchar(basename(swf_filename))-7 )

dire = args$output

dataOrig= tryCatch({
    swf_read(swf_filename)
  }, error= function(e) {
    data.frame(job_id=c(NA), submit_time=c(NA), wait_time=c(NA), run_time=c(NA), proc_alloc=c(NA), cpu_time_used=c(NA), mem_used=c(NA), proc_req=c(NA), time_req=c(NA), mem_req=c(NA), status=c(NA), user_id=c(NA), group_id=c(NA), exec_id=c(NA), queue_id=c(NA), partition_id=c(NA), previous_job_id=c(NA), think_time=c(NA))
    print(paste(swf_filename, "NOT FOUND"))
    quit("no")
  })

  nbefore = nrow(dataOrig)
  dataOrig = dataOrig[which(!is.na(dataOrig$wait_time)),]
  dataOrig = dataOrig[which(!is.na(dataOrig$run_time)),]
  if( nbefore != nrow(dataOrig))
	print(paste("There were", nbefore-nrow(dataOrig), "jobs with NA"))

mintime = min(dataOrig$submit_time)
maxtime = max(dataOrig$submit_time + dataOrig$wait_time + dataOrig$run_time)
midtime = (maxtime-mintime)/2.0 + mintime


data = dataOrig[which(dataOrig$submit_time > midtime),]

doit(data, swf_filename, paste(dire,"/sim_analysis_after50/individual/",csvfile,".csv",sep=""))

data = dataOrig[which(dataOrig$submit_time <= midtime),]

doit(data, swf_filename, paste(dire,"/sim_analysis_before50/individual/",csvfile,".csv",sep=""))












###################END BLOCK#####################

#############X11 OUTPUT MANAGEMENT###############
#################MODIFY IF NEEDED################
#pause_output(options_vector)
###################END BLOCK#####################


