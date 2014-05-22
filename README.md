ts2docx
=======

Python script to convert to and from:
 - Qt Translation files (ts)
 - docx with tables

It consist of a pyqtts mini module that define, load and save ts file (xml)
And then two scripts

----------------------------------------------------------------------------------------

ts2docx with the following usage line:
 usage: ts2docx.py [-h] [-o OUTPUT] [--light] input

This script load a ts file in memory and create a docx
with a table with 3 columns and one row for every translation in the ts file

the first one with the translation context
the second with the original text
the third with space for the translation

if the light flag is specified only translation that are not finished or obsolete
are inserted in the docx

----------------------------------------------------------------------------------------

tsDocxUpdater with the following usage line:
 usage: tsDocxUpdater.py [-h] [--docx DOCX] [--output OUTPUT] input
 
This script load a ts and a docx files in memory
then update the translations insie the ts file with the information in the docx file



