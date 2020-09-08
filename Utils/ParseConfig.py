from configparser import ConfigParser
from Config.VarConfig import desiredcapsFilePath

class ParseConfig(object):
    def __init__(self,path):
        self.cf = ConfigParser()
        self.cf.read(path)

    def getItemsSection(self,sectionName):
        optionsDcit = dict(self.cf.items(sectionName))
        #optionsDcit = self.cf.items(sectionName)
        #print(optionsDcit)
        #print(type(optionsDcit))
        return  optionsDcit


    def getOptionValue(self,sectionName,optionName):
        optionValue = self.cf.get(sectionName,optionName)
        return optionValue


if __name__ == "__main__":
    print(desiredcapsFilePath)
    pc = ParseConfig(desiredcapsFilePath)
    print(pc.getItemSection("Desired_caps"))
    print(pc.getOptionValue("Desired_caps","platformName"))