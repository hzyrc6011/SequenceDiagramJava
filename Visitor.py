import plyj.model as model

class JMethodInvocation:
    #the classContainingInvocation is the location of the invocation -- NOT the declaration/definition of the invoked method.
    def __init__(self, name, target, classContainingInvocation):
        self.name = str(name)
        if target == None:
            #then we called a method in our own class!
            self.jClass = None
        elif str(target.value) == 'this' or str(target.value) == classContainingInvocation:
            self.jClass = None
        else:
            self.jClass = str(target.value)
            
    def getName(self):
        return self.name

    def getClass(self):
        return self.jClass

class JordanVisitor(model.Visitor):
    #we add method invocations to methodInvocationList
    def __init__(self, className, methodName, methodInvocationList):
        super(JordanVisitor, self).__init__()
        self.className = className
        self.methodName = methodName
        self.methodInvocationList = methodInvocationList


    def visit_ClassDeclaration(self, class_declaration):
        if class_declaration.name == self.className:
            print("Found the class: " + self.className)
            return True
        else:
            return False

    def visit_MethodDeclaration(self, method_declaration):
        if method_declaration.name == self.methodName:
            print("Found the method: " + self.methodName)
            return True
        else:
            return False
    
    def visit_VariableDeclaration(self, variable_declaration):
        #our variable declarations
        for declaration in variable_declaration.variable_declarators:
            print(declaration.variable.name)





    def leave_MethodInvocation(self, method_invocation):
        print("Leaving method invocation: " + str(method_invocation))
        self.methodInvocationList.append(JMethodInvocation(method_invocation.name, method_invocation.target, self.className))
        return True
        
