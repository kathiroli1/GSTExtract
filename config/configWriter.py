from configparser import ConfigParser

config=ConfigParser()

config['AZURE_DOCUMENT_AI_SERVICE']={
   "key":"value"
}
#config.ini is hidden with help of git-ignore

def generateConfigFile():
    with open('config.ini','w') as f:
        config.write(f)

if __name__=="__main__":
    generateConfigFile()