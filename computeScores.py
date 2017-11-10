'''
Bloom filter templates score computation for a given database and a specific protocol.
More details on the Bloom filter based BTP scheme in:

[IF18] M. Gomez-Barrero, C. Rathgeb, G. Li, R. Raghavendra, J. Galbally and C. Busch
        "Multi-Biometric Template Protection Based on Bloom Filters", in Information Fusion, vol. 42, pp. 37-50, 2018.

Please remember to reference article [IF18] on any work made public, whatever the form,
based directly or indirectly on these metrics.
'''

__author__ = "Marta Gomez-Barrero"
__copyright__ = "Copyright (C) 2017 Hochschule Darmstadt"
__license__ = "License Agreement provided by Hochschule Darmstadt (https://share.nbl.nislab.no/g03-06-btp/multibiometric-bf-btp/blob/master/hda-license.pdf)"
__version__ = "1.0"

import numpy
import math
import os
import argparse

######################################################################
### Parameter and arguments definition

# location of source templates and score files
parser = argparse.ArgumentParser(description='Compute protected Bloom filter scores from a given DB and protocol.')

parser.add_argument('DB_BFtemplates', help='directory where the protected BF templates are stored', type=str)
parser.add_argument('matedComparisonsFile', help='file comprising the mated comparisons to be carried out', type=str)
parser.add_argument('nonMatedComparisonsFile', help='file comprising the non-mated comparisons to be carried out', type=str)
parser.add_argument('--scoresDir', help='directory where unprotected and protected scores will be stored', type=str, nargs='?', default = './scores/')
parser.add_argument('--matedScoresFile', help='file comprising the mated scores computed', type=str, nargs='?', default = 'matedScoresBF.txt')
parser.add_argument('--nonMatedScoresFile', help='file comprising the non-mated scores computed', type=str, nargs='?', default = 'nonMatedScoresBF.txt')

args = parser.parse_args()
DB_BFtemplates = args.DB_BFtemplates
matedComparisonsFile = args.matedComparisonsFile
nonMatedComparisonsFile = args.nonMatedComparisonsFile
scoresDir = args.scoresDir
matedScoresFile = args.matedScoresFile
nonMatedScoresFile = args.nonMatedScoresFile

if not os.path.exists(scoresDir):
    os.mkdir(scoresDir)

####################################################################
### Some auxiliary functions

def hamming_distance(X, Y):
    '''Computes the normalised Hamming distance between two Bloom filter templates'''
    dist = 0

    N_BF = X.shape[0]
    for i in range(N_BF):
        A = X[i, :]
        B = Y[i, :]

        suma = sum(A) + sum(B)
        if suma > 0:
            dist += float(sum(A ^ B)) / float(suma)

    return dist / float(N_BF)

####################################################################
### Score computation

# read protocol files
matedF = open(matedComparisonsFile, 'r')
nonMatedF = open(nonMatedComparisonsFile, 'r')

# pre-allocate score arrays
matedScoresBF = []
nonMatedScoresBF = []

# compute scores for each reference template and save at each iteration
for l in matedF.readlines():
    r = l.split()

    aBF = numpy.loadtxt(DB_BFtemplates + r[0]).astype(int)
    bBF = numpy.loadtxt(DB_BFtemplates + r[1]).astype(int)
    matedScoresBF.append(hamming_distance(aBF, bBF))

for l in nonMatedF.readlines():
    r = l.split()

    aBF = numpy.loadtxt(DB_BFtemplates + r[0]).astype(int)
    bBF = numpy.loadtxt(DB_BFtemplates + r[1]).astype(int)
    nonMatedScoresBF.append(hamming_distance(aBF, bBF))

numpy.savetxt(scoresDir+matedScoresFile, matedScoresBF)
numpy.savetxt(scoresDir+nonMatedScoresFile, nonMatedScoresBF)
