#Data : 2019-7-12
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Runtime node class for MDL. It would show the dependencies and runnning information of the model.

from .IRuntime import RequriementConfig, SoftwareConfig, IRuntime
import xml.etree.ElementTree as ET

class Runtime(IRuntime):
    def __init__(self):
        # self._name = ''
        self._version = ''
        self._entry = ''
        self._baseDir = ''
        self._hardware = []
        self._software = []
        self._assembly = []
        self._support = []

    # def getName(self):
    #     return self._name

    # def setName(self, name:str):
    #     self._name = name
    #     return True
        
    def getVersion(self):
        return self._version
        
    def setVersion(self, version:str):
        self._version = version
        return True
        
    def getEntry(self):
        return self._entry
        
    def setEntry(self, entry:str):
        self._entry = entry
        return True
        
    def getBaseDirectory(self:str):
        return self._baseDir
        
    def setBaseDirectory(self, baseDir:str):
        self._baseDir = baseDir
        return True

    def addHardwareRequirement(self, hardware:RequriementConfig):
        for index,hw in enumerate(self._hardware):
            if hw.key == hardware.key:
                self._hardware[index] = hardware.clone()
                return False
        self._hardware.append(hardware.clone())
        return True

    def getHardwareRequirementCount(self):
        return len(self._hardware)

    def getHardwareRequirement(self, index:int):
        if index < len(self._hardware) and index > 0:
            return self._hardware[index]
        return None

    def removeHardwareRequirement(self, index:int):
        if index < len(self._hardware) and index > 0:
            self._hardware.remove(self._hardware[index])
            return True
        return False
        

    def addSoftwareRequirement(self, software:SoftwareConfig):
        for index,sw in enumerate(self._software):
            if sw.key == software.key:
                self._software[index] = software.clone()
                return False
        self._software.append(software.clone())
        return True

    def getSoftwareRequirementCount(self):
        return len(self._software)

    def getSoftwareRequirement(self, index:int):
        if index < len(self._software) and index > 0:
            return self._software[index]
        return None

    def removeSoftwareRequirement(self, index:int):
        if index < len(self._software) and index > 0:
            self._software.remove(self._software[index])
            return True
        return False



    def addModelAssembly(self, assembly:RequriementConfig):
        for index,ab in enumerate(self._assembly):
            if ab.key == assembly.key:
                self._assembly[index] = assembly.clone()
                return False
        self._assembly.append(assembly.clone())
        return True

    def getModelAssemblyCount(self):
        return len(self._assembly)

    def getModelAssembly(self, index:int):
        if index < len(self._assembly) and index > 0:
            return self._assembly[index]
        return None

    def removeModelAssembly(self, index:int):
        if index < len(self._assembly) and index > 0:
            self._assembly.remove(self._assembly[index])
            return True
        return False
        

    def addSupportiveResource(self, support:RequriementConfig) -> bool:
        for index,sp in enumerate(self._support):
            if sp.key == support.key:
                self._support[index] = support.clone()
                return False
        self._support.append(support.clone())
        return True

    def getSupportiveResourceCount(self):
        return len(self._support)

    def getSupportiveResource(self, index:int):
        if index < len(self._support) and index > 0:
            return self._support[index]
        return None

    def removeSupportiveResource(self, index:int):
        if index < len(self._support) and index > 0:
            self._support.remove(self._support[index])
            return True
        return False

    def formatToXML(self):
        runtime = ET.Element('Runtime')
        hardwareNode = ET.Element('HardwareConfigures')
        softwareNode = ET.Element('SoftwareConfigures')
        assembliesNode = ET.Element('Assemblies')
        sopportResNode = ET.Element('SupportiveResources')

        # runtime.set('name', self._name)
        runtime.set('version', self._version)
        runtime.set('baseDir', self._baseDir)
        runtime.set('entry', self._entry)

        for hw in self._hardware:
            hwNode = ET.Element('Add')
            hwNode.set('key', hw.key)
            hwNode.set('value', hw.value)
            hardwareNode.append(hwNode)

        for sw in self._software:
            swNode = ET.Element('Add')
            swNode.set('key', sw.key)
            swNode.set('value', sw.value)
            swNode.set('platform', sw.platform)
            softwareNode.append(swNode)

        for asm in self._assembly:
            asmNode = ET.Element('Add')
            asmNode.set('key', asm.key)
            asmNode.set('value', asm.value)
            assembliesNode.append(asmNode)

        for sp in self._support:
            spNode = ET.Element('Add')
            spNode.set('key', sp.key)
            spNode.set('value', sp.value)
            sopportResNode.append(spNode)

        runtime.append(hardwareNode)
        runtime.append(softwareNode)
        runtime.append(assembliesNode)
        runtime.append(sopportResNode)

        return runtime

    def parseXML(self, ele:ET.Element):
        # self.setName(ele.get('name'))
        self.setEntry(ele.get('entry'))
        self.setBaseDirectory(ele.get('baseDir'))
        self.setVersion(ele.get('version'))

        hardwareConfigs = ele.find('HardwareConfigures')
        hardwareConfig = hardwareConfigs.findall('Add')
        for hw in hardwareConfig:
            self.addHardwareRequirement(RequriementConfig(hw.get('key'), hw.get('value')))

        softwareConfigs = ele.find('SoftwareConfigures')

        for sw in softwareConfigs:
            self.addSoftwareRequirement(SoftwareConfig(sw.get('key'), sw.get('value'), sw.get('platform')))

        assembliesConfigs = ele.find('Assemblies')
        for asmb in assembliesConfigs:
            self.addModelAssembly(RequriementConfig(asmb.get('key'), asmb.get('value')))

        supportiveResConfigs = ele.find('SupportiveResources')
        for sr in supportiveResConfigs:
            self.addSupportiveResource(RequriementConfig(sr.get('key'), sr.get('value')))
