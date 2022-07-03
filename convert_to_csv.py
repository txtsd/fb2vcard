#!/usr/bin/env python

from bs4 import BeautifulSoup as bs
import csv
# from fuzzywuzzy import fuzz
import glob
from pprint import pprint
import re
import calendar
import phonenumbers

DIR_DATA = 'data/'
PATTERN_BIRTHDAY = re.compile(r'(?P<month>\w+?) (?P<day>\d+)([, ]+(?P<year>\d+)){0,}')
FIELDNAMES = ['Name','Given Name','Additional Name','Family Name','Yomi Name','Given Name Yomi','Additional Name Yomi','Family Name Yomi','Name Prefix','Name Suffix','Initials','Nickname','Short Name','Maiden Name','Birthday','Gender','Location','Billing Information','Directory Server','Mileage','Occupation','Hobby','Sensitivity','Priority','Subject','Notes','Language','Photo','Group Membership','E-mail 1 - Type','E-mail 1 - Value','IM 1 - Type','IM 1 - Service','IM 1 - Value','Website 1 - Type','Website 1 - Value','Phone 1 - Type','Phone 1 - Value']


list_files = glob.glob(DIR_DATA + 'about_*.html')
list_of_things = set()

with open('from_facebook.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
    writer.writeheader()

for file in list_files:
    # print(file)
    with open(file) as f:
        file_data = f.read()
        soup = bs(file_data, 'lxml')

        # Look for files with incorrect content
        match = (soup.title.text == "You Can't Use This Feature Right Now") or \
            (soup.title.text == "Content Not Found") or \
            (soup.title.text == "Error Facebook")
        if match:
            print(file, 'is wrong. Skipping.')
            print()
            continue

        # Name
        match = soup.select_one('div span div span strong')
        # name_full = match.get_text()
        name_full = ''.join(text for text in match.find_all(text=True) if text.parent.name != 'span')

        # Alternate Name
        match_1 = match.select_one('.alternate_name')
        name_alternate = None
        if match_1:
            name_alternate = match_1.get_text()[1:-1]

        # Birthday
        birthday = None
        birthday_google = None
        match = soup.find(text='Birthday')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text()
            if match_1:
                match_2 = PATTERN_BIRTHDAY.search(match_1)
                if match_2:
                    year = None
                    month = match_2['month']
                    day = match_2['day']
                    if match_2.group(3):
                        year = match_2['year']
                    num_month = format(list(calendar.month_name).index(month), '02d')
                    num_day = day.zfill(2)
                    if year:
                        birthday = year + num_month + num_day
                        birthday_google = num_month + '/' + num_day + '/' + year
                    else:
                        birthday = '--' + num_month + num_day
                        birthday_google = num_month + '/' + num_day

        # Gender
        gender = None
        match = soup.find(text='Gender')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                gender = match_1

        # Email
        list_email = list()
        matches = soup.find_all(text='Email')
        if matches:
            for match in matches:
                match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
                if match_1:
                    list_email.append(match_1)

        # Adress
        relationship = None
        match = soup.find(text='Relationship')
        if match:
            match_1 = match.parent.parent.parent.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                relationship = match_1

        # Relationship
        address = None
        match = soup.find(text='Address')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text()
            if match_1:
                address = match_1

        # facebook link
        link_facebook = None
        match = soup.find(text='Facebook')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                link_facebook = match_1

        # instagram link
        link_instagram = None
        match = soup.find(text='Instagram')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                link_instagram = match_1

        # YouTube link
        link_youtube = None
        match = soup.find(text='YouTube')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                link_youtube = match_1

        # Twitter link
        link_twitter = None
        match = soup.find(text='Twitter')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                link_twitter = match_1

        # Generic website link
        list_link_websites = list()
        matches = soup.find_all(text='Websites')
        if matches:
            for match in matches:
                match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
                if match_1:
                    list_link_websites.append(match_1)

        # Other website link
        link_other = None
        match = soup.find(text='Other Service')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                link_other = match_1

        # Tumblr link
        link_tumblr = None
        match = soup.find(text='Tumblr')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                link_tumblr = match_1

        # Snapchat
        social_snapchat = None
        match = soup.find(text='Snapchat')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                social_snapchat = match_1

        # eBuddy
        social_ebuddy = None
        match = soup.find(text='eBuddy')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                social_ebuddy = match_1

        # LINE
        social_line = None
        match = soup.find(text='LINE')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                social_line = match_1

        # Skype
        social_skype = None
        match = soup.find(text='Skype')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                social_skype = match_1

        # Current City
        city_current = None
        match = soup.find(text='Current City')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                city_current = match_1

        # Hometown
        city_home = None
        match = soup.find(text='Hometown')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                city_home = match_1

        # Mobile
        number_mobile = None
        match = soup.find(text='Mobile')
        if match:
            match_1 = match.parent.parent.parent.next_sibling.get_text(strip=True)
            if match_1:
                number_parsed = phonenumbers.parse(match_1, 'IN')
                number_rfc3966 = phonenumbers.format_number(number_parsed, phonenumbers.PhoneNumberFormat.RFC3966)
                number_mobile = number_rfc3966





        # # Print All
        # print(name_full)
        # if name_alternate:
        #     print(name_alternate)
        # if birthday:
        #     print(birthday)
        # if gender:
        #     print(gender)
        # if list_email:
        #     for email in list_email:
        #         print(email)
        # if relationship:
        #     print(relationship)
        # if address:
        #     print(address)
        # if link_facebook:
        #     print(link_facebook)
        # if link_instagram:
        #     print(link_instagram)
        # if link_youtube:
        #     print(link_youtube)
        # if link_twitter:
        #     print(link_twitter)
        # if list_link_websites:
        #     for link in list_link_websites:
        #         print(link)
        # if link_other:
        #     print(link_other)
        # if link_tumblr:
        #     print(link_tumblr)
        # if social_snapchat:
        #     print(social_snapchat)
        # if social_ebuddy:
        #     print(social_ebuddy)
        # if social_line:
        #     print(social_line)
        # if social_skype:
        #     print(social_skype)
        # if city_current:
        #     print(city_current)
        # if city_home:
        #     print(city_home)
        # if number_mobile:
        #     print(number_mobile)



        # Save to CSV
        with open('from_facebook.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
            csv_dict = dict()
            csv_dict['Name'] = name_full
            if birthday:
                csv_dict['Birthday'] = birthday
            if gender:
                csv_dict['Gender'] = gender
            if list_email:
                csv_dict['E-mail 1 - Value'] = email
            if number_mobile:
                csv_dict['Phone 1 - Value'] = number_mobile
            writer.writerow(csv_dict)
















#         # Output Contact Info Types
#         match = soup.select('#contact-info > div > div:nth-of-type(2) table tr td div span')
#         print(name_full, match)
#         for thing in match:
#             list_of_things.add(thing.get_text())
# pprint(list_of_things)
