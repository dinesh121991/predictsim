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
parser=parser_files(description,epilog)

#additional argparse entries for this particular script.
#e.g. parser$add_argument('-s','--sum', dest='accumulate', action='store_const', const=sum, default=max,help='sum the integers (default: find the max)')

#files you want to source from the rfold folder for this Rscript
#e.g. c('common.R','histogram.R')
userfiles=c('draw_losscurve.R')
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
source('Rscript/output_management.R')
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

require("reshape")
n=length(args$filenames)
ndf=read.table(args$filenames[1])
#summary(ndf)
m=min(ndf[which(!ndf$predictor=="predictor_clairvoyant"),]$RMSBSLD,na.rm=TRUE)
ndf$valuation=ndf$RMSBSLD/m
ndf$count= rep(1,nrow(ndf))
ndf=ndf[,c("predictor","scheduler","corrector","pweight","pleftparam","prightparam","pleftside","prightside","pthreshold","valuation","count")]

#print(unique(ndf$pleftparam))
#print(unique(ndf$pleftside))
#print(unique(ndf$prightparam))
#print(unique(ndf$prightside))
#print(unique(ndf$threshold))

for (i in 2:n-1){
  filename=args$filenames[i]
  data=read.table(filename)
  m=min(data[which(!data$predictor=="predictor_clairvoyant"),]$RMSBSLD,na.rm=TRUE)
  data$RMSBSLD=data$RMSBSLD/m
  data$present=rep(1,nrow(data))

  #print(unique(data$pleftparam))
  #print(unique(data$pleftside))
  #print(unique(data$prightparam))
  #print(unique(data$prightside))
  #print(unique(data$threshold))
  #print(nrow(ndf[which(data$prightparam==0.00001),]))

  ndf=merge(ndf,data,by=c("predictor","scheduler","corrector","pweight","pleftparam","prightparam","pleftside","prightside","pthreshold"))


  ndf$valuation=ndf$valuation+ndf$RMSBSLD
  ndf$count=ndf$count+ndf$present

  ndf=ndf[,c("predictor","scheduler","corrector","pweight","pleftparam","prightparam","pleftside","prightside","pthreshold","valuation","count")]
}

ndf$SELECT=ndf$valuation/ndf$count
ndf$valuation=NULL

prop_df=read.table(args$filenames[1])

ndf=merge(ndf,prop_df,by=c("predictor","scheduler","corrector","pweight","pleftparam","prightparam","pleftside","prightside","pthreshold"))
ndf=ndf[which(!ndf$predictor=="predictor_clairvoyant"),]


ndf$name=NULL
ndf$length=NULL
ndf$avgft=NULL
ndf$avgstretch=NULL
ndf$maxstretch=NULL
ndf$RMSS=NULL
ndf$maxft=NULL
ndf$maxbsld=NULL
ndf$simultime=NULL
ndf$hash=NULL
ndf=ndf[with(ndf, order(SELECT)),]
ndf$rank=c(1:nrow(ndf))
#ndf$SELECT=NULL
ndf$RMSFT=NULL
ndf$avgbsld=NULL

write.table(ndf,paste(args$output,"/ranked_list",sep=""),sep="   ",row.names=FALSE)

#print(ndf[1,])
#for (i in 1:10) {

#draw_curve(ndf[1,])
#}

best_curve=ndf[1,]
filename=args$filenames[n]
data=read.table(filename)
selected=merge(data,best_curve,by=c("predictor","scheduler","corrector","pweight","pleftparam","prightparam","pleftside","prightside","pthreshold"))
print(selected[,c("RMSBSLD.x","predictor","scheduler","corrector","pweight","pleftparam","prightparam","pleftside","prightside","pthreshold")])
write.table(selected[,c("RMSBSLD.x","predictor","scheduler","corrector","pweight","pleftparam","prightparam","pleftside","prightside","pthreshold")],paste(args$output,"/validation",sep=""),sep="   ",row.names=TRUE)

for (i in 1:40) {
  draw_curve(ndf[i,],xlim=86600)
  #draw_curve(ndf[i,])
}

###################END BLOCK#####################

#############X11 OUTPUT MANAGEMENT###############
#################MODIFY IF NEEDED################
#pause_output(options_vector)
###################END BLOCK#####################
