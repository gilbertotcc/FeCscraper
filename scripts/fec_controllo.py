## Licenza Libera progetto originario di Claudio Pizzillo (codice per accesso al sito)
## Antonino Accardo (codice per il controllo del file)
## Crapanzano Salvatore (riadattamento per controllo fattura ed invio diretto)
## Per effettuare il controllo sul portale ivaservizi.agenziaentrate.gov.it, inserire il nome del file nella relativa parte del codice
## Vers. 1.0 del 28012021
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import re
import sys
import pytz
import json
import time
from datetime import datetime


def unixTime():
    dt = datetime.now(tz=pytz.utc)
    return str(int(dt.timestamp() * 1000))

now = datetime.now() # current date and time
profilo = 1
CF = sys.argv[1]
PIN = sys.argv[2]
Password  = sys.argv[3]
cfstudio = sys.argv[4]
cfcliente = sys.argv[5]
pivadiretta  = sys.argv[6]
nome_file = sys.argv[7]

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'})
s.headers.update({'Connection': 'keep-alive'})

cookie_obj1 = requests.cookies.create_cookie(domain='ivaservizi.agenziaentrate.gov.it',name='LFR_SESSION_STATE_20159',value='expired')
s.cookies.set_cookie(cookie_obj1)
cookie_obj2 = requests.cookies.create_cookie(domain='ivaservizi.agenziaentrate.gov.it',name='LFR_SESSION_STATE_10811916',value=unixTime())
s.cookies.set_cookie(cookie_obj2)
r = s.get('https://ivaservizi.agenziaentrate.gov.it/portale/web/guest', verify=False)

print('Collegamento alla homepage')
cookieJar = s.cookies

print('Effettuo il login')
payload = {'_58_saveLastPath': 'false', '_58_redirect' : '', '_58_doActionAfterLogin': 'false', '_58_login': CF , '_58_pin': PIN, '_58_password': Password}    
r = s.post('https://ivaservizi.agenziaentrate.gov.it/portale/home?p_p_id=58&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_pos=3&p_p_col_count=4&_58_struts_action=%2Flogin%2Flogin', data=payload)
cookieJar = s.cookies

liferay = re.findall(r"Liferay.authToken = '.*';", r.text)[0]
p_auth = liferay.replace("Liferay.authToken = '","")
p_auth = p_auth.replace("';", "")

r = s.get('https://ivaservizi.agenziaentrate.gov.it/dp/api?v=' + unixTime())
cookieJar = s.cookies

print('Seleziono il tipo di incarico')
# payload = {'sceltaincarico': cfstudio + '-000', 'tipoincaricante' : 'incDiretto'}    
# r = s.post('https://ivaservizi.agenziaentrate.gov.it/portale/scelta-utenza-lavoro?p_auth='+ p_auth + '&p_p_id=SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet_javax.portlet.action=incarichiAction', data=payload)

if profilo == 1:
# Delega Diretta
            payload = {'cf_inserito': cfcliente};
            r = s.post('https://ivaservizi.agenziaentrate.gov.it/portale/scelta-utenza-lavoro?p_auth='+ p_auth + '&p_p_id=SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet_javax.portlet.action=delegaDirettaAction', data=payload);
            payload = {'cf_inserito': cfcliente, 'sceltapiva' : pivadiretta};    
            r = s.post('https://ivaservizi.agenziaentrate.gov.it/portale/scelta-utenza-lavoro?p_auth='+ p_auth + '&p_p_id=SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet_javax.portlet.action=delegaDirettaAction', data=payload);
# Me stesso
elif profilo == 2:
            payload = {'sceltaincarico': cfstudio + '-000', 'tipoincaricante' : 'incDiretto'};
            r = s.post('https://ivaservizi.agenziaentrate.gov.it/portale/scelta-utenza-lavoro?p_auth='+ p_auth + '&p_p_id=SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet_javax.portlet.action=meStessoAction', data=payload)
            payload = {'sceltaincarico': cfstudio + '-000', 'tipoincaricante' : 'incDiretto', 'sceltapiva' : pivadiretta};    
            r = s.post('https://ivaservizi.agenziaentrate.gov.it/portale/scelta-utenza-lavoro?p_auth='+ p_auth + '&p_p_id=SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet_javax.portlet.action=meStessoAction', data=payload);
# Login per STUDIO ASSOCIATO
else:
            payload = {'sceltaincarico': cfstudio + '-000', 'tipoincaricante' : 'incDelega', 'cf_inserito': cfcliente};
            r = s.post('https://ivaservizi.agenziaentrate.gov.it/portale/scelta-utenza-lavoro?p_auth='+ p_auth + '&p_p_id=SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet_javax.portlet.action=incarichiAction', data=payload);
            payload = {'sceltaincarico': cfstudio + '-000', 'tipoincaricante' : 'incDelega', 'cf_inserito': cfcliente, 'sceltapiva' : pivadiretta};
            r = s.post('https://ivaservizi.agenziaentrate.gov.it/portale/scelta-utenza-lavoro?p_auth='+ p_auth + '&p_p_id=SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet_javax.portlet.action=incarichiAction', data=payload);




print('Aderisco al servizio')
r = s.get('https://ivaservizi.agenziaentrate.gov.it/ser/api/fatture/v1/ul/me/adesione/stato/')
cookieJar = s.cookies

headers_token = {'x-xss-protection': '1; mode=block',
           'strict-transport-security': 'max-age=16070400; includeSubDomains',
           'x-content-type-options': 'nosniff',
           'x-frame-options': 'deny'}
r = s.get('https://ivaservizi.agenziaentrate.gov.it/cons/cons-services/sc/tokenB2BCookie/get?v='+unixTime() , headers = headers_token )
cookieJar = s.cookies
tokens = r.headers

xb2bcookie = r.headers.get('x-b2bcookie')
xtoken = r.headers.get('x-token')


s.headers.update({'Host': 'ivaservizi.agenziaentrate.gov.it'})
s.headers.update({'Referer': 'https://ivaservizi.agenziaentrate.gov.it/cons/cons-web/?v=' + unixTime()})
s.headers.update({'Accept': 'application/json, text/plain, */*'})
s.headers.update({'Accept-Encoding': 'gzip, deflate, br'})
s.headers.update({'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6'})
s.headers.update({'DNT': '1'})
s.headers.update({'X-XSS-Protection': '1; mode=block'})
s.headers.update({'Strict-Transport-Security': 'max-age=16070400; includeSubDomains'})
s.headers.update({'X-Content-Type-Options': 'nosniff'})
s.headers.update({'X-Frame-Options': 'deny'})
s.headers.update({'x-b2bcookie': xb2bcookie})
s.headers.update({'x-token': xtoken})

headers = {'Host': 'ivaservizi.agenziaentrate.gov.it',
           'referer': 'https://ivaservizi.agenziaentrate.gov.it/cons/cons-web/?v=' + unixTime(),
           'accept': 'application/json, text/plain, */*',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
           'DNT': '1',
           'x-xss-protection': '1; mode=block',
           'strict-transport-security': 'max-age=16070400; includeSubDomains',
           'x-content-type-options': 'nosniff',
           'x-frame-options': 'deny',
           'x-b2bcookie': xb2bcookie,
           'x-token': xtoken,
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}

print('Accetto le condizioni')
r = s.get('https://ivaservizi.agenziaentrate.gov.it/cons/cons-services/rs/disclaimer/accetta?v='+unixTime() , headers = headers_token )
cookieJar = s.cookies


print('controllo file')
r = s.get('https://ivaservizi.agenziaentrate.gov.it/ser/fatturewizard/html/partials/supporto/controllo.html?v='+now.strftime("%Y-%m-%d"), headers = headers)

   

#seleziona file 
## nome_file='IT02081640845_00001.xml'
f=open(nome_file, "rb")

headers_file= { 'Host': 'ivaservizi.agenziaentrate.gov.it',
                'referer': 'https://ivaservizi.agenziaentrate.gov.it/ser/fatturewizard/',
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate',
                'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
                'x-xss-protection': '1; mode=block',
                'strict-transport-security': 'max-age=16070400; includeSubDomains',
                'x-content-type-options': 'nosniff',
                'Origin': 'https://ivaservizi.agenziaentrate.gov.it',
                'X-XSS-Protection': '1, mode=block',
                'x-frame-options': 'deny',
                'x-b2bcookie': xb2bcookie,
                'x-token': xtoken,
                'sec-fetch-site': 'same-origin',
                'content-length':'9049',
                'content-type': 'application/octet-stream',
                'sec-fetch-mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'connection': 'keep-alive',
                'x-nome-file': nome_file,
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}    

print(f)    
r = s.post('https://ivaservizi.agenziaentrate.gov.it/ser/api/fatture/v1/conservazione/fatture/?v='+unixTime(),headers=headers_file , data=f)
# https://ivaservizi.agenziaentrate.gov.it/ser/api/fatture/v1/conservazione/fatture/?v=1611829854516
print(r.status_code)
if r.status_code == 500:
    print('Servizio dell''Azenzia delle entrate non disponibile')
    print('Controllo non andanto a buon fine, riprovare più tardi')
    print('Disconnessione in corso')
    r = s.get('https://ivaservizi.agenziaentrate.gov.it/portale/c/portal/logout')
    sys.exit()
if r.status_code == 200:
    print('ok')
    print(r.text)
c=str(r.text)
time.sleep(10)
r = s.get('https://ivaservizi.agenziaentrate.gov.it/ser/api/fatture/v1/controllo/fatture/'+c+'/?v='+unixTime(), headers=headers)
if r.status_code == 200:
    print('ok')
time.sleep(10) 
with open('fe_controllo.json', 'wb') as f:
    f.write(r.content)

with open('fe_controllo.json') as data_file:    
    datas = json.load(data_file)
    control= (datas['completato'])
    print (control)
if control != 'True':
     print('Controllo andanto a buon fine')
     print('Lavoro finito disconnessione in corso')
     r = s.get('https://ivaservizi.agenziaentrate.gov.it/portale/c/portal/logout')
     if r.status_code == 200:
      print('Fine sessione')   
     else:
        print('Controllo non andanto a buon fine')
        print('Lavoro finito disconnessione in corso')
        r = s.get('https://ivaservizi.agenziaentrate.gov.it/portale/c/portal/logout')
        if r.status_code == 200:
         print('Fine sessione')

sys.exit()
