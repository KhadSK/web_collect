from selenium import webdriver
import time
import urllib.request
import os
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import logging
import json
from pathlib import Path



def main():
    with open(pathFileFamily) as jsonFile:
        data = json.load(jsonFile)
        if 'family' in data:
            createInitLogger()
            
            for fam in data['family']:
                if 'name' and 'id' not in fam:
                    continue
                familyName = fam['name']
                familyId = fam['id']
                
                dirWebOutput = './google/'+familyName
                driver.get('https://www.google.com/')
                search = driver.find_element_by_name('q')
    
                # create directory
                Path(dirWebOutput).mkdir(parents=True, exist_ok=True)
                
                max_attempts = 3
                attempts = 0
                # sleep time in second
                sleeptime = 2            
                
                while attempts < max_attempts:
                    time.sleep(sleeptime)
                    try:                   
                        logging.info('family name in process : ' + familyName)                                        
                        #download image
                        downloadImages(search, familyName, dirWebOutput)
                        break
                    
                    except Exception as e:
                        returnError = 'e.args'
                        print(type(returnError))
                        logging.warning('return error : '+ returnError +' - recovery page KO : '+ familyName +' - attempt : '+ str(attempts))
                        if not os.path.exists(pathFailedFamily):
                            createInitFamilyFailedFile()
    
                        with open(pathFailedFamily, 'r+', encoding='utf-8') as f:
                            if attempts == (max_attempts - 1):
                                writeFamilyFailedFile(f, returnError, fam)
                            f.close()
                                       
                    finally:
                        attempts += 1


def downloadImages(search, keyWord, dirWebOutput):   
    search.send_keys(keyWord,Keys.ENTER)
    # click on Images page
    elem = driver.find_element_by_link_text('Images')
    elem.get_attribute('href')
    elem.click()    #comment out for testing
    sub = driver.find_elements_by_tag_name('img')
    
    for i in sub[1:10]:
        src = i.get_attribute('src')
        try:
            if src != None:
                src = str(src)
                print(src)
                urllib.request.urlretrieve(src, os.path.join(dirWebOutput, 'image'+str(5)+'.jpg'))
                # rename img name to species name
            else:
                raise TypeError
        except TypeError:
            print('Fail')    
        finally:
            driver.close()
        
def writeFamilyFailedFile(file, returnCode, fam):
    jdataFailed = json.load(file)
    #add family with error code
    fam['returnError'] = returnCode
    jdataFailed['family'].append(fam)
    json.dump(jdataFailed, open(pathFailedFamily,'w', encoding='utf-8'))  
    logging.debug('write - modification : '+ str(jdataFailed))

def createInitFamilyFailedFile():
    with open(pathFailedFamily, 'w+', encoding='utf-8') as file: 
        data = {'family':[{'id': None, 'name': None}]}
        json.dump(data, file, ensure_ascii=False)
        logging.debug('create file json family failed : '+ file.name)
        
def createInitLogger():
    # create log file
    with open(pathLog,'a+') as f:
        f.write('log file : ' + pathFailedFamily + '\n')
        f.close()
    # DEBUG, INFO, WARNING, ERROR
    logging.basicConfig(filename=pathLog, 
                        format='%(asctime)s : %(levelname)s : %(message)s', 
                        datefmt='%Y/%m/%d %H:%M:%S', 
                        encoding='utf-8', 
                        level=logging.DEBUG)


if __name__ == "__main__":
    # creating object 
    # open driver
    driver = webdriver.Firefox()
    dateTime = datetime.today().strftime('%Y%m%d %H:%M:%S')
    # ./src/in/family.json
    pathFileFamily = './src/in/test_family.json'
    pathFailedFamily = './log/json/google_family ' + dateTime + '.json'
    pathLog = './log/google_log ' + dateTime + '.log'
    familyName = None
    familyId = None
    urlWebPage = ''
    dirWebOutput = ''    
    main()
