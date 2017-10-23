"""
Created on Sun Oct  1 08:03:39 2017

@author: Robin Wareing

Series of functions to produce emperical sound powers/pressures
Based on Chapter 11 of Engineering Noise Control, Bies & Hansen

Vibration based on TRL and NZTA research report 268?
"""
import math

def BladePassFrequency(numBlades,RPM):
    '''Calculates blade pass frequency of a fan'''
    return numBlades*RPM*1./60

def LargeCompressorExt(compressorType,compressorPower):
    '''Calculates the noise emissions of a large compressor.
    Using Eqns. 11.13, 11.14, 11.15
    Compressor types: rotary/reciprocating, centrifugal - casing,
    centrifugal - inlet'''
    if compressorType == "rotary/reciprocating":
        Lw = 90+math.log10(compressorPower)
    elif compressorType == "centrifugal - casing":
        Lw = 79+math.log10(compressorPower)    
    elif compressorType == "centrifugal - inlet":
        Lw = 80+math.log10(compressorPower)
    return Lw

def LargeCompressorExtOctBand(compressorType,compressorPower):
    '''Produces 1/1 octave band compressor noise'''
    Lw = LargeCompressorExt(compressorType,compressorPower)
    if compressorType == "rotary/reciprocating":
        correction = [11,15,10,11,13,10,5,8,15]
    elif compressorType == "centrifugal - casing":
        correction = [10,10,11,13,13,11,7,8,12]
    elif compressorType == "centrifugal - inlet":
        correction = [18,16,14,10,8,6,5,10,16]
    LwBands = []
    for item in correction:
        LwBands.append(Lw-item)
    return LwBands

def CoolingTower(coolingTowerType,coolingTowerPower):
    '''Calculates the noise emissions of a large compressor.
    Using Eqns. 11.16, 11.17, 11.18, 11.19
    Compressor types: propeller, centrifugal'''
    if coolingTowerType == "propeller":
        if coolingTowerPower <= 75:
            Lw = 100+8*math.log10(coolingTowerPower)
        elif coolingTowerPower > 75:
            Lw = 96+10*math.log10(coolingTowerPower)
    elif coolingTowerType == "centrifugal":
        if coolingTowerPower <= 60:
            Lw = 85+11*math.log10(coolingTowerPower)
        elif coolingTowerPower > 60:
            Lw = 93+7*math.log10(coolingTowerPower)
    return Lw

def CoolingTowerOctBand(coolingTowerType,coolingTowerPower):
    '''Produces 1/1 octave band compressor noise'''
    Lw = CoolingTower(coolingTowerType,coolingTowerPower)
    if coolingTowerType == "propeller":
        correction = [8,5,5,8,11,15,18,21,29]
    elif coolingTowerType == "centrifugal":
        correction = [6,6,8,10,11,13,12,18,25]
    LwBands = []
    for item in correction:
        LwBands.append(Lw-item)
    return LwBands

def TunnelingVibration(tunnelDist):
    '''From Table E1 in BS5228-2:2009'''
    return 180./(math.pow(tunnelDist,1.3))

def TunnelingGroundBournNoise(tunnelDist):
    '''From Table E1 in BS5228-2:2009'''
    return 127-54*math.log10(tunnelDist)

def VibroStoneColumns(receiverDist):
    '''From Table E1 in BS5228-2:2009
    Produces a range of vibration levels
    [5%, 33%, 50%]'''
    v5Percent = 95./math.pow(receiverDist)
    v33Percent = 44./math.pow(receiverDist)
    v50Percent = 33./math.pow(receiverDist)
    return [v5Percent,v33Percent,v50Percent]

def BlastionOverpressure(chargeMass,receiverDist,siteCondition):
    if siteCondition == "Unconfined":
        siteConstant = 516
    elif siteCondition == "Confined":
        siteConstant = 100
    overpressure = siteConstant*(receiverDist/(chargeMass**(1/3)))**-1.45
    return overpressure

def AirBlastNoise(chargeMass,receiverDist,siteCondition):
    overpressure = BlastionOverpressure(chargeMass,receiverDist,siteCondition)
    return 20*math.log10(overpressure/0.02)

def VibrationCompaction(runCondition,drumAmplitude,drumNumber,drumWidth,receiverDist):
    if runCondition == "steady-state":
        v5Percent = 75*math.sqrt(drumNumber)*(drumAmplitude/(receiverDist+drumWidth))**1.5
        v33Percent = 143*math.sqrt(drumNumber)*(drumAmplitude/(receiverDist+drumWidth))**1.5
        v50Percent = 276*math.sqrt(drumNumber)*(drumAmplitude/(receiverDist+drumWidth))**1.5
    elif runCondition == "start-up":
        v5Percent = 65*math.sqrt(drumNumber)*((drumAmplitude**1.5)/((receiverDist+drumWidth)**1.3))
        v33Percent = 106*math.sqrt(drumNumber)*((drumAmplitude**1.5)/((receiverDist+drumWidth)**1.3))
        v50Percent = 177*math.sqrt(drumNumber)*((drumAmplitude**1.5)/((receiverDist+drumWidth)**1.3))
    return [v5Percent,v33Percent,v50Percent]

def PercussivePiling(pileDiveCondition,hammerEnergy,receiverDist):
    if pileDiveCondition == "to refusal":
        scalingFactor = 5
    elif pileDiveCondition == "driven through":
        scalingFactor = 3
    elif pileDiveCondition == "not driven through":
        scalingFactor = 1.5
    return scalingFactor*(math.sqrt(hammerEnergy)/(receiverDist**1.3))

def VibroPiling(receiverDist,runCondition):
    if runCondition == "start-up":
        decayFactor = 1.2
    elif runCondition == "steady-state":
        decayFactor = 1.4
    else:
        decayFactor = 1.3
    v5Percent = 60/(receiverDist**decayFactor)
    v33Percent = 126/(receiverDist**decayFactor)
    v50Percent = 266/(receiverDist**decayFactor)
    return [v5Percent,v33Percent,v50Percent]

def DynamicCompaction(receiverDist,damperEnergy):
    return 0.037*(math.sqrt(damperEnergy)/receiverDist)**1.7
