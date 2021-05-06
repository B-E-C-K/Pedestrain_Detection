import pandas as pd
import os
import csv

max_width = 1920
max_height = 1080
filename_list = []

def clean_csv(input_csv_filename,input_csv_dir,output_csv_filename,output_csv_dir):
    os.chdir(input_csv_dir)
    df = pd.read_csv(input_csv_filename, header=None)
    rowlist = []

    f = open("test.txt", "w+")
    violation = False
    violate_frame = ""
    frame_rows = ""
    current_frame = ""  #record the current frame number
    last_frame = "" #keep track of the last frame number

    for index,row in df.iterrows():
        print("Processing:" + str(index))

        current_frame = row[1] #frameNumber

        if (current_frame != last_frame):
            f.write(frame_rows)

        if violate_frame != current_frame: #frameNumber
            violation = False

        if not (violation):
            if ((row[10] > max_width) | (row[8] < 0) | (row[11] > max_height) | (row[9] < 0) ):
                fname = str(int(row[1])) + ".jpg"
                filename_list.append(fname)
                violation = True
                violate_frame = row[1]
                frame_rows = ""
                continue
            else:
                frame_rows += f"{int(row[0])},{int(row[1])},{int(row[2])},{int(row[3])},{row[4]},{row[5]},{row[6]},{row[7]},{row[8]},{row[9]},{row[10]},{row[11]}\n"

        last_frame = current_frame

    f.close()


def clean_images(image_dir):
    os.chdir(image_dir)
    print("a")
    print(filename_list)
    for img_file in filename_list:
        if os.path.exists(img_file):
            print(f"Removing: {img_file}")
            os.remove(img_file)


def clean_xml_annotations(annotation_dir):

    xml_list = []
    for file in filename_list:
        filename = file.replace('.jpg','.xml')
        xml_list.append(filename)

    os.chdir(annotation_dir)
    for xml_file in xml_list:
        if os.path.exists(xml_file):
            os.remove(xml_file)

clean_csv("TownCentre-groundtruth.csv",r"D:\cJc\Study\Swinburne\COS30018_Int_Sys\Assignments\PedestrainDetection\dataset","TownCentre-groundtruth_cleaned.csv",r"D:\cJc\Study\Swinburne\COS30018_Int_Sys\Assignments\PedestrainDetection\dataset")
#clean_csv("test_labels.csv",r"C:\Users\User\Desktop\dataset","test_labels2.csv",r"C:\Users\User\Desktop\dataset")
clean_images(r"D:\cJc\Study\Swinburne\COS30018_Int_Sys\Assignments\PedestrainDetection\images")
#clean_images(r"C:\Users\User\Desktop\dataset\images\test_img")
#clean_xml_annotations(r"C:\Users\User\Desktop\dataset\annotations\train_annotations")
#clean_xml_annotations(r"C:\Users\User\Desktop\dataset\annotations\test_annotations")
