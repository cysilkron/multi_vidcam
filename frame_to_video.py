import cv2
import numpy as np
import os
from os.path import isfile, join
import yaml

def convert_frames_to_video(pathIn,pathOut,fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
    #for sorting the file names properly
    files.sort(key = lambda x: int(x[6:-4]))
    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        print(filename)
        #inserting the frames into an image array
        frame_array.append(img)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
    
def main(yaml_opt):
    pathIn= yaml_opt['pathIn']
    pathOut = yaml_opt['pathOut']
    fps = yaml_opt['fps']
    convert_frames_to_video(pathIn, pathOut, fps)

def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

if __name__=="__main__":
    yaml_opt = read_yaml('frame_to_video_opt.yaml')
    main(yaml_opt)