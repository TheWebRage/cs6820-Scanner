from os.path import exists


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


# Returns a new file path with the extension passed in
def getNewFilePath(filePath, extension):
    splitFile = filePath.split('/')
    folderPath = flatten(splitFile[:-1], '/') # TODO: check length before taking off extension?
    return folderPath + splitFile[-1].split('.')[0] + extension


# Logs the error in xxx.err and in the console
def logError(errorString, filePath, lineNumber):
    errorString += f"ERROR: Line {str(lineNumber)} - {errorString}"

    # Printing error to console would be nice too
    print(errorString)
    
    # Errors print to xxx.err and say something like 'Error: There was as error on line x'
        # If error is produced ignore anything in xxx.asm file
    file = open(getNewFilePath(filePath, '.err'), 'w')
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
        return 'imul' # TODO: make this a looped muli command


# Checks the line for a math operand passed in and preforms correct logic, including call math recursively
def mathCheckLine(operand, symbolTable, line):
    outputString = ""

    lineSplit = line.split(operand)

    # read any values from memory needed # Use math() again for this
    if operand == '^':
        outputString += math(symbolTable, lineSplit[0], 'eax') # TODO: fix exponents
    outputString += math(symbolTable, flatten(lineSplit[1], operand), 'ebx')

    # preform math operation
    outputString += f'{operandToAsm(operand)} eax, ebx\n'

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

    # TODO: maybe save varType from symbolTable?

    line = line.replace(" ", "")
    lineSplit = line.split("=")

    varName = lineSplit[0]

    # Perform math and save value
    if '=' in line:
        outputString += math(symbolTable, lineSplit[1])

    # No variable name is same as a keyword
    if isKeyword(varName):
        raise SyntaxError(f"{varName} is a reserved keyword. Please use something else.")

    # No two vars initialized use same name
    elif isInit and varName in symbolTable:
        raise SyntaxError(f'{varName} was already declared. ')
    
    elif isInit:
        # Keep track of vars types
        symbolTable.update({varName: varType})

    else:
        # Save value back to memory
        outputString += f'mov [{lineSplit[0]}], eax\n\n'

    return outputString


# returns the result of an arithmetic sequence
def math(symbolTable, line, reg = 'eax'):
    outputString = ""
    # Arithmetic - Check for highest PEMDAS operator
    # Parenthesis - Not needed to support in this version

    # Exponent
    if '^' in line:
        mathLine = line.split('^')
        outputString += f'mov eax, {mathLine[0]}\n'

        for i in range(0, int(mathLine[1])):
            outputString += mathCheckLine('^', symbolTable, line)

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
        # Store variable into ebx register
        outputString += f"mov {reg}, [{line}]\n"
        
    elif isDigit(line):
        outputString += f"mov {reg}, {line}\n"

    else:
        # Error is produced if var is used before it is declared
        raise SyntaxError(f'{line} was not declared.')

    return outputString


# Write Statement - Writes to console
def write(symbolTable, line):
    outputString = ''
    line = getLine(line).replace("write ", "")

    # Write out a number
    if isDigit(line):
        outputString = f'push %rbx\nlea  intFormat(%rip), %rdi\nmov  $1, {line}\nxor %eax, %eax\ncall printf\npop %rbx\n\n'
    
    # Write out a variable
    elif line in symbolTable: # TODO: make work for other types of vars
        outputString = f'push %rbx\nlea  intFormat(%rip), %rdi\nmov  $1, [{line}]\nxor %eax, %eax\ncall printf\npop %rbx\n\n'
    
    # Write out a string
    else:
        line.replace("\"", "")

        for i in range(0, len(line))[::4]: # TODO: finish this print stuff
            outputString = f"""mov  ecx, "{line}" 
                                mov  [stringBuffer + {i}], ecx
                                call _printString"""

    outputString += """mov  ecx, 0xA 
                        mov  [stringBuffer], ecx
                        call _printString"""

        # <EXP> part it optional
    return outputString


# Returns the data section for the beginning of the file
def getTopSection(symbolTable):
    # After each write statement is always a new line
    outputString = 'extern printf\n\nsection .data\nstringFormat: .asciz "%s\\n"\nintFormat: .asciz "%d\\n"\n'

    for var in symbolTable:
        outputString += f'{var}: dd 0\n'

    outputString += """global _start

                    sys_exit        equ     1
                    sys_write       equ     4
                    stdout          equ     1

                    section .text

                    _printString: 
                    ; calculate the length of string
                        mov     rdi, stringBuffer   ; stringBuffer to destination index
                        xor     rcx, rcx            ; zero rcx
                        not     rcx                 ; set rcx = -1
                        xor     al,al               ; zero the al register (initialize to NUL)
                        cld                         ; clear the direction flag
                        repnz   scasb               ; get the string length (dec rcx through NUL)
                        not     rcx                 ; rev all bits of negative results in absolute value
                        dec     rcx                 ; -1 to skip the null-terminator, rcx contains length
                        mov     rdx, rcx            ; put length in rdx

                    ; write string to stdout
                        mov     rsi, stringBuffer   ; stringBuffer to source index
                        mov     rax, 1              ; set write to command
                        mov     rdi,rax             ; set destination index to rax (stdout)
                        syscall                     ; call kernel

                        ret
                        
                    _start:\n"""

    return outputString


# Accept command line arguments
# TODO: add command line arguments
filePath = './src/basics.txt' 
# TODO: Use program name to create output files
outputString = ''
symbolTable = {}
isComment = False
lineNumber = 0

try:
    # Error is produced if file does not exist
    if exists(filePath) == False:
        raise FileNotFoundError(f'{filePath} was not found. Please enter a valid path')
    else:
        pass
        # Creates xxx.asm and xxx.err if file exists
        open(getNewFilePath(filePath, '.asm'), 'w').close()
        open(getNewFilePath(filePath, '.err'), 'w').close()

    # Read in file into memory
    file = open(filePath, 'r').readlines()

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
                # TODO: add in program name for output file names
            elif command == 'begin':
                foundCommand = True
                # TODO: add in start block
            elif command == 'end':
                foundCommand = True
                # TODO: add in end block

            # Don't need to store other types of variables for now
            # Detects 'num ' (with space) to know new var declaration
            # Save asm to output
            elif command == 'num ' or '=' in command:
                foundCommand = True
                outputString += saveVarIntoTable(symbolTable, line, command)

            elif command == 'write':
                foundCommand = True
                outputString += write(symbolTable, line)
            
            if foundCommand:
                break

    outputStringHeader = getDataSection(symbolTable)
    outputString = f'{outputStringHeader}\n{outputString}'
    
    # Output asm to xxx.asm
    file = open(getNewFilePath(filePath, '.asm'), 'w')
    file.write(outputString)
    file.close()


# Output and errors to xxx.err and stop program # Always create even if empty # Only create one file (xxx.err) if we cannot determine input program name
except Exception as error:
    logError(repr(error), filePath, lineNumber)
