# Written by Ash Johnson
# ----------------------

import facebook
from termcolor import colored
from os import system, name
import requests
import json
import csv
import time
import sys

def wrap_by_word(s, n):
    a = s.split()
    ret = ''
    for i in range(0, len(a), n):
        ret += ' '.join(a[i:i+n]) + '\n'
    return ret

def new_access_token():
    access_token = input(colored('✖︎✖︎✖︎✖︎✖︎✖︎ ACCESS TOKEN ✖︎✖︎✖︎✖︎✖︎✖︎\n', 'blue', attrs=['reverse', 'bold']))
    with open('instagram_access_token.txt', 'w') as f:
        f.write(access_token)
    return access_token
# get the API KEY
try:
    with open('instagram_access_token.txt', 'r') as f:
        access_token = f.readline()
except:
    access_token = ''

#  Check if the access token has been loaded for the first time
if not access_token:
    system('clear')
    print(colored('Access Token not found', 'red'))
    access_token = new_access_token()
# Access the API

api_accessed = False
while not api_accessed:
    try:
        system('clear')
        graph = facebook.GraphAPI(access_token=access_token, version="2.12")
        #  Get the first post
        # Fetch Facebook post id
        me = graph.get_object('me/accounts')
        facebook_id = me['data'][0]['id']
        print(colored('✅ Facebook page id → ', 'green') + colored(facebook_id, 'yellow' ))
        #  Fetch Instagram id
        instagram = graph.get_object(facebook_id, fields='instagram_business_account')
        instagram_id = instagram['instagram_business_account']['id']
        print(colored('✅ Instagram id → ', 'green') + colored(instagram_id, 'yellow'))
        # Fetch posts
        posts = graph.get_object(instagram_id+'/media')
        api_accessed = True
    except:
        system('clear')
        print(colored('✖︎✖︎✖︎✖︎✖︎✖︎ ERROR ✖︎✖︎✖︎✖︎✖︎✖︎', 'red', attrs=['reverse', 'bold']))
        print(colored('There is an issue with the access token. You need to get a new one from', 'red'))
        print(colored('https://developers.facebook.com/tools/explorer/', 'magenta'))
        access_token = new_access_token()

#  THE APP:
for post in posts['data']:
    post_data = graph.get_object(post['id'], fields='caption')
    post_id = post_data['id']
    print(colored('📷 Post id → ', 'green') + colored(post_id, 'yellow' ) + '\n')
    print(colored(wrap_by_word(
        post_data['caption'], 10), 'white', attrs=['dark']))
    #  Get user input
    input_required = True
    get_comment = ''
    while input_required:
        get_comment = input(colored("Get comments 'y/n/q'? ", 'magenta'))
        if get_comment == "y" or get_comment == 'n':
            input_required = False
        elif get_comment == 'q':
            sys.exit(1)
        else:
            print(colored('Not a valid option. Use y/n/q', 'red'))
    if get_comment == 'y':
        break

#  Process the post to scrape all comments
post_data = graph.get_object(post_id + '/comments', fields='username,text')
#  Comment
print(colored('\n✅ Data fetched', 'green'))

data = post_data['data']
get_all_data = False
print('  total items: ' + str(len(data)))

while not get_all_data:
    try:
        page = post_data['paging']['next']
        post_data = requests.get(page).json()
        data += post_data['data']
        #  Comment
        print(colored('→ Loading next page...', 'blue'))
        print('  total items: ' + str(len(data)))

    except:
        get_all_data = True
#  Comment
print(colored('\n✅ TOTAL IMPORTED: ' + str(len(data)), 'green'))

#  Write out the file
filename = str(int(time.time())) + '.csv'
#  Comment
print(colored('\n💾 exporting to ' + filename, 'yellow'))
file = open(filename, 'w', newline='')

with file:
    export = csv.writer(file)
    export.writerow(["Username", "Comment", "ID"])
    for row in data:
        export.writerow([row["username"],
                            row["text"],
                        row["id"]])
print(colored('\n✅ File successfully exported', 'green'))
