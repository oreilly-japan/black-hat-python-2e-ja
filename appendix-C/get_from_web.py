# -*- config:utf-8 -*-
__author__ = 'Hiroyuki Kakara'

from bs4 import BeautifulSoup
from datetime import datetime
import filetype
from io import StringIO
import os
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import requests
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    laparams.detect_vertical = True
    device = TextConverter(rsrcmgr, 
        retstr, codec=codec, laparams=laparams)
    with open(path, 'rb') as fp:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        file_str = ''
        try:
            for page in PDFPage.get_pages(fp, set(), maxpages=0, caching=True, check_extractable=True):
                interpreter.process_page(page)
                file_str += retstr.getvalue()
        except Exception as e:
            fp.close()
            device.close()
            retstr.close()
            return -2        
    device.close()
    retstr.close()
    return file_str

class get_from_web:
    def get_web_content(self, url):
        try:
            re = requests.get(url, timeout=(3.0, 7.5))
        except Exception as ex:
            return str(ex)
        saveFileName = str(datetime.now().timestamp())
        saveFile = open(saveFileName, 'wb')
        saveFile.write(re.content)
        saveFile.close()
        file_type = filetype.guess(saveFileName)
        if file_type is not None and file_type.extension =="pdf":
            pdf_text = convert_pdf_to_txt(saveFileName)
            os.remove(saveFileName)
            return pdf_text
        else:
            try:
                os.remove(saveFileName)
                options = Options()
                options.add_argument('--headless')
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--no-sandbox')
                options.add_argument('--headless')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument(f'--user-agent={user_agent}')
                chrome_service = service.Service(executable_path
                 ='!!解凍したWebドライバのフルパスを入力!!')
                driver = webdriver.Chrome(service=chrome_service, options=options)
                driver.set_page_load_timeout(10)
                driver.get(url)
                result = driver.page_source.encode('utf-8')
                driver.quit()
                soup=BeautifulSoup(result,"html.parser")
                return soup.get_text(" ")
            except Exception as e:
                print(e)
                return -1