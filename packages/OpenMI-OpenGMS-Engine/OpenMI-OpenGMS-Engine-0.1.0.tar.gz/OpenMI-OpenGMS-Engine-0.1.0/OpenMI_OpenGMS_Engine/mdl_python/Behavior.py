#Data : 2019-7-11
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Behavior node class for MDL. It would show the behaviors, including IO and data template, of the model.

from .IBehavior import ModelParameter, ModelState, ModelStateTransition, ModelDatasetItem, ModelEvent, IBehavior
import xml.etree.ElementTree as ET

class Behavior(IBehavior):
    def __init__(self):
        self._dataitems = []
        self._states = []
        self._stateTrans = []
        self._processParams = []
        self._controlParams = []

    def addModelDatasetItem(self, dataset:ModelDatasetItem):
        for index,ds in enumerate(self._dataitems):
            if ds.datasetName == dataset.datasetName:
                self._dataitems[index] = ds.clone()
                return False
        self._dataitems.append(dataset.clone())
        return True

    def removeModelDatasetItem(self, datasetName:str = None, index:int = None):
        if datasetName != None:
            for index,ds in enumerate(self._dataitems):
                if ds.datasetName == datasetName:
                    self._dataitems.remove(ds)
        if index < len(self._dataitems) and index > -1:
            return self._dataitems.remove(self._dataitems[index])
        
    def getModelDatasetItemCount(self):
        return len(self._dataitems)
        
    def getModelDatasetItem(self, datasetName:str = None, index:int = None):
        if datasetName != None:
            for index,ds in enumerate(self._dataitems):
                if ds.datasetName == datasetName:
                    return ds
        if index < len(self._dataitems) and index > -1:
            return self._dataitems[index]
        return None


    def updateModelDatasetItem(self, dataset:ModelDatasetItem):
        for index,ds in enumerate(self._dataitems):
            if ds.datasetName == dataset.dataName:
                self._dataitems[index] = dataset.clone()
                return True
        return False
        
    def addModelState(self, state:ModelState):
        for index,state in enumerate(self._states):
            if state.stateId == state.stateId:
                self._states[index] = state.clone()
                return False
        self._states.append(state.clone())
        return True
        
    def removeModelState(self, stateId:str = None, stateName:str = None, index:int = None):
        if stateId != None:
            for index,state in enumerate(self._states):
                if state.stateId == stateId:
                    self._states.remove(state)
                    return True
        if stateName != None:
            for index,state in enumerate(self._states):
                if state.stateName == stateName:
                    self._states.remove(state)
                    return True
        if index < len(self._dataitems) and index > -1:
            return self._states.remove(self._dataitems[index])
        
    def getModelStateCount(self):
        return len(self._states)
        
    def getModelState(self, stateId:str = None, stateName:str = None, index:int = None):
        if stateId != None:
            for index,state in enumerate(self._states):
                if state.stateId == stateId:
                    return state
        if stateName != None:
            for index,state in enumerate(self._states):
                if state.stateName == stateName:
                    return state
        if index < len(self._dataitems) and index > -1:
            return self._states[index]
        
    def updateModelState(self, state:ModelState):
        for index,stateItem in enumerate(self._states):
            if stateItem.stateId == state.stateId:
                self._states[index] = state.clone()
                return True
        return False
        
    def addModelStateTransition(self, transition:ModelStateTransition):
        for trans in enumerate(self._stateTrans):
            if trans.sfrom == transition.sfrom and trans.sto == transition.sto:
                return False
        self._stateTrans.append(transition.clone())
        
    def removeModelStateTransition(self, index:int):
        if index < len(self._stateTrans) and index > -1:
            self._stateTrans.remove(self._states[index])
            return True
        return False
        
    def getModelStateTransitionCount(self):
        return len(self._stateTrans)
        
    def getModelStateTransition(self, index:int):
        if index < len(self._stateTrans) and index > -1:
            return self._stateTrans[index]
        return None
        
    def addProcessParameter(self, parameter:ModelParameter):
        for index,pp in enumerate(self._processParams):
            if pp.key == parameter.key:
                self._processParams[index] = parameter.clone()
        self._processParams.append(parameter.clone())
        
    def getProcessParameterCount(self):
        return len(self._processParams)
        
    def getProcessParameter(self, index:int):
        if index < len(self._processParams) and index > -1:
            return self._processParams[index]
        return None
        
    def removeProcessParameter(self, index:int):
        if index < len(self._processParams) and index > -1:
            return self._processParams.remove(self._processParams[index])
        return None
        
    def addControlParameter(self, parameter:ModelParameter):
        for index,pp in enumerate(self._controlParams):
            if pp.key == parameter.key:
                self._controlParams[index] = parameter.clone()
        self._controlParams.append(parameter.clone())
        
    def getControlParameterCount(self):
        return len(self._controlParams)
        
    def getControlParameter(self, index:int):
        if index < len(self._controlParams) and index > -1:
            return self._controlParams[index]
        return None
        
    def removeControlParameter(self, index:int):
        if index < len(self._controlParams) and index > -1:
            return self._controlParams.remove(self._controlParams[index])
        return None
        
    def formatToXML(self):
        behavior = ET.Element('Behavior')
        relatedDs = ET.Element('RelatedDatasets')
        parameters = ET.Element('Parameters')
        stategroup = ET.Element('StateGroup')

        for ds in self._dataitems:
            dsNode = ET.Element('DatasetItem')
            dsNode.set('name', ds.datasetName)
            dsNode.set('type', ds.datasetType)
            dsNode.set('description', ds.datasetDes)
            if ds.datasetType == 'external':
                dsNode.set('externalId', ds.externalId)
            elif ds.datasetType == 'internal':
                dsNode.text = ds.UdxContent
            relatedDs.append(dsNode)

        processParams = ET.Element('ProcessParameters')
        controlParams = ET.Element('ControlParameters')

        for pp in self._processParams:
            ppNode = ET.Element('Add')
            ppNode.set('key', pp.key)
            ppNode.set('description', pp.description)
            ppNode.set('defaultValue', pp.defaultValue)
            processParams.append(ppNode)
            
        for cp in self._controlParams:
            cpNode = ET.Element('Add')
            cpNode.set('key', cp.key)
            cpNode.set('description', cp.description)
            cpNode.set('defaultValue', cp.defaultValue)
            processParams.append(cpNode)

        parameters.append(processParams)
        parameters.append(controlParams)

        states = ET.Element('States')
        statesTrans = ET.Element('StateTransitions')

        for state in self._states:
            stateNode = ET.Element('State')
            stateNode.set('id', state.stateId)
            stateNode.set('name', state.stateName)
            stateNode.set('type', state.stateType)
            stateNode.set('description', state.stateDes)

            for event in state.events:
                eventNode = ET.Element('Event')
                eventNode.set('name', event.eventName)
                eventNode.set('type', event.eventType)
                eventNode.set('optional', str(event.optional))
                eventNode.set('description', event.eventDescription)
                parameterNode = None
                if event.eventType == 'response':
                    parameterNode = ET.Element('ResponseParameter')
                else:
                    parameterNode = ET.Element('DispatchParameter')
                parameterNode.set('datasetReference', event.dataRef)
                parameterNode.set('description', event.parameterDes)
                eventNode.append(parameterNode)
                stateNode.append(eventNode)
            states.append(stateNode)

        for trans in self._stateTrans:
            transNode = ET.Element('Add')
            transNode.set('from', trans.sfrom)
            transNode.set('to', trans.sto)
            statesTrans.append(transNode)

        stategroup.append(states)
        stategroup.append(statesTrans)

        behavior.append(relatedDs)
        behavior.append(parameters)
        behavior.append(stategroup)

        return behavior

    def parseXML(self, ele:ET.Element):
        relatedDsNodes = ele.find('RelatedDatasets')
        dsItemNode = relatedDsNodes.findall('DatasetItem')
        for ds in dsItemNode:
            name = ds.get('name')
            dstype = ds.get('type')
            description = ds.get('description')
            eid = ds.get('externalId')
            udxcontent = ds.text
            self.addModelDatasetItem(ModelDatasetItem(name, dstype, description, eid, udxcontent))
        
        pNodes = ele.find('Parameters')
        ppNodes = pNodes.find('ProcessParameters')
        ppNode = ppNodes.find('Add')
        cpNodes = pNodes.find('ControlParameters')
        cpNode = cpNodes.find('Add')

        if ppNode != None:
            for pp in ppNode:
                self.addProcessParameter(ModelParameter(pp.get('key'), pp.get('description'), pp.get('defaultValue')))

        if cpNode != None:
            for cp in cpNode:
                self.addControlParameter(ModelParameter(cp.get('key'), cp.get('description'), cp.get('defaultValue')))

        stateGroupNode = ele.find('StateGroup')
        stateNodes = stateGroupNode.find('States')
        stateNode = stateNodes.findall('State')

        for state in stateNode:
            stat = ModelState(state.get('id'), state.get('name'), state.get('type'), state.get('description'), [])
            events = state.findall('Event')
            for event in events:
                if event.get('type') == 'response':
                    eventParam = event.find('ResponseParameter')
                else:
                    eventParam = event.find('DispatchParameter')
                evt = ModelEvent(event.get('name'), event.get('type'), event.get('description'), eventParam.get('datasetReference'), eventParam.get('description'), bool(event.get('optional')))
                stat.events.append(evt)
            self.addModelState(stat)

        statesTransNodes = stateGroupNode.find('StateTransitions')
        statesTransNode = statesTransNodes.find('Add')
        
        if statesTransNode != None:
            for trans in statesTransNode:
                self.addModelStateTransition(ModelStateTransition(trans.get('from'), trans.get('to')))
