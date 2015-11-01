import json

class Replace:
    def __init__(self, s, r):
        self.search = s
        self.replace = r


class Command:
    def __init__(self, raw):
        self.raw = raw
        self.cmd = ''
        self.args = []
        self.classification = []
        self.bList = []

        self.findBrackets()
        self.findArguments()

        self.getCmd()

        if self.bList:
            self.name = raw[0:self.bList[0]]
        else:
            self.name = raw

    def addArgument(self, arg):
        self.args.append(arg)

    def addClassification(self, cl):
        self.classification = cl

    def findBrackets(self):
        bList = []
        for i in range(0, len(self.raw)):
            if self.raw[i] == '[' or self.raw[i] == '{':
                bList.append(i)
        self.bList = bList

    def findArguments(self):
        for idx in self.bList:
            if self.raw[idx] == '[':
                # optional argument
                # find end
                arg = self.raw[idx:self.raw[idx::].find(']')+idx+1]
                self.addArgument(arg)
            elif self.raw[idx] == '{':
                # non optional argument
                arg = self.raw[idx:self.raw[idx::].find('}')+idx+1]
                self.addArgument(arg)
            else:
                print 'warning: no bracket at this location.'

    def getCmd(self):
        if len(self.bList) > 0:
            self.cmd = self.raw[0:self.bList[0]]
        else:
            self.cmd = self.raw


class CWL:
    def __init__(self, fname):
        self.filename = fname
        self.commands = []
        self.includes = []
        self.replaces = []
        self.readingKeyvals = False
        self.readingOptionals = False
        self.process()

    def show(self):
        print "CWL instance, with", len(self.commands), 'commands'

    def process(self):
        f = open(self.filename, 'r')
        for line in f:
            if len(line) is 1:
                continue

            if self.readingKeyvals:
                # process a keyval here
                if line.startswith('#endkeyvals'):
                    self.readingKeyvals = False
                continue

            elif line.startswith('#include'):
                self.includes.append(line[9::])

            elif line.startswith('#repl'):
                toreplace = line[6::].split()
                if len(toreplace) is not 2:
                    print('The following replace line has not been processed,'
                          'it involves more then 1 space.')
                    print line
                    continue
                else:
                    repl = Replace(toreplace[0], toreplace[1])
                    self.replaces.append(repl)

            elif line.startswith('#keyvals'):
                self.readingKeyvals = True

            elif line.startswith('#endkeyvals'):
                # if input is correct, this line is never reached
                self.readingKeyvals = False

            elif line.startswith('#ifOption'):  # currently does nothing
                self.readingOptionals = True

            elif line.startswith('#endif'):
                self.readingOptionals = False  # currently does nothing

            elif line.startswith('#'):
                # this is a comment line
                # currently just skips
                continue

            elif line.startswith('\\'):
                # found a command, process it
                command = line.split('#')
                cmd = Command(command[0])

                if len(command) > 1:
                    cmd.addClassification(command[1::])

                self.commands.append(cmd)

            else:
                print "warning unable to process the following line:"
                print line[0:-1], '\n'
        f.close()


class Completions:
    def __init__(self):
        self.scope = 'text.tex'
        self.completions = []

    def add(self, c):
        self.completions.append(c)

    def toJSON(self):
        JSONstring = json.dumps(self.__dict__,
                                default=lambda o: o.__dict__,
                                indent=4)
        return JSONstring


class Completion:
    def __init__(self, cmd):
        # set the trigger
        bString = ''
        if cmd.bList:
            for b in cmd.bList:
                bString = bString + cmd.raw[b]
                if cmd.raw[b] is '{':
                    bString = bString + '}'
                else:
                    bString = bString + ']'
        self.trigger = cmd.cmd + bString
        
        contentString = cmd.cmd
        argNo = 0
        for arg in cmd.args:
            argNo = argNo + 1
            # ${1:Guillermo}
            if len(arg) is 0:
                continue
            contentString = contentString + arg[0] + '${' + str(argNo) + ':' + \
                arg[1:-1] + '}' + arg[-1]
        self.contents = contentString