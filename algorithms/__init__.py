#   
#   Algorithms lib. Make sure we're using this one and not some overlapping lib.
#   

from algorithms.naive import NaiveAlgorithm
from algorithms.annoyingset import AnnoyingSetAlgorithm
from algorithms.annoyingset_levavs_try import AnnoyingSetAlgorithmLevavsTry

get_loaded = [
    NaiveAlgorithm,
    AnnoyingSetAlgorithm,
    AnnoyingSetAlgorithmLevavsTry
]
