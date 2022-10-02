from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


# import Action chains
from selenium.webdriver.common.action_chains import ActionChains
 
# import KEYS
from selenium.webdriver.common.keys import Keys
import json
import time

# utilities
import urllib.parse
import warnings
import requests
import shutil




class getResult:
    req_string = 'https://github.com/search?q={}&type={}'
    # req_string = 'https://github.com/search?p={}&q={}&type={}'

    def __init__(self, findText, options ):
        self.type = "repositories"

        # for running multiple threads / processes. Check if multiple threads can write onto disk siimolutaneously
        self.pageCountBegin = 1
        self.pageCountEnd = 100
        self.delay = 6

        if(options["type"] != None):
            self.type = options["type"] 
        if(options["pageCountBegin"] != None):
            self.pageCountBegin = options["pageCountBegin"]
        if(options["pageCountEnd"] != None):
            self.pageCountEnd = options["pageCountEnd"]
        if(options["delay"] != None):
            self.delay = options["delay"]
        

        self.findText = urllib.parse.quote(findText)
        self.req_string = getResult.req_string.format(self.findText, self.type)
        self.errorLog = open("errorLog.txt", "w")

    def getHTML(self, pageNum):
        time.sleep(self.delay)
        print(pageNum)
        local_req_string = self.req_string + f"&p={pageNum}"
        get = requests.get(local_req_string)
        if(get.status_code != 200):
            warnings.warn(f"Request to {local_req_string} gave status code {get.status_code}")
            self.errorLog.write(f"Request to {local_req_string} gave status code {get.status_code}\n")
            return 1
        f = open(f"q={self.findText}&type={self.type}.txt&p={pageNum}", "w")
        f.write(get.text)
        f.close()
        return

    def getHTML_repair(self):

        # need to flush to disk before reading the file. OSs cache instead to writing to disk directly
        self.errorLog.flush()
        errorFile = open("errorLog.txt","r")
        errorFile_temp = open("errorLog_temp.txt", "w")
        errorFileLogs = errorFile.readlines()
        self.delay = self.delay * 500
        for i in errorFileLogs:
            link = i.split(" ")[2] 
            print(link)
            time.sleep(self.delay)
            local_req_string = link
            get = requests.get(local_req_string)
            if(get.status_code != 200):
                warnings.warn(f"Request to {local_req_string} gave status code {get.status_code}")
                errorFile_temp.write(f"Request to {local_req_string} gave status code {get.status_code}\n")
            name = link.split("?")[-1]
            f = open(f"{name}.txt", "w+")
            f.write(get.text)
            f.close()
        shutil.copyfile("errorLog_temp.txt", "errorLog.txt")
        






    def run(self):
        for i in range(self.pageCountBegin,self.pageCountEnd + 1):
            self.getHTML(i)


    
        
            




if __name__ == '__main__':
    queryText = "C++"
    options = {}
    options["type"] = "repositories"
    options["pageCountBegin"] = 1
    options["pageCountEnd"] = 30
    options["delay"] = 0.01
    print(options)

    getResultInstances = []
    getResultInstances.append(getResult(queryText, options))

    for i in getResultInstances:
        i.run()
    for i in getResultInstances:
        i.getHTML_repair()







