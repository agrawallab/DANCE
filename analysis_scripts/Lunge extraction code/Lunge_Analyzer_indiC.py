import os
import shutil
import csv
import os
import glob
import numpy
import matlab.engine

while True:
	#Renaming_scorefiles
	def rename_files_recursively(root_path):
		score_folder = "score_files"
		new_path = os.path.join(root_path, score_folder)
		try:
			os.mkdir(new_path)
			print("score_files folder created")
		except:
			print("score_files folder already exists")
		for upperdir in os.listdir(root_path):
			upperdir_path = os.path.join(root_path, upperdir)
			new_folder = os.path.join(root_path + str("/") + "score_files" + str("/") + upperdir)
			if not upperdir == "score_files":
				try:
					os.mkdir(new_folder)
				except:
					print( new_folder + " folder already exists in score_files folder")
			for dir in os.listdir(upperdir_path):
				dir_path = os.path.join(upperdir_path, dir)
				if os.path.isdir(dir_path):
					for subdir in os.listdir(dir_path):
						subdir_path = os.path.join(dir_path, subdir)
						if os.path.isdir(subdir_path):
							for folder in os.listdir(subdir_path):
								folder_path = os.path.join(subdir_path, folder)
								if os.path.isdir(folder_path):
									for file in os.listdir(folder_path):
										file_path = os.path.join(folder_path, file)
										name, extension = os.path.splitext(file)
										if "Lunge" in name:
											new_name = os.path.join(root_path + str("/") + "score_files" + str("/") + upperdir + str("/") + dir + "_" + name + extension)
											# os.rename(file_path, new_name)
											print (new_name)
											shutil.copy(file_path, new_name)
											continue

		print(f"Score files were renamed and copied to {root_path}")

	root_path = input(r"What is the complete path of the parent folder containing all videos and JAABA folders?")
	if __name__ == "__main__":
		rename_files_recursively(root_path)

	#Extracting lunge frames data from mat score files to csv
	os.chdir(os.path.join(root_path, "score_files"))
	for upperdir in os.listdir(root_path + str("/") + "score_files"):
		if os.path.isdir(root_path + str("/") + "score_files" + str("/") + upperdir):
			os.chdir(os.path.join(root_path + str("/") + "score_files" + str("/") + upperdir))
			eng = matlab.engine.start_matlab()
			eng.SheetMaker(nargout=0)
			eng.quit()

	#Lunge counting and compiling into single csv sheet 
	path = root_path + str("/") + "score_files"
	extension = 'csv'
	os.chdir(path)
	for directory in os.listdir(path):
		directory_path = os.path.join(path, directory)
		if os.path.isdir(directory_path):
			os.chdir(directory_path)
			filenames = glob.glob('*.{}'.format(extension))
			print(filenames)
			new_filename = directory + ".csv"
			max=0
			norows = 0
			rows = []
			for file in filenames:
				filename = str(file)
				# reading csv file
				with open(filename, 'r') as csvfile: 
					# creating a csv reader object
					csvreader = csv.reader(csvfile)
					# extracting each data row one by one
					for row in csvreader:
						norows += 1
						if max <= len(row):
							max = len(row)
						rows.append(row)
					# get total number of rows
					#print("Total no. of rows: %d" % (csvreader.line_num)
			print(rows)
			for i in range(0,max):
				for j in range (0, norows):
					print (j,i)
					try:
						rows[j][i]
					except:
						rows[j].append("NaN")
						print (rows[j][i])
			os.chdir(path)
			with open(new_filename, 'w', newline="") as csvfile:
				csvwriter = csv.writer(csvfile)
				csvwriter.writerows(rows)

			continue

	
	#Lunge counting and compiling into single csv sheet 
	path = root_path + str("/") + "score_files"
	extension = 'csv'
	os.chdir(path)
	filenames = glob.glob('*.{}'.format(extension))
	print(filenames)
	new_filename = "compiled.csv"
	new_rows = []
	for file in filenames:
		filename = str(file)
		rows = []
		# reading csv file
		with open(filename, 'r') as csvfile: 
			# creating a csv reader object
			csvreader = csv.reader(csvfile)
			# extracting each data row one by one
			for row in csvreader:
				rows.append(row)
			# get total number of rows
			#print("Total no. of rows: %d" % (csvreader.line_num))
		new_row = [str(filename)]

		for n in range(0,len(rows),2):
			lunges = 0
			for col in rows[n]:
				if col != "NaN":
						lunges = lunges + 1
			for col in rows[n+1]:
				if col != "NaN":
						lunges = lunges + 1
			new_row.append(lunges)   

		new_rows.append(new_row)

	with open(new_filename, 'w', newline="") as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerows(new_rows)

	continue

