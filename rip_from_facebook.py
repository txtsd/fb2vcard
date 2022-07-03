#!/usr/bin/env python

import re
import html
import time
import calendar
import json
from pprint import pprint
from pathlib import Path

import requests
from bs4 import BeautifulSoup as bs


LINK_MAIN = 'https://m.facebook.com'
LINK_LOGIN = 'https://m.facebook.com/login/device-based/regular/login/?refsrc=https://m.facebook.com/&lwv=100&refid=8'
LINK_FRIENDS = 'https://m.facebook.com/friends/center/friends/'
LINK_LANGUAGE = 'https://m.facebook.com/a/language.php?l=en_US&lref=%2Fsettings%2Flanguage%2F&sref=legacy_mobile_settings&gfid=AQADZjSUoWMlr7lH'

PATTERN_HOVERCARD_NAME = re.compile(r'<a class="b[qo]" href="(?P<link>.+?)">(?P<name>.+?)</a>')
PATTERN_SEEMORE = re.compile(r'[0ki]"><a href="(.+?)"><span>See More</span></a>')
PATTERN_PROFILE = re.compile(r'<div class="(?:bc|x)"><a href="(.+?)"')
PATTERN_DEACTIVATED = re.compile(r'This account has been deactivated.')
PATTERN_ABOUT = re.compile(r'[dgl]"><a href="(.+?)" class="\w\w">About</a>')
PATTERN_RATELIMIT = re.compile(r'We limit how often you can post, comment or do other things in a given amount of time in order to help protect the community from spam. You can try again later.')
PATTERN_BIRTHDAY = re.compile(r'Birthday</span></div></td><td valign="top" class="\w\w"><div class="\w\w">(?P<month>\w+?) (?P<day>\d+)([, ]+(?P<year>\d+)){0,}</div>')

list_friends = dict()
data_dict = dict()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
}

session = requests.Session()

print('Loading m.facebook.com')
result = session.get(LINK_MAIN)
soup = bs(result.content, 'lxml')
form = soup.select_one('form')
for nput in form.select('input'):
    if not nput.get('name') in ['sign_up']:
        data_dict[nput.get('name')] = nput.get('value')

data_dict['login'] = 'Log In'
data_dict['email'] = ''
data_dict['pass'] = r""

print('Logging in')
time.sleep(5)
result = session.post(LINK_LOGIN,data=data_dict)
print('Logged in!')

time.sleep(5)
result = session.get(LINK_LANGUAGE)
print('Language reset')

print('Reading friends JSON')
with open('data/' + 'list_friends.json', 'r') as f:
    list_friends = json.load(f)

print('Populating friends')
result = session.get(LINK_FRIENDS)
# with open('data/downloaded.html', 'wb') as f:
#     f.write(result.content)
while True:
    # matches = PATTERN_HOVERCARD_NAME.findall(result.text)
    soup = bs(result.content, 'lxml')
    soup_match = None
    soup_matches = soup.select('#friends_center_main table td > a')

    for soup_match in soup_matches:
        name_safe = soup_match.get_text().title()
        link_safe = soup_match.get('href')
        if name_safe not in list_friends:
            print('Added:', name_safe)
            list_friends[name_safe] = {'link_hovercard': LINK_MAIN + link_safe}
    # pprint(list_friends)

    # link_next = PATTERN_SEEMORE.search(result.text)
    soup_match_next = None
    soup_match_next = soup.select_one('#friends_center_main div > a')
    if not soup_match_next:
    # if soup_match_next:
        break
    link_next_safe = soup_match_next.get('href')
    time.sleep(10)
    result = session.get(LINK_MAIN + link_next_safe)
print('Done populating friends!')

print('Writing friends JSON')
with open('data/' + 'list_friends.json', 'w') as f:
    json.dump(list_friends, f, indent=2, ensure_ascii=False)
print('Done writing friends JSON')


for person in list_friends:
    # Visit hovercard link and grab profile link
    reprocess = False
    # if 'link_profile' in list_friends[person] and list_friends[person]['link_profile'] == 'DEACTIVATED':
    #     reprocess = True
    if 'link_profile' not in list_friends[person] or reprocess:
        link = list_friends[person]['link_hovercard']
        time.sleep(10)
        result = session.get(link)
        with open('data/' + 'hovercard_' + person + '.html', 'wb') as f:
            f.write(result.content)
        # match = None
        # match = PATTERN_PROFILE.search(result.text)
        soup = bs(result.content, 'lxml')
        soup_match = None
        soup_match = soup.select_one('#objects_container table td div div:nth-of-type(3) > a')
        print('Visit hovercard > Get profile link:', person)
        if soup_match and soup_match.span.get_text() == 'View Profile':
            link_profile_safe = soup_match.get('href')
            list_friends[person]['link_profile'] = LINK_MAIN + link_profile_safe
        elif PATTERN_DEACTIVATED.search(result.text):
            list_friends[person]['link_profile'] = "DEACTIVATED"
        with open('data/' + 'list_friends.json', 'w') as f:
            json.dump(list_friends, f, indent=2, ensure_ascii=False)

for person in list_friends:
    # Visit profile link and get about link
    if not list_friends[person]['link_profile'] == 'DEACTIVATED':
        if 'link_about' not in list_friends[person]:
            link = list_friends[person]['link_profile']
            time.sleep(30)
            result = session.get(link)
            with open('data/' + 'timeline_' + person + '.html', 'wb') as f:
                f.write(result.content)
            # match = None
            # match = PATTERN_ABOUT.search(result.text)
            soup = bs(result.content, 'lxml')
            soup_match = None
            soup_match = soup.select_one('#m-timeline-cover-section > div:nth-of-type(4) > a')
            soup_match_ratelimit = (soup.title.text == "You Can't Use This Feature Right Now")
            print('Visit profile > Get about link:', person)
            if soup_match and soup_match.get_text() == 'About':
                link_about_safe = soup_match.get('href')
                list_friends[person]['link_about'] = LINK_MAIN + link_about_safe
            else:
                print('ERROR: No about link!')
            with open('data/' + 'list_friends.json', 'w') as f:
                json.dump(list_friends, f, indent=2, ensure_ascii=False)

for person in list_friends:
    # Visit about link and save html to parse later
    if 'link_about' in list_friends[person]:
        filename = 'data/' + 'about_' + person + '.html'
        file = Path(filename)
        redownload = False
        if file.is_file():
            with open(filename) as f:
                file_html = f.read()
            soup = bs(file_html, 'lxml')
            soup_match = None
            soup_match = (soup.title.text == "You Can't Use This Feature Right Now") or \
                (soup.title.text == "Content Not Found") or \
                (soup.title.text == "Error Facebook") or \
                (soup.title.text == "Profile Pictures")
            # match = None
            # match = PATTERN_RATELIMIT.search(file_html)
            if soup_match:
                redownload = True
        if (not file.is_file()) or redownload:
            print('Visit About > Save HTML:', person)
            link = list_friends[person]['link_about']
            time.sleep(30)
            result = session.get(link)
            with open(filename, 'wb') as f:
                f.write(result.content)



# for person in list_friends:

#     # Print Name
#     print('')
#     print(person)

#     # Name
#     fullname = person
#     names = fullname.split(' ')
#     if len(names) == 3:
#         name_first = names[0]
#         name_mid = names[1]
#         name_last = names[2]
#     elif len(names) == 2:
#         name_first = names[0]
#         name_mid = ''
#         name_last = names[1]
#     elif len(names) == 4:
#         name_first = names[0]
#         name_mid = names[1] + ',' + names[2]
#         name_last = names[3]
#     else:
#         name_first = ''
#         name_mid = ''
#         name_last = ''
#     name = '{family};{given};{additional};{prefix};{suffix}'.format(family=name_last, given=name_first, additional=name_mid, prefix='', suffix='')
#     print('FN:' + fullname)
#     print('N:' + name)


# pprint(list_friends)
