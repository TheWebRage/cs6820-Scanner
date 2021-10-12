from os.path import exists
import sys

immediateName = 0

# Returns a string from the combined elements in a list
def flatten(listObject, seperator = ""):
    if not isinstance(listObject, list):
        return listObject

    returnString = ''
    for string in listObject:
        returnString += string + seperator
    return returnString


# Returns the line up to the semi-colon
def getLine(line):
    command = ""

    for char in line:
        # Remove spaces at beginning of line
        if char == ' ' and command == '':
            continue
        elif char == '\t':
            continue
        elif char == ';':
            break

        command += char
    
    return command


# Returns the folder path of the file
def getFolderPath(filePath):
    splitFile = filePath.split('/')
    return flatten(splitFile[:-1], '/')

# Returns a new file path with the extension passed in
def getNewFilePath(filePath, extension):
    splitFile = filePath.split('/')
    return getFolderPath(filePath) + splitFile[-1].split('.')[0] + extension


# Logs the error in xxx.err and in the console
def logError(errorString, outputFile, lineNumber):
    errorString += f"ERROR: Line {str(lineNumber)} - {errorString}"

    # Printing error to console would be nice too
    print(errorString)
    
    # Errors print to xxx.err and say something like 'Error: There was as error on line x'
        # If error is produced ignore anything in xxx.asm file
    file = open(getNewFilePath(outputFile, '.err'), 'w')
    file.write(errorString)


# Checks to see if passed string is a keyword for the language
def isKeyword(inputString):
    keywords = ["num", "write", "begin", "program", "end"]

    for keyword in keywords:
        if inputString == keyword:
            return True
    
    return False


# Checks to see if the input is a digit
def isDigit(inputString):
    try:
        a = int(inputString)
        return True
    except:
        return False


# Gets the asm instruction for the operand
def operandToAsm(operand):
    if operand == "+":
        return 'add'
    if operand == "-":
        return 'sub'
    if operand == "*":
        return 'imul'
    if operand == "^":
        return 'imul'


# Checks the line for a math operand passed in and preforms correct logic, including call math recursively
def mathCheckLine(operand, symbolTable, line):
    outputString = ""

    lineSplit = line.split(operand)

    # read any values from memory needed # Use math() again for this
    outputString += math(symbolTable, lineSplit[0], 'r8')

    if operand == '^':
        pass
        # outputString += math(symbolTable, lineSplit[0], 'rbx')
    else:
        outputString += math(symbolTable, flatten(lineSplit[1], operand), 'r9')

    # preform math operation
    outputString += f'{operandToAsm(operand)} r8, r9\n'
    outputString += f'mov rax, r8\n'

    # save value of register into memory address

    return outputString


# Symbol Table # Get variable name and value; Store into symbol table; throw error if variable name is invalid
def saveVarIntoTable(symbolTable, line, varType = ""):
    outputString = ""

    # Check if variable is being initialized
    isInit = (varType not in symbolTable) and (varType == 'num ')

    # Parse line for command
    line = getLine(line)

    # If initializing, then remove varType at beginning of line
    if isInit:
        line = line.replace(varType, "")

    line = line.replace(" ", "")
    lineSplit = line.split("=")

    varName = lineSplit[0]

    # No variable name is same as a keyword
    if isKeyword(varName):
        raise SyntaxError(f"{varName} is a reserved keyword. Please use something else.")

    # No two vars initialized use same name
    elif isInit and varName in symbolTable:
        raise SyntaxError(f'{varName} was already declared. ')
    
    elif isInit:
        # Keep track of vars names in asm
        symbolTable.update({varName: f'var{len(symbolTable)}_{varName}'})

    elif '=' not in line:
        # Save value back to memory
        outputString += f'mov [qword {symbolTable[lineSplit[0]]}], rax\n'

    # Perform math and save value
    if '=' in line:
        outputString += math(symbolTable, lineSplit[1])
        outputString += f'mov [qword {symbolTable[lineSplit[0]]}], rax\n\n'

    return outputString


# returns the result of an arithmetic sequence
def math(symbolTable, line, reg = 'rax'):
    outputString = ""
    # Arithmetic - Check for highest PEMDAS operator
    # Parenthesis - Not needed to support in this version

    # Exponent
    if '^' in line:
        mathLine = line.split('^')

        if 'immediateName' not in globals():
            global immediateName
            immediateName = 0
        else:
            immediateName += 1

        outputString += math(symbolTable, mathLine[1], reg = 'r9')
        outputString += math(symbolTable, mathLine[0], reg = 'r8')

        outputString += f"""xor     rdi, rdi
mov     rax, 1
mov     rdx, r9

exp_start{immediateName}:
cmp rdi, rdx
jz exp_done{immediateName}
imul rax, r8
inc rdi
jmp exp_start{immediateName}

exp_done{immediateName}:
"""


    # Multiplication
    elif '*' in line:
        outputString += mathCheckLine('*', symbolTable, line)

    # Division - Not needed to support in this version

    # Addition
    elif '+' in line:
        outputString += mathCheckLine('+', symbolTable, line)

    # Subtraction
    elif '-' in line:
        outputString += mathCheckLine('-', symbolTable, line)

    # Default if none are found, return the value if found in symbolTable
    elif line in symbolTable:
        # Store variable into rbx register
        outputString += f"mov rax, [qword {symbolTable[line]}]\n"
        outputString += f'mov {reg}, rax\n'
        
    elif isDigit(line):
        outputString += f"mov rax, {line}\n"
        outputString += f'mov {reg}, rax\n'

    else:
        # Error is produced if var is used before it is declared
        raise SyntaxError(f'{line} was not declared.')

    return outputString


# Returns the asm for a print string (Includes splitting the string into sections of 4 chars)
def asmSplitAndPrintString(line):
    outputString = ''
    line = line.replace("\"", "")

    for i in range(0, len(line))[::4]:          
        sectionsOfFour = ''

        for j in range(0, 4):
            if (i + j < len(line)):
                sectionsOfFour += line[i + j]

        outputString += asmPrintToConsole(sectionsOfFour, offset = i)

    return outputString + "call printString\n\n\n"


# Returns the asm for a print to console command
def asmPrintToConsole(stringToConsole, offset = 0, isLabel = False):
    if isDigit(stringToConsole):# Add digit support here
        return f"""mov  rax, {stringToConsole} 
call printInt\n\n"""

    if isLabel:
        return f"""mov  rax, [qword {stringToConsole}] 
call printInt\n\n"""

    return f"""mov  rax, {stringToConsole}
call printString\n\n"""


# Write Statement - Writes to console
def write(symbolTable, stringValues, line):
    outputString = ''
    line = getLine(line).replace("write ", "").strip()

    # Write out a number or variable
    if isDigit(line) or line in symbolTable:
        outputString += asmPrintToConsole(symbolTable[line], isLabel = line in symbolTable)
    
    # Write out a string
    else:
        consoleString = line.replace("\"", '')
        stringValues[consoleString] = f'string{len(stringValues)}'
        outputString += asmPrintToConsole(stringValues[consoleString])
    
        # <EXP> part it optional
    return outputString


# Returns the data section for the beginning of the file
def getTopSection(symbolTable, stringValues):
    # After each write statement is always a new line
    outputString = """;-----------------------------
; exports
;-----------------------------
GLOBAL main

;-----------------------------
; imports
;-----------------------------
extern printf

;-----------------------------
; initialized data
;-----------------------------
section .data
"""

    outputString += f'\n    ; Variable Values\n'
    for var in symbolTable:
        outputString += f'    {symbolTable[var]}: dq 0\n'
    
    outputString += f'\n    ; String Values\n'
    for stringValue in stringValues:
        outputString += f'    {stringValues[stringValue]}: dq "{stringValue}"\n'

    outputString += f'\n    ; Formats\n'
    outputString += """    stringBuffer   db "%s", 0xA, 0
    intBuffer   db "%d", 0x0d, 0x0a, 0

;-----------------------------
; Code! (execution starts at main
;-----------------------------
section .text
printInt:
        ; We need to call printf, but we are using rax, rbx, and rcx.  printf
        ; may destroy rax and rcx so we will save these before the call and
        ; restore them afterwards.
        push    rbp                     ; Avoid stack alignment isses
        push    rax                     ; save rax and rcx
        push    rcx

        mov     rdi, intBuffer      ; set printf format parameter
        mov     rsi, rax                ; set printf value paramete
        xor     rax, rax                ; set rax to 0 (number of float/vector regs used is 0)

        call    [rel printf wrt ..got]
        pop     rcx                     ; restore rcx
        pop     rax                     ; restore rax
        pop     rbp                     ; Avoid stack alignment issues
        ret

printString: 
        ; We need to call printf, but we are using rax, rbx, and rcx.  printf
        ; may destroy rax and rcx so we will save these before the call and
        ; restore them afterwards.
        push    rbp                     ; Avoid stack alignment issues
        push    rax                     ; save rax and rcx
        push    rcx

        mov     rdi, stringBuffer       ; set printf format parameter
        mov     rsi, rax                ; set printf value paramete
        xor     rax, rax                ; set rax to 0 (number of float/vector regs used is 0)

        call    [rel printf wrt ..got]
        pop     rcx                     ; restore rcx
        pop     rax                     ; restore rax
        pop     rbp                     ; Avoid stack alignment issues
        ret


main:\n"""

    return outputString


# Accept command line arguments
outputFile = sys.argv[1] 

outputString = ''
symbolTable = {}
stringValues = {}
isComment = False
lineNumber = 0

try:
    # Error is produced if file does not exist
    if exists(outputFile) == False:
        raise FileNotFoundError(f'{outputFile} was not found. Please enter a valid path')

    # Read in file into memory
    file = open(outputFile, 'r').readlines()

    # Scan over each line
    for line in file:
        
        command = ''
        foundCommand = False
        lineNumber += 1

        for char in line:

            # Remove spaces at beginning of line
            if char == ' ' and command == '':
                continue
            elif char == '\t':
                continue

            command += char

            # Ignore comments / Both '//' and '/* */'
            if isComment and command == '*/':
                isComment = False
            elif command == '//':
                break
            elif command == '/*':
                isComment = True
                break
            if isComment:
                continue

            # Handle Boilerplate
            elif command == 'program ':
                foundCommand = True
                outputFile = getFolderPath(outputFile) + flatten(line.replace(command, '').replace(';', '').strip())
            elif command == 'begin':
                foundCommand = True
            elif command == 'end':
                foundCommand = True
                # TODO: add in end block

            # Don't need to store other types of variables for now
            # Detects 'num ' (with space) to know new var declaration
            # Save asm to output
            elif command == 'num ' or '=' in command:
                foundCommand = True
                outputString += f';{line}'
                outputString += saveVarIntoTable(symbolTable, line, command)

            elif command == 'write':
                foundCommand = True
                outputString += f';{line}'
                outputString += write(symbolTable, stringValues, line)
            
            if foundCommand:
                break

    outputStringHeader = getTopSection(symbolTable, stringValues)

    endString = """mov       rax, 60                 ; system call for exit
xor       rdi, rdi                ; exit code 0
syscall                           ; invoke operating system to exit\n\n"""

    outputString = f'{outputStringHeader}\n{outputString}\n{endString}'
    
    # Output asm to xxx.asm
    # Creates xxx.asm and xxx.err if file exists
    open(getNewFilePath(outputFile, '.err'), 'w').close()
    file = open(getNewFilePath(outputFile, '.asm'), 'w')
    file.write(outputString)
    file.close()


# Output and errors to xxx.err and stop program # Always create even if empty # Only create one file (xxx.err) if we cannot determine input program name
except Exception as error:
    logError(repr(error), outputFile, lineNumber)
