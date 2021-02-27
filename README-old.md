# Downloader Fatture elettroniche e i modelli f24 bolli

Progetto derivato da FeCscraper di Pizzillo e modificato da Salvatore Crapanzano https:\\www.salvatorecrapanzano.com

py fec_emesse_dylog.py Codice_entratel_fiscoonline codice_PIN_entratel_fiscoonline password_fiscoonline codice_fiscale_studio_intermediario 01012020 31032020 CF_cliente Partita_IVA_cliente

py fec_ricevutedisposizione.py Codice_entratel_fiscoonline codice_PIN_entratel_fiscoonline password_fiscoonline codice_fiscale_studio_intermediario 01012020 31032020 CF_cliente Partita_IVA_cliente 1

py fec_trasfrontalieremesse.py Codice_entratel_fiscoonline codice_PIN_entratel_fiscoonline password_fiscoonline codice_fiscale_studio_intermediario 01012020 31032020 CF_cliente Partita_IVA_cliente 1

py fec_ricevute.py Codice_entratel_fiscoonline codice_PIN_entratel_fiscoonline password_fiscoonline codice_fiscale_studio_intermediario 01012020 31032020 CF_cliente Partita_IVA_cliente 1


Script per automatizzare il download delle fatture elettroniche e i bolli e le fatture transfrontaliere e le fatture a disposizione usando il servizio Fatture e Corrispettivi. 

Scarica:
a) le fatture emesse e ricevute per data di emissione e per data do ricezione (incorpora le modifiche della AdE di febbraio 2020)
b) modello f24 dei bolli
c) le fatture a disposizione

Vi consiglio di eseguire lo script per il download delle fatture elettroniche ricevute dopo l'esecuzione dello script fatture a disposizione.

Dipendenze Librerie da installare via pip: requests e pytz.

Dati di input in ordine:

CF (Codice fiscale o codice Entratel dell'intermediario commercialista o dello studio associato o del contribuente) di FeC.
PIN di FeC.
Password di FeC.
Codice Fiscale # indicare il cf del cliente o cf del soggetto intermediario appartenente allo studio associato
Data dal
Data al
cf cliente # ripete il cf del cliente, 
piva cliente
[1/2] solo per le fatture ricevute scaricamento per data di ricezione e/o emissione  # 1 per data di ricezione 2 per data di emissione

Nella sottocartella contenente il cf del contribuente troverai le tue FE e i relativi metadati.

Per i bolli 
CF (Codice fiscale o codice Entratel) di FeC.
PIN di FeC.
Password di FeC.
Codice Fiscale
Partita IVA
Numero Trimestre es: 1 o 2 o 3 o 4 
Anno Es. 2020

att.ne per funzionare la data di scaricamento devi essere antecedente o uguale alla data di pagamento

Ci sono diverse modalitù di accesso, da madificare direttamente nel file
a) me stesso
b) incaricati singoli professionisti
c) incaricati professionisti che fanno parte di uno studio associato

SE NON FUNZIONA, PER VOI DOVETE VEDERE QUESTA PARTE DEL CODICE. CON LO SCRIPT CHE HO CARICATO. FUNZIONA!

Esempio riga comando:
py fec_emesse_dylog.py Codice_entratel_fiscoonline codice_PIN_entratel_fiscoonline password_fiscoonline codice_fiscale_studio_intermediario 01012020 31032020 CF_cliente Partita_IVA_cliente

py fec_ricevutedisposizione.py Codice_entratel_fiscoonline codice_PIN_entratel_fiscoonline password_fiscoonline codice_fiscale_studio_intermediario 01012020 31032020 CF_cliente Partita_IVA_cliente 1

py fec_trasfrontalieremesse.py Codice_entratel_fiscoonline codice_PIN_entratel_fiscoonline password_fiscoonline codice_fiscale_studio_intermediario 01012020 31032020 CF_cliente Partita_IVA_cliente 1

py fec_ricevute.py Codice_entratel_fiscoonline codice_PIN_entratel_fiscoonline password_fiscoonline codice_fiscale_studio_intermediario 01012020 31032020 CF_cliente Partita_IVA_cliente 1



