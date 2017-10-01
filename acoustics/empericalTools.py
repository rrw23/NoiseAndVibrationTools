"""
Created on Sun Oct  1 08:03:39 2017

@author: Robin Wareing

Series of functions to produce emperical sound powers/pressures
Based on Chapter 11 of Engineering Noise Control, Bies & Hansen
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

