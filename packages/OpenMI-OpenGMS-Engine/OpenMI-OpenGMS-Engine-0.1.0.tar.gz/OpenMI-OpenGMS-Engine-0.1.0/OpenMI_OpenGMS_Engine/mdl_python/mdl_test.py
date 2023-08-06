from IAttributeSet import Category, LocalAttribute
from IBehavior import ModelDatasetItem, ModelEvent, ModelParameter, ModelState, ModelStateTransition
from IRuntime import RequriementConfig, SoftwareConfig
from ModelClass import ModelClass

model = ModelClass('Test', '7bdfea5d-ff63-43f3-a016-49f04d796e74', 'SimpleCalculation')

attr = model.getModelAttribute()

localAttr_CN = LocalAttribute('CN', '测试模型', 'http://www.opengms.com.cn', ['模型', '测试'], 'Test test test Test test test Test test test Test test test')
localAttr_EN = LocalAttribute('EN', 'TestModel', 'http://www.opengms.com.cn', ['Model', 'Test'], 'Test test test Test test test Test test test Test test test')

localAttr_EN2 = LocalAttribute('EN', 'TestModel', 'http://www.opengms.com.cn', ['Model', 'Test', 'Simulation'], 'Test test test Test test test Test test test Test test test')

attr.addLocalAttributeInfo(localAttr_CN)
attr.addLocalAttributeInfo(localAttr_EN)

localAttr_EN3 = attr.getLocalAttribute('EN')

attr.updateLocalAttribute(localAttr_EN2)

localAttr_EN3 = attr.getLocalAttribute('EN')

cate1 = Category('Earth', 'AAA-BBB')
cate2 = Category('GEO', 'CCC-DDD')
cate3 = Category('ISO', 'EEE-FFF')
attr.addCategoryInfo(cate1)
attr.addCategoryInfo(cate2)
attr.addCategoryInfo(cate3)


cate4 = attr.getCategory(0)

attr.removeCategory(0)

behavior = model.getBehavior()

rasrer_tmp = ModelDatasetItem('Rasrer', 'external', 'Rasrer data template', 'F73F31FF-2F23-4C7A-A57D-39D0C7A6C4E6')
behavior.addModelDatasetItem(rasrer_tmp)

state1 = ModelState('3a397593-94f3-4565-aac4-f2c454db9c60', 'RUNNINGSTATE', 'basic', 'Running for test')
event_input = ModelEvent('DEM', 'response', 'Load DEM', 'rasrer_tmp', 'Rester', False)
event_output = ModelEvent('D8', 'noresponse', 'Ouput D8', 'rasrer_tmp', 'Rester', False)
state1.events.append(event_input)
state1.events.append(event_output)

behavior.addModelState(state1)

runtime = model.getRuntime()

# runtime.setName('TestName')
runtime.setVersion('1.2.0.0')
runtime.setBaseDirectory('$(ModelServicePath)\\')
runtime.setEntry('Test.exe')

runtime.addHardwareRequirement(RequriementConfig('Main Frequency', '2.8'))
runtime.addHardwareRequirement(RequriementConfig('Memory Size', '1024MB'))

runtime.addSoftwareRequirement(SoftwareConfig('Operation Platform', 'Windows', 'x64'))
runtime.addSoftwareRequirement(SoftwareConfig('Language Platform', 'C# 2010', 'x64'))

runtime.addModelAssembly(RequriementConfig('GDALRasterMapping.exe', '$(DataMappingPath)\\GDALRasterMapping\\'))

runtime.addSupportiveResource(RequriementConfig('library', 'GDAL'))

model.formatToXMLFile('test.mdl')

model2 = ModelClass()
model2.LoadFromXmlFile('test.mdl')

model2.formatToXMLFile('test2.mdl')

stream = model2.formatToXMLStream()

model3 = ModelClass()
model3.LoadFromXMLStream(stream)

print('finished!')
