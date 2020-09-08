from Config.VarConfig import desiredcapsFilePath
from Utils.ParseConfig import ParseConfig


def getDesiredcaps():
    pcf = ParseConfig(desiredcapsFilePath)
    items = pcf.getItemsSection("Desired_caps")
    desired_caps = {
        'platformName': items['platformname'],
        'platformVersion': items['platformversion'],
        'deviceName': items['devicename'],
        'appPackage': items['apppackage'],
        'appActivity': items['appactivity'],
        'autoAcceptAlerts': True,
        'unicodeKeyboard': True,
        'resetKeyboard': True,
        'noReset': True,
        'newCommandTimeout': 6000
    }
    return desired_caps

if __name__ =="__main__":
    print(getDesiredcaps())