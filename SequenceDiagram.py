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
            f.write('@startuml \n')
            for invocation in invocationList:
                if isinstance(invocation, LoopStart):
                    f.write('loop \n')
                elif isinstance(invocation, LoopEnd):
                    f.write('end\n')
                else:
                    if invocation.getClass() == None:
                        #self referential -- method invocation is member of class 
                        f.write(className + ' -> ' + className + ' : ' + invocation.getName() + '\n')
                    else:
                        f.write(className + ' -> ' + invocation.getClass() + ' : ' + invocation.getName() + '\n')
                        f.write(invocation.getClass() + ' -> ' + className + '\n')
            f.write('@enduml')


                        


if len(sys.argv) == 5:
    parser = plyj.Parser()
    diagram(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
else:
    print("Usage: javaFileName, outputFileName, className, methodName")

