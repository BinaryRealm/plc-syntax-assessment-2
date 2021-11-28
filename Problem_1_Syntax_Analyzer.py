import re
import sys
tokens=[]

special_symbols=["+", "-", "*", "/", "=", "(", ")", "{", "}", "[", "]", ">", "<", ";", "%", ":"]

keywords = ["for", "if", "else", "while", "do", "int", "float", "switch", "foreach", "return", "void", "main", "case", "default", "in"]

identifier = re.compile("[A-Za-z][A-Za-z0-9_]*")

number = re.compile("(0[0-7]*)(ul|UL|Ul|uL|lu|LU|Lu|lU|u|l|U|L)?|([1-9][0-9]*)(ul|UL|Ul|uL|lu|LU|Lu|lU|u|l|U|L)?|(0(x|X)[0-9A-Fa-f][0-9A-Fa-f]*)(ul|UL|Ul|uL|lu|LU|Lu|lU|u|l|U|L)?")

float = re.compile("[0-9][0-9]*(e|E)(\+|-)?[0-9][0-9]*(fl|FL|Fl|fL|lf|LF|Lf|lF|f|l|F|L)?|[0-9][0-9]*(\.)?(e|E)(\+|-)?[0-9][0-9]*(fl|FL|Fl|fL|lf|LF|Lf|lF|f|l|F|L)?|[0-9][0-9]*\.[0-9][0-9]*(e|E)(\+|-)?[0-9][0-9]*(fl|FL|Fl|fL|lf|LF|Lf|lF|f|l|F|L)?|[0-9][0-9]*\.[0-9][0-9]*(fl|FL|Fl|fL|lf|LF|Lf|lF|f|l|F|L)?|[0-9][0-9]*\.(fl|FL|Fl|fL|lf|LF|Lf|lF|f|l|F|L)?|\.[0-9][0-9]*(e|E)(\+|-)?[0-9][0-9]*(fl|FL|Fl|fL|lf|LF|Lf|lF|f|l|F|L)?|\.[0-9][0-9]*(fl|FL|Fl|fL|lf|LF|Lf|lF|f|l|F|L)?|0(x|X)[0-9A-Fa-f][0-9A-Fa-f]*(\.)?(p|P)(\+|-)?[0-9][0-9]*(fl|FL|Fl|fL|lf|LF|Lf|lF|f|l|F|L)?|0(x|X)[0-9A-Fa-f][0-9A-Fa-f]*\.[0-9A-Fa-f][0-9A-Fa-f]*(p|P)(\+|-)?[0-9][0-9]*(fl|FL|Fl|fL|lf|LF|Lf|lF|f|l|F|L)?|0(x|X)*\.[0-9A-Fa-f][0-9A-Fa-f]*(p|P)(\+|-)?[0-9][0-9]*(fl|FL|Fl|fL|lf|LF|Lf|lF|f|l|F|L)?")

whitespace = re.compile("\s")

def lexify(input):
    lexeme=""
    length = len(input)
    identifier_state = False
    number_state = False
    float_state = False
    i=0
    while i < length:
        lexeme+=input[i]
        if i!=length-1:
            if(len(lexeme)==1):
                m = identifier.fullmatch(lexeme)
                n = number.fullmatch(lexeme)
                if m:
                    identifier_state = True
                    if (input[i+1] in special_symbols) or (whitespace.fullmatch(input[i+1])):
                        tokens.append(("identifier", lexeme))
                        lexeme=""
                elif n:
                    number_state = True
                    if (input[i+1] in special_symbols) or (whitespace.fullmatch(input[i+1])):
                        tokens.append(("integer", lexeme))
                        lexeme=""
                elif lexeme=="." and float.fullmatch("."+input[i+1]):
                    number_state = True
                elif lexeme in special_symbols:
                    tokens.append(("special symbol", lexeme))
                    lexeme=""
                elif whitespace.fullmatch(lexeme):
                    lexeme=""
                else:
                    print("lexer error: invalid character")
                    break
            elif identifier_state==True:
                m = identifier.fullmatch(lexeme+input[i+1])
                if m:
                    ""
                else:
                    if (input[i+1] not in special_symbols) and (whitespace.fullmatch(input[i+1])==None) and (re.compile("[a-zA-Z0-9]").fullmatch(input[i+1])==None):
                        print("lexer error: invalid character")
                        break
                    identifier_state = False
                    if lexeme not in keywords:
                        tokens.append(("identifier", lexeme))
                    else:
                        for j in range(len(keywords)):
                            if lexeme == keywords[j]:
                                tokens.append((keywords[j]+"_code", 30+j))
                    lexeme=""
            elif number_state==True:
                m = number.fullmatch(lexeme+input[i+1])
                n = float.fullmatch(lexeme+input[i+1])
                if m:
                    ""
                elif n:
                    float_state = True
                else:
                    if input[i+1] not in special_symbols and whitespace.fullmatch(input[i+1])==None and input[i+1] not in ["e", "E", "p", "P", "."]:
                        print("lexer error: invalid character")
                        break
                    if float_state==True and ((input[i+1] in ["e", "E", "p", "P"]) or ((input[i] in ["e", "E", "p", "P"]) and (input[i+1] in ["+", "-"]))) or input[i+1]==".":
                        float_state = True
                    else:
                        if float_state:
                            tokens.append(("float", lexeme))
                        else:
                            tokens.append(("integer", lexeme))
                        number_state = False
                        lexeme=""
            i+=1
        else:
            if identifier.fullmatch(lexeme):
                added=False
                for j in range(len(keywords)):
                    if lexeme == keywords[j]:
                        tokens.append((keywords[j]+"_code", 30+j))
                        added=True
                if added==False:
                    tokens.append(("identifier", lexeme))
            elif number.fullmatch(lexeme):
                tokens.append(("integer", lexeme))
            elif float.fullmatch(lexeme):
                tokens.append(("float", lexeme))
            elif lexeme in special_symbols:
                tokens.append(("special symbol", lexeme))
            elif whitespace.fullmatch(lexeme):
                pass
            else:
                print("lexer error: invalid character")
            break
    tokens.append(("EOF", ""))
    print(tokens)
    print()
    lex.counter = 0
    lex.nextToken = tokens[0]

def error():
    sys.exit("SYNTAX ERROR")

def lex():
    lex.counter+=1
    lex.nextToken = tokens[lex.counter]

#SYNTAX ANALYSIS
#Note: All syntax follows the grammar rules of C except for the 
#foreach statement which follows the rules of C#



#<foreachstmt> -> foreach '(' (int|float) id in id ')' <stmt>
def foreachstmt():
    print("Enter <foreachstmt>")
    if lex.nextToken[0] != "foreach_code":
        error()
    else:
        print(lex.nextToken)
        lex()
        if lex.nextToken[1] != "(":
            error()
        else:
            print(lex.nextToken)
            lex()
            if lex.nextToken[0] != "int_code" and lex.nextToken[0] != "float_code":
                error()
            else:
                print(lex.nextToken)
                lex()
                if lex.nextToken[0] != "identifier":
                    error()
                else:
                    print(lex.nextToken)
                    lex()
                    if lex.nextToken[0] != "in_code":
                        error()
                    else:
                        print(lex.nextToken)
                        lex()
                        if lex.nextToken[0] != "identifier":
                            error()
                        else:
                            print(lex.nextToken)
                            lex()
                            if lex.nextToken[1] != ")":
                                error()
                            else:
                                print(lex.nextToken)
                                lex()
                                stmt()
    print("Exit <foreachstmt>")

#<forstmt> -> for "(" [<Expr>] ; [<expr>] ; [<Expr>] ")" <stmt>
#Note: Capitalized Expr includes assignments
def forstmt():
    print("Enter <forstmt>")
    if lex.nextToken[0] != "for_code":
        error()
    else:
        lex()
        if lex.nextToken[1] != "(":
            error()
        else: #(
            lex()
            if lex.nextToken[1] != ";": #(e
                Expr()
                if lex.nextToken[1] != ";":
                    error()
                else:
                    lex()
                    if lex.nextToken[1] != ";": #(e;e
                        expr()#intexpr()
                        if lex.nextToken[1] != ";":
                            error()
                        else:
                            lex()
                            if lex.nextToken[1] != ")":#(e;e;e
                                Expr()
                                if lex.nextToken[1] != ")":
                                    error()
                                else:#(e;e;e)
                                    lex()
                                    stmt()
                            else:#(e;e;)
                                lex()
                                stmt()
                    else:#(e;;
                        lex()
                        if lex.nextToken[1] != ")":#(e;;e
                            Expr()
                            if lex.nextToken[1] != ")":
                                error()
                            else:
                               lex()
                               stmt()
                        else:#(e;;)
                            lex()
                            stmt()
            else: #(;
                lex()
                if lex.nextToken[1] != ";": #(;e
                    expr()#intexpr()
                    if lex.nextToken[1] != ";":
                        error()
                    else:
                        lex()
                        if lex.nextToken[1] != ")":#(;e;e
                            Expr()
                            if lex.nextToken[1] != ")":
                                error()
                            else:#(;e;e)
                                lex()
                                stmt()
                        else:#(;e;)
                            lex()
                            stmt()
                else: #(;;
                    lex()
                    if lex.nextToken[1] != ")":#(;;e
                        Expr()
                        if lex.nextToken[1] != ")":
                            error()
                        else:#(;;e)
                            lex()
                            stmt()
                    else:#(;;)
                        if lex.nextToken[1] != ")":
                            error()
                        else:
                            lex()
                            stmt()
    print("Exit <forstmt>")

def switchState():
    pass
switchState.inSwitch=False
switchState.defaultCount=0

#<casestmt> -> case <expr> : <stmt>
#Note: only permitted to be used within a switch statement
def casestmt():
    print("Enter <casestmt>")
    if switchState.inSwitch==False:
        error()
    else:
        if lex.nextToken[0] != "case_code":
            error()
        else:
            print(lex.nextToken)
            lex()
            expr()
            if lex.nextToken[1] != ":":
                error()
            else:
                print(lex.nextToken)
                lex()
                stmt()
    print("Exit <casestmt>")

#<defaultstmt> -> default : <stmt>
#Note: only permitted to be used just one time within a switch statement
def defaultstmt():
    print("Enter <defaultstmt>")
    switchState.defaultCount+=1
    if switchState.inSwitch==False or switchState.defaultCount==2:
        error()
    else:
        if lex.nextToken[0] != "default_code":
            error()
        else:
            lex()
            if lex.nextToken[1] != ":":
                error()
            else:
                lex()
                stmt()
    print("Exit <defaultstmt>")

#<switchstmt> -> switch "(" <expr> ")" <stmt>
def switchstmt():
    print("Enter <switchstmt>")
    switchState.inSwitch=True
    if lex.nextToken[0] != "switch_code":
        error()
    else:
        print(lex.nextToken)
        lex()
        if lex.nextToken[1] != "(":
            error()
        else:
            print(lex.nextToken)
            lex()
            expr()
            if lex.nextToken[1] != ")":
                error()
            else:
                print(lex.nextToken)
                lex()
                stmt()
    switchState.inSwitch=False
    switchState.defaultCount=0
    print("Exit <switchstmt>")

#<whilestmt> -> while "(" <expr> ")"  <stmt>
def whilestmt():
    print("Enter <whilestmt>")
    if lex.nextToken[0] != "while_code":
        error()
    else:
        print(lex.nextToken)
        lex()
        if lex.nextToken[1] != "(":
            error()
        else:
            print(lex.nextToken)
            lex()
            expr()
            if lex.nextToken[1] != ")":
                error()
            else:
                print(lex.nextToken)
                lex()
                stmt()
    print("Exit <whilestmt>")


#<dowhilestmt> -> do <statement> while '(' <expr> ')' ';'
def dowhilestmt():
    print("Enter <dowhilestmt>")
    if lex.nextToken[0] != "do_code":
        error()
    else:
        print(lex.nextToken)
        lex()
        stmt()
        if lex.nextToken[0] != "while_code":
            error()
        else:
            print(lex.nextToken)
            lex()
            if lex.nextToken[1] != "(":
                error()
            else:
                print(lex.nextToken)
                lex()
                expr()
                if lex.nextToken[1] != ")":
                    error()
                else:
                    print(lex.nextToken)
                    lex()
                    if lex.nextToken[1] != ";":
                        error()
                    else:
                        lex()
    print("Exit <dowhilestmt>")

#<block> -> '{' {<stmt>} '}'
def block():
    print("Enter <block>")
    if lex.nextToken[1] != "{":
        error()
    else:
        lex()
        while(lex.nextToken[1] != "}"):
            stmt()
        print(lex.nextToken)
        lex()
    print("Exit <block>")
    pass

#<ifstmt> -> if "(" <expr> ")" <stmt> [else <stmt>]
def ifstmt():
    print("Enter <ifstmt>")
    if lex.nextToken[0] != "if_code":
        error()
    else:
        print(lex.nextToken)
        lex()
        if lex.nextToken[1] != "(":
            error()
        else:
            print(lex.nextToken)
            lex()
            expr()
            if lex.nextToken[1] != ")":
                error()
            else:
                print(lex.nextToken)
                lex()
                stmt()
                if lex.nextToken[0] == "else_code":
                    print(lex.nextToken)
                    lex()
                    stmt()
    print("Exit <ifstmt>")

#<assignment> -> id = <expr>
def assignment():
    print("Enter <assignment>")
    if lex.nextToken[0] != "identifier":
        error()
    else:
        print(lex.nextToken)
        lex()
        if lex.nextToken[1] != "=":
            error()
        else:
            print(lex.nextToken)
            lex()
            expr()
    print("Exit <assignment>")

#<returnstmt> -> return <expr>
def returnstmt():
    print("Enter <returnstmt>")
    if lex.nextToken[0] != "return_code":
        error()
    else:
        print(lex.nextToken)
        lex()
        expr()
    print("Exit <returnstmt>")

#<stmt> -> <switchstmt>|<foreachstmt>|<forstmt>|<whilestmt>|<dowhilestmt>|<block>|<ifstmt>|<assignment>';'|<returnstmt>';'
def stmt():
    print("Enter <statement>")
    if lex.nextToken[0] == "switch_code":
        switchstmt()
    elif lex.nextToken[0] == "foreach_code":
        foreachstmt()
    elif lex.nextToken[0] == "for_code":
        forstmt()
    elif lex.nextToken[0] == "while_code":
        whilestmt()
    elif lex.nextToken[0] == "do_code":
        dowhilestmt()
    elif lex.nextToken[1] == "{":
        block()
    elif lex.nextToken[0] == "if_code":
        ifstmt()
    elif lex.nextToken[0] == "identifier":
        assignment()
        print(lex.nextToken)
        if lex.nextToken[1] != ';':
            error()
        lex()
    elif lex.nextToken[0] == "return_code":
        returnstmt()
        print(lex.nextToken)
        if lex.nextToken[1] != ';':
            error()
        lex()
    elif lex.nextToken[0] == "case_code":
        casestmt() 
    elif lex.nextToken[0] == "default_code":
        defaultstmt()
    else:
        error()
    print("Exit <statement>")

#<program> -> void main '(' ')' <block>
def program():
    print("Enter <program>")
    if lex.nextToken[0] != "void_code":
        error()
    else:
        print(lex.nextToken)
        lex()
        if lex.nextToken[0] != "main_code":
            error()
        else:
            print(lex.nextToken)
            lex()
            if lex.nextToken[1] != "(":
                error()
            else:
                print(lex.nextToken)
                lex()
                if lex.nextToken[1] != ")":
                    error()
                else:
                    print(lex.nextToken)
                    lex()
                    block()
    print("Exit <program>")

#<Expr> -> <expr> | <assignment>
#note: used for for-loop
def Expr():
    print("Enter <Expr>")
    if tokens[lex.counter][0]=="identifier" and tokens[lex.counter+1][1]=="=":
        assignment()
    else:
        expr()
    print("Exit <Expr>")    

#<expr> -> <term> {(+ | -) <term>}
def expr():
    print("Enter <expr>")
    term()
    while lex.nextToken[1] == '+' or lex.nextToken[1] == '-':
        print(lex.nextToken)
        lex()
        term()
    print("Exit <expr>")

#<term> -> <factor> {(* | /| %) <factor>}
def term():
    print("Enter <term>")
    factor()
    while lex.nextToken[1] == '*' or lex.nextToken[1] == '/' or lex.nextToken[1] == '%':
        print(lex.nextToken)
        lex()
        factor()
    print("Exit <term>")

#<factor> -> id | int_constant | float_constant | ( <expr> )
def factor():
    print("Enter <factor>")
    if lex.nextToken[0] == "identifier" or lex.nextToken[0] == "integer" or lex.nextToken[0] == "float":
        print(lex.nextToken)
        lex()
    else:
        if lex.nextToken[1] == "(":
            print(lex.nextToken)
            lex()
            expr()
            if lex.nextToken[1] == ")":
                print(lex.nextToken)
                lex()
            else:
                error()
        else:
            error()
    print("Exit <factor>")



#lexer test
"""
int i=1;
for if(float x==0) float switch
 07 while 1234u hello_world + 123.456e-67 { } 0.56 abc1 0x1.ep+3 2.0e+308 1.0e-324"""



code ="""
void main(){
    foreach(int x in list){
        y=x;
    }

    switch(x){
        case 1: 
            return 1;
        case 2: 
            return 2;
        default:
            return 3;
    }

    if(2+2){
        ijk = (sum + 47) / total;
    }
    else{
        j=2;
        k=3;
        return 2+5 ;
    }
    while(1){
        return 1+1;
    }
        x=2;
}
"""
lexify(code)
program()

if(lex.counter+1) != len(tokens):
    error()