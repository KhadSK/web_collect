from google_images_download import google_images_download
import json
from pathlib import Path
import os
import time
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
                
                dirWebOutput = './google/'+familyName
    
                # create directory
                #Path(dirWebOutput).mkdir(parents=True, exist_ok=True)
                
                max_attempts = 3
                attempts = 0
                # sleep time in second
                sleeptime = 2            
                
                while attempts < max_attempts:
                    time.sleep(sleeptime)
                    try:                   
                        logging.info('family name in process : ' + familyName)                                        
                        #download image
                        downloadImages(familyName, dirWebOutput)
                        break
                    
                    except Exception as e:
                        returnError = e.args
                        logging.warning('return error : '+ returnError +' - recovery page KO : '+ familyName +' - attempt : '+ str(attempts))
                        if not os.path.exists(pathFailedFamily):
                            createInitFamilyFailedFile()
    
                        with open(pathFailedFamily, 'r+', encoding='utf-8') as f:
                            if attempts == (max_attempts - 1):
                                writeFamilyFailedFile(f, returnError, fam)
                            f.close()
                                       
                    finally:
                        attempts += 1

def downloadImages(query, dirOutput): 
    # keywords is the search query 
    # format is the image file format 
    # limit is the number of images to be downloaded 
    # print urs is to print the image file url 
    # size is the image size which can 
    # be specified manually ("large, medium, icon") 
    # aspect ratio denotes the height width ratio 
    # of images to download. ("tall, square, wide, panoramic") 
    #  'format': 'jpg', 'aspect_ratio': 'panoramic',
    arguments = {'keywords': query,
                 'limit': 3, 
                 'print_urls': True, 
                 'size': 'medium', 
                 'print_urls': True,
                 'image_directory': dirOutput} 
    response.download(arguments) 

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
    response = google_images_download.googleimagesdownload()    
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