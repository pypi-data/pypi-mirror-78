# -*- coding: utf-8 -*-
from lxml import etree
import csv


class Modifier(object):
    def __init__(self, target):
        self._target = target

    @property
    def target(self):
        return self._target

    def modify(self):
        pass


class Standoff(Modifier):
    TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
    TEI = "{%s}" % TEI_NAMESPACE
    XML_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
    XML = "{%s}" % XML_NAMESPACE
    NSMAP = {None: TEI_NAMESPACE, "xml": XML_NAMESPACE}

    def __init__(self, target):
        self.namespaces = {"tei": "http://www.tei-c.org/ns/1.0",
                           "xml": "http://www.w3.org/XML/1998/namespace"}
        super().__init__(target)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, filename):
        with open(filename) as file:
            reader = csv.DictReader(file, dialect="excel-tab")
            self._data = []
            for row in reader:
                self._data.append(row.copy())

    def modify(self):
        for row in self.data:
            expr = f"//*[@xml:id = \"{row['id']}\"]"
            place = self.target.tei_doc.xpath(expr)[0]
            placeName = place.xpath('tei:placeName',
                                    namespaces=self.namespaces)
            if len(placeName):
                placeName[0].text = row['placeName']
            else:
                placeName = etree.element(self.TEI + "placeName",
                                          nsmap=self.NSMAP)
                placeName.text = row['placeName']
                place.append(placeName)

            if row['coordinate location']:
                location = etree.SubElement(place, self.TEI + "location",
                                            nsmap=self.NSMAP)
                geo = etree.SubElement(location, self.TEI + "geo",
                                       nsmap=self.NSMAP)
                # TODO: remove comma in the geo text
                geo.text = row['coordinate location'].replace(',', ' ')

            if row['QID']:
                idno = etree.SubElement(place, self.TEI + "idno",
                                        nsmap=self.NSMAP)
                idno.set("type", "WD")
                idno.text = row['QID']
