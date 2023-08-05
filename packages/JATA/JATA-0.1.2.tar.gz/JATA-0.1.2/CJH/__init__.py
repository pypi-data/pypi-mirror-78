import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from Helpers import find_between


class CJH_Archives:

    def __init__(self, repo, url=False):
        self.repo = repo
        self.url = url

    def get_meta_data(self, object_type, page_to_start_at, maximum_pages_to_scrape):
        def scrape_all_records(object_type='records', start_page=1, stop_after_pages=0, url_override=False):

            """
            URL OVERRIDE MUST BE WITHOUT THE START PAGE
            """
            if start_page <= 0:
                print("Must start at minimum of page 1")
                start_page = 1
                page = start_page
            else:
                page = start_page
            if object_type.upper() == 'RECORDS':
                print("Scraping All Individual Records")

                headless_url = "https://archives.cjh.org/repositories/3/objects?q[]=%2A&op[]=OR&field[]=keyword&from_year[]=&to_year[]=&limit=digital_object,archival_object&sort=title_sort%20asc&page="
                base_URL = str(headless_url + str(page))
            elif object_type.upper() == 'COLLECTIONS':
                # page = start_page
                print("Scraping Collections (Finding Aids)")
                headless_url = "https://archives.cjh.org/repositories/3/resources?q[]=%2A&op[]=&field[]=title&from_year[]=&to_year[]=&limit=resource&sort=year_sort%20asc&page="
                base_URL = str(headless_url + str(page))
            elif object_type.upper() == 'DIGITAL':
                # page = start_page
                print("Scraping Digital Records")
                headless_url = "https://archives.cjh.org/repositories/3/objects?q[]=%2A&op[]=OR&field[]=keyword&from_year[]=&to_year[]=&limit=digital_object&sort=year_sort%20asc&page="
                base_URL = str(headless_url + str(page))

            elif object_type.upper() == 'CUSTOM':
                headless_url = url_override
                base_URL = str(headless_url + str(page))

            def scrape_record(name, link, web_page, object_type):
                # print(web_page, link)
                # (.+?)
                # meta_dict = find_between(str(i),'<script type="application/ld+json">','  </script>' )
                # meta_dict = re.findall(r'>(', str(web_page))
                title = (web_page.title)
                part_of = web_page.find_all('ul', {'class': 'breadcrumb'})
                part_of = part_of[0].find_all('a')

                location_tupes = []
                for i in part_of:
                    link = (str(i).split('"')[1])
                    found_loc_name = (str(i).split('>')[1]).split('<')[0]
                    tupp = (found_loc_name, link)
                    location_tupes.append(tupp)

                locs = (location_tupes)

                subnotes = web_page.find_all('div', {'class': 'upper-record-details'})[0].text

                div_data_1 = [("Name", name), ("Link", link)]

                acord = web_page.find_all('div', {'class': 'acc_holder clear'})[0].text

                acc_data = []

                if object_type.upper() == 'RECORDS':
                    possible_fields_1 = [
                        "Scope and Contents",
                        "Dates",
                        "Language of Materials",
                        "Access Restrictions",
                        "Extent",
                    ]
                    possible_fields_2 = [
                        "Related Names",
                        "Digital Material",
                        "Physical Storage Information",
                        "Repository Details",

                    ]
                elif object_type.upper() == 'COLLECTIONS':
                    possible_fields_1 = [
                        "Scope and Content Note",
                        "Dates",
                        "Creator",
                        "Access Restrictions",
                        "Use Restrictions",
                        "Conditions Governing Access",
                        "Conditions Governing Use",
                        "Extent",
                        "Language of Materials"

                    ]
                    possible_fields_2 = [
                        "Additional Description",
                        "Subjects",
                        "Related Names",
                        "Finding Aid & Administrative Information",
                        'Physical Storage Information',
                        'Repository Details',

                    ]

                ##subnotes
                b1 = []
                pc_1 = []
                for i in possible_fields_1:

                    if i in str(subnotes):
                        out = True
                    else:
                        out = False
                        missingTuple = (i, '')
                        div_data_1.append(missingTuple)
                    pc_1.append(str(subnotes).find(i))
                    b1.append(out)

                ##accordian
                b2 = []
                pc_2 = []
                for i in possible_fields_2:
                    if i in str(acord):
                        out = True

                    else:
                        out = False
                        missingTuple = (i, '')
                        div_data_1.append(missingTuple)
                    pc_2.append(str(acord).find(i))
                    b2.append(out)

                xs = possible_fields_1
                ys = b1
                filtered1 = np.array(xs)[np.array(ys)]

                xs = possible_fields_2
                ys = b2
                filtered2 = np.array(xs)[np.array(ys)]

                no_emps1 = filter(lambda a: a != -1, pc_1)
                no_emps2 = filter(lambda a: a != -1, pc_2)

                aaa = [y for x, y in sorted(zip(no_emps1, filtered1))]
                bbb = [y for x, y in sorted(zip(no_emps2, filtered2))]

                indexer = 0

                filtered1 = aaa
                filtered2 = bbb

                for i in filtered1:
                    first = i
                    try:
                        next = filtered1[indexer + 1]
                    except BaseException as e:
                        next = '$$$'
                    value = find_between(subnotes, first, next)
                    value = value.replace('\n', ' ').strip().replace('\t', ' ')

                    val = (i, value)
                    div_data_1.append(val)
                    indexer += 1

                indexer = 0
                for i in filtered2:
                    first = i
                    try:
                        next = filtered1[indexer + 1]
                    except BaseException as e:
                        next = '$$$'

                    value = find_between(acord, first, next)

                    value = value.replace('\n', ' ').strip().replace('\t', ' ')
                    val = (i, value)
                    div_data_1.append(val)
                    indexer += 1

                bigList = (div_data_1)
                return tuple(bigList)

            URL = base_URL
            web_page = BeautifulSoup(requests.get(URL, {}).text, "lxml")
            pagnation = web_page.find_all('ul', {'class': 'pagination'})[0].find_all('li')
            next_link = (web_page.find_all('li', {'class': 'next'})[0]).find('a', href=True)
            linkky = str(next_link)
            nextPage_ = str("https://archives.cjh.org" + (linkky.split('"')[1]))

            pageList = []
            s_pages = []

            for i in pagnation:
                number = str(i).split('>')[2].split('<')[0]
                pageList.append((number))

            test_list = []
            for i in pageList:
                try:

                    test_list.append(int(i))
                except:
                    pass

            last_page__ = (max(test_list))
            __lastPage = page + stop_after_pages

            page_counter = page

            tupleList = []
            for i in range(page, __lastPage):

                row_list = []
                pagez = i

                print("Scraping Archive Index for Entry Links", pagez)
                page_current = page_counter
                URL = str(headless_url + str(i))
                web_page = BeautifulSoup(requests.get(URL, {}).text, "lxml")
                h3s = web_page.find_all('h3')

                for i in h3s:

                    try:
                        link = ((str(i).split('href="')[1]).split('"'))[0]
                        name = (str(i).split('">'))[1].split("</a")[0]

                        data_tuple = (name, str("https://archives.cjh.org" + link), link)
                        tupleList.append(data_tuple)

                    except BaseException as e:
                        pass
                page_counter += 1
            archIndex = pd.DataFrame.from_records(tupleList, columns=['Names', 'Link', 'Location'])

            # ...
            counter = 0
            print("Number of Objects Extracted: ", len(archIndex))
            print("Scraping entry meta data...")
            for i in archIndex.itertuples():
                counter += 1

                name = i.Names
                link = i.Link
                link123 = link
                Location = i.Location
                web_page = BeautifulSoup(requests.get(link, {}).text, "lxml")

                record_row = scrape_record(name, link123, web_page, object_type.upper())
                row_list.extend(record_row)
                print("Record: ", counter, link123, name)

                s_pages.extend(row_list)

            d = {}
            for x, y in s_pages:
                d.setdefault(x, []).append(y)
            df = pd.DataFrame.from_records(d).drop_duplicates()
            if object_type.upper() == 'RECORDS':
                pass
            elif object_type.upper() == 'COLLECTIONS':

                df['Use Terms'] = df['Use Restrictions'] + df['Conditions Governing Use']
                # df1.replace('NA',np.nan,inplace=True)
                df['Access Terms'] = df['Access Restrictions'] + df['Conditions Governing Access']
                dropThese = [
                    'Use Restrictions',
                    'Conditions Governing Use',
                    'Access Restrictions',
                    'Conditions Governing Access',
                ]
                df.drop(columns=dropThese, inplace=True)
            else:
                pass

            return (df.reset_index(drop=True))

        if self.repo.upper() == 'AJHS':
            print('Creating CJHA Scraper Object for AJHS')
            self.meta_df = scrape_all_records(object_type, page_to_start_at, maximum_pages_to_scrape)
            return self.meta_df
        elif self.repo.upper() == 'CUSTOM':
            self.meta_df = scrape_all_records(page_to_start_at, maximum_pages_to_scrape, self.url)
        else:
            print("Sorry, only AJHS and CUSTOM are currently supported :,(")
            pass
