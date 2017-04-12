
if(exists("homePath"))
{
  setwd(homePath)
}else
{
  homePath<-getwd()
}

#Enter the Year for which the Graph to be plotted 
year <- "2009"
year2<-"2010"

#Enter the Station Name for which Graph to be Plotted
stationName <- "MALANA  HPS"

#Path for Dataset
pathForFile <- paste(getwd(),"/DataSet/Generation/",year,sep="") 
pathForFile2 <- paste(getwd(),"/DataSet/Generation/",year2,sep="") 

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

#load all files
filesarray2 <- list.files(path = pathForFile2, pattern = NULL, all.files = FALSE,
                         full.names = FALSE, recursive = FALSE)

j<-1
yearlyDataFrame2 <- list()   #Will hold year long Data
setwd(pathForFile2)          #Change Current Working Directory to Dataset Files
for(i in filesarray2)
{
  yearlyDataFrame2[[j]] <-read.csv(file=i,head=TRUE,sep=",")
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

j <- 1
actualGeneratedValues2<-vector()
for (i in yearlyDataFrame2)
{
  b <- i[grep(stationName,i$STATION),]
  actualGeneratedValues2[j] <- b$ACTUAL.GENERATION
  j <- j+1
}

setwd(homePath)

ymax = max(max(actualGeneratedValues),max(actualGeneratedValues2))
#Plot the Line chart.
plot(actualGeneratedValues,type = "l",ylim=c(0,ymax), col = "red", xlab = "Month", ylab = "Actual Generation", main = paste(stationName,"Generation of Electricty",year,"vs",year2),xaxt="n")

axis(side = 1, at=seq(1,12,1),labels = T)
text(1:12,actualGeneratedValues,actualGeneratedValues,pos = 1)

lines(actualGeneratedValues2,type="l",col="blue")
text(1:12,actualGeneratedValues2,actualGeneratedValues2,pos = 1)


ifelse(!dir.exists(file.path(homePath, "Plots")), dir.create(file.path(homePath, "Plots")), FALSE)

fname = paste("./Plots/",stationName,"-Plot-",year,".jpg",sep="")
dev.copy(jpeg,filename=fname);

dev.off ()

