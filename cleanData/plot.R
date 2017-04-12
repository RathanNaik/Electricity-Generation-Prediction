
if(exists("homePath"))
{
  setwd(homePath)
}else
{
  homePath<-getwd()
}

#Enter the Year for which the Graph to be plotted 
year <- "2009"

#Enter the Station Name for which Graph to be Plotted
stationName <- "Dr. N.TATA RAO TPS"

#Path for Dataset
pathForFile <- paste("./DataSet/Generation/",year,sep="") 

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
  b <- i[grep(stationName,i$STATION),]
  actualGeneratedValues[j] <- b$ACTUAL.GENERATION
  j <- j+1
}

setwd(homePath)

#Plot the Line chart.
plot(actualGeneratedValues,type = "o", col = "red", xlab = "Month", ylab = "Actual Generation(GWHr)", main = paste(stationName,"Generation of Electricty",year),xaxt="n")
text(1:12,actualGeneratedValues,actualGeneratedValues,pos = 4)

axis(side = 1, at=seq(1,12,1),labels = T)

ifelse(!dir.exists(file.path(homePath, "Plots")), dir.create(file.path(homePath, "Plots")), FALSE)

fname = paste("./Plots/",stationName,"-Plot-",year,".jpg",sep="")
dev.copy(jpeg,filename=fname);

dev.off ()

