#Data : 2019-7-11
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Runtime node interface for MDL. It would show the dependencies and runnning information of the model.

from abc import ABC,abstractclassmethod

class RequriementConfig(object):
    def __init__(self, key = '', value = ''):
        self.key = key
        self.value = value

    def clone(self):
        return RequriementConfig(self.key, self.value)

class SoftwareConfig(RequriementConfig):
    def __init__(self, key = '', value = '', platform = ''):
        self.key = key
        self.value = value
        self.platform = platform

    def clone(self):
        return SoftwareConfig(self.key, self.value, self.platform)

class IRuntime(ABC):
    # @abstractclassmethod
    # def getName(self) -> str:
    #     """
    #     """
    
    # @abstractclassmethod
    # def setName(self, name: str) -> bool:
    #     """
    #     """
        
    @abstractclassmethod
    def getVersion(self) -> str:
        """
        """
        
    @abstractclassmethod
    def setVersion(self, version: str) -> bool:
        """
        """
        
    @abstractclassmethod
    def getEntry(self) -> str:
        """
        """
        
    @abstractclassmethod
    def setEntry(self, entry: str) -> bool:
        """
        """
        
    @abstractclassmethod
    def getBaseDirectory(self) -> str:
        """
        """
        
    @abstractclassmethod
    def setBaseDirectory(self, baseDir: str) -> bool:
        """
        """

    @abstractclassmethod
    def addHardwareRequirement(self, hardware: RequriementConfig) -> bool:
        """
        """

    @abstractclassmethod
    def getHardwareRequirementCount(self) -> int:
        """
        """

    @abstractclassmethod
    def getHardwareRequirement(self, index: int) -> RequriementConfig:
        """
        """

    @abstractclassmethod
    def removeHardwareRequirement(self, index: int) -> bool:
        """
        """
        

    @abstractclassmethod
    def addSoftwareRequirement(self, hardware: SoftwareConfig) -> bool:
        """
        """

    @abstractclassmethod
    def getSoftwareRequirementCount(self) -> int:
        """
        """

    @abstractclassmethod
    def getSoftwareRequirement(self, index: int) -> SoftwareConfig:
        """
        """

    @abstractclassmethod
    def removeSoftwareRequirement(self, index: int) -> bool:
        """
        """



    @abstractclassmethod
    def addModelAssembly(self, hardware: RequriementConfig) -> bool:
        """
        """

    @abstractclassmethod
    def getModelAssemblyCount(self) -> int:
        """
        """

    @abstractclassmethod
    def getModelAssembly(self, index: int) -> RequriementConfig:
        """
        """

    @abstractclassmethod
    def removeModelAssembly(self, index: int) -> bool:
        """
        """
        

    @abstractclassmethod
    def addSupportiveResource(self, hardware: RequriementConfig) -> bool:
        """
        """

    @abstractclassmethod
    def getSupportiveResourceCount(self) -> int:
        """
        """

    @abstractclassmethod
    def getSupportiveResource(self, index: int) -> RequriementConfig:
        """
        """

    @abstractclassmethod
    def removeSupportiveResource(self, index: int) -> bool:
        """
        """