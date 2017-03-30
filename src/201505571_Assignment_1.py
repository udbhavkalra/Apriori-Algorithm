#Apriori Algorithm

import sys, itertools, math
from sets import Set

def findCombOfLength(sortedList, lengthOfItems):		#return list of tuples
	listlen = len(sortedList); returnThisList = []
	if lengthOfItems == 1:
		for firstIndex in range(listlen-1):
			for secIndex in range(firstIndex+1,listlen):
				returnThisList.append((sortedList[firstIndex][0],sortedList[secIndex][0]))
		return returnThisList

	for firstIndex in range(listlen-1):
		matchFirstTuple = sortedList[firstIndex][0][:lengthOfItems-1]
		for secIndex in range(firstIndex+1, listlen):
			if matchFirstTuple == sortedList[secIndex][0][:lengthOfItems-1]:
				tempList = [item for item in matchFirstTuple]
				tempList.append(sortedList[firstIndex][0][lengthOfItems-1])
				tempList.append(sortedList[secIndex][0][lengthOfItems-1])
				returnThisList.append(tuple(tempList))
			else:
				break
	return returnThisList

#give the dictionary to this function. It will return the list after joining the most frequent allItemsDict
def findAllCombinations(allItemsDict, supportThreshold):				#return the tuple of all combination possible
	if len(allItemsDict.values()) == 0:
		return ()
	lengthOfItems = len(allItemsDict)
	for item in allItemsDict.keys():
		if type(item) == str:
			lengthOfItems = 1
			break
		lengthOfItems = len(item)
		break
	return findCombOfLength(sorted(allItemsDict.items(), key=lambda s: s[0]), lengthOfItems)

#generating finalItems which have value|frequence > threshold|support
def findCombinationsForSupportThreshold(allItemsDict, finalItems, supportThreshold, allItemsDictCopy):
	itemsForAssociation = []
	while len(allItemsDict.values()) != 0:
		firstTime = 1 									#to add items into itemsForAssociation
		for item in allItemsDict.keys():
			if len(allItemsDict[item]) < supportThreshold:
				allItemsDict.pop(item)
			else:
				if firstTime == 1:
					itemsForAssociation = []
					firstTime = 0
				itemsForAssociation.append(item)
		finalItems.update(allItemsDict)					#all values of allItemsDict got into finalItems
		listOfCombinations = findAllCombinations(allItemsDict, supportThreshold)
		allItemsDict.clear()			#clear all the values and add all other values with new_len=prev_len+1
		intersectionResult = Set([])
		for resultantItemTuple in listOfCombinations:
			firstTime = 0
			for thisItem in resultantItemTuple:
				if firstTime==0:
					intersectionResult = allItemsDictCopy[thisItem]
					firstTime = 1
					continue
				intersectionResult = intersectionResult.intersection(allItemsDictCopy[thisItem])
			allItemsDict[resultantItemTuple] = intersectionResult
	return itemsForAssociation

def findValidAssociationRules(allItemsDictCopy, allAssociationList, threshold):
	rowNums = Set([]); firstTime = 1; count = 0; returnThisList = []; numeratorFlag=0
	# print 'all:',allAssociationList
	for thisRule in allAssociationList:
		firstTime = 1; copyCurrentLeftSide = thisRule[0]; copyCurrentRightSide = thisRule[1]
		for leftSideEle in thisRule[0]:
			if firstTime == 1:
				firstTime = 0;	rowNums = allItemsDictCopy[leftSideEle]
			else:
				rowNums = rowNums.intersection(allItemsDictCopy[leftSideEle])
		denominator = len(rowNums)
		if numeratorFlag == 0:
			numeratorFlag = 1
			for rightSideEle in thisRule[1]:
				rowNums = rowNums.intersection(allItemsDictCopy[rightSideEle])
			numerator = len(rowNums)

		# print thisRule,numerator
		if denominator != 0.0 and float(float(numerator)/denominator) >= threshold:
			returnThisList.append(thisRule)
	return returnThisList

#return all subsets possible in form of list of tuples where first ele is leftside of '=>' and 2nd, right side of rule
def findAllSubsetsForAssociation(itemsForAssociation, allAssociationList):
	returnThisList = []
	length = len(itemsForAssociation); thisSet = Set(itemsForAssociation)
	for thisItem in thisSet:
		superSet = Set(thisItem)
		if type(thisItem) != str:
			length = len(superSet)
		for subsetSize in range(1,length):
			setsOfThisSize = Set(itertools.combinations(superSet,subsetSize))
			for currentSet in setsOfThisSize:
				leftSide = currentSet;	rightSide = superSet.difference(currentSet)
				allAssociationList.append((leftSide,rightSide))
		allAssociationList = findValidAssociationRules(allItemsDictCopy, allAssociationList, confidence)
		returnThisList.append(allAssociationList)
	# return allAssociationList
	return returnThisList

print "Enter the location of the folder:"
folderPath = raw_input()
readFileObj = open(folderPath+"/"+"config.csv")
lines = readFileObj.readlines()
inputInfo = {}; lineNumber = 0; allItemsDict = {}; finalItems = {}; allItemsDictCopy = {}
for line in lines:
	line = line.split(',')
	inputInfo[line[0]] = line[1].replace("\n","")					#stored as inputInfo{'input':'inputFilePath', other values}

givenData = open(inputInfo['input'],'r').readlines()
for line in givenData:
	line = line.split(',')
	for item in line:
		item = item.replace("\n","")
		if not allItemsDict.has_key(item):
			allItemsDict[item] = Set([lineNumber])
		else:
			allItemsDict[item].add(lineNumber)
	lineNumber += 1

# print 'all items:',allItemsDict
allItemsDictCopy.update(allItemsDict)			#have a copy of items to use it for searching
support = float(inputInfo['support']); confidence=float(inputInfo['confidence']); stringWriteToFile = ""
outputFile= open(inputInfo['output'],'w'); flag=inputInfo['flag']; itemsForAssociation = []; allAssociationList = []
supportThreshold = math.ceil(float(float(support)*lineNumber))
itemsForAssociation = findCombinationsForSupportThreshold(allItemsDict, finalItems, supportThreshold, allItemsDictCopy)

stringWriteToFile = str(len(finalItems.keys()))+'\n'
for item in finalItems.keys():
	if type(item) == str:
		stringWriteToFile += str(item)+','
	else:
		for thisItem in item:
			stringWriteToFile += str(thisItem)+','
	stringWriteToFile = stringWriteToFile[:-1:];stringWriteToFile += '\n'

# to find all association rules:
if flag == '1':
	# print 'items:',itemsForAssociation
	allAssociationList = findAllSubsetsForAssociation(itemsForAssociation, allAssociationList)
	# print allAssociationList
	# allAssociationList = findValidAssociationRules(allItemsDictCopy, allAssociationList, confidence)
	# print allAssociationList
	stringWriteToFile += str(len(allAssociationList))+'\n'
	for thisRule in allAssociationList:
		# print 'this:',thisRule
		for leftSideEle in thisRule[0]:
			stringWriteToFile += str(leftSideEle)+','
		stringWriteToFile += ' => '
		for rightSideEle in thisRule[0]:
			stringWriteToFile += str(rightSideEle)+','
		stringWriteToFile += '\n'
		
#to write into the output file
outputFile.write(str(stringWriteToFile))							#write to the output file