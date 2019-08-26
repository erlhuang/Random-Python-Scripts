import requests, os, bs4, re
#TODO, make exceptions for weird manga with v in link
#Give option if want in separate directories or same directory
print('Hi, welcome to the Manga Downloader (title WIP obviously) Please provide a link from your preferred manga at Mangatown, starting with the lastchapter you would like to download.')
while True:
    givenURL = input() #While look checks to make sure input is usable
    if 'mangatown.com' not in givenURL:
        print('You did not give a mangatown URL. Please try again.')
    else:
        break
givenURL = 'http://www.mangatown.com/manga/yakusoku_no_neverland/c001/'
res = requests.get(givenURL)
res.raise_for_status() #Now check if mangatown link isn't a dead link

print('Nice link bro')
os.makedirs('promisedneverland', exist_ok=True)
mangaSoup = bs4.BeautifulSoup(res.text, "html.parser")
#Selects the img to download (img inside an anchor tag that's inside a viewier id)
mangaImg = mangaSoup.select('#viewer a img')
chapterNum = 1
i = 1
baseUrl = givenURL
chapRegex = re.compile(r'c(\d+)')
mo1 = chapRegex.search(baseUrl)
numlength = len(str(mo1.group())) - 1
while True:
    res = requests.get(givenURL)
    res.raise_for_status() #Now check if mangatown link isn't a dead link
    mangaSoup = bs4.BeautifulSoup(res.text, "html.parser")
    #Selects the img to download (img inside an anchor tag that's inside a viewier id)
    mangaImg = mangaSoup.select('#viewer a img')
    if mangaImg == []:
        print('Could not find given image, ending')
        break
    else:
        imgUrl = mangaImg[0].get('src')
        res = requests.get(imgUrl)
        res.raise_for_status()
        imageFile = open(os.path.join('promisedneverland', os.path.basename(str(chapterNum) + '-' + str(i)) + '.png'), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
        #Go To Next Page
        nextPage = mangaSoup.select('.next_page')
        #change givenUrl so its used in next loop
        newUrl = nextPage[0].get('href')
        i += 1
        if 'featured.html' in newUrl: #gotta go to next chapter
            print('Finished downloading Chapter ' + str(chapterNum))
            chapterNum += 1
            strngChap = str(chapterNum)
            lenChapter = len(str(chapterNum))
            if(lenChapter == numlength): #Means they have same amt of digits
                #directly replace w regex thingy
                givenURL = re.sub(r'c(\d+)', r'c%s' % str(strngChap), baseUrl)
            elif(lenChapter < numlength):
                diffLen = numlength - lenChapter
                if(diffLen == 1):
                    givenURL = re.sub(r'c(\d+)', r'c0%s' % str(strngChap), baseUrl)
                    print('Going to:%s ' % givenURL )
                    baseUrl = givenURL
                elif(diffLen == 2):
                    givenURL = re.sub(r'c(\d+)', r'c00%s' % str(strngChap), baseUrl)
                    print('Going to:%s ' % givenURL )
                    baseUrl = givenURL
            else:
                print("Didnt get diff numlength, break")
                break
            #option = mangaSoup.select('.chapter_select')
            #print(str(option))
            #chList = mangaSoup.select('option')
            #givenURL = chList[chapterNum].get('value')
            #print(givenURL)
            #baseUrl = givenURL
            i = 1
        else:
            givenURL = baseUrl + newUrl
