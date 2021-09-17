#! /usr/bin/python

import sys, os, subprocess

#############################################################################
# Env Config
NVCC_PATH = "/usr/local/cuda/bin/nvcc"
ROOT_PATH = "/root/Rodinia-LLFI-GPU"
RODINIA_CUDA_LIB_PATH = ROOT_PATH + "/rodinia/common/cuda"
RODINIA_SOURCE_PATH = ROOT_PATH + "/rodinia/cuda/kmeans"
DATA_PATH = ROOT_PATH + "/rodinia/data/kmeans"
PROGRAM_NAME = "kmeans_cuda"
SOURCE_CODE_LIST = "/kmeans_cuda.cu"
GEN_OBJECT_LIST = "kmeans_cuda.o"
DATA_LIST =DATA_PATH + "/100" # example data: 100, 204800txt, 819200.txt kdd_cup

#############################################################################
# FI Config
staticInstIndex = "" # fiInstIndex=20 or ""
staticKernelIndex = "" # 5 or ""
dynamicKernelIndex = "" # 3 or ""
bitIndex = "" # 63 or ""	
#############################################################################
#flagHeader = staticInstIndex + " CICC_MODIFY_OPT_MODULE=1 LD_PRELOAD=./libnvcc.so nvcc -arch=sm_30 -rdc=true -dc -g -G -Xptxas -O0 -D BAMBOO_PROFILING"
flagHeader = staticInstIndex + "CICC_MODIFY_OPT_MODULE=1 LD_PRELOAD=./libnvcc.so \
    	/usr/local/cuda/bin/nvcc -isystem /usr/include -isystem "+ RODINIA_CUDA_LIB_PATH + \
        " -arch=sm_30 -rdc=true -dc -g -G -Xptxas -O0 -D BAMBOO_PROFILING \
        --generate-line-info -Xcompiler \
        -lnvToolsExt -lcuda -lnvToolsExt "
ktraceFlag = " -D KERNELTRACE"
linkFlags = ""
optFlags = ""
#############################################################################
makeCommand1 = "cc -O2 -isystem /usr/include -isystem " + RODINIA_CUDA_LIB_PATH + " -c -o " + RODINIA_SOURCE_PATH + "/cluster.o " + RODINIA_SOURCE_PATH + "/cluster.c"
makeCommand2 = "cc -O2 -isystem /usr/include -isystem " + RODINIA_CUDA_LIB_PATH + " -c -o " + RODINIA_SOURCE_PATH + "/kmeans.o " + RODINIA_SOURCE_PATH + "/kmeans.c"
makeCommand3 = "cc -O2 -isystem /usr/include -isystem " + RODINIA_CUDA_LIB_PATH + " -c -o " + RODINIA_SOURCE_PATH + "/kmeans_clustering.o " + RODINIA_SOURCE_PATH + "/kmeans_clustering.c"
makeCommand4 = "cc -O2 -isystem /usr/include -isystem " + RODINIA_CUDA_LIB_PATH + " -c -o " + RODINIA_SOURCE_PATH + "/rmse.o " + RODINIA_SOURCE_PATH + "/rmse.c"
makeCommand5 = flagHeader + RODINIA_SOURCE_PATH + SOURCE_CODE_LIST + " -o " + GEN_OBJECT_LIST + ktraceFlag
# makeCommand5 = "CICC_MODIFY_OPT_MODULE=1 LD_PRELOAD=./libnvcc.so     	/usr/local/cuda/bin/nvcc -isystem /usr/include -isystem /root/Rodinia-LLFI-GPU/rodinia/common/cuda -arch=sm_30 -rdc=true -dc -g -G -Xptxas -O0 -D BAMBOO_PROFILING         --generate-line-info -Xcompiler         -lnvToolsExt -lcuda -lnvToolsExt /root/Rodinia-LLFI-GPU/rodinia/cuda/kmeans/kmeans_cuda.cu -o kmeans_cuda.o -D KERNELTRACE"

linkList = " " + PROGRAM_NAME + ".o "  + RODINIA_SOURCE_PATH + "/cluster.o " + RODINIA_SOURCE_PATH + "/kmeans.o " + RODINIA_SOURCE_PATH + "/kmeans_clustering.o " + RODINIA_SOURCE_PATH + "/rmse.o " + "profiling_runtime.o "
outputExeFile = PROGRAM_NAME+ ".out"
############################################################################
bmName = PROGRAM_NAME
inputParameters = " -i " + DATA_LIST
#############################################################################


def runProfile():
	# 	# Prepare lib and files
	# 	# TODO: mkdir for bamboo_fi and baboo_lib
	originalFileList = os.listdir("/")
	os.system("mkdir bamboo_fi")
	os.system("mkdir bamboo_fi/baseline")
	os.system("cp " + ROOT_PATH + "/bamboo_lib/profiling_lib/* .")

	# Compile to profiling pass and pathfinder program
	print ("***[GPGPU-BAMBOO]*** Generating Profiling Pass ... ")
	os.system(makeCommand1)
	print(makeCommand1)
	os.system(makeCommand2)
	print(makeCommand2)
	os.system(makeCommand3)
	print(makeCommand3)
	os.system(makeCommand4)
	print(makeCommand4)
	os.system(makeCommand5)
	print(makeCommand5)
	os.system(NVCC_PATH + " -arch=sm_30 profiling_runtime.cu -c -dc -O0 -o profiling_runtime.o")
	linkCommand = NVCC_PATH + " -Xcompiler -lnvToolsExt -lcuda -lnvToolsExt  -arch=sm_30 " + linkList + " -o " + outputExeFile + " -O0 " + linkFlags
	os.system(linkCommand)

	# Run profiling pass and dump bamboo.profile.txt
	print ("***[GPGPU-BAMBOO]*** Generating Profiling Traces ... ")
	os.system("rm bamboo.profile.txt > /dev/null 2>&1")
	
	goldenOutput = subprocess.check_output("./" +outputExeFile+ " " + inputParameters, shell=True)
	print goldenOutput
	goldenOutputFile = open("bamboo_fi/baseline/golden_output", "w")
	goldenOutputFile.write(goldenOutput)
	goldenOutputFile.close()
	
	# Clean obj files
	os.system("rm bamboo_profiling.cu profiling_runtime.o profiling_runtime.cu " + linkList + " libcicc.so libnvcc.so " + outputExeFile)
	
	# TODO: Move output files to bamboo_fi
	os.system("mv bamboo.profile.txt bamboo_fi/")
	os.system("mv opt_bamboo_before.ll bamboo_fi/" +bmName+ "_kernels.ll")
	os.system("mv opt_bamboo_after.ll bamboo_fi/" +bmName+ "_profile.ll")

	updatedFileList = os.listdir("/")
	newFileList = set(updatedFileList).difference(originalFileList)
	for newFileName in newFileList:
		if newFileName != "bamboo_fi":
			os.system("mv " + newFileName + " bamboo_fi/baseline")

	print ("***[GPGPU-BAMBOO]*** Done! ")




def main():
	runProfile();


##############################################################################
main()
			
	
	


