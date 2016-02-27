from optparse import OptionParser
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE")
parser.add_option("-o", "--browse", dest="browser",
                  help="write report to FILE", metavar="FILE")
parser.add_option("-i", "--index", dest="index",
                  help="write report to FILE", metavar="FILE")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

  
#bdbcontrib.query(bdb,'''drop table dfr''')
#bdbcontrib.query(bdb,'''drop generator dfr_cc''')


import pandas as pd
import numpy as np
import re
import matplotlib
matplotlib.use('nbAgg')
from matplotlib import ft2font
import matplotlib.pyplot as plt
from bdbcontrib.recipes import quickstart
import crosscat
import crosscat.MultiprocessingEngine as ccme
import bayeslite.metamodels.crosscat
import os
import bayeslite
from bayeslite.read_pandas import bayesdb_read_pandas_df
import bdbcontrib
from bdbcontrib import cursor_to_df as df
from bdbcontrib.recipes import quickstart
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.getdefaultencoding()

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


#counting the NaN type
def count(dataset):
    import pandas as pd    
    return (dataset.count().sum(),dataset.isnull().sum().sum())

  
#Chosing if the script has to be run on the entire directory or on a specific csv file
#List of all the files entered as an input by the user
lst=args
a = "Descriptions.csv"
if a in lst:
  lst.remove(a)
  
#Get the list of csv files of the directory and keep them in a list
l = []
for f in lst:
  if f[-4:] == ".csv":
    l.append(f)

a = "Descriptions.csv"
if a in l:
  l.remove(a)
#Keep all the csv files that are the descriptions of the variable names in another list
b=[]
for i in range((len(l))):
  c = str(l[i][:-4])+"_col.csv"
  b.append(c)

#Take out all the descriptions csvs from list l in order to only keep the datasets
for i in range((len(l))):
  if b[i] in l:
    l.remove(b[i])

print color.BLUE + str(l) + color.END   

ind = 30

if not options.index:
  inf = ind

else: 
  ind = ind + int(options.index)



for i in range(len(l)):
  basename = l[i][:-4] 
  ###loading the dataset
  data = pd.read_csv(l[i][:], delimiter=',', low_memory = False)
  #reducing to 20 columns
  datareduce = data.iloc[0:1000,1:ind]
  
  
  for j in range(len(datareduce.columns)-4):
    if 'Site ID' in datareduce.columns[j]:
      datareduce.drop(str(datareduce.columns[j]), axis=1, inplace=True)
  
    if 'id' in datareduce.columns[j]:
      datareduce.drop(str(datareduce.columns[j]), axis=1, inplace=True)       
  
    if 'ID' in datareduce.columns[j]:
      datareduce.drop(str(datareduce.columns[j]), axis=1, inplace=True) 

    if 'IDO' in datareduce.columns[j]:
      datareduce.drop(str(datareduce.columns[j]), axis=1, inplace=True)  

    if 'SITEID' in datareduce.columns[j]:
      datareduce.drop(str(datareduce.columns[j]), axis=1, inplace=True)  
     
    if 'SEXN' in datareduce.columns[j]:
      datareduce.drop(str(datareduce.columns[j]), axis=1, inplace=True)    
 

  if str(str(l[i][:-4])+"_col.csv") in lst:
    cols = pd.read_csv(l[i][:-4] + '_col.csv', delimiter=';', low_memory = False)

    liste_col = list(map(str.lower,cols.iloc[:,0]))
    liste_desc = list(map(str.lower,cols.iloc[:,1]))
    liste_datar = list(map(str.lower,datareduce.columns))

    #L = [cols[cols.iloc[:,0]==c]['Study ID'].iloc[0] for c in liste_datar]
    L=[]
    
    for element in liste_datar:
      if element in liste_col:
        liste_datar[liste_datar.index(element)] = liste_desc[liste_col.index(element)]
    
    
    datareduce.columns = liste_datar
    
    
  #creating the bdb file

  
  bdb = bayeslite.bayesdb_open("bdb/"+str(str(l[i][:-4]))+".bdb")
  bdbcontrib.query(bdb,'''drop generator if exists dfr_cc''')
  bdbcontrib.query(bdb,'''drop table if exists dfr''')
  bayesdb_read_pandas_df(bdb, "dfr", datareduce, create=True)
  test = quickstart(name='dfr', bdb_path="bdb/"+str(str(l[i][:-4]))+".bdb")
  q = test.q


#run analysis
  import time
  start_time = time.time()
  test.analyze(models=30, iterations=70)
  t = int(time.time() - start_time)
#Depprob matrix

  img = test.heatmap(test.q('''ESTIMATE DEPENDENCE PROBABILITY FROM PAIRWISE COLUMNS OF %g'''))
  ax = img.add_subplot(111)
  handles, labels = ax.get_legend_handles_labels()
  lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1))
  for text in lgd.get_texts():
    plt.setp(text, color = 'white')

  plt.savefig("images/"+basename,bbox_extra_artists=(lgd,), bbox_inches='tight')

  matt = np.array(bdbcontrib.describe_generator_columns(bdb, 'dfr_cc'))
  datar = datareduce[matt[:,1]]

  #query table
  variables = []
  table_tr = np.array(q('select*from %t limit 3').transpose())
  
  header1 = [str(open("html/header_select.html").read())]
  def query():
      table_tr = np.array(q('select*from %t limit 3').transpose())
      variables = q('select*from %t limit 3').columns
      header1 = [str(open("html/header_select.html").read())]
      for j in range(0,10):
        row = str(open("html/row_select.html").read()).format(varname = str(variables[j]), 
            value1 = str(table_tr[j][0]),
            value2 = str(table_tr[j][1]),
           value3 = str(table_tr[j][2]))
        header1.append(row)
        footer = str(open("html/footer_select.html").read())
        
      header1.append(footer)
      final = ' '.join(header1)
      return final

  #pairplot
  liste = test.quick_describe_columns()
  
  gen_cols = [str(liste.iloc[0,1]),str(liste.iloc[1,1])]
  PP = bdbcontrib.pairplot(bdb, '''
    SELECT {string1},{string2}
        FROM dfr;'''.format(string1='"' + gen_cols[0] + '"', string2='"' + gen_cols[1] + '"'));
  plt.savefig("images/PP_"+basename,bbox_extra_artists=(lgd,), bbox_inches='tight')



  #Missing values
  n = len(matt)
  def miss():
    matt = np.array(bdbcontrib.describe_generator_columns(bdb, 'dfr_cc'))
    array = datareduce.columns.values
    header = [str(open("html/header_table.html").read())]
    for (j,k) in zip(range(0, (n/2)-1),range(n/2, n-1)):
      
      row = str(open("html/row_table.html").read()).format(colname1 = str(matt[j][1]), 
            count1 = datar.count()[j],
            type1 = str(matt[j,2]),
           missing1 = 100*datar.isnull().sum()[j]/(datar.isnull().sum()[j]+datar.count()[j]),
           colname2 = str(matt[k][1]), 
            count2 = datar.count()[k],
            type2 = str(matt[k,2]),
           missing2 = 100*datar.isnull().sum()[k]/(datar.isnull().sum()[k]+datar.count()[k]))
      header.append(row)
      
    footer = str(open("html/footer_table.html").read() ).format(string5 = datar.count().sum(),
           string6 = 100 * datar.isnull().sum().sum()/(datar.shape[0]*datar.shape[1]))
    
    header.append(footer)
    final = ' '.join(header)
    return final
  #Description of the dataset (extracted from a csv file)
  import pandas as pd
  import numpy as np


  desc = pd.read_csv("Descriptions.csv", delimiter=';', low_memory = False)
  obj = np.array(desc)
  a = []
  for k in range(len(desc)):
      if basename == obj[k,0]:
         a = obj[k,1]
                

  head = str(open("html/core.html").read() ).format(string1 = data.shape[0],
           string2 = data.shape[1], 
           string3 = datar.shape[0],
           string4 = datar.shape[1],
           string7 = "images/" + basename + '.png',
           string8 = basename,
           string10 = a,
           time = t ,
           models = test.analysis_status().iloc[0,0],
           iterations = int(test.analysis_status().index.tolist()[0]),
           pplot = "images/PP_"+basename + '.png') 
    
   

  if str(l[i][:-4])+"_col.csv" not in lst:
    head = str(open("html/core_miss.html").read() ).format(string1 = data.shape[0],
           string2 = data.shape[1], 
           string3 = datar.shape[0],
           string4 = datar.shape[1],
           string7 = "images/" + basename + '.png',
           string8 = basename,
           string10 = a,
           time = t ,
           models = test.analysis_status().iloc[0,0],
           iterations = int(test.analysis_status().index.tolist()[0]),
           pplot = "images/PP_"+basename + '.png') 

  liste =[head]
  liste.append(query())
  liste.append(miss())

  contents = ' '.join(liste)

  def main():
    browseLocal(contents)
      
  def strToFile(text, filename):
      output = open(filename,"w")
      output.write(text)
      output.close()

  import platform
    
  def browseLocal(webpageText, filename='Sample_Sketch_' + basename):
    filename  = filename + '.html'
    import webbrowser, os.path
    strToFile(webpageText, filename)
    if options.browser == "yes":
      webbrowser.open("file:///" + os.path.abspath(filename))
    else:
      if platform.system() == 'Darwin':
        print color.RED + "You are on Mac OS" + color.END
        print color.RED + ("Enter $open %s to browse your sketch")%filename + color.END
      if platform.system() == 'Linux':
        print color.RED + ("You are on Linux", 'red') + color.END
        print color.RED + ("Enter $firefox %s to browse your sketch")%filename + color.END
      if platform.system() == 'Windows':
        print color.RED + ("You are on Windows", 'red') + color.END
        print color.RED + ("Enter $start %s to browse your sketch")%filename  + color.END
        
  if __name__ == "__main__":
    main()   
      

  
    
