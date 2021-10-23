# fastqcDataClassify
this script classify the overrepresented sequences of the fastqc data, by compare the sequence to the input files sequences.

* Dependency:
  * Python 3.x
  * pandas

* Manual:

  `-i <path1,path2,...>: any csv file which separated by tab, including sequence & id columns. for multiply input files use the seperator ','.
  all the input files should be in the same format.`

  `-f <path>: fastqc_data.txt input path.`
  
  `-sc <column_name1,column_name2,...>: sequences columns name, for multiply sequences columns use the seperator ','.`
  
  `-idc <column_name>: id column name.` 
  
  `-o <path>: output path.`






* Example Run:

  `python fastqcDataClassify.py -i novel.txt,novel451.txt -f fastqc_data.txt -sc hairpinSeq -idc name -o fastqc_data_classify.csv`
