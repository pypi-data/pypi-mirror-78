#Data : 2019-7-12
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Model Description Language Interface.

from abc import ABC, abstractclassmethod
from .IAttributeSet import IAttributeSet
from .IBehavior import IBehavior
from .IRuntime import IRuntime

class IModelClass(ABC):
    @abstractclassmethod
    def getName(self) -> str:
        """
        """
        
    @abstractclassmethod
    def setName(self, name: str) -> bool:
        """
        """
        
    @abstractclassmethod
    def getUID(self) -> str:
        """
        """
        
    @abstractclassmethod
    def setUID(self, uid: str) -> bool:
        """
        """
        
    @abstractclassmethod
    def getExecutionStyle(self) -> str:
        """
        """
        
    @abstractclassmethod
    def setExecutionStyle(self, style: str) -> bool:
        """
        """
        
    @abstractclassmethod
    def getModelAttribute(self) -> IAttributeSet:
        """
        """
        
    @abstractclassmethod
    def getBehavior(self) -> IBehavior:
        """
        """
        
    @abstractclassmethod
    def getRuntime(self) -> IRuntime:
        """
        """
    

    @abstractclassmethod
    def formatToXMLFile(self, path:str) -> bool:
        """
        """

    @abstractclassmethod
    def formatToXMLStream(self) -> str:
        """
        """

    @abstractclassmethod
    def LoadFromXmlFile(self, path:str) -> bool:
        """
        """

    @abstractclassmethod
    def LoadFromXMLStream(self, stream:str) -> bool:
        """
        """