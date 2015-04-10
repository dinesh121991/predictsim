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
###################END BLOCK#####################


#type stuff here.
require("ggplot2")

#print(args)
df<-read.table(args$filenames[1])
#summary(df)
ranked=df[with(df, order(RMSBSLD)), ]

printable=ranked[, (colnames(ranked) %in% c("scheduler","predictor","corrector","pweight","pleftside","prightside","RMSS","RMSBSLD","pthreshold","prightparam","pleftparam"))]

draw_curve<-function(row,rank){

  if (row$scheduler=="easy_plus_plus_scheduler") {
    scheduler="Easy-SJBF"
  }else{
    scheduler="Easy-FCBF"
  }

  if (row$predictor=="predictor_sgdlinear") {
    predictor="learning"
  }else if (row$predictor=="predictor_tsafrir"){
    predictor="AVG2"
  }else if (row$predictor=="predictor_reqtime"){
    predictor="requested"
  }else if (row$predictor=="predictor_clairvoyant"){
    predictor="clairvoyant"
  }else{
    predictor=row$predictor
  }

  filename=paste(args$output,'/',rank,'_',as.integer(row$RMSBSLD),'_',scheduler,'_',predictor,'.pdf',sep='')
  set_output(device='pdf',filename=filename,ratio=1,execution_wd)


  if (!row$predictor=="predictor_sgdlinear") {


    p=plot(1, type="n", axes=F, xlab="", ylab="")
  }else{


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

    xlim=86400
    ylim=max(lossfunc(xlim),lossfunc(-xlim))
    p=ggplot(data.frame(x=c(-xlim,xlim)), aes(x)) +
    stat_function(fun=lossfunc) +
    scale_color_brewer(palette="Set3")+
    xlab("Prediction error")+
    ylab("Loss")+
    annotate("text",x=0,y=5*ylim/10,label=paste("scheduler:",scheduler),colour="blue")+
    annotate("text",x=0,y=5.5*ylim/10,label=paste("corrector:",row$corrector),colour="black")+
    annotate("text",x=0,y=6*ylim/10,label=paste("weight:",row$pweight),colour="black")+
    annotate("text",x=-3*xlim/4,y=8*ylim/10,label="underprediction\n may delay reservation",colour="blue")+
    annotate("text",x=3*xlim/4,y=8*ylim/10,label="overprediction\n no reservation delay",colour="blue")

  }
  print(p)
}

for (i in 1:20) {
  draw_curve(printable[i,],i)
  print(i)
  print(printable[i,])
}
###################END BLOCK#####################


#############X11 OUTPUT MANAGEMENT###############
#################MODIFY IF NEEDED################
#pause_output(options_vector)
###################END BLOCK#####################


