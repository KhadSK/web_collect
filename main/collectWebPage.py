import json
from pathlib import Path
import os
import time
import subprocess
from datetime import datetime
import logging


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
                urlWebPage = 'https://www.fishbase.de/photos/FamilyPictureSearchList.php?Family='+familyName
                dirWebOutput = './src/out/web/'+familyName
    
                # create directory
                Path(dirWebOutput).mkdir(parents=True, exist_ok=True)
                
                max_attempts = 3
                attempts = 0
                # sleep time in second
                sleeptime = 4            
                
                while attempts < max_attempts:
                    time.sleep(sleeptime)
                    try:                   
                        logging.info('family name in process : ' + familyName)                                        
                        #downloadPage = wget.download(urlWebPage, out=dirWebOutput)
                        #wget -nd -r -P /save/location -A jpeg,jpg,bmp,gif,png http://www.domain.com
                        #wget -nd -r -P /save/location -E -H -k -K -p http://www.domain.com
                        #downloadPage = os.system("wget -P '%s' -E -H -k -K -p '%s'" %(dirWebOutput, urlWebPage))
                        #downloadPage = subprocess.Popen(["wget -P '%s' -E -H -k -K -p '%s'" %(dirWebOutput, urlWebPage)], shell = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        #downloadPage.stdout.readline()
                        # return code
                        #returnCode = downloadPage.poll()
                        #if returnCode is not None:
                            #print('RETURN CODE : ', returnCode)                    
                        subprocess.check_output(["wget -P '%s' -E -H -k -K -p '%s'" %(dirWebOutput, urlWebPage)], shell = True, stderr=subprocess.STDOUT)
                        break
                    
                    except subprocess.CalledProcessError as e:
                        returnCode = e.returncode
                        logging.warning('return code : '+ str(returnCode) +' - recovery page KO : '+ familyName +' - attempt : '+ str(attempts))
                        if not os.path.exists(pathFailedFamily):
                            createInitFamilyFailedFile()
    
                        with open(pathFailedFamily, 'r+', encoding='utf-8') as f:
                            if attempts == (max_attempts - 1):
                                writeFamilyFailedFile(f, returnCode, fam)
                            f.close()
                                       
                    finally:
                        attempts += 1

def writeFamilyFailedFile(file, returnCode, fam):
    jdataFailed = json.load(file)
    #add family with error code
    fam['returnCode'] = returnCode
    jdataFailed['family'].append(fam)
    json.dump(jdataFailed, open(pathFailedFamily,'w', encoding='utf-8'))  
    logging.debug('write - modification : '+ str(jdataFailed))

def createInitFamilyFailedFile():
    with open(pathFailedFamily, 'w+', encoding='utf-8') as file: 
        data = {'family':[{'id': None, 'name': None}]}
        json.dump(data, file, ensure_ascii=False)
        logging.debug('create file json family failed : '+ file.name)
        file.close()

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
    dateTime = datetime.today().strftime('%Y%m%d %H:%M:%S')
    # ./src/in/test_family.json
    pathFileFamily = './src/in/family.json'
    pathFailedFamily = './log/json/family ' + dateTime + '.json'
    pathLog = './log/family_log ' + dateTime + '.log'
    familyName = None
    familyId = None
    urlWebPage = ''
    dirWebOutput = ''    
    main()