# Sample Sketch

Prerequisites:
Bayeslite Bdbcontrib Crosscat Matplotlib

In the directory you will find:

The script sketch.py
a bdb folder where all your bdb files will be saved in
an html folder with the html parts needed
an images folder where all your plots will be saved
a main.css file for design purposes
A csv file called Descriptions.cv where the first column will be the exact name of your csv file to analyze and the second column will be a brief description of it
a csv_file_col.csv file that HAS TO be named like your dataset csv file + ‘_col.csv’
This _col csv file is the codebook with two columns: variable name where you should write all your opaque variable names and Description corresponding to the meaning of each variable

TO RUN:

$python sketch.py file.csv file_col.csv

If you want to run it on all of your datasets:

$python sketch.py


A message will appear at the end of the run on your terminal telling you how to open the generated file