# -*- coding: utf-8 -*-
""" Main application - scrapes water temp """

import re
import requests
from bs4 import BeautifulSoup
import requests
import sys
from datetime import datetime
from datetime import timedelta

URL = 'http://hydro.chmi.cz/hpps/popup_hpps_prfdyn.php?seq=307046'

def get_api_key():
    key = ''
    with open('owm.key', 'r') as file:
        key = file.read().replace('\n','')
    return key

def make_owm_request(path, **kwargs):
    params = dict(**kwargs)

    params['appid'] = get_api_key()
    params['exclude'] = 'current,minutely,daily,alerts'
    params['units'] = 'metric'

    result = requests.get(
        'https://api.openweathermap.org/data/2.5/' + path,
        params=params
    )

    message = result.json()

    return result.json()

def into_utc(hours):
    return hours - 1

def get_forecast():
    lat=48.959655
    lon=14.478576
    pocasi = make_owm_request('onecall', lat=lat, lon=lon)
    
    # od 7mi hodin ukazuje teplotu na zitra
    zanor_zitra = datetime.utcnow().hour >= into_utc(7)

    cas_dalsiho_zanoru = None
    now = datetime.utcnow()

    cas_dalsiho_zanoru = datetime(now.year, now.month, now.day, into_utc(7), 0)
    if zanor_zitra:
        cas_dalsiho_zanoru += timedelta(days=1)

    for hodinova_predpoved in pocasi["hourly"]:
        if hodinova_predpoved["dt"] == int(cas_dalsiho_zanoru.timestamp()):
            return hodinova_predpoved

def vypis_predpoved(forecast):
    zanor_zitra = datetime.utcnow().hour >= into_utc(7)
    text = ''
    if zanor_zitra:
        text += 'Zítřejší zánor v 7:15:' + '\n'
    else:
        text += 'Dnešní zánor v 7:15:' + '\n'

    text += 'Teplota: ' + str(forecast['temp']) + '\n'
    text += 'Pocitovka: ' + str(forecast['feels_like']) + '\n'
    text += 'Otužilecký nebe: ' + str(100 - int(forecast['clouds'])) + ' %\n'
    text += 'Chcanec: ' + str(forecast['pop']) + ' %'
    return text

def main():
    """ Hlavni funkce programu """

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    # dostaneme div, ve kterym to je
    div = soup.find_all(class_='tborder center_text')

    # jdeme dovnitr divu
    table = list(div[0].children)[1]
    # zde uz je 1. header, 3. je prvni zaznam,
    # 5. je druhej zaznam, ... (mezi tim jsou '\n')

    # ziska prvni radek cely tabulky
    first_record = list(table.children)[3]

    # ziska zaznamy o case a teplote
    time_record = list(first_record.children)[1]
    temp_record = list(first_record.children)[7]

    # zaznam musi obsahovat cislo, '.' nebo ':' a koncit cislem
    # tim padem to nejdriv ziska datum a pak dalsi jeste cas
    date = re.findall("[0-9.:]*[0-9]", str(time_record))[0]
    time = re.findall("[0-9.:]*[0-9]", str(time_record))[1]

    # tady vezmu nejakej pocet cisel, tecku a pak jedno cislo
    # pylint: disable-msg=anomalous-backslash-in-string
    temp = re.findall("[0-9.]*[0-9]", str(temp_record))[0]

    out_data = "Datum: " + date + "\n"
    out_data += "Čas: " + time + "\n"
    out_data += "Teplota vody: " + temp + " °C" + "\n"

    out_data += "----------------------\n"
    forecast = get_forecast()
    out_data += vypis_predpoved(forecast)

    with open('chmu_teplota_vody.json', 'w') as out_file:
        out_file.write(out_data)


if __name__ == "__main__":
    main()
