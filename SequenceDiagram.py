#!/usr/bin/python

import plyj.parser as plyj
from Visitor import *
import sys




class NoClassExists(Exception):
    def __init__(self, className):
        self.value = "No class named: " + className + " exists in the file"

class NoMethodExists(Exception):
    def __init__(self, methodName):
        self.value = "No method name: " + methodName + " exists"


def diagram(javaFileName, outputFileName, className, methodName):
    tree = parser.parse_file(open(javaFileName))
    foundClass = False
    foundMethod = False
    #go through the

    invocationList = list()
    tree.accept(JordanVisitor(className, methodName, invocationList))
    #now we have our invocations lined up in the queue.
    if len(invocationList) == 0:
        print("Method was not found, or it does not contain any method invocations")
    else:
        with open(outputFileName, 'w') as f:
            f.write('seqdiag { \n')
            for invocation in invocationList:
                if invocation.getClass() == None:
                    #self referential -- method invocation is member of class 
                    f.write(className + ' -> ' + className + ' [label=\"' + invocation.getName() + '\"];\n')
                else:
                    f.write(className + ' -> ' + invocation.getClass() + ' [label=\"' + invocation.getName() + '\"];\n')
                    f.write(className + ' <- ' + invocation.getClass() + ';\n')
            f.write('}')


                        


if len(sys.argv) == 5:
    parser = plyj.Parser()
    diagram(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
else:
    print("Usage: javaFileName, outputFileName, className, methodName")

