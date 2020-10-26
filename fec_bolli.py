## Licenza Libera progetto originario di Claudio Pizzillo
## Modifiche e riadattamenti da Salvatore Crapanzano
## V. 1.1 - Intermediari e Diretto

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import re
import time
from datetime import timedelta, datetime, tzinfo, timezone
import sys
import pytz
import json
import os
    
def unixTime():
    dt = datetime.now(tz=pytz.utc)
    return str(int(dt.timestamp() * 1000))

CF = sys.argv[1]
PIN = sys.argv[2]
Password  = sys.argv[3]
CODFISC  = sys.argv[4]
PIVA = sys.argv[5] // PARTA IVA STUDIO ASSOCIATO
TRIM = sys.argv[6]
ANNO = sys.argv[7]

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
# Delega diretta
payload = {'cf_inserito': CODFISC}    
r = s.post('https://ivaservizi.agenziaentrate.gov.it/portale/scelta-utenza-lavoro?p_auth='+ p_auth + '&p_p_id=SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet_javax.portlet.action=delegaDirettaAction', data=payload)

# Me stesso
# payload = {'sceltaincarico': PIVA + '-000', 'tipoincaricante' : 'incDiretto'}    
# r = s.post('https://ivaservizi.agenziaentrate.gov.it/portale/scelta-utenza-lavoro?p_auth='+ p_auth + '&p_p_id=SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet_javax.portlet.action=meStessoAction', data=payload)

# MODIFICA STUDIO ASSOCIATO
# payload = {'sceltaincarico': PIVA + '-000', 'tipoincaricante' : 'incDelega', 'cf_inserito': CODFISC}    
# r = s.post('https://ivaservizi.agenziaentrate.gov.it/portale/scelta-utenza-lavoro?p_auth='+ p_auth + '&p_p_id=SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet_javax.portlet.action=incarichiAction', data=payload)
#
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
		   'Content-Type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}


# print('Accetto le condizioni')
# r = s.get('https://ivaservizi.agenziaentrate.gov.it/cons/cons-services/rs/disclaimer/accetta?v='+unixTime() , headers = headers )
# cookieJar = s.cookies

# r = s.get('https://ivaservizi.agenziaentrate.gov.it/ser/api/monitoraggio/v1/monitoraggio/fatture/?v='+unixTime()+'&idFiscCedente=&idFiscDestinatario=&idFiscEmittente=&idFiscTrasmittente=&idSdi=&perPage=10&start=1&statoFile=&tipoFattura=EMESSA')

print('Scarico il json deI BOLLI ELETTRONICI per la CODICE FISCALE ' + CODFISC)
r = s.get('https://ivaservizi.agenziaentrate.gov.it/cons/cons-web/?v='+unixTime()+'#/fatture/bollo', headers = headers)
cookieJar = s.cookies
r = s.get('https://ivaservizi.agenziaentrate.gov.it/cons/cons-services/rs/fe/bollo/elenco/X/'+ANNO+'/'+TRIM+'?v=+unixTime()', headers = headers_token)
cookieJar = s.cookies
with open('fe_bollo.json', 'wb') as f:
    f.write(r.content)
print('Inizio a scaricare i bolli')
path = r'F24_Bolli_' + TRIM + ANNO
if not os.path.exists(path):
    os.makedirs(path)
r = s.get('https://ivaservizi.agenziaentrate.gov.it/cons/cons-services/rs/fe/bollo/dettaglio/'+TRIM+''+ANNO+''+PIVA+'?v='+unixTime() , headers = headers )
cookieJar = s.cookies
data = json.load(open("fe_bollo.json"))
bollojson3 = data['fattureBollo'][0]
print(bollojson3)
url = 'https://ivaservizi.agenziaentrate.gov.it/cons/cons-services/rs/fe/bollo/stampa/F24'
response = requests.post(url, data=json.dumps(bollojson3).encode("utf-8"), verify=False, headers = headers, cookies=cookieJar)
if r.status_code == 200:
    with open(path + '/' + CODFISC + '_F24_BOLLI.PDF', 'wb') as f:
        f.write(response.content)
sys.exit()
