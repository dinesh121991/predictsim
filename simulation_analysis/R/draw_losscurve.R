require("ggplot2")

draw_curve<-function(row,xlim=424800){

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

  filename=paste(args$output,'/',row$rank,'_',as.integer(row$RMSBSLD),'_',scheduler,'_',predictor,'.pdf',sep='')
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

