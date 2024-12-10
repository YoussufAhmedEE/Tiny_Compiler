
# @dataclass
class Token:
    def __init__(self, value, type):
        self.type = type
        self.value = value
    def __str__(self):
        return f"{self.value}, {self.type}"

class Scanner:
    symbols = {
        ";": "SEMICOLON",
        "<": "LESSTHAN",
        "=": "EQUAL",
        "+": "PLUS",
        "-": "MINUS",
        "*": "MULT",
        "/": "DIV",
        "(": "OPENBRACKET",
        ")": "CLOSEDBRACKET",
        ":=": "ASSIGN",
        "if": "IF",
        "then": "THEN",
        "else":"ELSE",
        "end": "END",
        "repeat": "REPEAT",
        "until": "UNTIL",
        "read": "READ",
        "write": "WRITE",
    }
    def __init__(self):
        pass
    def __init__(self, file_contents: str):
        self.file_contents = file_contents + "$"
        self.token_list = []
        self._found_space = False  # Used in adding tokens
        self._parse_contents()

    def __str__(self):
        return '\n'.join(str(obj) for obj in self.token_list)

    def _parse_contents(self):
        inside_comment_flag = False
        inside_identifier_flag = False
        inside_number_flag = False

        current_token_string = ""

        for character in self.file_contents:
            if character == "{":
                inside_identifier_flag = False
                inside_number_flag = False
                inside_comment_flag = True
                self._add_token(current_token_string)
                current_token_string = ""

            elif character == "}":
                inside_comment_flag = False
                continue
            if inside_comment_flag:
                continue
            
            elif not character.isalpha() and not character.isdigit():
                inside_identifier_flag = False
                inside_number_flag = False

            elif character.isalpha() and not inside_identifier_flag:
                inside_identifier_flag = True
                inside_number_flag = False

            elif character.isdigit() and not inside_number_flag:
                inside_identifier_flag = False
                inside_number_flag = True

            else:
                current_token_string += character
                continue

            self._add_token(current_token_string)
            current_token_string = character

    def _check_for_space_character(self, unstripped_token: str):
        token = unstripped_token.strip()
        if token and token[-1] == unstripped_token[-1]:
            return False
        else:
            return True

    def _check_for_assign_symbol(self, unstripped_token: str):
        token = unstripped_token.strip()
        if token == "=" \
            and self.token_list and self.token_list[-1].value == ":" \
            and not self._found_space:
                self.token_list.pop()
                token = ":" + token

        #adding elif to recognize colon ":" with no following equal "=" 
        elif token != "=" \
            and self.token_list and self.token_list[-1].value == ":" \
            and not self._found_space:
                self.token_list.pop()
                raise RuntimeError("Error: Unknown Parameter \":\" " )

        self._found_space = self._check_for_space_character(unstripped_token)
        return token

    def _add_token(self, unstripped_token: str):
        if not unstripped_token:
            return

        token = unstripped_token.strip()
        token = self._check_for_assign_symbol(unstripped_token)
        if token in Scanner.symbols:
            self.token_list.append(Token(token, Scanner.symbols[token]))
        elif token.isalpha():
            self.token_list.append(Token(token, "IDENTIFIER"))
        elif token.isdigit():
            self.token_list.append(Token(token, "NUMBER"))
        elif token==':' :
            self.token_list.append(Token(token, "CheckTheNext"))
        elif token:
            raise RuntimeError("Error: Unknown Parameter : ", token)
    



def scan(file_path: str):
        import FileHandler as fh
        file_contents = fh.FileHandler.read_file(file_path)
        scanner_object = Scanner(file_contents)
        fh.FileHandler.write_file("./", "Tokens.txt" ,scanner_object)
        return scanner_object.token_list
        
