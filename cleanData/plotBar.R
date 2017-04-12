#library(plotly)

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
stationName <- "MALANA  HPS"

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
programmedGeneration <- vector()
for (i in yearlyDataFrame)
{
  b <- i[grep(stationName,i$STATION),]
  actualGeneratedValues[j] <- b$ACTUAL.GENERATION
  programmedGeneration[j] <- b$PROGRAM.GENERATION
  j <- j+1
}

setwd(homePath)


x <- rbind(programmedGeneration,actualGeneratedValues)
colnames(x) <- c(1,2,3,4,5,6,7,8,9,10,11,12)
cols<-c("blue","yellow")
barplot(x, beside = TRUE,xlab = "Months",ylab="Power(GWHr)",main = paste(stationName,"Programmed-Generated ",year),col=cols)


ifelse(!dir.exists(file.path(homePath, "Plots")), dir.create(file.path(homePath, "Plots")), FALSE)

fname = paste("./Plots/",stationName," Bar-Plot-",year,".jpg",sep="")
dev.copy(jpeg,filename=fname);

dev.off ()

