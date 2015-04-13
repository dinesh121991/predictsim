



a = read.csv2('AAA_metrics_complete', sep="", header=TRUE)
a = a[,c("trace", "predictor", "RMSBSLD")]


res_trace = c()
res_clair = c()
res_reqti = c()

for(trace in levels(a$trace)) {
	clair = as.double(as.character(a[which(a$trace == trace & a$predictor == "clairvoyant"),]$RMSBSLD))
	reqti = as.double(as.character(a[which(a$trace == trace & a$predictor == "reqtime"),]$RMSBSLD))
	res_trace = c(res_trace, trace)
	res_clair = c(res_clair, clair)
	res_reqti = c(res_reqti, reqti)
}


res = data.frame(trace=res_trace, reqti=res_reqti, clair=res_clair)

res$impr = res$reqti/res$clair*100

print(res)

