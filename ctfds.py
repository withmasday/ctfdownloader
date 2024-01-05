import requests, sys, re, json, os

# INIT
sess = requests.Session()

username = input('[?] USERNAME : ')
password = input('[?] PASSWORD : ')
url = input('[?] URL      : ')
out = input('[?] DIR      : ')

try:
    os.mkdir(out)
except:
    pass

check = sess.get(url + '/login').text
nonce = re.findall(f'<input id="nonce" name="nonce" type="hidden" value="(.*?)">', check)[0]
credential = {
    "name": username,
    "password": password,
    "_submit": "Submit",
    "nonce": nonce,
}

signin = sess.post(url + '/login', data=credential).text
if 'Your username or password is incorrect' in signin:
    print ('[!] Invalid Credential.')
    sys.exit()
    
jsonChalls = sess.get(url +'/api/v1/challenges').text
challenges = json.loads(jsonChalls)

for chall in challenges['data']:
    challID = chall['id']
    categories = chall['category']
    name = chall["name"]
    name = name.replace(' ', '')
    
    try:
        os.mkdir(f'{out}/{categories}')
        print (f' [~] Create cat directory : {out}/{categories}')
    except:
        print (f' [!] Directory {out}/{categories} avaiable.')
        
    print (f' [~] Downloading - {categories} - {name}')
    
    detChall = sess.get(url +'/api/v1/challenges/'+ str(challID)).text
    jsonChall = json.loads(detChall)['data']
    
    description = jsonChall['description']
    
    try:
        os.mkdir(f'{out}/{categories}/{name}')
        print (f' [~] Create chall directory : {out}/{categories}/{name}')
    except:
        print (f' [!] Directory {out}/{categories}/{name} avaiable.')
        
    readme = open(f'{out}/{categories}/{name}/README.md', 'w')
    readme.write(f'{name}\n')
    readme.write(f'Description : {description}\n')
    readme.write(f'Hint : ')
    
    try:
        for hints in jsonChall:
            if "content" in hints:
                readme.write(f' - {hints.content}\n')
    except:pass
    
    readme.write('\n\n')
    for attachment in jsonChall['files']:
        filename = attachment.split("?token")[0].split("/")[-1]
        filedata = sess.get(url + '/' + attachment).content
        
        fileChall = open(f'{out}/{categories}/{name}/{filename}', 'wb')
        fileChall.write(filedata)
        fileChall.close()
        
        try:
            readme.write(f'Attachment : \n{url}{attachment}')
        except:pass
    
    readme.close()
    
    print ("")
