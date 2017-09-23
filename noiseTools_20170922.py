# Basic tools to calculate noise information
# Robin Wareing - 22/09/2017

import math

def BS5228_PropigationLoss(receiverDist,sourceDist):
    '''Calculates the propigation loss over a set distance using BS5338-2 method'''
    if receiverDist < 25:
        propigationLoss = 20*math.log10(receiverDist/sourceDist)
    else:
        propigationLoss = 25*math.log10(receiverDist/sourceDist)-2
    return propigationLoss

def OpenSpacePowerToPressure(soundPowerLevel,distance,geometricFactor):
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

def BuildThirdOctave(startFreq,stopFreq):
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
    
def BuildOctave(startFreq,stopFreq):
    referenceOctaves = [16,31.5,63,125,
                       250,500,1000,2000,
                       4000,8000,10000]

    octaves = []
    for band in referenceOctaves:
        if band >= startFreq and band <= stopFreq:
            octaves.append(band)    
    return octaves

def speedOfSound(temp):
    R = 8.314
    M = 0.029
    y = 1.4
    T = 273 + temp
    return math.sqrt(y*R*T/M)

def ThirdOctaveWeightingCurves(wieghtingType,startFreq,stopFreq):
    aa
    if wieghtingType == "A":
        weighting = [['frequencies'],
                     ['corrections']]
    elif weightingType == "C":
        weighting = [['frequencies'],
                     ['corrections']]
    return weighting
    
def dBA(levels,freq,bandType):
    weightedLevel = []
    if bandType == "1/1":
        weightingCurve = ThirdOctaveWeightingCurves("A",freq[0],freq[-1])
    elif bandType == "1/3":
        weightingCurve = OctaveWeightingCurves("A",freq[0],freq[-1])
    for i in range(levels):
        weightedLevel.append(levels[i] + wieghtingCurve[1][i])
    return dBadd(weightedLevel)
    
def dBC(levels,freq,bandType):
    weightedLevel = []
    if bandType == "1/1":
        weightingCurve = ThirdOctaveWeightingCurves("C",freq[0],freq[-1])
    elif bandType == "1/3":
        weightingCurve = OctaveWeightingCurves("C",freq[0],freq[-1])
    for i in range(levels):
        weightedLevel.append(levels[i] + wieghtingCurve[1][i])
    return dBadd(weightedLevel)
    
def dBadd(levels):
    pressureAbs
    for level in levels:
        pressureAbs = pressureAbs + 10**(level/10)
    return 10*math.log10(pressureAbs)
    
def dBavg(levels):
    pressureAbs
    for level in levels:
        pressureAbs = pressureAbs + 10**(level/10)
    return 10*math.log10(pressureAbs/len(levels))
    
def simpleCRTN(annualAvgTraffic,percentageHeavyVehicles,speed,gradient,surfaceCorrection,receiverDist,angleOfView)::
    
def simpleISO9140():
    


print("Check propigation loss")
print(BS5228_PropigationLoss(100,10))
print("Test Power to Pressure Calculator")
print(OpenSpacePowerToPressure(110,50,"spherical"))
print("Check third octaves")
print(BuildThirdOctave(50,500))
print("Check octaves")
print(BuildOctave(50,500))
print("Check speed of sound")
print(speedOfSound(20))
