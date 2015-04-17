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
description=''
epilog=''

#External parser function: for usual options.
#e.g. parser=parser_swf(description,epilog)
parser=parser_pred(description,epilog)


#additional argparse entries for this particular script.
#e.g. parser$add_argument('-s','--sum', dest='accumulate', action='store_const', const=sum, default=max,help='sum the integers (default: find the max)')

#files you want to source from the rfold folder for this Rscript
#e.g. c('common.R','histogram.R')
userfiles=c()

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
options_vector=set_output(args$device,args$output,args$ratio,execution_wd)
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
library('plyr')
library('ggplot2')


#type stuff here.
plot_rec_curves <- function(preds,true_values,labelnames){
  true_runtime=ldply(true_values,data.frame)
  colnames(true_runtime)<-c("value")
  preds_dfs=data.frame()

  for (i in 1:length(preds)){
    d=ldply(preds[i],data.frame)

    d$value=labelnames[i]
    colnames(d)<-c("value","type")
    d$value=d$value-true_runtime$value
    #print(typeof(d))
    #print(class(d))

    #print(summary(d))
    preds_dfs=rbind(preds_dfs,d)
  }

  #print(summary(preds_dfs))


  theme_bwTUNED<-function()
  {
    return(theme_bw() +theme(
                             plot.title = element_text(face="bold", size=11),
                             axis.title.x = element_text(face="bold", size=11),
                             axis.title.y = element_text(face="bold", size=11, angle=90),
                             axis.text.x = element_text(size=10),
                             axis.text.y = element_text(size=10),
                             panel.grid.minor = element_blank(),
                             # 		panel.grid = element_blank(),
                             legend.key = element_rect(colour="white")))
  }

  mi=min(preds_dfs$value)
  ma=max(preds_dfs$value)

  p0 = ggplot(preds_dfs, aes(x = value,colour=type,linetype=type)) +
  theme_bwTUNED()+
  scale_linetype_manual(values=c(11,"dashed","dotdash","dotted"),
                       name="Prediction Method",
                       labels=c("E-Loss Regression", "Requested Time", "Squared Loss Regression","AVE(2)")
                      )+
scale_colour_manual(values=c("#5e3c99", "#fdb863","#b2abd2","#e66101"),
                       name="Prediction Method",
                       labels=c("E-Loss Regression", "Requested Time", "Squared Loss Regression","AVE(2)"))+
stat_ecdf(aes(group = type))+
coord_cartesian(xlim = c(-100000, 100000)) +
  scale_x_continuous(breaks=c(-21600,-43200,-64800,-86400,0,21600,43200,64800,86400),
                     labels=c(-6,-12,-18,-24,0,6,12,18,24))+
ylab("Cumulative Density")+
xlab("Prediction Error(hours)")+
theme(legend.justification=c(1,0), legend.position=c(0.95,0.01), legend.box="horizontal", legend.box.just="top")
#ggtitle("Cumulative distribution of prediction errors.")

#annotate("text", x =0.1*mi+0.9+ma , y = 0.5, label = "Over-Prediction\n Pure Backfill Mechanism")+
#annotate("text", x =0.1*ma+0.9+mi , y = 0.5, label = "Under-Prediction\n Prediction Failure")
#print(p0)
ggsave("rec.pdf",p0,width=10,height=4)

}

print(args$pred_filenames)
data=lapply(args$pred_filenames,read.table)
plot_rec_curves(preds=data[-1],true_values=data[1],labelnames=args$pred_filenames[-1])
print(args$pred_filenames)


###################END BLOCK#####################

#############X11 OUTPUT MANAGEMENT###############
#################MODIFY IF NEEDED################
pause_output(options_vector)
###################END BLOCK#####################


