# -*- coding: utf-8 -*-
""" Main application - scrapes water temp """

import re
import requests
from bs4 import BeautifulSoup

URL = 'http://hydro.chmi.cz/hpps/popup_hpps_prfdyn.php?seq=307046'

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
    temp = re.findall("[0-9]*[0-9]", str(temp_record))[0]

    out_data = "Datum: " + date + "\n"
    out_data += "Čas: " + time + "\n"
    out_data += "Teplota vody: " + temp + " °C" + "\n"

    with open('chmu_teplota_vody.json', 'w') as out_file:
        out_file.write(out_data)

if __name__ == "__main__":
    main()
