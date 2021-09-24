from os.path import exists


# Returns a string from the combined elements in a list
def flatten(list, seperator = ""):
    returnString = ''
    for string in list:
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
            break;

        command += char
    
    return command


# Returns a new file path with the extension passed in
def getNewFilePath(filePath, extension):
    splitFile = filePath.split('/')
    folderPath = flatten(splitFile[:-1], '/') # TODO: check length before taking off extension?
    return folderPath + splitFile[-1].split('.')[0] + extension


# Logs the error in xxx.err and in the console
def logError(errorString, filePath, lineNumber):
    errorString += "ERROR: Line " + lineNumber + " - " + errorString

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


# Checks the line for a math operand passed in and preforms correct logic, including call math recursively
def mathCheckLine(operand, symbolTable, line):
    lineSplit = line.split(operand)
    if len(lineSplit) > 1:
        # TODO: Generate asm for first two operands, then preform math on the rest
        #math(symbolTable, flatten())
    
    # TODO: return asm equivelent
    # read any values from memory needed # Use math() again for this
    # preform math operation
    # save value of register into memory address


# Symbol Table # Get variable name and value; Store into symbol table; throw error if variable name is invalid
def saveVarIntoTable(symbolTable, line, varType = ""):
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

    # Convert value to correct type
    if varType == "num ":
        varValue = math(symbolTable, line) if len(lineSplit) > 1 else 0 

    # No variable name is same as a keyword
    if isKeyword(varName):
        raise SyntaxError(inputString + " is a reserved keyword. Please use something else.")

    # No two vars initialized use same name
    elif isInit and varName in symbolTable:
        raise SyntaxError(varName + ' was already declared. ')

    # Keep track of vars types
    symbolTable.update({varName: varValue}) # TODO: Maybe change this to be the address?

    # TODO: return the asm equivelent
    # read any values from memory needed
    # preform any math operands needed
    # save back to memory


    # TODO: if isInit, then output extra asm in data section
    return 'save\n'


# returns the result of an arithmetic sequence
def math(symbolTable, line):
    # Example Input => 1+(3*1+4) => math(1 + math(math(3 * 1) + 4) )
    # Example Input => 3*(2+3)*3 => math(3 * math (2 + 3) * 3)
    # Example Input => 3*(2+(3-4)-2) => 3 * math(2+(3-4)-2) => 2 + math((3-4)-2) => math(3-4) - 2 => 3-4

    # TODO: outputString for this section?

    # Arithmetic - Check for highest PEMDAS operator
    # Parenthesis - Not needed to support in this version

    # Exponent
    if '^' in line:
        mathCheckLine('^', symbolTable, line)

    # Multiplication
    if '*' in line:
        mathCheckLine('*', symbolTable, line)

    # Division - Not needed to support in this version

    # Addition
    if '+' in line:
        mathCheckLine('+', symbolTable, line)

    # Subtraction
    if '-' in line:
        mathCheckLine('-', symbolTable, line)

    # Default if none are found, return the value if found in symbolTable
    if line in symbolTable:
        # TODO: asm to put value from memory into register, then return the register with asm?
    else:
        # Error is produced if var is used before it is declared
        raise SyntaxError(line + ' was not declared.')

    return 'math\n'


# Writes to console
def write(symbolTable, line):
    # Write Statement
        # <EXP> part it optional
        # Write out a number
        # Write out a string
        # After each write statement is always a new line
    return 'write\n'


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
        raise FileNotFoundError(filePath + ' was not found. Please enter a valid path')
    else:
        # Creates xxx.asm and xxx.err if file exists
        open(getNewFilePath(filePath, '.asm'), 'w').close()
        open(getNewFilePath(filePath, '.err'), 'w').close()

    # Read in file into memory
    file = open(filePath, 'r').readlines()

    # Scan over each line
    for line in file:
        
        command = ''
        foundCommand = False
        lineNumber = lineNumber + 1

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
            elif command == 'program':
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
         
    # Output asm to xxx.asm
    file = open(getNewFilePath(filePath, '.asm'), 'w')
    file.write(outputString)


# Output and errors to xxx.err and stop program # Always create even if empty # Only create one file (xxx.err) if we cannot determine input program name
except Exception as error:
    logError(repr(error), filePath, lineNumber)
