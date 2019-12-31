"""
GeneSet MAPR implementation
	main file to run all steps

author: Aamir Hasan & Greg Linkowski
	for KnowEnG by UIUC & NIH
"""

"""WARNING: THIS FILE HAS NOT BEEN TESTED COMPLETELY"""

import argparse
import MAPR_networkPrep as m1
import MAPR_buildFeatures as m2
import MAPR_characterizeSet as m3


################################################################
# ANCILLARY FUNCTION(S)
def readCommandLineFlags():
	"""
	Read command-line arguments & provide documentation using '--help'
	:return:
	"""
	parser = argparse.ArgumentParser()
	
	parser.add_argument('netEdgeFile', type=str,
	                    help='path & file name of network edge file')
	parser.add_argument('-f', '--folds', type=int, default=4,
						help='number of cross-validation folds')
	parser.add_argument('-i', '--ignore', type=str, default='NONE',
	                    help='text file containing list of edge types to ignore')
	parser.add_argument('-k', '--keep', type=str, default='',
	                    help='path & file name of network keep file')
	parser.add_argument('-l', '--length', type=int, default=3,
	                    help='maximum meta-path depth')
	parser.add_argument('-m', '--numModels', type=int, default=101,
	                    help='number of random null sets to use for comparison')
	parser.add_argument('-n', '--networkPath', type=str, default='./networks',
	                    help='output directory to store processed network')
	parser.add_argument('-o', '--output', type=str, default='./output',
						help='output directory to store processed network')
	parser.add_argument('-p', '--plotAUCs', type=bool, default=False,
	                    help='to save plots of AUC curves, set to "True"')
	parser.add_argument('-s', '--sample', type=str, default='samples/',
						help='samples directory')
	parser.add_argument('-t', '--textSubNets', type=bool, default=False,
	                    help='whether to save separate subnetwork text files')
	parser.add_argument('-v', '--verbose', type=int, default=0,
	                    help='enable verbose output to terminal: 0=none, 2=all')
	
	flags = parser.parse_args()
	
	return flags
#end def #################################



################################################################
# MAIN FUNCTION & CALL
def main():
	# Collect arguments from the command line
	params = readCommandLineFlags()
	
	# Run core script 1
	netNameShort = m1.main(params)
	# Run core script 2
	resultsDir = m2.main(params, netNameShort)
	# Run core script 3
	rankedListFile = m3.main(params, resultsDir)
	
	print("\nRanked list of non-input genes for each input set found at: ")
	print("    {}/full-.../{}".format(resultsDir.rstrip('/'), rankedListFile))
	
	return
# end def #################################


if __name__ == "__main__":
	main()
# end if
