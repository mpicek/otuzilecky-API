# Otužilecký API
API pro otužilce u Malše v Českých Budějovicích u schůdků v 7:15 ráno. Hodně specifická aplikace.

Nejdříve je třeba si zařídit na [openweathermap.org](openweathermap.org) účet a získat klíč k API. Tento klíč uložte v tomto repozitáři do souboru, který pojmenujte `owm.key`. Tím máme funkční připojení k získávání předpovědi počasí. Aktuální stav vody je pak scrapován z webu [chmi.cz](http://hydro.chmi.cz/hpps/popup_hpps_prfdyn.php?seq=307046).

Pro získání informace o počasí, spusťe `run_scraper.sh`. Můžete jej spouštět jednou za určitou dobu pomocí linuxové utility Cron. Tutoriál např. [zde](https://linuxhint.com/schedule_crontab_job_every_hour/). Informace o nejbližším dalším zánoru je pak v souboru `chmu_teplota_vody.json` (nenechte se zmást, není to .json soubor, jen jsem línej to předělat).

Aplikace je spuštěna na webu mýho kámoše na [bramborak.kulych.cz](http://bramborak.kulych.cz/). Díky kámo, že to pro mě děláš, vážím si toho, že plejtváš svý resources takovoudle naprostou kravinou.

Zánoru zdar!
