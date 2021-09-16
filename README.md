LLFI-GPU for Rodinia
====

LLFI-GPU for Rodinia use LLFI-GPU to injection faults into the LLVM IR of the Rodinia source code of GPU CUDA kernels. For more information of Rodinia please refer to the [Rodinia Benchmark Suit](https://github.com/JuliaParallel/rodinia).


LLFI-GPU
====
LLFI-GPU is an LLVM based fault injection tool, that injects faults into the LLVM IR of the application source code of GPU CUDA kernels.  The faults can be injected into specific program points, and the effect can be easily tracked back to the source code.  LLFI-GPU is typically used to map fault characteristics back to source code, and hence understand source level or program characteristics for various kinds of fault outcomes. For more information of Rodinia please refer to the [LLFI-GPU](https://github.com/DependableSystemsLab/LLFI-GPU).



INSTALLATION
===

Dependencies (Tested):

1. Python 2.7
2. NVCC v6.5
3. CUDA SDK v6.5.16 
4. LLVM 3.4
5. Ubuntu 14.04 LTS x64

1. Modify 'makeCommands'to compile target benchmark in profile.py and inject.py. Put benchmark input in 'inputParameters'.
2. Configure fault injection parameters in '# FI Config' section in profile.py and inject.py.
3. Add headers in target benchmark source code. This is shown in line 9-17 in example.cu. Label GPU kernel calls so that you can trace it. This is added in line 124 and 126 in exmple.cu.

That's it. Run "python profile.py" and "python inject.py" to start fault injections. All fault injection logs and IR files are located under folder called 'bamboo_fi'.

An example of the command line output by running the above scripts can be found in example.output

We tested on NVIDIA K20 and GTX960 GPUs.

Have fun!


PAPER
===
[Understanding Error Propagation in GPGPU Applications (SC'16)](http://blogs.ubc.ca/karthik/2016/06/20/understanding-error-propagation-in-gpgpu-applications/)


