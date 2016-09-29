import timeit

# This is almost certainly premature optimization, but hey, I was curious.

setup = '''import numpy as np
from numpy.linalg import slogdet, det, matrix_rank
from scipy import linalg
matrix = np.array([[-1.626155973110368, -1.5823159378605818, -0.03176405753823852, -0.5177135004548361, -1.7070685949235997],
 [-1.131783510557717, -1.1434647220154712, -1.0336283163134605, -1.957908079059242, -0.6887508890000416],
 [-1.7512746251012603, -1.11085839218418, -0.8172346596309343, -0.8889898313165916, -1.2057710493735698],
 [-0.12494369588114784, -1.770702124769635, -0.45733433266176227, -0.8277486924562267, -0.6842054764082699],
 [-0.23052852039452243, -1.1574487035953767, -1.562842787047289, -0.6191529117512236, -0.5327481101266072]])'''
def main():

    #slogdet_test = timeit.timeit(setup=setup, stmt='slogdet(matrix)')
    #print('slogdet: {}'.format(slogdet_test))
    #det_test = timeit.timeit(setup=setup, stmt='det(matrix)')
    #print('det: {}'.format(det_test))
    #rank_test = timeit.timeit(setup=setup,
    #                          stmt='matrix_rank(matrix)')
    #print('matrix_rank: {}'.format(rank_test)) # takes 60 seconds!
    return (slogdet_test, det_test)
