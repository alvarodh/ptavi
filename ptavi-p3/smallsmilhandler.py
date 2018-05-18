#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler


class SmallSMILHandler(ContentHandler):

    def __init__(self):

        self.list = []
        self.att = {'root-layout': ['width', 'height', 'background-color'],
                    'region': ['id', 'top', 'bottom', 'left', 'right'],
                    'img': ['src', 'region', 'begin', 'dur'],
                    'audio': ['src', 'begin', 'dur'],
                    'textstream': ['src', 'region']}

    def startElement(self, name, attrs):

        dicc = {}
        if name in self.att:
            for att in self.att[name]:
                dicc[att] = attrs.get(att, '')
            self.list.append([name, dicc])

    def get_tags(self):

        return self.list

if __name__ == '__main__':

    parser = make_parser()
    cHandler = SmallSMILHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open('karaoke.smil'))
    print(cHandler.get_tags())
