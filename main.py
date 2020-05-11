
def CreateInitialLists():
	global Steps
	global Time
	global Total_msd
	Steps = []
	X_msd = []
	Y_msd = []
	Z_msd = []
	Time  = []
	Total_msd = []
	print("The lists Steps, X_msd, Y_msd, Z_msd, Time, and Total_msd were Created.")
	return




def ReadMsdFileAndAddToList(file1):
	file_input = open(file1 , 'r')
	for line in file_input:
		if '#' not in line:
			line_splitted = line.split()
			Steps.append(int(line_splitted[0]))
			Total_msd.append(float(line_splitted[4]))
	file_input.close()
	print("The Steps and Total_msd values were read on " + file1 + " file.")
	return




def GetTemperature(temperature_in_kelvin):
	global Temperature
	Temperature = int(temperature_in_kelvin)
	print("The temperature value was set to " + str(Temperature) + " K.")
	return



def GetTimeStep(timestep_in_picoseconds):
	global TimeStep 
	TimeStep = float(timestep_in_picoseconds)
	print("The timestep of " + str(TimeStep) + "  picoseconds was acquired.")
	return




def GetTimeValues():
	for element in Steps:
		Time.append(element*TimeStep) 
	print("Time values acquired from TimeStep and Steps values.")
	return

def AutomaticDefine3TimeRanges():
	global MaxTimeIndex1
	global MaxTimeIndex2
	global MaxTimeIndex3
	Steps_length = len(Steps)
	Steps_length_divided_by_3 = int (len(Steps)/3)
	MaxTimeIndex1 = Steps_length_divided_by_3
	MaxTimeIndex2 = Steps_length_divided_by_3 *2
	MaxTimeIndex3 = Steps_length-1
	print("Three automatic time ranges were defined, [0, " + str(Time[MaxTimeIndex1]) + "], [0, " + str(Time[MaxTimeIndex2]) + "], and [0, " + str(Time[MaxTimeIndex3]) + "], times in picoseconds.")
	return



def ManualDefine3TimeRanges(ManualMaxTime1, ManualMaxTime2, ManualMaxTime3):
	global MaxTimeIndex1
	global MaxTimeIndex2
	global MaxTimeIndex3
	
	TimeValueCLosestToRange1 = min(Time, key = lambda x:abs(x - float(ManualMaxTime1)))
	TimeValueCLosestToRange2 = min(Time, key = lambda x:abs(x - float(ManualMaxTime2)))
	TimeValueCLosestToRange3 = min(Time, key = lambda x:abs(x - float(ManualMaxTime3))) 

	for i in range(0,len(Time)):
		if Time[i] == TimeValueCLosestToRange1:
			MaxTimeIndex1 = i
		if Time[i] == TimeValueCLosestToRange2:
			MaxTimeIndex2 = i
		if Time[i] == TimeValueCLosestToRange3:
			MaxTimeIndex3 = i

	print("The manual time ranges were defined,  [0, " + str(Time[MaxTimeIndex1]) + "], [0, " + str(Time[MaxTimeIndex2]) + "], and [0, " + str(Time[MaxTimeIndex3]) + "], times in picoseconds.")
	return



def CreateTimeAndMsdListsAccordingToRanges():
	global TimeRange1 
	global TimeRange2 
	global TimeRange3 

	global TotalMsdRange1
	global TotalMsdRange2 
	global TotalMsdRange3 

	TimeRange1 = []
	TimeRange2 = []
	TimeRange3 = []

	TotalMsdRange1 = []
	TotalMsdRange2 = []
	TotalMsdRange3 = []

	for i in range (0,len(Time)):
		if i <= MaxTimeIndex1:
			TimeRange1.append(Time[i])
			TotalMsdRange1.append(Total_msd[i])

		if i <= MaxTimeIndex2:
			TimeRange2.append(Time[i])
			TotalMsdRange2.append(Total_msd[i])

		if i <= MaxTimeIndex3:
			TimeRange3.append(Time[i])
			TotalMsdRange3.append(Total_msd[i])
	
	print("The Time and MSD lists were create according to obtained Ranges.")
	return



def LinearAdjust():
	from scipy import polyfit
	from scipy import polyval
	from sklearn import metrics

	global PredictedMsdRange1
	global ScoreR2Range1
	global TotalMsdAdjustRange1

	global PredictedMsdRange2
	global ScoreR2Range2
	global TotalMsdAdjustRange2

	global PredictedMsdRange3
	global ScoreR2Range3
	global TotalMsdAdjustRange3

	TotalMsdAdjustRange1 = polyfit(TimeRange1,TotalMsdRange1,1)
	PredictedMsdRange1 = polyval(TotalMsdAdjustRange1,TimeRange1)
	ScoreR2Range1 = metrics.r2_score(TotalMsdRange1,PredictedMsdRange1)
	print("The total msd linear regression was done in range 1, r2 = " + str(ScoreR2Range1))

	TotalMsdAdjustRange2 = polyfit(TimeRange2, TotalMsdRange2,1)
	PredictedMsdRange2 = polyval(TotalMsdAdjustRange2,TimeRange2)
	ScoreR2Range2 = metrics.r2_score(TotalMsdRange2,PredictedMsdRange2)
	print("The total msd linear regression was done in range 2, r2 = " + str(ScoreR2Range2))

	TotalMsdAdjustRange3 = polyfit(TimeRange3,TotalMsdRange3,1)
	PredictedMsdRange3 = polyval(TotalMsdAdjustRange3, TimeRange3)
	ScoreR2Range3 = metrics.r2_score(TotalMsdRange3,PredictedMsdRange3)
	print("The total msd linear regression was done in range 3, r2 = " + str(ScoreR2Range3))

	return



def CalcDiffusionCoefficients():
	global D1
	global D2
	global D3

	D1_Angstron_per_picosecond = TotalMsdAdjustRange1[0]/6
	D1 = D1_Angstron_per_picosecond*10e-8

	D2_Angstron_per_picosecond = TotalMsdAdjustRange2[0]/6
	D2 = D2_Angstron_per_picosecond*10e-8

	D3_Angstron_per_picosecond = TotalMsdAdjustRange3[0]/6
	D3 = D3_Angstron_per_picosecond*10e-8

	print("The Diffusion Coefficients were calculated, D1 = " + str(D1) + " m2/s, D2 =  " + str(D2) + " m2/s, and D3 = "+ str(D3)+" m2/s.")

	return


def CreateFinalListsToPlot():
	global ListValuesX
	global ListRealValuesY
	global ListPredictedValuesY
	global ListMaxIndexTime
	global ListR2Score
	global ListAdjusts
	global ListDiffusionCoefficients

	ListValuesX = [TimeRange1,TimeRange2,TimeRange3]
	ListRealValuesY = [TotalMsdRange1,TotalMsdRange2,TotalMsdRange3]
	ListPredictedValuesY = [PredictedMsdRange1,PredictedMsdRange2,PredictedMsdRange3]
	ListMaxIndexTime = [MaxTimeIndex1, MaxTimeIndex2, MaxTimeIndex3]
	ListR2Score = [ScoreR2Range1,ScoreR2Range2,ScoreR2Range3]
	ListAdjusts = [TotalMsdAdjustRange1,TotalMsdAdjustRange2,TotalMsdAdjustRange3]
	ListDiffusionCoefficients = [D1,D2,D3]

	print("The final lists were created to plot the adjusts according to the TimeRanges.")



def PlotAndSave():
	import matplotlib.pyplot as plt 
	for index in range (0,len(ListValuesX)):
		f = plt.figure()
		ax = f.add_subplot(111)
		plt.plot(ListValuesX[index], ListRealValuesY[index],'r-')
		plt.plot(ListValuesX[index],ListPredictedValuesY[index],'b-')
		plt.xlabel("Time(ps)")
		plt.ylabel("Total MSD ($\AA ^2$)")
		textstr = '\n'.join( ("r2 = " + str(ListR2Score[index]), "slope = " + str(ListAdjusts[index][0]),\
			"intercept = " + str(ListAdjusts[index][1]), 
			"D =  " + str(ListDiffusionCoefficients[index]) + "  m2/s", "Temperature = " + str(Temperature) + " K"))
		plt.text(0.3,0.8, textstr, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)
		plt.savefig("total_msd_"+ str(int(Time[ListMaxIndexTime[index]])) + "ps.png")
		plt.show()
		plt.close()

	print("The figures were saved as total_msd_**ps.png")
	

	return



CreateInitialLists()
ReadMsdFileAndAddToList("example.txt")
GetTemperature(400)
GetTimeStep(0.001)
GetTimeValues()
AutomaticDefine3TimeRanges()
#ManualDefine3TimeRanges(value1_in_picoseconds,value2_in_picoseconds,value3_in_picoseconds)
CreateTimeAndMsdListsAccordingToRanges()
LinearAdjust()
CalcDiffusionCoefficients() 
CreateFinalListsToPlot()
PlotAndSave()
