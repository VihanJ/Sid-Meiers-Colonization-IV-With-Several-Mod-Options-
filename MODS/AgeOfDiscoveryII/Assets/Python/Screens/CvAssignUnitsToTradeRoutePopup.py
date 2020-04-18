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
oGameText = CyGameTextMgr()

oMap = CyMap()
oGame = CyGame()
oInterface = CyInterface()

alert = CvAlertManager.CvAlertManager()

utils = JTradeRoutesUtils.g_oUtils
############################################################################
			

class CvAssignUnitsToTradeRoutePopup:
	"A Blank Civ4 Screen"
	
	def __init__(self):
		self.sWidgetPrefix = "TradeRoutesAssignUnitPopup"
		
		self.MANAGER_SCREEN_ID = self.sWidgetPrefix + "MainWindow"
		self.BACKGROUND_ID = self.sWidgetPrefix + "BackgroundImage"
		self.HEADER_PANEL_ID = self.sWidgetPrefix + "HeaderPanelWidget"
		self.FOOTER_PANEL_ID = self.sWidgetPrefix + "FooterPanelWidget"
		self.HEADER_ID = self.sWidgetPrefix + "HeaderTextWidget"
		self.EXIT_ID = self.sWidgetPrefix + "ExitTextWidget"

		self.TITLE = u"<font=4b>TRADE ROUTES</font>"

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

                self.TABLE_PANEL_ID = self.sWidgetPrefix + "TablePanel"
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
                self.iButtonSize = 48
                self.iRowHeight = 40

                ###################################################

		self.iPlayer = -1
		self.pPlayer = None
		self.iTradeRoute = -1
		self.pTradeRoute = None
		self.pSourceCity = None
		self.pDestinationCity = None

                ###################################################

		self.lTransports = []

                ###################################################

                self.X_SCROLL_PANEL = self.X_SCREEN
                self.Y_SCROLL_PANEL = self.Y_SCREEN + self.H_BAR - 10
                self.W_SCROLL_PANEL = self.W_SCREEN + 10
                self.H_SCROLL_PANEL = self.H_SCREEN - (self.H_BAR * 2) + 10

                self.X_PANEL = self.X_SCREEN
                self.Y_PANEL = self.Y_SCREEN# + self.H_BAR - 10
                self.W_PANEL = self.W_SCREEN - 10
                self.H_PANEL = self.H_SCREEN - (self.H_BAR * 2)
                
                self.X_TABLE = self.X_PANEL + 38
                self.Y_TABLE = self.Y_SCROLL_PANEL + 40#self.Y_PANEL + 84
                self.W_TABLE = self.W_PANEL - 60 - 590
                self.H_TABLE = self.H_PANEL - 60

                ###################################################

		self.X_LEFT_MINIMAP = self.X_TABLE + self.W_TABLE + self.iBorder
		self.W_MINIMAP = self.W_SCREEN - self.X_LEFT_MINIMAP - self.iBorder
		self.X_RIGHT_MINIMAP = self.X_LEFT_MINIMAP + self.W_MINIMAP

		#self.Y_TOP_MINIMAP = self.Y_TABLE
		self.H_MINIMAP = self.H_TABLE - (self.H_TABLE / 4)
		if (oMap.getGridWidth() > 0):# Must check this so we don't get Division by 0 Exception
                        self.H_MINIMAP_PREF = (self.W_MINIMAP * oMap.getGridHeight()) / oMap.getGridWidth()
                        if (self.H_MINIMAP > self.H_MINIMAP_PREF):
                                self.H_MINIMAP = self.H_MINIMAP_PREF

		self.Y_BOTTOM_MINIMAP = self.Y_TABLE + self.H_TABLE#self.Y_TOP_MINIMAP + self.H_MINIMAP
		self.Y_TOP_MINIMAP = self.Y_BOTTOM_MINIMAP - self.H_MINIMAP

                ###################################################

                self.Y_CITY_PANEL = 32
                self.W_CITY_PANEL = (self.W_MINIMAP - self.iMargin) / 2
                self.H_CITY_PANEL = self.H_TABLE - self.H_MINIMAP - self.iBorder

                self.X_SOURCE_CITY_PANEL = self.X_LEFT_MINIMAP - 8
                self.X_DESTINATION_CITY_PANEL = self.X_SOURCE_CITY_PANEL + self.W_CITY_PANEL + self.iMargin
		return None
				
        #############################################################################################################

	def getScreen(self):
		return CyGInterfaceScreen(self.MANAGER_SCREEN_ID, CvScreenEnums.JTRADEROUTES_ASSIGN_UNITS_TO_TRADE_ROUTE_POPUP)

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
                elif (iData1 == utils.iTableTransports):
                        pTransport = gc.getActivePlayer().getUnit(iData2)
			return oGameText.getSpecificUnitHelp(pTransport, False, True)#utils.getText("TXT_KEY_INTERFACE_BUTTON_HELP_BACK", iColor = -1)
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
	def interfaceScreen(self, iPlayer, iTradeRoute, bTradeRoutesScreen = False, iTradeRoutesTab = 0):
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
		self.iTradeRoute = iTradeRoute
		self.pTradeRoute = self.pPlayer.getTradeRoute(self.iTradeRoute)

                kCity = self.pTradeRoute.getSourceCity()
		self.pSourceCity = gc.getPlayer(kCity.eOwner).getCity(kCity.iID)
                kCity = self.pTradeRoute.getDestinationCity()
		self.pDestinationCity = gc.getPlayer(kCity.eOwner).getCity(kCity.iID)

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
		sTitle = u"<font=4>%s</font>" %(utils.getTradeRouteName(self.pTradeRoute))#oLocalText.changeTextColor(self.TITLE, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
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
                self.initMinimap()

		self.drawScrollPanel()
                self.drawPanel()
                self.drawBasicInfo()
		self.drawSourceCityPanel()
                self.drawSourceCityTexts()
		self.drawDestinationCityPanel()
                self.drawDestinationCityTexts()
		self.updateContent()
                return None

        def updateContent(self):
                self.updateTable()
                self.updateFlashingTiles()
                return None

        def clearContent(self):
                screen = self.getScreen()
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
		screen.attachPanelAt(self.SCROLL_PANEL_ID, self.TABLE_PANEL_ID,
                                     u"", u"",
                                     True, True,
                                     PanelStyles.PANEL_STYLE_IN,#PANEL_STYLE_MAIN,#
                                     self.X_PANEL, self.Y_PANEL,
                                     self.W_PANEL, self.H_PANEL,
                                     WidgetTypes.WIDGET_GENERAL, -1, -1)
		return None

        #############################################################################################################

	def drawBasicInfo(self):
		screen = self.getScreen()
                iY = self.iMargin + 6
                # Trade Route Domain Type
                sLand = utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_LAND", iColor = -1)
		sSea = utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_SEA", iColor = -1)
		if (self.pTradeRoute.isLandRoute() and self.pTradeRoute.isSeaRoute()):
                        sTextR = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_LAND_AND_SEA",
                                                                      (sLand, sSea)))
                elif (self.pTradeRoute.isLandRoute()):
                        sTextR = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_LAND"))
                elif (self.pTradeRoute.isSeaRoute()):
                        sTextR = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_SEA"))
                else:
                        sTextR = u"<font=3>Unknown</font>"
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_DOMAIN", (sTextR, )))
                iX = self.X_TABLE - 10
                screen.setTextAt(self.getNextWidgetName(), self.SCROLL_PANEL_ID,
                                sText,
                                CvUtil.FONT_LEFT_JUSTIFY,
                                iX, iY, 0,
                                FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Trade Route Yield
		sDesc = gc.getYieldInfo(self.pTradeRoute.getYield()).getDescription()
		sChar = gc.getYieldInfo(self.pTradeRoute.getYield()).getChar()
                sText = u"<font=3>%s %c</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_YIELD", (sDesc, )), sChar)
                iX = self.X_SOURCE_CITY_PANEL#self.iBorder + 4
                screen.setTextAt(self.getNextWidgetName(), self.SCROLL_PANEL_ID,
                                sText,
                                CvUtil.FONT_LEFT_JUSTIFY,
                                iX, iY, 0,
                                FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

                # Trade Route Estimated Distance
                if (not self.pTradeRoute.isSourceEurope()) and (not self.pTradeRoute.isDestinationEurope()):
                        iDistance = oMap.calculatePathDistance(self.pSourceCity.plot(), self.pDestinationCity.plot())
                        sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_DISTANCE", (iDistance, )))
                else:
                        sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_NO_DISTANCE"))
                iX = self.X_DESTINATION_CITY_PANEL
                screen.setTextAt(self.getNextWidgetName(), self.SCROLL_PANEL_ID,
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
                self.drawCityTexts(self.pTradeRoute.getSourceCity(),
                                   self.pSourceCity, self.SOURCE_CITY_PANEL_ID)
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
                self.drawCityTexts(self.pTradeRoute.getDestinationCity(),
                                   self.pDestinationCity, self.DESTINATION_CITY_PANEL_ID)
                return None

        #############################################################################################################

        def drawCityTexts(self, kCity, pCity, sPanel):
		screen = self.getScreen()
		# City Name
		if (kCity.eOwner == self.pTradeRoute.getSourceCity().eOwner) \
                   and (kCity.iID == self.pTradeRoute.getSourceCity().iID):
                        sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_SOURCE_CITY", (pCity.getName(), )))
		if (kCity.eOwner == self.pTradeRoute.getDestinationCity().eOwner) \
                   and (kCity.iID == self.pTradeRoute.getDestinationCity().iID):
                        sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_DESTINATION_CITY", (pCity.getName(), )))
                iX = 0
                iY = self.iMargin
                screen.setTextAt(self.getNextWidgetName(), sPanel,
                                sText,
                                CvUtil.FONT_LEFT_JUSTIFY,
                                iX, iY, 0,
                                FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

                # Yield Rate
		if (kCity.iID == self.pTradeRoute.getEuropeCityID()):
                        sText = utils.getText("TXT_KEY_SCREEN_NA")
                else:
                        iYieldRate = pCity.getYieldRate(self.pTradeRoute.getYield())
                        #sText = u"<font=3>%s:   %d</font>" %(utils.getText("Yield Rate", iColor = -1), iYieldRate)
                        sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRADE_ROUTE_YIELD_RATE", (iYieldRate, )))
                iY += self.iBorder + self.iMargin
                screen.setTextAt(self.getNextWidgetName(), sPanel,
                                sText,
                                CvUtil.FONT_LEFT_JUSTIFY,
                                iX, iY, 0,
                                FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

                # Yield Stored
		if (kCity.iID == self.pTradeRoute.getEuropeCityID()):
                        sTotalText = utils.getText("TXT_KEY_SCREEN_NA")
                else:
                        iYieldStored = pCity.getYieldStored(self.pTradeRoute.getYield())
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
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_POPUP_TRANSPORT_NAME", (), -1))
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
		iPlayer = oGame.getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		iRow = -1
		self.lTransports = []
		for pLoopUnit in utils.getPlayerUnits(self.iPlayer):
                        if (pLoopUnit.cargoSpace() < 1):
                                continue
                                """
                        if (not pLoopUnit.canAssignTradeRoute(self.iTradeRoute)) \
                           and (not pLoopUnit.getGroup().isAssignedTradeRoute(self.iTradeRoute)):"""
                        elif (self.pTradeRoute.isSeaRoute()) and (not self.pTradeRoute.isLandRoute()) \
                           and (pLoopUnit.getDomainType() != gc.getInfoTypeForString("DOMAIN_SEA")):
                                continue
                        elif (self.pTradeRoute.isLandRoute()) and (not self.pTradeRoute.isSeaRoute()) \
                           and (pLoopUnit.getDomainType() != gc.getInfoTypeForString("DOMAIN_LAND")):
                                continue
                        self.lTransports += [pLoopUnit]
                        #alert.alert(0, "Ok")
                        iRow += 1
                        screen.appendTableRow(self.TABLE_ID)
                        screen.setTableRowHeight(self.TABLE_ID, iRow, self.iRowHeight)

                        iColumn = -1

                        # Transport Name
                        iColumn += 1
                        sText = pLoopUnit.getName()
                        sText = self.getText(sText)
                        screen.setTableText(self.TABLE_ID,
                                            iColumn, iRow,
                                            sText, "",
                                            WidgetTypes.WIDGET_GENERAL,
                                            utils.iTableTransports, pLoopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)

                        # Assign/Unassign Button
                        iColumn += 1
                        if (pLoopUnit.getGroup().isAssignedTradeRoute(self.iTradeRoute)):
                                sText = u"<font=4>%s</font>" %(utils.getText("-", iColor = -1))
                        else:
                                sText = u"<font=4>%s</font>" %(utils.getText("+", iColor = -1))
                        screen.setButtonGFC("RouteToggle" + str(iRow),
                                            sText, "",
                                            0, 0,
                                            30, 30,
                                            WidgetTypes.WIDGET_ASSIGN_TRADE_ROUTE,#WIDGET_GENERAL,#
                                            pLoopUnit.getID(), self.iTradeRoute,
                                            ButtonStyles.BUTTON_STYLE_STANDARD)
                        screen.attachControlToTableCell("RouteToggle" + str(iRow), self.TABLE_ID, iRow, iColumn)

                        # Is Trade Route Assigned
                        iColumn += 1
                        if (pLoopUnit.getGroup().isAssignedTradeRoute(self.iTradeRoute)):
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

        def updateCityFlash(self):
		screen = self.getScreen()
                iColor = gc.getInfoTypeForString("COLOR_GREEN")
                screen.minimapFlashPlot(self.pSourceCity.getX(), self.pSourceCity.getY(), iColor, -1)
                iColor = gc.getInfoTypeForString("COLOR_RED")
                screen.minimapFlashPlot(self.pDestinationCity.getX(), self.pDestinationCity.getY(), iColor, -1)
                return None

	def updateTransportFlash(self):
		screen = self.getScreen()
		iRows = screen.getTableNumRows(self.TABLE_ID)
		if (not screen.isRowSelected(self.TABLE_ID, iRows - 1)):
                        pTransport = None
                        for iRow in range(len(self.lTransports)):
                                if (screen.isRowSelected(self.TABLE_ID, iRow)):
                                        pTransport = self.lTransports[iRow]
                                        break
                        iColor = gc.getInfoTypeForString("COLOR_WHITE")
                        if (pTransport == None) and (len(self.lTransports) > 0):
                                pTransport = self.lTransports[0]
                        if (pTransport != None) and (not pTransport.isNone()):
                                screen.minimapFlashPlot(pTransport.getX(), pTransport.getY(), iColor, -1)
                return None

        #############################################################################################################

	def getText(self, sText, tArgs = (), iColor = gc.getInfoTypeForString("COLOR_FONT_CREAM")):
                #sText = u"%s" %(sText)
                try:
                        sText = oLocalText.getText(sText, tArgs)
                except:
                        pass
                sText = oLocalText.changeTextColor(sText, iColor)
                return sText

        #############################################################################################################

