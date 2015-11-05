import plyj.model as model

class LoopStart:
    def __init__(self, loop_num):
        self.loop_num = loop_num
    def getLoopNum(self):
        return self.loop_num

class LoopEnd:
    pass
    

class JMethodInvocation:
    #the classContainingInvocation is the location of the invocation -- NOT the declaration/definition of the invoked method.
    def __init__(self, name, target, classContainingInvocation, variableTypes, fieldTypes):
        
            
        if type(name) is not str:
            name = name.value
        if type(target) is not str and target is not None:
            if isinstance(target, model.FieldAccess):
                #then the target is a field
                #if target.target is 'this' or classContainingInvocation, then self reference
                target = fieldTypes[target.name]
            else:
                #They could be accessing a field, but let's check in variableTypes first. If not in variableTypes, then in fieldTypes.
                if target.value in variableTypes.keys():
                    target = variableTypes[target.value]
                elif target.value in fieldTypes.keys():
                    target = fieldTypes[target.value]
                else:
                    target = target.value
        if target == None:
            #then we called a method in our own class!
            self.jClass = None
        elif target == 'this' or target == classContainingInvocation:
            self.jClass = None
        else:
            self.jClass = target
        self.name = name
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
        #map variables and fields to their types
        self.variableTypes = dict()
        self.fieldTypes = dict()
        self.loopDepth = 0
        self.ignoreMInvocations = False
    def visit_ClassDeclaration(self, class_declaration):
        if class_declaration.name == self.className:
            print("Found the class: " + self.className)
            return True
        else:
            return False

    def visit_MethodDeclaration(self, method_declaration):
        if method_declaration.name == self.methodName:
            print("Found the method: " + self.methodName)
            for parameter in method_declaration.parameters:
                if type(parameter.type) is str:
                    #Seems to be for primitives
                    self.variableTypes[parameter.variable.name] = parameter.type
                else:
                    #seems to be for objects
                    self.variableTypes[parameter.variable.name] = parameter.type.name.value
            return True
        else:
            return False
    

    def visit_For(self, for_loop):
        print("For loop: " + str(for_loop))
        self.methodInvocationList.append(LoopStart(self.loopDepth))
        self.loopDepth += 1
        
        
        self.ignoreMInvocations = True
        
        for_loop.init.accept(self)
        for_loop.predicate.accept(self)
        if isinstance(for_loop.update, list):
            for x in for_loop.update:
                x.accept(self)
        else:
            for_loop.update.accept(self)    

        self.ignoreMInvocations = False
        for_loop.body.accept(self)
        self.methodInvocationList.append(LoopEnd())
        self.loopDepth -= 1
        return False

    def visit_While(self, while_loop):

        self.methodInvocationList.append(LoopStart(self.loopDepth))
        self.loopDepth += 1
        #we want to iterate body of loop, but not start or ends.
        
        self.ignoreMInvocations = True
        while_loop.predicate.accept(self)
        self.ignoreMInvocations = False
        while_loop.body.accept(self)
        self.methodInvocationList.append(LoopEnd())
        self.loopDepth -= 1
        return False


    def visit_ForEach(self, foreach_loop):
        self.methodInvocationList.append(LoopStart(self.loopDepth))
        self.loopDepth += 1
        #we want to iterate body of loop, but not start or ends.
        self.ignoreMInvocations = True
        foreach_loop.variable.accept(self)
        self.ignoreMInvocations = False
        foreach_loop.body.accept(self)
        self.methodInvocationList.append(LoopEnd())
        self.loopDepth -= 1
        return False


    def visit_DoWhile(self, dowhile_loop):

        self.methodInvocationList.append(LoopStart(self.loopDepth))
        self.loopDepth += 1
        #we want to iterate body of loop, but not start or ends.
        
        self.ignoreMInvocations = True
        dowhile_loop.predicate.accept(self)
        self.ignoreMInvocations = False
        dowhile_loop.body.accept(self)
        self.methodInvocationList.append(LoopEnd())
        self.loopDepth -= 1
        return False
        
    def visit_VariableDeclaration(self, variable_declaration):
        for vd in variable_declaration.variable_declarators:
            if type(variable_declaration.type) is str:
                self.variableTypes[vd.variable.name] = variable_declaration.type
            else:
                self.variableTypes[vd.variable.name] = variable_declaration.type.name.value
        return True


    def visit_FieldDeclaration(self, field_declaration):
        for vd in field_declaration.variable_declarators:
            if type(field_declaration.type) is str:
                self.fieldTypes[vd.variable.name] = field_declaration.type
            else:
                self.fieldTypes[vd.variable.name] = field_declaration.type.name.value
        return True



    def leave_MethodInvocation(self, method_invocation):
        if self.ignoreMInvocations != True:
            print("Leaving method invocation: " + str(method_invocation))
            self.methodInvocationList.append(JMethodInvocation(method_invocation.name, method_invocation.target, self.className, self.variableTypes, self.fieldTypes))
        return True
        
