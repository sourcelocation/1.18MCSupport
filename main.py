import argparse
from zipfile import *
from shutil import make_archive, rmtree
import json
import os
from pathlib import Path
from support import log

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
		paths[i] = passed_path + "/" + path
else:
	paths = [passed_path]

if not os.path.exists("tmp"):
	os.makedirs("tmp")

for path in paths:
	log("Unzipping " + path + "...")
	#Unzip
	mod_name = (path.split("/")[-1]).split(".jar")[0]
	res_folder = f"tmp/{mod_name}"
	with ZipFile(path) as zip: 
		zip.extractall(res_folder)
	
	#Edit
	log("Editing " + path + "...")
	fabric_mod_file_dir = res_folder + "/fabric.mod.json"
	fabric_mod_json = ""
	with open(fabric_mod_file_dir, "r") as file:
		fabric_mod_json = json.loads(file.read())
		fabric_mod_json["depends"]["minecraft"] = ["~1.16","~1.17","~1.18"]
	
	with open(fabric_mod_file_dir, "w") as file:
		file.write(json.dumps(fabric_mod_json))
		file.close()
	
	#Zip it back
	log("Zipping " + path + "...")
	make_archive(mod_name, 'zip', root_dir=res_folder, base_dir=None)
	log("Moving " + path + "to 'output/'")
	os.rename(mod_name + ".zip", mod_name + ".jar")
	Path(mod_name + ".jar").rename("output/" + mod_name + ".jar")
	
log("Cleaning up...")
rmtree("tmp")
