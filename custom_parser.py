from scanner import Scanner
import  GrammerOfTinyLanguage as Tinylanguage
from node import *
#functions that recogniza non-terminals


#
#
# import traceback
# import types
#
# import inspect
#
# def get_function_stack():
#     # Extracts a clean list of function names in the call stack
#     stack = inspect.stack()
#     return [frame.function for frame in stack[1:]]  # Skip the current 'get_function_stack'
#
# def wrap_function(func):
#     def wrapper(*args, **kwargs):
#         stack = get_function_stack()
#         stack = [s for s in stack if s != "wrapper"]
#         print(f"\nCall Stack: {stack}")
#         try:
#             print(args[0].TokenList[args[0].pointer])
#         except:
#             pass
#         return func(*args, **kwargs)
#     return wrapper
#
# def auto_wrap_class_methods(cls):
#     for attr_name, attr_value in vars(cls).items():
#         if isinstance(attr_value, types.FunctionType):  # Check if it's a method
#             setattr(cls, attr_name, wrap_function(attr_value))
#     return cls
#
# # Example: Automatically wrapping all methods in the class
# @auto_wrap_class_methods
class NonTerminals:

    def __init__(self,filepath):
        self.TokenList = Scanner.scan(filepath)
        self.pointer = 0
        self.MaxPointerValue = len(self.TokenList)-1
        self.debug = True #True :> for printing the statments
        self.root = Node(None, None, None, None, None)


    def loggs(self):
        print("the value of first token ",self.TokenList[self.pointer].value)
        print("read from tiny grammer ", Tinylanguage.tiny_grammar["read_stmt"][0][0])

        if(self.TokenList[self.pointer].value == Tinylanguage.tiny_grammar["read_stmt"][0][0]):
            print ("okay")

    def parse(self):
        self.root.center = self.stmt_sequence()

    def increment_ptr(self):
        self.pointer += 1

    def factor (self):
        if(self.TokenList[self.pointer].value == Tinylanguage.tiny_grammar["factor"][0][0]):
            self.increment_ptr()
            op = self.exp()

            if(self.TokenList[self.pointer].value==Tinylanguage.tiny_grammar["factor"][0][2]):
                self.increment_ptr()

            else:
                raise RuntimeError("Error: ')' is expected")
            return op
        # Below, these will be children of some "op", ops are caught in term() for */, or simple_exp() for +-, or exp() for comparison
        elif((self.TokenList[self.pointer].type)==Tinylanguage.tiny_grammar["factor"][1][0]):
            fac = Factor("const", self.TokenList[self.pointer].value)
            self.increment_ptr()
        elif((self.TokenList[self.pointer].type)==Tinylanguage.tiny_grammar["factor"][2][0]):
            fac = Factor("id", self.TokenList[self.pointer].value)
            self.increment_ptr()
        else:
            raise RuntimeError("Error: '(' or 'number' is expected")
        return fac

    def term (self):
        fac = self.factor()
        while((self.pointer<self.MaxPointerValue) and ((self.TokenList[self.pointer].value in Tinylanguage.tiny_grammar["mulop"][0][0] ) \
            or(self.TokenList[self.pointer].value in Tinylanguage.tiny_grammar["mulop"][1][0]) )):
                op = Operation(None, None, None)
                op.text = self.TokenList[self.pointer].value
                op.left = fac
                self.increment_ptr()
                op.right = self.factor()
                return op
        return fac

    def simple_exp(self):
        fac = self.term()
        while((self.pointer<self.MaxPointerValue)and ((self.TokenList[self.pointer].value in Tinylanguage.tiny_grammar["addop"][0][0] ) \
            or (self.TokenList[self.pointer].value in Tinylanguage.tiny_grammar["addop"][1][0]) )):
                op = Operation(None, None, None)
                op.text = self.TokenList[self.pointer].value
                op.left = fac
                self.increment_ptr()
                op.right = self.term()
                return op
        return fac

    def exp(self):
        fac = self.simple_exp()
        while((self.pointer<self.MaxPointerValue)and ((self.TokenList[self.pointer].value in Tinylanguage.tiny_grammar["comparison_op"][0][0] ) \
            or (self.TokenList[self.pointer].value in Tinylanguage.tiny_grammar["comparison_op"][1][0])) ):
                op = Operation(None, None, None)
                op.text = self.TokenList[self.pointer].value
                op.left = fac
                self.increment_ptr()
                op.right = self.simple_exp()
                return op
        return fac

    def write_stmt(self):
        if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["write_stmt"][0][0]):
            self.increment_ptr()
            stmt = Statement("write", None, None, None, None)
            stmt.center = self.exp()
        else:
            raise RuntimeError("Error: 'write' key word is expected")
        return stmt

    def read_stmt (self):
        if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["read_stmt"][0][0]):
            self.increment_ptr()
            if(self.TokenList[self.pointer].type== Tinylanguage.tiny_grammar["read_stmt"][0][1]):
                stmt = Statement("read", self.TokenList[self.pointer].value, None, None, None)
                self.increment_ptr()
            else:
                raise RuntimeError("Error: missing 'identifier' in read statment")
        else:
            raise RuntimeError("Error: 'read' key word is expected")
        return stmt

    def assign_stmt(self):
        if(self.TokenList[self.pointer].type== Tinylanguage.tiny_grammar["assign_stmt"][0][0]):
            stmt = Statement("assign", self.TokenList[self.pointer].value, None, None, None)
            self.increment_ptr()
            if(self.TokenList[self.pointer].value == Tinylanguage.tiny_grammar["assign_stmt"][0][1]):
                self.increment_ptr()
                stmt.center = self.exp()
            else:
                raise RuntimeError("Error: ':=' is missing")

        else:
            raise RuntimeError("Error: missing 'identifier in assign statment'")
        return stmt

    def repeat_stmt(self):
        stmt = Statement("repeat", None, None, None, None)
        if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["repeat_stmt"][0][0]):
            self.increment_ptr()
            stmt.left = self.stmt_sequence()
            if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["repeat_stmt"][0][2]):
                self.increment_ptr()
                stmt.right = self.exp()
            else:
                raise RuntimeError("Error: 'until' key word is expected ")

        else:
            raise RuntimeError("Error: 'repeat' key word is expected ")
        return stmt

    def if_stmt(self):
        stmt = Statement("if", None, None, None, None)
        if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["if_stmt"][0][0]):
            self.increment_ptr()
            stmt.left = self.exp()
            if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["if_stmt"][0][2]):
                self.increment_ptr()
                stmt.center = self.stmt_sequence()
                if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["if_stmt"][1][4]):
                    self.increment_ptr()
                    stmt.right = self.stmt_sequence()
                    if(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["if_stmt"][1][6]):
                        self.increment_ptr()
                    else:
                        raise RuntimeError("Error: 'end' of else is expected ")

                elif(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["if_stmt"][0][4]):
                    self.increment_ptr()
                else:
                    raise RuntimeError("Error: 'end' of if is expected ")

            else:
                raise RuntimeError("Error: 'then' key word is expected ")

        else:
            raise RuntimeError("Error: 'if' key word is expected ")
        return stmt

    def stmt_sequence(self):
        """
        @EXP
        Each time we are at this point in the program, we are called via root or if_stmt or repeat_stmt
        This means there's a connection between our node going up to whoever called us (or coming down from, if you will.)
        """
        sequence = [self.statement()]
        while((self.pointer<self.MaxPointerValue)and(self.TokenList[self.pointer].value== Tinylanguage.tiny_grammar["stmt_sequence"][0][1])):
            #store the semicolocn
            self.increment_ptr()

            sequence.append(self.statement())

        return sequence


    def statement(self):

        if(self.TokenList[self.pointer].value == "if" ):
            if self.debug:
                print("if statement")
            stmt = self.if_stmt()

        elif(self.TokenList[self.pointer].value == "repeat" ):
            if self.debug:
                print("repeat statement")
            stmt = self.repeat_stmt()

        elif(self.TokenList[self.pointer].type == "IDENTIFIER" ):
            if self.debug:
                print("assign statement")
            stmt = self.assign_stmt()

        elif(self.TokenList[self.pointer].value =="read"):
            if self.debug:
                print("read statement")
            stmt = self.read_stmt()

        elif(self.TokenList[self.pointer].value =="write"):
            if self.debug:
                print("write statement")
            stmt = self.write_stmt()
        else:
            raise RuntimeError("Invalid statement.") #mariam
        return stmt
if __name__ == "__main__":
    #TODO get the file name from user

    obj = NonTerminals("test.txt")
    obj.parse()
    obj.root.print_tree()
