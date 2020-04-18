#
# Civilization 4: Colonization
# JTradeRoutes Mod
# by Jeckel
# 
# 

from CvPythonExtensions import *
import CvScreensInterface
import CvScreenEnums
import CvUtil

import CvAlertManager
import JTradeRoutesUtils

############################################################################
# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
oLocalText = CyTranslator()

oMap = CyMap()
oGame = CyGame()
oInterface = CyInterface()
oGameText = CyGameTextMgr()

alert = CvAlertManager.CvAlertManager()

utils = JTradeRoutesUtils.g_oUtils
############################################################################
			

class CvAssignTradeRoutesToUnitPopup:
	"A Blank Civ4 Screen"
	
	def __init__(self):
		self.sWidgetPrefix = "TradeRoutesAssignUnitPopup"
		
		self.MANAGER_SCREEN_ID = self.sWidgetPrefix + "MainWindow"
		self.BACKGROUND_ID = self.sWidgetPrefix + "BackgroundImage"
		self.HEADER_PANEL_ID = self.sWidgetPrefix + "HeaderPanelWidget"
		self.FOOTER_PANEL_ID = self.sWidgetPrefix + "FooterPanelWidget"
		self.HEADER_ID = self.sWidgetPrefix + "HeaderTextWidget"
		self.EXIT_ID = self.sWidgetPrefix + "ExitTextWidget"

		self.TITLE = u"<font=4b>ASSIGN TRADE ROUTES</font>"

		self.X_SCREEN = 0
		self.Y_SCREEN = 0
		self.W_SCREEN = 1024
		self.H_SCREEN = 768

		self.H_BAR = 55
		
		self.Z_BACKGROUND = -6.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2

		self.nWidgetCount = 0

		self.initWidgetIDs()
		self.initValues()

	def initWidgetIDs(self):
		self.BACK_ID = self.sWidgetPrefix + "BackTextWidget"

                self.SCROLL_PANEL_ID = self.sWidgetPrefix + "ScrollPanel"

                self.PANEL_ID = self.sWidgetPrefix + "Panel"

                self.UNIT_PANEL_ID = self.sWidgetPrefix + "UnitPanel"

                self.TABLE_ID = self.sWidgetPrefix + "Table"

                self.SOURCE_CITY_PANEL_ID = self.sWidgetPrefix + "SourceCityPanel"

                self.DESTINATION_CITY_PANEL_ID = self.sWidgetPrefix + "DestinationCityPanel"
                return None

        def initValues(self):
                self.bTradeRoutesScreen = False
                self.iTradeRoutesTab = 0
                self.iScreenDirty = -1
                self.iMargin = 10
                self.iBorder = 20
                self.iBorder2 = self.iBorder * 2
                self.iButtonSize = 48
                self.iRowHeight = 40

                ###################################################

		self.iPlayer = -1
		self.pPlayer = None
		self.iUnit = -1
		self.pUnit = None

                ###################################################

		self.lTradeRoutes = []

                ###################################################

                self.X_SCROLL_PANEL = self.X_SCREEN
                self.Y_SCROLL_PANEL = self.Y_SCREEN + self.H_BAR - 10
                self.W_SCROLL_PANEL = self.W_SCREEN + 10
                self.H_SCROLL_PANEL = self.H_SCREEN - (self.H_BAR * 2) + 10

                self.X_PANEL = self.X_SCREEN
                self.Y_PANEL = self.Y_SCREEN# + self.H_BAR - 10
                self.W_PANEL = self.W_SCREEN - 10
                self.H_PANEL = self.H_SCREEN - (self.H_BAR * 2)

                ###################################################

		self.W_UNIT_ANIMATION = 128
		self.H_UNIT_ANIMATION = 128
		self.X_UNIT_ANIMATION = self.X_PANEL + self.iBorder2
		self.Y_UNIT_ANIMATION = (self.H_SCREEN - self.H_BAR) - self.H_UNIT_ANIMATION - (self.iBorder2)
		
		self.X_ROTATION_UNIT_ANIMATION = -20
		self.Z_ROTATION_UNIT_ANIMATION = 30
		self.SCALE_ANIMATION = 1.0

                ###################################################
                
                self.X_UNIT_PANEL = self.X_UNIT_ANIMATION + self.W_UNIT_ANIMATION + self.iMargin
                self.Y_UNIT_PANEL = self.Y_UNIT_ANIMATION - 54
                self.W_UNIT_PANEL = 218
                self.H_UNIT_PANEL = self.H_UNIT_ANIMATION

                ###################################################
                
                self.X_TABLE = self.X_UNIT_ANIMATION
                self.Y_TABLE = self.Y_SCROLL_PANEL + self.iBorder2#self.Y_PANEL + 84
                self.W_TABLE = 364
                self.H_TABLE = 440#self.H_PANEL - 60

                ###################################################

                self.X_SOURCE_CITY_PANEL = self.X_TABLE + self.W_TABLE + self.iBorder
                iW = self.W_SCREEN - self.X_SOURCE_CITY_PANEL - self.iBorder2
                self.W_CITY_PANEL = (iW - self.iMargin) / 2
                self.X_DESTINATION_CITY_PANEL = self.X_SOURCE_CITY_PANEL + self.W_CITY_PANEL + self.iMargin

                self.Y_CITY_PANEL = 32
                self.H_CITY_PANEL = 200#self.H_TABLE - self.H_MINIMAP - self.iBorder

                ###################################################

		self.X_LEFT_MINIMAP = self.X_SOURCE_CITY_PANEL + self.iMargin
		self.W_MINIMAP = self.W_SCREEN - self.X_SOURCE_CITY_PANEL - self.iBorder2 - 2
		self.X_RIGHT_MINIMAP = self.X_LEFT_MINIMAP + self.W_MINIMAP

		#self.Y_TOP_MINIMAP = self.Y_TABLE
		self.H_MINIMAP = 350#self.H_TABLE - (self.H_TABLE / 4)
		if (oMap.getGridWidth() > 0):# Must check this so we don't get Division by 0 Exception
                        self.H_MINIMAP_PREF = (self.W_MINIMAP * oMap.getGridHeight()) / oMap.getGridWidth()
                        if (self.H_MINIMAP > self.H_MINIMAP_PREF):
                                self.H_MINIMAP = self.H_MINIMAP_PREF

		self.Y_BOTTOM_MINIMAP = self.H_SCREEN - self.H_BAR - self.iBorder2#self.Y_TABLE + self.H_TABLE#self.Y_TOP_MINIMAP + self.H_MINIMAP
		self.Y_TOP_MINIMAP = self.Y_BOTTOM_MINIMAP - self.H_MINIMAP
		return None
				
        #############################################################################################################

	def getScreen(self):
		return CyGInterfaceScreen(self.MANAGER_SCREEN_ID, CvScreenEnums.JTRADEROUTES_ASSIGN_TRADE_ROUTES_TO_UNIT_POPUP)

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()
		return None

	def update(self, fDelta):
                if (self.iScreenDirty < 0):
                        return None
                elif (self.iScreenDirty > 0):
                        self.iScreenDirty -= 1
                else:
                        self.updateContent()
                        self.iScreenDirty -= 1
		return None

	# handle the input for this screen...
	def handleInput(self, inputClass):
		screen = self.getScreen()
		iNotifyCode = inputClass.getNotifyCode()
		iNotifyClicked = NotifyCode.NOTIFY_CLICKED
		iNotifyChar = NotifyCode.NOTIFY_CHARACTER
		iNotifyListSelect = NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED
		iNotifyScrollUp = NotifyCode.NOTIFY_SCROLL_UP
		iNotifyScrollDown = NotifyCode.NOTIFY_SCROLL_DOWN

                sFunctionName = inputClass.getFunctionName()
                iData1 = inputClass.getData1()
                iData2 = inputClass.getData2()
                #alert.debug(0, "(iData1, iData2)", (iData1, iData2))
		if (sFunctionName == self.BACK_ID) and (self.bTradeRoutesScreen):
                        #alert.debug(0, "self.bTradeRoutesScreen", self.bTradeRoutesScreen)
                        CvScreensInterface.showTradeRoutesScreen(self.iTradeRoutesTab)
                        return 1
                # Transports Table Clicked
		elif (sFunctionName == self.TABLE_ID):
                        self.drawBasicInfo()
                        self.updateCityTexts()
                        self.updateFlashingTiles()
                        return 1
                # Transport Assign Trade Route Button Clicked
                elif (inputClass.getButtonType() == WidgetTypes.WIDGET_ASSIGN_TRADE_ROUTE):
                        #alert.debug(0, "Assign Trade Route", True)
                        #self.clearTable()
                        self.iScreenDirty = 20
                        #self.updateTable()
		return 0

	# Adds Mouse Over Help to General Widgets
	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList

                if (iData1 == utils.iButtonExit):
			return utils.getText("TXT_KEY_INTERFACE_BUTTON_HELP_EXIT", iColor = -1)
                elif (iData1 == utils.iButtonBack):
			return utils.getText("TXT_KEY_INTERFACE_BUTTON_HELP_BACK", iColor = -1)
		elif (iData1 == utils.iTableTradeRoutes):
                        sText = u""
                        lTransports = utils.getTradeRouteTransports(oGame.getActivePlayer(), iData2)
                        iTransports = len(lTransports)
                        if (iTransports < 1):
                                return utils.getText("TXT_KEY_INTERFACE_NO_ASSIGNED_TRANSPORTS_HELP_TITLE", iColor = -1)
                        sText += utils.getText("TXT_KEY_INTERFACE_ASSIGNED_TRANSPORTS_HELP_TITLE", iColor = -1)
                        for iIndex in range(iTransports):
                                pTransport = lTransports[iIndex]
                                sText += u"\n"
                                tArgs = (oGameText.getSpecificUnitHelp(pTransport, False, True), )
                                sText += utils.getText("TXT_KEY_INTERFACE_TRANSPORT_HELP", tArgs, iColor = -1)
			return unicode(sText)
		return u""

        #############################################################################################################
										
	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.sWidgetPrefix + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName
	
	def deleteDynamicWidgets(self):
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while (i >= 0):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = 0
		return None
				
        #############################################################################################################

	# Screen construction function
	def interfaceScreen(self, iPlayer, iUnit, bTradeRoutesScreen = False, iTradeRoutesTab = 0):
		screen = self.getScreen()
		if (screen.isActive()):
			return None
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		#screen.setDimensions(self.X_SCREEN, self.Y_SCREEN, self.W_SCREEN, self.H_SCREEN)
			
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.showWindowBackground(True)

		self.initValues()
		self.bTradeRoutesScreen = bTradeRoutesScreen
		self.iTradeRoutesTab = iTradeRoutesTab

		self.iPlayer = iPlayer
		self.pPlayer = gc.getPlayer(self.iPlayer)
		self.iUnit = iUnit
		self.pUnit = self.pPlayer.getUnit(self.iUnit)

		iX = 0
		iY = 0

		# Set the background widget
		screen.addDrawControl(self.BACKGROUND_ID,
                                      ArtFileMgr.getInterfaceArtInfo("FATHER_BG").getPath(),
                                      self.X_SCREEN, self.Y_SCREEN,
                                      self.W_SCREEN, self.H_SCREEN,
                                      WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.drawHeader()
		self.drawFooter()

		self.drawContent()
				
        #############################################################################################################

        def drawHeader(self):
		screen = self.getScreen()
		iX = 0
		iY = 0
		screen.addDDSGFC(self.HEADER_PANEL_ID,
                                 ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TITLE").getPath(),
                                 self.X_SCREEN, self.Y_SCREEN,
                                 self.W_SCREEN, self.H_BAR,
                                 WidgetTypes.WIDGET_GENERAL, -1, -1)
		sTitle = u"<font=4>%s</font>" %(oGameText.getSpecificUnitHelp(self.pUnit, True, False))#%(self.TITLE)
		sTitle = self.getText(sTitle)
		screen.setText(self.HEADER_ID, self.BACKGROUND_ID, sTitle,
                               CvUtil.FONT_CENTER_JUSTIFY,
                               self.W_SCREEN / 2, self.Y_SCREEN + 4,
                               0,
                               FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		return None

        def drawFooter(self):
		screen = self.getScreen()
		screen.addPanel(self.FOOTER_PANEL_ID, u"", u"", True, False,
                                self.X_SCREEN, self.H_SCREEN - self.H_BAR,
                                self.W_SCREEN, self.H_BAR,
                                PanelStyles.PANEL_STYLE_BOTTOMBAR, WidgetTypes.WIDGET_GENERAL, -1, -1)
		# Need a Back Button to return to the Trade Routes Advisor Screen
		sText = u"<font=4>%s</font>" %(utils.getText("TXT_KEY_PEDIA_SCREEN_BACK", iColor = -1).upper())
		screen.setText(self.BACK_ID, self.BACKGROUND_ID, sText,
                               CvUtil.FONT_RIGHT_JUSTIFY,
                               self.W_SCREEN - 30, self.H_SCREEN - 40,
                               self.Z_CONTROLS,
                               FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN,
                               utils.iButtonBack, -1)
		# Move the Exit Button to the left
		sText = u"<font=4>%s</font>" %(utils.getText("TXT_KEY_PEDIA_SCREEN_EXIT", iColor = -1).upper())
		screen.setText(self.EXIT_ID, self.BACKGROUND_ID, sText,
                               CvUtil.FONT_RIGHT_JUSTIFY,
                               self.W_SCREEN - 30 - 200, self.H_SCREEN - 40,
                               self.Z_CONTROLS,
                               FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN,
                               utils.iButtonExit, -1)
		screen.setFocus(self.EXIT_ID)
		return None
				
        #############################################################################################################

        def drawContent(self):
		screen = self.getScreen()
                #for s in dir(screen):
                #        alert.alert(0, s)
                self.initMinimap()

		self.drawScrollPanel()
                self.drawPanel()
                self.drawAnimation()
                self.drawUnitPanel()
                self.drawUnitTexts()
		self.updateContent()
                return None

        def updateContent(self):
                self.updateTable()
		self.updateCityTexts()
                self.drawBasicInfo()
                self.updateFlashingTiles()
                return None

        def updateCityTexts(self):
		self.drawSourceCityPanel()
		self.drawDestinationCityPanel()
                self.drawSourceCityTexts()
                self.drawDestinationCityTexts()
                return None

        def clearContent(self):
                screen = self.getScreen()
                #screen.deleteWidget(self.TABLE_ID)
                #screen.deleteWidget(self.TABLE_ID)
                return None
				
        #############################################################################################################

	def drawScrollPanel(self):
		screen = self.getScreen()
		screen.addScrollPanel(self.SCROLL_PANEL_ID, u"",
                                      self.X_SCROLL_PANEL, self.Y_SCROLL_PANEL,
                                      self.W_SCROLL_PANEL, self.H_SCROLL_PANEL,
                                      PanelStyles.PANEL_STYLE_EXTERNAL, True, WidgetTypes.WIDGET_GENERAL, -1, -1)
		return None

        #############################################################################################################

	def drawPanel(self):
		screen = self.getScreen()
		screen.attachPanelAt(self.SCROLL_PANEL_ID, self.PANEL_ID,
                                     u"", u"",
                                     True, True,
                                     PanelStyles.PANEL_STYLE_IN,#PANEL_STYLE_MAIN,#
                                     self.X_PANEL, self.Y_PANEL,
                                     self.W_PANEL, self.H_PANEL,
                                     WidgetTypes.WIDGET_GENERAL, -1, -1)
		return None

        #############################################################################################################

	def drawAnimation(self):
		screen = self.getScreen()
                # Unit animation
		screen.addUnitGraphicGFC(self.getNextWidgetName(),
                                         self.pUnit.getUnitType(), -1,
                                         self.X_UNIT_ANIMATION, self.Y_UNIT_ANIMATION,
                                         self.W_UNIT_ANIMATION, self.H_UNIT_ANIMATION,
                                         WidgetTypes.WIDGET_GENERAL, -1, -1,
                                         self.X_ROTATION_UNIT_ANIMATION, self.Z_ROTATION_UNIT_ANIMATION,
                                         self.SCALE_ANIMATION, True)
                return None

        #############################################################################################################

	def drawUnitPanel(self):
		screen = self.getScreen()
		screen.attachPanelAt(self.SCROLL_PANEL_ID, self.UNIT_PANEL_ID,
                                     u"", u"",
                                     True, True,
                                     PanelStyles.PANEL_STYLE_IN,#PANEL_STYLE_MAIN,#
                                     self.X_UNIT_PANEL, self.Y_UNIT_PANEL,
                                     self.W_UNIT_PANEL, self.H_UNIT_PANEL,
                                     WidgetTypes.WIDGET_GENERAL, -1, -1)
                return None

        def drawUnitTexts(self):
		screen = self.getScreen()
		# Unit Domain
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRANSPORT_DOMAIN", (gc.getDomainInfo(self.pUnit.getDomainType()).getDescription(), )))
                iX = 0
                iY = self.iMargin
                screen.setTextAt(self.getNextWidgetName(), self.UNIT_PANEL_ID,
                                sText,
                                CvUtil.FONT_LEFT_JUSTIFY,
                                iX, iY, 0,
                                FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		# Unit Cargo Space
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRANSPORT_CARGO_SPACE", (self.pUnit.cargoSpace(), )))
                iY += self.iBorder + self.iMargin
                screen.setTextAt(self.getNextWidgetName(), self.UNIT_PANEL_ID,
                                sText,
                                CvUtil.FONT_LEFT_JUSTIFY,
                                iX, iY, 0,
                                FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                return None

        #############################################################################################################

	def drawBasicInfo(self):
		screen = self.getScreen()
		pTradeRoute = self.getSelectedTradeRoute()
                iY = self.iMargin + 6
                # Trade Route Domain Type
                sLand = utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_LAND", iColor = -1)
		sSea = utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_SEA", iColor = -1)
		if (pTradeRoute == None):
                        sTextR = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SCREEN_NA"))
		elif (pTradeRoute.isLandRoute() and pTradeRoute.isSeaRoute()):
                        sTextR = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_LAND_AND_SEA",
                                                                      (sLand, sSea)))
                elif (pTradeRoute.isLandRoute()):
                        sTextR = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_LAND"))
                elif (pTradeRoute.isSeaRoute()):
                        sTextR = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_SEA"))
                else:
                        sTextR = u"<font=3>Unknown</font>"
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_DOMAIN", (sTextR, )))
                iX = self.X_TABLE - 10
                screen.setTextAt("TradeRouteDomainText", self.SCROLL_PANEL_ID,
                                sText,
                                CvUtil.FONT_LEFT_JUSTIFY,
                                iX, iY, 0,
                                FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Trade Route Yield
		if (pTradeRoute == None):
                        sDesc = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SCREEN_NA"))
                        sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_YIELD", (sDesc, )))
                else:
                        sDesc = gc.getYieldInfo(pTradeRoute.getYield()).getDescription()
                        sChar = gc.getYieldInfo(pTradeRoute.getYield()).getChar()
                        sText = u"<font=3>%s %c</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_YIELD", (sDesc, )), sChar)
                iX = self.X_SOURCE_CITY_PANEL#self.iBorder + 4
                screen.setTextAt("TradeRouteYieldText", self.SCROLL_PANEL_ID,
                                sText,
                                CvUtil.FONT_LEFT_JUSTIFY,
                                iX, iY, 0,
                                FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

                # Trade Route Estimated Distance
                if (pTradeRoute != None) and (not pTradeRoute.isSourceEurope()) and (not pTradeRoute.isDestinationEurope()):
                        pSourceCity = gc.getPlayer(pTradeRoute.getSourceCity().eOwner).getCity(pTradeRoute.getSourceCity().iID)
                        pDestinationCity = gc.getPlayer(pTradeRoute.getDestinationCity().eOwner).getCity(pTradeRoute.getDestinationCity().iID)
                        iDistance = oMap.calculatePathDistance(pSourceCity.plot(), pDestinationCity.plot())
                        sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_DISTANCE", (iDistance, )))
                else:
                        sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_NO_DISTANCE"))
                iX = self.X_DESTINATION_CITY_PANEL
                screen.setTextAt("TradeRouteDistanceText", self.SCROLL_PANEL_ID,
                                 sText,
                                 CvUtil.FONT_LEFT_JUSTIFY,
                                 iX, iY, 0,
                                 FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		return None

        #############################################################################################################

	def drawSourceCityPanel(self):
		screen = self.getScreen()
		screen.attachPanelAt(self.SCROLL_PANEL_ID, self.SOURCE_CITY_PANEL_ID,
                                     u"", u"",
                                     True, True,
                                     PanelStyles.PANEL_STYLE_IN,#PANEL_STYLE_MAIN,#
                                     self.X_SOURCE_CITY_PANEL, self.Y_CITY_PANEL,
                                     self.W_CITY_PANEL, self.H_CITY_PANEL,
                                     WidgetTypes.WIDGET_GENERAL, -1, -1)
                return None

	def drawSourceCityTexts(self):
		screen = self.getScreen()
		pTradeRoute = self.getSelectedTradeRoute()
		if (pTradeRoute != None):
                        kCity = pTradeRoute.getSourceCity()
                        pCity = gc.getPlayer(kCity.eOwner).getCity(kCity.iID)
                        self.drawCityTexts(kCity, pCity, pTradeRoute, self.SOURCE_CITY_PANEL_ID)
                return None

        #############################################################################################################

	def drawDestinationCityPanel(self):
		screen = self.getScreen()
		screen.attachPanelAt(self.SCROLL_PANEL_ID, self.DESTINATION_CITY_PANEL_ID,
                                     u"", u"",
                                     True, True,
                                     PanelStyles.PANEL_STYLE_IN,#PANEL_STYLE_MAIN,#
                                     self.X_DESTINATION_CITY_PANEL, self.Y_CITY_PANEL,
                                     self.W_CITY_PANEL, self.H_CITY_PANEL,
                                     WidgetTypes.WIDGET_GENERAL, -1, -1)
                return None

	def drawDestinationCityTexts(self):
		screen = self.getScreen()
		pTradeRoute = self.getSelectedTradeRoute()
		if (pTradeRoute != None):
                        kCity = pTradeRoute.getDestinationCity()
                        pCity = gc.getPlayer(kCity.eOwner).getCity(kCity.iID)
                        self.drawCityTexts(kCity, pCity, pTradeRoute, self.DESTINATION_CITY_PANEL_ID)
                return None

        #############################################################################################################

        def drawCityTexts(self, kCity, pCity, pTradeRoute, sPanel):
		screen = self.getScreen()
		# City Name
		if (kCity.eOwner == pTradeRoute.getSourceCity().eOwner) \
                   and (kCity.iID == pTradeRoute.getSourceCity().iID):
                        sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_SOURCE_CITY", (pCity.getName(), )))
		if (kCity.eOwner == pTradeRoute.getDestinationCity().eOwner) \
                   and (kCity.iID == pTradeRoute.getDestinationCity().iID):
                        sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_DESTINATION_CITY", (pCity.getName(), )))
                iX = 0
                iY = self.iMargin
                screen.setTextAt(self.getNextWidgetName(), sPanel,
                                sText,
                                CvUtil.FONT_LEFT_JUSTIFY,
                                iX, iY, 0,
                                FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

                # Yield Rate
		if (kCity.iID == pTradeRoute.getEuropeCityID()):
                        sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_YIELD_NO_RATE"))
                else:
                        iYieldRate = pCity.getYieldRate(pTradeRoute.getYield())
                        sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_YIELD_RATE", (iYieldRate, )))
                iY += self.iBorder + self.iMargin
                screen.setTextAt(self.getNextWidgetName(), sPanel,
                                sText,
                                CvUtil.FONT_LEFT_JUSTIFY,
                                iX, iY, 0,
                                FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

                # Yield Stored
		if (kCity.iID == pTradeRoute.getEuropeCityID()):
                        sTotalText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SCREEN_NA"))
                else:
                        iYieldStored = pCity.getYieldStored(pTradeRoute.getYield())
                        sTextL = u"<font=3>%d</font>" %(iYieldStored)
                        iMaxYield = pCity.getMaxYieldCapacity()
                        if (iYieldStored >= iMaxYield):
                                iColor = gc.getInfoTypeForString("COLOR_RED")
                        elif (iYieldStored >= iMaxYield / 2):
                                iColor = gc.getInfoTypeForString("COLOR_YELLOW")
                        else:
                                iColor = gc.getInfoTypeForString("COLOR_GREEN")
                        sTextL = utils.getText(sTextL, (), iColor)
                        sTextR = u"<font=3> (%d)</font>" %(iMaxYield)
                        sTextR = utils.getText(sTextR)
                        sTotalText = sTextL + sTextR
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_YIELD_STORED", (sTotalText, )))
                iY += self.iBorder + self.iMargin
                screen.setTextAt(self.getNextWidgetName(), sPanel,
                                sText,
                                CvUtil.FONT_LEFT_JUSTIFY,
                                iX, iY, 0,
                                FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                return None

        #############################################################################################################

        def updateTable(self):
                self.drawTable()
                self.drawTableHeaders()
                self.fillTable()
                return None

        def clearTable(self):
                screen = self.getScreen()
                screen.deleteWidget(self.TABLE_ID)
                return None

        def drawTable(self):
		screen = self.getScreen()
                iColumns = 20
		screen.addTableControlGFC(self.TABLE_ID,
                                          iColumns,
                                          self.X_TABLE, self.Y_TABLE,
                                          self.W_TABLE, self.H_TABLE,
                                          True, True,
                                          self.iButtonSize, self.iButtonSize,
                                          TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.TABLE_ID, True)
		screen.enableSort(self.TABLE_ID)
		screen.setStyle(self.TABLE_ID, "Table_StandardCiv_Style")
		return None

        def drawTableHeaders(self):
		screen = self.getScreen()
                iTotalWidth = 0
                iColumn = -1

                iColumn += 1
                iColumnWidth = 250
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTES", (), -1))
		screen.setTableColumnHeader(self.TABLE_ID,
                                            iColumn, sText, iColumnWidth)
                iColumn += 1
                iColumnWidth = 40
                iTotalWidth += iColumnWidth
                sText = u""#u"<font=3>%s</font>" %(utils.getText("Assigned", (), -1))
		screen.setTableColumnHeader(self.TABLE_ID,
                                            iColumn, sText, iColumnWidth)
                iColumn += 1
                iColumnWidth = 74
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_ASSIGNED", (), -1))
		screen.setTableColumnHeader(self.TABLE_ID,
                                            iColumn, sText, iColumnWidth)
                iColumn += 1
                iColumnWidth = self.W_TABLE - iTotalWidth
                iTotalWidth += iColumnWidth
                sText = u"%s" %(iColumnWidth)
		screen.setTableColumnHeader(self.TABLE_ID,
                                            iColumn, sText, iColumnWidth)
		return None

	def fillTable(self):
		#alert.alert(0, "fillTradeRoutesList")
		screen = self.getScreen()
		#iPlayer = oGame.getActivePlayer()
		#pPlayer = gc.getPlayer(iPlayer)
		iRow = -1
		self.lTradeRoutes = []
		for pTradeRoute in utils.getPlayerTradeRoutes(self.iPlayer):
                        if (not pTradeRoute.isLandRoute()) and (self.pUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_LAND")):
                                continue
                        if (not pTradeRoute.isSeaRoute()) and (self.pUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_SEA")):
                                continue
                        self.lTradeRoutes += [pTradeRoute]
                        iTradeRoute = pTradeRoute.getID()
                        iRow += 1
                        screen.appendTableRow(self.TABLE_ID)
                        screen.setTableRowHeight(self.TABLE_ID, iRow, self.iRowHeight)

                        iColumn = -1

                        # Trade Route Name
                        iColumn += 1
                        sText = utils.getTradeRouteName(pTradeRoute)
                        sText = self.getText(sText)
                        screen.setTableText(self.TABLE_ID,
                                            iColumn, iRow,
                                            sText, "",
                                            WidgetTypes.WIDGET_GENERAL,
                                            utils.iTableTradeRoutes, pTradeRoute.getID(), CvUtil.FONT_LEFT_JUSTIFY)

                        # Assign/Unassign Button
                        iColumn += 1
                        if (self.pUnit.getGroup().isAssignedTradeRoute(iTradeRoute)):
                                sText = u"<font=4>%s</font>" %(utils.getText("-", iColor = -1))
                        else:
                                sText = u"<font=4>%s</font>" %(utils.getText("+", iColor = -1))
                        screen.setButtonGFC("RouteToggle" + str(iRow),
                                            sText, "",
                                            0, 0,
                                            30, 30,
                                            WidgetTypes.WIDGET_ASSIGN_TRADE_ROUTE,#WIDGET_GENERAL,#
                                            self.pUnit.getID(), iTradeRoute,
                                            ButtonStyles.BUTTON_STYLE_STANDARD)
                        screen.attachControlToTableCell("RouteToggle" + str(iRow), self.TABLE_ID, iRow, iColumn)

                        # Is Trade Route Assigned
                        iColumn += 1
                        if (self.pUnit.getGroup().isAssignedTradeRoute(iTradeRoute)):
                                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_YES"))
                        else:
                                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_NO"))
                        #sText = self.getText(sText)
                        screen.setTableText(self.TABLE_ID,
                                            iColumn, iRow,
                                            sText, "",
                                            WidgetTypes.WIDGET_GENERAL,
                                            -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
                iRow += 1
                screen.appendTableRow(self.TABLE_ID)
                screen.setTableRowHeight(self.TABLE_ID, iRow, self.iRowHeight)
		return None

        #############################################################################################################

	def initMinimap(self):
		screen = self.getScreen()

		self.viewMargin = 20
		self.viewX = 455 - self.viewMargin
		self.viewY = 60
		self.viewWidth = self.W_SCREEN - self.viewX
		self.viewHeight = self.H_SCREEN - 220

		mapWidth = self.viewWidth - 2 * self.viewMargin
		mapHeight = self.viewHeight - 2 * self.viewMargin

		mapHeightPref = (mapWidth * CyMap().getGridHeight()) / CyMap().getGridWidth()
		if (mapHeightPref > mapHeight):
			mapWidth = (mapHeight * CyMap().getGridWidth()) / CyMap().getGridHeight()
			horMapMargin = (self.viewWidth - mapWidth) / 2
			verMapMargin = self.viewMargin
		else:
			mapHeight = mapHeightPref
			horMapMargin = self.viewMargin
			verMapMargin = (self.viewHeight - mapHeight) / 2

		"""screen.initMinimap(self.viewX + horMapMargin, self.viewX + self.viewWidth - horMapMargin,
                                   self.viewY + verMapMargin, self.viewY + self.viewHeight - verMapMargin,
                                   self.Z_CONTROLS, False)"""

		screen.initMinimap(self.X_LEFT_MINIMAP, self.X_RIGHT_MINIMAP,
                                   self.Y_TOP_MINIMAP, self.Y_BOTTOM_MINIMAP,
                                   self.Z_CONTROLS, False)
		screen.updateMinimapSection(False)

		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_MILITARY)

		iOldMode = CyInterface().getShowInterface()
		CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_MINIMAP_ONLY)
		screen.updateMinimapVisibility()
		CyInterface().setShowInterface(iOldMode)
		return None

        #############################################################################################################

	def updateFlashingTiles(self):
		screen = self.getScreen()
                screen.minimapClearAllFlashingTiles()
                self.updateCityFlash()
                self.updateTransportFlash()
                return None

        def updateTransportFlash(self):
		screen = self.getScreen()
                iColor = gc.getInfoTypeForString("COLOR_WHITE")
                screen.minimapFlashPlot(self.pUnit.getX(), self.pUnit.getY(), iColor, -1)
                return None

	def updateCityFlash(self):
		screen = self.getScreen()
		pTradeRoute = self.getSelectedTradeRoute()
                if (pTradeRoute != None):# and (not pTradeRoute.isNone()):
                        pSourceCity = gc.getPlayer(pTradeRoute.getSourceCity().eOwner).getCity(pTradeRoute.getSourceCity().iID)
                        pDestinationCity = gc.getPlayer(pTradeRoute.getDestinationCity().eOwner).getCity(pTradeRoute.getDestinationCity().iID)
                        iColor = gc.getInfoTypeForString("COLOR_GREEN")
                        screen.minimapFlashPlot(pSourceCity.getX(), pSourceCity.getY(), iColor, -1)
                        iColor = gc.getInfoTypeForString("COLOR_RED")
                        screen.minimapFlashPlot(pDestinationCity.getX(), pDestinationCity.getY(), iColor, -1)
                return None

        #############################################################################################################

        def getSelectedTradeRoute(self):
		screen = self.getScreen()
		pTradeRoute = None
		iRows = screen.getTableNumRows(self.TABLE_ID)
		if (not screen.isRowSelected(self.TABLE_ID, iRows - 1)):
                        for iRow in range(len(self.lTradeRoutes)):
                                if (screen.isRowSelected(self.TABLE_ID, iRow)):
                                        pTradeRoute = self.lTradeRoutes[iRow]
                                        break
                        if (pTradeRoute == None) and (len(self.lTradeRoutes) > 0):
                                pTradeRoute = self.lTradeRoutes[0]
                return pTradeRoute

	def getText(self, sText, tArgs = (), iColor = gc.getInfoTypeForString("COLOR_FONT_CREAM")):
                #sText = u"%s" %(sText)
                try:
                        sText = oLocalText.getText(sText, tArgs)
                except:
                        pass
                sText = oLocalText.changeTextColor(sText, iColor)
                return sText

        #############################################################################################################

