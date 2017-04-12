
if(exists("homePath"))
{
  setwd(homePath)
}else
{
  homePath<-getwd()
}

#Enter the Year for which the Graph to be plotted 
year <- "2010"

#Enter the Station Name for which Graph to be Plotted
stationName <- "Dr. N.TATA RAO TPS"

#Path for Dataset
pathForFile <- paste("./DataSet/monthlyCoal/",year,sep="") 

#load all files
filesarray <- list.files(path = pathForFile, pattern = NULL, all.files = FALSE,
                         full.names = FALSE, recursive = FALSE)

j<-1

yearlyDataFrame <- list()   #Will hold year long Data
setwd(pathForFile)          #Change Current Working Directory to Dataset Files
for(i in filesarray)
{
  yearlyDataFrame[[j]] <-read.csv(file=i,head=TRUE,sep=",")
  j=j+1
}

j <- 1
actualGeneratedValues<-vector()
for (i in yearlyDataFrame)
{
  b <- i[grep(stationName,i$Station.Name.1),]
  actualGeneratedValues[j] <- sum(b$Actual.Stock...Total)
  j <- j+1
}
setwd(homePath)



#Plot the Line chart.
plot(actualGeneratedValues,type = "o", col = "blue", xlab = "Month", ylab = "Total Coal(Kilo Ton)", main = paste(stationName,"Coal Consumption",year),xaxt="n")
axis(side = 1, at=seq(1,12,1),labels = T)
text(1:12,actualGeneratedValues,actualGeneratedValues,pos = 4)
ifelse(!dir.exists(file.path(homePath, "Plots")), dir.create(file.path(homePath, "Plots")), FALSE)

fname = paste("./Plots/",stationName,"Coal"," Plot-",year,".jpg",sep="")
dev.copy(jpeg,filename=fname);

dev.off ()