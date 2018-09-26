#Caitlin Pinkard
#Snag Assessment
#Program Description: This program takes a file on command line, parses it manually, and outputs
#rows that correspond to optional query parameters also given on command line. There is functionality for
#outputting either the union or intersection of the given queries.
#USAGE: [Snag.py] [file name] [optional filters with form like "location=richmond"]

import sys
print("\n\n","-"*70,"\n",sep="")

numFilters = len(sys.argv) - 2
#if the user input more than 1 query filter, it will ask them if they want the union or intersection of
#those filters - if they input an invalid character, it will continue to prompt them with this question
orAnd = "NULL"
if numFilters > 1:
      while orAnd != "u" and orAnd != "i":
            orAnd = input("Would you like a union or an intersection of these queries (u/i)?  ")
      print("\n","-"*70,"\n",sep="")


rows = []
numFail = 0
failRowNum  = []
fileName = sys.argv[1]
rowNum = 0
sepCar = ","
#use with so that the file will be closed when read completely
#break the column up into lines and split lines on commas
#if a line fails, print the error and save the row number to output to the user
with open(fileName, 'r', encoding = 'utf-8-sig') as file:
      for line in file:
            try:
                  if(rowNum == 0):
                        if(line.find("\t") != -1):
                              sepCar = "\t"
                  line = line.strip()
                  rows.append(line.split(sep = sepCar))
            except Exception as e:
                  print(e)
                  numFail+=1
                  failRowNum.append(rowNum)
            rowNum += 1
                  


print("Number of successful rows read in:",len(rows),"\n")
if numFail > 0:
      print("Row Numbers of failures: ",failRowNum,"\n")
print("Number of failures encountered: ", numFail, "\n")
print("-"*70,"\n")


#queryDict will store filters
queryDict = {}
#this while loop will handle multiple filters input by the user
while numFilters > 0:
      strFilter = sys.argv[len(sys.argv)-numFilters]

      #parse each optional command line argument by splitting up it on an equal sign
      #store both the column name and the desired value in a dictionary
      #if the argument is invalid, inform the user of the correct form
      try:
            strip = [x.strip() for x in strFilter.split('=')]
            colName = strip[0]
            value = strip[1]
            queryDict[colName] = value                             
      except:
            print("\nIllegal Query - Please input a query of the form: ColumnName=DesiredValue\n")
            sys.exit()
      numFilters = numFilters - 1


retVal = []
GoodRowNums = []
#print(queryDict)
try:
      #if the user wants the union of their filters or only input one filter, we just accumulate
      #all of the columns that fit that criteria into retVal
      if orAnd == "u" or len(sys.argv) - 2 == 1:
            #iterate over the filters
            for key, value in queryDict.items():
                  colNum = rows[0].index(key)
                  #look through rows of data for those that match the filter criteria
                  for i in range(1,len(rows)):
                        if rows[i][colNum] == value and i not in GoodRowNums:
                              retVal.append(rows[i])
                              GoodRowNums.append(i)
      #if the user wants the intersection of their filters, we search each row and if it satisfies all
      #the filters, add it to the rows to be returned
      elif orAnd == "i":
            GoodRows = []
            for i in range(1,len(rows)):
                  flag = 0
                  for key, value in queryDict.items():
                        if rows[i][rows[0].index(key)] != value:
                              flag = 1
                  if flag == 0:
                        GoodRows.append(rows[i])
                        GoodRowNums.append(i)
                  retVal = GoodRows

 #alert the user if the column they input isn't in the data                       
except Exception as e:
      print(e)
      print("\nInvalid column ("+colName+") specified. Nothing returned for this query.\n")
      sys.exit()
                  
#if retVal is empty, alert the user that there are no rows matching their query
if not retVal:
      print("No rows matching that query.")
#otherwise print out their filters again, and any rows that fit their criteria
else:
      print("Rows with ",end = "")
      for key,val in queryDict.items():
            if  key == list(queryDict.keys())[-1]:
                  print(key,"=",val, end = ":")
            else:
                  if orAnd == "u":
                        print(key,"=",val, end = "  OR  ")
                  elif orAnd == "i":
                        print(key,"=",val, end = "  AND  ")
                  
      print("\n\n", retVal)
      print("\nRow numbers: ",GoodRowNums,"\n")

print("\n","-"*70,"\n\n",sep="")
