import argparse
from zipfile import *
from shutil import make_archive
import json
import os
from pathlib import Path

parser = argparse.ArgumentParser(description='Make mods support 1.18.')
parser.add_argument('path', metavar='PATH', type=str, nargs='+',
					help='the path to the .jar')
args = parser.parse_args()
paths = args.path

for path in paths:
	#Unzip
	mod_name = (path.split("/")[-1]).split(".jar")[0]
	res_folder = f"tmp/{mod_name}"
	with ZipFile(path) as zip: 
		zip.extractall(res_folder)
	
	#Edit
	fabric_mod_file_dir = res_folder + "/fabric.mod.json"
	fabric_mod_json = ""
	with open(fabric_mod_file_dir, "r") as file:
		fabric_mod_json = json.loads(file.read())
		fabric_mod_json["depends"]["minecraft"].append("~1.18")
	
	with open(fabric_mod_file_dir, "w") as file:
		file.write(json.dumps(fabric_mod_json))
		file.close()
	
	#Zip it back
	make_archive(mod_name, 'zip', root_dir=res_folder, base_dir=None)
	os.rename(mod_name + ".zip", mod_name + ".jar")
	Path(mod_name + ".jar").rename("output/" + mod_name + ".jar")