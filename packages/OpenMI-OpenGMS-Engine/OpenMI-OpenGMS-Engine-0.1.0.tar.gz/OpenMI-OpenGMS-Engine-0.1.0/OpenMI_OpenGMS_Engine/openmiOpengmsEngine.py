#Data : 2020-8-7
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : this engine aims to convert OpenGMS service to OpenMI component

import sys
import numpy as np
import json
import os
import uuid
import random
import shutil
import OGMSService
import shutil
from xml.dom.minidom import Document, parse

from .mdl_python import ModelClass, Category, LocalAttribute, ModelDatasetItem, ModelEvent, ModelParameter, ModelState, ModelStateTransition, RequriementConfig, SoftwareConfig

class OpenMIOpenGMSEngine():
    @staticmethod
    def convertOpenGMS2OpenMI(ip: str, port: int, serviceid: str, dataconfigs: object, output: str, supplement: str = None):
        
        if not os.path.exists(output):
            os.mkdir(output)

        dir_resource = os.path.dirname(__file__) + "/resource/"
        shutil.copy(dir_resource + "Newtonsoft.Json.dll", output + "Newtonsoft.Json.dll")
        shutil.copy(dir_resource + "NJModelServiceSDK.dll", output + "NJModelServiceSDK.dll")
        shutil.copy(dir_resource + "nxdat.csharp.dll", output + "nxdat.csharp.dll")
        shutil.copy(dir_resource + "nxmodel.mdl.csharp.dll", output + "nxmodel.mdl.csharp.dll")
        shutil.copy(dir_resource + "Oatc.OpenMI.Sdk.Backbone.dll", output + "Oatc.OpenMI.Sdk.Backbone.dll")
        shutil.copy(dir_resource + "Oatc.OpenMI.Sdk.Buffer.dll", output + "Oatc.OpenMI.Sdk.Buffer.dll")
        shutil.copy(dir_resource + "Oatc.OpenMI.Sdk.DevelopmentSupport.dll", output + "Oatc.OpenMI.Sdk.DevelopmentSupport.dll")
        shutil.copy(dir_resource + "Oatc.OpenMI.Sdk.Spatial.dll", output + "Oatc.OpenMI.Sdk.Spatial.dll")
        shutil.copy(dir_resource + "Oatc.OpenMI.Sdk.Wrapper.dll", output + "Oatc.OpenMI.Sdk.Wrapper.dll")
        shutil.copy(dir_resource + "OpenGMS.OpenMI.Case.dll", output + "OpenGMS.OpenMI.Case.dll")
        shutil.copy(dir_resource + "OpenMI.Standard.dll", output + "OpenMI.Standard.dll")
        
        server = OGMSService.OGMSService.CreateServer(ip, port)
        access = server.getServiceAccess()
        service = access.getModelServiceByID(serviceid)
        name = service.name

        # start write OMI file
        doc = Document()
        component = doc.createElement('LinkableComponent')
        component.setAttribute("Type", "OpenGMS.OpenMI.Case.OGMSModelLC")
        component.setAttribute("Assembly", output + "OpenGMS.OpenMI.Case.dll")
        
        args = doc.createElement("Arguments")
        
        tag_ip = doc.createElement("Argument")
        tag_ip.setAttribute("Key", "IP")
        tag_ip.setAttribute("ReadOnly", "true")
        tag_ip.setAttribute("Value", ip)
        args.appendChild(tag_ip)
        
        tag_port = doc.createElement("Argument")
        tag_port.setAttribute("Key", "Port")
        tag_port.setAttribute("ReadOnly", "true")
        tag_port.setAttribute("Value", str(port))
        args.appendChild(tag_port)
        
        tag_service = doc.createElement("Argument")
        tag_service.setAttribute("Key", "Service")
        tag_service.setAttribute("ReadOnly", "true")
        tag_service.setAttribute("Value", serviceid)
        args.appendChild(tag_service)

        for dc in dataconfigs:
            tag_dc = doc.createElement("Argument")
            tag_dc.setAttribute("Key", dc.state + dc.event)
            tag_dc.setAttribute("ReadOnly", "true")
            tag_dc.setAttribute("Value", dc.data)
            args.appendChild(tag_dc)

        component.appendChild(args)
        doc.appendChild(component)

        omifilename = output + name + ".omi"
        f = open(omifilename, 'w')
        doc.writexml(f, newl = "\n")
        f.close()

    @staticmethod
    def convertOpenMI2OpenGMS(omifile: str, appended: object, dataio: list, outputpackage: str):
        doc = parse(omifile)
        eleComponent = doc.getElementsByTagName("LinkableComponent")[0]
        assembly = eleComponent.getAttribute("Assembly")
        asstype = eleComponent.getAttribute("Type")
        eleArgs = eleComponent.getElementsByTagName("Arguments")[0]
        eleArgList = eleArgs.getElementsByTagName("Argument")

        for index in range(len(dataio)):
            dataio[index] = str(dataio[index])

        cfg = os.path.dirname(__file__) + "/data.cfg" 
        if os.path.exists(cfg):
            os.remove(cfg)
        f = open(cfg, "w")
        f.write("# Mark the input/output of OpenMI component\n")
        f.write("dataIO " + " ".join(dataio) + "\n\n")
        f.write("# Mark the appended files for th component\n")
        f.write("appendedDLL " + assembly + "\n")
        for item in appended:
            f.write("appended " + item + "\n")
        f.close()

        cmd = os.path.dirname(__file__) + "/resource/OpenMIOpenGMSWrapper.exe 1 " + omifile + " " + cfg + " " + outputpackage
        os.system(cmd)
        
