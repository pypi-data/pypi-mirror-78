#Data : 2019-7-12
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Model Description Language Interface.

from .IModelClass import IModelClass
from .AttributeSet import AttributeSet
from .Behavior import Behavior
from .Runtime import Runtime
import xml.etree.ElementTree as ET
import os
import random

class ModelClass(IModelClass):
    def __init__(self, name: str = '', uid: str = '', style: str = ''):
        self._name = name
        self._uid = uid
        self._style = style
        self._attr = AttributeSet()
        self._behavior = Behavior()
        self._runtime = Runtime()

    def getName(self):
        return self._name
        
    def setName(self, name:str):
        self._name = name
        return True
        
    def getUID(self):
        return self._uid
        
    def setUID(self, uid:str):
        self._uid = uid
        return True
        
    def getExecutionStyle(self):
        return self._style
        
    def setExecutionStyle(self, style:str):
        self._style = style
        return True
        
    def getModelAttribute(self):
        return self._attr
        
    def getBehavior(self):
        return self._behavior
        
    def getRuntime(self):
        return self._runtime

    def formatToXML(self):
        root = ET.Element('ModelClass')
        root.set('name', self._name)
        root.set('uid', self._uid)
        root.set('type', self._style)

        attributesSet = self._attr.formatToXML()
        root.append(attributesSet)
        
        behavior = self._behavior.formatToXML()
        root.append(behavior)
        
        runtime = self._runtime.formatToXML()
        root.append(runtime)

        tree = ET.ElementTree(root)
        return tree


    def formatToXMLFile(self, path:str):
        tree = self.formatToXML()
        tree.write(path, xml_declaration = True, encoding = 'UTF-8')
        return True

    def formatToXMLStream(self):
        tree = self.formatToXML()
        tmp_file = os.getcwd() + '/tmp_' + str(random.sample('zyxwvutsrqponmlkjihgfedcba',5)) + '.xml'
        tree.write(tmp_file, xml_declaration = True, encoding = 'UTF-8')
        f = open(tmp_file, 'r')
        stream = f.read()
        f.close()
        os.remove(tmp_file)
        return stream

    def LoadFromXmlFile(self, path:str):
        treeroot = ET.parse(path)
        root = treeroot.getroot()
        attrset = root.find('AttributeSet')
        self._attr.parseXML(attrset)

        behavior = root.find('Behavior')
        self._behavior.parseXML(behavior)

        runtime = root.find('Runtime')
        self._runtime.parseXML(runtime)

        return True

    def LoadFromXMLStream(self, stream:str):
        tmp_file = os.getcwd() + '/tmp_' + str(random.sample('zyxwvutsrqponmlkjihgfedcba',5)) + '.xml'
        f = open(tmp_file, 'w')
        f.write(stream)
        f.close()
        self.LoadFromXmlFile(tmp_file)
        os.remove(tmp_file)

        return True