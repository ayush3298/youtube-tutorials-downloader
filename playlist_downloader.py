import pafy
from tqdm import tqdm
import requests
from pydub import AudioSegment
import os
from bs4 import BeautifulSoup


class Downloader:
    def __init__ (self,url,count):
        
        self.url = url
        self.count= count
        self.video = pafy.new(self.url)
        self.videostreams = self.video.videostreams
        self.download_url =  self.videostreams[-1].url
        self.title = self.video.title
        self.local_name = str(str(self.count) + '-' + self.title+'.mp4').replace('/',' ')
        #self.local_name = 
        self.r = requests.get(self.download_url, stream=True)
        print(self.title)
        self.main()
        #self.download()
        #self.convert_to_mp3()

    def main(self):
        if os.path.exists(self.local_name):
            if str(os.path.getsize(self.local_name)) == str(self.r.headers['Content-Length']) :
                print('File already exists '+self.local_name)
            else:
                os.remove(self.local_name)
                print('file deleted '+ self.local_name)
                self.download()
        else:
            self.download()
        

    

    def download(self):
        r = self.r
        pbar = tqdm( unit="K", total=int( r.headers['Content-Length'] ) )
        print('File Downloading ' + self.local_name)
        with open(self.local_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=300): 
                if chunk:
                    pbar.update (len(chunk))
                    f.write(chunk)


def getPlaylistLinks(url):
    sourceCode = requests.get(url).text.encode('utf-8')
    soup = BeautifulSoup(sourceCode, 'html.parser')
    domain = 'https://www.youtube.com'
    playlist_name = soup.title.text.replace('- YouTube','')
    
    print(playlist_name)
    lst = list()
    for link in soup.find_all("a", {"dir": "ltr"}):
        href = link.get('href')
        if href.startswith('/watch?'):
            #print(link.string.strip())
            url = domain + href
            #url = url.split('&')[0]
            lst.append(url)
    return lst,playlist_name

            
if __name__== "__main__":
    query = str(input('Enter the url: '))
    query = 'https://www.youtube.com/playlist?list=PL3D7BFF1DDBDAAFE5'
    try:
        requests.get('https://www.google.com')
    except:
        print('please Connect to intrnet')
        exit()

    
    if len(query.split('list')) > 1:
        urls = getPlaylistLinks(query)
        playlist_name = urls[1]
        playlist_name = playlist_name.replace('/','')
        urlss = urls[0]
        
        count = 1
        
        if os.path.exists(playlist_name):
            os.chdir(playlist_name)
        else:
            os.mkdir(playlist_name)
            os.chdir(playlist_name)
        
        for url in urlss:
            
            print('*'*50)
            Downloader(url,count)
            count += 1
    else:
        Downloader(query,count)
    
        
    
    #audio()
    
    
