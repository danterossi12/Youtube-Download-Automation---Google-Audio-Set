#                      ****** Youtube to .WAV Converter Download Automation from Google Audio Set ******
#                                                  Dante Rossi
import get_indices_labels_url_function
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import glob
from pydub import AudioSegment

start_page = 'https://www.youtubeto.com/WAV.php'  # webpage to convert youtube videos to .wav
chrome_path = 'ENTER_CHROMEDRIVER_EXE_PATH'  # chromedriver path
download_path = 'ENTER_DEFAULT_DOWNLOAD_DIRECTORY'
download_path_split_files = 'ENTER_SPLIT_FILES_PATH'
# Google chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')  # Suppress terminal certificate error
chrome_options.add_argument('--ignore-ssl-errors')  # Suppress terminal ssl error
chrome_options.add_extension('Adblock-Plus_v.crx')  # Adblock extension
prefs = {
    'download.default_directory': download_path}  # choose default chrome download directory 
chrome_options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(executable_path=chrome_path,
                          chrome_options=chrome_options)  # define webdriver path and added save options

						  
'''
This portion of code allows you to run a search on specific keywords to download by generating
a text file with subjects, which is then used to generate a new 'url' text file of videos
containing content from those subjects. As the program stands right now, it will download
the entire list.

# generate requested_subjects.txt
with open('requested_subjects.txt', 'w') as requested_subjects: # text file prompts user which keywords to download in url text file
    keyword = raw_input('Enter keyword:\n')
    requested_subjects.write(keyword + '\n')
    while True:
        keyword = raw_input("Enter another keyword, press q when finished:\n")
        if keyword == 'q':
            break
        else:
            requested_subjects.write(keyword + '\n')

# generate urls_namingScheme.txt
value = get_indices_labels_url_function.main()
text = open("urls_namingScheme.txt", 'w+')
get_indices_labels_url_function.write_url_to_file(text, value)
text.close()
'''

# go to start_page
driver.get(start_page)

# Begin loop to pass through urls and filenames
with open("urls_namingScheme.txt") as infile:
    for line in infile:
        line = line.strip().strip('\n')
        if line:
            split = line.split(',')  # split text file
            yUrl = split[0].strip()  # youtube url
            yName = split[1].strip()  # name of file
            yStartIndices = int(split[2].strip())  # indices
            yEndIndices = int(split[3].strip())
            # START PAGE
            PassUrl = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'url')))  # wait for 'form' element
            PassUrl_ready = driver.find_element_by_id('url')  # locate 'form' element
            PassUrl_ready.send_keys(yUrl)  # pass url into element

            # DOWNLOAD
            downloadButton = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'DownloadWAV')))  # wait for 'download' element
            downloadButtonClick = driver.find_element_by_id('DownloadWAV')  # locate 'download' element
            downloadButtonClick.click()  # click 'convert another' element
            time.sleep(4)

            # wait for download
            while True:
                if glob.glob(download_path + '\*.wav.crdownload'):
                    name = glob.glob(download_path + '*.wav.crdownload')
                    name = name[0][:-11]
                    time.sleep(10)
                else:
                    print('breaking...')
                    break

            # split file
            t1 = yStartIndices * 1000  # Works in milliseconds
            t2 = yEndIndices * 1000
            newAudio = AudioSegment.from_wav(name)
            newAudio = newAudio[t1:t2]
            os.chdir(download_path_split_files)
            newAudio.export(yName + '.wav', format="wav")  # Exports to a wav file in the current path.
            os.chdir(download_path)
            # write to text file to track most recent successful downloads
            with open("most_recent_downloads.txt", 'a') as text_file:
                text_file.write("{}".format(yName) + yUrl + " 1\n")

            # delete first line of urls_namingScheme .txt
            with open('urls_namingScheme.txt', 'r') as fin:
                data = fin.read().splitlines(True)
            with open('urls_namingScheme.txt', 'w') as fout:
                fout.writelines(data[1:])

print ('finished successfully!')
