data1 <- read.csv(file.choose(), header = T)
print(data1) 
data1$capacity <- as.numeric(gsub(",","",data1$CAPACITY))
plot(data1$STATION_NAME, data1$capacity, main="scatterplot",xlab="X",ylab="y",las=1,xlim=c(0,100))
