#Read a local csv file
#mat <- read.csv("Name_of_file")

#Read an online csv file
mat <- read.csv(url("https://people.sc.fsu.edu/~jburkardt/data/csv/ford_escort.csv"))

#Calculate the correlation matrix
cor(mat)