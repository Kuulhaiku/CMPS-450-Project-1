#Sebesta Scanner translated from C++ to Python
#By Chau Cao - c00035898
#I certify that the following implementation is my own  work.

#Import Constants definitions and OS library
import sebestaScannerConstants, os

#global variable declaration block
charClass = 0
lexeme = ""
nextChar = " "
nextToken = 0
in_fp = open("front.in", "r")

#addChar()
#Writes the nextCHar into Lexeme
def addChar():
    global lexeme, nextChar
    lexeme += nextChar

#getChar()
#Gets the next character and sets charClass to the appropriate variable
def getChar():
    global nextChar, in_fp, charClass
    nextChar = in_fp.read(1)
    if nextChar == "":
        charClass = sebestaScannerConstants.EOF
    else:
        if nextChar.isalpha():
            charClass = sebestaScannerConstants.LETTER
        elif nextChar.isdigit():
            charClass = sebestaScannerConstants.DIGIT
        else:
            charClass = sebestaScannerConstants.UNKNOWN

#getNonBlank()
#Loops getting characters until the read character is not a space
def getNonBlank():
    global nextChar
    while nextChar.isspace() == True:
        getChar()

#The following functions are used to create a dictionary for a switch like statement
#The swap is based on the value of nexChar
def leftParen():
    global nextToken
    addChar()
    nextToken = sebestaScannerConstants.LEFT_PAREN

def rightParen():
    global nextToken
    addChar()
    nextToken = sebestaScannerConstants.RIGHT_PAREN

def addOp():
    global nextToken
    addChar()
    nextToken = sebestaScannerConstants.ADD_OP

def subOp():
    global nextToken
    addChar()
    nextToken = sebestaScannerConstants.SUB_OP

def multOp():
    global nextToken
    addChar()
    nextToken = sebestaScannerConstants.MULT_OP

def divOp():
    global nextToken
    addChar()
    nextToken = sebestaScannerConstants.DIV_OP

def defaultCase():
    global nextToken
    addChar()
    nextToken = sebestaScannerConstants.EOF


#lookUp()
#when charClass is unknown. determines what token is read
#defaults to EOF
def lookup():
    lookUpSwitch = {
        '(': leftParen,
        ')': rightParen,
        '+': addOp,
        '-': subOp,
        '*': multOp,
        '/': divOp
    }
    global nextChar
    func = lookUpSwitch.get(nextChar, defaultCase)
    func()

#The following functions are used to create a dictionary for a switchlike statement
#see lex() comments for further information
def letter():
    global charClass, nextToken
    addChar()
    getChar()
    while charClass == sebestaScannerConstants.LETTER or charClass == sebestaScannerConstants.DIGIT:
        addChar()
        getChar()
    nextToken = sebestaScannerConstants.IDENT

def lexdigit():
    global charClass, nextToken
    addChar()
    getChar()
    while charClass == sebestaScannerConstants.DIGIT:
        addChar()
        getChar()
    nextToken = sebestaScannerConstants.INT_LIT

def unknown():
    global nextChar
    lookup()
    getChar()

def endOF():
    global nextToken, lexeme
    nextToken = sebestaScannerConstants.EOF
    lexeme = "EOF"


#lex()
#driver function of scanner
#clears buffer at each iteration and gets a getNonBlank
#switch controller based on character class
#LETTER loops until a non alphanumeric read in
#DIGIT loops until a non decimal digit is read in
#UNKOWN looks up the token.
#EOF ends operation
def lex():
    lexSwitcher = {
      sebestaScannerConstants.LETTER: letter,
      sebestaScannerConstants.DIGIT: lexdigit,
      sebestaScannerConstants.UNKNOWN: unknown,
      sebestaScannerConstants.EOF: endOF
    }
    global lexeme, charClass, nextToken
    lexeme = ""
    getNonBlank()
    func = lexSwitcher.get(charClass)
    func()
    print ("Next token is: ", nextToken, ", Next Lexeme is: ", lexeme)


#main function.
#attempts to open front.in which will be located in the same directory as exe
#if not present, throw exception
#else call getChar and loop lex until EOF
def main():
    global in_fp
    try:
        in_fp = open("front.in", "r")
    except IOError:
        print ("ERROR: Cannot open front.in")
        cwd = os.getcwd()
        if cwd != "":
            print ("Current working dir: ", cwd)
        else:
            print ("getcwd error")
    else:
        getChar()
    while True:
        lex()
        if nextToken == sebestaScannerConstants.EOF:
            break

if __name__ == "__main__": main()
