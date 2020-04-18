## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
## 
## CvEventManager
## This class is passed an argsList from CvAppInterface.onEvent
## The argsList can contain anything from mouse location to key info
## The EVENTLIST that are being notified can be found


from CvPythonExtensions import *
#import Popup as PyPopup
import CvScreensInterface
import CvScreenEnums
import CvUtil

import CvAlertManager
import JTradeRoutesUtils

###################################################
# globals
gc = CyGlobalContext()
oLocalText = CyTranslator()

oGame = gc.getGame()
oMap = CyMap()

alert = CvAlertManager.CvAlertManager()

utils = JTradeRoutesUtils.g_oUtils
###################################################

class JTradeRoutesEventManager:
	def __init__(self, eventManager):
		self.EventKeyDown=6
		self.eventManager = eventManager

		#eventManager.addEventHandler("ModNetMessage", self.onModNetMessage)
		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)
		#eventManager.addEventHandler("improvementBuilt", self.onImprovementBuilt)
		#eventManager.addEventHandler("improvementDestroyed", self.onImprovementDestroyed)
		#eventManager.addEventHandler("routeBuilt", self.onRouteBuilt)

		self.eventManager.Events[CvUtil.EventCreateTradeRoute] = ("CreateTradeRoute",
                                                                          utils.createTradeRouteApply,
                                                                          utils.createTradeRouteBegin)
		self.eventManager.Events[CvUtil.EventEditTradeRoute] = ("EditTradeRoute",
                                                                          utils.editTradeRouteApply,
                                                                          utils.editTradeRouteBegin)
		self.eventManager.Events[utils.EventDeleteTradeRoute] = ("DeleteTradeRoute",
                                                                          utils.deleteTradeRouteApply,
                                                                          utils.deleteTradeRouteBegin)

	################################################################################################
		
	# This method handles the key input and will bring up the
	# Tile Naming Popup if the player presses the 'ALT + N' key
	def onKbdEvent(self, argsList):
		'keypress handler - return 1 if the event was consumed'
		eventType,key,mx,my,px,py = argsList
			
		theKey=int(key)

		pPlotCursor = CyMap().plot(px, py)

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()

		if (eventType == self.EventKeyDown):
                        iPlayer = gc.getGame().getActivePlayer()
                        pPlayer = gc.getPlayer(iPlayer)
                        if (theKey == InputTypes.KB_T) \
                           and (self.eventManager.bAlt) \
                           and (not self.eventManager.bCtrl) \
                           and (not self.eventManager.bShift):
                                pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
                                #CvScreensInterface.showTradeRoutesPopup(pHeadSelectedUnit)
                                CvScreensInterface.showTradeRoutesScreen(iTab = 0)
                                #self.__eventCreateTradeRouteBegin(pHeadSelectedUnit.getOwner())
                                #self.__eventEditTradeRouteBegin(pHeadSelectedUnit.getOwner(), 0)
                        elif (theKey == InputTypes.KB_R) \
                           and (not self.eventManager.bAlt) \
                           and (not self.eventManager.bCtrl) \
                           and (self.eventManager.bShift):
                                #alert.alert(0, "======================================")
                                #sText = gc.getPlayer(0).getTradeRoute(0).getDisplayName()
                                #alert.debug(0, "getDisplayName", sText)
                                #alert.alert(0, "end")
                                #for iTurn in range(oGame.getGameTurn()):
                                        #alert.debug(0, "getStoredYieldHistory(iTurn, iYield)",
                                        #            gc.getActivePlayer().getStoredYieldHistory(iTurn, iYield))
                                        #pass
                                pass
                return 0

	################################################################################################

























