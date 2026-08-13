import os
import shutil
import csv
import os
import glob
import numpy
import scipy.io
import numpy as np

def sheet_maker(folder_path):
	"""Reads JAABA .mat score files in folder_path and writes one CSV per .mat file.
	Row 0 = fly1 bout frame numbers, row 1 = fly2 bout frame numbers (columns).
	Uses allScores.scores > 0 to find bout frames, offset by tStart."""
	for mat_file in glob.glob(os.path.join(folder_path, '*.mat')):
		base_name = os.path.splitext(os.path.basename(mat_file))[0]
		out_csv = os.path.join(folder_path, base_name + ".csv")
		try:
			data = scipy.io.loadmat(mat_file, squeeze_me=True, struct_as_record=False)
			all_scores = data['allScores']
			if hasattr(all_scores, 'scores') and hasattr(all_scores, 'tStart'):
				t_start = np.atleast_1d(all_scores.tStart)
				with open(out_csv, 'w', newline='') as f:
					writer = csv.writer(f)
					for fly_idx in range(2):
						fly_scores = np.atleast_1d(all_scores.scores[fly_idx]).flatten()
						bout_frames = (np.where(fly_scores > 0)[0] + int(t_start[fly_idx])).tolist()
						writer.writerow(bout_frames)
			else:
				print(f"File {mat_file} does not contain expected fields: scores or tStart")
		except NotImplementedError:
			print(f"File {mat_file} is MATLAB v7.3 (HDF5) format — install h5py to read it")
		except Exception as e:
			print(f"Error processing file {mat_file}: {e}")


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
			if upperdir.startswith('.'):
				continue
			upperdir_path = os.path.join(root_path, upperdir)
			new_folder = os.path.join(root_path + str("/") + "score_files" + str("/") + upperdir)
			if not upperdir == "score_files":
				try:
					os.mkdir(new_folder)
				except:
					print( new_folder + " folder already exists in score_files folder")
			for file in os.listdir(upperdir_path):
				if file.startswith('.'):
					continue
				file_path = os.path.join(upperdir_path, file)
				if os.path.isfile(file_path):
					name, extension = os.path.splitext(file)
					if "Lunge" in name:
						new_name = os.path.join(new_path, upperdir, upperdir + "_" + name + extension)
						print(new_name)
						shutil.copy(file_path, new_name)

		print(f"Score files were renamed and copied to {root_path}")

	root_path = input(r"What is the complete path of the parent folder containing all videos and JAABA folders?")
	if __name__ == "__main__":
		rename_files_recursively(root_path)

	#Extracting lunge frames data from mat score files to csv
	os.chdir(os.path.join(root_path, "score_files"))
	for upperdir in os.listdir(root_path + str("/") + "score_files"):
		if os.path.isdir(root_path + str("/") + "score_files" + str("/") + upperdir):
			os.chdir(os.path.join(root_path + str("/") + "score_files" + str("/") + upperdir))
			sheet_maker(os.path.join(root_path, "score_files", upperdir))

	#Lunge counting and compiling into single csv sheet 
	path = root_path + str("/") + "score_files"
	extension = 'csv'
	os.chdir(path)
	for directory in os.listdir(path):
		directory_path = os.path.join(path, directory)
		if os.path.isdir(directory_path):
			os.chdir(directory_path)
			filenames = glob.glob('*.{}'.format(extension))
			filenames = [f for f in filenames if not f.endswith('_Fly1.csv') and not f.endswith('_Fly2.csv')]
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
	filenames = [f for f in filenames if not f.endswith('_Fly1.csv') and not f.endswith('_Fly2.csv')]
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
			if n+1 < len(rows):
				for col in rows[n+1]:
					if col != "NaN":
							lunges = lunges + 1
			new_row.append(lunges)   

		new_rows.append(new_row)

	with open(new_filename, 'w', newline="") as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerows(new_rows)

	continue

