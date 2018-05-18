#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import urllib.request
from smallsmilhandler import SmallSMILHandler
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

tag_names = ('root-layout', 'region', 'img', 'audio', 'textstream')


class KaraokeLocal:

    def __init__(self, file_name):

        try:
            parser = make_parser()
            cHandler = SmallSMILHandler()
            parser.setContentHandler(cHandler)
            parser.parse(open(file_name))
            self.tags = cHandler.get_tags()
        except FileNotFoundError:
            sys.exit('File not found')

    def __str__(self):

        tag_line = ''
        for tag in self.tags:
            tag_line += tag[0]
            for element in tag[1]:
                if tag[1][element] != '':
                    tag_line += '\t' + element + '="' + tag[1][element] + '"'
            tag_line += '\n'
        return tag_line

    def to_json(self, filesmil, filejson=''):

        if filejson == '':
            filejson = filesmil.replace('.smil', '.json')

        with open(filejson, 'w') as jsonfile:
            json.dump(self.tags, jsonfile, indent=3)

    def do_local(self):

        for tag in self.tags:
            for element in tag[1]:
                if element == 'src':
                    if tag[1][element].startswith('http'):
                        file_name = tag[1][element].split('/')[-1]
                        urllib.request.urlretrieve(tag[1][element], file_name)
                        tag[1][element] = file_name

if __name__ == '__main__':

    try:
        file_name = sys.argv[1]
    except IndexError:
        sys.exit('usage error: python3 karaoke.py file.smil')
    karaoke = KaraokeLocal(file_name)
    print(karaoke)
    karaoke.to_json(file_name)
    karaoke.do_local()
    karaoke.to_json(file_name, 'local.json')
    print(karaoke)
