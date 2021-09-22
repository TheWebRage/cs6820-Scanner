from os.path import exists

# Returns a string from the combined elements in a list
def flatten(list):
    returnString = ''
    for string in list:
        returnString += string + '/'
    return returnString

# Returns a new file path with the extension passed in
def getNewFilePath(filePath, extension):
    splitFile = filePath.split('/')
    folderPath = flatten(splitFile[:-1]) # TODO: check length before taking off extension?
    return folderPath + splitFile[-1].split('.')[0] + extension

# Logs the error in xxx.err and in the console
def logError(errorString, filePath):
    # Output and errors to xxx.err and stop program # Always create even if empty # Only create one file (xxx.err) if we cannot determine input program name
    # Use program name to create output files
    # Errors print to xxx.err and say something like 'Error: There was as error on line x'
        # Printing error to console would be nice too
        # If error is produced ignore anything in xxx.asm file
    errorString += "ERROR: " + errorString
    print(errorString)
    file = open(getNewFilePath(filePath, '.err'), 'w')
    file.write(errorString)

# Get variable name and value; Store into symbol table; throw error if variable name is invalid
def saveVarIntoTable(symbolTable, line):
    return 'save\n'
    # Symbol Table
        # No two vars use same name
        # No variable name is same as a keyword
        # Keep track of vars types

    # Error is produced if var is used before it is declared
    pass # TODO: get variable name and value

# returns the result of an arithmetic sequence
def math(symbolTable, line):
    return 'math\n'
    # Arithmetic
        # Addition
        # Subtraction
        # Multiplication
        # Exponentiation
    pass

# Writes to console
def write(symbolTable, line):
    return 'write\n'
    # Write Statement
        # <EXP> part it optional
        # Write out a number
        # Write out a string
        # After each write statement is always a new line
    pass

# Accept command line arguments
# TODO: add command line arguments
filePath = './src/basics.txt'
outputString = ''
symbolTable = {}
isComment = False

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
            elif command == 'num ':
                foundCommand = True
                outputString += saveVarIntoTable(symbolTable, line)

            elif '=' in command:
                foundCommand = True
                outputString += math(symbolTable, line)

            elif command == 'write':
                foundCommand = True
                outputString += write(symbolTable, line)
            
            if foundCommand:
                break
         
    # Output asm to xxx.asm
    file = open(getNewFilePath(filePath, '.asm'), 'w')
    file.write(outputString)


except Exception as error:
    logError(repr(error), filePath)
