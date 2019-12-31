"""
GeneSet MAPR implementation
	main file to run all steps

author: Aamir Hasan
	for KnowEnG by UIUC & NIH
"""

"""WARNING: THIS FILE HAS NOT BEEN TESTED COMPLETELY"""

import subprocess
import argparse
import sys
import MAPR_networkPrep as m1


PYTHON_VERSION = 'python' #TODO: this may vary depending on user's python installation


def readCommandLineFlags():
	parser = argparse.ArgumentParser()
	
	parser.add_argument('netEdgeFile', type=str,
	                    help='path & file name of network edge file')
	parser.add_argument('-k', '--keep', type=str, default='',
	                    help='path & file name of network keep file')
	parser.add_argument('-i', '--ignore', type=str, default='NONE',
	                    help='text file containing list of edge types to ignore')
	parser.add_argument('-l', '--length', type=int, default=3,
	                    help='maximum meta-path depth')
	parser.add_argument('-m', '--numModels', type=int, default=101,
	                    help='number of random null sets to use for comparison')
	parser.add_argument('-n', '--networkPath', type=str, default='./networks',
	                    help='output directory to store processed network')
	parser.add_argument('-o', '--output', type=str, default='./output',
						help='output directory to store processed network')
	parser.add_argument('-s', '--subnets', type=bool, default=False,
	                    help='whether to save separate subnetwork txt files')
	parser.add_argument('-v', '--verbose', type=int, default=0,
	                    help='enable verbose output to terminal: 0=none, 2=all')
	
	flags = parser.parse_args()
	
	return flags
	
def m1_main(fnEdge, fnKeep, maxMPLen, netPath, flagSaveSubNet, verbosity):
	"""
	This function copy/pasted from MAPR_networkPrep
	The command-line arguments are converted into function parameters
	
	:param fnEdge: params.netEdgeFile
	:param fnKeep: params.keep
	:param maxMPLen: params.length
	:param netPath: params.networkPath
	:param flagSaveSubNet: params.subnets
	:param verbosity: params.verbose
	:return: netName, str: short name of processed network
	"""
	
	# Upper bound on meta-path length to calculate (hard-coded)
	maxMPLen_UB = 3
	maxMPLen = min(maxMPLen, maxMPLen_UB)
	
	# Assign a name to the network
	fnEVect = fnEdge.split('/')
	netName = fnEVect[-1]
	if netName.endswith('.edge.txt'):
		netName = netName[0:-9]
	
	# Verify edge file exists
	fnEdge = m1.stripQuotesFromString(fnEdge)
	m1.verifyFile(fnEdge, True)
	
	# Check for keep file
	fnKeep = m1.stripQuotesFromString(fnKeep)
	if fnKeep:
		keepExists = m1.verifyFile(fnKeep, False)
	else:
		for i in range(len(fnEVect) - 1):
			fnKeep = fnKeep + fnEVect[i] + '/'
		fnKeep = fnKeep + netName + '.keep.txt'
		keepExists = m1.verifyFile(fnKeep, False)
	# end if
	
	netPath = m1.stripQuotesFromString(netPath)
	netPath = netPath.rstrip('/') + '/'
	
	##########################################
	# build the basic network files from provided edge list
	#   two methods: one uses keep file to specify network
	#       other assumes complete edge file
	if keepExists:
		m1.buildNetworkUsingKeep(fnEdge, fnKeep, netPath, netName, verbosity)
	else:
		# buildNetworkWithoutKeep(fnEdge, netPath, verbosity)
		print("This part coming soon ...")
	# end if
	
	##########################################
	# create primary adjacency matrices
	m1.createPrimaryMatrices(netPath, netName, flagSaveSubNet, verbosity)
	
	##########################################
	# create meta-path matrices
	m1.createMetaPathMatrices(netPath, netName, maxMPLen, verbosity)
	
	return netName


def runTerminalCommand(arguments):
	try:
		result = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		stdout, stderr = result.communicate()

		print(stdout.decode('utf-8'))
	except OSError:
		print("Invalid command:", arguments)


def main():

	# Collect parameters from the command line
	params = readCommandLineFlags()
	
	########################################### STEP ONE ###########################################
	
	#### OPTION 1 : call core script MAPR_networkPrep.py from command line
	#               Issue: the beginning of string may change per user (ie: 'python' vs 'python3'

	# networkPrepQuery = [PYTHON_VERSION, 'MAPR_networkPrep.py', params.netEdgeFile,
	# 					'-k', params.keep, '-l', str(params.length), '-v', str(params.verbose), '-n', params.networkPath, '-s', str(params.subnets)]
	# runTerminalCommand(networkPrepQuery)
	#
	# print('OPTION 1 complete')
	
	#### OPTION 2: import core script as a library
	#               I tried this two ways
	#               First, copy/paste main from core into this (above) and change arguments into function call params
	#                   This worked
	#               Second, just call main directly from core script.
	#                   Since the arguments are the same, no changes necessary
	#                   This also worked
	#  I recommend this last option
	
	# netNameShort =  m1_main(params.netEdgeFile, params.keep,  params.length, params.networkPath, params.subnets, params.verbose)
	netNameShort = m1.main()
	###############################################################################################

	sys.exit()
	
	########################################### STEP TWO ###########################################
	# Setting up arguments for buildFeatures
	networkName = 'test_small'
	outputDirectory = 'test_small/'
	samplesDirectory = './samples/test_small/'

	buildFeaturesQuery = [PYTHON_VERSION, 'MAPR_buildFeatures.py', networkName, '-o', outputDirectory, '-s',
						  samplesDirectory, '-v', str(verbose)]
	#runTerminalCommand(buildFeaturesQuery)
	###############################################################################################

	########################################## STEP THREE #########################################
	setsRoot = "./output/test_small_0000/char01-batch-000/"
	outputDir = "../output"

	characterizeSetQuery = [PYTHON_VERSION, 'MAPR_characterizeSet.py', setsRoot, '-o', outputDir, '-v', str(verbose),
						  '-l', str(length)]
	runTerminalCommand(characterizeSetQuery)

if __name__ == "__main__":
	main()
