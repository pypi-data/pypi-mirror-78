#Data : 2019-6-26
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : AttributeSet node interface for MDL. It would show the attributes or properties of the model, including category and brief introduction.

from abc import ABC, abstractclassmethod

class Category(object):
    def __init__(self, principle = '', path = ''):
        self._principle = principle
        self._path = path

    def getPrinciple(self):
        return self._principle

    def getPath(self):
        return self._path

    def clone(self):
        return Category(self.getPrinciple(), self.getPath())

class LocalAttribute(object):
    def __init__(self, local = '', localName = '', wiki = '', keywords = [], abstract = ''):
        self._local = local
        self._localName = localName
        self._wiki = wiki
        self._keywords = keywords
        self._abstract = abstract

    def getLocal(self):
        return self._local

    def getLocalName(self):
        return self._localName

    def getWiki(self):
        return self._wiki

    def getKeywords(self):
        return self._keywords

    def getAbstract(self):
        return self._abstract

    def clone(self):
        return LocalAttribute(self.getLocal(), self.getLocalName(), self.getWiki(), self.getKeywords(), self.getAbstract())

class IAttributeSet(ABC):
    @abstractclassmethod
    def getLocalAttributeCount(self) -> int:
        """ 
        """
    
    @abstractclassmethod
    def getLocalAttribute(self, local: str, index: int) -> LocalAttribute:
        """ 
        """

    @abstractclassmethod
    def addLocalAttributeInfo(self, localAttr: LocalAttribute) -> bool:
        """ 
        """

    @abstractclassmethod
    def removeLocalAttribute(self, local: str, index: int) -> bool:
        """ 
        """

    @abstractclassmethod
    def updateLocalAttribute(self, localAttr: LocalAttribute) -> int:
        """ 
        """

    @abstractclassmethod
    def getCategoryCount(self) -> int:
        """ 
        """

    @abstractclassmethod
    def getCategory(self, index: int) -> Category:
        """ 
        """

    @abstractclassmethod
    def addCategoryInfo(self, category: Category) -> bool:
        """ 
        """
        
    @abstractclassmethod
    def removeCategory(self, index: int) -> bool:
        """ 
        """
        
    @abstractclassmethod
    def updateCategory(self, category: Category) -> bool:
        """ 
        """
    