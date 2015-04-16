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
options_vector=set_output(args$device,args$output,1.5,execution_wd)
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
df1<-read.table(args$filenames[1])
df2<-read.table(args$filenames[2])
#summary(df)

df1 = df1[,(colnames(df1) %in% c("name","avgbsld","predictor","scheduler"))]
df2 = df2[,(colnames(df2) %in% c("name","avgbsld"))]
result=merge(df1, df2, by="name")
result=result[which(!is.na(result$avgbsld.x) & !is.na(result$avgbsld.y) & !result$predictor=="easy_backfill" & !result$predictor=="easy_backfill"),]
summary(result)

csp = cor(result$avgbsld.x , result$avgbsld.y  , method = "spearman")
cp = cor(result$avgbsld.x , result$avgbsld.y  , method = "pearson")



theme_bwTUNED<-function()
{
	return(theme_bw() +theme(
		plot.title = element_text(face="bold", size=14),
		axis.title.x = element_text(face="bold", size=14),
		axis.title.y = element_text(face="bold", size=14, angle=90),
		axis.text.x = element_text(size=10),
		axis.text.y = element_text(size=10),
		panel.grid.minor = element_blank(),
# 		panel.grid = element_blank(),
		legend.key = element_rect(colour="white")))
}


xlim=max(result$avgbsld.x)
ylim=max(result$avgbsld.y)
p=ggplot(result, aes(x=avgbsld.x,y=avgbsld.y))+
geom_point(aes(colour=factor(scheduler),shape=factor(predictor)))+
xlab(paste("AVGBSLD for KTH-SP2"))+
ylab(paste("AVGBSLD for CTC-SP2"))+
theme_bwTUNED()+
theme(legend.justification=c(1,0), legend.position=c(0.85,0.7), legend.box="horizontal", legend.box.just="top")+
scale_colour_manual(values=c("#000000", "#999999"), 
                       name="Scheduler",
                       breaks=c("easy_prediction_backfill_scheduler", "easy_plus_plus_scheduler"),
                       labels=c("EASY", "EASY++"))+
scale_shape_discrete(name="Predictor",
                        breaks=c("predictor_clairvoyant", "predictor_double_reqitme", "predictor_reqtime", "predictor_sgdlinear", "predictor_tsafrir"),
                        labels=c("Clairvoyant", "DOUBLE", "REQTIME", "SGDLINEAR", "TSAFRIR"))
# ggtitle("Scatter plot of algorithm's relative performance between the KTH-SP2 and SCDC-SP2 logs.")+


#annotate("text",x=9*xlim/10,y=9*ylim/10,
         #label=paste("Spearman's CC:",format(csp, digits=4)))+
#annotate("text",x=8*xlim/10,y=8*ylim/10,
         #label=paste("Pearson's CC:",format(cp, digits=4)))+
print(p)
###################END BLOCK#####################

#############X11 OUTPUT MANAGEMENT###############
#################MODIFY IF NEEDED################
#pause_output(options_vector)
###################END BLOCK#####################
