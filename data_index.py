from optparse import OptionParser
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE")
parser.add_option("-o", "--browse", dest="browser",
                  help="write report to FILE", metavar="FILE")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

import inspect
import os
import sys
import pandas as pd
import numpy as np

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)



import os
lst=os.listdir(get_script_dir())

csv = []
png = []
col=[]

#Colors
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


a = 'Descriptions.csv'
if a in lst:
  lst.remove(a)

for f in lst:
  if f[-4:] == ".csv":
    csv.append(f)


for i in range((len(csv))):
  c = str(csv[i][:-4])+"_col.csv"
  col.append(c)

for i in range((len(csv))):
  if col[i] in csv:
    csv.remove(col[i])

print color.RED + str(csv) + color.END

for f in lst:
	if f[-4:] == ".png":
		png.append(f)

def count(dataset):
    import pandas as pd    
    return (dataset.count().sum(),dataset.isnull().sum().sum())


head = str(open("html/header_index.html").read())


desc = pd.read_csv("Descriptions.csv", delimiter=';', low_memory = False)
obj = np.array(desc)
a = []



content = [head]
for i in range(len(csv)):
  for k in range(len(desc)):
    if csv[i][:-4] == obj[k,0]:
      a = obj[k,1]
    data = pd.read_csv(csv[i], delimiter=',', low_memory = False)

    if str(csv[i][:-4])+"_col.csv" not in lst:
      core = str(open("html/row_index_miss.html").read()).format(set = csv[i],
            title = 'Sample_Sketch_' + csv[i][:-4]+'.html',
           rows = data.shape[0], 
           columns = data.shape[1],
           miss = 100*count(data)[1]/(count(data)[0]+count(data)[1]),
           map = 'images/' + csv[i][:-4] + '.png',
           desc = a ) 
    else:
      core = str(open("html/row_index.html").read()).format(set = csv[i],
            title = 'Sample_Sketch_' + csv[i][:-4]+'.html',
           rows = data.shape[0], 
           columns = data.shape[1],
           miss = 100*count(data)[1]/(count(data)[0]+count(data)[1]),
           map = 'images/' + csv[i][:-4] + '.png',
           desc = a ) 
     
  content.append(core)	

if len(content)>6:
  content.insert(6, ''' </table><div style="page-break-after:always"></div>
  <table style  = "border-collapse: collapse; width: 100% " border="1" border-collapse=collapse>
  <tr>
    <td><font face="verdana" >Dataset</font></td>
    <td style="font-weight:bold;"><font face="verdana" >Shape</font></td>
    <td style="font-weight:bold;"><font face="verdana" >Missing values</font></td>
    <td style="font-weight:bold;"><font face="verdana" >Sketch of Dependencies</font></td>

</tr>''')

extra = str(open("html/footer_index.html").read())
content.append(extra)
contents = ' '.join(content)


def main():
     browseLocal(contents)
 
    
def strToFile(text, filename):
	output = open(filename,"w")
	output.write(text)
	output.close()
import platform
from termcolor import colored
def browseLocal(webpageText, filename='Data_Index'):
    filename  = filename + '.html'
    import webbrowser, os.path
    strToFile(webpageText, filename)
    if options.browser == "yes":
      webbrowser.open("file:///" + os.path.abspath(filename))
    else:
      if platform.system() == 'Darwin':
        print colored("You are on Mac OS", 'red')
        print colored("Enter $open %s to browse your sketch", 'red')%filename
      if platform.system() == 'Linux':
        print colored("You are on Linux", 'red')
        print colored("Enter $firefox %s to browse your sketch", 'red')%filename
      if platform.system() == 'Windows':
        print colored("You are on Windows", 'red')
        print colored("Enter $start %s to browse your sketch", 'red')%filename
      
	
    

main()








