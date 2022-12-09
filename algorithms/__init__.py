#   
#   Algorithms lib. Make sure we're using this one and not some overlapping lib.
#   

from algorithms.naive       import NaiveAlgorithm
from algorithms.treesearch  import TreeSearchAlgorithm

get_loaded =    [
                NaiveAlgorithm, 
                TreeSearchAlgorithm
                ]