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
parser=parser_flat(description,epilog)


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
source('Rscript/output_management.R')
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
require("ggplot2")

#print(args)
df<-read.table(args$filenames[1])
#summary(df)
ranked=df[with(df, order(RMSS)), ]

printable=ranked[, (colnames(ranked) %in% c("scheduler","predictor","corrector","pweight","pleftside","prightside","RMSS","RMSBSLD","pthreshold","prightparam","pleftparam"))]

draw_curve<-function(row,rank){

  if (!row$predictor=="predictor_sgdlinear") {
    return()
  }

  filename=paste(args$output,'/',rank,'_',row$scheduler,'.pdf',sep='')
  #options_vector=set_output(args$device,filename,args$ratio,execution_wd)
  set_output(device='pdf',filename=filename,ratio=1,execution_wd)
  #pause_output(options_vector)
  ###################END BLOCK#####################

  L<-function(type,alpha,x){
    if (type=="exp") {
      return(exp(alpha*x)-1)
    }else if (type=="abs"){
      return(alpha*x)
    }else if (type=="square"){
      return(alpha*x^2)
    }
  }

  lossfunc<-function(x){
    y=x
    t=row$pthreshold
    for (i in 1:length(x)) {
      if (x[i]>=t) {
        y[i]=L(row$prightside,row$prightparam,x[i]-t)
      }else{
        y[i]=L(row$pleftside,row$pleftparam,-x[i]+t)
      }
    }
    return(y)
  }

  p=ggplot(data.frame(x=c(-80000, 80000)), aes(x)) +
  stat_function(fun=lossfunc) +
  scale_color_brewer(palette="Set3")+
  xlab("Value of the error for predictor:" )+

  #for (i in 1:length(args$swf_filenames)){
    #p=p+annotate("text", x =14000 , y = 0.6-0.05*i, label = args$swf_filenames[i])
    #p=p+annotate("text", x =50000 , y = 0.6-0.05*i, label = paste("Max: ",sprintf("%e",maxes[i])))
    #p=p+annotate("text", x =70000 , y = 0.6-0.05*i, label = paste(" Mean :",sprintf("%2.0f",means[i])))
    #p=p+annotate("text", x =90000 , y = 0.6-0.05*i, label = paste(" RMSS:",sprintf("%1.1f",squares[i])))
  #}

  print(p)
}

for (i in 1:10) {
  draw_curve(printable[i,],i)
  print(i)
  print(printable[i,])
}
###################END BLOCK#####################


#############X11 OUTPUT MANAGEMENT###############
#################MODIFY IF NEEDED################
#pause_output(options_vector)
###################END BLOCK#####################


