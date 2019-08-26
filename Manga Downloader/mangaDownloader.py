import requests, os, bs4, re
#TODO, make exceptions for weird manga with v in link
#Give option if want in separate directories or same directory
print('Hi, welcome to the Manga Downloader. Please provide a link from your preferred manga at Mangatown, starting with the first chapter you would like to download.')
while True:
    givenURL = input() #While look checks to make sure input is usable
    if 'mangatown.com' not in givenURL:
        print('You did not give a mangatown URL. Please try again.')
    else:
        break
#givenURL = 'http://www.mangatown.com/manga/yakusoku_no_neverland/c001/'
res = requests.get(givenURL)
res.raise_for_status() #Now check if mangatown link isn't a dead link


mangaSoup = bs4.BeautifulSoup(res.text, "html.parser")
#Selects the img to download (img inside an anchor tag that's inside a viewier id)

mangaImg = mangaSoup.select('#viewer a img')
baseUrl = givenURL
chapRegex = re.compile(r'c(\d+)')
nameRegex = re.compile(r'manga/(.*)/c')
chapChars = chapRegex.search(baseUrl)
mangaName = nameRegex.search(baseUrl)
print('Series name: ' + str(mangaName.group(1)))
os.makedirs(str(mangaName.group(1)), exist_ok=True)
numlength = len(str(chapChars.group())) - 1
chapterNum = 1
i = 1
while True:
    res = requests.get(givenURL)
    res.raise_for_status() #Now check if mangatown link isn't a dead link
    mangaSoup = bs4.BeautifulSoup(res.text, "html.parser")
    #Selects the img to download (img inside an anchor tag that's inside a viewier id)
    mangaImg = mangaSoup.select('#viewer a img')
    if mangaImg == []:
        print('Finished download')
        break
    else:
        if(i == 1):
            print('Beginning download of Chapter ' + str(chapterNum))
        imgUrl = mangaImg[0].get('src')
        res = requests.get(imgUrl)
        res.raise_for_status()
        imageFile = open(os.path.join(str(mangaName.group(1)), os.path.basename(str(chapterNum) + '-' + str(i)) + '.png'), 'wb')
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
                #directly replace w regex
                givenURL = re.sub(r'c(\d+)', r'c%s' % str(strngChap), baseUrl)
            elif(lenChapter < numlength):
                diffLen = numlength - lenChapter
                if(diffLen == 1):
                    givenURL = re.sub(r'c(\d+)', r'c0%s' % str(strngChap), baseUrl)
                    baseUrl = givenURL
                elif(diffLen == 2):
                    givenURL = re.sub(r'c(\d+)', r'c00%s' % str(strngChap), baseUrl)
                    baseUrl = givenURL
                elif(diffLen == 3):
                    givenURL = re.sub(r'c(\d+)', r'c00%s' % str(strngChap), baseUrl)
                    baseUrl = givenURL
            else:
                print("Didnt get diff numlength, break")
                break
            i = 1
        else:
            givenURL = baseUrl + newUrl
