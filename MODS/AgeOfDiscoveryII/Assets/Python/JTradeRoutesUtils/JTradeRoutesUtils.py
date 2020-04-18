# JWeather Mod
# By: Jeckel
#

from CvPythonExtensions import *
import CvScreensInterface
import CvUtil

import CvAlertManager

###################################################
# globals
gc = CyGlobalContext()
oLocalText = CyTranslator()

oEngine = CyEngine()
oGame = CyGame()
oMap = CyMap()

alert = CvAlertManager.CvAlertManager()

dSQUARE = {"NORTH": (0, 1), "SOUTH": (0, -1),
           "EAST": (1, 0), "WEST": (-1, 0),
           "NORTHEAST": (1, 1), "NORTHWEST": (-1, 1),
           "SOUTHEAST": (1, -1), "SOUTHWEST": (-1, -1)}
tDIRECTIONS = ("NORTH", "NORTHEAST", "EAST", "SOUTHEAST", "SOUTH", "SOUTHWEST", "WEST", "NORTHWEST")
###################################################

class JTradeRoutesUtils:
        dSQUARE = dSQUARE
        tDIRECTIONS = tDIRECTIONS
        iButtonExit = 10000
        iButtonBack = 10001
        iButtonCreateTradeRouteID = 10002
        iButtonEditTradeRouteID = 10003
        iButtonDeleteTradeRouteID = 10004
        iButtonAssignToTradeRouteID = 10005
        iButtonAssignToLandUnitID = 10006
        iButtonAssignToSeaUnitID = 10007
        iTableTradeRoutes = 10100
        iTableTransports = 10101
        iTableCommoditiesTotalYield = 10102
        iTableCommodities = 10103
        iTableCommoditiesTotalCity = 10104
        EventDeleteTradeRoute = 10200
        EventAssignTradeRoute = 10201
        EventAssignUnitsToTradeRoute = 10202
	def __init__(self):
                pass

	def getText(self, sText, tArgs = (), iColor = -2):
                if (type(sText) != str) and (type(sText) != unicode):
                        sText = str(sText)
                try:
                        sText = oLocalText.getText(sText, tArgs)
                except:
                        pass
                if (iColor == -2):
                        iColor = gc.getInfoTypeForString("COLOR_FONT_CREAM")
                sText = oLocalText.changeTextColor(sText, iColor)
                return sText

        def getTradeRouteName(self, pTradeRoute):
		sText = pTradeRoute.getName()
		if (sText == ""):
                        tArgs = (gc.getYieldInfo(pTradeRoute.getYield()).getDescription(),
                                 pTradeRoute.getSourceCityName(),
                                 pTradeRoute.getDestinationCityName())
                        sText = self.getText("TXT_KEY_TRADE_ROUTE_DESCRIPTION", tArgs, -1)
                #sText = pTradeRoute.getDisplayName()
                return sText

	def getTradeRouteTransports(self, iPlayer, iTradeRoute):
                pPlayer = gc.getPlayer(iPlayer)
                pTradeRoute = pPlayer.getTradeRoute(iTradeRoute)
		lUnits = self.getPlayerUnits(iPlayer)
		lTransports = []
		for pUnit in lUnits:
                        if (not pUnit.getGroup().isAssignedTradeRoute(iTradeRoute)):
                                continue
                        lTransports += [pUnit]
		return lTransports

	def getPlayerUnits(self, iPlayer):
                pPlayer = gc.getPlayer(iPlayer)
		lUnits = []
		(pLoopUnit, iter) = pPlayer.firstUnit()
		while(pLoopUnit):
			if (not pLoopUnit.isDead()):
				lUnits += [pLoopUnit]
			(pLoopUnit, iter) = pPlayer.nextUnit(iter)
		return lUnits

	def getPlayerCities(self, iPlayer):
                pPlayer = gc.getPlayer(iPlayer)
		lCities = []
		(pLoopCity, iter) = pPlayer.firstCity(False)
		while(pLoopCity):
			if (not pLoopCity.isNone()):
				lCities += [pLoopCity]
			(pLoopCity, iter) = pPlayer.nextCity(iter, False)
		return lCities

	def getPlayerTradeRoutes(self, iPlayer):
                pPlayer = gc.getPlayer(iPlayer)
		lTradeRoutes = []
		for iTradeRoute in range(pPlayer.getNumTradeRoutes()):
                        pTradeRoute = pPlayer.getTradeRouteByIndex(iTradeRoute)
                        lTradeRoutes += [pTradeRoute]
		return lTradeRoutes

	def getUnitCurrentMoves(self, pUnit):
		iDenominator = 0
                if ((pUnit.movesLeft() % gc.getMOVE_DENOMINATOR()) > 0):
			iDenominator = 1
		return ((pUnit.movesLeft() / gc.getMOVE_DENOMINATOR()) + iDenominator)

	def getUnitCurrentStrength(self, pUnit):
                if (pUnit.isHurt()):
			return (float(pUnit.baseCombatStr() * pUnit.currHitPoints()) / float(pUnit.maxHitPoints()))
		return float(pUnit.baseCombatStr())

	def getUnitCargo(self, pUnit):
                pPlot = pUnit.plot()
                lUnits = []
                for iUnitID in range(pPlot.getNumUnits()):
                        pPlotUnit = pUnit.plot().getUnit(iUnitID)
                        if (pPlotUnit.getTransportUnit().getOwner() == pUnit.getOwner()) \
                           and (pPlotUnit.getTransportUnit().getID() == pUnit.getID()):
                                lUnits += [pPlotUnit]
                return lUnits

        def getUnitUsedCapacity(self, pUnit):
                lCargoUnits = self.getUnitCargo(pUnit)
                iTotal = 0
                for pCargoUnit in lCargoUnits:
                        iYield = pCargoUnit.getYield()
                        if (iYield < 0):
                                continue
                        iStored = pCargoUnit.getYieldStored()
                        if (iStored < 1):
                                continue
                        iTotal += iStored
                return iTotal

	def getTurnDate(self, iTurn):
		iYear = oGame.getTurnYear(iTurn)
		if (iYear < 0):
			sText = oLocalText.getText("TXT_KEY_TIME_BC", (-iYear,))
		else:
			sText = oLocalText.getText("TXT_KEY_TIME_AD", (iYear,))
		return sText

        #############################################################################################################

        def createTradeRouteBegin(self, iPlayer, iScreenW, iScreenH, tUserData = ("", -1)):
                pPlayer = gc.getPlayer(iPlayer)
		popup = CyPopup(CvUtil.EventCreateTradeRoute, EventContextTypes.EVENTCONTEXT_ALL, 1)
		iW = 400
		iH = 500
		popup.setSize(iW, iH)
		iX = iScreenW - iW - 30
		iY = 40
		popup.setPosition(iX, iY)
		popup.setUserData(tUserData)
		popup.setHeaderString(self.getText("TXT_KEY_CREATE_TRADE_ROUTE"), CvUtil.FONT_LEFT_JUSTIFY)

                popup.addSeparator()
		popup.setBodyString(self.getText("TXT_KEY_YIELD"), CvUtil.FONT_LEFT_JUSTIFY)
		popup.createPullDown(2)
		popup.addPullDownString(self.getText("TXT_KEY_NO_YIELD", iColor = -1), -1, 2)
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if (gc.getYieldInfo(iYield).isCargo()):
				popup.addPullDownString(gc.getYieldInfo(iYield).getDescription(), iYield, 2)

                popup.addSeparator()
		popup.setBodyString(self.getText("TXT_KEY_SOURCE"), CvUtil.FONT_LEFT_JUSTIFY)
		popup.createPullDown(0)
		popup.addPullDownString(self.getText("TXT_KEY_NO_SOURCE", iColor = -1), -1, 0)
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
                        pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if (pLoopPlayer.isAlive()) and (pPlayer.canLoadYield(iLoopPlayer)):
                                lCities = self.getPlayerCities(iLoopPlayer)
                                for pCity in lCities:
					iID = gc.getMAX_PLAYERS() * pCity.getID() + pCity.getOwner()
					popup.addPullDownString(pCity.getName(), iID, 0)

                popup.addSeparator()
		popup.setBodyString(self.getText("TXT_KEY_POPUP_TRADE_ROUTE_SOURCE_MAINTAIN"), CvUtil.FONT_LEFT_JUSTIFY)
		sText = ""
		popup.createEditBox(sText, 0)
		popup.setEditBoxMaxCharCount(3, 3, 0)

                popup.addSeparator()
		popup.setBodyString(self.getText("TXT_KEY_DESTINATION"), CvUtil.FONT_LEFT_JUSTIFY)
		popup.createPullDown(1)
		popup.addPullDownString(self.getText("TXT_KEY_NO_DESTINATION", iColor = -1), -2, 1)
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if (pLoopPlayer.isAlive()) and (pPlayer.canUnloadYield(iLoopPlayer)):
                                lCities = self.getPlayerCities(iLoopPlayer)
                                for pCity in lCities:
					iID = gc.getMAX_PLAYERS() * pCity.getID() + pCity.getOwner()
					popup.addPullDownString(pCity.getName(), iID, 1)

		if (pPlayer.canTradeWithEurope()):
			popup.addPullDownString(self.getText("TXT_KEY_CONCEPT_EUROPE", iColor = -1), -1, 1)

		popup.addSeparator()
		popup.setBodyString(self.getText("TXT_KEY_POPUP_TRADE_ROUTE_NAME"), CvUtil.FONT_LEFT_JUSTIFY)
		sText = ""
		popup.createEditBox(sText, 1)
		popup.setEditBoxMaxCharCount(300, 30, 1)

		"""popup.addSeparator()
		popup.setBodyString(self.getText("Priority (Optional)"), CvUtil.FONT_LEFT_JUSTIFY)
		sText = ""
		popup.createEditBox(sText, 2)
		popup.setEditBoxMaxCharCount(6, 3, 2)"""

		popup.addSeparator()
		popup.addSeparator()
		popup.addButton(self.getText("TXT_KEY_POPUP_CANCEL", iColor = -1))

		popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)
		return None

	def createTradeRouteApply(self, iPlayer, tUserData, pPopupReturn):
                #alert.debug(0, "createTradeRouteApply", tUserData)
                iButton = pPopupReturn.getButtonClicked()
                if (iButton == 0):
                        return None
                iSourceCity = pPopupReturn.getSelectedPullDownValue(0) / gc.getMAX_PLAYERS()
                if (iSourceCity == -1):
                        return None
                iSourcePlayer = pPopupReturn.getSelectedPullDownValue(0) % gc.getMAX_PLAYERS()
                if (iSourcePlayer == -1):
                        return None
                iDestinationCity = pPopupReturn.getSelectedPullDownValue(1) / gc.getMAX_PLAYERS()
                if (iDestinationCity == -2):
                        return None
                iDestinationPlayer = pPopupReturn.getSelectedPullDownValue(1) % gc.getMAX_PLAYERS()
                if (iDestinationPlayer == -1):
                        return None
                iYieldType = pPopupReturn.getSelectedPullDownValue(2)
                if (iYieldType == -1):
                        return None
		pPlayer = gc.getPlayer(iPlayer)
                iKept = 0
                sKept = pPopupReturn.getEditBoxString(0)
                if (sKept != ""):
                        try:
                                iKept = int(sKept)
                        except:
                                pass
                if (iKept > 0):
                        pCity = pPlayer.getCity(iSourceCity)
                        pCity.doTask(TaskTypes.TASK_YIELD_LEVEL, iYieldType, iKept, False)
                screen = None
                if (len(tUserData) > 0) and (iPlayer == oGame.getActivePlayer()):
                        if (type(tUserData[0]) == str) and (len(tUserData[0]) > 0) \
                           and (type(tUserData[1]) == int) and (tUserData[1] > -1):
                                screen = CyGInterfaceScreen(tUserData[0], tUserData[1])
                                if (screen.isActive()):
                                        screen.hideScreen()
		iTradeRoute = pPlayer.addTradeRoute(iSourcePlayer, iSourceCity,
                                                    iDestinationPlayer, iDestinationCity,
                                                    iYieldType)
		pTradeRoute = pPlayer.getTradeRoute(iTradeRoute)
		sName = pPopupReturn.getEditBoxString(1)
		if (sName != ""):
                        pTradeRoute.setName(sName)
                """sPriority = pPopupReturn.getEditBoxString(2)
                try:
                        iPriority = int(sPriority)
                except:
                        iPriority = 0
                if (iPriority != pTradeRoute.getPriority()):
                        pTradeRoute.setPriority(iPriority)"""

                if (iPlayer == oGame.getActivePlayer()):
                        CvScreensInterface.showTradeRoutesScreen()
                return None

        #############################################################################################################

        def editTradeRouteBegin(self, iPlayer, iTradeRoute, iScreenW, iScreenH, tUserData = ("", -1)):
                if (iPlayer < 0) or (iTradeRoute < 0):
                        return None
                pPlayer = gc.getPlayer(iPlayer)
                pTradeRoute = pPlayer.getTradeRoute(iTradeRoute)
                tUserData = (tUserData[0], tUserData[1], iTradeRoute)

		popup = CyPopup(CvUtil.EventEditTradeRoute, EventContextTypes.EVENTCONTEXT_ALL, 1)
		iW = 400
		iH = 500
		popup.setSize(iW, iH)
		iX = iScreenW - iW - 30
		iY = 40
		popup.setPosition(iX, iY)
		popup.setUserData(tUserData)
		popup.setHeaderString(oLocalText.getText("TXT_KEY_EDIT_TRADE_ROUTE", ()), CvUtil.FONT_LEFT_JUSTIFY)

                popup.addSeparator()
		popup.setBodyString(self.getText("TXT_KEY_YIELD"), CvUtil.FONT_LEFT_JUSTIFY)
		popup.createPullDown(2)
		popup.addPullDownString(self.getText("TXT_KEY_NO_YIELD", (), -1), -1, 2)
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if (gc.getYieldInfo(iYield).isCargo()):
				popup.addPullDownString(gc.getYieldInfo(iYield).getDescription(), iYield, 2)
		popup.setSelectedPulldownID(pTradeRoute.getYield(), 2)

                popup.addSeparator()
		popup.setBodyString(self.getText("TXT_KEY_SOURCE"), CvUtil.FONT_LEFT_JUSTIFY)
		popup.createPullDown(0)
		#popup.addPullDownString(self.getText("TXT_KEY_NO_SOURCE", (), -1), -1, 0)
		iSelected = -1
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if (pLoopPlayer.isAlive()) and (pPlayer.canLoadYield(iLoopPlayer)):
                                lCities = self.getPlayerCities(iLoopPlayer)
                                for pCity in lCities:
					iID = gc.getMAX_PLAYERS() * pCity.getID() + pCity.getOwner()
					popup.addPullDownString(pCity.getName(), iID, 0)
					if (pTradeRoute.getSourceCity().iID == pCity.getID()) \
                                           and (pTradeRoute.getSourceCity().eOwner == pCity.getOwner()):
						popup.setSelectedPulldownID(iID, 0)

                popup.addSeparator()
		popup.setBodyString(self.getText("TXT_KEY_POPUP_TRADE_ROUTE_SOURCE_MAINTAIN"), CvUtil.FONT_LEFT_JUSTIFY)
                sText = "%d" %(gc.getPlayer(pTradeRoute.getSourceCity().eOwner).getCity(pTradeRoute.getSourceCity().iID).getMaintainLevel(pTradeRoute.getYield()))
		popup.createEditBox(sText, 0)
		popup.setEditBoxMaxCharCount(3, 3, 0)

                popup.addSeparator()
		popup.setBodyString(self.getText("TXT_KEY_DESTINATION"), CvUtil.FONT_LEFT_JUSTIFY)
		popup.createPullDown(1)
		#popup.addPullDownString(self.getText("TXT_KEY_NO_DESTINATION", (), -1), -1, 1)
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if (pLoopPlayer.isAlive()) and (pPlayer.canUnloadYield(iLoopPlayer)):
                                lCities = self.getPlayerCities(iLoopPlayer)
                                for pCity in lCities:
					iID = gc.getMAX_PLAYERS() * pCity.getID() + pCity.getOwner()
					popup.addPullDownString(pCity.getName(), iID, 1)
					if (pTradeRoute.getDestinationCity().iID == pCity.getID()) \
                                           and (pTradeRoute.getDestinationCity().eOwner == pCity.getOwner()):
						popup.setSelectedPulldownID(iID, 1)

		if pPlayer.canTradeWithEurope():
			popup.addPullDownString(self.getText("TXT_KEY_CONCEPT_EUROPE", (), -1), -1, 1)
                        if (pTradeRoute.getDestinationCity().iID == -1) \
                           and (pTradeRoute.getDestinationCity().eOwner == iPlayer):
                                popup.setSelectedPulldownID(-1, 1)

		popup.addSeparator()
		popup.setBodyString(self.getText("TXT_KEY_POPUP_TRADE_ROUTE_NAME"), CvUtil.FONT_LEFT_JUSTIFY)
		sText = pTradeRoute.getName()
		popup.createEditBox(sText, 1)
		popup.setEditBoxMaxCharCount(80, 30, 1)

		"""popup.addSeparator()
		popup.setBodyString(self.getText("Priority (Optional)"), CvUtil.FONT_LEFT_JUSTIFY)
		sText = str(pTradeRoute.getPriority())
		popup.createEditBox(sText, 2)
		popup.setEditBoxMaxCharCount(6, 3, 2)"""

		popup.addSeparator()
		popup.addSeparator()
		popup.addButton(self.getText("TXT_KEY_POPUP_CANCEL", iColor = -1))

		popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)
		return None

        def editTradeRouteApply(self, iPlayer, tUserData, pPopupReturn):
                iButton = pPopupReturn.getButtonClicked()
                if (iButton == 0):
                        return None
                iSourceCity = pPopupReturn.getSelectedPullDownValue(0) / gc.getMAX_PLAYERS()
                iSourcePlayer = pPopupReturn.getSelectedPullDownValue(0) % gc.getMAX_PLAYERS()

                iDestinationCity = pPopupReturn.getSelectedPullDownValue(1) / gc.getMAX_PLAYERS()
                iDestinationPlayer = pPopupReturn.getSelectedPullDownValue(1) % gc.getMAX_PLAYERS()

                iYieldType = pPopupReturn.getSelectedPullDownValue(2)

                iKept = 0
                sKept = pPopupReturn.getEditBoxString(0)
                if (sKept != ""):
                        try:
                                iKept = int(sKept)
                        except:
                                pass
                if (iKept > -1) and (iKept != gc.getPlayer(iSourcePlayer).getCity(iSourceCity).getMaintainLevel(iYieldType)):
                        gc.getPlayer(iSourcePlayer).getCity(iSourceCity).doTask(TaskTypes.TASK_YIELD_LEVEL, iYieldType, iKept, False)

                sNameNew = pPopupReturn.getEditBoxString(1)

                """sPriorityNew = pPopupReturn.getEditBoxString(2)
                try:
                        iPriorityNew = int(sPriorityNew)
                except:
                        iPriorityNew = 0"""

                screen = None
                if (len(tUserData) > 0):
                        if (type(tUserData[0]) == str) and (len(tUserData[0]) > 0) \
                           and (type(tUserData[1]) == int) and (tUserData[1] > -1) \
                           and (type(tUserData[2]) == int) and (tUserData[2] > -1):
                                screen = CyGInterfaceScreen(tUserData[0], tUserData[1])
                                if (screen.isActive()) and (iPlayer == oGame.getActivePlayer()):
                                        screen.hideScreen()
                                pPlayer = gc.getPlayer(iPlayer)
                                #pPlayer.removeTradeRoute(tUserData[2])
                                pPlayer.editTradeRoute(tUserData[2],
                                                       iSourcePlayer, iSourceCity,
                                                       iDestinationPlayer, iDestinationCity,
                                                       iYieldType)
                                pTradeRoute = pPlayer.getTradeRoute(tUserData[2])
                                if (sNameNew != pTradeRoute.getName()):
                                        pTradeRoute.setName(sNameNew)
                                """if (iPriorityNew != pTradeRoute.getPriority()):
                                        pTradeRoute.setPriority(iPriorityNew)"""

                                if (iPlayer == oGame.getActivePlayer()):
                                        CvScreensInterface.showTradeRoutesScreen()
		return None

        #############################################################################################################

        def deleteTradeRouteBegin(self, iPlayer, iTradeRoute, iScreenW, iScreenH, tUserData = ("", -1)):
                if (iPlayer < 0) or (iTradeRoute < 0):
                        return None
                pPlayer = gc.getPlayer(iPlayer)
                pTradeRoute = pPlayer.getTradeRoute(iTradeRoute)
                tUserData = (tUserData[0], tUserData[1], iTradeRoute)

		popup = CyPopup(self.EventDeleteTradeRoute, EventContextTypes.EVENTCONTEXT_ALL, 1)
		iW = 400
		iH = 300
		popup.setSize(iW, iH)
		iX = iScreenW - iW - 30
		iY = 40
		popup.setPosition(iX, iY)
		popup.setUserData(tUserData)
		popup.setHeaderString(self.getText("TXT_KEY_DELETE_TRADE_ROUTE"), CvUtil.FONT_LEFT_JUSTIFY)

                popup.addSeparator()
		sText = gc.getYieldInfo(pTradeRoute.getYield()).getDescription()
                sText = self.getText("TXT_KEY_YIELD") + self.getText(":  ") + self.getText(sText)
		popup.setBodyString(sText, CvUtil.FONT_LEFT_JUSTIFY)

                popup.addSeparator()
		sText = pTradeRoute.getSourceCityName()
                sText = self.getText("TXT_KEY_SOURCE") + self.getText(":  ") + self.getText(sText)
                sText += self.getText(" (")
                sText += self.getText("TXT_KEY_POPUP_KEEP")
                sTempText = ": %d)" %(gc.getPlayer(pTradeRoute.getSourceCity().eOwner).getCity(pTradeRoute.getSourceCity().iID).getMaintainLevel(pTradeRoute.getYield()))
                sText += self.getText(sTempText)
		popup.setBodyString(sText, CvUtil.FONT_LEFT_JUSTIFY)

                popup.addSeparator()
		sText = pTradeRoute.getDestinationCityName()
                sText = self.getText("TXT_KEY_DESTINATION") + self.getText(":  ") + self.getText(sText)
		popup.setBodyString(sText, CvUtil.FONT_LEFT_JUSTIFY)

		popup.addSeparator()
		sText = self.getTradeRouteName(pTradeRoute)
                sText = self.getText("TXT_KEY_POPUP_NAME") + self.getText(":  ") + self.getText(sText)
		popup.setBodyString(sText, CvUtil.FONT_LEFT_JUSTIFY)

		"""popup.addSeparator()
		sText = str(pTradeRoute.getPriority())
                sText = self.getText("Priority") + self.getText(":  ") + self.getText(sText)
		popup.setBodyString(sText, CvUtil.FONT_LEFT_JUSTIFY)"""

		popup.addSeparator()
		popup.addSeparator()
		popup.addButton(self.getText("TXT_KEY_POPUP_CANCEL", iColor = -1))

		popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)
		return None

        def deleteTradeRouteApply(self, iPlayer, tUserData, pPopupReturn):
                #for s in dir(pPopupReturn):
                #        alert.alert(0, s)
                iButton = pPopupReturn.getButtonClicked()
                if (iButton == 0):
                        return None
                #screen = None
                #alert.debug(0, "deleteTradeRouteApply", tUserData)
                if (len(tUserData) > 0):
                        if (type(tUserData[0]) == str) and (len(tUserData[0]) > 0) \
                           and (type(tUserData[1]) == int) and (tUserData[1] > -1) \
                           and (type(tUserData[2]) == int) and (tUserData[2] > -1):
                                screen = CyGInterfaceScreen(tUserData[0], tUserData[1])
                                if (screen.isActive()) and (iPlayer == oGame.getActivePlayer()):
                                        screen.hideScreen()
                                pPlayer = gc.getPlayer(iPlayer)
                                pPlayer.removeTradeRoute(tUserData[2])

                                if (iPlayer == oGame.getActivePlayer()):
                                        CvScreensInterface.showTradeRoutesScreen()
		return None

        #############################################################################################################

g_oUtils = JTradeRoutesUtils()















