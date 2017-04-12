data1  <- read.csv(file.choose(), header = T)
#mpExpenses2012 is the large dataframe containing data for each MP
#Get the list of unique MP names
for (name in levels(data1$STATE))
{
  #Subset the data by MP
  tmp=subset(data1,data1$STATE==name)
  #Create a new filename for each MP - the folder 'mpExpenses2012' should already exist
  fn=paste('cleanData/Statewise/',gsub(' ','',name),sep='')
  #Save the CSV file containing separate expenses data for each MP
  write.csv(tmp,fn,row.names=FALSE)
}
for (name in levels(data1$REGION))
{
  #Subset the data by MP
  tmp=subset(data1,data1$REGION==name)
  #Create a new filename for each MP - the folder 'mpExpenses2012' should already exist
  fn=paste('cleanData/Region/',gsub(' ','',name),sep='')
  #Save the CSV file containing separate expenses data for each MP
  write.csv(tmp,fn,row.names=FALSE)
  
}
for (name in levels(data1$CATEGORY))
{
  #Subset the data by MP
  tmp=subset(data1,data1$CATEGORY==name)
  #Create a new filename for each MP - the folder 'mpExpenses2012' should already exist
  fn=paste('cleanData/Category/',gsub(' ','',name),sep='')
  #Save the CSV file containing separate expenses data for each MP
  write.csv(tmp,fn,row.names=FALSE)
  
}

