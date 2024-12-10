import scanner
import  GrammerOfTinyLanguage as Tinylanguage
#functions that recogniza non-terminals

class NonTerminals:
    
    def __init__(self,filepath):
        self.TokenList=scanner.scan(filepath)
        self.pointer=0
        self.MaxPointerValue=len(self.TokenList)-1
        self.debug= True #True :> for printing the statments 

    def loggs(self):
        print("the value of first token ",self.TokenList[self.pointer].value)
        print("read from tiny grammer ", Tinylanguage.tiny_grammar["read_stmt"][0][0])
        
        if(self.TokenList[self.pointer].value == Tinylanguage.tiny_grammar["read_stmt"][0][0]):
            print ("okay")    
            
            
            
    def factor (self):
        if(self.TokenList[self.pointer].value == Tinylanguage.tiny_grammar["factor"][0][0]):
            self.pointer+=1
            self.exp()
            
            if(self.TokenList[self.pointer].value==Tinylanguage.tiny_grammar["factor"][0][2]):
                self.pointer+=1
                
            else:
                raise RuntimeError("Error: ')' is expected")
        elif((self.TokenList[self.pointer].type)==Tinylanguage.tiny_grammar["factor"][1][0]):
            self.pointer+=1
        elif((self.TokenList[self.pointer].type)==Tinylanguage.tiny_grammar["factor"][2][0]):
            self.pointer+=1
        else:
            raise RuntimeError("Error: '(' or 'number' is expected")
        
        
    def term (self):
        self.factor()
        while((self.pointer<self.MaxPointerValue) and ((self.TokenList[self.pointer].value in Tinylanguage.tiny_grammar["mulop"][0][0] ) \
                or(self.TokenList[self.pointer].value in Tinylanguage.tiny_grammar["mulop"][1][0]) )):
                self.pointer+=1
                self.factor()
                    
            
    def simple_exp(self):
        self.term()
        
        while((self.pointer<self.MaxPointerValue)and ((self.TokenList[self.pointer].value in Tinylanguage.tiny_grammar["addop"][0][0] ) \
            or (self.TokenList[self.pointer].value in Tinylanguage.tiny_grammar["addop"][1][0]) )):
            self.pointer+=1
            self.term()
    
    def exp(self):
        self.simple_exp()
        while((self.pointer<self.MaxPointerValue)and ((self.TokenList[self.pointer].value in Tinylanguage.tiny_grammar["comparison_op"][0][0] ) \
            or (self.TokenList[self.pointer].value in Tinylanguage.tiny_grammar["comparison_op"][1][0])) ):
            self.pointer+=1
            self.simple_exp()
    
    def write_stmt(self):
        if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["write_stmt"][0][0]):
            self.pointer+=1
            self.exp()
        else:
            raise RuntimeError("Error: 'write' key word is expected")
    
    def read_stmt (self):
        if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["read_stmt"][0][0]):
            self.pointer+=1
            if(self.TokenList[self.pointer].type== Tinylanguage.tiny_grammar["read_stmt"][0][1]):
                self.pointer+=1
            else:
                raise RuntimeError("Error: missing 'identifier' in read statment")
        else:
            raise RuntimeError("Error: 'read' key word is expected")
        
    def assign_stmt(self):
        if(self.TokenList[self.pointer].type== Tinylanguage.tiny_grammar["assign_stmt"][0][0]):
            self.pointer+=1
            if(self.TokenList[self.pointer].value == Tinylanguage.tiny_grammar["assign_stmt"][0][1]):
                self.pointer+=1
                self.exp()
            else:
                raise RuntimeError("Error: ':=' is missing")
            
        else:
            raise RuntimeError("Error: missing 'identifier in assign statment'")
        
    def repeat_stmt(self):
        if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["repeat_stmt"][0][0]):
            self.pointer+=1
            self.stmt_sequence()
            if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["repeat_stmt"][0][2]):
                self.pointer+=1
                self.exp()
            else:
                raise RuntimeError("Error: 'until' key word is expected ")
            
        else:
            raise RuntimeError("Error: 'repeat' key word is expected ")
    
    def if_stmt(self):
        if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["if_stmt"][0][0]):
            self.pointer+=1
            self.exp()
            if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["if_stmt"][0][2]):
                self.pointer+=1
                self.stmt_sequence()
                if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["if_stmt"][1][4]):
                    self.pointer+=1
                    self.stmt_sequence()  
                    if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["if_stmt"][1][6]):
                        self.pointer+=1
                    else:
                        raise RuntimeError("Error: 'end' of else is expected ")
                    
                elif(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["if_stmt"][0][4]):
                    self.pointer+=1
                else:
                    raise RuntimeError("Error: 'end' of if is expected ")

            else:
                raise RuntimeError("Error: 'then' key word is expected ")
            
        else:
            raise RuntimeError("Error: 'if' key word is expected ")
        
    def stmt_sequence(self):
        self.statement()
        while((self.pointer<self.MaxPointerValue)and(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["stmt_sequence"][0][1])):
            #store the semicolocn
            self.pointer+=1
            self.statement()
        
            
    def statement(self):
        
        if(self.TokenList[self.pointer].value == "if" ): 
            if self.debug:
                print("if statement")
            self.if_stmt()
            
        elif(self.TokenList[self.pointer].value == "repeat" ):
            if self.debug:
                print("repeat statement")
            self.repeat_stmt()
        
        elif(self.TokenList[self.pointer].type == "IDENTIFIER" ):
            if self.debug: 
                print("assign statement")
            self.assign_stmt()
        
        elif(self.TokenList[self.pointer].value =="read"):
            if self.debug:
                print("read statement")
            self.read_stmt()
                
        elif(self.TokenList[self.pointer].value =="write"):
            if self.debug:
                print("write statement")
            self.write_stmt()

