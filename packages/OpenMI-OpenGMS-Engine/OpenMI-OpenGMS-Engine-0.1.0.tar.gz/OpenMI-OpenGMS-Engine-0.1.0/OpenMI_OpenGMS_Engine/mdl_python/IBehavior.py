#Data : 2019-7-10
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Behavior node interface for MDL. It would show the behaviors, including IO and data template, of the model.

from abc import ABC, abstractclassmethod

class ModelParameter(object):
    def __init__(self, key = '', description = '', defaultValue = ''):
        self.key = key
        self.description = description
        self.defaultValue = defaultValue
    
    def clone(self):
        return ModelParameter(self.key, self.description, self.defaultValue)

class ModelDatasetItem(object):
    def __init__(self, datasetName = '', datasetType = '', datasetDes = '', externalId = None, UdxContent = None):
        self.datasetName = datasetName
        self.datasetType = datasetType
        self.datasetDes = datasetDes
        self.externalId = externalId
        self.UdxContent = UdxContent
    
    def clone(self):
        return ModelDatasetItem(self.datasetName, self.datasetType, self.datasetDes, self.externalId, self.UdxContent)

class ModelEvent(object):
    def __init__(self, eventName = '', eventType = '', eventDescription = '', dataRef = '', parameterDes = '', optional = True):
        self.eventName = eventName
        self.eventType = eventType
        self.eventDescription = eventDescription
        self.dataRef = dataRef
        self.parameterDes = parameterDes
        self.optional = optional

    def clone(self):
        return ModelEvent(self.eventName, self.eventType, self.eventDescription, self.dataRef, self.parameterDes, self.optional)

class ModelState(object):
    def __init__(self, stateId = '', stateName = '', stateType = '', stateDes = '', events = []):
        self.stateId = stateId
        self.stateName = stateName
        self.stateType = stateType
        self.stateDes = stateDes
        self.events = events

    def clone(self):
        return ModelState(self.stateId, self.stateName, self.stateType, self.stateDes, self.events)

class ModelStateTransition(object):
    def __init__(self, sfrom = '', sto = ''):
        self.sfrom = ''
        self.sto = ''

    def clone(self):
        return ModelStateTransition(self.sfrom, self.sto)

class IBehavior(ABC):
    @abstractclassmethod
    def addModelDatasetItem(self, dataset: ModelDatasetItem) -> bool:
        """
        """

    @abstractclassmethod
    def removeModelDatasetItem(self, datasetName: str, index: int) -> bool:
        """
        """
        
    @abstractclassmethod
    def getModelDatasetItemCount(self) -> int:
        """
        """
        
    @abstractclassmethod
    def getModelDatasetItem(self, datasetName: str, index: int) -> ModelDatasetItem:
        """
        """

    def updateModelDatasetItem(self, dataset: ModelDatasetItem) -> bool:
        """
        """
        
    @abstractclassmethod
    def addModelState(self, state: ModelState) -> bool:
        """
        """
        
    @abstractclassmethod
    def removeModelState(self, stateId: str, stateName: str, index: int) -> bool:
        """
        """
        
    @abstractclassmethod
    def getModelStateCount(self) -> int:
        """
        """
        
    @abstractclassmethod
    def getModelState(self, stateId: str, stateName: str, index: int) -> ModelState:
        """
        """
        
    @abstractclassmethod
    def updateModelState(self, state: ModelState) -> bool:
        """
        """
        
    @abstractclassmethod
    def addModelStateTransition(self, transition: ModelStateTransition) -> bool:
        """
        """
        
    @abstractclassmethod
    def removeModelStateTransition(self, index: int) -> bool:
        """
        """
        
    @abstractclassmethod
    def getModelStateTransitionCount(self) -> int:
        """
        """
        
    @abstractclassmethod
    def getModelStateTransition(self, index: int) -> ModelStateTransition:
        """
        """
        
    @abstractclassmethod
    def addProcessParameter(self, parameter: ModelParameter) -> bool:
        """
        """
        
    @abstractclassmethod
    def getProcessParameterCount(self) -> int:
        """
        """
        
    @abstractclassmethod
    def getProcessParameter(self, index: int) -> ModelParameter:
        """
        """
        
    @abstractclassmethod
    def removeProcessParameter(self, index: int) -> bool:
        """
        """
        
    @abstractclassmethod
    def addControlParameter(self, parameter: ModelParameter) -> bool:
        """
        """
        
    @abstractclassmethod
    def getControlParameterCount(self) -> int:
        """
        """
        
    @abstractclassmethod
    def getControlParameter(self, index: int) -> ModelParameter:
        """
        """
        
    @abstractclassmethod
    def removeControlParameter(self, index: int) -> bool:
        """
        """
        