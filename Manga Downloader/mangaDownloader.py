import requests, os, bs4

print('Hi, welcome to the Manga Downloader (title WIP obviously) Please provide a link from your preferred manga at Mangatown, starting with the lastchapter you would like to download.')
while True:
    givenURL = input() #While look checks to make sure input is usable
    if 'mangatown.com' not in givenURL:
        print('You did not give a mangatown URL. Please try again.')
    else:
        break

res = requests.get(givenURL)
res.raise_for_status() #Now check if mangatown link isn't a dead link

print('Nice link bro')
os.makedirs('promisedneverland', exist_ok=True)
mangaSoup = bs4.BeautifulSoup(res.text, "html.parser")
#Selects the img to download (img inside an anchor tag that's inside a viewier id)
mangaImg = mangaSoup.select('#viewer a img')
i = 1
baseUrl = givenURL
while True:
    res = requests.get(givenURL)
    res.raise_for_status() #Now check if mangatown link isn't a dead link
    mangaSoup = bs4.BeautifulSoup(res.text, "html.parser")
    #Selects the img to download (img inside an anchor tag that's inside a viewier id)
    mangaImg = mangaSoup.select('#viewer a img')
    if mangaImg == []:
        print('Could not find given image')
    else:
        imgUrl = mangaImg[0].get('src')
        res = requests.get(imgUrl)
        res.raise_for_status()
        strI = str(i)
        imageFile = open(os.path.join('promisedneverland', os.path.basename(strI) + '.png'), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
        #Go To Next Page
        nextPage = mangaSoup.select('.next_page')
        #change givenUrl so its used in next loop
        newUrl = nextPage[0].get('href')
        i += 1
        if 'featured.html' in newUrl:
            print('We at the end fam')
            break
        givenURL = baseUrl + newUrl
