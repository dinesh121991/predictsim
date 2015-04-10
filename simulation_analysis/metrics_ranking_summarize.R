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
description='This script will give a summary of the data from the swf file.'
epilog='You can input as many swf files as you wish.'


#External parser function: for usual options.
#e.g. parser=parser_swf(description,epilog)
parser=parser_cli_swf(description,epilog)


#additional argparse entries for this particular script.
#e.g. parser$add_argument('-s','--sum', dest='accumulate', action='store_const', const=sum, default=max,help='sum the integers (default: find the max)')

#files you want to source from the rfold folder for this Rscript
#e.g. c('common.R','histogram.R')
userfiles=c('statistics.R','common.R')

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
#source('Rscript/output_management.R')
#options_vector=set_output(args$device,args$output,args$ratio,execution_wd)
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

df<-read.table(args$swf_filename)
summary(df)
ranked=df[with(df, order(RMSS)), ]
#ncut=which(ranked$predictor=="predictor_reqtime" )[1]
#df<-head(ranked,n=ncut+1)

#ranked=df[with(df, order(RMSBSLD)), ]
#ncut=which(ranked$predictor=="predictor_reqtime")[1]
#df<-head(ranked,n=ncut+1)

#ranked=df[with(df, order(maxbsld)), ]
#ncut=which(ranked$predictor=="predictor_reqtime")[1]
#df<-head(ranked,n=ncut+1)

#ranked=df[with(df, order(avgbsld)), ]
#ncut=which(ranked$predictor=="predictor_reqtime")[1]
#df<-head(ranked,n=ncut+1)

#ranked=df[with(df, order(maxstretch)), ]
#ncut=which(ranked$predictor=="predictor_reqtime")[1]
#df<-head(ranked,n=ncut+1)

#ranked=df[with(df, order(avgstretch)), ]
#ncut=which(ranked$predictor=="predictor_reqtime")[1]
#df<-head(ranked,n=ncut+1)


#param_vectors=df[, (colnames(df) %in% c("pleftparam","prightparam","pthreshold","pweight","pleftside","prightside","predictor","corrector","scheduler"))]

printable=ranked[, (colnames(ranked) %in% c("scheduler","predictor","corrector","pweight","pleftside","prightside","RMSS","RMSBSLD","pthreshold"))]
#printable=printable[with(printable, order(RMSBSLD)), ]
#summary(param_vectors)
#write.table(param_vectors,file="ranked_cut_metrics.csv")
write.table(printable,args$output,row.names=FALSE)
#param_vectors


###################END BLOCK#####################


#############X11 OUTPUT MANAGEMENT###############
#################MODIFY IF NEEDED################
#pause_output(options_vector)
###################END BLOCK#####################


