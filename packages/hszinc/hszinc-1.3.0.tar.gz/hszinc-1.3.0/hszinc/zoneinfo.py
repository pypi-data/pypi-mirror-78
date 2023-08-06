#!/usr/bin/python
# -*- coding: utf-8 -*-
# Project Haystack timezone data
# (C) 2016 VRT Systems
#
# vim: set ts=4 sts=4 et tw=78 sw=4 si: 

import pytz
import datetime

from .version import LATEST_VER

# The official list of timezones as of 6th Jan 2016:
# Yes, that's *without* the usual country prefix.
HAYSTACK_TIMEZONES="""Abidjan
Accra
Adak
Addis_Ababa
Adelaide
Aden
Algiers
Almaty
Amman
Amsterdam
Anadyr
Anchorage
Andorra
Antananarivo
Antigua
Apia
Aqtau
Aqtobe
Araguaina
Ashgabat
Asmara
Asuncion
Athens
Atikokan
Auckland
Azores
Baghdad
Bahia
Bahia_Banderas
Bahrain
Baku
Bangkok
Barbados
Beirut
Belem
Belgrade
Belize
Berlin
Bermuda
Beulah
Bishkek
Bissau
Blanc-Sablon
Boa_Vista
Bogota
Boise
Brisbane
Broken_Hill
Brunei
Brussels
Bucharest
Budapest
Buenos_Aires
Cairo
Cambridge_Bay
Campo_Grande
Canary
Cancun
Cape_Verde
Caracas
Casablanca
Casey
Catamarca
Cayenne
Cayman
Center
Ceuta
Chagos
Chatham
Chicago
Chihuahua
Chisinau
Chita
Choibalsan
Christmas
Chuuk
Cocos
Colombo
Comoro
Copenhagen
Cordoba
Costa_Rica
Creston
Cuiaba
Curacao
Currie
Damascus
Danmarkshavn
Dar_es_Salaam
Darwin
Davis
Dawson
Dawson_Creek
Denver
Detroit
Dhaka
Dili
Djibouti
Dubai
Dublin
DumontDUrville
Dushanbe
Easter
Edmonton
Efate
Eirunepe
El_Aaiun
El_Salvador
Enderbury
Eucla
Fakaofo
Faroe
Fiji
Fortaleza
Funafuti
GMT
GMT+1
GMT+10
GMT+11
GMT+12
GMT+2
GMT+3
GMT+4
GMT+5
GMT+6
GMT+7
GMT+8
GMT+9
GMT-1
GMT-10
GMT-11
GMT-12
GMT-13
GMT-14
GMT-2
GMT-3
GMT-4
GMT-5
GMT-6
GMT-7
GMT-8
GMT-9
Galapagos
Gambier
Gaza
Gibraltar
Glace_Bay
Godthab
Goose_Bay
Grand_Turk
Guadalcanal
Guam
Guatemala
Guayaquil
Guyana
Halifax
Havana
Hebron
Helsinki
Hermosillo
Ho_Chi_Minh
Hobart
Hong_Kong
Honolulu
Hovd
Indianapolis
Inuvik
Iqaluit
Irkutsk
Istanbul
Jakarta
Jamaica
Jayapura
Jerusalem
Johannesburg
Jujuy
Juneau
Kabul
Kaliningrad
Kamchatka
Kampala
Karachi
Kathmandu
Kerguelen
Khandyga
Khartoum
Kiev
Kiritimati
Knox
Kolkata
Kosrae
Krasnoyarsk
Kuala_Lumpur
Kuching
Kuwait
Kwajalein
La_Paz
La_Rioja
Lagos
Lima
Lindeman
Lisbon
London
Lord_Howe
Los_Angeles
Louisville
Luxembourg
Macau
Maceio
Macquarie
Madeira
Madrid
Magadan
Mahe
Majuro
Makassar
Maldives
Malta
Managua
Manaus
Manila
Maputo
Marengo
Marquesas
Martinique
Matamoros
Mauritius
Mawson
Mayotte
Mazatlan
Melbourne
Mendoza
Menominee
Merida
Metlakatla
Mexico_City
Midway
Minsk
Miquelon
Mogadishu
Monaco
Moncton
Monrovia
Monterrey
Montevideo
Monticello
Montreal
Moscow
Muscat
Nairobi
Nassau
Nauru
Ndjamena
New_Salem
New_York
Nicosia
Nipigon
Niue
Nome
Norfolk
Noronha
Noumea
Novokuznetsk
Novosibirsk
Ojinaga
Omsk
Oral
Oslo
Pago_Pago
Palau
Palmer
Panama
Pangnirtung
Paramaribo
Paris
Perth
Petersburg
Phnom_Penh
Phoenix
Pitcairn
Pohnpei
Pontianak
Port-au-Prince
Port_Moresby
Port_of_Spain
Porto_Velho
Prague
Puerto_Rico
Pyongyang
Qatar
Qyzylorda
Rainy_River
Rangoon
Rankin_Inlet
Rarotonga
Recife
Regina
Rel
Resolute
Reunion
Reykjavik
Riga
Rio_Branco
Rio_Gallegos
Riyadh
Rome
Rothera
Saipan
Sakhalin
Salta
Samara
Samarkand
San_Juan
San_Luis
Santa_Isabel
Santarem
Santiago
Santo_Domingo
Sao_Paulo
Scoresbysund
Seoul
Shanghai
Simferopol
Singapore
Sitka
Sofia
South_Georgia
Srednekolymsk
St_Johns
Stanley
Stockholm
Swift_Current
Sydney
Syowa
Tahiti
Taipei
Tallinn
Tarawa
Tashkent
Tbilisi
Tegucigalpa
Tehran
Tell_City
Thimphu
Thule
Thunder_Bay
Tijuana
Tirane
Tokyo
Tongatapu
Toronto
Tripoli
Troll
Tucuman
Tunis
UCT
UTC
Ulaanbaatar
Urumqi
Ushuaia
Ust-Nera
Uzhgorod
Vancouver
Vevay
Vienna
Vientiane
Vilnius
Vincennes
Vladivostok
Volgograd
Vostok
Wake
Wallis
Warsaw
Whitehorse
Winamac
Windhoek
Winnipeg
Yakutat
Yakutsk
Yekaterinburg
Yellowknife
Yerevan
Zaporozhye
Zurich""".split('\n')
HAYSTACK_TIMEZONES_SET=set(HAYSTACK_TIMEZONES)

# Mapping of pytz-recognised timezones to Haystack timezones.
_TZ_MAP = None
_TZ_RMAP = None

def _map_timezones():
    """
    Map the official Haystack timezone list to those recognised by pytz.
    """
    tz_map = {}
    todo = HAYSTACK_TIMEZONES_SET.copy()
    for full_tz in pytz.all_timezones:
        # Finished case:
        if not bool(todo): # pragma: no cover
            # This is nearly impossible for us to cover, and an unlikely case.
            break

        # Case 1: exact match
        if full_tz in todo:
            tz_map[full_tz] = full_tz   # Exact match
            todo.discard(full_tz)
            continue

        # Case 2: suffix match after '/'
        if '/' not in full_tz:
            continue

        (prefix, suffix) = full_tz.split('/',1)
        # Case 2 exception: full timezone contains more than one '/' -> ignore
        if '/' in suffix:
            continue

        if suffix in todo:
            tz_map[suffix] = full_tz
            todo.discard(suffix)
            continue

    return tz_map

def _gen_map():
    global _TZ_MAP
    global _TZ_RMAP
    if (_TZ_MAP is None) or (_TZ_RMAP is None):
        _TZ_MAP = _map_timezones()
        _TZ_RMAP = dict([(z,n) for (n,z) in list(_TZ_MAP.items())])

def get_tz_map(version=LATEST_VER):
    """
    Return the timezone map, generating it if needed.
    """
    _gen_map()
    return _TZ_MAP

def get_tz_rmap(version=LATEST_VER):
    """
    Return the reverse timezone map, generating it if needed.
    """
    _gen_map()
    return _TZ_RMAP

def timezone(haystack_tz, version=LATEST_VER):
    """
    Retrieve the Haystack timezone
    """
    tz_map = get_tz_map(version=version)
    try:
        tz_name = tz_map[haystack_tz]
    except KeyError:
        raise ValueError('%s is not a recognised timezone on this host' \
                % haystack_tz)
    return pytz.timezone(tz_name)

def timezone_name(dt, version=LATEST_VER):
    """
    Determine an appropriate timezone for the given date/time object
    """
    tz_rmap = get_tz_rmap(version=version)
    if dt.tzinfo is None:
        raise ValueError('%r has no timezone' % dt)

    # Easy case: pytz timezone.
    try:
        tz_name = dt.tzinfo.zone
        return tz_rmap[tz_name]
    except KeyError:
        # Not in timezone map
        pass
    except AttributeError:
        # Not a pytz-compatible tzinfo
        pass

    # Hard case, try to find one that's equivalent.  Hopefully we don't get
    # many of these.  Start by getting the current timezone offset, and a
    # timezone-naïve copy of the timestamp.
    offset  = dt.utcoffset()
    dt_notz = dt.replace(tzinfo=None)

    if offset == datetime.timedelta(0):
        # UTC?
        return 'UTC'

    for olson_name, haystack_name in list(tz_rmap.items()):
        if pytz.timezone(olson_name).utcoffset(dt_notz) == offset:
            return haystack_name

    raise ValueError('Unable to get timezone of %r' % dt)
