import argparse
import subprocess
import cv2
import pdb
import os
import tempfile
import numpy as np
from random import randint
from Levenshtein import distance as lev
import pdb
from utils.image_proc import augment
import shutil
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--outpath", required=True, help="Path to the outfolder")
ap.add_argument("-l", "--language", default="eng", help="language to choose")
ap.add_argument("-p", "--psm", type=int, default=4, help="segmentation mode")
args = vars(ap.parse_args())

tesseract_cmd = 'tesseract'
def run_tesseract(input_filename, output_file_name, psm=None, lang=None):
	command =[]
	command += (tesseract_cmd, input_filename, output_file_name)
	
	if psm != None:
		command+=('-psm', psm)
	if lang != None:
		command += ('-l', lang)
	
	subprocess.run(command, stderr=subprocess.PIPE)
	

def image_to_text(image_path, psm):
	
	dir_name, base_name = os.path.split(image_path)
	temp_name = tempfile.mktemp(prefix='tess_')
	output_file_name = 'output'
	run_tesseract(image_path, output_file_name, psm=psm)
	with open(output_file_name+'.txt', 'r') as output_file:
		text = output_file.read()
	
		return text
                                         
def text_to_image(text, outpath):
	image = np.ones((150, 200,3), np.uint8)*255
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(image, text, (20,50), font, 1,(0,0,0), 2, cv2.LINE_AA)
	cv2.imwrite('%s/%s.jpg'%(outpath, text), image)
	
def generate_strings(num):
	words = open('/etc/dictionaries-common/words').readlines()
	words = [word for word in words]
	rand = randint(0,len(words))
	def return_nearest():
		nearest = []
		rword = words[rand]
		words.remove(rword)	
		for word in words:
			if 2<= lev(word, rword)<=5:
				nearest.extend(word.rsplit())
				if len(nearest)>=num:
					break
			
		return nearest
	return return_nearest()

def gmkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def rename(image_locs):
	for k, image in enumerate(image_locs):
		base, name = os.path.split(image)
		new_name = '%d.jpg'%k
		destination = os.path.join(base, new_name)
		shutil.move(image, destination)

	return(list(map(lambda x: base +'/'+ x,os.listdir(base))))
	print('done')




if __name__ == "__main__":
	outpath = args["outpath"]
	
	lang = args["language"]
	psm = str(args["psm"])
	gmkdir(outpath)

	image_path = os.path.join(outpath,'output/')
	# try:
		# print(image_to_text(image_path, lang=lang,  psm=str(psm)))
	num = 100
	num_samples = 1000
	words = generate_strings(num)
	print(len(words))
	for word in words:
		text_to_image(word, outpath)
	augment(outpath, num_samples)
	images = os.listdir(image_path)
	image_locs = list(map(lambda x: image_path + x , images))
	image_locs = rename(image_locs)
	for image in image_locs[:-1]:
		image_name = (os.path.split(image)[1])
		text ='%s  %s'%(image_name, image_to_text(image, psm))
		

		with open('predictions.txt', 'a') as fp:
			fp.write('%s\n'%(text).rstrip())
	
