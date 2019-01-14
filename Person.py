class Person:

    def __init__(self, userName, ipAddress):
        self.name = self.setName(userName)
        self.hostAddress = ipAddress

    def getName(self):
        return self.name

    def getHostAddress(self, *ignore):
        return self.hostAddress

    def setName(self, newName):
        self.name = newName
