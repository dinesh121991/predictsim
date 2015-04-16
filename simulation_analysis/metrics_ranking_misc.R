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

#########
#ranking
df<-read.table(args$swf_filename)
df=df[which(!is.na(df$avgbsld)),]
#summary(df)
ranked=df[with(df, order(avgbsld)), ]
ranked$rank=c(1:nrow(ranked))


pretty <- function (rmsbslds,ranks) {
  r=rep(1,length(rmsbslds))
  for (i in 1:length(rmsbslds)) {
    r[i]=paste(format(rmsbslds[i],nsmall=1,digits=0),'/',ranks[i],sep="")
  }
  return(r)
}

########
#Global ranks of the Clairvoyant(x2), EASY FCFS and EASY++ algorithms
T1=ranked[which(
                (ranked$scheduler=="easy_prediction_backfill_scheduler" &
                 ranked$predictor=="predictor_reqtime")|
                (ranked$scheduler=="easy_plus_plus_scheduler" &
                 ranked$predictor=="predictor_reqtime")|
                (ranked$scheduler=="easy_plus_plus_scheduler" &
                 ranked$predictor=="predictor_tsafrir" &
                 ranked$corrector=="tsafrir") |
                (ranked$predictor=="predictor_clairvoyant")
                ),
(colnames(ranked) %in% c("rank","scheduler","corrector","predictor","RMSS","RMSBSLD","avgbsld"))]
T1$PRETTY=pretty(T1$avgbsld,T1$rank)
write.table(T1,paste(args$output,'/','table_intro',sep=''),row.names=FALSE)

#########
#Algo-wise ranks of the clairvoyant schedulers
filtered=ranked[which(ranked$scheduler=="easy_plus_plus_scheduler"),]
filtered$algo_rank=c(1:nrow(filtered))
T2=filtered[which(filtered$predictor=="predictor_clairvoyant")
            ,(colnames(filtered) %in% c("rank","algo_rank","scheduler","RMSS","RMSBSLD","avgbsld"))]
T2$PRETTY=pretty(T2$avgbsld,T2$rank)
write.table(T2,paste(args$output,'/','clairvoyant_rank_sjbf',sep=''),row.names=FALSE)

filtered=ranked[which(ranked$scheduler=="easy_prediction_backfill_scheduler"),]
filtered$algo_rank=c(1:nrow(filtered))
T3=filtered[which(filtered$predictor=="predictor_clairvoyant")
            ,(colnames(filtered) %in% c("rank","algo_rank","scheduler","RMSS","RMSBSLD","avgbsld"))]
T3$PRETTY=pretty(T3$avgbsld,T3$rank)
write.table(T3,paste(args$output,'/','clairvoyant_rank_fcfs',sep=''),row.names=FALSE)

#########
#Global and Algo-wise maximal and minimal ranks of the predictive schedulers
filtered=ranked[which(ranked$scheduler=="easy_plus_plus_scheduler"),]
filtered$algo_rank=c(1:nrow(filtered))
filtered2=filtered[which(filtered$predictor=="predictor_sgdlinear"),]
T4=filtered2[c(1,nrow(filtered2))
            ,(colnames(filtered) %in% c("algo_rank","rank","scheduler","predictor","RMSS","RMSBSLD","avgbsld"))]

T4$PRETTY=pretty(T4$avgbsld,T4$rank)
write.table(T4,paste(args$output,'/','learning_ranks_sjbf',sep=''),row.names=FALSE)

filtered=ranked[which(ranked$scheduler=="easy_prediction_backfill_scheduler"),]
filtered$algo_rank=c(1:nrow(filtered))
filtered2=filtered[which(filtered$predictor=="predictor_sgdlinear"),]
T5=filtered2[c(1,nrow(filtered2))
            ,(colnames(filtered) %in% c("algo_rank","rank","scheduler","predictor","RMSS","RMSBSLD","avgbsld"))]
T5$PRETTY=pretty(T5$avgbsld,T5$rank)
write.table(T5,paste(args$output,'/','learning_ranks_fcfs',sep=''),row.names=FALSE)


###################END BLOCK#####################


#############X11 OUTPUT MANAGEMENT###############
#################MODIFY IF NEEDED################
#pause_output(options_vector)
###################END BLOCK#####################


