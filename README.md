# SequenceDiagramJava
We had to create static sequence diagrams from Java source code for my Software Engineering class. We were supposed to use ModelGonn for this. However, I found that when I tried to create the diagrams for methods in my project (OmegaT), it threw a Null Pointer Exception.

I tried this on three computers, on 2 different OSes (Arch Linux and Windows) and 2 different versions of Eclipse (Mars and Luna), and had the same issue. 

Additionally, I tried ModelGoon on some small code; the results were less than stellar. I also find the output of ModelGoon to be difficult to read.

Therefore, I am creating this script to create static sequence diagrams from Java source code.

It depends on plyj [https://github.com/musiKk/plyj], and you need seqdiag (https://pypi.python.org/pypi/seqdiag/) to turn the diagram output to an image.
