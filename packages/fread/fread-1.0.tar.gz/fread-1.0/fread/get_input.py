def fileInput(mainFilePath, inputFilePath):
    with open(inputFilePath, 'a') as file:
        file.write('\n')
    with open(mainFilePath) as file:
        script = "fileOpenAsInput = open('"+inputFilePath+"')\n"
        line = file.readline()
        while line != '':
            if "fileInput" in line:
                line = file.readline()
                continue
            if "input()" in line:
                line = line.replace(
                    "input()", "fileOpenAsInput.readline()[:-1]")
            elif "sys.stdin.readline()" in line:
                line = line.replace("sys.stdin.readline()",
                                    "fileOpenAsInput.readline()[:-1]")
            script += line
            line = file.readline()
        exec(script)
    quit()
