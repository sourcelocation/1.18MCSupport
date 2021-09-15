import argparse
from zipfile import *
from shutil import rmtree
import json
import os
from pathlib import Path
from support import log, make_archive

TMP_FOLDER = Path("tmp")
OUTPUT_FOLDER = Path("output")

def simple_mod_dependency_edit(mod_contents):
	log("Editing " + path + "...")
	fabric_mod_file_dir = os.path.join(mod_contents, "fabric.mod.json")
	fabric_mod_json = ""
	with open(fabric_mod_file_dir, "r") as file:
		fabric_mod_json = json.loads(file.read())
		fabric_mod_json["depends"]["minecraft"] = ["~1.16","~1.17","~1.18"]
		
	with open(fabric_mod_file_dir, "w") as file:
		file.write(json.dumps(fabric_mod_json))
		file.close()

def preparation():
	if not os.path.exists("tmp"):
		os.makedirs("tmp")
	if not os.path.exists("output"):
		os.makedirs("output")

def parse_paths():
	parser = argparse.ArgumentParser(description='Make mods support 1.18.')
	parser.add_argument('path', metavar='PATH', type=str, nargs='+',
						help='the path to the .jar or folder of jars')
	args = parser.parse_args()
	passed_path = args.path[0]
	paths = []
	if passed_path.split("/")[-1].count(".jar") == 0:
		# Passed a folder
		paths = os.listdir(passed_path)
		if ".DS_Store" in paths:
			paths.remove(".DS_Store")
		for i,path in enumerate(paths):
			paths[i] = os.path.join(passed_path, path)
	else:
		paths = [passed_path]
	
	return paths


preparation()
paths = parse_paths()
for path in paths:
	log("Unzipping " + path + "...")
	#Unzip
	mod_name = (path.split("/")[-1]).split(".jar")[0]
	mod_contents = os.path.join(TMP_FOLDER, mod_name)
	with ZipFile(path) as zip: 
		zip.extractall(mod_contents)
	
	#Edit
	simple_mod_dependency_edit(mod_contents)
	
	#Zip it back
	log("Zipping " + path + "...")
	make_archive(mod_contents, os.path.join(OUTPUT_FOLDER, mod_name + ".zip"))
	os.rename(os.path.join(OUTPUT_FOLDER,mod_name + ".zip"), os.path.join(OUTPUT_FOLDER,mod_name + "_1.18.jar"))
	
log("Cleaning up...")
rmtree("tmp")