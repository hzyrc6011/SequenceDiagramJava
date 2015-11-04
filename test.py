import plyj.parser as plyj

parser = plyj.Parser()






class NoClassExists(Exception):
    def __init__(self, className):
        self.value = "No class named: " + className + " exists in the file"

class NoMethodExists(Exception):
    def __init__(self, methodName):
        self.value = "No method name: " + methodName + " exists"


def diagram(fileName, className, methodName):
    tree = parser.parse_file(open(fileName))
    foundClass = False
    foundMethod = False
    #go through the
    for tDeclaration in tree.type_declarations:
        if isinstance(tDeclaration, plyj.ClassDeclaration) and tDeclaration.name == className:
            foundClass = True
            for method in filter(lambda x: isinstance(x, plyj.MethodDeclaration), tDeclaration.body):
                if method.name == methodName:
                    foundMethod = True
                    for line in method.body:
                        #quickly check if there's a method invocation somewhere in this line.
                        
                        
                                
                        
                            #then we invoked a method
                        print('hi')
                    return method.body[1]


                    
print(diagram('Stuff.java', 'Stuff', 'printThing'))

