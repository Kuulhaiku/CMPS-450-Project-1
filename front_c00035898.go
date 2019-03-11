/*
Sebesta Scanner translated from C++ to Go
By Chau Cao - c00035898
I certify that the following implementation is my own  work.
*/
package main
//factored import statement
import (
  "bufio"
  "fmt"
  "io"
  "strings"
  "unicode"
  "os"
)

//constant variable block
const (
  LETTER = 0
  DIGIT = 1
  UNKNOWN = 99
  INT_LIT = 10
  IDENT = 11
  ADD_OP = 21
  SUB_OP = 22
  MULT_OP = 23
  DIV_OP = 24
  LEFT_PAREN = 25
  RIGHT_PAREN = 26
  EOF = -1
)

//global variable declaration block
var(
  charClass int
  lexeme strings.Builder
  nextChar rune
  token int
  nextToken int
  rbuff * bufio.Reader
)

//addChar()
//Writes the nextCHar rune into Lexeme from the buffer
func addChar() {
  lexeme.WriteRune(nextChar)
}

//getChar()
//Gets the next character and sets charClass to the appropriate variable
func getChar() {
  tempChar, sizeRune, err := rbuff.ReadRune()
  nextChar = tempChar //experienced issues using ReadRune due to error declaration so established a temp variable
  if sizeRune == 1{ //sizeRune use necessary for program to compile

  }

  //sets charClass to EOF if EOF reached
  if err != nil{
    if err == io.EOF {
      charClass = EOF
    }
  } else { //else sets charClass
    if unicode.IsLetter(nextChar) == true {
      charClass = LETTER
    } else if unicode.IsDigit(nextChar) == true {
      charClass = DIGIT
    } else {
      charClass = UNKNOWN
    }
  }
}

//getNonBlank()
//Loops getting characters until the read character is not a space
func getNonBlank() {
  for {
    if unicode.IsSpace(nextChar) == true {
      getChar()
    } else {
      break
    }
  }
}

//lookUp()
//when charClass is unknown. determines what token is read
//defaults to EOF
//not sure why it returns a value, but i translated the code as specified
func lookUp(ch rune) int {
  switch ch {
  case 40://'/u002':
    addChar()
    nextToken = LEFT_PAREN
    break
  case 41://'/u0029':
    addChar()
    nextToken = RIGHT_PAREN
    break
  case 43://'/u002B':
    addChar()
    nextToken = ADD_OP
    break
  case 45://'/u002D':
    addChar()
    nextToken = SUB_OP
    break
  case 42://'/u002A':
    addChar()
    nextToken = MULT_OP
    break
  case 47://'/u002F':
    addChar()
    nextToken = DIV_OP
    break
  default:
    addChar()
    nextToken = EOF
    break
  }
  return nextToken
}

//lex()
//driver function of scanner
//clears buffer at each iteration and gets a getNonBlank
//switch controller based on character class
//LETTER loops until a non alphanumeric read in
//DIGIT loops until a non decimal digit is read in
//UNKOWN looks up the token.
//EOF ends operation
func lex() {
  lexeme.Reset()
  getNonBlank()
  switch charClass {
  case LETTER:
    addChar()
    getChar()
    for {
      if charClass == LETTER || charClass == DIGIT {
        addChar()
        getChar()
      } else {
        break
      }
    }
    break
  case DIGIT:
    addChar()
    getChar()
    for {
      if charClass == DIGIT {
        addChar()
        getChar()
      } else {
        break
      }
    }
    break
  case UNKNOWN:
    lookUp(nextChar)
    getChar()
    break
  case EOF:
    nextToken = EOF
    lexeme.WriteString("EOF")
    break
  }
  fmt.Printf("Next token is: %d, Next Lexeme is: %s\n", nextToken, lexeme.String())
}

//main function.
//attempts to open front.in which will be located in the same directory as exe
//if not present, throw exception
//else initialize bufio reader, call getChar and loop lex until EOF
func main() {
  in_fp, err := os.Open("front.in")
  if err != nil {
    fmt.Printf("Cannot open front.in\n")
    cwd, derr := os.Getwd()
    if derr == nil {
      fmt.Printf("Current working dir: %s \n", cwd)
    }
  } else {
    rbuff = bufio.NewReader(in_fp)
    getChar()
    for {
      if nextToken != EOF {
        lex()
      } else {
        break
      }
    }
  }
}
