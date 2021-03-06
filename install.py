#!/usr/bin/env python
import os
import sys
major=sys.version_info[0]

errors=[]

def error(msg):
	errors.append(msg)

def sub(cmd,ignore_errors=False):
	if os.system(cmd) != 0:
		if not ignore_errors:
			errors.append("Command failed: %s"%cmd)
		return False
	else:
		return True

print("Checking Python version...")
if major != 2:
	error("Teaser currently requires Python 2! Version: %s"%str(sys.version_info))

print("Installing Python package dependencies...")


sub("pip2 install --user intervaltree",True)
sub("pip2 install --user tornado",True)
sub("pip2 install --user pyaml",True)
sub("pip2 install --user psutil",True)

sub("pip install --user intervaltree")
sub("pip install --user tornado")
sub("pip install --user pyaml")
sub("pip install --user psutil")

print("Downloading software packages (Mappers and Simulators)...")
sub("wget http://www.cibiv.at/software/teaser/teaser_software.tar.gz")
sub("tar -xvzf teaser_software.tar.gz")

print("Downloading example reference genome (E. coli)...")
os.chdir("references")
sub("wget http://www.cibiv.at/software/teaser/E_coli.fasta")
os.chdir("..")

print("Building BWA...")
os.chdir("software/bwa_build")
bwa_build_success=sub("make")
os.chdir("..")
if bwa_build_success:
	sub("mv bwa bwa_prebuilt")
	sub("cp bwa_build/bwa bwa")
os.chdir("..")

print("Building NGM...")
os.chdir("software/ngm_build")
sub("mkdir -p build/release")
os.chdir("build/release")
sub("cmake -DCMAKE_BUILD_TYPE=Release ../..")
sub("make")
os.chdir("../../../")
sub("cp -R ngm_build/bin/ngm-0.4.13/* ngm")
os.chdir("..")

print("Building DWGSIM...")
os.chdir("software/dwgsim_build")
dwgsim_build_success=sub("make")
os.chdir("..")
if dwgsim_build_success:
	sub("mv dwgsim dwgsim_prebuilt")
	sub("cp dwgsim_build/dwgsim dwgsim")
os.chdir("..")

sub("rm teaser_software.tar.gz")


print("Building tools...")
os.chdir("tools")
tool_build_success=sub("g++ fastindex.cpp -O3 -o fastindex_build")
if tool_build_success:
	sub("mv fastindex_build fastindex")
os.chdir("..")

if len(errors)==0:
	print("Installation completed successfully!")
else:
	print("Errors occured during installation:")
	for msg in errors:
		print("\t%s"%msg)
