# Slicer 
Simple wrapper for the Zathura and QPDF to slice the pdfs.

Warning:
This is just a toy project that I have to summarize the lectures.
There is probably a much better way, but this is funny.

Set Up:
Put this in Zathura config:
```
~/.config/zathura/zathurarc:
map <C-y> exec "echo $PAGE"
map <C-n> exec "echo -$PAGE"
```

The Slicer works by listening to the stdout from Zathura with number of pages,
then slightly processes the info and gives it to the qpdf which does the slicing, by the comand:
```
qpdf --empty --pages  <in_file> <pages> -- <out_file>
```
