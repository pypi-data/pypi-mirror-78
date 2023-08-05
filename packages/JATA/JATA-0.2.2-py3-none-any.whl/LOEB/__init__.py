import os
import re
import urllib.request
import urllib.request

import bs4
import pandas as pd
import requests

from Helpers import striplist


# collapse-hide
class loeb:
    """
    This class can be used to interact with the loeb image data base.
    The init funciton takes 1 argument which is the type of data to retreive.
    The input should be one of the following : 'paintings', silhouettes, photographs, or 'all'
    """

    def __init__(self, data_set='paintings'):

        def scrape_loeb(URL):
            requests.get(URL)
            web_page = bs4.BeautifulSoup(requests.get(URL, {}).text, "lxml")
            table = web_page.find_all('portfolio')
            div = web_page.find(id="portfolio")
            linkList = web_page.find_all('div', {'class': 'work-info'})
            df_dict = []
            for links in linkList:
                twolinks = links.find_all('a', href=True)
                details = str(twolinks[0]).split('"')[1]
                img = str(twolinks[1]).split('"')[3]
                new_df_tuple = {'info_link': details, 'img_link': img}
                df_dict.append(new_df_tuple)

            listOfDfs = []
            counter = 0
            df = pd.DataFrame.from_records(df_dict)
            total_entrys = len(df)
            for i in df.itertuples():
                img = i.img_link
                info = i.info_link

                profile = bs4.BeautifulSoup(requests.get(info, {}).text, "lxml")
                img = str(profile.find_all('img', src=True)[0]).split('"')[3]

                a = profile.find_all('h4')

                b = profile.find_all("h3")

                linkts = str(profile.find_all('a', {'id': 'viewzoom'}, href=True)[1]).split('"')[1]

                def scrape_bio_loeb(url):
                    bio = bs4.BeautifulSoup(requests.get(url, {}).text, "lxml")
                    abc = str(bio.find_all('p')[1]).replace("<p>", " ")
                    abcd = (str(abc).replace('</p>', " "))
                    bio_text = str(str(abcd.replace('<i>', ' ')).replace("</i>", ' '))
                    s = bio_text
                    bio_plain = re.sub(r'<.+?>', '', s)
                    if 'Lorem ipsum dolor sit amet,' in bio_plain:
                        bio_plain = ''
                    if "Lorem ipsum dolor sit amet," in s:
                        s = ''

                    return bio_plain, s

                bio__ = scrape_bio_loeb(linkts)

                headers4 = striplist((a))
                headers3 = striplist(b)
                headers4_ = ['Name']
                for i in headers4:
                    headers4_.append(i)

                headers4_ = headers4_[:-1]
                headers4_.append('Bio_Plain')
                headers3.append(bio__[0])

                headers4_.append('Bio_Links')
                headers3.append(bio__[1])
                df1 = pd.DataFrame({'Label': headers4_, 'Value': headers3})

                self.image_cache.append((img, df1))

                listOfDfs.append(df1)

                counter += 1

                self.list_of_dfs.extend(listOfDfs)
                # os.system('clear')
                print("Collected Data for ", counter, "out of", total_entrys, "images")

        self.list_of_dfs = []
        self.image_cache = []

        if data_set.upper() == 'ALL':
            data_options = ['paintings', 'silhouettes', 'photographs']

            for i in data_options:
                print(i)
                URL = str("http://loebjewishportraits.com/" + i + '/')
                scrape_loeb(URL)

        else:
            try:

                URL = str("http://loebjewishportraits.com/" + data_set + '/')
                scrape_loeb(URL)
            except BaseException as e:
                print(e)
                print("Could not find a data set for: ", data_set,
                      "Make sure you input either 'paintings', 'silhouettes', or 'photographs'!")

    def get_meta_data(self, export=False):
        """
        returns a meta dataframe with each painting as an entry in a row

        export can be csv or excel
        """
        listy = self.list_of_dfs
        transposed = [thing.transpose() for thing in listy]

        cc = 1
        newList = []
        for i in transposed:
            new_cols = (i.iloc[0])
            i.columns = new_cols
            i.drop(i.index[0], inplace=True)

        long_df_of_entrys = pd.concat(transposed)
        long_df_of_entrys.set_index('Name')

        return long_df_of_entrys.reset_index().drop_duplicates(keep='first')

    def download_images(self):
        def download_image(link, filename):
            urllib.request.urlretrieve(link, filename)

        for i in self.image_cache:
            name = (i[1].Value.iloc[0])

            fileName = str(name + '.jpg')

            try:
                download_image(i[0], fileName)
                print('Saved', fileName, 'to current directory')

            except BaseException as e:
                print("Could not download:", fileName, "Error:", e)
