'''
Implementation of the Bloom filter based biometric template protection for iris images. More details in:

[IF18] M. Gomez-Barrero, C. Rathgeb, G. Li, R. Raghavendra, J. Galbally and C. Busch
        "Multi-Biometric Template Protection Based on Bloom Filters", in Information Fusion, vol. 42, pp. 37-50, 2018.

Please remember to reference article and [IF18] on any work made public, whatever the form,
based directly or indirectly on these metrics.
'''

__author__ = "Marta Gomez-Barrero"
__copyright__ = "Copyright (C) 2017 Hochschule Darmstadt"
__license__ = "License Agreement provided by Hochschule Darmstadt (https://github.com/dasec/multibiometric-bf-btp/blob/master/hda-license.pdf)"
__version__ = "1.0"

import numpy
import argparse
import os

######################################################################
### Parameter and arguments definition

parser = argparse.ArgumentParser(description='Extract unprotected LGBPHS and protected Bloom filter templates from the FERET DB.')

# location of source images, final templates and intermediate steps (the latter for debugging purposes)
parser.add_argument('DB_BFtemplatesA', help='directory where the protected BF templates for characteristic A are stored', type=str)
parser.add_argument('DB_BFtemplatesB', help='directory where the protected BF templates for characteristic B are stored', type=str)
parser.add_argument('fusionList', help='file where the pairs of templates to be fused are specified', type=str)
parser.add_argument('--DB_BFtemplates_fused', help='directory where the protected fused BF templates will be stored', type=str, nargs='?', default = './BFtemplates_fused/')

args = parser.parse_args()
DB_BFtemplatesA = args.DB_BFtemplatesA
DB_BFtemplatesB = args.DB_BFtemplatesB
fusionList = args.fusionList
DB_BFtemplates_fused = args.DB_BFtemplates_fused

if not os.path.exists(DB_BFtemplates_fused):
    os.mkdir(DB_BFtemplates_fused)

## Some parameters of the BF templates
N_BF_A = 32 # iris in the example
BF_SIZE_A = 1024
N_BF_B = 32*3*10 # face in the example
BF_SIZE_B = 16


####################################################################
### Some auxiliary functions

def fuse_BF_templates(BFtempA, BFtempB, pos):
    '''Fuses tempA and tempB according to the position vector pos'''

    assert N_BF_A == BFtempA.shape[0], 'Dimensions from template A do not match: wrong number of Bloom filters'
    assert BF_SIZE_A == BFtempA.shape[1], 'Dimensions from template A do not match: wrong Bloom filter size'
    assert N_BF_B == BFtempB.shape[0], 'Dimensions from template B do not match: wrong number of Bloom filters'
    assert BF_SIZE_B == BFtempB.shape[1], 'Dimensions from template B do not match: wrong Bloom filter size'

    temp = BFtempA

    index = 0
    for p in pos:
        temp[p[0], p[1] : p[1] + BF_SIZE_B] = numpy.bitwise_or(temp[p[0], p[1] : p[1] + BF_SIZE_B], BFtempB[index, :])
        index += 1

    return temp

####################################################################
### Template fusion

# define position vector for the fusion
pos = numpy.zeros([2, N_BF_B], dtype=int)
ratio = N_BF_B / N_BF_A

for i in range(N_BF_A):
    pos[0, i * ratio: (i+1)*ratio] = i * numpy.ones([1, ratio])            # BF where it will be allocated (we ensure equal number of BFs of B fused per BF of A)
    pos[1, i * ratio: (i+1)*ratio] = range(0, BF_SIZE_B*ratio, BF_SIZE_B)  # position within the BF

index = 1
f = open(fusionList, 'r')
for filenames in f.readlines():
    print(filenames)

    r = filenames.split()
    tempA = numpy.loadtxt(DB_BFtemplatesA + r[0]).astype(int)
    tempB = numpy.loadtxt(DB_BFtemplatesB + r[1]).astype(int)
    bfs = fuse_BF_templates(tempA, tempB, pos)
    numpy.savetxt(DB_BFtemplates_fused + str(index) + '_BFtemplate.txt', bfs, fmt='%d')

    index += 1
