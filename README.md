# FeCscraper

This repository contains a collection of utilities to fetch data from the
[Fatture e Corrispettivi](https://ivaservizi.agenziaentrate.gov.it/portale/)
website by Agenzia delle Entrate.

Originally, this repository has been created by
[@claudiopizzillo](https://github.com/claudiopizzillo/FeCscraper) and forked by
[@socrat3](https://github.com/socrat3/FeCscraper).
The version of the code within this repository is a fork of the code updated by
@socrat3.

For more information see also old README file at [README-old.md](README-old.md).

## Configuration

Dependencies are defined in `requirements.txt` and can be installed with `pip`;
just run:

```shell
$ pip install -r requirements.txt
```

## Usage

The `scripts` directory contains the scripts to fetch data from Fatture e
Corrispettivi.
In the following, examples on how to run them.

> *:warning: If not specified, dates use `DDMMYYYY` format.*

### fe.py

```shell
$ python scripts/python fec.py \
    <FISCAL_CODE> \
    <PIN> <PASSWORD> \
    <VAT_NUMBER> \
    <DATE_FROM> <DATE_TO>
```

### fec_emesse_dylog.py

```shell
$ python scripts/fec_emesse_dylog.py \
    <Codice_entratel_fiscoonline> \
    <codice_PIN_entratel_fiscoonline> \
    <password_fiscoonline> \
    <codice_fiscale_studio_intermediario> \
    <DATE_FROM> <DATE_TO> \
    <CF_cliente> \
    <Partita_IVA_cliente> \
    1
```

### fec_ricevutedisposizione.py

```shell
$ python scripts/fec_ricevutedisposizione.py \
    <Codice_entratel_fiscoonline> \
    <codice_PIN_entratel_fiscoonline> \
    <password_fiscoonline> \
    <codice_fiscale_studio_intermediario> \
    <DATE_FROM> <DATE_TO> \
    <CF_cliente> \
    <Partita_IVA_cliente> \
    1
```

### fec_trasfrontalieremesse.py

```shell
$ python scripts/fec_trasfrontalieremesse.py \
    <Codice_entratel_fiscoonline> \
    <codice_PIN_entratel_fiscoonline> \
    <password_fiscoonline> \
    <codice_fiscale_studio_intermediario> \
    <DATE_FROM> <DATE_TO> \
    <CF_cliente> \
    <Partita_IVA_cliente> \
    1
```

### fec_ricevute.py

```shell
$ python scripts/fec_ricevute.py \
    <Codice_entratel_fiscoonline> \
    <codice_PIN_entratel_fiscoonline> \
    <password_fiscoonline> \
    <codice_fiscale_studio_intermediario> \
    <DATE_FROM> <DATE_TO> \
    <CF_cliente> \
    <Partita_IVA_cliente> \
    1
```

## Acknowledge

Thanks to
[@claudiopizzillo](https://github.com/claudiopizzillo/),
[@socrat3](https://github.com/socrat3) and
[Salvatore Crapanzano](https://www.salvatorecrapanzano.com/)
that, before me, contributed to this code.



