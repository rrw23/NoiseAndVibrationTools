# Basic tools to calculate noise information
# Robin Wareing - 22/09/2017

import math

def BS5228_PropigationLoss(receiverDist,sourceDist):
    '''Calculates the propigation loss over a set distance using BS5338-2 method'''
    if receiverDist < 25:
        propigationLoss = 20*math.log10(1.*receiverDist/sourceDist)
    else:
        propigationLoss = 25*math.log10(1.*receiverDist/sourceDist)-2
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

def ThirdOctaveWeightingCurves(weightingType,startFreq,stopFreq):
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
    weightedLevel = []
    if bandType == "1/1":
        weightingCurve = OctaveWeightingCurves("A",freq[0],freq[-1])
    elif bandType == "1/3":
        weightingCurve = ThirdOctaveWeightingCurves("A",freq[0],freq[-1])
    for i in range(len(levels)):
        weightedLevel.append(levels[i] + weightingCurve[1][i])
    return dBadd(weightedLevel)
    
def dBC(levels,freq,bandType):
    weightedLevel = []
    if bandType == "1/1":
        weightingCurve = OctaveWeightingCurves("C",freq[0],freq[-1])
    elif bandType == "1/3":
        weightingCurve = ThirdOctaveWeightingCurves("C",freq[0],freq[-1])
    for i in range(len(levels)):
        weightedLevel.append(levels[i] + weightingCurve[1][i])
    return dBadd(weightedLevel)
    
def dBadd(levels):
    pressureAbs = 0
    for level in levels:
        pressureAbs = pressureAbs + 10**(level/10)
    return 10*math.log10(pressureAbs)
    
def dBavg(levels):
    pressureAbs = 0
    for level in levels:
        pressureAbs = pressureAbs + 10**(level/10)
    return 10*math.log10(pressureAbs/len(levels))
    
def simpleCRTN(annualAvgTraffic,percentageHeavyVehicles,speed,gradient,
               surfaceCorrection,receiverDist,angleOfView):
    ''' Nothing in her yet...'''
    
def simpleISO9140():
    '''Nothin in here yet'''

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
print('Check A-weighting')
print(ThirdOctaveWeightingCurves("A",50,500))
print(OctaveWeightingCurves("A",50,500))
print('Check C-weighting')
print(ThirdOctaveWeightingCurves("C",50,500))
print(OctaveWeightingCurves("C",50,500))
print('Check dBA - 1/3')
print(print(dBA([90,90,90],[50,63,80],"1/3")))
print('Check dBA - 1/1')
print(print(dBA([90,90,90],[63,125,250],"1/1")))
print('Check dBC - 1/3')
print(print(dBC([90,90,90],[50,63,80],"1/3")))
print('Check dBC - 1/1')
print(print(dBC([90,90,90],[63,125,250],"1/1")))
print('Check dBadd')
print(dBadd([90,90]))
print('Check dBavg')
print(dBavg([90,90,90]))
print('Check simple CRTN')
print('-------')
print('Check ISO9140')
print('-------')