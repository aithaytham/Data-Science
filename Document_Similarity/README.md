
# Document Similarity
The objective of this programming assignment is to be able to implement a system for document similarity, using the Min-Hash and Locality Sensitive Hashing methods presented in the lectures.

# Description
this directory contains 5 files which are as follows:
 * tweets.txt : which is a test file containing documents to compare for our algorithms. This file was downloaded from https://www.lri.fr/~maniu/tweets.txt
 * Report_Document_Similarity.pdf : This file contains the report of our work
 * Project_Requirements.pdf : This file contains the description of the work to be done
 * Notebook1.py : This file contains the program we made in python version
 * Notebook1.ipynb : This file contains the program we made in jupyter version. This version of the code contains more informations and explanations: this is where you can correctly view the images
 
# Run program

For the python file to work, you will need to run the Notebook1.py program on a terminal like so:
Notebook1.py name_file.txt similarity_value
where name_file.txt is a file that is in the same directory as the python program and similarity_value is the value of the jaccard similarity threshold.
for example by running the following command :
 * python Notebook1.py tweets.txt 0.05
 
we will see this in the terminal.
(base)  python Notebook1.py tweets.txt 0.05

0      238      0.05102040816326531

0      455      0.061068702290076333

1      237      0.125

1      238      0.14285714285714285

1      454      0.07017543859649122

1      455      0.05747126436781609

1      464      0.0847457627118644

1      468      0.05660377358490566

2      4      0.07228915662650602

2      5      0.0759493670886076

2      237      0.057692307692307696

2      238      0.05555555555555555

2      265      0.06722689075630252

2      468      0.05555555555555555

2      469      0.06315789473684211

4      5      0.06521739130434782

4      209      0.05405405405405406

4      265      0.08527131782945736

4      468      0.07692307692307693

4      469      0.05555555555555555

5      469      0.057692307692307696

8      61      0.09375

8      62      0.1875

8      63      0.09375

8      64      0.05172413793103448

8      104      0.06666666666666667

8      105      0.05454545454545454

8      241      0.125

8      242      0.0625

8      300      0.07692307692307693

8      301      0.12

8      303      0.16666666666666666

8      304      0.10344827586206896

8      305      0.1

8      485      0.0625

10      12      0.20192307692307693

10      17      0.05434782608695652

10      48      0.05343511450381679

10      86      0.05102040816326531

10      160      0.05128205128205128

10      240      0.05102040816326531

10      246      0.09821428571428571

10      249      0.05063291139240506

10      373      0.05844155844155844

10      411      0.17647058823529413

12      246      0.054945054945054944

12      249      0.05303030303030303

12      280      0.06578947368421052

12      282      0.060240963855421686

12      287      0.056818181818181816
