tiny_grammar = {
    "program": ["stmt_sequence"],
    
    "stmt_sequence": [
        ["stmt_sequence", ";", "statement"],
        ["statement"]
    ],
    "statement": [
        ["if_stmt"],
        ["repeat_stmt"],
        ["assign_stmt"],
        ["read_stmt"],
        ["write_stmt"]
    ],
    "if_stmt": [
        ["if", "exp", "then", "stmt_sequence", "end"],
        ["if", "exp", "then", "stmt_sequence", "else", "stmt_sequence", "end"]
    ],
    "repeat_stmt": [
        ["repeat", "stmt_sequence", "until", "exp"]
    ],
    "assign_stmt": [
        ["IDENTIFIER", ":=", "exp"]
    ],
    "read_stmt": [
        ["read", "IDENTIFIER"]
    ],
    "write_stmt": [
        ["write", "exp"]
    ],
    "exp": [
        ["simple_exp", "comparison_op", "simple_exp"],
        ["simple_exp"]
    ],
    "comparison_op": [
        ["<"],
        ["="]
    ],
    "simple_exp": [
        ["simple_exp", "addop", "term"],
        ["term"]
    ],
    "addop": [
        ["+"],
        ["-"]
    ],
    "term": [
        ["term", "mulop", "factor"],
        ["factor"]
    ],
    "mulop": [
        ["*"],
        ["/"]
    ],
    "factor": [
        ["(", "exp", ")"],
        ["NUMBER"],
        ["IDENTIFIER"]
    ]
}


