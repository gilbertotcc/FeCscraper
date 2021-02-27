import requests
import re
import time
import sys
import pytz
import json
import os
import datetime

from datetime import datetime

    
def unixTime():
    dt = datetime.now(tz=pytz.utc)
    return str(int(dt.timestamp() * 1000))

profilo = 1 # Impostare il profilo Delega diretta codice 1, Me stesso 2, Studio Associato Default
CF = sys.argv[1]
PIN = sys.argv[2]
Password  = sys.argv[3]
cfstudio  = sys.argv[4]
Dal = sys.argv[5]
Al = sys.argv[6]
cfcliente = sys.argv[7]
pivadiretta = sys.argv[8]
print('Sintassi:')
print('py fec_emesse.py UTENZA_ENTRATEL pin_entratel password_entratel cfstudio Data_inizio Data_fine cf_cliente piva_cliente')
time.sleep(5)

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

# r = s.get('https://ivaservizi.agenziaentrate.gov.it/ser/api/monitoraggio/v1/monitoraggio/fatture/?v='+unixTime()+'&idFiscCedente=&idFiscDestinatario=&idFiscEmittente=&idFiscTrasmittente=&idSdi=&perPage=10&start=1&statoFile=&tipoFattura=EMESSA')
print('Scarico il json delle fatture Emesse per la Partita IVA ' + cfcliente)
r = s.get('https://ivaservizi.agenziaentrate.gov.it/cons/cons-services/rs/ft/emesse/dal/'+Dal+'/al/'+Al+'?v=' + unixTime(), headers = headers)

with open('fe_emessetr.json', 'wb') as f:
    f.write(r.content)
    
print('Inizio a scaricare le fatture emesse')
path = r'FattureEmesseTRAN_' + cfcliente
if not os.path.exists(path):
    os.makedirs(path)
with open('fe_emessetr.json') as data_file:    
    data = json.load(data_file)
    numero_fatture = 0
    numero_notifiche = 0
    for fattura in data['fatture']:
        fatturaFile = fattura['tipoInvio']+fattura['idFattura']
        idInviofile = fattura['fileDownload']['idInvio']
        datafatturajson = fattura['dataFattura']
        datafatturaAAAAMMDD = datetime.strptime(datafatturajson, "%Y-%m-%d")
        strdatafatturaGGMMAAAA = datetime.strftime(datafatturaAAAAMMDD, "%m/%d/%Y")
        filejsonindinvio = 'fatturaID'+idInviofile+'.json'
        r = s.get('https://ivaservizi.agenziaentrate.gov.it/cons/cons-services/rs/fatture/file/'+fatturaFile+'?tipoFile=FILE_FATTURA&download=1&v='+unixTime() , headers = headers_token )
        if r.status_code == 200:
            numero_fatture = numero_fatture + 1
            d = r.headers['content-disposition']
            fname = re.findall("filename=(.+)", d)
            print('Downloading ' + fname[0])
            print('Totale fatture scaricate: ', numero_fatture)
            pathsub = r'FattureEmesse_' + cfcliente + '_' + str(numero_fatture)
            if not os.path.exists(path):
                 os.makedirs(path)
            with open(path + '/' + fname[0], 'wb') as f:
                f.write(r.content)
                fmetadato = re.findall("filename=(.+)", d)
                r = s.get('https://ivaservizi.agenziaentrate.gov.it/ser/api/monitoraggio/v1/monitoraggio/fatture/dettaglio/?v='+unixTime()+'&idSdi='+idInviofile+'&operatore=e', headers = headers_token )
        # filejsonindinvio = json.dumps(dict(requests.get('https://ivaservizi.agenziaentrate.gov.it/ser/api/monitoraggio/v1/monitoraggio/fatture/dettaglio/?v='+unixTime()+'&idSdi='+idInviofile+'&operatore=e').headers_token))
        if r.status_code == 200:
            filejsonindinvio = 'fatturaID'+idInviofile+'.json'
        with open(filejsonindinvio, 'wb') as fj:
            fj.write(r.content)
            print('Scarico file json della fattura emessa: '+'fatturaID'+idInviofile+'.json')
        with open(filejsonindinvio) as dati:
            print(dati)
            datajson = json.load(dati)
            if datajson['elencoNotifiche'] == []:
                print('No Data123!')
            else:
                for idSDIelenco in datajson['elencoNotifiche'] :
                    print('ID Invio:' + str(idSDIelenco['id']))
                    print('nome:' + str(idSDIelenco['nome']))
                    print('Data UNIX' + str(idSDIelenco['dataConsegna']))
                for idSDIelenco in datajson['elencoNotifiche']:
                    tipettofile = str(idSDIelenco['nome'])
                    if tipettofile == "File dei metadati":
                         print("Ho Scaricato correttamente il file metadati!")
                    else:
                        idSDIinvio = idSDIelenco['id']
                        stridSDIinvio = str(idSDIinvio)
                        r = s.get('https://ivaservizi.agenziaentrate.gov.it/ser/api/monitoraggio/v1/monitoraggio/fatture/notifiche/'+stridSDIinvio+'/download/' , headers = headers_token)
                        if r.status_code == 200:
                             d = r.headers['content-disposition']
                             fname = re.findall("filename=(.+)", d)
                             with open(path + '/' + fname[0], 'wb') as f:
                                 f.write(r.content)
        #os.system('cls')
print('Per il cliente: ', cfcliente)
print('Totale fatture trasfrontaliere scaricate: ', numero_fatture)
print('Totale notifiche scaricate: ', numero_notifiche)
sys.exit()

