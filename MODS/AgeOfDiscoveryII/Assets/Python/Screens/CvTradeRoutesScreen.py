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
oArtFileMgr = CyArtFileMgr()
oLocalText = CyTranslator()
oGameText = CyGameTextMgr()

oMap = CyMap()
oGame = CyGame()
oInterface = CyInterface()

alert = CvAlertManager.CvAlertManager()

utils = JTradeRoutesUtils.g_oUtils
############################################################################
			

class CvTradeRoutesScreen:
	"A Blank Civ4 Screen"
	
	def __init__(self):
		self.sWidgetPrefix = "TradeRoutesScreen"
		
		self.MANAGER_SCREEN_ID = self.sWidgetPrefix + "MainWindow"
		self.BACKGROUND_ID = self.sWidgetPrefix + "BackgroundImage"
		self.HEADER_PANEL_ID = self.sWidgetPrefix + "HeaderPanelWidget"
		self.FOOTER_PANEL_ID = self.sWidgetPrefix + "FooterPanelWidget"
		self.HEADER_ID = self.sWidgetPrefix + "HeaderTextWidget"
		self.EXIT_ID = self.sWidgetPrefix + "ExitTextWidget"

		self.TITLE = "TXT_KEY_SCREEN_TRADE_ROUTES_TITLE"

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
                self.FOOTER_TAB_ON_ID_PREFIX = self.sWidgetPrefix + "FooterTabOn_"
                self.FOOTER_TAB_OFF_ID_PREFIX = self.sWidgetPrefix + "FooterTabOff_"

                self.SCROLL_PANEL_ID = self.sWidgetPrefix + "ScrollPanel"
                self.TRADE_ROUTES_TABLE_PANEL_ID = self.sWidgetPrefix + "TradeRoutesTablePanel"
                self.TRADE_ROUTES_BUTTON_CREATE_ID = self.sWidgetPrefix + "TradeRoutesButtonCreate"
                self.TRADE_ROUTES_BUTTON_EDIT_ID = self.sWidgetPrefix + "TradeRoutesButtonEdit"
                self.TRADE_ROUTES_BUTTON_DELETE_ID = self.sWidgetPrefix + "TradeRoutesButtonDelete"
                self.TRADE_ROUTES_BUTTON_ASSIGN_ID = self.sWidgetPrefix + "TradeRoutesButtonAssign"
                self.TRADE_ROUTES_TABLE_ID = self.sWidgetPrefix + "TradeRoutesTable"

                self.COMMODITIES_TABLE_PANEL_ID = self.sWidgetPrefix + "CommoditiesTablePanel"
                self.YIELD_STORED_TOTAL_TABLE_ID = self.sWidgetPrefix + "YieldStoredTable"
                self.COMMODITIES_TABLE_ID = self.sWidgetPrefix + "CommoditiesTable"
                self.CITY_STORED_TOTAL_TABLE_ID = self.sWidgetPrefix + "CityStoredTable"

                self.TRANSPORTS_TABLE_PANEL_ID = self.sWidgetPrefix + "TransportsTablePanel"
                self.TRANSPORTS_LAND_TABLE_ID = self.sWidgetPrefix + "TransportsLandTable"
                self.TRANSPORTS_SEA_TABLE_ID = self.sWidgetPrefix + "TransportsSeaTable"
                self.TRANSPORTS_BUTTON_LAND_ASSIGN_ID = self.sWidgetPrefix + "TransportsButtonLandAssign"
                self.TRANSPORTS_BUTTON_SEA_ASSIGN_ID = self.sWidgetPrefix + "TransportsButtonSeaAssign"

                self.GRAPH_CHOOSE_YIELD_DROPDOWN_ID = self.sWidgetPrefix + "GraphChooseYieldDropdown"
                self.GRAPH_CHOOSE_GRAPH_DROPDOWN_ID = self.sWidgetPrefix + "GraphChooseGraphDropdown"
                self.GRAPH_CHOOSE_GRAPH_INFO_DROPDOWN_ID = self.sWidgetPrefix + "GraphChooseGraphInfoDropdown"
                self.GRAPH_LEGEND_DRAW_CONTROL_ID = self.sWidgetPrefix + "GraphLegendDrawControl"
                self.GRAPH_LEGEND_PANEL_ID = self.sWidgetPrefix + "GraphLegendPanel"

                self.GRAPH_PANEL_ID = self.sWidgetPrefix + "GraphPanel"
                self.GRAPH_SCROLL_PANEL_ID = self.sWidgetPrefix + "GraphScrollPanel"
                self.GRAPH_DRAW_CONTROL_ID = self.sWidgetPrefix + "GraphDrawControl"
                self.GRAPH_PANEL_ID = self.sWidgetPrefix + "GraphPanel"
                self.GRAPH_X_TOP_BORDER_LINE_ID = self.sWidgetPrefix + "GraphXTopBorderLine"
                self.GRAPH_X_BOTTOM_BORDER_LINE_ID = self.sWidgetPrefix + "GraphXBottomBorderLine"
                self.GRAPH_Y_LEFT_BORDER_LINE_ID = self.sWidgetPrefix + "GraphYLeftBorderLine"
                self.GRAPH_Y_RIGHT_BORDER_LINE_ID = self.sWidgetPrefix + "GraphYRightBorderLine"
                self.GRAPH_X_LABEL_LEFT_ID = self.sWidgetPrefix + "GraphXLabelLeft"
                self.GRAPH_X_LABEL_RIGHT_ID = self.sWidgetPrefix + "GraphXLabelRight"
                return None

        def initValues(self):
                self.iTabID = 1111

                self.nLineCount = 0
                self.nTextCount = 0
                self.iButtonSize = 48
                self.iLastTab = 0
                self.iCurrentTab = 0
		self.lTabNames = []
		self.lTabNames += ["TXT_KEY_SCREEN_TAB_DOMESTIC_TRADE_ROUTES"]
		self.lTabNames += ["TXT_KEY_SCREEN_TAB_FOREIGN_TRADE_ROUTES"]
		self.lTabNames += ["TXT_KEY_SCREEN_TAB_TRANSPORTS"]
		self.lTabNames += ["TXT_KEY_SCREEN_TAB_COMMODITIES"]
		self.lTabNames += ["TXT_KEY_SCREEN_TAB_GRAPHS"]
                self.iNumTabs = len(self.lTabNames)
                self.iRowHeight = 30
                self.iMargin = 10
                self.iBorder = 20
                self.iGraphColumnW = 60
                self.iGraphRowH = 46
                self.iGraphDiv = 20
		self.iGraphOffset = 30

                self.lYieldTypes = range(YieldTypes.YIELD_HAMMERS)
                self.iYieldCount = len(self.lYieldTypes)
                self.lYieldGraphStates = ([True] * (self.iYieldCount + 1))

                self.dGraphYieldDisplays = {}
                self.dGraphYieldDisplays[0] = "TXT_KEY_SCREEN_GRAPH_YIELDS_STORED"
                self.dGraphYieldDisplays[1] = "TXT_KEY_SCREEN_GRAPH_YIELD_RATES"

                self.dGraphYieldTypes = {0: range(YieldTypes.YIELD_HAMMERS),
                                         1: range(YieldTypes.NUM_YIELD_TYPES)}
                self.dGraphYieldCount = {0: len(range(YieldTypes.YIELD_HAMMERS)),
                                         1: len(range(YieldTypes.NUM_YIELD_TYPES))}
                self.dGraphYieldDisplayDivs = {0: 1,
                                               1: 1}
                self.dGraphYieldDisplayOffsets = {0: 1.0,
                                                  1: 0.10}
                self.iGraphYieldDisplay = 0

                self.lTradeRoutes = []
                self.lTransportsLand = []
                self.lTransportsSea = []

                ###################################################

                self.X_TRADE_ROUTES_SCROLL_PANEL = self.X_SCREEN
                self.Y_TRADE_ROUTES_SCROLL_PANEL = self.Y_SCREEN + self.H_BAR - 10
                self.W_TRADE_ROUTES_SCROLL_PANEL = self.W_SCREEN + 10
                self.H_TRADE_ROUTES_SCROLL_PANEL = self.H_SCREEN - (self.H_BAR * 2) + 10

                self.X_TRADE_ROUTES_PANEL = self.X_SCREEN
                self.Y_TRADE_ROUTES_PANEL = self.Y_SCREEN# + self.H_BAR - 10
                self.W_TRADE_ROUTES_PANEL = self.W_SCREEN - 10
                self.H_TRADE_ROUTES_PANEL = self.H_SCREEN - (self.H_BAR * 2)
                
                self.X_TRADE_ROUTES_TABLE = self.X_TRADE_ROUTES_PANEL + 38
                self.Y_TRADE_ROUTES_TABLE = self.Y_TRADE_ROUTES_PANEL + 84
                self.W_TRADE_ROUTES_TABLE = self.W_TRADE_ROUTES_PANEL - 60
                self.H_TRADE_ROUTES_TABLE = self.H_TRADE_ROUTES_PANEL - 60

                iSpace = 200
                self.Y_TRADE_ROUTES_BUTTONS = self.Y_TRADE_ROUTES_SCROLL_PANEL + self.iMargin
                self.X_TRADE_ROUTES_BUTTON_CREATE = self.X_TRADE_ROUTES_TABLE
                self.X_TRADE_ROUTES_BUTTON_EDIT = self.X_TRADE_ROUTES_BUTTON_CREATE + iSpace
                self.X_TRADE_ROUTES_BUTTON_DELETE = self.X_TRADE_ROUTES_BUTTON_EDIT + iSpace
                self.X_TRADE_ROUTES_BUTTON_ASSIGN = self.X_TRADE_ROUTES_BUTTON_DELETE + iSpace + 120

                ###################################################

                self.X_YIELD_STORED_TOTAL_TABLE = self.X_TRADE_ROUTES_PANEL + 38
                self.Y_YIELD_STORED_TOTAL_TABLE = self.Y_TRADE_ROUTES_PANEL + 84
                self.W_YIELD_STORED_TOTAL_TABLE = self.W_TRADE_ROUTES_PANEL - 60 - 60
                self.H_YIELD_STORED_TOTAL_TABLE = (self.iRowHeight * 1) + 24

                self.X_COMMODITIES_TABLE = self.X_YIELD_STORED_TOTAL_TABLE
                self.Y_COMMODITIES_TABLE = self.Y_YIELD_STORED_TOTAL_TABLE + self.H_YIELD_STORED_TOTAL_TABLE + self.iBorder
                self.W_COMMODITIES_TABLE = self.W_YIELD_STORED_TOTAL_TABLE
                self.H_COMMODITIES_TABLE = (self.H_TRADE_ROUTES_PANEL + 24) - self.Y_COMMODITIES_TABLE

                self.X_CITY_STORED_TOTAL_TABLE = self.X_COMMODITIES_TABLE + self.W_COMMODITIES_TABLE + self.iBorder
                self.Y_CITY_STORED_TOTAL_TABLE = self.Y_COMMODITIES_TABLE
                self.W_CITY_STORED_TOTAL_TABLE = 50
                self.H_CITY_STORED_TOTAL_TABLE = self.H_COMMODITIES_TABLE

                ###################################################

                self.X_TRANSPORTS_LAND_TABLE = self.X_TRADE_ROUTES_PANEL + 38
                self.Y_TRANSPORTS_LAND_TABLE = self.Y_TRADE_ROUTES_PANEL + 84
                self.W_TRANSPORTS_LAND_TABLE = self.W_TRADE_ROUTES_PANEL - 60
                self.H_TRANSPORTS_LAND_TABLE = (self.H_TRADE_ROUTES_PANEL - (self.X_TRANSPORTS_LAND_TABLE * 2) - self.iBorder) / 2

                self.X_TRANSPORTS_SEA_TABLE = self.X_TRANSPORTS_LAND_TABLE
                self.Y_TRANSPORTS_SEA_TABLE = self.Y_TRANSPORTS_LAND_TABLE + self.H_TRANSPORTS_LAND_TABLE + self.iBorder
                self.W_TRANSPORTS_SEA_TABLE = self.W_TRANSPORTS_LAND_TABLE
                self.H_TRANSPORTS_SEA_TABLE = self.H_TRANSPORTS_LAND_TABLE + 16

                self.X_TRANSPORTS_BUTTON_LAND_ASSIGN = self.X_TRADE_ROUTES_BUTTON_CREATE + iSpace + iSpace
                self.X_TRANSPORTS_BUTTON_SEA_ASSIGN = self.X_TRANSPORTS_BUTTON_LAND_ASSIGN + iSpace + 100

                ###################################################

                self.X_GRAPH_DROPDOWN = self.X_SCREEN + 20
                self.W_GRAPH_DROPDOWN = 200

                self.Y_GRAPH_CHOOSE_YIELD_DROPDOWN = self.Y_SCREEN + self.H_BAR + (self.iBorder * 2)
                self.Y_GRAPH_CHOOSE_GRAPH_DROPDOWN = self.Y_GRAPH_CHOOSE_YIELD_DROPDOWN + 40
                self.Y_GRAPH_CHOOSE_GRAPH_INFO_DROPDOWN = self.Y_GRAPH_CHOOSE_GRAPH_DROPDOWN + 40

                self.W_GRAPH_LEGEND_LINE = 50
                self.H_GRAPH_LEGEND_ROW = 20
                self.H_GRAPH_LEGEND = self.dGraphYieldCount[self.iGraphYieldDisplay] * self.H_GRAPH_LEGEND_ROW

                self.X_GRAPH_LEGEND = self.X_SCREEN + 20
                self.Y_GRAPH_LEGEND = (self.H_SCREEN - self.H_BAR - self.iBorder) - self.H_GRAPH_LEGEND
                self.W_GRAPH_LEGEND = 200

                self.X_GRAPH_SCROLL_PANEL = self.X_GRAPH_DROPDOWN + self.W_GRAPH_DROPDOWN + self.iBorder + self.iMargin
                self.Y_GRAPH_SCROLL_PANEL = self.Y_GRAPH_CHOOSE_YIELD_DROPDOWN - 16
                self.W_GRAPH_SCROLL_PANEL = self.W_SCREEN - (self.X_GRAPH_SCROLL_PANEL + self.iBorder)
                self.H_GRAPH_SCROLL_PANEL = self.H_SCREEN - (self.Y_GRAPH_SCROLL_PANEL + self.H_BAR + self.iBorder) + 2

                self.X_GRAPH_PANEL = 0
                self.Y_GRAPH_PANEL = 0
                self.W_GRAPH_PANEL_MIN = self.W_SCREEN - (self.X_GRAPH_LEGEND + self.W_GRAPH_LEGEND) - 70

                self.W_GRAPH_PANEL = ((oGame.getGameTurn() - oGame.getStartTurn()) * self.iGraphColumnW) + (self.iBorder * 3)#self.W_GRAPH_CANVAS + 1000
                self.W_GRAPH_PANEL = max(0, self.W_GRAPH_PANEL)
                self.W_GRAPH_PANEL = max(self.W_GRAPH_PANEL_MIN, self.W_GRAPH_PANEL)

                self.H_GRAPH_PANEL = self.H_GRAPH_SCROLL_PANEL - self.iMargin

                self.X_GRAPH_CANVAS = 0
                self.Y_GRAPH_CANVAS = 0
                self.W_GRAPH_CANVAS = self.W_GRAPH_PANEL
                self.H_GRAPH_CANVAS = self.H_GRAPH_PANEL - self.iBorder

                self.X_GRAPH_LEFT = 0 + self.iMargin#(self.iBorder * 2)
                self.X_GRAPH_RIGHT = self.W_GRAPH_CANVAS - self.iMargin
                self.Y_GRAPH_TOP = 0 + self.iMargin
                self.Y_GRAPH_BOTTOM = self.H_GRAPH_CANVAS - self.iMargin
		return None
				
        #############################################################################################################

	def getScreen(self):
		return CyGInterfaceScreen(self.MANAGER_SCREEN_ID, CvScreenEnums.JTRADEROUTES_SCREEN)

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()
		return None

	def update(self, fDelta):
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
                # Graph Page - Choose Graph Yield Dropdown
		if (sFunctionName == self.GRAPH_CHOOSE_YIELD_DROPDOWN_ID):
                        iID = screen.getSelectedPullDownID(self.GRAPH_CHOOSE_YIELD_DROPDOWN_ID)
                        if (iID == 0):
                                self.lYieldGraphStates = ([True] * (self.dGraphYieldCount[self.iGraphYieldDisplay] + 1))#(self.iYieldCount + 1))
                        else:
                                self.lYieldGraphStates = ([False] * (self.dGraphYieldCount[self.iGraphYieldDisplay] + 1))#(self.iYieldCount + 1))
                                self.lYieldGraphStates[iID] = True
                        self.updateGraph()
                        return 1
                # Graph Page - Choose Graph Dropdown
		elif (sFunctionName == self.GRAPH_CHOOSE_GRAPH_DROPDOWN_ID):
                        self.iGraphYieldDisplay = screen.getSelectedPullDownID(self.GRAPH_CHOOSE_GRAPH_DROPDOWN_ID)
                        iID = screen.getSelectedPullDownID(self.GRAPH_CHOOSE_YIELD_DROPDOWN_ID)
                        if (iID == 0):
                                lNewStates = ([True] * (self.dGraphYieldCount[self.iGraphYieldDisplay] + 1))
                        else:
                                lNewStates = ([False] * (self.dGraphYieldCount[self.iGraphYieldDisplay] + 1))
                        iNewStates = len(lNewStates)
                        iStates = len(self.lYieldGraphStates)
                        for i in range(iStates):
                                if (i >= iNewStates):
                                        break
                                lNewStates[i] = self.lYieldGraphStates[i]
                        self.lYieldGraphStates = lNewStates
                        self.updateGraph()
                        return 1
                # Graph Page - Choose Graph Info Dropdown
		elif (sFunctionName == self.GRAPH_CHOOSE_GRAPH_INFO_DROPDOWN_ID):
                        self.updateGraph()
                        return 1
                # Any Page - Create Trade Route
		elif (sFunctionName == self.TRADE_ROUTES_BUTTON_CREATE_ID):
                        if (gc.getActivePlayer().getNumCities() > 0):
                                utils.createTradeRouteBegin(oGame.getActivePlayer(), self.W_SCREEN, self.H_SCREEN,
                                                            (self.MANAGER_SCREEN_ID, CvScreenEnums.JTRADEROUTES_SCREEN))
                        return 1
                # Trade Routes Page - Edit Trade Route
		elif (sFunctionName == self.TRADE_ROUTES_BUTTON_EDIT_ID):
                        iTradeRoute = self.getSelectedTradeRoute()
                        """for iRow in range(len(self.lTradeRoutes)):
                                if (screen.isRowSelected(self.TRADE_ROUTES_TABLE_ID, iRow)):
                                        iTradeRoute = self.lTradeRoutes[iRow]
                                        break
                        if (iTradeRoute < 0) and (len(self.lTradeRoutes) > 0):
                                iTradeRoute = self.lTradeRoutes[0]"""
                        if (iTradeRoute > -1):
                                utils.editTradeRouteBegin(oGame.getActivePlayer(), iTradeRoute,
                                                          self.W_SCREEN, self.H_SCREEN,
                                                          (self.MANAGER_SCREEN_ID, CvScreenEnums.JTRADEROUTES_SCREEN))
                        return 1
                # Trade Routes Page - Delete Trade Route
		elif (sFunctionName == self.TRADE_ROUTES_BUTTON_DELETE_ID):
                        iTradeRoute = self.getSelectedTradeRoute()
                        """for iRow in range(len(self.lTradeRoutes)):
                                if (screen.isRowSelected(self.TRADE_ROUTES_TABLE_ID, iRow)):
                                        iTradeRoute = self.lTradeRoutes[iRow]
                                        break
                        if (iTradeRoute < 0) and (len(self.lTradeRoutes) > 0):
                                iTradeRoute = self.lTradeRoutes[0]"""
                        if (iTradeRoute > -1):
                                utils.deleteTradeRouteBegin(oGame.getActivePlayer(), iTradeRoute,
                                                            self.W_SCREEN, self.H_SCREEN,
                                                            (self.MANAGER_SCREEN_ID, CvScreenEnums.JTRADEROUTES_SCREEN))
                        return 1
                # Trade Routes Page - Assign Units To Trade Route
		elif (sFunctionName == self.TRADE_ROUTES_BUTTON_ASSIGN_ID):
                        iTradeRoute = self.getSelectedTradeRoute()
                        """for iRow in range(len(self.lTradeRoutes)):
                                if (screen.isRowSelected(self.TRADE_ROUTES_TABLE_ID, iRow)):
                                        iTradeRoute = self.lTradeRoutes[iRow]
                                        break
                        if (iTradeRoute < 0) and (len(self.lTradeRoutes) > 0):
                                iTradeRoute = self.lTradeRoutes[0]"""
                        if (iTradeRoute > -1):
                                CvScreensInterface.showAssignUnitsToTradeRoutePopup(oGame.getActivePlayer(), iTradeRoute,
                                                                                    True, self.iCurrentTab)
                                """utils.assignTradeRouteBegin(oGame.getActivePlayer(), iTradeRoute,
                                                    (self.MANAGER_SCREEN_ID, CvScreenEnums.JTRADEROUTES_SCREEN))"""
                        return 1
                # Transports Page - Assign Trade Routes To Land Unit
		elif (sFunctionName == self.TRANSPORTS_BUTTON_LAND_ASSIGN_ID):
                        iUnit = -1
                        for iRow in range(len(self.lTransportsLand)):
                                if (screen.isRowSelected(self.TRANSPORTS_LAND_TABLE_ID, iRow)):
                                        iUnit = self.lTransportsLand[iRow]
                                        break
                        if (iUnit < 0) and (len(self.lTransportsLand) > 0):
                                iUnit = self.lTransportsLand[0]
                        if (iUnit > -1):
                                CvScreensInterface.showAssignTradeRoutesToUnitPopup(oGame.getActivePlayer(), iUnit,
                                                                                    True, self.iCurrentTab)
                        return 1
                # Transports Page - Assign Trade Routes To Sea Unit
		elif (sFunctionName == self.TRANSPORTS_BUTTON_SEA_ASSIGN_ID):
                        iUnit = -1
                        for iRow in range(len(self.lTransportsSea)):
                                if (screen.isRowSelected(self.TRANSPORTS_SEA_TABLE_ID, iRow)):
                                        iUnit = self.lTransportsSea[iRow]
                                        break
                        if (iUnit < 0) and (len(self.lTransportsSea) > 0):
                                iUnit = self.lTransportsSea[0]
                        if (iUnit > -1):
                                CvScreensInterface.showAssignTradeRoutesToUnitPopup(oGame.getActivePlayer(), iUnit,
                                                                                    True, self.iCurrentTab)
                        return 1
                # Graph Page - Legend Yield Text
                elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL) and (iData1 == 2222):
                        self.lYieldGraphStates[iData2 + 1] = (not self.lYieldGraphStates[iData2 + 1])
                        self.updateGraph()
                        return 1
                # Trade Routes Page - Trade Route Name
                elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL) and (iData1 == 3333):
                        return 1
                # Screen Footer Tabs
		if(iNotifyCode == iNotifyClicked):
                        sInputName = inputClass.getFunctionName()
                        #alert.alert(0, sInputName)
                        if (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL) and (iData1 == self.iTabID):
				iCurrentTab = inputClass.getData2()
				return self.updateContent(iCurrentTab)
		return 0

	# Adds Mouse Over Help to General Widgets
	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList

                if (iData1 == utils.iButtonExit):
			return utils.getText("TXT_KEY_INTERFACE_BUTTON_HELP_EXIT", iColor = -1)
		elif (iData1 == utils.iButtonCreateTradeRouteID):
			return utils.getText("TXT_KEY_INTERFACE_BUTTON_HELP_TRADE_ROUTE_CREATE", iColor = -1)
		elif (iData1 == utils.iButtonEditTradeRouteID):
			return utils.getText("TXT_KEY_INTERFACE_BUTTON_HELP_TRADE_ROUTE_EDIT", iColor = -1)
		elif (iData1 == utils.iButtonDeleteTradeRouteID):
			return utils.getText("TXT_KEY_INTERFACE_BUTTON_HELP_TRADE_ROUTE_DELETE", iColor = -1)
		elif (iData1 == utils.iButtonAssignToTradeRouteID):
			return utils.getText("TXT_KEY_INTERFACE_BUTTON_HELP_ASSIGN_UNITS_TO_TRADE_ROUTE", iColor = -1)
		elif (iData1 == utils.iButtonAssignToLandUnitID):
			return utils.getText("TXT_KEY_INTERFACE_BUTTON_HELP_ASSIGN_TRADE_ROUTES_TO_LAND_UNIT", iColor = -1)
		elif (iData1 == utils.iButtonAssignToSeaUnitID):
			return utils.getText("TXT_KEY_INTERFACE_BUTTON_HELP_ASSIGN_TRADE_ROUTES_TO_SEA_UNIT", iColor = -1)
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
                                tArgs = (oGameText.getSpecificUnitHelp(pTransport, False, False), )
                                sText += utils.getText("TXT_KEY_INTERFACE_TRANSPORT_HELP", tArgs, iColor = -1)
			return unicode(sText)
		elif (iData1 == utils.iTableTransports):
                        sText = u""
                        lTradeRoutes = utils.getPlayerTradeRoutes(oGame.getActivePlayer())
                        iTradeRoutes = len(lTradeRoutes)
                        pTransport = gc.getActivePlayer().getUnit(iData2)
                        bFound = False
                        sText += utils.getText("TXT_KEY_INTERFACE_ASSIGNED_TRADE_ROUTES_HELP_TITLE", iColor = -1)
                        for iIndex in range(iTradeRoutes):
                                pTradeRoute = lTradeRoutes[iIndex]
                                if (not pTransport.getGroup().isAssignedTradeRoute(pTradeRoute.getID())):
                                        continue
                                if (not bFound):
                                        bFound = True
                                sText += u"\n"
                                sYield = u"%c" %(gc.getYieldInfo(pTradeRoute.getYield()).getChar())
                                tArgs = (utils.getTradeRouteName(pTradeRoute), sYield)
                                iColor = -1
                                sText += utils.getText("TXT_KEY_INTERFACE_TRADE_ROUTE_HELP", tArgs, iColor)
                        if (not bFound):
                                sText = utils.getText("TXT_KEY_INTERFACE_NO_ASSIGNED_TRADE_ROUTES_HELP_TITLE", iColor = -1)
			return unicode(sText)
		elif (iData1 == utils.iTableCommodities) or (iData1 == utils.iTableCommoditiesTotalCity):
                        sText = u""
                        pCity = gc.getActivePlayer().getCity(iData2)
                        sText += pCity.getName()
                        for iYield in range(YieldTypes.YIELD_HAMMERS):
                                pYield = gc.getYieldInfo(iYield)
                                sText += u"  "
                                sText += u"%d%c" %(pCity.getYieldRate(iYield), pYield.getChar())
                        return unicode(sText)
		elif (iData1 == utils.iTableCommoditiesTotalYield):
                        sText = u""
                        pYield = gc.getYieldInfo(iData2)
                        sText += pYield.getDescription()
                        lCities = utils.getPlayerCities(oGame.getActivePlayer())
                        iTotal = 0
                        for pCity in lCities:
                                iTotal += pCity.getYieldRate(iData2)
                        sText += u"  %d%c" %(iTotal, pYield.getChar())
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

	def getNextLineName(self):
		szName = self.sWidgetPrefix + "Line" + str(self.nLineCount)
		self.nLineCount += 1
		return szName

	def deleteAllLines(self):
		screen = self.getScreen()
		i = self.nLineCount - 1
		while (i >= 0):
			self.nLineCount = i
			screen.removeLineGFC(self.GRAPH_DRAW_CONTROL_ID, self.getNextLineName())
			i -= 1

		self.nLineCount = 0
		return None

	def getNextTextName(self):
		szName = self.sWidgetPrefix + "Text" + str(self.nTextCount)
		self.nTextCount += 1
		return szName

	def deleteAllTexts(self):
		screen = self.getScreen()
		i = self.nTextCount - 1
		while (i >= 0):
			self.nTextCount = i
			screen.deleteWidget(self.getNextTextName())
			i -= 1

		self.nTextCount = 0
		return None
				
        #############################################################################################################

	# Screen construction function
	def interfaceScreen(self, iTab = 0):
		screen = self.getScreen()
		if (screen.isActive()):
			return None
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		#screen.setDimensions(self.X_SCREEN, self.Y_SCREEN, self.W_SCREEN, self.H_SCREEN)
			
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.showWindowBackground(True)

		self.initValues()
		#self.iCurrentTab = iTab

		iX = 0
		iY = 0

		# Set the background widget
		try:
                        sBackgroundArtPath = oArtFileMgr.getInterfaceArtInfo("SCREEN_WEATHER_PATTERNS_LIGHNING_STRIKE").getPath()
                except:
                        sBackgroundArtPath = oArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath()
		#screen.addDDSGFC(self.BACKGROUND_ID, sBackgroundArtPath, iX, iY, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
                screen.addDrawControl(self.BACKGROUND_ID,
                                      oArtFileMgr.getInterfaceArtInfo("FATHER_BG").getPath(),
                                      self.X_SCREEN, self.Y_SCREEN,
                                      self.W_SCREEN, self.H_SCREEN,
                                      WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.drawHeader()
		#self.drawFooter()
		self.drawTabFooter()
		self.drawHelpTextArea()

		#self.drawTradeRoutes()
		self.updateContent(iTab)

		sArtPath = oArtFileMgr.getInterfaceArtInfo("INTERFACE_DOMESTIC_ADVISOR").getPath()
		iSize = 48
		iX = self.X_TRADE_ROUTES_TABLE - (iSize / 2)
		iY = (self.H_BAR / 2) - (iSize / 2)
                screen.setImageButton("DomesticAdvisorButton", sArtPath,
                                      iX, iY,
                                      iSize, iSize,
                                      WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_DOMESTIC_SCREEN).getActionInfoIndex(), -1)
                screen.setImageShape("DomesticAdvisorButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
                screen.setHitMargins("DomesticAdvisorButton", iSize / 6, iSize / 6)

        #############################################################################################################

        def drawHelpTextArea(self):
		screen = self.getScreen()
                iWMin = 200
                iWMax = 1000
                iX = 80
                iY = 0
                screen.setHelpTextArea(iWMax,
                                       FontTypes.SMALL_FONT,
                                       iX, iY, -0.1,
                                       True, "", True, True,
                                       CvUtil.FONT_RIGHT_JUSTIFY, iWMin)
                return None

        #############################################################################################################

        def drawHeader(self):
		screen = self.getScreen()
		iX = 0
		iY = 0
		screen.addDDSGFC(self.HEADER_PANEL_ID,
                                 oArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TITLE").getPath(),
                                 self.X_SCREEN, self.Y_SCREEN,
                                 self.W_SCREEN, self.H_BAR,
                                 WidgetTypes.WIDGET_GENERAL, -1, -1)
		#sTitle = oLocalText.changeTextColor(self.TITLE, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		sTitle = u"<font=4b>%s</font>" %(utils.getText(self.TITLE))
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
		sText = u"<font=4>%s</font>" %(utils.getText("TXT_KEY_PEDIA_SCREEN_EXIT", iColor = -1))
		screen.setText(self.EXIT_ID, self.BACKGROUND_ID, sText,
                               CvUtil.FONT_RIGHT_JUSTIFY,
                               self.W_SCREEN - 30, self.H_SCREEN - 40,
                               self.Z_CONTROLS,
                               FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN,
                               utils.iButtonExit, -1)
		screen.setFocus(self.EXIT_ID)
		return None

        def drawTabFooter(self):
		screen = self.getScreen()
		
                self.drawTabs()
                self.setTabState(self.iCurrentTab, True)
		return None
				
        #############################################################################################################

        def drawTabs(self):
                screen = self.getScreen()

		iExitTabWidth = 130
		iTabWidth = (self.W_SCREEN - (iExitTabWidth * 9 / 10)) / self.iNumTabs

		for iTab in range(self.iNumTabs):
			sNameTabOn = self.FOOTER_TAB_ON_ID_PREFIX + str(iTab)
			iEdgeWidth = 25
			screen.addPanel(sNameTabOn + "Left", "", "", False, False, iTabWidth * iTab, self.H_SCREEN - self.H_BAR, iEdgeWidth, self.H_BAR, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addPanel(sNameTabOn + "Center", "", "", False, False, (iTabWidth * iTab) + iEdgeWidth, self.H_SCREEN - self.H_BAR, iTabWidth - (iEdgeWidth * 2), self.H_BAR, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addPanel(sNameTabOn + "Right", "", "", False, False, (iTabWidth * iTab) + iTabWidth - iEdgeWidth, self.H_SCREEN - self.H_BAR, iEdgeWidth, self.H_BAR, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)

			screen.addDrawControl(sNameTabOn + "Left", oArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_START").getPath(), iTabWidth * iTab, self.H_SCREEN - self.H_BAR, iEdgeWidth, self.H_BAR, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addDrawControl(sNameTabOn + "Center", oArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_ON").getPath(), (iTabWidth * iTab) + iEdgeWidth, self.H_SCREEN - self.H_BAR, iTabWidth - (iEdgeWidth * 2), self.H_BAR, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addDrawControl(sNameTabOn + "Right", oArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_END").getPath(), (iTabWidth * iTab) + iTabWidth - iEdgeWidth, self.H_SCREEN - self.H_BAR, iEdgeWidth, self.H_BAR, WidgetTypes.WIDGET_GENERAL, -1, -1)

			sTabText = u"<font=3>%s</font>" %(utils.getText(self.lTabNames[iTab]))
			#sTabText = oLocalText.changeTextColor(sTabText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))

                        iX = 65 - 50
                        iY = 33
			screen.setLabelAt("OnTabTitle" + str(iTab), sNameTabOn + "Center",
                                          sTabText,
                                          CvUtil.FONT_LEFT_JUSTIFY,
                                          iX, iY,
                                          0,
                                          FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.hide(sNameTabOn + "Left")
			screen.hide(sNameTabOn + "Center")
			screen.hide(sNameTabOn + "Right")

			OffTabName = "OffTab" + str(iTab)
			screen.addPanel(OffTabName, "", "", False, False, iTabWidth * iTab, self.H_SCREEN - self.H_BAR, iTabWidth, self.H_BAR, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, self.iTabID, iTab)
			screen.addDrawControl(OffTabName, oArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_OFF").getPath(), iTabWidth * iTab, self.H_SCREEN - self.H_BAR, iTabWidth, self.H_BAR, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setTextAt("OffTabTitle" + str(iTab), OffTabName,
                                         sTabText,
                                         CvUtil.FONT_LEFT_JUSTIFY,
                                         iEdgeWidth + iX, iY,
                                         0,
                                         FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.iTabID, iTab)

		screen.addPanel("ExitTab", "", "", False, False, self.W_SCREEN - iExitTabWidth, self.H_SCREEN - self.H_BAR, iExitTabWidth, self.H_BAR, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addDrawControl("ExitTab", oArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_OFF").getPath(), self.W_SCREEN - iExitTabWidth, self.H_SCREEN - self.H_BAR, iExitTabWidth, self.H_BAR, WidgetTypes.WIDGET_GENERAL, -1, -1)
		sText = u"<font=4>%s</font>" %(utils.getText("TXT_KEY_PEDIA_SCREEN_EXIT", iColor = -1).upper())
		screen.setTextAt("ExitTabTitle", "ExitTab", sText, CvUtil.FONT_RIGHT_JUSTIFY,
                                 iExitTabWidth - 20, self.H_BAR - 18, 0, FontTypes.TITLE_FONT,
                                 WidgetTypes.WIDGET_CLOSE_SCREEN, utils.iButtonExit, -1)
		return None

	def setTabState(self, iTab, State):
		screen = self.getScreen()
		sNameTabOn = self.FOOTER_TAB_ON_ID_PREFIX + str(iTab)

		if (State):
			screen.show(sNameTabOn + "Left")
			screen.show(sNameTabOn + "Center")
			screen.show(sNameTabOn + "Right")
			screen.hide("OffTab" + str(iTab))
		else:
			screen.hide(sNameTabOn + "Left")
			screen.hide(sNameTabOn + "Center")
			screen.hide(sNameTabOn + "Right")
			screen.show("OffTab" + str(iTab))
		return None

        #############################################################################################################

	def updateContent(self, iCurrentTab):
		for iTab in range(self.iNumTabs):
                        if (iTab == iCurrentTab):
                                self.setTabState(iTab, True)
                        else:
                                self.setTabState(iTab, False)
                # Save the Last Selected Tab
                self.iLastTab = self.iCurrentTab
                # Clear the Last Displayed Page
                if (self.lTabNames[self.iLastTab] == "TXT_KEY_SCREEN_TAB_DOMESTIC_TRADE_ROUTES") \
                           or (self.lTabNames[self.iLastTab] == "TXT_KEY_SCREEN_TAB_FOREIGN_TRADE_ROUTES"):
                        self.clearTradeRoutes()
                elif (self.lTabNames[self.iLastTab] == "TXT_KEY_SCREEN_TAB_TRANSPORTS"):
                        self.clearTransports()
                elif (self.lTabNames[self.iLastTab] == "TXT_KEY_SCREEN_TAB_COMMODITIES"):
                        self.clearCommodities()
                elif (self.lTabNames[self.iLastTab] == "TXT_KEY_SCREEN_TAB_GRAPHS"):
                        self.clearGraph()
                                        
                # Set the new Current Selected Tab
                self.iCurrentTab = iCurrentTab
                # Draw the new Current Page
                if (self.lTabNames[iCurrentTab] == "TXT_KEY_SCREEN_TAB_DOMESTIC_TRADE_ROUTES") \
                                           or (self.lTabNames[iCurrentTab] == "TXT_KEY_SCREEN_TAB_FOREIGN_TRADE_ROUTES"):
                        self.drawTradeRoutes()
                elif (self.lTabNames[iCurrentTab] == "TXT_KEY_SCREEN_TAB_TRANSPORTS"):
                        self.drawTransports()
                elif (self.lTabNames[iCurrentTab] == "TXT_KEY_SCREEN_TAB_COMMODITIES"):
                        self.drawCommodities()
                elif (self.lTabNames[iCurrentTab] == "TXT_KEY_SCREEN_TAB_GRAPHS"):
                        self.drawGraph()
                self.drawCreateTradeRouteButton()
                return 1

        #############################################################################################################
        #############################################################################################################
	# Domestic and Foriegn Trade Routes Pages
        #############################################################################################################
        #############################################################################################################

	def drawTradeRoutes(self):
		self.drawTradeRoutesScrollPanel()
		self.updateTradeRoutes()
                return None

        def updateTradeRoutes(self):
		self.drawEditTradeRouteButton()
		self.drawDeleteTradeRouteButton()
		self.drawAssignTradeRouteButton()
                self.drawTradeRoutesPanel()
                self.drawTradeRoutesTable()
                self.drawTradeRoutesTableHeaders()
                self.fillTradeRoutesTable()
                return None

        def clearTradeRoutes(self):
                screen = self.getScreen()
                screen.deleteWidget(self.TRADE_ROUTES_TABLE_PANEL_ID)
                screen.deleteWidget(self.TRADE_ROUTES_TABLE_ID)
                screen.deleteWidget(self.TRADE_ROUTES_BUTTON_EDIT_ID)
                screen.deleteWidget(self.TRADE_ROUTES_BUTTON_DELETE_ID)
                screen.deleteWidget(self.TRADE_ROUTES_BUTTON_ASSIGN_ID)
                return None
				
        #############################################################################################################

	def drawTradeRoutesScrollPanel(self):
		screen = self.getScreen()
		screen.addScrollPanel(self.SCROLL_PANEL_ID, u"",
                                      self.X_TRADE_ROUTES_SCROLL_PANEL, self.Y_TRADE_ROUTES_SCROLL_PANEL,
                                      self.W_TRADE_ROUTES_SCROLL_PANEL, self.H_TRADE_ROUTES_SCROLL_PANEL,
                                      PanelStyles.PANEL_STYLE_EXTERNAL, True, WidgetTypes.WIDGET_GENERAL, -1, -1)
		return None
				
        #############################################################################################################

        def drawCreateTradeRouteButton(self):
		screen = self.getScreen()
                sText = u"<font=3b>%s</font>" %(utils.getText("TXT_KEY_SCREEN_BUTTON_CREATE_TRADE_ROUTE"))#("Create Trade Route")
                #sText = utils.getText(sText)
                screen.setText(self.TRADE_ROUTES_BUTTON_CREATE_ID, self.SCROLL_PANEL_ID,
                                 sText, CvUtil.FONT_LEFT_JUSTIFY,
                                 self.X_TRADE_ROUTES_BUTTON_CREATE, self.Y_TRADE_ROUTES_BUTTONS, 0,
                                 FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, utils.iButtonCreateTradeRouteID, -1)
		return None

        def drawEditTradeRouteButton(self):
		screen = self.getScreen()
                sText = u"<font=3b>%s</font>" %(utils.getText("TXT_KEY_SCREEN_BUTTON_EDIT_TRADE_ROUTE"))
                #sText = utils.getText(sText)
                screen.setText(self.TRADE_ROUTES_BUTTON_EDIT_ID, self.SCROLL_PANEL_ID,
                                 sText, CvUtil.FONT_LEFT_JUSTIFY,
                                 self.X_TRADE_ROUTES_BUTTON_EDIT, self.Y_TRADE_ROUTES_BUTTONS, 0,
                                 FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, utils.iButtonEditTradeRouteID, -1)
		return None

        def drawDeleteTradeRouteButton(self):
		screen = self.getScreen()
                sText = u"<font=3b>%s</font>" %(utils.getText("TXT_KEY_SCREEN_BUTTON_DELETE_TRADE_ROUTE"))
                #sText = utils.getText(sText)
                screen.setText(self.TRADE_ROUTES_BUTTON_DELETE_ID, self.SCROLL_PANEL_ID,
                                 sText, CvUtil.FONT_LEFT_JUSTIFY,
                                 self.X_TRADE_ROUTES_BUTTON_DELETE, self.Y_TRADE_ROUTES_BUTTONS, 0,
                                 FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, utils.iButtonDeleteTradeRouteID, -1)
		return None

        def drawAssignTradeRouteButton(self):
		screen = self.getScreen()
                sText = u"<font=3b>%s</font>" %(utils.getText("TXT_KEY_SCREEN_BUTTON_ASSIGN_UNITS_TO_TRADE_ROUTE"))
                sText = utils.getText(sText)
                screen.setText(self.TRADE_ROUTES_BUTTON_ASSIGN_ID, self.SCROLL_PANEL_ID,
                                 sText, CvUtil.FONT_LEFT_JUSTIFY,
                                 self.X_TRADE_ROUTES_BUTTON_ASSIGN, self.Y_TRADE_ROUTES_BUTTONS, 0,
                                 FontTypes.TITLE_FONT,
                               WidgetTypes.WIDGET_GENERAL, utils.iButtonAssignToTradeRouteID, -1)
		return None

	def drawTradeRoutesPanel(self):
		screen = self.getScreen()
		screen.attachPanelAt(self.SCROLL_PANEL_ID, self.TRADE_ROUTES_TABLE_PANEL_ID,
                                     u"", u"",
                                     True, True,
                                     PanelStyles.PANEL_STYLE_IN,#PANEL_STYLE_MAIN,#
                                     self.X_TRADE_ROUTES_PANEL, self.Y_TRADE_ROUTES_PANEL,
                                     self.W_TRADE_ROUTES_PANEL, self.H_TRADE_ROUTES_PANEL,
                                     WidgetTypes.WIDGET_GENERAL, -1, -1)
		return None

        def drawTradeRoutesTable(self):
		screen = self.getScreen()
                iColumns = 20
		screen.addTableControlGFC(self.TRADE_ROUTES_TABLE_ID,
                                          iColumns,
                                          self.X_TRADE_ROUTES_TABLE, self.Y_TRADE_ROUTES_TABLE,
                                          self.W_TRADE_ROUTES_TABLE, self.H_TRADE_ROUTES_TABLE,
                                          True, True,
                                          self.iButtonSize, self.iButtonSize,
                                          TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.TRADE_ROUTES_TABLE_ID, True)
		screen.enableSort(self.TRADE_ROUTES_TABLE_ID)
		screen.setStyle(self.TRADE_ROUTES_TABLE_ID, "Table_StandardCiv_Style")
		return None

        def drawTradeRoutesTableHeaders(self):
		screen = self.getScreen()
                iTotalWidth = 0
                iColumn = -1

                iColumn += 1
                iColumnWidth = 240
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_TRADE_ROUTE_NAME", iColor = -1))
		screen.setTableColumnHeader(self.TRADE_ROUTES_TABLE_ID,
                                            iColumn, sText, iColumnWidth)
                """iColumn += 1
                iColumnWidth = 70
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("Priority", (), -1))
		screen.setTableColumnHeader(self.TRADE_ROUTES_TABLE_ID,
                                            iColumn, sText, iColumnWidth)"""
                iColumn += 1
                iColumnWidth = 135
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SOURCE", iColor = -1))#(oLocalText.getText("TXT_KEY_SOURCE", ()))
		screen.setTableColumnHeader(self.TRADE_ROUTES_TABLE_ID,
                                            iColumn, sText, iColumnWidth)
                iColumn += 1
                iColumnWidth = 140
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_DESTINATION", iColor = -1))
		screen.setTableColumnHeader(self.TRADE_ROUTES_TABLE_ID,
                                            iColumn, sText, iColumnWidth)
                iColumn += 1
                iColumnWidth = 55
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_YIELD", iColor = -1))
		screen.setTableColumnHeader(self.TRADE_ROUTES_TABLE_ID,
                                            iColumn, sText, iColumnWidth)
                iColumn += 1
                iColumnWidth = 115
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_TRADE_ROUTE_SOURCE_STORAGE", iColor = -1))
		screen.setTableColumnHeader(self.TRADE_ROUTES_TABLE_ID,
                                            iColumn, sText, iColumnWidth)
                iColumn += 1
                iColumnWidth = 145
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_TRADE_ROUTE_DESTINATION_STORAGE", iColor = -1))
		screen.setTableColumnHeader(self.TRADE_ROUTES_TABLE_ID,
                                            iColumn, sText, iColumnWidth)
                iColumn += 1
                #iColumnWidth = 120#self.W_TRADE_ROUTES_TABLE - 290
                iColumnWidth = self.W_TRADE_ROUTES_TABLE - iTotalWidth
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN", iColor = -1))
		screen.setTableColumnHeader(self.TRADE_ROUTES_TABLE_ID,
                                            iColumn, sText, iColumnWidth)
		return None

	def fillTradeRoutesTable(self):
		#alert.alert(0, "fillTradeRoutesList")
		screen = self.getScreen()
		pPlayer = gc.getActivePlayer()
		iRow = -1

		lTradeRoutes = []

		for iTradeRoute in range(pPlayer.getNumTradeRoutes()):
                        pTradeRoute = pPlayer.getTradeRouteByIndex(iTradeRoute)

                        if (self.lTabNames[self.iCurrentTab] == "TXT_KEY_SCREEN_TAB_DOMESTIC_TRADE_ROUTES"):
                                if (pTradeRoute.isSourceEurope()) or (pTradeRoute.isDestinationEurope()):
                                        continue
                                pass
                        elif (self.lTabNames[self.iCurrentTab] == "TXT_KEY_SCREEN_TAB_FOREIGN_TRADE_ROUTES"):
                                if (not pTradeRoute.isSourceEurope()) and (not pTradeRoute.isDestinationEurope()):
                                        continue
                                pass
                        else:
                                continue
			pSourceCity = pPlayer.getCity(pTradeRoute.getSourceCity().iID)
			pDestinationCity = pPlayer.getCity(pTradeRoute.getDestinationCity().iID)
                        iRow += 1
                        screen.appendTableRow(self.TRADE_ROUTES_TABLE_ID)
                        screen.setTableRowHeight(self.TRADE_ROUTES_TABLE_ID, iRow, self.iRowHeight)
                        lTradeRoutes += [pTradeRoute.getID()]

			iColumn = -1

                        # Trade Route Name
			iColumn += 1
			sText = utils.getTradeRouteName(pTradeRoute)
			sText = utils.getText(sText)
			screen.setTableText(self.TRADE_ROUTES_TABLE_ID,
                                            iColumn, iRow,
                                            sText, "", WidgetTypes.WIDGET_GENERAL,
                                            utils.iTableTradeRoutes, pTradeRoute.getID(), CvUtil.FONT_LEFT_JUSTIFY)

                        """# Trade Route Priority
			iColumn += 1
			sText = "%d" %(pTradeRoute.getPriority())
			sText = utils.getText(sText)
                        screen.setTableInt(self.TRADE_ROUTES_TABLE_ID,
                                           iColumn, iRow,
                                           sText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)"""

                        # Source City Name
			iColumn += 1
			sText = pTradeRoute.getSourceCityName()
			sText = utils.getText(sText)
			screen.setTableText(self.TRADE_ROUTES_TABLE_ID,
                                            iColumn, iRow,
                                            sText, "", WidgetTypes.WIDGET_GENERAL,
                                            utils.iTableTradeRoutes, pTradeRoute.getID(), CvUtil.FONT_LEFT_JUSTIFY)

                        # Destination City Name
			iColumn += 1
			sText = pTradeRoute.getDestinationCityName()
			sText = utils.getText(sText)
			screen.setTableText(self.TRADE_ROUTES_TABLE_ID,
                                            iColumn, iRow,
                                            sText, "", WidgetTypes.WIDGET_GENERAL,
                                            utils.iTableTradeRoutes, pTradeRoute.getID(), CvUtil.FONT_LEFT_JUSTIFY)

			# Cargo Yeild Icon
			iColumn += 1
			sText = u"<font=3>%c</font>" %(gc.getYieldInfo(pTradeRoute.getYield()).getChar())
			sText = utils.getText(sText)
			screen.setTableText(self.TRADE_ROUTES_TABLE_ID,
                                            iColumn, iRow,
                                            sText, "", WidgetTypes.WIDGET_GENERAL,
                                            utils.iTableTradeRoutes, pTradeRoute.getID(), CvUtil.FONT_LEFT_JUSTIFY)

                        # Source Cargo Amount
			iColumn += 1
			#if (pTradeRoute.getSourceCityID() == pTradeRoute.getEuropeCityID()):
			if (pTradeRoute.getSourceCity().iID == pTradeRoute.getEuropeCityID()):
                                sText = "N/A"
                                sText = utils.getText(sText)
                        else:
                                iYieldStored = pSourceCity.getYieldStored(pTradeRoute.getYield())
                                sTextL = u"<font=3>%d</font>" %(iYieldStored)
                                iMaxYield = pSourceCity.getMaxYieldCapacity()
                                if (iYieldStored >= iMaxYield):
                                        iColor = gc.getInfoTypeForString("COLOR_RED")
                                elif (iYieldStored >= iMaxYield / 2):
                                        iColor = gc.getInfoTypeForString("COLOR_YELLOW")
                                else:
                                        iColor = gc.getInfoTypeForString("COLOR_GREEN")
                                sTextL = utils.getText(sTextL, (), iColor)
                                sTextR = u"<font=3> (%d)</font>" %(iMaxYield)
                                sTextR = utils.getText(sTextR, ())
                                sText = sTextL + sTextR
                        screen.setTableInt(self.TRADE_ROUTES_TABLE_ID,
                                           iColumn, iRow,
                                           sText, "", WidgetTypes.WIDGET_GENERAL,
                                            utils.iTableTradeRoutes, pTradeRoute.getID(), CvUtil.FONT_LEFT_JUSTIFY)

                        # Destination Cargo Amount
			iColumn += 1
			#if (pTradeRoute.getDestinationCityID() == pTradeRoute.getEuropeCityID()):
			if (pTradeRoute.getDestinationCity().iID == pTradeRoute.getEuropeCityID()):
                                sText = "N/A"
                                sText = utils.getText(sText)
                        else:
                                iYieldStored = pDestinationCity.getYieldStored(pTradeRoute.getYield())
                                sTextL = u"<font=3>%d</font>" %(iYieldStored)
                                iMaxYield = pDestinationCity.getMaxYieldCapacity()
                                if (iYieldStored >= iMaxYield):
                                        iColor = gc.getInfoTypeForString("COLOR_RED")
                                elif (iYieldStored >= iMaxYield / 2):
                                        iColor = gc.getInfoTypeForString("COLOR_YELLOW")
                                else:
                                        iColor = gc.getInfoTypeForString("COLOR_GREEN")
                                sTextL = utils.getText(sTextL, (), iColor)
                                sTextR = u"<font=3> (%d)</font>" %(iMaxYield)
                                sTextR = utils.getText(sTextR, ())
                                sText = sTextL + sTextR
                        screen.setTableInt(self.TRADE_ROUTES_TABLE_ID,
                                           iColumn, iRow,
                                           sText, "", WidgetTypes.WIDGET_GENERAL,
                                            utils.iTableTradeRoutes, pTradeRoute.getID(), CvUtil.FONT_LEFT_JUSTIFY)

                        # Route Type
			iColumn += 1
			#pSourceArea = pSourceCity.area()
			#pDestinationArea = pDestinationCity.area()
			sLand = utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_LAND", iColor = -1)
			sSea = utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_SEA", iColor = -1)
			if (pTradeRoute.isLandRoute() and pTradeRoute.isSeaRoute()):
                                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_LAND_AND_SEA",
                                                                             (sLand, sSea)))
                        elif (pTradeRoute.isLandRoute()):
                                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_LAND"))
                        elif (pTradeRoute.isSeaRoute()):
                                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_TRADE_ROUTE_DOMAIN_SEA"))
                        else:
                                sText = u"<font=3>Unknown</font>"
                        #sText = utils.getText(sText)
                        screen.setTableText(self.TRADE_ROUTES_TABLE_ID,
                                            iColumn, iRow,
                                            sText, "",
                                            WidgetTypes.WIDGET_GENERAL,
                                            utils.iTableTradeRoutes, pTradeRoute.getID(), CvUtil.FONT_LEFT_JUSTIFY)
                self.lTradeRoutes = lTradeRoutes
		return None

        #############################################################################################################
        #############################################################################################################
	# Transports Page
        #############################################################################################################
        #############################################################################################################

	def drawTransports(self):
                self.drawTransportsPanel()
                self.updateTransports()
                return None

        def updateTransports(self):
                self.drawAssignTransportsLandButton()
                self.drawAssignTransportsSeaButton()
                self.drawTransportsLandTable()
                self.drawTransportsLandTableHeaders()
                self.fillTransportsLandTable()
                self.drawTransportsSeaTable()
                self.drawTransportsSeaTableHeaders()
                self.fillTransportsSeaTable()
                return None

	def clearTransports(self):
                screen = self.getScreen()
                screen.deleteWidget(self.TRANSPORTS_BUTTON_LAND_ASSIGN_ID)
                screen.deleteWidget(self.TRANSPORTS_BUTTON_SEA_ASSIGN_ID)
                screen.deleteWidget(self.TRANSPORTS_TABLE_PANEL_ID)
                screen.deleteWidget(self.TRANSPORTS_LAND_TABLE_ID)
                screen.deleteWidget(self.TRANSPORTS_SEA_TABLE_ID)
                return None

        #############################################################################################################

	def drawTransportsPanel(self):
		screen = self.getScreen()

		screen.attachPanelAt(self.SCROLL_PANEL_ID, self.TRANSPORTS_TABLE_PANEL_ID,
                                     u"", u"",
                                     True, True,
                                     PanelStyles.PANEL_STYLE_IN,#PANEL_STYLE_MAIN,#
                                     self.X_TRADE_ROUTES_PANEL, self.Y_TRADE_ROUTES_PANEL,
                                     self.W_TRADE_ROUTES_PANEL, self.H_TRADE_ROUTES_PANEL,
                                     WidgetTypes.WIDGET_GENERAL, -1, -1)
		return None

        #############################################################################################################

        def drawAssignTransportsLandButton(self):
		screen = self.getScreen()
                sText = u"<font=3b>%s</font>" %(utils.getText("TXT_KEY_SCREEN_BUTTON_ASSIGN_TRADE_ROUTES_TO_LAND_UNIT"))
                screen.setText(self.TRANSPORTS_BUTTON_LAND_ASSIGN_ID, self.SCROLL_PANEL_ID,
                                 sText, CvUtil.FONT_LEFT_JUSTIFY,
                                 self.X_TRANSPORTS_BUTTON_LAND_ASSIGN, self.Y_TRADE_ROUTES_BUTTONS, 0,
                                 FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL,
                               utils.iButtonAssignToLandUnitID, -1)
		return None

        def drawAssignTransportsSeaButton(self):
		screen = self.getScreen()
                sText = u"<font=3b>%s</font>" %(utils.getText("TXT_KEY_SCREEN_BUTTON_ASSIGN_UNITS_TRADE_ROUTES_TO_SEA_UNIT"))
                screen.setText(self.TRANSPORTS_BUTTON_SEA_ASSIGN_ID, self.SCROLL_PANEL_ID,
                                 sText, CvUtil.FONT_LEFT_JUSTIFY,
                                 self.X_TRANSPORTS_BUTTON_SEA_ASSIGN, self.Y_TRADE_ROUTES_BUTTONS, 0,
                                 FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL,
                               utils.iButtonAssignToSeaUnitID, -1)
		return None

        #############################################################################################################

        def drawTransportsLandTable(self):
		screen = self.getScreen()
		iColumns = 10
		screen.addTableControlGFC(self.TRANSPORTS_LAND_TABLE_ID,
                                          iColumns,
                                          self.X_TRANSPORTS_LAND_TABLE, self.Y_TRANSPORTS_LAND_TABLE,
                                          self.W_TRANSPORTS_LAND_TABLE, self.H_TRANSPORTS_LAND_TABLE,
                                          True, True,
                                          self.iButtonSize, self.iButtonSize,
                                          TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.TRANSPORTS_LAND_TABLE_ID, True)
		screen.enableSort(self.TRANSPORTS_LAND_TABLE_ID)
		screen.setStyle(self.TRANSPORTS_LAND_TABLE_ID, "Table_StandardCiv_Style")
		return None

	def drawTransportsLandTableHeaders(self):
		screen = self.getScreen()
		iTotalWidth = 0
                iColumn = -1

                iColumn += 1
                iColumnWidth = 58
                iTotalWidth += iColumnWidth
                sText = u""
                screen.setTableColumnHeader(self.TRANSPORTS_LAND_TABLE_ID, iColumn, sText, iColumnWidth)

                iColumn += 1
                iColumnWidth = 250
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SCREEN_UNIT_NAMES", iColor = -1))
                screen.setTableColumnHeader(self.TRANSPORTS_LAND_TABLE_ID, iColumn, sText, iColumnWidth)

                iColumn += 1
                iColumnWidth = 50
                iTotalWidth += iColumnWidth
                sText = u"<font=3> %c</font>" %(CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
                screen.setTableColumnHeader(self.TRANSPORTS_LAND_TABLE_ID, iColumn, sText, iColumnWidth)

                iColumn += 1
                iColumnWidth = 50
                iTotalWidth += iColumnWidth
                sText = u"<font=3> %c</font>" %(CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
                screen.setTableColumnHeader(self.TRANSPORTS_LAND_TABLE_ID, iColumn, sText, iColumnWidth)

                iColumn += 1
                iColumnWidth = 130
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SCREEN_UNIT_CARGO_SPACE", iColor = -1))
                screen.setTableColumnHeader(self.TRANSPORTS_LAND_TABLE_ID, iColumn, sText, iColumnWidth)

                iColumn += 1
                iColumnWidth = self.W_TRANSPORTS_LAND_TABLE - iTotalWidth
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SCREEN_UNIT_CURRENT_CARGO", iColor = -1))
                screen.setTableColumnHeader(self.TRANSPORTS_LAND_TABLE_ID, iColumn, sText, iColumnWidth)
		return None

	def fillTransportsLandTable(self):
		screen = self.getScreen()
                iRow = -1
                lUnits = utils.getPlayerUnits(oGame.getActivePlayer())
                lTransports = []
                for pLoopUnit in lUnits:
                        if (pLoopUnit.getDomainType() != gc.getInfoTypeForString("DOMAIN_LAND")) \
                           or (pLoopUnit.cargoSpace() < 1):
                                continue
                        iRow += 1
                        self.fillTransportsTableRow(self.TRANSPORTS_LAND_TABLE_ID, iRow, pLoopUnit)
                        lTransports += [pLoopUnit.getID()]
                self.lTransportsLand = lTransports
                return None

        #############################################################################################################

        def drawTransportsSeaTable(self):
		screen = self.getScreen()
		iColumns = 10
		screen.addTableControlGFC(self.TRANSPORTS_SEA_TABLE_ID,
                                          iColumns,
                                          self.X_TRANSPORTS_SEA_TABLE, self.Y_TRANSPORTS_SEA_TABLE,
                                          self.W_TRANSPORTS_SEA_TABLE, self.H_TRANSPORTS_SEA_TABLE,
                                          True, True,
                                          self.iButtonSize, self.iButtonSize,
                                          TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.TRANSPORTS_SEA_TABLE_ID, True)
		screen.enableSort(self.TRANSPORTS_SEA_TABLE_ID)
		screen.setStyle(self.TRANSPORTS_SEA_TABLE_ID, "Table_StandardCiv_Style")
		return None

	def drawTransportsSeaTableHeaders(self):
		screen = self.getScreen()
		iTotalWidth = 0
                iColumn = -1

                iColumn += 1
                iColumnWidth = 58
                iTotalWidth += iColumnWidth
                sText = u""
                screen.setTableColumnHeader(self.TRANSPORTS_SEA_TABLE_ID, iColumn, sText, iColumnWidth)

                iColumn += 1
                iColumnWidth = 250
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SCREEN_UNIT_NAMES", iColor = -1))
                screen.setTableColumnHeader(self.TRANSPORTS_SEA_TABLE_ID, iColumn, sText, iColumnWidth)

                iColumn += 1
                iColumnWidth = 50
                iTotalWidth += iColumnWidth
                sText = u"<font=3> %c</font>" %(CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
                screen.setTableColumnHeader(self.TRANSPORTS_SEA_TABLE_ID, iColumn, sText, iColumnWidth)

                iColumn += 1
                iColumnWidth = 50
                iTotalWidth += iColumnWidth
                sText = u"<font=3> %c</font>" %(CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
                screen.setTableColumnHeader(self.TRANSPORTS_SEA_TABLE_ID, iColumn, sText, iColumnWidth)

                iColumn += 1
                iColumnWidth = 130
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SCREEN_UNIT_CARGO_SPACE", iColor = -1))
                screen.setTableColumnHeader(self.TRANSPORTS_SEA_TABLE_ID, iColumn, sText, iColumnWidth)

                iColumn += 1
                iColumnWidth = self.W_TRANSPORTS_LAND_TABLE - iTotalWidth
                iTotalWidth += iColumnWidth
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SCREEN_UNIT_CURRENT_CARGO", iColor = -1))
                screen.setTableColumnHeader(self.TRANSPORTS_SEA_TABLE_ID, iColumn, sText, iColumnWidth)
		return None

	def fillTransportsSeaTable(self):
		screen = self.getScreen()
                iRow = -1
                lUnits = utils.getPlayerUnits(oGame.getActivePlayer())
                lTransports = []
                for pLoopUnit in lUnits:
                        if (pLoopUnit.getDomainType() != gc.getInfoTypeForString("DOMAIN_SEA")) \
                           or (pLoopUnit.cargoSpace() < 1):
                                continue
                        iRow += 1
                        self.fillTransportsTableRow(self.TRANSPORTS_SEA_TABLE_ID, iRow, pLoopUnit)
                        lTransports += [pLoopUnit.getID()]
                self.lTransportsSea = lTransports
                return None

        #############################################################################################################

        def fillTransportsTableRow(self, sTableName, iRow, pUnit):
                screen = self.getScreen()
                iColumn = -1
                screen.appendTableRow(sTableName)
                screen.setTableRowHeight(sTableName, iRow, self.iGraphRowH)

                # Unit's Button
                iColumn += 1
                sText = u""
                sArtPath = pUnit.getButton()
		screen.setTableText(sTableName, iColumn, iRow,
                                    sText, sArtPath,
                                    WidgetTypes.WIDGET_GENERAL,
                                    pUnit.getOwner(), pUnit.getID(),
                                    CvUtil.FONT_LEFT_JUSTIFY)
                # Unit's Name
                iColumn += 1
                sText = u"<font=3>%s" %(pUnit.getName())
                if (pUnit.plot().isCity()):
                        sText += u"  (%s)" %(pUnit.plot().getPlotCity().getName())
                elif (pUnit.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE):
                        sText += u"  (%s %s)" %(utils.getText("TXT_KEY_IN_PORT", (), -1), utils.getText("TXT_KEY_CONCEPT_EUROPE", (), -1))
                elif (pUnit.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_TO_EUROPE):
                        sText += u"  (%s %s)" %(utils.getText("TXT_KEY_IN_BOUND", (), -1), utils.getText("TXT_KEY_CONCEPT_EUROPE", (), -1))
                elif (pUnit.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE):
                        sText += u"  (%s %s)" %(utils.getText("TXT_KEY_OUTBOUND", (), -1), utils.getText("TXT_KEY_CONCEPT_EUROPE", (), -1))
                sText += u"</font>"
                sText = utils.getText(sText)
		screen.setTableText(sTableName, iColumn, iRow,
                                    sText, "",
                                    WidgetTypes.WIDGET_GENERAL,
                                    utils.iTableTransports, pUnit.getID(),
                                    CvUtil.FONT_LEFT_JUSTIFY)

                # Unit's Strength
                iColumn += 1
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SCREEN_NA"))
                if (pUnit.baseCombatStr() > 0):
                        fCurrent = utils.getUnitCurrentStrength(pUnit)
                        iBase = pUnit.baseCombatStr()
                        if (fCurrent == float(iBase)):
                                iColor = gc.getInfoTypeForString("COLOR_GREEN")
                        elif (fCurrent >= (float(iBase) / 2.0)):
                                iColor = gc.getInfoTypeForString("COLOR_YELLOW")
                        else:
                                iColor = gc.getInfoTypeForString("COLOR_RED")
                        sTextL = u"<font=3>%.1f</font>" %(fCurrent)
                        sTextR = u"<font=3>/%d</font>" %(iBase)
                        sText = utils.getText(sTextL, (), iColor) + utils.getText(sTextR)
		screen.setTableInt(sTableName, iColumn, iRow,
                                   sText, "",
                                   WidgetTypes.WIDGET_GENERAL,
                                   utils.iTableTransports, pUnit.getID(),
                                   CvUtil.FONT_LEFT_JUSTIFY)

                # Unit's Movement
                iColumn += 1
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SCREEN_NA"))
                if (pUnit.baseMoves() > 0):
                        iCurrent = utils.getUnitCurrentMoves(pUnit)
                        iBase = pUnit.baseMoves()
                        if (iCurrent == 0):
                                iColor = gc.getInfoTypeForString("COLOR_RED")
                        elif (iCurrent == iBase):
                                iColor = gc.getInfoTypeForString("COLOR_GREEN")
                        else:
                                iColor = gc.getInfoTypeForString("COLOR_YELLOW")
                        sTextL = u"<font=3>%d</font>" %(iCurrent)
                        sTextR = u"<font=3>/%d</font>" %(iBase)
                        sText = utils.getText(sTextL, (), iColor) + utils.getText(sTextR)
		screen.setTableInt(sTableName, iColumn, iRow,
                                   sText, "",
                                   WidgetTypes.WIDGET_GENERAL,
                                   utils.iTableTransports, pUnit.getID(),
                                   CvUtil.FONT_LEFT_JUSTIFY)

                # Unit's Cargo Space
                iColumn += 1
                iUsedCargo = pUnit.getCargo()
                iCargoSpace = pUnit.cargoSpace()
                iUsedCapacity = utils.getUnitUsedCapacity(pUnit)
                iCargoCapacity = oGame.getCargoYieldCapacity()
                iTotalCapacity = iCargoSpace * iCargoCapacity
                if (iUsedCargo == 0):
                        iColorA = gc.getInfoTypeForString("COLOR_GREEN")
                elif (iUsedCargo == iCargoSpace):
                        iColorA = gc.getInfoTypeForString("COLOR_RED")
                else:
                        iColorA = gc.getInfoTypeForString("COLOR_YELLOW")
                if (iUsedCapacity == 0):
                        iColorB = gc.getInfoTypeForString("COLOR_GREEN")
                elif (iUsedCapacity == iTotalCapacity):
                        iColorB = gc.getInfoTypeForString("COLOR_RED")
                else:
                        iColorB = gc.getInfoTypeForString("COLOR_YELLOW")
                sTextLA = u"<font=3>%d</font>" %(iUsedCargo)
                sTextRA = u"<font=3>/%d</font>" %(iCargoSpace)
                sTextLB = u"<font=3> (%d</font>" %(iUsedCapacity)
                sTextRB = u"<font=3>/%d)</font>" %(iTotalCapacity)
                sText = utils.getText(sTextLA, (), iColorA) + utils.getText(sTextRA) \
                        + utils.getText(sTextLB, (), iColorB) + utils.getText(sTextRB)
		screen.setTableInt(sTableName, iColumn, iRow,
                                   sText, "",
                                   WidgetTypes.WIDGET_GENERAL,
                                   utils.iTableTransports, pUnit.getID(),
                                   CvUtil.FONT_LEFT_JUSTIFY)

		# Unit's Current Cargo
                iColumn += 1
		sPanel = self.getNextWidgetName()
		screen.addPanel(sPanel, u"", u"",
                                True, False,
                                0, 0,
                                self.iButtonSize, self.iButtonSize,
                                PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, iRow, -1)
		screen.attachControlToTableCell(sPanel, sTableName, iRow, iColumn)
		lCargo = utils.getUnitCargo(pUnit)
		for iCount in range(len(lCargo)):
                        pCargoUnit = lCargo[iCount]
                        sButton = self.getNextWidgetName()
                        iX = iCount * (self.iButtonSize + 1)
                        screen.addCheckBoxGFCAt(sPanel, sButton,
                                                pCargoUnit.getButton(),
                                                oArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
                                                iX, 0,
                                                self.iButtonSize, self.iButtonSize,
                                                WidgetTypes.WIDGET_GENERAL,
                                                4444, pCargoUnit.getID(),
                                                ButtonStyles.BUTTON_STYLE_LABEL)
                        iYield = pCargoUnit.getYield()
                        if (iYield < 0):
                                continue
                        iStored = pCargoUnit.getYieldStored()
                        if (iStored < 1):
                                continue
                        sLabel = self.getNextWidgetName()
                        sText = "<font=4>%d</font>" %(iStored)
                        sText = utils.getText(sText)
			screen.setLabelAt(sLabel, sButton,
                                          sText, CvUtil.FONT_RIGHT_JUSTIFY,
                                          42, 35, -1.3,
                                          FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                return None

        #############################################################################################################
        #############################################################################################################
	# Commodities Page
        #############################################################################################################
        #############################################################################################################

	def drawCommodities(self):
                self.drawCommoditiesPanel()
                self.updateCommodities()
                return None

        def updateCommodities(self):
                self.drawYieldStoredTotalTable()
		self.drawYieldStoredTotalTableHeaders()
		self.fillYieldStoredTotalTable()
                self.drawCommoditiesTable()
                self.drawCommoditiesTableHeaders()
                self.fillCommoditiesTable()
                self.drawCityStoredTotalTable()
		self.drawCityStoredTotalTableHeaders()
		self.fillCityStoredTotalTable()
                return None

	def clearCommodities(self):
                screen = self.getScreen()
                screen.deleteWidget(self.COMMODITIES_TABLE_PANEL_ID)
                screen.deleteWidget(self.YIELD_STORED_TOTAL_TABLE_ID)
                screen.deleteWidget(self.COMMODITIES_TABLE_ID)
                screen.deleteWidget(self.CITY_STORED_TOTAL_TABLE_ID)
                return None

        #############################################################################################################

	def drawCommoditiesPanel(self):
		screen = self.getScreen()

		screen.attachPanelAt(self.SCROLL_PANEL_ID, self.COMMODITIES_TABLE_PANEL_ID,
                                     u"", u"",
                                     True, True,
                                     PanelStyles.PANEL_STYLE_IN,#PANEL_STYLE_MAIN,#
                                     self.X_TRADE_ROUTES_PANEL, self.Y_TRADE_ROUTES_PANEL,
                                     self.W_TRADE_ROUTES_PANEL, self.H_TRADE_ROUTES_PANEL,
                                     WidgetTypes.WIDGET_GENERAL, -1, -1)
		return None

        #############################################################################################################

        def drawYieldStoredTotalTable(self):
		screen = self.getScreen()
		iColumns = self.iYieldCount + 1
		screen.addTableControlGFC(self.YIELD_STORED_TOTAL_TABLE_ID,
                                          iColumns,
                                          self.X_YIELD_STORED_TOTAL_TABLE, self.Y_YIELD_STORED_TOTAL_TABLE,
                                          self.W_YIELD_STORED_TOTAL_TABLE, self.H_YIELD_STORED_TOTAL_TABLE,
                                          True, True,
                                          self.iButtonSize, self.iButtonSize,
                                          TableStyles.TABLE_STYLE_STANDARD)
		screen.setStyle(self.YIELD_STORED_TOTAL_TABLE_ID, "Table_StandardCiv_Style")
                iRow = 0
		screen.appendTableRow(self.YIELD_STORED_TOTAL_TABLE_ID)
		screen.setTableRowHeight(self.YIELD_STORED_TOTAL_TABLE_ID, iRow, self.iRowHeight)
		return None

        def drawYieldStoredTotalTableHeaders(self):
		screen = self.getScreen()
                iColumnWidth = 150
                iColumn = -1
                iColumn += 1
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SCREEN_CITY_NAMES", iColor = -1))
                screen.setTableColumnHeader(self.YIELD_STORED_TOTAL_TABLE_ID,
                                            iColumn,
                                            sText,
                                            iColumnWidth)
                iColumnWidth = ((self.W_YIELD_STORED_TOTAL_TABLE - iColumnWidth) / (self.iYieldCount)) + (0)
                for iYield in self.lYieldTypes:
                        iColumn += 1
                        sText = u"<font=3>  %c</font>" %(gc.getYieldInfo(iYield).getChar())
                        screen.setTableColumnHeader(self.YIELD_STORED_TOTAL_TABLE_ID,
                                                    iColumn,
                                                    sText,
                                                    iColumnWidth + (iYield % 2))
		return None

	def fillYieldStoredTotalTable(self):
		screen = self.getScreen()
		iRow = 0
		lTotals = [0] * (self.iYieldCount + 1)
		lCities = utils.getPlayerCities(oGame.getActivePlayer())
                for pLoopCity in lCities:
                        lTotals[0] += 1
                        for iYield in self.lYieldTypes:
                                iStored = pLoopCity.getYieldStored(iYield)
                                lTotals[iYield + 1] += iStored
                for iColumn in range(self.iYieldCount + 1):
                        iTotal = lTotals[iColumn]
                        sText = u"<font=3>%d</font>" %(iTotal)
                        sText = utils.getText(sText)
                        if (iColumn == 0):
                                iData1 = -1
                                iData2 = -1
                        else:
                                iData1 = utils.iTableCommoditiesTotalYield
                                iData2 = iColumn - 1
			screen.setTableInt(self.YIELD_STORED_TOTAL_TABLE_ID,
                                           iColumn, iRow,
                                           sText,
                                           "", WidgetTypes.WIDGET_GENERAL,
                                           iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
		return None

        #############################################################################################################

        def drawCommoditiesTable(self):
		screen = self.getScreen()
		iColumns = self.iYieldCount + 1
		screen.addTableControlGFC(self.COMMODITIES_TABLE_ID,
                                          iColumns,
                                          self.X_COMMODITIES_TABLE, self.Y_COMMODITIES_TABLE,
                                          self.W_COMMODITIES_TABLE, self.H_COMMODITIES_TABLE,
                                          False, True,
                                          self.iButtonSize, self.iButtonSize,
                                          TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.COMMODITIES_TABLE_ID, True)
		screen.setStyle(self.COMMODITIES_TABLE_ID, "Table_StandardCiv_Style")
		return None

	def drawCommoditiesTableHeaders(self):
		screen = self.getScreen()
                iColumnWidth = 150
                iColumn = -1
                iColumn += 1
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_COMMODITIES_CITY_NAME", iColor = -1))
                screen.setTableColumnHeader(self.COMMODITIES_TABLE_ID,
                                            iColumn,
                                            sText,
                                            iColumnWidth)
                iColumnWidth = ((self.W_YIELD_STORED_TOTAL_TABLE - iColumnWidth) / (self.iYieldCount)) + (0)
                for iYield in self.lYieldTypes:
                        iColumn += 1
                        sText = u"<font=3>  %c</font>" %(gc.getYieldInfo(iYield).getChar())
                        screen.setTableColumnHeader(self.COMMODITIES_TABLE_ID,
                                                    iColumn,
                                                    sText,
                                                    iColumnWidth + (iYield % 2))
		return None

	def fillCommoditiesTable(self):
		screen = self.getScreen()
                iRow = -1
                lCities = utils.getPlayerCities(oGame.getActivePlayer())
                for pLoopCity in lCities:
                        iRow += 1
                        screen.appendTableRow(self.COMMODITIES_TABLE_ID)
                        screen.setTableRowHeight(self.COMMODITIES_TABLE_ID, iRow, self.iGraphRowH)

                        iColumnWidth = 100
                        iColumn = -1

                        # City Name
                        iColumn += 1
                        sText = u"<font=3>%s</font>" %(pLoopCity.getName())
                        sText = utils.getText(sText)
			screen.setTableText(self.COMMODITIES_TABLE_ID,
                                            iColumn, iRow,
                                            sText,
                                            "",#oArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath(),
                                            WidgetTypes.WIDGET_GENERAL,
                                            utils.iTableCommodities, pLoopCity.getID(),
                                            CvUtil.FONT_LEFT_JUSTIFY);
                        iMaxYield = pLoopCity.getMaxYieldCapacity()
                        for iYield in self.lYieldTypes:
                                iColumn += 1
                                iYieldStored = pLoopCity.getYieldStored(iYield)
                                sTextL = u"<font=2>%d</font>" %(iYieldStored)
                                if (iYieldStored == 0):
                                        iColor = gc.getInfoTypeForString("COLOR_FONT_CREAM")
                                elif (iYieldStored >= iMaxYield):
                                        iColor = gc.getInfoTypeForString("COLOR_RED")
                                elif (iYieldStored >= iMaxYield / 2):
                                        iColor = gc.getInfoTypeForString("COLOR_YELLOW")
                                else:
                                        iColor = gc.getInfoTypeForString("COLOR_GREEN")
                                sTextL = utils.getText(sTextL, (), iColor)
                                sTextR = u"<font=2> (%d)</font>" %(iMaxYield)
                                sTextR = utils.getText(sTextR, ())
                                sText = sTextL# + sTextR
                                screen.setTableText(self.COMMODITIES_TABLE_ID,
                                                    iColumn, iRow,
                                                    sText, "",
                                                    WidgetTypes.WIDGET_GENERAL,
                                                    utils.iTableCommodities, pLoopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
                return None
                for iYield in self.lYieldTypes:
                        sText = u"<font=3> %c</font>" %(gc.getYieldInfo(iYield).getChar())
			screen.setTableText(self.COMMODITIES_TABLE_ID,
                                            iColumn, iRow,
                                            sText,
                                            "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			iColumn += 1
                return None

        #############################################################################################################

        def drawCityStoredTotalTable(self):
		screen = self.getScreen()
		iColumns = 1
		screen.addTableControlGFC(self.CITY_STORED_TOTAL_TABLE_ID,
                                          iColumns,
                                          self.X_CITY_STORED_TOTAL_TABLE, self.Y_CITY_STORED_TOTAL_TABLE,
                                          self.W_CITY_STORED_TOTAL_TABLE, self.H_CITY_STORED_TOTAL_TABLE,
                                          False, True,
                                          self.iButtonSize, self.iButtonSize,
                                          TableStyles.TABLE_STYLE_STANDARD)
		#screen.setHitTest(self.CITY_STORED_TOTAL_TABLE_ID, HitTestTypes.HITTEST_NOHIT)
		screen.setStyle(self.CITY_STORED_TOTAL_TABLE_ID, "Table_StandardCiv_Style")
		return None

        def drawCityStoredTotalTableHeaders(self):
		screen = self.getScreen()
                iColumnWidth = self.W_CITY_STORED_TOTAL_TABLE
                iColumn = 0
                sText = u"<font=3>%s</font>" %(utils.getText("TXT_KEY_SCREEN_CITY_TOTALS", iColor = -1))
                screen.setTableColumnHeader(self.CITY_STORED_TOTAL_TABLE_ID,
                                            iColumn,
                                            sText,
                                            iColumnWidth)
		return None

	def fillCityStoredTotalTable(self):
		screen = self.getScreen()
		iColumn = 0
		iRow = -1
		lCities = utils.getPlayerCities(oGame.getActivePlayer())
                for pLoopCity in lCities:
                        iRow += 1
                        screen.appendTableRow(self.CITY_STORED_TOTAL_TABLE_ID)
                        screen.setTableRowHeight(self.CITY_STORED_TOTAL_TABLE_ID, iRow, self.iGraphRowH)

                        iTotal = 0
                        for iYield in self.lYieldTypes:
                                iStored = pLoopCity.getYieldStored(iYield)
                                iTotal += iStored
                        sText = u"<font=3>%d</font>" %(iTotal)
                        sText = utils.getText(sText)
			screen.setTableInt(self.CITY_STORED_TOTAL_TABLE_ID,
                                           iColumn, iRow,
                                           sText,
                                           "", WidgetTypes.WIDGET_GENERAL,
                                           utils.iTableCommoditiesTotalCity, pLoopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
		return None

        #############################################################################################################
        #############################################################################################################
	# Graph Page
        #############################################################################################################
        #############################################################################################################

	def drawGraph(self):
                self.drawChooseYieldDropdown()
                self.drawChooseGraphDropdown()
                self.drawChooseGraphInfoDropdown()
                self.updateGraph()
                return None

        def updateGraph(self):
                screen = self.getScreen()
                self.drawGraphLegend()
                self.drawGraphCanvas()
                self.drawGraphBorderLines()
                self.drawGraphYLabels()
                self.drawGraphLines()
                return None

        def clearGraph(self):
                screen = self.getScreen()
                screen.deleteWidget(self.GRAPH_CHOOSE_YIELD_DROPDOWN_ID)
                screen.deleteWidget(self.GRAPH_CHOOSE_GRAPH_DROPDOWN_ID)
                screen.deleteWidget(self.GRAPH_CHOOSE_GRAPH_INFO_DROPDOWN_ID)

                screen.deleteWidget(self.GRAPH_LEGEND_PANEL_ID)
                screen.deleteWidget(self.GRAPH_LEGEND_DRAW_CONTROL_ID)

                #screen.deleteWidget(self.GRAPH_X_LABEL_LEFT_ID)
                #screen.deleteWidget(self.GRAPH_X_LABEL_RIGHT_ID)
                self.deleteAllTexts()
                screen.deleteWidget(self.GRAPH_DRAW_CONTROL_ID)
                screen.deleteWidget(self.GRAPH_SCROLL_PANEL_ID)
                return None

        #############################################################################################################

	def drawChooseYieldDropdown(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC(self.GRAPH_CHOOSE_YIELD_DROPDOWN_ID,
                                         self.X_GRAPH_DROPDOWN, self.Y_GRAPH_CHOOSE_YIELD_DROPDOWN,
                                         self.W_GRAPH_DROPDOWN,
                                         WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		sText = u"%s" %(utils.getText("TXT_KEY_SCREEN_GRAPH_ALL_YIELDS", iColor = -1))
		screen.addPullDownString(self.GRAPH_CHOOSE_YIELD_DROPDOWN_ID, sText, -1, -1, True)
		for iYield in self.dGraphYieldTypes[self.iGraphYieldDisplay]:
                        pInfo = gc.getYieldInfo(iYield)
                        sText = "%s" %(pInfo.getDescription())
                        screen.addPullDownString(self.GRAPH_CHOOSE_YIELD_DROPDOWN_ID,
                                                 sText, -1, -1, False)
                return None

	def drawChooseGraphDropdown(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC(self.GRAPH_CHOOSE_GRAPH_DROPDOWN_ID,
                                         self.X_GRAPH_DROPDOWN, self.Y_GRAPH_CHOOSE_GRAPH_DROPDOWN,
                                         self.W_GRAPH_DROPDOWN,
                                         WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for iID in self.dGraphYieldDisplays.keys():
                        sTextKey = self.dGraphYieldDisplays[iID]
                        sText = u"%s" %(utils.getText(sTextKey, iColor = -1))
                        screen.addPullDownString(self.GRAPH_CHOOSE_GRAPH_DROPDOWN_ID,
                                                 sText, -1, -1, False)
                return None

	def drawChooseGraphInfoDropdown(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC(self.GRAPH_CHOOSE_GRAPH_INFO_DROPDOWN_ID,
                                         self.X_GRAPH_DROPDOWN, self.Y_GRAPH_CHOOSE_GRAPH_INFO_DROPDOWN,
                                         self.W_GRAPH_DROPDOWN,
                                         WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		sText = u"%s" %(utils.getText("TXT_KEY_SCREEN_GRAPH_NO_INFORMATION", iColor = -1))
		screen.addPullDownString(self.GRAPH_CHOOSE_GRAPH_INFO_DROPDOWN_ID,
                                         sText, -1, -1, False)
		sText = u"%s" %(utils.getText("TXT_KEY_SCREEN_GRAPH_TURN_TOTALS", iColor = -1))
		screen.addPullDownString(self.GRAPH_CHOOSE_GRAPH_INFO_DROPDOWN_ID,
                                         sText, -1, -1, False)
                return None

	def drawGraphLegend(self):
		screen = self.getScreen()

                self.H_GRAPH_LEGEND = self.dGraphYieldCount[self.iGraphYieldDisplay] * self.H_GRAPH_LEGEND_ROW
                self.Y_GRAPH_LEGEND = (self.H_SCREEN - self.H_BAR - self.iBorder) - self.H_GRAPH_LEGEND

		screen.addPanel(self.GRAPH_LEGEND_PANEL_ID, "", "",
                                True, True,
                                self.X_GRAPH_LEGEND, self.Y_GRAPH_LEGEND,
                                self.W_GRAPH_LEGEND, self.H_GRAPH_LEGEND,
                                PanelStyles.PANEL_STYLE_IN, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addDrawControl(self.GRAPH_LEGEND_DRAW_CONTROL_ID,
                                      None,
                                      self.X_GRAPH_LEGEND, self.Y_GRAPH_LEGEND,
                                      self.W_GRAPH_LEGEND, self.H_GRAPH_LEGEND,
                                      WidgetTypes.WIDGET_GENERAL, -1, -1)

                iStartX = self.iMargin
                iStartY = self.H_GRAPH_LEGEND_ROW / 2
                iEndX = iStartX + self.W_GRAPH_LEGEND_LINE
                iEndY = self.H_GRAPH_LEGEND_ROW / 2
                """screen.addLineGFC(self.GRAPH_LEGEND_DRAW_CONTROL_ID, self.getNextLineName(),
                                  iStartX, iStartY,
                                  iEndX, iEndY,
                                  gc.getInfoTypeForString("COLOR_RED"))"""
		for iYield in self.dGraphYieldTypes[self.iGraphYieldDisplay]:#self.lYieldTypes:
                        iR = iYield % 256
                        iG = iYield % 256
                        iB = iYield % 256
                        iColor = self.getGraphLineColor(iYield)
                        if (self.lYieldGraphStates[iYield + 1]):
                                self.drawLine(self.GRAPH_LEGEND_DRAW_CONTROL_ID,
                                              iStartX, iStartY,
                                              iEndX, iEndY,
                                              iColor, 1)

                        sText = u"<font=3>%s</font>" %(gc.getYieldInfo(iYield).getDescription())
                        sText = oLocalText.changeTextColor(sText, iColor)
                        screen.setTextAt(self.getNextWidgetName(), self.GRAPH_LEGEND_DRAW_CONTROL_ID,
                                         sText,
                                         CvUtil.FONT_LEFT_JUSTIFY,
                                         iEndX + self.iMargin, iStartY, 0,
                                         FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 2222, iYield)
                        iStartY += self.H_GRAPH_LEGEND_ROW
                        iEndY += self.H_GRAPH_LEGEND_ROW
		return None

        #############################################################################################################

	def drawGraphCanvas(self):
		screen = self.getScreen()
		screen.addScrollPanel(self.GRAPH_SCROLL_PANEL_ID, u"",
                                      self.X_GRAPH_SCROLL_PANEL, self.Y_GRAPH_SCROLL_PANEL,
                                      self.W_GRAPH_SCROLL_PANEL, self.H_GRAPH_SCROLL_PANEL,
                                      PanelStyles.PANEL_STYLE_EXTERNAL, True, WidgetTypes.WIDGET_GENERAL, -1, -1)

                screen.attachPanelAt(self.GRAPH_SCROLL_PANEL_ID, self.GRAPH_PANEL_ID,
                                     u"", u"",
                                     False, True,
                                     PanelStyles.PANEL_STYLE_EMPTY,#PANEL_STYLE_MAIN,#PANEL_STYLE_IN,#
                                     self.X_GRAPH_PANEL, self.Y_GRAPH_PANEL,
                                     self.W_GRAPH_PANEL, self.H_GRAPH_PANEL,
                                     WidgetTypes.WIDGET_GENERAL, -1, -1)

                screen.addDrawControlAt(self.GRAPH_DRAW_CONTROL_ID, self.GRAPH_PANEL_ID,
                                        oArtFileMgr.getInterfaceArtInfo("SCREEN_BG").getPath(),
                                        self.X_GRAPH_CANVAS, self.Y_GRAPH_CANVAS,
                                        self.W_GRAPH_CANVAS, self.H_GRAPH_CANVAS,
                                        WidgetTypes.WIDGET_GENERAL, -1, -1)
                return None

        def drawGraphBorderLines(self):
		screen = self.getScreen()
		# Draw Horizontial Top line
                screen.addLineGFC(self.GRAPH_DRAW_CONTROL_ID, self.GRAPH_X_TOP_BORDER_LINE_ID,
                                  self.X_GRAPH_LEFT, self.Y_GRAPH_TOP,
                                  self.X_GRAPH_RIGHT, self.Y_GRAPH_TOP,
                                  gc.getInfoTypeForString("COLOR_GREY"))

		# Draw Horizontial Bottom Border line
                screen.addLineGFC(self.GRAPH_DRAW_CONTROL_ID, self.GRAPH_X_BOTTOM_BORDER_LINE_ID,
                                  self.X_GRAPH_LEFT, self.Y_GRAPH_BOTTOM,
                                  self.X_GRAPH_RIGHT, self.Y_GRAPH_BOTTOM,
                                  gc.getInfoTypeForString("COLOR_GREY"))

                # Draw Verticial Left Border line
                screen.addLineGFC(self.GRAPH_DRAW_CONTROL_ID, self.GRAPH_Y_LEFT_BORDER_LINE_ID,
                                  self.X_GRAPH_LEFT, self.Y_GRAPH_TOP,
                                  self.X_GRAPH_LEFT, self.Y_GRAPH_BOTTOM,
                                  gc.getInfoTypeForString("COLOR_GREY"))

                # Draw Verticial Right Border line
                screen.addLineGFC(self.GRAPH_DRAW_CONTROL_ID, self.GRAPH_Y_RIGHT_BORDER_LINE_ID,
                                  self.X_GRAPH_RIGHT, self.Y_GRAPH_TOP,
                                  self.X_GRAPH_RIGHT, self.Y_GRAPH_BOTTOM,
                                  gc.getInfoTypeForString("COLOR_GREY"))
                return None

        def drawGraphYLabels(self):
		screen = self.getScreen()
		self.deleteAllTexts()
		iX = self.X_GRAPH_SCROLL_PANEL + 8
		iGraphBottom = self.Y_GRAPH_SCROLL_PANEL + (self.H_GRAPH_CANVAS - 14)
                iGraphH = (self.Y_GRAPH_BOTTOM - self.Y_GRAPH_TOP)
                iOffset = (iGraphH / self.iGraphDiv)
                iMaxValue = self.getGraphYValue(self.Y_GRAPH_TOP)
                for iLoop in range(self.iGraphDiv + 1):
                        iY = iGraphBottom - (iLoop * iOffset)
                        iValueY = self.Y_GRAPH_BOTTOM - (iLoop * iOffset)
                        iValue = self.getGraphYValue(iValueY)
                        sText = u"<font=3>%d</font>" %(iValue)
                        sText = utils.getText(sText)
                        screen.setText(self.getNextTextName(), self.BACKGROUND_ID,#self.GRAPH_PANEL_ID,
                                 sText,
                                 CvUtil.FONT_RIGHT_JUSTIFY,
                                 iX, iY, 0,
                                 FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		return None

        def drawGraphLines(self):
		screen = self.getScreen()
		self.deleteAllLines()
                iStartTurn = oGame.getStartTurn()
                iGameTurn = oGame.getGameTurn()
                if (iGameTurn <= iStartTurn):
                        return None
                pPlayer = gc.getActivePlayer()
                lTurns = range(iStartTurn, iGameTurn)
                #alert.alert(0, lTurns)
                for iTurnIndex in range(len(lTurns)):
                        iTurn = lTurns[iTurnIndex]
                        iStartX = self.X_GRAPH_LEFT + (self.iGraphColumnW * (iTurnIndex - 1))
                        iEndX = self.X_GRAPH_LEFT + (self.iGraphColumnW * iTurnIndex)
                        sText = u"<font=2>%s</font>" %(utils.getTurnDate(iTurn))
                        sText = utils.getText(sText)
                        iY = self.Y_GRAPH_BOTTOM + self.iBorder
                        screen.setTextAt(self.getNextWidgetName(), self.GRAPH_PANEL_ID,
                                         sText,
                                         CvUtil.FONT_CENTER_JUSTIFY,
                                         iEndX, iY, 0,
                                         FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
                        for iYield in self.dGraphYieldTypes[self.iGraphYieldDisplay]:
                                if (not self.lYieldGraphStates[iYield + 1]):
                                        continue
                                iLastTurnIndex = iTurnIndex - 1
                                if (iLastTurnIndex < 0):
                                        continue
                                iColor = self.getGraphLineColor(iYield)

                                iLastTurn = lTurns[iLastTurnIndex]
                                if (self.dGraphYieldDisplays[self.iGraphYieldDisplay] == "TXT_KEY_SCREEN_GRAPH_YIELDS_STORED"):
                                        iLastValue = pPlayer.getYieldStoredHistory(iLastTurn, iYield)
                                elif (self.dGraphYieldDisplays[self.iGraphYieldDisplay] == "TXT_KEY_SCREEN_GRAPH_YIELD_RATES"):
                                        iLastValue = pPlayer.getYieldRateHistory(iLastTurn, iYield)
                                else:
                                        iLastValue = 0
                                iStartY = self.getGraphY(iLastValue)

                                if (self.dGraphYieldDisplays[self.iGraphYieldDisplay] == "TXT_KEY_SCREEN_GRAPH_YIELDS_STORED"):
                                        iValue = pPlayer.getYieldStoredHistory(iTurn, iYield)
                                elif (self.dGraphYieldDisplays[self.iGraphYieldDisplay] == "TXT_KEY_SCREEN_GRAPH_YIELD_RATES"):
                                        iValue = pPlayer.getYieldRateHistory(iTurn, iYield)
                                else:
                                        iValue = 0
                                iEndY = self.getGraphY(iValue)
                                self.drawLine(self.GRAPH_DRAW_CONTROL_ID,
                                              iStartX, iStartY,
                                              iEndX, iEndY,
                                              iColor, 1, 1)
                                iGraphInfo = screen.getSelectedPullDownID(self.GRAPH_CHOOSE_GRAPH_INFO_DROPDOWN_ID)
                                if (iGraphInfo == 1):
                                        if (iTurnIndex == 1):
                                                sText = u"<font=3>%d</font>" %(iLastValue)
                                                sText = utils.getText(sText, (), iColor)
                                                screen.setTextAt(self.getNextWidgetName(), self.GRAPH_PANEL_ID,
                                                                 sText, CvUtil.FONT_CENTER_JUSTIFY,
                                                                 iStartX, iStartY, 0,
                                                                 FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, iYield)
                                        sText = u"<font=3>%d</font>" %(iValue)
                                        sText = utils.getText(sText, (), iColor)
                                        screen.setTextAt(self.getNextWidgetName(), self.GRAPH_PANEL_ID,
                                                         sText, CvUtil.FONT_CENTER_JUSTIFY,
                                                         iEndX, iEndY, 0,
                                                         FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, iYield)
                                continue
                        continue
                return None

        #############################################################################################################

	def getGraphLineColor(self, iYield):
                return iYield + 6

        def getGraphY(self, iValue):
                fGraphOffset = self.dGraphYieldDisplayOffsets[self.iGraphYieldDisplay]
                if (fGraphOffset < 1.0):
                        return self.Y_GRAPH_BOTTOM - (iValue * int(1.0 / fGraphOffset))
                iGraphDiv = self.dGraphYieldDisplayDivs[self.iGraphYieldDisplay]
                return self.Y_GRAPH_BOTTOM - (iValue / int(iGraphDiv))

        def getGraphYValue(self, iY):
                if (iY > self.Y_GRAPH_BOTTOM):
                        return 0
                iHeight = (self.Y_GRAPH_BOTTOM - iY)
                fGraphOffset = self.dGraphYieldDisplayOffsets[self.iGraphYieldDisplay]
                if (fGraphOffset < 1.0):
                        return iHeight / int(1.0 / fGraphOffset)
                iGraphDiv = self.dGraphYieldDisplayDivs[self.iGraphYieldDisplay]
                return iHeight * iGraphDiv

	def drawLine(self, pCanvas, iStartX, iStartY, iEndX, iEndY, ColorType, iEndRounding = 0, iNumLines = 1):
		screen = self.getScreen()
		if (type(ColorType) == str):
                        iColor = gc.getInfoTypeForString(ColorType)
                elif (type(ColorType) == int) or (type(ColorType) == ColorTypes):
                        iColor = ColorType
                else:
                        iColor = 0

                # Draw our main middle line
		screen.addLineGFC(pCanvas, self.getNextLineName(), iStartX, iStartY, iEndX, iEndY, iColor)
		if (iNumLines > 1):
                        # Draw the top and bottom lines
                        #if (iEndRounding > 0):
                        #        iStartX += iEndRounding
                        #        iEndX -= iEndRounding
                        screen.addLineGFC(pCanvas, self.getNextLineName(), iStartX, iStartY - 1, iEndX, iEndY - 1, iColor)
                        screen.addLineGFC(pCanvas, self.getNextLineName(), iStartX, iStartY + 1, iEndX, iEndY + 1, iColor)
		return None

	def getSelectedTradeRoute(self):
		screen = self.getScreen()
                iTradeRoute = -1
                for iRow in range(len(self.lTradeRoutes)):
                        if (screen.isRowSelected(self.TRADE_ROUTES_TABLE_ID, iRow)):
                                iTradeRoute = self.lTradeRoutes[iRow]
                                break
                if (iTradeRoute < 0) and (len(self.lTradeRoutes) > 0):
                        iTradeRoute = self.lTradeRoutes[0]
                return iTradeRoute

        #############################################################################################################

