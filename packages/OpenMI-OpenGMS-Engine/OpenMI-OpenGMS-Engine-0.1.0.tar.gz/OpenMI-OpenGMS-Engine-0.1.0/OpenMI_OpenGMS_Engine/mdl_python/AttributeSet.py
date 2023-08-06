#Data : 2019-7-10
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : AttributeSet node class for MDL. It would show the attributes or properties of the model, including category and brief introduction.

from .IAttributeSet import Category, IAttributeSet, LocalAttribute
import xml.etree.ElementTree as ET

class AttributeSet(IAttributeSet):
    def __init__(self):
        self._categories = []
        self._attributes = []

    def getLocalAttributeCount(self):
        return len(self._attributes)
    
    def getLocalAttribute(self, local:LocalAttribute = None, index:int = None):
        if local != None:
            for la in self._attributes:
                if la.getLocal() == local:
                    return la
        elif index != None:
            if index < len(self._attributes) and index > -1:
                return self._attributes[index]
        return None

    def addLocalAttributeInfo(self, localAttr:LocalAttribute):
        if self.getLocalAttribute(localAttr.getLocal()) == None:
            self._attributes.append(localAttr.clone())
            return True
        else:
            self.updateLocalAttribute(localAttr)
            return False

    def removeLocalAttribute(self, local:str = None, index:int = None):
        if local != None:
            for la in self._attributes:
                if la.getLocal() == local:
                    self._attributes.remove(la)
                    return True
        elif index != None:
            if index > -1 and index < len(self._attributes):
                self._attributes.remove(self._attributes[index])
                return True
        return False

    def updateLocalAttribute(self, localAttr:LocalAttribute):
        for index,la in enumerate(self._attributes):
            if la.getLocal() == localAttr.getLocal():
                self._attributes[index] = localAttr.clone()
                return True
        return False

    def getCategoryCount(self):
        return len(self._categories)

    def getCategory(self, index:int):
        if index < len(self._categories) and index > -1:
            return self._categories[index]
        return None

    def addCategoryInfo(self, category:Category):
        for cate in self._categories:
            if cate.getPrinciple() == category.getPrinciple():
                self.updateCategory(cate)
                return False
        self._categories.append(category.clone())
        
    def removeCategory(self, index:int):
        if index < len(self._categories) and index > -1:
            self._categories.remove(self._categories[index])
        
    def updateCategory(self, category:Category):
        for cate in self._categories:
            if cate.getPrinciple() == category.getPrinciple():
                cate = category.clone()
                return True
        return False

    def formatToXML(self):
        attributesSet = ET.Element('AttributeSet')
        categories = ET.Element('Categories')
        localAttributes = ET.Element('LocalAttributes')

        for cate in self._categories:
            cateNode = ET.Element('Category')
            cateNode.set('principle', cate.getPrinciple())
            cateNode.set('path', cate.getPath())
            categories.append(cateNode)

        for local in self._attributes:
            localNote = ET.Element('LocalAttribute')
            keywordsNode = ET.Element('Keywords')
            abstractNode = ET.Element('Abstract')
            keywordsNode.text = ','.join(local.getKeywords())
            abstractNode.text = local.getAbstract()
            localNote.set('local', local.getLocal())
            localNote.set('localName', local.getLocalName())
            localNote.set('wiki', local.getWiki())
            localNote.append(keywordsNode)
            localNote.append(abstractNode)
            localAttributes.append(localNote)

        attributesSet.append(categories)
        attributesSet.append(localAttributes)

        return attributesSet

    def parseXML(self, ele: ET.Element):
        categories = ele.find('Categories')
        cates = categories.findall('Category')
        for cate in cates:
            path = cate.get('path')
            principle = cate.get('principle')
            self.addCategoryInfo(Category(principle, path))

        localAttrs = ele.find('LocalAttributes')
        localAttr = localAttrs.findall('LocalAttribute')
        for attr in localAttr:
            local = attr.get('local')
            localName = attr.get('localName')
            wiki = attr.get('wiki')
            keywords = attr.find('Keywords').text.split(',')
            abstract = attr.find('Abstract').text
            self.addLocalAttributeInfo(LocalAttribute(local, localName, wiki, keywords, abstract))