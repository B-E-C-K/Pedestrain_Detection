import pandas as pd
import os
import csv

max_width = 960
max_height = 540
filename_list = []
def clean_csv(input_csv_filename,input_csv_dir,output_csv_filename,output_csv_dir):
    os.chdir(input_csv_dir)
    df = pd.read_csv(input_csv_filename)
    rowlist = []
    for index,row in df.iterrows():
        if((row['xmax'] > max_width)|(row['xmin'] < 0) | (row['ymax'] > max_height) | (row['ymin'] < 0) | (pd.isnull(row['filename'])) | (pd.isnull(row['width'])) | (pd.isnull(row['height'])) | (pd.isnull(row['class'])) | (pd.isnull(row['xmin'])) | (pd.isnull(row['ymin'])) | (pd.isnull(row['xmax'])) | (pd.isnull(row['ymax'])) ):
            filename = row['filename']
            if (filename in filename_list):
                pass
            else:
                filename_list.append(filename)

    with open(input_csv_filename,'r') as file:
        reader = csv.reader(file)
        for row in reader:
            count_field = 0
            for field in row:
                if field in filename_list:
                    count_field += 1
                    break
            if(count_field == 0):
                rowlist.append(row)


    print(len(filename_list))
    os.chdir(output_csv_dir)
    open(output_csv_filename,'x')
    with open(output_csv_filename,'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rowlist)




def clean_images(image_dir):
    os.chdir(image_dir)
    for img_file in filename_list:
        if os.path.exists(img_file):
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



clean_csv("train_labels.csv",r"C:\Users\User\Desktop\dataset","train_labels2.csv",r"C:\Users\User\Desktop\dataset")
clean_csv("test_labels.csv",r"C:\Users\User\Desktop\dataset","test_labels2.csv",r"C:\Users\User\Desktop\dataset")
clean_images(r"C:\Users\User\Desktop\dataset\images\train_img")
clean_images(r"C:\Users\User\Desktop\dataset\images\test_img")
clean_xml_annotations(r"C:\Users\User\Desktop\dataset\annotations\train_annotations")
clean_xml_annotations(r"C:\Users\User\Desktop\dataset\annotations\test_annotations")
