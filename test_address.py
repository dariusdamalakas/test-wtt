#!/usr/bin/python
# vim: set fileencoding=utf-8 :

import urllib
import string
import fileinput
import sys
import csv

def get_address_page(address):
    url = 'http://parasykjiems.lt/pjweb/'
    params = urllib.urlencode({'address_input': address})
    return urllib.urlopen(url, params).read()


def get_page_stats(address, html):
    
    result = [address]
    if html.find('id="address_table"') >=0:
        if html.find("Nerasta joki") >= 0:
            result = result + [1, 0, 0, 0, 0]
            return result
            
        indexFrom = html.find('Rasti apygardų adresai')
        slice = html[indexFrom:]
        numStreets = slice.count("<tr>")
        result = result + [numStreets, 0, 0, 0, 0]
        return result
       
    patterns = ['>Seimo narys <', '>Meras <', '>Seniūnas <', '>Seniūnaitis <']
        
    result.append("1")
    for pat in patterns:
        result.append(string.count(html, pat))
    return result


# main:

adr = 'Gedimino pr. 9, Vilnius'

writer = csv.writer(sys.stdout)

writer.writerow( ['Adresas', 'Surasta gatvių', 'Seimo narys', 'Meras', 'Seniūnas', 'Seniūnaitis'] )

for adr in fileinput.input():
    adr = adr.strip()
    writer.writerow( get_page_stats(adr, get_address_page(adr)) )
