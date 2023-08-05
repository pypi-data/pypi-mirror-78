import json
import RPi.GPIO as GPIO
from .traintrackingservice import TrackingService
from .models.CommandResultModel import CommandResultModel
from .models.GPIORelaisModel import GPIORelaisModel
from .models.GPIORelaisModel import GPIOStoppingPoint
from .models.GPIORelaisModel import GPIOSwitchPoint
from .databaseControllerModule import DatabaseController

gpioRelais = []
trackingServices = []

# Inital Loading and Setup

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    setupTrackingDefault()

def loadInitialData():
    switchModels = DatabaseController().getAllSwichtModels()
    for model in switchModels:
        gpioRelais.append(model)
    stopModels = DatabaseController().getAllStopModels()
    for stop in stopModels:
        gpioRelais.append(stop)
    setAllToDefault()

def setupTrackingDefault():
    for relais in gpioRelais:
        if isinstance(relais, GPIOStoppingPoint) and relais.measurmentpin is not None:
            startTrackingFor(relais)            
        
def startTrackingFor(relais):
    trackingService = TrackingService(relais)
    trackingServices.append(trackingService)
    trackingService.startTracking()

def resetData():
    DatabaseController().removeAll()
    del gpioRelais [:]
    del trackingServices [:]

def createSwitch(id, default, switchType):
    switch = GPIOSwitchPoint(id, switchType, id)
    switch.setDefaultValue(default)
    switch.toDefault()
    DatabaseController().insertSwitchModel(switch)
    gpioRelais.append(switch)
    return id

def createStop(id, measurmentid):
    stop = GPIOStoppingPoint(id, id, measurmentid)
    DatabaseController().insertStopModel(id, measurmentid)
    gpioRelais.append(stop)
    return id

def getValueForPin(pin, id, commandType):
    pinValue = GPIO.input(pin)
    return json.dumps(CommandResultModel(commandType, id, str(pinValue)).__dict__)

def getRelaisWithID(id): 
    return next((relais for relais in gpioRelais if relais.id == id), None)


# Relais Actions

def switchPin(relais):        
    if relais.getStatus():
        if isinstance(relais, GPIOStoppingPoint):
            trackingService = next((tracker for tracker in trackingServices if tracker.stoppingPoint.id == relais.id), None)
            if trackingService :
                trackingService.stopTracking()
                trackingServices.remove(trackingService)
        return relais.setStatus(GPIO.LOW)
    else:
        if isinstance(relais, GPIOStoppingPoint) and relais.measurmentpin is not None:
            startTrackingFor(relais)        
        return relais.setStatus(GPIO.HIGH)

def receivedMessage(message):
    if is_json(message):
        jsonData = json.loads(message) 
        results = "["
        if "CONFIG" in jsonData[0]["commandType"]:
            resetData()
        for commandData in jsonData:
            results = results +  performCommand(commandData) + ","

        results = results[:-1] + "]"
        return results
    # Insert more here
    else:
        return "msg:Not valid json"

def performCommand(command):
    commandType = command["commandType"]
    if commandType == "SET_SWITCH" or commandType == "SET_STOPPING_POINT":
        relais = getRelaisWithID(int(command["id"]))
        if relais is not None:
            return json.dumps(CommandResultModel(commandType, command["id"], switchPin(relais)).__dict__)
        else:
            return "{ \"error\":\"Relais not found\"}"
    elif commandType == "GET_SWITCH" or commandType == "GET_STOPPING_POINT":
        return getValueForPin(int(command["id"]), command["id"], commandType)
    elif commandType == "CONFIG_SWITCH":
        params = command["params"]
        resultId = createSwitch(int(command["id"]), int(command["defaultValue"]), params["switchType"])
        return json.dumps(CommandResultModel(commandType, resultId, "success").__dict__)
    elif commandType == "CONFIG_STOPPING_POINT":
        if 'measurmentId' in command:
            resultId = createStop(int(command["id"]), int(command["measurmentId"]))
        else:
            resultId = createStop(int(command["id"]), None)
        return json.dumps(CommandResultModel(commandType, resultId, "success").__dict__)
    elif commandType == "PERFORM_GIT_UPDATE":
        return json.dumps(CommandResultModel(commandType, 0, 'success').__dict__)
    else:
        return "{ \"error\":\"Command not supported\"}"

def setAllToDefault():
    for relais in gpioRelais:
        print(relais)
        relais.toDefault()

# Validation

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError:
    return False
  return True