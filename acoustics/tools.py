# Basic tools to calculate a range of acoustic properties
#
# Authors:
# Robin Wareing - r.r.wareing@gmail.com
# John Bull - 
# Michael Smith
#
# Sources:
# Engineering Noise Control - Fourth Edition - Bies & Hansen
# Guide to assessing road traffic noise - NZ Trasport Agency
# BS5228-1
# BS5228-2

import math

def BS5228_PropigationLoss(receiverDist,sourceDist):
    '''Calculates the propigation loss over a set distance using BS5338-1 method'''
    if receiverDist < 25:
        propigationLoss = 20*math.log10(1.*receiverDist/sourceDist)
    else:
        propigationLoss = 25*math.log10(1.*receiverDist/sourceDist)-2
    return propigationLoss

def OpenSpacePowerToPressure(soundPowerLevel,distance,geometricFactor):
    '''Basic conversion from sound power to sound pressure. 
    Based on geometical spreading with no ground absorption'''
    if geometricFactor == "spherical":
        Q = 1
    elif geometricFactor == "hemispherical":
        Q = 2
    elif geometricFactor == "quarter-spherical":
        Q = 4
    elif geometricFactor == "eigth-spherical":
        Q = 8
    soundPressure = soundPowerLevel-math.log10((4*math.pi*distance**2)/Q)
    return soundPressure

def BuildThirdOctave(startFreq = 12.5,stopFreq = 20000):
    '''Generates array of 1/3rd octaves between start and stop frequency'''
    referenceThirdOctaves = [12.5,16,20,25,
                       31.5,40,50,63,
                       80,100,125,160,
                       200,250,315,400,
                       500,630,800,1000,
                       1250,1600,2000,2500,
                       3150,4000,5000,6300,
                       8000,10000,12500,16000,
                       20000]
    thirdOctaves = []
    for band in referenceThirdOctaves:
        if band >= startFreq and band <= stopFreq:
            thirdOctaves.append(band)
    return thirdOctaves
    
def BuildOctave(startFreq = 16,stopFreq = 10000):
    '''Generates array of octaves between start and stop frequency'''
    referenceOctaves = [16,31.5,63,125,
                       250,500,1000,2000,
                       4000,8000,10000]

    octaves = []
    for band in referenceOctaves:
        if band >= startFreq and band <= stopFreq:
            octaves.append(band)    
    return octaves

def SpeedOfSound(temp = 20):
    '''Calculates speed of sound based on air temperature'''
    R = 8.314
    M = 0.029
    y = 1.4
    T = 273 + temp
    return math.sqrt(y*R*T/M)

def AirDensity(temp = 20):
    R = 287.058
    P = 101.325
    T = 273 + temp
    return P/(R*T)

def Wavelength(frequency):
    C = SpeedOfSound()
    return C/frequency

def ThirdOctaveWeightingCurves(weightingType,startFreq,stopFreq):
    '''Generates a 2D array of third octave band centre frequencies,
    and weighting values for A and C weighing curves'''
    if weightingType == "A":
        rawWeighting = [[10,12.5,16,20,
                      35,31.5,40,50,
                      63,80,100,125,
                      160,200,250,315,
                      400,500,630,800,
                      1000,1250,1600,2000,
                      2500,3150,4000,5000,
                      6300,8000,10000,12500,
                      16000,20000],
                     [-70.4,-63.4,-56.7,-50.5,
                      -44.7,-39.4,-34.6,-30.2,
                      -26.2,-22.5,-19.1,-16.1,
                      -13.4,-10.9,-8.6,-6.6,
                      -4.8,-3.2,-1.9,-0.8,
                      0.0,0.6,1.0,1.2,
                      1.3,1.2,1.0,0.5,
                      -0.1,-1.1,-2.5,-4.3,
                      -6.6,-9.3]]
    elif weightingType == "C":
        rawWeighting = [[10,12.5,16,20,
                      35,31.5,40,50,
                      63,80,100,125,
                      160,200,250,315,
                      400,500,630,800,
                      1000,1250,1600,2000,
                      2500,3150,4000,5000,
                      6300,8000,10000,12500,
                      16000,20000],
                     [-14.3,-11.2,-8.5,-6.2,
                      -4.4,-3.0,-2.0,-1.3,
                      -0.8,-0.5,-0.3,-0.2,
                      -0.1,0.0,0.0,0.0,
                      0.0,0.0,0.0,0.0,
                      0.0,0.0,-0.1,-0.2,-0.3,
                      -1.3,-2.0,-3.0,-4.4,
                      -6.2,-8.5,-11.2]]
    weights = []
    frequencies = []
    for i in range(len(rawWeighting[0])):
        if rawWeighting[0][i] >= startFreq and rawWeighting[0][i] <= stopFreq:
            weights.append(rawWeighting[1][i])
            frequencies.append(rawWeighting[0][i])
    weighting = [frequencies,weights]
    return weighting

def OctaveWeightingCurves(weightingType,startFreq,stopFreq):
    '''Generates a 2D array of octave band centre frequencies,
    and weighting values for A and C weighing curves'''
    if weightingType == "A":
        rawWeighting = [[31.5,63,125,
                       250,500,1000,2000,
                       4000,8000],
                     [-39.4,-26.2,-16.1,-8.6,
                      -3.2,0,1.2,1,-1.1
                      ]]
    elif weightingType == "C":
        rawWeighting = [[31.5,63,125,
                       250,500,1000,2000,
                       4000,8000],
                     [-3,-0.8,-0.2,0,
                      0,0,-0.2,-0.8,-3]]
    weights = []
    frequencies = []
    for i in range(len(rawWeighting[0])):
        if rawWeighting[0][i] >= startFreq and rawWeighting[0][i] <= stopFreq:
            weights.append(rawWeighting[1][i])
            frequencies.append(rawWeighting[0][i])
    weighting = [frequencies,weights]
    return weighting
    
def dBA(levels,freq,bandType):
    '''Calculates total dBA level for either 1/3 or 1/1 octave band data'''
    weightedLevel = []
    if bandType == "1/1":
        weightingCurve = OctaveWeightingCurves("A",freq[0],freq[-1])
    elif bandType == "1/3":
        weightingCurve = ThirdOctaveWeightingCurves("A",freq[0],freq[-1])
    for i in range(len(levels)):
        weightedLevel.append(levels[i] + weightingCurve[1][i])
    return dBadd(weightedLevel)
    
def dBC(levels,freq,bandType):
    '''Calculates total dBC level for either 1/3 or 1/1 octave band data'''
    weightedLevel = []
    if bandType == "1/1":
        weightingCurve = OctaveWeightingCurves("C",freq[0],freq[-1])
    elif bandType == "1/3":
        weightingCurve = ThirdOctaveWeightingCurves("C",freq[0],freq[-1])
    for i in range(len(levels)):
        weightedLevel.append(levels[i] + weightingCurve[1][i])
    return dBadd(weightedLevel)
    
def dBadd(levels):
    '''Performs dB addition (logarithmic addition)'''
    pressureAbs = 0
    for level in levels:
        pressureAbs = pressureAbs + 10**(level/10)
    return 10*math.log10(pressureAbs)
    
def dBavg(levels):
    '''Performs dB averaging (logarithmic average)'''
    pressureAbs = 0
    for level in levels:
        pressureAbs = pressureAbs + 10**(level/10)
    return 10*math.log10(pressureAbs/len(levels))
    
def SimpleCRTN(annualAvgTraffic,percentageHeavyVehicles,speed,gradient,
               surfaceCorrection,receiverDist,receiverHeight,
               angleOfView,percentAbsorption):
    ''' Performs a simple CoRTN calculation,.
    This does NOT include screening/barriers'''
    Cdist = -10.0*math.log10(receiverDist/13.5)
    Cuse = (33.0*math.log10(speed+40+(500./speed))+
            10.0*math.log10(1+(5.0*percentageHeavyVehicles/speed))-
            68.8)
    Cgrad = 0.2*gradient
    Ccond = 0
    if receiverHeight >= 1.0 and receiverHeight <= (receiverDist/3-1.2):
        Cground = 5.2*percentAbsorption*math.log10(3*receiverHeight/(receiverDist+3.5))
    elif receiverHeight > (receiverDist/3-1.2):
        Cground = 0
    elif receiverHeight <= 1.0:
        Cground = 5.2*percentAbsorption*math.log10(3/(receiverDist+3.5)) 
    Cbarrier = 0
    Cview = 10*math.log10(angleOfView/180)
    LA10 = (29.1 + 10*math.log10(annualAvgTraffic)+Cdist+Cuse+Cgrad+Ccond+
            Cground+Cbarrier+Cview)
    LAeq = LA10 - 3
    return LAeq
    
def SimpleISO9140():
    '''Nothin in here yet'''

def SourceCountCorrectinon(num):
    '''Correction factor for multiple sources'''
    return 10*math.log10(num)

def DutyCycleCorrection(dutyCycle):
    '''Correction factor for duty cycle of sources'''
    return 10*math.log10(dutyCycle)

def NZS6806_Category(level,roadType):
    '''Returns the NZS6806 category (A, B or C) based on the input level and 
    road type (New, New(HighFlow), or Altered)'''
    if roadType == "New":
        if level <= 57:
            return "A"
        elif level > 57 and level <= 64:
            return "B"
        elif level > 64:
            return "C"
    if roadType == "New(HighFlow)":
        if level <= 64:
            return "A"
        elif level > 64 and level <= 67:
            return "B"
        elif level > 67:
            return "C"
    if roadType == "Altered":
        if level <= 64:
            return "A"
        elif level > 64 and level <= 67:
            return "B"
        elif level > 67:
            return "C"

def RoadSurfaceCorrection():
    '''nothin in 'ere yet...'''

def TeirOneRoadTrafficScreen(numberOfPPFs,AADT):
    '''Performs teir 1 assessment of road traffic noise'''
    '''PPF risk rating'''
    if numberOfPPFs == 0:
        riskPPFs = "N/A"
    elif numberOfPPFs > 0 and numberOfPPFs <= 50:
        riskPPFs = "Low"
    elif numberOfPPFs > 50 and numberOfPPFs <= 200:
        riskPPFs = "Medium"
    elif numberOfPPFs > 200:
        riskPPFs = "High"
    '''AADT risk rating'''
    if AADT <= 2000:
        riskAADT = "N/A"
    elif numberOfPPFs > 2000 and numberOfPPFs <= 10000:
        riskAADT = "Low"
    elif numberOfPPFs > 10000 and numberOfPPFs <= 50000:
        riskAADT = "Medium"
    elif numberOfPPFs > 50000:
        riskAADT = "High"
    '''Total risk rating'''
    if riskPPFs == "N/A" or riskAADT == "N/A":
        teir1Risk = "N/A"
    elif riskPPFs == "Low" and riskAADT == "Low":
        teir1Risk = "Low"
    elif riskPPFs == "High" or riskAADT == "High":
        teir1Risk = "High"
    else:
        teir1Risk = "Medium"
    return [riskPPFs,riskAADT,teir1Risk]
    
def InfiniteSeriesOfPoints(coherance,sourceSpacing,receiverDist,sourcePower):
    speedOfSound = SpeedOfSound(20)
    airDensity = AirDensity(20)
    if coherance == "Coherant":
        sourceLevel = (sourcePower - 6 - 10*math.log10(receiverDist)- 10*math.log10(sourceSpacing)+10*math.log10(speedOfSound*airDensity/400))
    elif coherance == "Incoherant":
        sourceLevel = (sourcePower - 8 - 10*math.log10(receiverDist)- 10*math.log10(sourceSpacing)+10*math.log10(speedOfSound*airDensity/400))
    return sourceLevel
        
def DirectivityIndex(directivityFactor):
    if directivityFactor == 1:
        directivityIndex = 0
    elif directivityFactor == 2:
        directivityIndex = 3
    elif directivityFactor == 3:
        directivityIndex = 6
    elif directivityFactor == 4:
        directivityIndex = 9
    return directivityIndex

def VibrationAtADistance(soilAttenuation,measuredVibration,measurementDist,receiverDist):
    return measuredVibration*((measurementDist/receiverDist)**0.5)*math.exp(-1*soilAttenuation*(receiverDist-measurementDist))


#==============================================================================
#     
# Below is a list of items to be included into the tool set (RW 20170930)
# Add/update this list accordingly.
#
# In additin 
#
# - flow resistivity
# - Wavenumber
# - ISO9613-2 propagation tools
# - CONCAWE propagation tools
# - CNOSSOS propagation tools
# - NZS6806 screening tools (teir 1 assessment done)
# Propagation loss for the following:
# - Point source
# - line source
# - plane source
# - array of points source
# - Angle of view correction
# - SEL calculation tools
# Single number ratings:
# - Rw
# -Ctr
# -Rw+C
# -Rw+Ctr
# -STC
# - Ln,w
# - IIC
#==============================================================================