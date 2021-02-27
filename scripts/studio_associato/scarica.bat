# Versione per Studio Associato 1.0 - Lillo
@echo off
set INIZIO=
SET FINE=
SET /P INIZIO=Digita Data Inizio:
SET /P FINE=Digita Data Fine:
set STRINGA=
set /P STRINGA=Digita cliente: 
SET /P cliente=%STRINGA%
SET /P DATAINIZIO=%INIZIO%
SET /P DATAFINE=%FINE%
cls
py fec_emesse.py utente pin password 024XXXXXXXX %INIZIO% %FINE% %STRINGA%
py fec_ricevute3.py utente pin password 024XXXXXXXX %INIZIO% %FINE% %STRINGA%
py fec_trasfontalieremesse.py utente pin password 024XXXXXXXX %INIZIO% %FINE% %STRINGA%
cls
echo                       Programma Terminato.
