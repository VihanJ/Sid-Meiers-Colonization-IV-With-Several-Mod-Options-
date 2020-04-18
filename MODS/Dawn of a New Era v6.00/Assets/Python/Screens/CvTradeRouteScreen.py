## Copyright Fratelli Marconni, M07 12-15-2013

#########################################
########## Trade route screen ###########
#########################################

import CvScreenEnums
import CvUtil
import CvMainInterface
from CvPythonExtensions import *


ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()
gc = CyGlobalContext()

class CvTradeRouteScreen:
	"Trade route screen"

	def __init__(self):
		self.WIDGET_ID = "TradeRouteScreenWidget"
		self.CIV_DROP_DOWN = "CivDropDown"
		self.nWidgetCount = 0

		self.EDIT_SEAWAY_NAME = 2

		self.SHOW_PANEL = False
		self.SHOW_ALL_YIELDS = False

		self.EUROPE_ID = -1
		self.UNSELECT_ID = -2

		self.CHANGE_SOURCE_CITY = 1
		self.CHANGE_DESTINATION_CITY = 2
		self.CHANGE_SELECTED_ROUTE = 3
		self.CHANGE_VIEW = 4
		self.CREATE_ROUTE = 5
		self.REMOVE_ROUTE = 6
		self.EDIT_ROUTE = 7
		self.SELECT_IMP_EXP_YIELD = 8
		self.REMOVE_YIELD_IMP_EXP = 9
		self.CHANGE_ACTIVE_RADIO = 10
		self.CHANGE_ACTIVE_EUROPEAN_RADIO = 11
		self.INACTIVE_CHECK_BOX = 12
		self.ACTIVE_CHECK_BOX = 13
		self.EJECT_UNIT_TO_GROUP = 14
		self.DISPLAY_SEAWAY_VIEW = 15
		self.EXIT_SEAWAY_VIEW = 16
		self.CHANGE_SEAWAY_PAGE = 17
		self.REMOVE_SEAWAY = 18
		self.RENAME_SEAWAY = 19
		self.SELECT_SEAWAY = 20
		self.SELECT_SEAWAY_HELP = 21
		self.ACTIVE_SEAWAY_CHECK_BOX = 22
		self.CHECK_BOX_GROUPS = 23
		self.CHANGE_SELECTED_ROUTE_PAGE = 24
		self.CHANGE_KEPT_AUTO_IN_WARTIME = 25
		self.ONLY_SHIP_HELP = 26
		self.ONLY_WAGON_HELP = 27
		self.SHIP_AND_WAGON_HELP = 28
		self.CHANGE_MIN_GOLD_TO_CONSERVE = 29

		self.TRADE_ROUTES_VIEW = 0
		#self.CREATE_TRADE_ROUTE_VIEW = 1
		self.EDIT_ROUTE_VIEW = 2
		self.EDIT_ROUTE_TRANSPORTS_VIEW = 3
		self.EDIT_ROUTE_ADD_TRANSPORTS_VIEW = 4

		self.View = self.TRADE_ROUTES_VIEW
		self.FirstUpdate = True

	def getScreen(self):
		return CyGInterfaceScreen("CvTradeRouteScreen", CvScreenEnums.TRADE_ROUTE_SCREEN)

	def initText(self):
		###### TEXT ######
		self.SCREEN_TITLE = u"<font=4b>" + localText.getText("TXT_KEY_TRADE_ROUTE_SCREEN_TITLE", ()).upper() + u"</font>"
		self.SCREEN_EXIT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
		self.SCREEN_BACK = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_BACK", ()).upper() + "</font>"

	def interfaceScreen(self, iGroupId):
		if ( CyGame().isPitbossHost() ):
			return

		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		self.pPlayer = pPlayer

		if pPlayer.getParent() == PlayerTypes.NO_PLAYER:
			return

		# Create screen
		screen = self.getScreen()
		if screen.isActive():
			return
		self.PanelType = PanelStyles.PANEL_STYLE_EMPTY
		if self.SHOW_PANEL:
			 self.PanelType = PanelStyles.PANEL_STYLE_MAIN

		self.iSliderQuantity = 0

		self.SourceCity = self.UNSELECT_ID
		self.DestinationCity = self.UNSELECT_ID
		self.SelectedRoute = self.UNSELECT_ID
		self.View = self.TRADE_ROUTES_VIEW
		self.PreviousView = self.TRADE_ROUTES_VIEW

		self.ImpExpYield = YieldTypes.NO_YIELD
		self.ImpYield = YieldTypes.NO_YIELD

		self.RouteID = self.UNSELECT_ID

		self.DisplaySeawayView = False
		self.LastAreaUnitsText = ""
		self.SelectedGroupId = -1
		self.CurrentSeawayPage = 1

		self.lOrderedSeaways = None
		self.ColonyList = []
		self.MainColor = gc.getInfoTypeForString("COLOR_PLAYER_LIGHT_BROWN_TEXT")

		self.calculateSizesAndPositions()
		self.initText()

		# Create screen		
		screen.addDDSGFC("TradeRoutesScreenUp", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BANDEAU_MARRON").getPath(), 0, 0, self.XResolution, 40, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("TradeRoutesScreenDown", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BANDEAU_MARRON").getPath(), 0, self.YResolution - 40, self.XResolution, 40, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addDDSGFC("TopPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TITLE").getPath(), 0, 0, self.XResolution, self.TOP_PANEL_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.showWindowBackground( False )
		# Set the background and exit button, and show the screen
		screen.setDimensions(0, 0, self.XResolution, self.YResolution)
		
		self.SCREEN_TITLE = localText.changeTextColor(self.SCREEN_TITLE, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setText("TitleOfScreen", "Background", self.SCREEN_TITLE, CvUtil.FONT_CENTER_JUSTIFY, self.XResolution / 2, 4, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					
		screen.addDDSGFC("TradeRouteBackground", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_SCREEN").getPath(), 0, 40, self.XResolution, self.YResolution - 80,  WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		self.initTradeRoutes(iGroupId)

		#Debug PullDown
		if CyGame().isDebugMode():
			xSize = 192
			screen.addDropDownBoxGFC(self.CIV_DROP_DOWN, self.XResolution - xSize*3/2, 0, xSize, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.SMALL_FONT )
			screen.setActivation(self.CIV_DROP_DOWN, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

			for j in range(gc.getMAX_PLAYERS()):
				loopPlayer = gc.getPlayer(j)
				if (loopPlayer.isAlive() and not loopPlayer.isEurope() and not loopPlayer.isNative()):
					screen.addPullDownString(self.CIV_DROP_DOWN, loopPlayer.getName(), j, j, False )
		else:
			screen.hide(self.CIV_DROP_DOWN)

		BottomPanelHight = 55
		screen.addPanel("ExitTab", "", "", False, False, 0, self.H_SCREEN - BottomPanelHight, self.W_SCREEN, BottomPanelHight, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addDrawControl("ExitTab", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_OFF").getPath(), 0, self.H_SCREEN - BottomPanelHight, self.W_SCREEN, BottomPanelHight, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setTextAt("ExitTabTitle", "ExitTab", self.SCREEN_EXIT, CvUtil.FONT_RIGHT_JUSTIFY, self.W_SCREEN - self.X_BOTTOM_LINKS_MARGIN , self.Y_BOTTOM_LINKS_MARGIN, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)
		
		# draw the contents
		self.drawContents()

		# MINIMAP INITIALIZATION
		screen.initMinimap(self.X_MINIMAP_START, self.X_MINIMAP_END, self.Y_MINIMAP_START, self.Y_MINIMAP_END, self.Z_CONTROLS, false )
		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_MILITARY)
		
		CvMainInterface.CvMainInterface().appendtoHideState(screen, "_FXS_Screen_Bogus_Minimap_Name", CvMainInterface.HIDE_TYPE_MAP, CvMainInterface.HIDE_LEVEL_ALL)
		CvMainInterface.CvMainInterface().appendtoHideState(screen, "_FXS_Screen_Bogus_Minimap_Name", CvMainInterface.HIDE_TYPE_CITY, CvMainInterface.HIDE_LEVEL_ALL)
		CvMainInterface.CvMainInterface().appendtoHideState(screen, "_FXS_Screen_Bogus_Minimap_Name", CvMainInterface.HIDE_TYPE_GLOBAL, CvMainInterface.HIDE_LEVEL_ALL)

	def initTradeRoutes(self, iGroupId):
		pPlayer = self.pPlayer
		
		self.orderCitiesByTradeRoutes()

		self.initSelectedRoute(True)

		if(iGroupId >= 0):
			pGroup = pPlayer.getSelectionGroup(iGroupId)
			if pGroup:
				pTradeRoute = pPlayer.getTradeRoute(pGroup.getTradeRoute())
				if pTradeRoute:
					self.View = self.EDIT_ROUTE_TRANSPORTS_VIEW
					self.RouteID = pTradeRoute.getID()
					self.SelectedRoute = pTradeRoute.getID()
					self.SourceCity = pTradeRoute.getSourceCity().iID
					self.DestinationCity = pTradeRoute.getDestinationCity().iID
					self.SelectedGroupId = iGroupId


	def drawContents(self):

		pPlayer = self.pPlayer
		
		self.deleteAllWidgets()

		if self.View == self.TRADE_ROUTES_VIEW:
			self.refreshFilteredTradeRoutes()

		self.displaySelectedColoniesView()

		self.displayColoniesView()

		if self.View == self.TRADE_ROUTES_VIEW:

			if self.shouldDisplayCreateRouteView():
				self.displayCreateRouteView()
			else:
				self.displayTradeRoutesView()

		elif self.View == self.EDIT_ROUTE_VIEW:
			self.displayEditRouteView()

		elif self.View == self.EDIT_ROUTE_TRANSPORTS_VIEW:
			self.displayTradeRouteGroups()

		elif self.View == self.EDIT_ROUTE_ADD_TRANSPORTS_VIEW:
			self.displaySourceAndDestinationGroups()

		self.displayBacklink()

		return 0

	def displayBacklink(self):
		screen = self.getScreen()
		if self.PreviousView == self.View:
			return 0

		screen.setTextAt(self.getNextWidgetName(), "ExitTab", self.SCREEN_BACK, CvUtil.FONT_LEFT_JUSTIFY, self.X_BOTTOM_LINKS_MARGIN , self.Y_BOTTOM_LINKS_MARGIN, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.CHANGE_VIEW, self.PreviousView)

	def shouldDisplayCreateRouteView(self):
		return len(self.FilteredTradeRoutes) == 0

	def initSelectedRoute(self, testCurrentRoute):
		pPlayer = self.pPlayer

		if self.View != self.TRADE_ROUTES_VIEW:
			return

		iCurrentTradeRouteId = pPlayer.getCurrentTradeRouteId()
		if testCurrentRoute and iCurrentTradeRouteId >= 0:
			self.SelectedRoute = iCurrentTradeRouteId
			return
		firstRouteId = self.UNSELECT_ID

		(loopTradeRoute, iter) = pPlayer.firstTradeRoute()
		while(loopTradeRoute):
			if(self.SourceCity == self.UNSELECT_ID or self.SourceCity == loopTradeRoute.getSourceCity().iID ):
				if(self.DestinationCity == self.UNSELECT_ID or self.DestinationCity == loopTradeRoute.getDestinationCity().iID ):
					if firstRouteId == self.UNSELECT_ID:
						firstRouteId = loopTradeRoute.getID()
					if self.SelectedRoute == loopTradeRoute.getID():
						return
					
			(loopTradeRoute, iter) = pPlayer.nextTradeRoute(iter)

		self.SelectedRoute = firstRouteId

	def displaySourceAndDestinationColonies(self, iSourceId, iDestinationId):
		screen = self.getScreen()
		pPlayer = self.pPlayer

		screen.moveToFront("TradeRouteBackground")#We move to front  the backgrong to put pictures behind
		
		# SOURCE 
		szNameSource = "???"

		self.SourcePicture = self.getNextWidgetName()
		if iSourceId == self.UNSELECT_ID:
			screen.addDDSGFC(self.SourcePicture, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_NO_CITY_SELECTED").getPath(), self.X_LEFT_COLONY_PANEL_START + self.X_CITY_ANIMATION, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION, self.W_CITY_ANIMATION, self.H_CITY_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		else:
			if iSourceId == self.EUROPE_ID:
				szNameSource = localText.getText("TXT_KEY_EUROPE_SCREEN_TITLE", ())
				screen.addDDSGFC(self.SourcePicture, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_COLONY_PICTURE").getPath(), self.X_LEFT_COLONY_PANEL_START + self.X_CITY_ANIMATION, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION, self.W_CITY_ANIMATION, self.H_CITY_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			else :
				pCity = pPlayer.getCity(iSourceId)
				pPlot = pCity.plot()
				szNameSource = pCity.getName()
				screen.addPlotGraphicGFC(self.SourcePicture, self.X_LEFT_COLONY_PANEL_START + self.X_CITY_ANIMATION, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION, self.W_CITY_ANIMATION, self.H_CITY_ANIMATION, pPlot, self.Z_CITY_DISTANCE, false, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.moveBackward(self.SourcePicture)
		#DESTINATION
		szNameDestination = "???"
		self.DestinationPicture = self.getNextWidgetName()
		if iDestinationId == self.UNSELECT_ID:
			screen.addDDSGFC(self.DestinationPicture, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_NO_CITY_SELECTED").getPath(), self.X_RIGHT_COLONY_PANEL_START + self.X_CITY_ANIMATION, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION, self.W_CITY_ANIMATION, self.H_CITY_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		else:
			if iDestinationId == self.EUROPE_ID:
				szNameDestination = localText.getText("TXT_KEY_EUROPE_SCREEN_TITLE", ())
				screen.addDDSGFC(self.DestinationPicture, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_COLONY_PICTURE").getPath(), self.X_RIGHT_COLONY_PANEL_START + self.X_CITY_ANIMATION, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION, self.W_CITY_ANIMATION, self.H_CITY_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			else:
				pCity = pPlayer.getCity(iDestinationId)
				pPlot = pCity.plot()
				szNameDestination = pCity.getName()
				screen.addPlotGraphicGFC(self.DestinationPicture, self.X_RIGHT_COLONY_PANEL_START + self.X_CITY_ANIMATION, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION, self.W_CITY_ANIMATION, self.H_CITY_ANIMATION, pPlot, self.Z_CITY_DISTANCE, false, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.moveBackward(self.DestinationPicture)
		# SOURCE 
		screen.setLabel(self.getNextWidgetName(), "Background", "<font=3b>" +  localText.changeTextColor(localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_START", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM")) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_LEFT_COLONY_PANEL_START + self.W_COLONY_PANEL/2, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION / 3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel(self.getNextWidgetName(), "Background", "<font=3>" +  self.mainColor(szNameSource) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_LEFT_COLONY_PANEL_START + self.W_COLONY_PANEL/2, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		#DESTINATION
		screen.setLabel(self.getNextWidgetName(), "Background", "<font=3b>" +localText.changeTextColor(localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_DESTINATION", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM")) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_RIGHT_COLONY_PANEL_START + self.W_COLONY_PANEL/2, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION / 3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel(self.getNextWidgetName(), "Background", "<font=3>" + self.mainColor(szNameDestination) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_RIGHT_COLONY_PANEL_START + self.W_COLONY_PANEL/2, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
	def displaySelectedColoniesView(self):
		pPlayer = self.pPlayer
		if self.View == self.TRADE_ROUTES_VIEW and self.SelectedRoute != self.UNSELECT_ID:
			pTraderoute = pPlayer.getTradeRoute(self.SelectedRoute)
			iSourceCityID = pTraderoute.getSourceCity().iID
			iDestinationCityID = pTraderoute.getDestinationCity().iID
			self.displaySourceAndDestinationColonies(iSourceCityID, iDestinationCityID)
		else:
			self.displaySourceAndDestinationColonies(self.SourceCity, self.DestinationCity)

	def displayTitle(self, szTitle):
		screen = self.getScreen()
		screen.setLabel(self.getNextWidgetName(), "Background", "<font=3b>" +  self.mainColor(szTitle) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.XResolution/2, self.Y_COLONY_PANEL_START - 8 - self.Y_MIDDLE_OFFSET, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
	
	def displayCreateRouteView(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer

		szTitle = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_HEADER_CREATING_ROUTE", ()).upper()
		self.displayTitle(szTitle)

		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_DESCRIPTION_BOX").getPath(), self.X_MID_VIEW, self.Y_TRADE_ROUTES, self.W_TRADE_ROUTES, self.H_DESC_CREATE_ROUTE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.DescriptionPanel = self.getNextWidgetName()
		
		szInformation = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_HELP_CREATING_ROUTE", ())
		screen.addMultilineText(self.getNextWidgetName(), "<font=3b>" +  self.descColor(szInformation) + "</font>", self.X_MID_VIEW + self.xSize(10), self.Y_TRADE_ROUTES + self.ySize(20), self.W_TRADE_ROUTES - 2 * self.xSize(10), self.H_DESC_CREATE_ROUTE, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
		
		createBtnName = self.getNextWidgetName()
		screen.setButtonGFC(createBtnName, localText.getText("TXT_KEY_TRADE_ROUTES_CREATE_ROUTE", ()), "", self.X_MID_VIEW + self.W_TRADE_ROUTES / 2 - self.W_CREATE_ROUTE_BTN / 2, self.Y_TRADE_ROUTES + self.H_DESC_CREATE_ROUTE, self.W_CREATE_ROUTE_BTN, self.H_CREATE_ROUTE_BTN, WidgetTypes.WIDGET_GENERAL, self.CREATE_ROUTE, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		if self.SourceCity  == self.UNSELECT_ID or self.DestinationCity  == self.UNSELECT_ID :
			screen.enable(createBtnName, False)
			
	def displayYieldsImpExp(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer

		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_BEST_YIELDS_BOX").getPath(), self.X_BEST_YIELDS_BOX, self.Y_BEST_YIELDS_BOX - self.Y_MIDDLE_OFFSET*3/2, self.W_BEST_YIELDS_BOX, self.H_BEST_YIELDS_BOX, WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.BestYieldPanel = self.getNextWidgetName()
		screen.addPanel(self.BestYieldPanel, "", "", True, True, self.X_BEST_YIELDS_BOX, self.Y_BEST_YIELDS_BOX - self.Y_MIDDLE_OFFSET*3/2, self.W_BEST_YIELDS_BOX, self.H_BEST_YIELDS_BOX, self.PanelType, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		szTitle = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_HEADER_BEST_YIELDS", ()).upper()
		screen.setLabelAt(self.getNextWidgetName(), self.BestYieldPanel, "<font=1b>" +  self.mainColor(szTitle) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W_BEST_YIELDS_BOX/2, 5, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if self.RouteID == self.UNSELECT_ID:
			return

		pTraderoute = pPlayer.getTradeRoute(self.RouteID)

		self.ColonyList = []
		(pCity, iter) = pPlayer.firstCity(false)
		while (pCity):
			numTradeRoutes = iter
			self.ColonyList.append((numTradeRoutes, pCity))
			(pCity, iter) = pPlayer.nextCity(iter, false)
			
		if len(self.ColonyList) > 0:
			self.ColonyList.sort()
			#self.ColonyList.reverse()

		bLeftYields = False
		bRightYields = False
		YieldList = []
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				if (not pPlayer.isHasYieldUnknown(iYield)):
					iValue = pTraderoute.getYieldValue(iYield)
					if iValue > 0:
						YieldList.append((iValue, iYield))
					if(pTraderoute.getTradeType(iYield) == TradeTypes.TRADE_IMPORT):
						bRightYields = True
					elif(pTraderoute.getTradeType(iYield) == TradeTypes.TRADE_EXPORT):
						bLeftYields = True
					
		if len(YieldList) > 0:
			YieldList.sort()
			YieldList.reverse()
			YieldSize = self.W_IMP_EXP_YIELD
			xLocation = self.X_IMP_EXP_PANEL
			yLocation = self.Y_IMP_EXP_PANEL
			xOffset = 0
			yOffset = 0
			
			for iYieldElement in YieldList:
				iYield = iYieldElement[1]
				kYield = gc.getYieldInfo(iYield)
				screen.addDragableButtonAt(self.BestYieldPanel, self.getNextWidgetName(), kYield.getIcon(), "", xLocation + xOffset * YieldSize * 15 / 11, yLocation + yOffset * YieldSize, YieldSize, YieldSize, WidgetTypes.WIDGET_TRADE_ROUTE_BEST_YIELD, iYield, -1, ButtonStyles.BUTTON_STYLE_LABEL)
				xOffset += 1
				if(xOffset == 10):
					yOffset += 1
					xOffset = 0

		#ARROWS HELPS
		if(not bLeftYields):
			screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_ARROW_LEFT_TOP").getPath(), self.X_BEST_YIELDS_BOX - self.ARROW_MIDDLE_SIZE/3 - 10, self.Y_BEST_YIELDS_BOX - self.ARROW_MIDDLE_SIZE*3/4, self.ARROW_MIDDLE_SIZE, self.ARROW_MIDDLE_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		if(not bRightYields):
			screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_ARROW_RIGHT_TOP").getPath(), self.X_BEST_YIELDS_BOX + self.W_TRADE_ROUTES + self.ARROW_MIDDLE_SIZE/3, self.Y_BEST_YIELDS_BOX - self.ARROW_MIDDLE_SIZE*3/4, self.ARROW_MIDDLE_SIZE, self.ARROW_MIDDLE_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
	def displayTopDescritptionRoute(self, pTraderoute):
		screen = self.getScreen()
		pPlayer = self.pPlayer
		
		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_DESCRIPTION_BOX").getPath(), self.X_MID_VIEW, self.Y_TRADE_ROUTES, self.W_TRADE_ROUTES, self.H_DESC_CREATE_ROUTE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.DescriptionPanel = self.getNextWidgetName()
		screen.addPanel(self.DescriptionPanel, "", "", True, True, self.X_MID_VIEW, self.Y_TRADE_ROUTES, self.W_TRADE_ROUTES, self.H_DESC_CREATE_ROUTE, self.PanelType, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		iRow = 0

		iCapacity = pTraderoute.getTransportUnitsCapacity()
			
		if iCapacity == 0:
			szText = localText.getText("TXT_KEY_TRADE_ROUTE_WARNING_INACTIVE_NO_TRANSPORT", ())
			screen.attachMultilineTextAt(self.DescriptionPanel, self.getNextWidgetName(), u"<font=4>" + self.warningColor(szText) + u"</font>", self.X_ROW_DESC_OFFSET, 0, self.W_TRADE_ROUTES - 2*self.X_ROW_DESC_OFFSET, self.H_DESC_CREATE_ROUTE + 2*self.W_TRADE_ROUTES,  WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)	
		else:
			iRow += 1
			screen.setLabelAt(self.getNextWidgetName(), self.DescriptionPanel, "<font=3>" + self.mainColor(localText.getText("TXT_KEY_TRADE_ROUTES_DESC_UNITS_CAPACITY", (iCapacity, ))) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ROW_DESC_OFFSET, iRow * self.W_ROW_DESC_OFFSET, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			iRow += 1
			iAverageLoad = pTraderoute.getLoadedCargoPercent()
			screen.setLabelAt(self.getNextWidgetName(), self.DescriptionPanel, "<font=3>" + self.mainColor(localText.getText("TXT_KEY_TRADE_ROUTES_DESC_LOAD_AVERAGE", (iAverageLoad, ))) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ROW_DESC_OFFSET, iRow * self.W_ROW_DESC_OFFSET, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			iRow += 1
			iAverageLoadTenRotations = pTraderoute.getLoadedCargoHistPercent()
			screen.setLabelAt(self.getNextWidgetName(), self.DescriptionPanel, "<font=3>" + self.mainColor(localText.getText("TXT_KEY_TRADE_ROUTES_DESC_LOAD_AVERAGE_X_ROTATION", (iAverageLoadTenRotations, gc.getNUM_TRADE_ROUTE_HIST_TURN(), ))) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ROW_DESC_OFFSET, iRow * self.W_ROW_DESC_OFFSET, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			if self.SourceCity == self.EUROPE_ID or self.DestinationCity == self.EUROPE_ID: 	
				iRow += 1
				iGoldAmountToAlwaysConserve = pTraderoute.getGoldAmountToAlwaysConserve()
				screen.setLabelAt(self.getNextWidgetName(), self.DescriptionPanel, "<font=3>" + self.mainColor(localText.getText("TXT_KEY_TRADE_ROUTES_GOLD_AMOUNT_TO_ALWAYS_CONSERVE", (iGoldAmountToAlwaysConserve, ))) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ROW_DESC_OFFSET, iRow * self.W_ROW_DESC_OFFSET, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setImageButtonAt(self.getNextWidgetName(), self.DescriptionPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_RENAME").getPath(), self.W_TRADE_ROUTES - self.X_OUTSIDE_CHANGE_MIN_GOLD_TO_CONSERVE_MARGIN, iRow * self.W_ROW_DESC_OFFSET - self.Y_OUTSIDE_CHANGE_MIN_GOLD_TO_CONSERVE_MARGIN, self.CHANGE_MIN_GOLD_TO_CONSERVE_ICON_SIZE, self.CHANGE_MIN_GOLD_TO_CONSERVE_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, self.CHANGE_MIN_GOLD_TO_CONSERVE, -1)
				
	def displayEditRouteView(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer

		if self.RouteID == self.UNSELECT_ID:
			return

		pTraderoute = pPlayer.getTradeRoute(self.RouteID)
		
		szTitle = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_HEADER_EDITING_ROUTE", ()).upper()
		self.displayTitle(szTitle)
		
		# DESCIPTION PANEL
		self.displayTopDescritptionRoute(pTraderoute)

		# TRANSPORTS VIEW BUTTON
		iCapacity = pTraderoute.getTransportUnitsCapacity()
			
		if iCapacity == 0:
			action = self.EDIT_ROUTE_ADD_TRANSPORTS_VIEW
			TransportViewButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_TRANSPORTS_VIEW_BUTTON").getPath()
		else: 
			action = self.EDIT_ROUTE_TRANSPORTS_VIEW
			TransportViewButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_TRANSPORTS_VIEW_EYE_BUTTON").getPath()

		screen.setImageButton(self.getNextWidgetName(), TransportViewButton, self.X_MID_VIEW + self.W_TRADE_ROUTES - self.W_TRANSPORTS_VIEW_BUTTON, self.Y_TRADE_ROUTES + self.H_DESC_CREATE_ROUTE, self.W_TRANSPORTS_VIEW_BUTTON, self.H_TRANSPORTS_VIEW_BUTTON, WidgetTypes.WIDGET_GENERAL, self.CHANGE_VIEW, action)
					
		# YIELDS EXPORT	
		SourceName = pTraderoute.getSourceCityName()
		DestinationName = pTraderoute.getDestinationCityName()

		self.ExportListBox = self.getNextWidgetName()
		self.ExportList = self.getNextWidgetName()
		screen.addDDSGFC(self.ExportListBox, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_IMP_EXP_BOX").getPath(), self.X_LEFT_COLONY_PANEL_START + 10, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION + self.H_SEPARATION - 3, self.W_COLONY_PANEL - 10, self.H_IMP_EXP_LIST + 11, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addScrollPanel(self.ExportList, u"", self.X_LEFT_COLONY_PANEL_START + 5, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION + self.H_SEPARATION - 5, self.W_COLONY_PANEL, self.H_IMP_EXP_LIST - 20, self.PanelType, False, WidgetTypes.WIDGET_TRADE_ROUTE_IMP_EXP_LIST, self.RouteID, TradeTypes.TRADE_EXPORT)
				
		bNoExportedYield = True
		iCount = 0
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				if(pTraderoute.getTradeType(iYield) == TradeTypes.TRADE_EXPORT):
					szText = u"%c %s" % (gc.getYieldInfo(iYield).getChar(), gc.getYieldInfo(iYield).getDescription())
					if self.ImpExpYield == iYield:
						szText = self.activeColor(szText)
					else:
						szText = self.unactiveColor(szText)
					screen.setTextAt(self.getNextWidgetName(), self.ExportList, u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 10, 10 + iCount*self.H_OFFSET_ROWS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.SELECT_IMP_EXP_YIELD, iYield)
					screen.setImageButtonAt(self.getNextWidgetName(), self.ExportList,  ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_REMOVE").getPath(), self.W_COLONY_PANEL - 11 - self.REMOVE_ICON_SIZE*2, iCount*self.H_OFFSET_ROWS, self.REMOVE_ICON_SIZE, self.REMOVE_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, self.REMOVE_YIELD_IMP_EXP, iYield)
					bNoExportedYield = False
					iCount += 1

		if bNoExportedYield:
			szHelp = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_IMPORT_EXPORT_YIELD_HELP", (SourceName, DestinationName, ))
			screen.attachMultilineTextAt(self.ExportListBox, self.getNextWidgetName(), u"<font=3>" + szHelp + u"</font>", 5, self.H_IMP_EXP_LIST/5, self.W_COLONY_PANEL - 18, self.H_IMP_EXP_LIST + 5,  WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			
		screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_EXPORT_BOX").getPath(), self.X_LEFT_COLONY_PANEL_START + 10, self.Y_BEST_YIELDS_BOX, self.W_COLONY_PANEL - 10, self.H_IMP_EXP_YIELDS_BOX, WidgetTypes.WIDGET_TRADE_ROUTE_IMP_EXP_BOX, self.RouteID, TradeTypes.TRADE_EXPORT)
		
		# YIELDS IMPORT	
		self.ImportListBox = self.getNextWidgetName()
		self.ImportList = self.getNextWidgetName()
		screen.addDDSGFC(self.ImportListBox, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_IMP_EXP_BOX").getPath(), self.X_RIGHT_COLONY_PANEL_START + 10, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION + self.H_SEPARATION - 3, self.W_COLONY_PANEL - 10, self.H_IMP_EXP_LIST + 11, WidgetTypes.WIDGET_GENERAL, -1, -1) 
		screen.addScrollPanel(self.ImportList, u"", self.X_RIGHT_COLONY_PANEL_START + 5, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION + self.H_SEPARATION - 5, self.W_COLONY_PANEL, self.H_IMP_EXP_LIST - 20, self.PanelType, False, WidgetTypes.WIDGET_TRADE_ROUTE_IMP_EXP_LIST, self.RouteID, TradeTypes.TRADE_IMPORT)
				
		bNoImportYield = True
		iCount = 0
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				if(pTraderoute.getTradeType(iYield) == TradeTypes.TRADE_IMPORT or self.SHOW_ALL_YIELDS):
					szText = u"%c %s" % (gc.getYieldInfo(iYield).getChar(), gc.getYieldInfo(iYield).getDescription())
					if self.ImpExpYield == iYield:
						szText = self.activeColor(szText)
					else:
						szText = self.unactiveColor(szText)
					screen.setTextAt(self.getNextWidgetName(), self.ImportList, u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 10, 10 + iCount*self.H_OFFSET_ROWS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.SELECT_IMP_EXP_YIELD, iYield)
					screen.setImageButtonAt(self.getNextWidgetName(), self.ImportList,  ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_REMOVE").getPath(), self.W_COLONY_PANEL - 11 - self.REMOVE_ICON_SIZE*2, iCount*self.H_OFFSET_ROWS, self.REMOVE_ICON_SIZE, self.REMOVE_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, self.REMOVE_YIELD_IMP_EXP, iYield)
					iCount += 1
					bNoImportYield = False

		if bNoImportYield:
			szHelp = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_IMPORT_EXPORT_YIELD_HELP", (DestinationName, SourceName, ))
			screen.attachMultilineTextAt(self.ImportListBox, self.getNextWidgetName(), u"<font=3>" + szHelp + u"</font>", 5, self.H_IMP_EXP_LIST/5, self.W_COLONY_PANEL - 18, self.H_IMP_EXP_LIST + 5, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

		screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_IMPORT_BOX").getPath(), self.X_RIGHT_COLONY_PANEL_START + 10, self.Y_BEST_YIELDS_BOX, self.W_COLONY_PANEL - 10, self.H_IMP_EXP_YIELDS_BOX, WidgetTypes.WIDGET_TRADE_ROUTE_IMP_EXP_BOX, self.RouteID, TradeTypes.TRADE_IMPORT )
		
		self.displayYieldsImpExp()

		self.displayYieldDescription()

	def getSourceID(self, pTradeRoute):
		if self.ImpExpYield == YieldTypes.NO_YIELD:
			return -1

		if(pTradeRoute.getTradeType(self.ImpExpYield) == TradeTypes.TRADE_IMPORT):
			return pTradeRoute.getDestinationCity().iID
		elif(pTradeRoute.getTradeType(self.ImpExpYield) == TradeTypes.TRADE_EXPORT):
			return pTradeRoute.getSourceCity().iID
			
		return -1
		
	def getDestinationID(self, pTradeRoute):
		if self.ImpExpYield == YieldTypes.NO_YIELD:
			return -1

		if(pTradeRoute.getTradeType(self.ImpExpYield) == TradeTypes.TRADE_IMPORT):
			return pTradeRoute.getSourceCity().iID
		elif(pTradeRoute.getTradeType(self.ImpExpYield) == TradeTypes.TRADE_EXPORT):
			return pTradeRoute.getDestinationCity().iID

		return -1

	def getSourceCityName(self, pTradeRoute):
		if self.ImpExpYield == YieldTypes.NO_YIELD:
			return ""

		if(pTradeRoute.getTradeType(self.ImpExpYield) == TradeTypes.TRADE_IMPORT):
			return pTradeRoute.getDestinationCityName()
		elif(pTradeRoute.getTradeType(self.ImpExpYield) == TradeTypes.TRADE_EXPORT):
			return pTradeRoute.getSourceCityName()
			
		return ""

	def getDestinationCityName(self, pTradeRoute):
		if self.ImpExpYield == YieldTypes.NO_YIELD:
			return ""

		if(pTradeRoute.getTradeType(self.ImpExpYield) == TradeTypes.TRADE_IMPORT):
			return pTradeRoute.getSourceCityName()
		elif(pTradeRoute.getTradeType(self.ImpExpYield) == TradeTypes.TRADE_EXPORT):
			return pTradeRoute.getDestinationCityName()

		return ""

	def displayYieldDescription(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer
		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_DESCRIPTION_BOX").getPath(), self.X_MID_VIEW, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION + self.H_SEPARATION - self.Y_MIDDLE_OFFSET*2 - 3, self.W_TRADE_ROUTES, self.H_IMP_EXP_LIST + 11, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		if self.RouteID == self.UNSELECT_ID:
			return

		pTraderoute = pPlayer.getTradeRoute(self.RouteID)
		
		self.YieldDescriptionPanel = self.getNextWidgetName()

		screen.addPanel(self.YieldDescriptionPanel, "", "", True, True, self.X_MID_VIEW, self.Y_MID_VIEW, self.W_TRADE_ROUTES, self.H_IMP_EXP_LIST + 11, self.PanelType, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		if self.ImpExpYield == YieldTypes.NO_YIELD:
			bLeftYields = False
			bRightYields = False
			for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				if gc.getYieldInfo(iYield).isCargo():
					if(pTraderoute.getTradeType(iYield) == TradeTypes.TRADE_IMPORT):
						bRightYields = True
					elif(pTraderoute.getTradeType(iYield) == TradeTypes.TRADE_EXPORT):
						bLeftYields = True
			szText = ""
			if(bRightYields and bLeftYields):
				szText = localText.getText("TXT_KEY_TRADE_ROUTES_SELECT_LEFT_OR_RIGHT_PART", ())
			elif bLeftYields:
				szText = localText.getText("TXT_KEY_TRADE_ROUTES_SELECT_LEFT_PART", ())
			elif bRightYields:
				szText = localText.getText("TXT_KEY_TRADE_ROUTES_SELECT_RIGHT_PART", ())
			if(bRightYields or bLeftYields):
				screen.attachMultilineTextAt(self.YieldDescriptionPanel, self.getNextWidgetName(), u"<font=3>" + szText + u"</font>", self.W_TRADE_ROUTES/20 -5, self.H_IMP_EXP_LIST/5, self.W_TRADE_ROUTES*18/20, self.H_IMP_EXP_LIST/2, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			
			#ARROWS HELPS
			if(bLeftYields):
				screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_ARROW_LEFT_MIDDLE").getPath(), self.X_MID_VIEW - self.W_ARROW_MIDDLE/2 - 10, self.Y_MID_VIEW + self.H_IMP_EXP_LIST/3, self.W_ARROW_MIDDLE, self.H_ARROW_MIDDLE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
			if(bRightYields):
				screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_ARROW_RIGHT_MIDDLE").getPath(), self.X_MID_VIEW + self.W_TRADE_ROUTES - self.W_ARROW_MIDDLE/2, self.Y_MID_VIEW + self.H_IMP_EXP_LIST/3, self.W_ARROW_MIDDLE, self.H_ARROW_MIDDLE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			return

		iSourceID = self.getSourceID(pTraderoute)
		iDestinationID = self.getDestinationID(pTraderoute)

		SourceName = self.getSourceCityName(pTraderoute)
		DestinationName = self.getDestinationCityName(pTraderoute)

		#TITLE
		szText = localText.getText("TXT_KEY_TRADE_ROUTE_DESC_YIELD_TITLE", (gc.getYieldInfo(self.ImpExpYield).getDescription(), )).upper()
		screen.setLabelAt(self.getNextWidgetName(), self.YieldDescriptionPanel, "<font=2>" + self.mainColor(szText) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, 18, 18, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		if self.EUROPE_ID != iSourceID:
			#RADIOS
			iRow = 1
			radioOption = pTraderoute.getRadioOption(self.ImpExpYield, TradeRouteRadioTypes.SEND_EVERYTHING_TO)
			szText = localText.getText("TXT_KEY_TRADE_ROUTES_RADIO_SEND_EVERYTHING_TO", (DestinationName, ))
			self.addRadioYieldDescription(TradeRouteRadioTypes.SEND_EVERYTHING_TO, iRow, szText, radioOption.isActivate, self.CHANGE_ACTIVE_RADIO)
			
			iRow += 1
			radioOption = pTraderoute.getRadioOption(self.ImpExpYield, TradeRouteRadioTypes.SEND_FIXED_QUANTITY)
			iQuantity = radioOption.iQuantity
			szQuantity = self.UKNOWN_VALUE
			if iQuantity > -1 and radioOption.isActivate:
				szQuantity = u"%s" % (iQuantity, )
			szText = localText.getText("TXT_KEY_TRADE_ROUTES_RADIO_SEND_FIXED_QUANTITY", (szQuantity, gc.getYieldInfo(self.ImpExpYield).getChar(), ))
			self.addRadioYieldDescription(TradeRouteRadioTypes.SEND_FIXED_QUANTITY, iRow, szText, radioOption.isActivate, self.CHANGE_ACTIVE_RADIO)
			
			if self.EUROPE_ID != iDestinationID:
				iRow += 1
				radioOption = pTraderoute.getRadioOption(self.ImpExpYield, TradeRouteRadioTypes.ENSURE_THE_NEEDS)
				iQuantity = radioOption.iQuantity
				szBufferQuantity = self.UKNOWN_VALUE
				if iQuantity > -1 and radioOption.isActivate:
					szBufferQuantity = u"%s" % (iQuantity, )

				szText = localText.getText("TXT_KEY_TRADE_ROUTES_RADIO_ENSURE_THE_NEEDS", (DestinationName, szBufferQuantity, gc.getYieldInfo(self.ImpExpYield).getChar(), ))
				self.addRadioYieldDescription(TradeRouteRadioTypes.ENSURE_THE_NEEDS, iRow, szText, radioOption.isActivate, self.CHANGE_ACTIVE_RADIO)

			screen.addDDSGFCAt(self.getNextWidgetName(), self.YieldDescriptionPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_SMALL_LINE").getPath(), 10 + self.RADIO_SIZE, self.H_IMP_EXP_LIST/2 + 5, self.W_TRADE_ROUTES/2, 4, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
						
			#CHECKBOXES
			iRow = 0

			if self.EUROPE_ID != iDestinationID:
				iRow += 1
				cbOption = pTraderoute.getCheckBoxOption(self.ImpExpYield, TradeRouteCheckBoxTypes.DO_NOT_EXCEED)
				iQuantity = cbOption.iQuantity
				szQuantity = self.UKNOWN_VALUE
				if iQuantity > -1 and cbOption.isActivate:
					szQuantity = u"%s" % (iQuantity, )
				szText = localText.getText("TXT_KEY_TRADE_ROUTES_CHECK_BOX_DO_NOT_EXCEED", (szQuantity, gc.getYieldInfo(self.ImpExpYield).getChar(), DestinationName, ))
				self.addCheckBoxYieldDescription(TradeRouteCheckBoxTypes.DO_NOT_EXCEED, iRow, szText, cbOption.isActivate)
			
			iRow += 1
			cbOption = pTraderoute.getCheckBoxOption(self.ImpExpYield, TradeRouteCheckBoxTypes.ALWAYS_KEEP)
			iQuantity = cbOption.iQuantity
			szQuantity = self.UKNOWN_VALUE
			if iQuantity > -1 and cbOption.isActivate:
				szQuantity = u"%s" % (iQuantity, )
			szText = localText.getText("TXT_KEY_TRADE_ROUTES_CHECK_BOX_ALWAYS_KEEP", (szQuantity, gc.getYieldInfo(self.ImpExpYield).getChar(), SourceName, ))
			self.addCheckBoxYieldDescription(TradeRouteCheckBoxTypes.ALWAYS_KEEP, iRow, szText, cbOption.isActivate)
			
			iRow += 1
			cbOption = pTraderoute.getCheckBoxOption(self.ImpExpYield, TradeRouteCheckBoxTypes.CONSERVE_NECESSARY_RESOURCES)
			szText = localText.getText("TXT_KEY_TRADE_ROUTES_CHECK_BOX_CONSERVE_NECESSARY_RESOURCES", (SourceName, ))
			self.addCheckBoxYieldDescription(TradeRouteCheckBoxTypes.CONSERVE_NECESSARY_RESOURCES, iRow, szText, cbOption.isActivate)
		else :
			#RADIOS
			iRow = 1
			radioOption = pTraderoute.getEuropeanRadioOption(self.ImpExpYield, TradeRouteRadioEuropeanTypes.DO_NOTHING)
			szText = localText.getText("TXT_KEY_TRADE_ROUTES_EUROPEAN_RADIO_DO_NOTHING", ())
			self.addRadioYieldDescription(TradeRouteRadioEuropeanTypes.DO_NOTHING, iRow, szText, radioOption.isActivate, self.CHANGE_ACTIVE_EUROPEAN_RADIO)
			
			iRow += 1
			radioOption = pTraderoute.getEuropeanRadioOption(self.ImpExpYield, TradeRouteRadioEuropeanTypes.BUY_QUANTITY)
			iQuantity = radioOption.iQuantity
			szQuantity = self.UKNOWN_VALUE
			if iQuantity > -1 and radioOption.isActivate:
				szQuantity = u"%s" % (iQuantity, )
			iQuantityPerTurn = radioOption.iQuantityPerTurn
			szQuantityPerTurn = ""
			# if iQuantityPerTurn > 0:
			# 	szQuantityPerTurn = localText.getText("TXT_KEY_TRADE_ROUTES_EUROPEAN_RADIO_BUY_QUANTITY_PER_TURN", (iQuantityPerTurn, gc.getYieldInfo(self.ImpExpYield).getChar(), ))
			szText = localText.getText("TXT_KEY_TRADE_ROUTES_EUROPEAN_RADIO_BUY_QUANTITY", (szQuantity, gc.getYieldInfo(self.ImpExpYield).getChar(), szQuantityPerTurn, ))
			self.addRadioYieldDescription(TradeRouteRadioEuropeanTypes.BUY_QUANTITY, iRow, szText, radioOption.isActivate, self.CHANGE_ACTIVE_EUROPEAN_RADIO)
			
			iRow += 1
			radioOption = pTraderoute.getEuropeanRadioOption(self.ImpExpYield, TradeRouteRadioEuropeanTypes.BUY_UNTIL_QUANTITY_REACHED)
			iQuantity = radioOption.iQuantity
			szBufferQuantity = self.UKNOWN_VALUE
			if iQuantity > -1 and radioOption.isActivate:
				szBufferQuantity = u"%s" % (iQuantity, )
			
			szText = localText.getText("TXT_KEY_TRADE_ROUTES_RADIO_ENSURE_THE_NEEDS", (DestinationName, szBufferQuantity, gc.getYieldInfo(self.ImpExpYield).getChar(), ))
			self.addRadioYieldDescription(TradeRouteRadioEuropeanTypes.BUY_UNTIL_QUANTITY_REACHED, iRow, szText, radioOption.isActivate, self.CHANGE_ACTIVE_EUROPEAN_RADIO)

			screen.addDDSGFCAt(self.getNextWidgetName(), self.YieldDescriptionPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_SMALL_LINE").getPath(), 10 + self.RADIO_SIZE, self.H_IMP_EXP_LIST/2 + 5, self.W_TRADE_ROUTES/2, 4, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
			#CHECKBOXES
			iRow = 1

			cbOption = pTraderoute.getCheckBoxOption(self.ImpExpYield, TradeRouteCheckBoxTypes.MAINTAIN_QUANTITY)
			iQuantity = cbOption.iQuantity
			szQuantity = self.UKNOWN_VALUE
			if iQuantity > -1 and cbOption.isActivate:
				szQuantity = u"%s" % (iQuantity, )
			szText = localText.getText("TXT_KEY_TRADE_ROUTE_EUROPEAN_RADIO_QUANTITY_PER_TURN_TEXT", (szQuantity, gc.getYieldInfo(self.ImpExpYield).getChar(), SourceName, ))
			self.addCheckBoxYieldDescription(TradeRouteCheckBoxTypes.MAINTAIN_QUANTITY, iRow, szText, cbOption.isActivate)
			
	def addCheckBoxYieldDescription(self, idCheckBox, iRow, szText, bActive):
		screen = self.getScreen()
		if bActive:
			szText = self.activeColor(szText)
			CheckBoxState = self.ACTIVATE_CHECK_BOX
			CheckBoxAction = self.INACTIVE_CHECK_BOX
		else:
			szText = self.unactiveColor(szText)
			CheckBoxState = self.DESACTIVATE_CHECK_BOX
			CheckBoxAction = self.ACTIVE_CHECK_BOX
		screen.setImageButtonAt(self.getNextWidgetName(), self.YieldDescriptionPanel, CheckBoxState, 10, self.H_IMP_EXP_LIST/2 + iRow*self.RADIO_SIZE, self.RADIO_SIZE, self.RADIO_SIZE, WidgetTypes.WIDGET_GENERAL, CheckBoxAction, idCheckBox)
		screen.setTextAt(self.getNextWidgetName(), self.YieldDescriptionPanel, u"<font=2>" + szText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, 10 + self.RADIO_SIZE, self.H_IMP_EXP_LIST/2 + iRow*self.RADIO_SIZE + self.RADIO_SIZE / 2, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CheckBoxAction, idCheckBox)

	def addRadioYieldDescription(self, idRadio, iRow, szText, bActivate, RadioAction):
		screen = self.getScreen()
		iRadioVal = idRadio
		if bActivate:
			szText = self.activeColor(szText)
			RadioState = self.ACTIVATE_RADIO
		else:
			szText = self.unactiveColor(szText)
			RadioState = self.DESACTIVATE_RADIO
			
		screen.setImageButtonAt(self.getNextWidgetName(), self.YieldDescriptionPanel, RadioState, 10, iRow*self.RADIO_SIZE, self.RADIO_SIZE, self.RADIO_SIZE, WidgetTypes.WIDGET_GENERAL, RadioAction, iRadioVal)
		screen.setTextAt(self.getNextWidgetName(), self.YieldDescriptionPanel, u"<font=2>" + szText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, 10 + self.RADIO_SIZE, iRow*self.RADIO_SIZE + self.RADIO_SIZE / 2, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, RadioAction, iRadioVal)
	
	def refreshFilteredTradeRoutes(self):
		pPlayer = self.pPlayer
		self.FilteredTradeRoutes = [] 
		self.CurrentTradeRoutePos = -1
		iPos = 0

		(loopTradeRoute, iter) = pPlayer.firstTradeRoute()
		while(loopTradeRoute):
			if(self.SourceCity == self.UNSELECT_ID or self.SourceCity == loopTradeRoute.getSourceCity().iID ):
				if(self.DestinationCity == self.UNSELECT_ID or self.DestinationCity == loopTradeRoute.getDestinationCity().iID ):
					if loopTradeRoute.getID() == self.SelectedRoute:
						self.CurrentTradeRoutePos = iPos
					iPos += 1
					self.FilteredTradeRoutes.append(loopTradeRoute)
			(loopTradeRoute, iter) = pPlayer.nextTradeRoute(iter)

		if self.CurrentTradeRoutePos == -1 and iPos > 0:
			self.CurrentTradeRoutePos = 0
			self.SelectedRoute = self.FilteredTradeRoutes[0].getID()

	def displayTradeRoutesView(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer

		szTitle = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_HEADER", ()).upper()
		self.displayTitle(szTitle)
		
		self.TradeRoutesPanel = self.getNextWidgetName() 
		screen.addPanel(self.TradeRoutesPanel, "", "", True, True, self.X_MID_VIEW, self.Y_TRADE_ROUTES, self.W_TRADE_ROUTES, self.H_TRADE_ROUTES, self.PanelType, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		self.displayedTradeRoutes = []
		iStartTradeRoute = 0

		iCurrentTradeRoutePos = self.CurrentTradeRoutePos
		

		iNumTradeRoute = len(self.FilteredTradeRoutes)
		self.CurrentTradeRoutePage = iCurrentTradeRoutePos / self.NUM_TRADE_ROUTES_BY_PAGE + 1
		iNumPages = (iNumTradeRoute-1)/self.NUM_TRADE_ROUTES_BY_PAGE + 1
		iMinTradeRoute = self.NUM_TRADE_ROUTES_BY_PAGE * (self.CurrentTradeRoutePage - 1)
		iMaxTradeRoute =  min(self.NUM_TRADE_ROUTES_BY_PAGE * self.CurrentTradeRoutePage, iNumTradeRoute)
		iNumTradeRouteOnPage = iMaxTradeRoute - iMinTradeRoute

		iPos = 0
		if iNumTradeRoute > 0:
			for iRoute in range(iNumTradeRouteOnPage):
				iIndex = iRoute+iMinTradeRoute
				loopTradeRoute = self.FilteredTradeRoutes[iIndex]
				
				szText = localText.getText("TXT_KEY_TRADE_ROUTES_ROW", (loopTradeRoute.getSourceCityName(), loopTradeRoute.getDestinationCityName(), ))
				if loopTradeRoute.getID() == self.SelectedRoute:
					szText = self.activeColor(szText)
				else :
					 szText = self.unactiveColor(szText)
				screen.setTextAt(self.getNextWidgetName(), self.TradeRoutesPanel, u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRADE_ROUTES_OFFSET, self.Y_TRADE_ROUTES_OFFSET + iPos*self.H_TRADE_ROUTES_OFFSET - self.H_TRADE_ROUTES_OFFSET/8, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.addDDSGFCAt(self.getNextWidgetName(), self.TradeRoutesPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_ROW_SEPARATION").getPath(), self.X_TRADE_ROUTES_OFFSET, self.Y_TRADE_ROUTES_OFFSET + iPos*self.H_TRADE_ROUTES_OFFSET + 12, self.W_TRADE_ROUTES - self.X_TRADE_ROUTES_OFFSET, 4, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
				screen.setImageButtonAt(self.getNextWidgetName(), self.TradeRoutesPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_REMOVE").getPath(), self.W_TRADE_ROUTES - self.W_TRADE_ROUTES_ICON , self.Y_TRADE_ROUTES_OFFSET + iPos*self.H_TRADE_ROUTES_OFFSET - self.H_TRADE_ROUTES_OFFSET / 2, self.W_TRADE_ROUTES_ICON, self.W_TRADE_ROUTES_ICON, WidgetTypes.WIDGET_GENERAL, self.REMOVE_ROUTE, loopTradeRoute.getID())
				screen.setImageButtonAt(self.getNextWidgetName(), self.TradeRoutesPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_MAGNIFYING_GLASS").getPath(), self.W_TRADE_ROUTES - self.W_TRADE_ROUTES_ICON * 2, self.Y_TRADE_ROUTES_OFFSET + iPos*self.H_TRADE_ROUTES_OFFSET - self.H_TRADE_ROUTES_OFFSET / 2, self.W_TRADE_ROUTES_ICON, self.W_TRADE_ROUTES_ICON, WidgetTypes.WIDGET_GENERAL, self.EDIT_ROUTE, loopTradeRoute.getID())
				#screen.setImageButtonAt(self.getNextWidgetName(), self.TradeRoutesPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_RENAME").getPath(), self.W_TRADE_ROUTES - self.W_TRADE_ROUTES_ICON * 3, self.Y_TRADE_ROUTES_OFFSET + iPos*self.H_TRADE_ROUTES_OFFSET - self.W_TRADE_ROUTES_ICON / 2, self.W_TRADE_ROUTES_ICON, self.W_TRADE_ROUTES_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setImageButtonAt(self.getNextWidgetName(), self.TradeRoutesPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_TRANSFERT_INVISIBLE").getPath(), self.X_TRADE_ROUTES_OFFSET, self.Y_TRADE_ROUTES_OFFSET + iPos*self.H_TRADE_ROUTES_OFFSET - self.H_TRADE_ROUTES_OFFSET/2, self.W_TRADE_ROUTES - self.X_TRADE_ROUTES_OFFSET - 2  - self.W_TRADE_ROUTES_ICON * 3, self.H_TRADE_ROUTES_OFFSET, WidgetTypes.WIDGET_GENERAL, self.CHANGE_SELECTED_ROUTE, loopTradeRoute.getID())
	
				iPos += 1

		if iNumPages > 1:
			#Navigation page of trade routes			
			if self.CurrentTradeRoutePage > 1:
				tradeRouteId = self.FilteredTradeRoutes[iMinTradeRoute - self.NUM_TRADE_ROUTES_BY_PAGE].getID()
				screen.setImageButtonAt(self.getNextWidgetName(), self.TradeRoutesPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_LEFT").getPath(), self.X_TRADE_ROUTE_ARROW_LEFT, self.Y_TRADE_ROUTE_ARROW, self.W_TRADE_ROUTE_ARROW, self.H_TRADE_ROUTE_ARROW, WidgetTypes.WIDGET_GENERAL, self.CHANGE_SELECTED_ROUTE_PAGE, tradeRouteId)
			else:
				screen.setImageButtonAt(self.getNextWidgetName(), self.TradeRoutesPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_LEFT_SHADOW").getPath(), self.X_TRADE_ROUTE_ARROW_LEFT, self.Y_TRADE_ROUTE_ARROW, self.W_TRADE_ROUTE_ARROW, self.H_TRADE_ROUTE_ARROW, WidgetTypes.WIDGET_GENERAL, -1, -1)
			if self.CurrentTradeRoutePage < iNumPages:
				tradeRouteId = self.FilteredTradeRoutes[iMinTradeRoute + self.NUM_TRADE_ROUTES_BY_PAGE].getID()
				screen.setImageButtonAt(self.getNextWidgetName(), self.TradeRoutesPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_RIGHT").getPath(), self.X_TRADE_ROUTE_ARROW_RIGHT, self.Y_TRADE_ROUTE_ARROW, self.W_TRADE_ROUTE_ARROW, self.H_TRADE_ROUTE_ARROW, WidgetTypes.WIDGET_GENERAL, self.CHANGE_SELECTED_ROUTE_PAGE, tradeRouteId)
			else:
				screen.setImageButtonAt(self.getNextWidgetName(), self.TradeRoutesPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_RIGHT_SHADOW").getPath(), self.X_TRADE_ROUTE_ARROW_RIGHT, self.Y_TRADE_ROUTE_ARROW, self.W_TRADE_ROUTE_ARROW, self.H_TRADE_ROUTE_ARROW, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			szPage = u"<font=3b>%d</font>" % (self.CurrentTradeRoutePage, )
			screen.setLabelAt(self.getNextWidgetName(), self.TradeRoutesPanel, self.mainColor(szPage), CvUtil.FONT_CENTER_JUSTIFY, self.X_TRADE_ROUTE_PAGINATION - self.xSize(1), self.Y_TRADE_ROUTE_ARROW + self.ySize(9), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
		# Description Trade Route View
		self.displayDescriptionTradeRouteView()

		# Keep automation in war time
		szText = localText.getText("TXT_KEY_PLAYER_OPTION_KEPT_AUTO_IN_WARTIME_HELP", ())
		if(pPlayer.isSecondaryOption(SecondaryPlayerOptionTypes.SECONDARYPLAYEROPTION_KEPT_AUTO_IN_WARTIME)):
			InterfaceRequirments = ArtFileMgr.getInterfaceArtInfo("INTERFACE_UNIT_COCHE_ACTIVATE").getPath()
			szText = self.activeColor(szText)
		else:
			InterfaceRequirments =  ArtFileMgr.getInterfaceArtInfo("INTERFACE_UNIT_COCHE_NO_ACTIVATE").getPath()
			szText = self.unactiveColor(szText)
		
		screen.setImageButton(self.getNextWidgetName(), InterfaceRequirments, self.X_KEPT_AUTO_IN_WARTIME, self.Y_KEPT_AUTO_IN_WARTIME - self.CHECKBOX_SIZE / 6, self.CHECKBOX_SIZE, self.CHECKBOX_SIZE, WidgetTypes.WIDGET_GENERAL, self.CHANGE_KEPT_AUTO_IN_WARTIME, -1)
		screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_KEPT_AUTO_IN_WARTIME + self.CHECKBOX_SIZE, self.Y_KEPT_AUTO_IN_WARTIME, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.CHANGE_KEPT_AUTO_IN_WARTIME, -1)
				
	def isExistingSource(self, idSource):
		pPlayer = self.pPlayer
		(loopTradeRoute, iter) = pPlayer.firstTradeRoute()
		while(loopTradeRoute):
			if idSource == loopTradeRoute.getSourceCity().iID:
				return True
			(loopTradeRoute, iter) = pPlayer.nextTradeRoute(iter)
		return False
		
	def isExistingDestination(self, idDestination):
		pPlayer = self.pPlayer
		(loopTradeRoute, iter) = pPlayer.firstTradeRoute()
		while(loopTradeRoute):
			if idDestination == loopTradeRoute.getDestinationCity().iID:
				return True
			(loopTradeRoute, iter) = pPlayer.nextTradeRoute(iter)
		return False

	def displayColoniesView(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer	
		
		if self.View != self.TRADE_ROUTES_VIEW:
			return

		szTitle = localText.getText("TXT_KEY_TRADE_ROUTES_FILTER_TITLE", ())
		if len(self.FilteredTradeRoutes) == 0:
			szTitle = localText.getText("TXT_KEY_TRADE_ROUTES_CHOICE_TITLE", ())
		
		screen.setLabel(self.getNextWidgetName(), "Background", "<font=3>" + self.mainColor(szTitle) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_LEFT_COLONY_PANEL_START + self.W_COLONY_PANEL/2, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION + self.H_SEPARATION - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
	
		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_SMALL_LINE").getPath(), self.X_LEFT_COLONY_PANEL_START + 10 + 2, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION + self.H_SEPARATION, self.W_COLONY_PANEL - 2*10, 8,  WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
		self.CityListLeft = self.getNextWidgetName()
		screen.addScrollPanel(self.CityListLeft, u"", self.X_LEFT_COLONY_PANEL_START + 5, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION + self.H_SEPARATION, self.W_COLONY_PANEL + 2, self.H_COLONY_PANEL - self.H_CITY_ANIMATION - 2 * self.Y_MARGIN_COLONY_PANEL - self.Y_MARGIN_COLONY_PANEL, self.PanelType, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		#Add Europe Row
		szText = localText.getText("TXT_KEY_EUROPE_SCREEN_TITLE", ())
		action = self.CHANGE_SOURCE_CITY
		if(self.SourceCity == self.EUROPE_ID):
			szText = self.activeColor(szText)
		elif(self.DestinationCity == self.EUROPE_ID or (self.DestinationCity != self.UNSELECT_ID and not pPlayer.getCity(self.DestinationCity).isCoastal(1))):
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_PLAYER_GRAY_WARM"))
			action = -1
		else:
			szText = self.unactiveColor(szText)

		screen.setTextAt(self.getNextWidgetName(), self.CityListLeft, u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W_COLONY_PANEL/2 - 13, 18, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, action, self.EUROPE_ID)
				
		#Add Colonies Rows
		if len(self.ColonyList) > 0:
			for iColony in range(len(self.ColonyList)):
				iNumTradeRoutes = self.ColonyList[iColony][0]
				pColony = self.ColonyList[iColony][1]
				szText = pColony.getName()
				action = self.CHANGE_SOURCE_CITY

				if(self.SourceCity == pColony.getID()):
					szText = self.activeColor(szText)
				elif(self.DestinationCity == pColony.getID() or (self.DestinationCity == self.EUROPE_ID and not pColony.isCoastal(1))):
					szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_PLAYER_GRAY_WARM"))
					action = -1
				else:
					szText = self.unactiveColor(szText)

				screen.setTextAt(self.getNextWidgetName(), self.CityListLeft, u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W_COLONY_PANEL/2 - 13, 18 + (iColony+1)*(self.H_COLONY_ROW + self.H_COLONY_ROW_OFFSET), 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, action, pColony.getID())
				
		
		screen.setLabel(self.getNextWidgetName(), "Background", "<font=3>" + self.mainColor(szTitle) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_RIGHT_COLONY_PANEL_START + self.W_COLONY_PANEL/2, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION + self.H_SEPARATION - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_SMALL_LINE").getPath(), self.X_RIGHT_COLONY_PANEL_START + 10 + 2, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION + self.H_SEPARATION, self.W_COLONY_PANEL - 2*10, 8,  WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		self.CityListRight = self.getNextWidgetName()
		screen.addScrollPanel(self.CityListRight, u"", self.X_RIGHT_COLONY_PANEL_START + 5, self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION + self.H_SEPARATION, self.W_COLONY_PANEL + 2, self.H_COLONY_PANEL - self.H_CITY_ANIMATION - 2 * self.Y_MARGIN_COLONY_PANEL - self.Y_MARGIN_COLONY_PANEL, self.PanelType, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		#Add Europe Row
		szText = localText.getText("TXT_KEY_EUROPE_SCREEN_TITLE", ())
		action = self.CHANGE_DESTINATION_CITY
		if(self.DestinationCity == self.EUROPE_ID):
			szText = self.activeColor(szText)
		elif(self.SourceCity == self.EUROPE_ID or (self.SourceCity != self.UNSELECT_ID and not pPlayer.getCity(self.SourceCity).isCoastal(1))):
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_PLAYER_GRAY_WARM"))
			action = -1
		else:
			szText = self.unactiveColor(szText)

		screen.setTextAt(self.getNextWidgetName(), self.CityListRight, u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W_COLONY_PANEL/2 - 13, 18, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, action, self.EUROPE_ID)
				
		#Add Colonies Rows
		if len(self.ColonyList) > 0:
			for iColony in range(len(self.ColonyList)):
				iNumTradeRoutes = self.ColonyList[iColony][0]
				pColony = self.ColonyList[iColony][1]
				szText = pColony.getName()
				action = self.CHANGE_DESTINATION_CITY
				if(self.DestinationCity == pColony.getID()):
					szText = self.activeColor(szText)
				elif(self.SourceCity == pColony.getID() or ( self.SourceCity == self.EUROPE_ID and not pColony.isCoastal(1))):
					szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_PLAYER_GRAY_WARM"))
					action = -1
				else:
					szText = self.unactiveColor(szText)
				screen.setTextAt(self.getNextWidgetName(), self.CityListRight, u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W_COLONY_PANEL/2 -10, 18 + (iColony+1)*(self.H_COLONY_ROW + self.H_COLONY_ROW_OFFSET), 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, action, pColony.getID())

	def displayDescriptionTradeRouteView(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer

		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_DESCRIPTION_BOX").getPath(), self.X_MID_VIEW, self.Y_DESCRIPTION_PANEL_SIZE, self.W_TRADE_ROUTES, self.H_DESCRIPTION_PANEL_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		self.DescriptionPanel = self.getNextWidgetName()
		screen.addPanel(self.DescriptionPanel, "", "", True, True, self.X_MID_VIEW, self.Y_DESCRIPTION_PANEL_SIZE, self.W_TRADE_ROUTES + 2*self.X_TRADE_ROUTES_OFFSET, self.H_DESCRIPTION_PANEL_SIZE, self.PanelType, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setLabelAt(self.getNextWidgetName(), self.DescriptionPanel, "<font=3b>" + self.mainColor(localText.getText("TXT_KEY_TRADE_ROUTES_DESCRPTION", ())) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W_TRADE_ROUTES/2, 13, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if self.SelectedRoute != self.UNSELECT_ID:
			pTraderoute = pPlayer.getTradeRoute(self.SelectedRoute)

			pTransportType = pTraderoute.getTransportType()
			if pTransportType == TransportTypes.ONLY_SHIP:
				screen.addDDSGFCAt(self.getNextWidgetName(), self.DescriptionPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_ICON_ONLY_SHIP").getPath(), self.X_ICON_TRANSPORT_TYPE - self.SMALL_ICON_TRANSPORT_TYPE_SIZE, self.Y_ICON_TRANSPORT_TYPE, self.SMALL_ICON_TRANSPORT_TYPE_SIZE, self.SMALL_ICON_TRANSPORT_TYPE_SIZE, WidgetTypes.WIDGET_GENERAL, self.ONLY_SHIP_HELP, -1, False )
			elif pTransportType == TransportTypes.ONLY_WAGON:
				screen.addDDSGFCAt(self.getNextWidgetName(), self.DescriptionPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_ICON_ONLY_WAGON").getPath(), self.X_ICON_TRANSPORT_TYPE - self.SMALL_ICON_TRANSPORT_TYPE_SIZE, self.Y_ICON_TRANSPORT_TYPE, self.SMALL_ICON_TRANSPORT_TYPE_SIZE, self.SMALL_ICON_TRANSPORT_TYPE_SIZE, WidgetTypes.WIDGET_GENERAL, self.ONLY_WAGON_HELP, -1, False )
			elif pTransportType == TransportTypes.SHIP_AND_WAGON:
				screen.addDDSGFCAt(self.getNextWidgetName(), self.DescriptionPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_ICON_SHIP_AND_WAGON").getPath(), self.X_ICON_TRANSPORT_TYPE - self.SMALL_ICON_TRANSPORT_TYPE_SIZE *2, self.Y_ICON_TRANSPORT_TYPE, self.SMALL_ICON_TRANSPORT_TYPE_SIZE * 2, self.SMALL_ICON_TRANSPORT_TYPE_SIZE, WidgetTypes.WIDGET_GENERAL, self.SHIP_AND_WAGON_HELP, -1, False )
			
			iRow = 2
			iCapacity = pTraderoute.getTransportUnitsCapacity()
			screen.setLabelAt(self.getNextWidgetName(), self.DescriptionPanel, "<font=3>" + self.descColor(localText.getText("TXT_KEY_TRADE_ROUTES_DESC_UNITS_CAPACITY", (iCapacity, ))) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ROW_DESC_OFFSET, iRow * self.W_ROW_DESC_OFFSET, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			iRow += 1
			iAverageLoad = pTraderoute.getLoadedCargoPercent()
			screen.setLabelAt(self.getNextWidgetName(), self.DescriptionPanel, "<font=3>" + self.descColor(localText.getText("TXT_KEY_TRADE_ROUTES_DESC_LOAD_AVERAGE", (iAverageLoad, ))) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ROW_DESC_OFFSET, iRow * self.W_ROW_DESC_OFFSET, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			iRow += 1
			iAverageLoadTenRotations = pTraderoute.getLoadedCargoHistPercent()
			screen.setLabelAt(self.getNextWidgetName(), self.DescriptionPanel, "<font=3>" + self.descColor(localText.getText("TXT_KEY_TRADE_ROUTES_DESC_LOAD_AVERAGE_X_ROTATION", (iAverageLoadTenRotations, gc.getNUM_TRADE_ROUTE_HIST_TURN(), ))) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ROW_DESC_OFFSET, iRow * self.W_ROW_DESC_OFFSET, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			ExportedYield = ""
			ImportedYield = ""
			for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				if gc.getYieldInfo(iYield).isCargo():
					if(pTraderoute.getTradeType(iYield) == TradeTypes.TRADE_EXPORT):
						if ExportedYield != "":
							ExportedYield += ", "
						ExportedYield += u"%c" % (gc.getYieldInfo(iYield).getChar(), )
					if(pTraderoute.getTradeType(iYield) == TradeTypes.TRADE_IMPORT):
						if ImportedYield != "":
							ImportedYield += ", "
						ImportedYield += u"%c" % (gc.getYieldInfo(iYield).getChar(), )
			if ExportedYield != "":
				iRow += 1
				screen.setLabelAt(self.getNextWidgetName(), self.DescriptionPanel, "<font=3>" + self.descColor(localText.getText("TXT_KEY_TRADE_ROUTES_DESC_EXPORTED_YIELD", (ExportedYield, ))) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ROW_DESC_OFFSET, iRow * self.W_ROW_DESC_OFFSET, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
			if ImportedYield != "":
				iRow += 1
				screen.setLabelAt(self.getNextWidgetName(), self.DescriptionPanel, "<font=3>" + self.descColor(localText.getText("TXT_KEY_TRADE_ROUTES_DESC_IMPORTED_YIELD", (ImportedYield, ))) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ROW_DESC_OFFSET, iRow * self.W_ROW_DESC_OFFSET, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			iRow += 1
			TradeProfits = pTraderoute.getTradeProfits()
			screen.setLabelAt(self.getNextWidgetName(), self.DescriptionPanel, "<font=3>" + self.descColor(localText.getText("TXT_KEY_TRADE_ROUTES_DESC_LAST_ROTATION_PROFITS", (TradeProfits, ))) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ROW_DESC_OFFSET, iRow * self.W_ROW_DESC_OFFSET, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			iRow += 1
			TradeProfitsHist = pTraderoute.getTradeProfitsHist()
			screen.setLabelAt(self.getNextWidgetName(), self.DescriptionPanel, "<font=3>" + self.descColor(localText.getText("TXT_KEY_TRADE_ROUTES_DESC_LAST_X_ROTATION_PROFITS", (TradeProfitsHist, gc.getNUM_TRADE_ROUTE_HIST_TURN(), ))) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ROW_DESC_OFFSET, iRow * self.W_ROW_DESC_OFFSET, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			iRow += 1
			TotalProfits = pTraderoute.getTotalProfits()
			screen.setLabelAt(self.getNextWidgetName(), self.DescriptionPanel, "<font=3>" + self.descColor(localText.getText("TXT_KEY_TRADE_ROUTES_DESC_TOTAL_PROFITS", (TotalProfits, ))) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ROW_DESC_OFFSET, iRow * self.W_ROW_DESC_OFFSET, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def routeHasYields(self, pTraderoute):
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				if(pTraderoute.getTradeType(iYield) == TradeTypes.TRADE_EXPORT):
					return True
				if(pTraderoute.getTradeType(iYield) == TradeTypes.TRADE_IMPORT):
					return True
		return False

	def displayTradeRouteGroups(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer
		if self.SelectedRoute == self.UNSELECT_ID:
			return

		szTitle = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_HEADER_EDITING_ROUTE_TRANSPORTS", ()).upper()
		self.displayTitle(szTitle)
		
		pTraderoute = pPlayer.getTradeRoute(self.SelectedRoute)
		# DESCIPTION PANEL
		self.displayTopDescritptionRoute(pTraderoute)

		# YIELD VIEW BUTTON
		
		if(self.routeHasYields(pTraderoute)):
			YieldsViewButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_YIELDS_VIEW_EYE_BUTTON").getPath()
		else:
			YieldsViewButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_YIELDS_VIEW_BUTTON").getPath()

		screen.setImageButton(self.getNextWidgetName(), YieldsViewButton, self.X_MID_VIEW + self.W_TRADE_ROUTES - self.W_TRANSPORTS_VIEW_BUTTON, self.Y_TRADE_ROUTES + self.H_DESC_CREATE_ROUTE, self.W_TRANSPORTS_VIEW_BUTTON, self.H_TRANSPORTS_VIEW_BUTTON, WidgetTypes.WIDGET_GENERAL, self.CHANGE_VIEW, self.EDIT_ROUTE_VIEW )
		
		self.Fleets = []
		pSelectionGroup, Iterator = pPlayer.firstSelectionGroup(false)
		while (pSelectionGroup != None):
			if (pSelectionGroup.isAssignedTradeRoute(self.SelectedRoute)):
				self.Fleets.append(pSelectionGroup)
				if(self.SelectedGroupId == -1):
					self.SelectedGroupId = pSelectionGroup.getID()
			pSelectionGroup, Iterator = pPlayer.nextSelectionGroup(Iterator, false)

		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_DESCRIPTION_BOX").getPath(), self.X_FLEETS_PANEL, self.Y_FLEETS_PANEL, self.W_FLEETS_PANEL + self.X_FLEET_START * 2, self.H_FLEETS_PANEL + self.Y_FLEET_START * 3 / 2, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		fleetsPanel = self.getNextWidgetName()
		screen.addScrollPanel(fleetsPanel, u"", self.X_FLEETS_PANEL + 5, self.Y_FLEETS_PANEL, self.W_FLEETS_PANEL + 5, self.H_FLEETS_PANEL - 10, PanelStyles.PANEL_STYLE_MAIN, True, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
			
		iNumFleets = len(self.Fleets)

		screen.addDDSGFCAt(self.getNextWidgetName(), fleetsPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_ADD_CONVOY_SMALL").getPath(), self.X_FLEET_START, self.Y_FLEET_START + self.ySize(1), self.FLEET_BOX_SIZE_SMALL, self.FLEET_BOX_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
		screen.addDDSGFCAt(self.getNextWidgetName(), fleetsPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_ARROW_RIGHT_BOTTOM").getPath(), self.X_FLEET_START - self.W_ARROW_RIGHT_BOTTOM_SIZE /2, self.Y_FLEET_START + (self.FLEET_BOX_SIZE - self.H_ARROW_RIGHT_BOTTOM_SIZE)/4, self.W_ARROW_RIGHT_BOTTOM_SIZE, self.H_ARROW_RIGHT_BOTTOM_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
		screen.setImageButtonAt(self.getNextWidgetName(), fleetsPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_TRANSFERT_INVISIBLE").getPath(), self.X_FLEET_START, self.Y_FLEET_START + self.ySize(1), self.FLEET_BOX_SIZE_SMALL, self.FLEET_BOX_SIZE, WidgetTypes.WIDGET_GENERAL, self.CHANGE_VIEW, self.EDIT_ROUTE_ADD_TRANSPORTS_VIEW)
	
		for iFleet in range(iNumFleets):
			pGroup = self.Fleets[iFleet]
			szShipPane = self.getNextWidgetName()
			pUnit = pGroup.getMostPowerfulUnit()

			xPanelShip = self.X_FLEET_START + (self.FLEET_BOX_SIZE_SMALL +self.X_FLEET_OFFSET) + (iFleet)*(self.FLEET_BOX_SIZE+self.X_FLEET_OFFSET)
			screen.attachPanelAt(fleetsPanel, szShipPane, "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY, xPanelShip, self.Y_FLEET_START, self.FLEET_BOX_SIZE, self.FLEET_BOX_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.displayTransportUnit(pGroup, szShipPane)
			xOffset = 0
			if gc.getUnitInfo(pUnit.getUnitType()).isMechUnit():
				if (pUnit.canChooseSeaway()):	
					screen.setImageButtonAt(self.getNextWidgetName(), fleetsPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_WHICH_SEAWAYS").getPath(), xPanelShip + xOffset + self.xSize(5), self.Y_FLEET_START - self.ICON_ON_SHIP * 2 / 5, self.ICON_ON_SHIP, self.ICON_ON_SHIP, WidgetTypes.WIDGET_GENERAL, self.DISPLAY_SEAWAY_VIEW, pGroup.getID())
				else:
					screen.setImageButtonAt(self.getNextWidgetName(), fleetsPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_NO_WHICH_SEAWAYS").getPath(), xPanelShip + xOffset + self.xSize(5), self.Y_FLEET_START - self.ICON_ON_SHIP * 2 / 5, self.ICON_ON_SHIP, self.ICON_ON_SHIP, WidgetTypes.WIDGET_GENERAL, -1, -1)
				xOffset += self.ICON_ON_SHIP

			if pGroup.getNumUnits() > 1:
				screen.setImageButtonAt(self.getNextWidgetName(), fleetsPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EJECT_UNIT_TO_GROUP").getPath(), xPanelShip + xOffset + self.xSize(5), self.Y_FLEET_START - self.ICON_ON_SHIP * 2 / 5, self.ICON_ON_SHIP, self.ICON_ON_SHIP, WidgetTypes.WIDGET_GENERAL, self.EJECT_UNIT_TO_GROUP, pUnit.getID())
		
		# Check boxes options
		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_DESCRIPTION_BOX").getPath(), self.X_FLEETS_PANEL, self.Y_FLEET_ACTION_PANEL, self.W_FLEETS_PANEL + self.X_FLEET_START * 2, self.H_FLEET_ACTION_PANEL, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.GroupOptionsPanel = self.getNextWidgetName()
		screen.addScrollPanel(self.GroupOptionsPanel, u"", self.X_FLEETS_PANEL + 5, self.Y_FLEET_ACTION_PANEL, self.W_FLEETS_PANEL + self.X_FLEET_START * 2 + 5, self.H_FLEET_ACTION_PANEL -10, PanelStyles.PANEL_STYLE_MAIN, True, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_SPECIFIC_OPTIONS", ())
		screen.setLabelAt(self.getNextWidgetName(), self.GroupOptionsPanel, u"<font=4>" + self.mainColor(szText) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, (self.W_FLEETS_PANEL + self.X_FLEET_START * 2 + 5) / 2, self.ySize(10), 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iRow = 0
		if self.SelectedGroupId == -1:
			return
		pGroup = pPlayer.getSelectionGroup(self.SelectedGroupId)

		szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_STOP_CONVOY", ())
		self.addCheckBoxGroups(TradeRouteCheckBoxGroupsTypes.STOP_CONVOY, iRow, szText, pGroup.shouldStopConvoy())
		iRow += 1

		szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_AUTO_HEAL", ())
		self.addCheckBoxGroups(TradeRouteCheckBoxGroupsTypes.AUTO_HEAL, iRow, szText, pGroup.shouldAutoHeal())
		iRow += 1

		# Have to disable RESUPPLY_AUTO because it cause an exe crash to add variable on CvSelectionGroup ... 
		# szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_RESUPPLY_AUTO", ())
		# self.addCheckBoxGroups(TradeRouteCheckBoxGroupsTypes.RESUPPLY_AUTO, iRow, szText, pGroup.shouldResupplyAuto())
		# iRow += 1
		szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_RESUPPLY_AUTO", ())
		screen.setTextAt(self.getNextWidgetName(), self.GroupOptionsPanel, u"<font=3>" + self.activeColor(szText) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.xSize(10), self.ySize(35) + iRow*self.RADIO_SIZE + self.RADIO_SIZE / 2, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iRow += 1

		#Seaways
		if self.DisplaySeawayView:
			self.displaySeawayView()

	def addCheckBoxGroups(self, idCheckBox, iRow, szText, bActive):
		screen = self.getScreen()
		CheckBoxAction = self.CHECK_BOX_GROUPS
		if bActive:
			szText = self.activeColor(szText)
			CheckBoxState = self.ACTIVATE_CHECK_BOX
		else:
			szText = self.unactiveColor(szText)
			CheckBoxState = self.DESACTIVATE_CHECK_BOX
		screen.setImageButtonAt(self.getNextWidgetName(), self.GroupOptionsPanel, CheckBoxState, self.xSize(10), self.ySize(35) + iRow*self.RADIO_SIZE, self.RADIO_SIZE, self.RADIO_SIZE, WidgetTypes.WIDGET_GENERAL, CheckBoxAction, idCheckBox)
		screen.setTextAt(self.getNextWidgetName(), self.GroupOptionsPanel, u"<font=3>" + szText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.xSize(10) + self.RADIO_SIZE, self.ySize(35) + iRow*self.RADIO_SIZE + self.RADIO_SIZE / 2, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CheckBoxAction, idCheckBox)

	def displayTransportUnit(self, pGroup, szUnitPane):
		screen = self.getScreen()
		pPlayer = self.pPlayer
		pUnit = pGroup.getMostPowerfulUnit()

		szName = pUnit.getName() 
		ArtBox = ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_IN_PORT_BOX_SQUARE").getPath()
		if self.SelectedGroupId == pGroup.getID():
			ArtBox = ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_IN_PORT_BOX_SQUARE_GRAY_SELECTED").getPath()
			szName = self.activeColor(szName)			

		screen.addDDSGFCAt(self.getNextWidgetName(), szUnitPane, ArtBox, 0, 0, self.FLEET_BOX_SIZE, self.FLEET_BOX_SIZE - self.ySize(1), WidgetTypes.WIDGET_TRADE_ROUTE_MOVE_TRANSPORT_TO_TRANSPORT, pUnit.getID(), pPlayer.getID(), False)
		screen.setImageButtonAt(self.getNextWidgetName(), szUnitPane, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_TRANSFERT_INVISIBLE").getPath(), 0, 0, self.FLEET_BOX_SIZE, self.FLEET_BOX_SIZE - self.ySize(1), WidgetTypes.WIDGET_TRADE_ROUTE_MOVE_TRANSPORT_TO_TRANSPORT, pUnit.getID(), pPlayer.getID())
		
		screen.setLabelAt(self.getNextWidgetName(), szUnitPane, "<font=2>" + szName + "</font>", CvUtil.FONT_LEFT_JUSTIFY, 6, self.FLEET_BOX_SIZE*7/8, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		xChange = 0
		if pUnit.getDomainType() != DomainTypes.DOMAIN_SEA:
			xChange = self.FLEET_BOX_SIZE/3
		screen.addDragableButtonAt(szUnitPane, self.getNextWidgetName(), pUnit.getFullLengthIcon(), "", 0 + xChange/2, 0 + xChange/3, self.FLEET_BOX_SIZE*3/4 - xChange, self.FLEET_BOX_SIZE*3/4 - xChange/4, WidgetTypes.WIDGET_TRADE_ROUTE_MOVE_TRANSPORT_TO_TRANSPORT, pUnit.getID(), pPlayer.getID(), ButtonStyles.BUTTON_STYLE_IMAGE)
		szText = localText.changeTextColor(u"x%d" %(pGroup.getNumUnits()), gc.getInfoTypeForString("COLOR_YELLOW"))
		screen.setLabelAt( self.getNextWidgetName(), szUnitPane, "<font=4b>" + szText + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.FLEET_BOX_SIZE - self.xSize(5), self.FLEET_BOX_SIZE/4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if pGroup.shouldWaitForMerging():
			screen.addDDSGFCAt(self.getNextWidgetName(), szUnitPane, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_CHAIN").getPath(), self.FLEET_BOX_SIZE*4/5 - self.xSize(5), self.FLEET_BOX_SIZE*4/5 - self.ySize(3), self.FLEET_BOX_SIZE/5, self.FLEET_BOX_SIZE/5, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

	def displaySeawayView(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer
		pTraderoute = pPlayer.getTradeRoute(self.SelectedRoute)
		if self.SelectedGroupId == -1:
			return
		pGroup = pPlayer.getSelectionGroup(self.SelectedGroupId)

		#Seaway Panel
		self.SeawayPanel = self.getNextWidgetName()
		screen.addPanel(self.SeawayPanel, u"", u"", True, False, 0, 0, self.XResolution, self.YResolution, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)		
		screen.addDrawControl(self.SeawayPanel,  ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SEAWAY_BOX").getPath(), self.X_SEAWAY_PANEL, self.Y_SEAWAY_PANEL, self.W_SEAWAY_PANEL, self.H_SEAWAY_PANEL, WidgetTypes.WIDGET_GENERAL, -1, -1)		
		
		screen.setImageButtonAt(self.getNextWidgetName(), self.SeawayPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_CLOSE").getPath(), self.W_SEAWAY_PANEL - self.CLOSE_BUTTON_SIZE * 6 / 5 , self.CLOSE_BUTTON_SIZE / 5, self.CLOSE_BUTTON_SIZE, self.CLOSE_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, self.EXIT_SEAWAY_VIEW, -1)

		self.addMinimap()

		szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_SEAWAY_TITLE", ())
		screen.setTextAt(self.getNextWidgetName(), self.SeawayPanel, u"<font=3>" + self.mainColor(szText) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SEAWAY_ROW + self.W_SEAWAY_ROW_SEPARATION / 2, self.Y_SEAWAY_TITLE, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
		currentSeawayID = pGroup.getSeawayId()
		
		if currentSeawayID == -1:
			szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_SEAWAY_EXPLANATION_DEFAULT", ())
			screen.attachMultilineTextAt(self.SeawayPanel, self.getNextWidgetName(), u"<font=2>" + self.blackColor(szText) + u"</font>", self.X_SEAWAY_ROW, self.Y_MULTILINE_SEAWAY_DESCRIPTION, self.W_SEAWAY_ROW_SEPARATION * 9 / 8, self.H_MULTILINE_SEAWAY_DESCRIPTION, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		else:
			pSeaway = pPlayer.getSeawayByID(currentSeawayID)
			szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_SEAWAY_SELECTED", (pSeaway.getName(), ))
			screen.attachMultilineTextAt(self.SeawayPanel, self.getNextWidgetName(), u"<font=2>" + self.blackColor(szText) + u"</font>", self.X_SEAWAY_ROW, self.Y_MULTILINE_SEAWAY_DESCRIPTION, self.W_SEAWAY_ROW_SEPARATION * 9 / 8, self.H_MULTILINE_SEAWAY_SELECTED_DESCRIPTION, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
			screen.addDDSGFCAt(self.getNextWidgetName(), self.SeawayPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_ROW_SEPARATION").getPath(), self.X_SEAWAY_ROW + self.W_SEAWAY_ROW_SEPARATION/4, self.Y_MULTILINE_SEAWAY_DESCRIPTION + self.H_MULTILINE_SEAWAY_SELECTED_DESCRIPTION, self.W_SEAWAY_ROW_SEPARATION/2, self.H_SEAWAY_ROW_SEPARATION, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
			# Check Box
			szText = self.unactiveColor(localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_SEAWAY_CHECK_BOX", ()))
			screen.setImageButtonAt(self.getNextWidgetName(), self.SeawayPanel, self.DESACTIVATE_CHECK_BOX, self.X_SEAWAY_ROW, self.Y_MULTILINE_SEAWAY_DESCRIPTION + self.H_MULTILINE_SEAWAY_SELECTED_DESCRIPTION + self.H_SEAWAY_ROW_SEPARATION, self.RADIO_SIZE, self.RADIO_SIZE, WidgetTypes.WIDGET_GENERAL, self.ACTIVE_SEAWAY_CHECK_BOX, -1)
			screen.setTextAt(self.getNextWidgetName(), self.SeawayPanel, u"<font=2>" + szText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_SEAWAY_ROW + self.RADIO_SIZE, self.Y_MULTILINE_SEAWAY_DESCRIPTION + self.H_MULTILINE_SEAWAY_SELECTED_DESCRIPTION + self.H_SEAWAY_ROW_SEPARATION + self.RADIO_SIZE / 2, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.ACTIVE_SEAWAY_CHECK_BOX, -1)
			#Text
			szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_SEAWAY_OTHER", ())
			screen.attachMultilineTextAt(self.SeawayPanel, self.getNextWidgetName(), u"<font=2>" + self.blackColor(szText) + u"</font>", self.X_SEAWAY_ROW, self.Y_MULTILINE_SEAWAY_DESCRIPTION_OTHER, self.W_SEAWAY_ROW_SEPARATION * 9 / 8, self.H_MULTILINE_SEAWAY_SELECTED_DESCRIPTION_OTHER, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
			
		lSeaways = self.getSeaways()
		iNumSeaways = len(lSeaways)
		bShowArrow = iNumSeaways > 1
		iNumPages = (iNumSeaways-1)/self.NUM_SEAWAYS_BY_PAGE + 1
		iMinSeaway = self.NUM_SEAWAYS_BY_PAGE * (self.CurrentSeawayPage - 1)
		iMaxSeaway =  min(self.NUM_SEAWAYS_BY_PAGE * self.CurrentSeawayPage, iNumSeaways)
		iNumSeawayOnPage = iMaxSeaway - iMinSeaway
		
		for index in range(iNumSeawayOnPage):
			iPosSeaway = index+iMinSeaway
			iStepDistance = lSeaways[iPosSeaway][0]
			loopSeaway = lSeaways[iPosSeaway][1]
			szSeaway = loopSeaway.getName()
			szStepDistance = u"%d." % (iStepDistance, )
			if currentSeawayID == loopSeaway.getID():
			 	szSeaway = self.activeColor(szSeaway)
			 	szStepDistance = self.activeColor(szStepDistance)
			else :
			 	szSeaway = self.unactiveColor(szSeaway)
			 	szStepDistance = self.unactiveColor(szStepDistance)
			screen.addDDSGFCAt(self.getNextWidgetName(), self.SeawayPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_ROW_SEPARATION").getPath(), self.X_SEAWAY_ROW, self.Y_SEAWAY_ROW + index*self.H_SEAWAY_ROW + self.ySize(10), self.W_SEAWAY_ROW_SEPARATION, self.H_SEAWAY_ROW_SEPARATION, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
			
			screen.setTextAt(self.getNextWidgetName(), self.SeawayPanel, u"<font=3>" + szSeaway + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_SEAWAY_ROW + self.W_SEAWAY_ARROW, self.Y_SEAWAY_ROW + index*self.H_SEAWAY_ROW, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, iPosSeaway)
			screen.setTextAt(self.getNextWidgetName(), self.SeawayPanel, u"<font=3>" + szStepDistance + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SEAWAY_ROW + self.W_SEAWAY_ARROW/2, self.Y_SEAWAY_ROW + index*self.H_SEAWAY_ROW, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, self.SELECT_SEAWAY_HELP, iPosSeaway)
			screen.setImageButtonAt("SelectSeaway" + str(iPosSeaway), self.SeawayPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_TRANSFERT_INVISIBLE").getPath(), self.X_SEAWAY_ROW + self.W_SEAWAY_ARROW, self.Y_SEAWAY_ROW + index*self.H_SEAWAY_ROW - self.ySize(10), self.W_SEAWAY_ROW_SEPARATION * 3 / 4, self.H_SEAWAY_ROW, WidgetTypes.WIDGET_GENERAL, self.SELECT_SEAWAY, iPosSeaway)
			screen.setImageButtonAt(self.getNextWidgetName(), self.SeawayPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_REMOVE").getPath(), self.X_SEAWAY_ROW + self.W_SEAWAY_ROW_SEPARATION - self.SEAWAY_ICON_SIZE, self.Y_SEAWAY_ROW + index*self.H_SEAWAY_ROW - self.ySize(10), self.SEAWAY_ICON_SIZE, self.SEAWAY_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, self.REMOVE_SEAWAY, iPosSeaway)
			screen.setImageButtonAt(self.getNextWidgetName(), self.SeawayPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_RENAME").getPath(), self.X_SEAWAY_ROW + self.W_SEAWAY_ROW_SEPARATION - self.SEAWAY_ICON_SIZE*2 , self.Y_SEAWAY_ROW + index*self.H_SEAWAY_ROW - self.ySize(8), self.SEAWAY_ICON_SIZE, self.SEAWAY_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, self.RENAME_SEAWAY, iPosSeaway)
	
		#Navigation page of seaway			
		if self.CurrentSeawayPage > 1:
			screen.setImageButtonAt(self.getNextWidgetName(), self.SeawayPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_LEFT").getPath(), self.X_SEAWAY_ARROW_LEFT, self.Y_SEAWAY_ARROW, self.W_SEAWAY_ARROW, self.H_SEAWAY_ARROW, WidgetTypes.WIDGET_GENERAL, self.CHANGE_SEAWAY_PAGE, -1)
		else:
			screen.setImageButtonAt(self.getNextWidgetName(), self.SeawayPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_LEFT_SHADOW").getPath(), self.X_SEAWAY_ARROW_LEFT, self.Y_SEAWAY_ARROW, self.W_SEAWAY_ARROW, self.H_SEAWAY_ARROW, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if self.CurrentSeawayPage < iNumPages:
			screen.setImageButtonAt(self.getNextWidgetName(), self.SeawayPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_RIGHT").getPath(), self.X_SEAWAY_ARROW_RIGHT, self.Y_SEAWAY_ARROW, self.W_SEAWAY_ARROW, self.H_SEAWAY_ARROW, WidgetTypes.WIDGET_GENERAL, self.CHANGE_SEAWAY_PAGE, 1)
		else:
			screen.setImageButtonAt(self.getNextWidgetName(), self.SeawayPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_RIGHT_SHADOW").getPath(), self.X_SEAWAY_ARROW_RIGHT, self.Y_SEAWAY_ARROW, self.W_SEAWAY_ARROW, self.H_SEAWAY_ARROW, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szPage = u"<font=3b>%d</font>" % (self.CurrentSeawayPage, )
		screen.setLabelAt(self.getNextWidgetName(), self.SeawayPanel, self.mainColor(szPage), CvUtil.FONT_CENTER_JUSTIFY, self.X_SEAWAY_PAGINATION - self.xSize(1), self.Y_SEAWAY_ARROW + self.ySize(9), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
	def addMinimap(self):
		screen = self.getScreen()
		
		screen.show("_FXS_Screen_Bogus_Minimap_Name")
		screen.moveToFront("_FXS_Screen_Bogus_Minimap_Name")
		screen.minimapClearAllFlashingTiles()
		screen.minimapClearLayer(0)
		screen.updateMinimapSection(False)

		iOldMode = CyInterface().getShowInterface()
		CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_MINIMAP_ONLY)
		screen.updateMinimapVisibility()
		CyInterface().setShowInterface(iOldMode)
		self.refreshMinimap()

	def refreshMinimap(self):
		screen = self.getScreen()	
		screen.minimapClearAllFlashingTiles()
		screen.updateMinimapVisibility()
		screen.minimapClearLayer(0)
		
		pPlayer = self.pPlayer
		
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if ( pLoopPlayer.isAlive() and gc.getTeam(pLoopPlayer.getTeam()).isHasMet((pPlayer).getTeam())):
				screen.updateMinimapColorFromMap(MinimapModeTypes.MINIMAPMODE_TERRITORY, iLoopPlayer, 0.4)
		
		
		iColor = gc.getPlayerColorInfo(pPlayer.getPlayerColor()).getColorTypePrimary()
		
		iNumSeaways = pPlayer.getNumSeaways()
		for index in range(iNumSeaways):
			loopSeaway = pPlayer.getSeaway(index)
			pPlot = loopSeaway.plot()
			screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_MILITARY, pPlot.getX(), pPlot.getY(), iColor, 0.7)
		
		self.flashSourceCity()

	def displaySourceAndDestinationGroups(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer
		if self.SelectedRoute == self.UNSELECT_ID:
			return

		szTitle = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_HEADER_EDITING_ROUTE_TRANSPORTS", ()).upper()
		self.displayTitle(szTitle)
		
		pTraderoute = pPlayer.getTradeRoute(self.SelectedRoute)

		# DESCIPTION PANEL
		self.displayTopDescritptionRoute(pTraderoute)

		xOffset = 0
		# YIELD VIEW BUTTON
		if(self.routeHasYields(pTraderoute)):
			YieldsViewButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_YIELDS_VIEW_EYE_BUTTON").getPath()
		else:
			YieldsViewButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_YIELDS_VIEW_BUTTON").getPath()
		screen.setImageButton(self.getNextWidgetName(), YieldsViewButton, self.X_MID_VIEW + self.W_TRADE_ROUTES - self.W_TRANSPORTS_VIEW_BUTTON, self.Y_TRADE_ROUTES + self.H_DESC_CREATE_ROUTE, self.W_TRANSPORTS_VIEW_BUTTON, self.H_TRANSPORTS_VIEW_BUTTON, WidgetTypes.WIDGET_GENERAL, self.CHANGE_VIEW, self.EDIT_ROUTE_VIEW )
		xOffset -= self.W_TRANSPORTS_VIEW_BUTTON
		
		# TRANSPORTS VIEW BUTTON
		iCapacity = pTraderoute.getTransportUnitsCapacity()
			
		if iCapacity > 0:
			screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_TRANSPORTS_VIEW_EYE_BUTTON").getPath(), self.X_MID_VIEW + self.W_TRADE_ROUTES - self.W_TRANSPORTS_VIEW_BUTTON + xOffset, self.Y_TRADE_ROUTES + self.H_DESC_CREATE_ROUTE, self.W_TRANSPORTS_VIEW_BUTTON, self.H_TRANSPORTS_VIEW_BUTTON, WidgetTypes.WIDGET_GENERAL, self.CHANGE_VIEW, self.EDIT_ROUTE_TRANSPORTS_VIEW )
		
		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_DESCRIPTION_BOX").getPath(), self.X_ADD_FLEETS_PANEL, self.Y_ADD_FLEETS_PANEL, self.W_ADD_FLEETS_PANEL, self.H_ADD_FLEETS_PANEL, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addScrollPanel("AddSourceFleetsPanel", u"", self.X_ADD_FLEETS_PANEL + self.xSize(5), self.Y_ADD_FLEETS_PANEL, self.W_ADD_FLEETS_PANEL - self.xSize(8), self.H_ADD_FLEETS_PANEL*9/10 - self.ySize(5), PanelStyles.PANEL_STYLE_MAIN, True, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_AVAILABLE_TRANSPORTS_TO_CITY", (pTraderoute.getSourceCityName(), ))
		if pTraderoute.getSourceCity().iID == self.EUROPE_ID:
			szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_AVAILABLE_TRANSPORTS_TO_EUROPE", ())
		screen.setLabel(self.getNextWidgetName(), "Background", "<font=3>" +  self.descColor(szText) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_ADD_FLEETS_PANEL + self.W_ADD_FLEETS_PANEL/2 - self.xSize(5), self.Y_ADD_FLEETS_PANEL + self.ySize(5), 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		

		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_DESCRIPTION_BOX").getPath(), self.X_ADD_FLEETS_PANEL_RIGHT, self.Y_ADD_FLEETS_PANEL, self.W_ADD_FLEETS_PANEL, self.H_ADD_FLEETS_PANEL, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addScrollPanel("AddDestinationFleetsPanel", u"", self.X_ADD_FLEETS_PANEL_RIGHT + self.xSize(5), self.Y_ADD_FLEETS_PANEL, self.W_ADD_FLEETS_PANEL - self.xSize(8), self.H_ADD_FLEETS_PANEL*9/10 - self.ySize(5), PanelStyles.PANEL_STYLE_MAIN, True, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_AVAILABLE_TRANSPORTS_TO_CITY", (pTraderoute.getDestinationCityName(), ))
		if pTraderoute.getDestinationCity().iID == self.EUROPE_ID:
			szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_AVAILABLE_TRANSPORTS_TO_EUROPE", ())
		screen.setLabel(self.getNextWidgetName(), "Background", "<font=3>" +  self.descColor(szText) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_ADD_FLEETS_PANEL_RIGHT + self.W_ADD_FLEETS_PANEL/2 - self.xSize(5), self.Y_ADD_FLEETS_PANEL + self.ySize(5), 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		AreaMidlePanel = self.getNextWidgetName()
		screen.addDDSGFC(AreaMidlePanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_DESCRIPTION_BOX").getPath(), self.X_MIDDLE_AREA_FLEETS_PANEL, self.Y_MIDDLE_AREA_FLEETS_PANEL, self.W_MIDDLE_AREA_FLEETS_PANEL, self.H_MIDDLE_AREA_FLEETS_PANEL, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		szText = self.warningColor(localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_AREA_MIDDLE_HELP", ()))
		if self.LastAreaUnitsText != "":
			szText = self.LastAreaUnitsText
		screen.attachMultilineTextAt(AreaMidlePanel, self.getNextWidgetName(), u"<font=4>" + szText + u"</font>", self.W_MIDDLE_AREA_FLEETS_PANEL/10, self.H_MIDDLE_AREA_FLEETS_PANEL/4, self.W_MIDDLE_AREA_FLEETS_PANEL*8/10, self.H_MIDDLE_AREA_FLEETS_PANEL/2, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)	
		screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_TRANSFERT_INVISIBLE").getPath(), self.X_MIDDLE_AREA_FLEETS_PANEL, self.Y_MIDDLE_AREA_FLEETS_PANEL, self.W_MIDDLE_AREA_FLEETS_PANEL, self.H_MIDDLE_AREA_FLEETS_PANEL, WidgetTypes.WIDGET_ADD_TRANSPORT_AREA_TO_TRADE_ROUTES, self.SelectedRoute, -1 )

		self.updateSourceOrDestinationFleet(pTraderoute)
		iNumFleetByRow = 2
		iNumSourceFleet = len(self.SourceFleets)
		if iNumSourceFleet == 0:
			idSourceCity = pTraderoute.getSourceCity().iID
			if idSourceCity != self.EUROPE_ID:
				pSourceCity = pPlayer.getCity(idSourceCity)
				szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_NO_TRANSPORT_UNIT_AVAILABLE_IN_CITY", (pSourceCity.getName(), ))
			else:
				szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_NO_TRANSPORT_UNIT_AVAILABLE_IN_EUROPE", ())
			screen.attachMultilineTextAt("AddSourceFleetsPanel", self.getNextWidgetName(),  u"<font=4>" + localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_PLAYER_DARK_RED")) + u"</font>", self.W_ADD_FLEETS_PANEL/12, self.H_MIDDLE_AREA_FLEETS_PANEL/8, self.W_ADD_FLEETS_PANEL*8/10, self.H_MIDDLE_AREA_FLEETS_PANEL*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)	
			
		for iFleet in range(iNumSourceFleet):
			row = iFleet/iNumFleetByRow
			column = iFleet%iNumFleetByRow
		
			pGroup = self.SourceFleets[iFleet]
			szShipPane = self.getNextWidgetName()
			screen.attachPanelAt("AddSourceFleetsPanel", szShipPane, "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY, self.X_FLEET_START*6/10 + (column)*(self.FLEET_BOX_SIZE+self.X_FLEET_OFFSET), self.Y_FLEET_START + (row)*(self.FLEET_BOX_SIZE+self.Y_FLEET_OFFSET), self.FLEET_BOX_SIZE, self.FLEET_BOX_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.displayTransportUnit(pGroup, szShipPane)

		iNumDestinationFleet = len(self.DestinationFleets)
		if iNumDestinationFleet == 0:
			idDestinationCity = pTraderoute.getDestinationCity().iID
			if idDestinationCity != self.EUROPE_ID:
				pDestinationCity = pPlayer.getCity(idDestinationCity)
				szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_NO_TRANSPORT_UNIT_AVAILABLE_IN_CITY", (pDestinationCity.getName(), ))
			else:
				szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_NO_TRANSPORT_UNIT_AVAILABLE_IN_EUROPE", ())
			screen.attachMultilineTextAt("AddDestinationFleetsPanel", self.getNextWidgetName(),  u"<font=4>" + localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_PLAYER_DARK_RED")) + u"</font>", self.W_ADD_FLEETS_PANEL/12, self.H_MIDDLE_AREA_FLEETS_PANEL/8, self.W_ADD_FLEETS_PANEL*8/10, self.H_MIDDLE_AREA_FLEETS_PANEL*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)	
			
		for iFleet in range(iNumDestinationFleet):
			row = iFleet/iNumFleetByRow
			column = iFleet%iNumFleetByRow
		
			pGroup = self.DestinationFleets[iFleet]
			szShipPane = self.getNextWidgetName()
			screen.attachPanelAt("AddDestinationFleetsPanel", szShipPane, "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY, self.X_FLEET_START*6/10 + (column)*(self.FLEET_BOX_SIZE+self.X_FLEET_OFFSET), self.Y_FLEET_START + (row)*(self.FLEET_BOX_SIZE+self.Y_FLEET_OFFSET), self.FLEET_BOX_SIZE, self.FLEET_BOX_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.displayTransportUnit(pGroup, szShipPane)

	def updateSourceOrDestinationFleet(self, pTraderoute):
		pPlayer = self.pPlayer
		self.SourceFleets = [] 
		self.DestinationFleets = [] 

		pSourceCity = None
		idSourceCity = pTraderoute.getSourceCity().iID
		if idSourceCity != self.EUROPE_ID:
			pSourceCity = pPlayer.getCity(idSourceCity)

		pDestinationCity = None
		idDestinationCity = pTraderoute.getDestinationCity().iID
		if idDestinationCity != self.EUROPE_ID:
			pDestinationCity = pPlayer.getCity(idDestinationCity)

		(unit, iter) = pPlayer.firstUnit()
		while (unit):
			if (not unit.isCargo() and not unit.isDelayedDeath() and (not gc.getUnitInfo(unit.getUnitType()).isMechUnit() or unit.hasCrew())):
				pSelectionGroup = unit.getGroup()
				isInGroup = pSelectionGroup.getMostPowerfulUnit().getID() == unit.getID()
				if (not unit.isAutomated() or not pSelectionGroup.isHurt()):
					if isInGroup and not pSelectionGroup.isAutomated() and pSelectionGroup.canAssignTradeRoute(self.SelectedRoute, false):
						if pSourceCity != None:
							pPlotCity = pSelectionGroup.plot().getPlotCity()
							if pPlotCity and pPlotCity.getID() == idSourceCity:
								self.SourceFleets.append(pSelectionGroup)	
						elif (unit.canTradeInEurope(False, True)):
								self.SourceFleets.append(pSelectionGroup)
						if pDestinationCity != None:
							pPlotCity = pSelectionGroup.plot().getPlotCity()
							if pPlotCity and pPlotCity.getID() == idDestinationCity:
								self.DestinationFleets.append(pSelectionGroup)	
						elif (unit.canTradeInEurope(False, True)):
								self.DestinationFleets.append(pSelectionGroup)
			
			(unit, iter) = pPlayer.nextUnit(iter)

	def handleInput( self, inputClass ):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):
				if (inputClass.getData1() == self.CHANGE_SOURCE_CITY) :
					self.changeSourceCity(inputClass.getData2())
				elif (inputClass.getData1() == self.CHANGE_DESTINATION_CITY) :
					self.changeDestinationCity(inputClass.getData2())
				elif (inputClass.getData1() == self.CHANGE_SELECTED_ROUTE) :
					self.changeSelectedRoute(inputClass.getData2())
				elif (inputClass.getData1() == self.CHANGE_SELECTED_ROUTE_PAGE) :
					self.changeSelectedRoute(inputClass.getData2())
				elif (inputClass.getData1() == self.CHANGE_VIEW) :
					self.changeView(inputClass.getData2())
				elif (inputClass.getData1() == self.CREATE_ROUTE) :
					self.createRoute()
				elif (inputClass.getData1() == self.REMOVE_ROUTE) :
					self.removeRoute(inputClass.getData2())
				elif (inputClass.getData1() == self.EDIT_ROUTE) :
					self.editRoute(inputClass.getData2())
				elif (inputClass.getData1() == self.REMOVE_YIELD_IMP_EXP) :
					self.removeYieldImpExpPopup(inputClass.getData2())
				elif (inputClass.getData1() == self.CHANGE_ACTIVE_RADIO) :
					self.changeActiveRadio(inputClass.getData2())
				elif (inputClass.getData1() == self.CHANGE_ACTIVE_EUROPEAN_RADIO) :
					self.changeActiveEuropeanRadio(inputClass.getData2())
				elif (inputClass.getData1() == self.INACTIVE_CHECK_BOX) :
					self.setCheckBoxStatus(inputClass.getData2(), False)
				elif (inputClass.getData1() == self.ACTIVE_CHECK_BOX) :
					self.setCheckBoxStatus(inputClass.getData2(), True)
				elif (inputClass.getData1() == self.SELECT_IMP_EXP_YIELD) :
					self.selectImpExpYield(inputClass.getData2())
				elif (inputClass.getData1() == self.EJECT_UNIT_TO_GROUP) :
					self.ejectUnitsToGroup(inputClass.getData2())
				elif (inputClass.getData1() == self.DISPLAY_SEAWAY_VIEW) :
					self.displaySeawayViewAction(inputClass.getData2())
				elif (inputClass.getData1() == self.EXIT_SEAWAY_VIEW) :
					self.DisplaySeawayView = False
				elif (inputClass.getData1() == self.CHANGE_SEAWAY_PAGE) :
					self.CurrentSeawayPage += inputClass.getData2()
				elif (inputClass.getData1() == self.REMOVE_SEAWAY) :
					self.removeSeaway(inputClass.getData2())
				elif (inputClass.getData1() == self.RENAME_SEAWAY) :
					self.renameSeaway(inputClass.getData2())
				elif (inputClass.getData1() == self.ACTIVE_SEAWAY_CHECK_BOX) :
					self.activeSewayCheckBox()
				elif (inputClass.getData1() == self.SELECT_SEAWAY) :
					self.selectSeaway(inputClass.getData2())
				elif (inputClass.getData1() == self.CHECK_BOX_GROUPS) :
					self.setCheckBoxGroups(inputClass.getData2())
				elif (inputClass.getData1() == self.CHANGE_KEPT_AUTO_IN_WARTIME) :
					self.inverseKeptAutoInWartimeOption()
				elif (inputClass.getData1() == self.CHANGE_MIN_GOLD_TO_CONSERVE) :
					self.launchChangeMinGoldToConservePopup()
				self.drawContents()

			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_TRADE_ROUTE_MOVE_TRANSPORT_TO_TRANSPORT):
				self.changeSelectedGroup(inputClass.getData1())
				self.drawContents()

		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON) :
			if (inputClass.getFunctionName() == "SelectSeaway") :
				 self.flashSeawayPosition(inputClass.getID())
					
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF) :
			if (inputClass.getFunctionName() == "SelectSeaway") :
				screen = self.getScreen()
				screen.minimapClearAllFlashingTiles()
				self.flashSourceCity()
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (inputClass.getFunctionName() == self.CIV_DROP_DOWN):				
				self.CivDropDown(inputClass)
		
		# elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_SLIDER_NEWSTOP):
		# 	if (inputClass.getFunctionName() + str(inputClass.getID()) == self.szSliderId):
		# 		if self.iSliderQuantity != inputClass.getData():			
		# 			self.iSliderQuantity = inputClass.getData()
		# 			self.redrawSlidersValue()
		return 0

	def launchChangeMinGoldToConservePopup(self):
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_CHANGE_MIN_GOLD_TO_CONSERVE_FOR_TRADE_ROUTE)
		popupInfo.setData1(self.RouteID)
		CyInterface().addPopup(popupInfo, self.pPlayer.getID(), True, True)

	def CivDropDown(self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			screen = self.getScreen()
			iIndex = screen.getSelectedPullDownID(self.CIV_DROP_DOWN)
			self.pPlayer = gc.getPlayer(screen.getPullDownData(self.CIV_DROP_DOWN, iIndex))
			self.initTradeRoutes(-1)
			self.drawContents()

	
	def inverseKeptAutoInWartimeOption(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer

		CyMessageControl().sendPlayerAction(pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_SEND_SECONDARYPLAYER_OPTION, SecondaryPlayerOptionTypes.SECONDARYPLAYEROPTION_KEPT_AUTO_IN_WARTIME, not pPlayer.isSecondaryOption(SecondaryPlayerOptionTypes.SECONDARYPLAYEROPTION_KEPT_AUTO_IN_WARTIME), -1)
		
	def setCheckBoxGroups(self, iOption):
		pPlayer = self.pPlayer
		pGroup = pPlayer.getSelectionGroup(self.SelectedGroupId)
		if(iOption == TradeRouteCheckBoxGroupsTypes.STOP_CONVOY):
			bValue = pGroup.shouldStopConvoy()
		elif (iOption == TradeRouteCheckBoxGroupsTypes.RESUPPLY_AUTO):
			bValue = pGroup.shouldResupplyAuto()
		elif (iOption == TradeRouteCheckBoxGroupsTypes.AUTO_HEAL):
			bValue = pGroup.shouldAutoHeal()
		CyMessageControl().sendPlayerAction(pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_SET_TRADE_ROUTE_CHECK_BOX_OPTION_GROUP, self.SelectedGroupId, iOption, not bValue)

	def displaySeawayViewAction(self, iGroupId):
		self.DisplaySeawayView = True
		self.SelectedGroupId = iGroupId

	def selectSeaway(self, iPosSeaway):
		lSeaways = self.getSeaways()
		if lSeaways == None:
			return
		pSeaway =  lSeaways[iPosSeaway][1]
		CyMessageControl().sendPlayerAction(self.pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_SELECT_SEAWAY_FOR_GROUP, self.SelectedGroupId, pSeaway.getID(), -1)

	def activeSewayCheckBox(self):
		CyMessageControl().sendPlayerAction(self.pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_SELECT_SEAWAY_FOR_GROUP, self.SelectedGroupId, -1, -1)

	def renameSeaway(self, iPosSeaway):
		lSeaways = self.getSeaways()
		if lSeaways == None:
			return
		pSeaway =  lSeaways[iPosSeaway][1]
		CyMessageControl().sendModNetMessage(self.EDIT_SEAWAY_NAME, self.pPlayer.getID(), -1, pSeaway.getID(), -1)

	def removeSeaway(self, iPosSeaway):
		lSeaways = self.getSeaways()
		if lSeaways == None:
			return
		pSeaway =  lSeaways[iPosSeaway][1]
		CyMessageControl().sendPlayerAction(self.pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_REMOVE_SEAWAY, -1, pSeaway.getID(), -1)

	def flashSeawayPosition(self, iPosSeaway):
		screen = self.getScreen()
		lSeaways = self.getSeaways()
		if lSeaways == None:
			return
		pSeaway =  lSeaways[iPosSeaway][1]
		pPlot = pSeaway.plot()
		if pPlot:
			szColor = gc.getInfoTypeForString("COLOR_WHITE")
			screen.minimapFlashPlot(pPlot.getX(), pPlot.getY(), szColor, -1)

	def flashSourceCity(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer
		
		pCity = self.getCityOfTradeRoute()

		if pCity:
			pPlot = pCity.plot()
		
		if pPlot != None:
			screen.minimapFlashPlot(pPlot.getX(), pPlot.getY(), gc.getInfoTypeForString("COLOR_PLAYER_DARK_RED"), -1)

	def ejectUnitsToGroup(self, idUnit):
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_EJECT_UNIT_TO_GROUP)
		popupInfo.setData1(idUnit)
		CyInterface().addPopup(popupInfo, self.pPlayer.getID(), true, true)

	def changeSelectedGroup(self, idUnit):
		pPlayer = self.pPlayer
		pUnit = pPlayer.getUnit(idUnit)
		self.SelectedGroupId = pUnit.getGroup().getID()
		
	def setCheckBoxStatus(self, idCheckBox, bState):
		pPlayer = self.pPlayer	
		routeID = self.RouteID
		if routeID == self.UNSELECT_ID:
			return
		if bState:
			CyMessageControl().sendPlayerAction(pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_SET_TRADE_ROUTE_CHECK_BOX_OPTION_ACTIVATE, routeID, idCheckBox, self.ImpExpYield)		
		else: 
			CyMessageControl().sendPlayerAction(pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_SET_TRADE_ROUTE_CHECK_BOX_OPTION_DESACTIVATE, routeID, idCheckBox, self.ImpExpYield)		
		
	def changeActiveRadio(self, iState):
		pPlayer = self.pPlayer	
		routeID = self.RouteID
		if routeID == self.UNSELECT_ID:
			return
		CyMessageControl().sendPlayerAction(pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_SET_TRADE_ROUTE_RADIO_OPTION, routeID, iState, self.ImpExpYield)		
	
	def changeActiveEuropeanRadio(self, iState):
		pPlayer = self.pPlayer	
		routeID = self.RouteID
		if routeID == self.UNSELECT_ID:
			return
		CyMessageControl().sendPlayerAction(pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_SET_TRADE_ROUTE_EUROPEAN_RADIO_OPTION, routeID, iState, self.ImpExpYield)		
	
	def removeYieldImpExpPopup(self, iYield):		
		pPlayer = self.pPlayer	
		routeID = self.RouteID
		if routeID == self.UNSELECT_ID:
			return
		eTrade = TradeTypes.NO_TRADE

		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setData1(routeID)
		popupInfo.setData2(eTrade)
		popupInfo.setData3(iYield)
		popupInfo.setText(localText.getText("TXT_KEY_TRADE_ROUTE_POPUP_REMOVE_BODY", (gc.getYieldInfo(iYield).getDescription(), )))
		popupInfo.setOnClickedPythonCallback("tradeRoutesOnClickedCallback")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
		CyInterface().addPopup(popupInfo, pPlayer.getID(), true, false)

	def selectImpExpYield(self, iYield):
		self.ImpExpYield = iYield

	def editRoute(self, routeID):
		pPlayer = self.pPlayer
		self.View = self.EDIT_ROUTE_VIEW
		self.RouteID = routeID
		self.SelectedRoute = routeID

		pTraderoute = pPlayer.getTradeRoute(routeID)
		self.SourceCity = pTraderoute.getSourceCity().iID
		self.DestinationCity = pTraderoute.getDestinationCity().iID
		self.ImpExpYield = YieldTypes.NO_YIELD
		CyMessageControl().sendPlayerAction(pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_SET_CURRENT_TRADE_ROUTE, routeID, -1, -1)
		
	def removeRoute(self, routeID):
		CyMessageControl().sendPlayerAction(self.pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_REMOVE_TRADE_ROUTE, routeID, -1, -1)

	def createRoute(self):
		if self.SourceCity != self.UNSELECT_ID and self.DestinationCity != self.UNSELECT_ID:
			CyMessageControl().sendPlayerAction(self.pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_CREATE_TRADE_ROUTE, self.SourceCity, self.DestinationCity, -1)
	

	def changeView(self, iView):
		# We save the previous view if we want to come back
		if iView == self.PreviousView:
			self.PreviousView = self.TRADE_ROUTES_VIEW
		else:
			self.PreviousView = self.View

		if iView == self.TRADE_ROUTES_VIEW:
			pPlayer = self.pPlayer
			if pPlayer.getNumTradeRoutes() > 0 or CyGame().isDebugMode():
				self.View = iView
				self.RouteID = self.UNSELECT_ID
				self.SourceCity = self.UNSELECT_ID
				self.DestinationCity = self.UNSELECT_ID
				self.initSelectedRoute(True)
		else:
			self.View = iView
		self.ImpExpYield = YieldTypes.NO_YIELD
		self.LastAreaUnitsText = ""

	def changeSelectedRoute(self, iRouteID):
		self.SelectedRoute = iRouteID

	def changeSourceCity(self, cityId):
		if(cityId == self.SourceCity) :
			self.SourceCity = self.UNSELECT_ID
		elif cityId != self.DestinationCity :
			self.SourceCity = cityId
		self.initSelectedRoute(False)

	def changeDestinationCity(self, cityId):
		if(cityId == self.DestinationCity) :
			self.DestinationCity = self.UNSELECT_ID
		elif cityId != self.SourceCity :
			self.DestinationCity = cityId
		self.initSelectedRoute(False)

	def update(self, fDelta):
		screen = self.getScreen()
		if (CyInterface().isDirty(InterfaceDirtyBits.TradeRoutes_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.TradeRoutes_DIRTY_BIT, False)
			pPlayer = self.pPlayer
			self.lOrderedSeaways = None
			self.drawContents()
		if (CyInterface().isDirty(InterfaceDirtyBits.TradeRoutesResetSelection_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.TradeRoutesResetSelection_DIRTY_BIT, False)
			pPlayer = self.pPlayer

			self.View = self.TRADE_ROUTES_VIEW
			self.initSelectedRoute(True)
			self.drawContents()

	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList
		if eWidgetType == WidgetTypes.WIDGET_GENERAL:
			if  iData1 == self.CHANGE_SELECTED_ROUTE:
				return localText.getText("TXT_KEY_TRADE_ROUTES_SELECT", ())
			elif iData1 == self.CHANGE_SOURCE_CITY :
				return self.getChangeSourceCityHelp(iData2)
			elif iData1 == self.CHANGE_DESTINATION_CITY:
				return self.getChangeDestinationCityHelp(iData2)
			elif iData1 == self.SELECT_IMP_EXP_YIELD:
				return self.getImpExpYieldHelp(iData2)
			elif iData1 == self.REMOVE_YIELD_IMP_EXP:
				return localText.getText("TXT_KEY_TRADE_ROUTES_REMOVE_YIELD", ())
			elif iData1 == self.CHANGE_VIEW:
				return self.changeViewhelp(iData2)
			elif iData1 == self.EDIT_ROUTE:
				return localText.getText("TXT_KEY_TRADE_ROUTES_EDIT_ROUTE_HELP", ())
			elif iData1 == self.REMOVE_ROUTE:
				return localText.getText("TXT_KEY_TRADE_ROUTES_REMOVE_ROUTE_HELP", ())
			elif iData1 == self.ONLY_SHIP_HELP:
				return localText.getText("TXT_KEY_ONLY_SHIP_HELP", ())
			elif iData1 == self.ONLY_WAGON_HELP:
				return localText.getText("TXT_KEY_ONLY_WAGON_HELP", ())
			elif iData1 == self.SHIP_AND_WAGON_HELP:
				return localText.getText("TXT_KEY_SHIP_AND_WAGON_HELP", ())
			elif iData1 == self.CHANGE_MIN_GOLD_TO_CONSERVE:
				return localText.getText("TXT_KEY_CHANGE_MIN_GOLD_TO_CONSERVE_HELP", ())
			elif iData1 == self.EXIT_SEAWAY_VIEW:
				return localText.getText("TXT_KEY_CLOSE_WINDOW_POPUP", ())
			elif iData1 == self.REMOVE_SEAWAY:
				return localText.getText("TXT_KEY_REMOVE_SEAWAY_HELP", ())
			elif iData1 == self.RENAME_SEAWAY:
				return localText.getText("TXT_KEY_RENAME_SEAWAY_HELP", ())
			elif iData1 == self.SELECT_SEAWAY_HELP:
				return self.selectSeawayHelp(iData2)
			
		return u""

	def getCityOfTradeRoute(self):
		pPlayer = self.pPlayer
		pTraderoute = pPlayer.getTradeRoute(self.RouteID)
		idCity = pTraderoute.getSourceCity().iID
		if idCity != self.EUROPE_ID:
			return pPlayer.getCity(idCity)
		
		idCity = pTraderoute.getDestinationCity().iID
		if idCity != self.EUROPE_ID:
			return pPlayer.getCity(idCity)
		return None

	def selectSeawayHelp(self, iSeawayPos):
		pPlayer = self.pPlayer
		pSourceCity = self.getCityOfTradeRoute()
		lSeaways = self.getSeaways()
		if pSourceCity == None or lSeaways == None:
			return
		iDistance = lSeaways[iSeawayPos][0]

		return  localText.getText("TXT_KEY_SELECT_SEAWAY_HELP", (iDistance, pSourceCity.getName(), ))

	def changeViewhelp(self, iView):
		if(iView == self.EDIT_ROUTE_TRANSPORTS_VIEW):
			return localText.getText("TXT_KEY_TRADE_ROUTE_ADD_TRANSPORT_BUTTON", ())
		elif(iView == self.EDIT_ROUTE_VIEW and (self.View == self.EDIT_ROUTE_TRANSPORTS_VIEW or self.View == self.EDIT_ROUTE_ADD_TRANSPORTS_VIEW)):
			return localText.getText("TXT_KEY_TRADE_ROUTE_ADD_RESOURCES_BUTTON", ())
		elif (self.View == self.EDIT_ROUTE_TRANSPORTS_VIEW and iView == self.EDIT_ROUTE_ADD_TRANSPORTS_VIEW):
			return localText.getText("TXT_KEY_TRADE_ROUTE_EDIT_ROUTE_ADD_TRANSPORTS_VIEW", ())
		return u""
 
	def getImpExpYieldHelp(self, iYield):
		pPlayer = self.pPlayer
			
		szText =  "<font=3b>" + gc.getYieldInfo(iYield).getDescription() + "</font>\n"
		if self.RouteID != self.UNSELECT_ID:
			pTraderoute = pPlayer.getTradeRoute(self.RouteID)
			eTrade = pTraderoute.getTradeType(iYield)
			bBuyPrice = True
			if eTrade == TradeTypes.TRADE_EXPORT:
				idCity = pTraderoute.getSourceCity().iID
				if idCity != self.EUROPE_ID:
					pCity = pPlayer.getCity(idCity)
					szText += localText.getText("TXT_KEY_TRADE_ROUTES_QUANTITY_HELP", (pCity.getYieldStored(iYield), pCity.calculateNetYield(iYield), ))
					szText += "\n"
					bBuyPrice = False
			elif eTrade == TradeTypes.TRADE_IMPORT:
				idCity = pTraderoute.getDestinationCity().iID
				if idCity != self.EUROPE_ID:
					pCity = pPlayer.getCity(idCity)
					szText += localText.getText("TXT_KEY_TRADE_ROUTES_QUANTITY_HELP", (pCity.getYieldStored(iYield), pCity.calculateNetYield(iYield), ))
					szText += "\n"
					bBuyPrice = False

			if bBuyPrice:
				szTextKey = "TXT_KEY_TRADE_ROUTES_YIELD_BUY_PRICE_HELP"
				szText += localText.getText(szTextKey, (pPlayer.getBuyPriceForYield(iYield, 1), ))
			else:
				szTextKey = "TXT_KEY_TRADE_ROUTES_YIELD_PRICE_HELP"
				szText += localText.getText(szTextKey, (pPlayer.getSellPriceForYield(iYield, 1), ))
		return szText

	def getChangeSourceCityHelp(self, iCityId):
		if self.View == self.TRADE_ROUTES_VIEW:
			if(self.SourceCity == iCityId):
				return localText.getText("TXT_KEY_TRADE_ROUTES_FILTER_SOURCE_HELP_ALREADY_SELECTED", ())
			elif(self.DestinationCity == iCityId):
				return localText.getText("TXT_KEY_TRADE_ROUTES_FILTER_SOURCE_HELP_ALREADY_SELECTED_ON_DESTINATION", ())
			elif(not self.isExistingSource(iCityId)):
				return localText.getText("TXT_KEY_TRADE_ROUTES_FILTER_SOURCE_HELP_NO_TRADE_ROUTE", ())
			else:
				return localText.getText("TXT_KEY_TRADE_ROUTES_FILTER_SOURCE_HELP", ())
		else :
			return localText.getText("TXT_KEY_TRADE_ROUTES_SELECT_SOURCE_HELP", ())
	
	def getChangeDestinationCityHelp(self, iCityId):
		if self.View == self.TRADE_ROUTES_VIEW:
			if(self.DestinationCity == iCityId):
				return localText.getText("TXT_KEY_TRADE_ROUTES_FILTER_SOURCE_HELP_ALREADY_SELECTED", ())
			elif(self.SourceCity == iCityId):
				return localText.getText("TXT_KEY_TRADE_ROUTES_FILTER_DESTINATION_HELP_ALREADY_SELECTED_ON_DESTINATION", ())
			elif(not self.isExistingDestination(iCityId)):
				return localText.getText("TXT_KEY_TRADE_ROUTES_FILTER_DESTINATION_HELP_NO_TRADE_ROUTE", ())
			else:
				return localText.getText("TXT_KEY_TRADE_ROUTES_FILTER_DESTINATION_HELP", ())
		else :
			return localText.getText("TXT_KEY_TRADE_ROUTES_SELECT_DESTINATION_HELP", ())
	
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def deleteAllWidgets(self):
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while (i >= 0):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = 0

	def calculateSizesAndPositions(self):
		self.X_SCREEN = 0
		self.Y_SCREEN = 0

		screen = self.getScreen()

		self.XResolution = screen.getXResolution()
		self.YResolution = screen.getYResolution()

		self.W_SCREEN = screen.getXResolution()
		self.H_SCREEN = screen.getYResolution()

		self.W_EXIT = self.xSize(120)
		self.H_EXIT = self.ySize(30)

		self.Y_BOTTOM_LINKS_MARGIN = self.ySize(37)
		self.X_BOTTOM_LINKS_MARGIN = self.xSize(30)

		self.Y_MIDDLE_OFFSET = 12

		self.TOP_PANEL_SIZE = self.ySize(55)

		self.X_EXIT = self.XResolution - self.W_EXIT 
		self.Y_EXIT = self.YResolution - self.H_EXIT

		## COLONY PANEL START
		self.X_MARGIN_COLONY_PANEL = self.xSize(57)
		self.Y_MARGIN_COLONY_PANEL = self.ySize(35)

		self.Y_COLONY_PANEL_START = self.TOP_PANEL_SIZE + self.Y_MARGIN_COLONY_PANEL
		self.W_COLONY_PANEL = self.xSize(180)
		self.H_COLONY_PANEL = self.YResolution - 2 * (self.TOP_PANEL_SIZE + self.Y_MARGIN_COLONY_PANEL)
		self.X_LEFT_COLONY_PANEL_START = self.X_MARGIN_COLONY_PANEL
		self.X_RIGHT_COLONY_PANEL_START = self.XResolution - self.W_COLONY_PANEL - self.X_MARGIN_COLONY_PANEL

		self.H_CITY_ANIMATION = self.ySize(102)
		self.W_CITY_ANIMATION = self.xSize(164)
		self.X_CITY_ANIMATION = (self.W_COLONY_PANEL - self.W_CITY_ANIMATION) / 2
		self.Y_CITY_ANIMATION = self.ySize(36)

		self.H_SEPARATION = self.ySize(55)

		self.H_COLONY_ROW = self.ySize(20)
		self.H_COLONY_ROW_OFFSET = 0

		self.Z_CITY_DISTANCE = 450
		## COLONY PANEL END

		self.X_MID_VIEW = self.X_LEFT_COLONY_PANEL_START + self.W_COLONY_PANEL + self.X_MARGIN_COLONY_PANEL
		self.H_TRADE_ROUTES = self.H_SCREEN /2 - self.ySize(20)
		self.Y_TRADE_ROUTES = self.Y_COLONY_PANEL_START - self.Y_MIDDLE_OFFSET + self.ySize(30)
		self.W_TRADE_ROUTES = self.XResolution - 2*self.X_MID_VIEW + 20
		
		self.X_TRADE_ROUTES_OFFSET = self.xSize(10)
		self.Y_TRADE_ROUTES_OFFSET = self.ySize(20)
		self.H_TRADE_ROUTES_OFFSET = self.ySize(30)

		self.W_TRADE_ROUTES_ICON = self.minSize(25)
		
		self.Y_DESCRIPTION_PANEL_SIZE = self.Y_TRADE_ROUTES + self.Y_MIDDLE_OFFSET + self.H_TRADE_ROUTES + self.ySize(10) - self.H_EXIT
		self.H_DESCRIPTION_PANEL_SIZE = self.YResolution - self.Y_DESCRIPTION_PANEL_SIZE - self.TOP_PANEL_SIZE - self.H_EXIT * 3 /2
		self.W_ROW_DESC_OFFSET = self.xSize(20)
		self.X_ROW_DESC_OFFSET = self.xSize(10)

		self.H_DESC_CREATE_ROUTE = self.ySize(100)

		self.W_CREATE_ROUTE_BTN = self.xSize(130)
		self.H_CREATE_ROUTE_BTN = self.ySize(30)

		self.X_BEST_YIELDS_BOX = self.X_MID_VIEW - self.X_MARGIN_COLONY_PANEL
		self.Y_BEST_YIELDS_BOX = self.Y_TRADE_ROUTES + self.Y_MIDDLE_OFFSET + self.H_TRADE_ROUTES + self.ySize(85)

		self.H_BEST_YIELDS_BOX = self.H_DESCRIPTION_PANEL_SIZE * 3 /4
		self.W_BEST_YIELDS_BOX = self.XResolution - 2*self.X_MID_VIEW + self.X_MARGIN_COLONY_PANEL * 2

		self.H_IMP_EXP_YIELDS_BOX = self.H_BEST_YIELDS_BOX * 4 / 5
		self.H_IMP_EXP_LIST = self.H_COLONY_PANEL - self.H_CITY_ANIMATION - 2 * self.Y_MARGIN_COLONY_PANEL - self.Y_MARGIN_COLONY_PANEL - self.H_CITY_ANIMATION
		
		self.W_TRANSPORTS_VIEW_BUTTON = self.xSize(100)
		self.H_TRANSPORTS_VIEW_BUTTON = self.ySize(50)

		self.H_OFFSET_ROWS = self.ySize(25)
		self.REMOVE_ICON_SIZE = self.minSize(23)

		self.Y_MID_VIEW = self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION + self.H_SEPARATION - self.Y_MIDDLE_OFFSET*2 - 3
		
		self.W_ARROW_MIDDLE = self.xSize(100)
		self.H_ARROW_MIDDLE = self.ySize(50)

		self.ARROW_MIDDLE_SIZE = self.xSize(100)

		self.RADIO_SIZE = self.minSize(30)
		self.ACTIVATE_RADIO = ArtFileMgr.getInterfaceArtInfo("INTERFACE_UNIT_RADIO_ACTIVATE").getPath()
		self.DESACTIVATE_RADIO = ArtFileMgr.getInterfaceArtInfo("INTERFACE_UNIT_RADIO_NO_ACTIVATE").getPath()
		self.ACTIVATE_CHECK_BOX = ArtFileMgr.getInterfaceArtInfo("INTERFACE_UNIT_COCHE_ACTIVATE").getPath()
		self.DESACTIVATE_CHECK_BOX = ArtFileMgr.getInterfaceArtInfo("INTERFACE_UNIT_COCHE_NO_ACTIVATE").getPath()

		self.FLEET_BOX_SIZE = self.minSize(150)
		self.FLEET_BOX_SIZE_SMALL = self.FLEET_BOX_SIZE / 3
		self.X_FLEET_START = self.xSize(20)
		self.Y_FLEET_START = self.ySize(20)
		self.Y_FLEET_OFFSET = self.Y_FLEET_START
		self.NUM_FLEET_BY_ROW = 5

		self.W_ARROW_RIGHT_BOTTOM_SIZE = self.xSize(45) 
		self.H_ARROW_RIGHT_BOTTOM_SIZE = self.ySize(55)
		
		self.X_FLEETS_PANEL = self.X_LEFT_COLONY_PANEL_START
		self.Y_FLEETS_PANEL = self.Y_COLONY_PANEL_START + self.Y_CITY_ANIMATION + self.H_CITY_ANIMATION + self.H_SEPARATION / 2
		self.W_FLEETS_PANEL = self.XResolution - 2*self.X_FLEETS_PANEL - 20	
		self.H_FLEETS_PANEL = self.FLEET_BOX_SIZE + self.Y_FLEET_START * 2

		self.Y_FLEET_ACTION_PANEL = self.Y_FLEETS_PANEL + self.H_FLEETS_PANEL + self.Y_FLEET_OFFSET + self.ySize(20)
		self.H_FLEET_ACTION_PANEL = self.H_FLEETS_PANEL

		self.X_FLEET_OFFSET = (self.W_FLEETS_PANEL - self.NUM_FLEET_BY_ROW * self.FLEET_BOX_SIZE - self.X_FLEET_START * 2 - self.FLEET_BOX_SIZE_SMALL) / (self.NUM_FLEET_BY_ROW)

		self.X_ADD_FLEETS_PANEL = self.X_FLEETS_PANEL
		self.Y_ADD_FLEETS_PANEL = self.Y_FLEETS_PANEL
		self.W_ADD_FLEETS_PANEL = self.FLEET_BOX_SIZE * 2 + self.X_FLEET_OFFSET * 3 + self.X_FLEET_START * 2
		self.H_ADD_FLEETS_PANEL = self.FLEET_BOX_SIZE * 2 + self.Y_FLEET_OFFSET * 3 + self.Y_FLEET_START * 3 / 2
		self.X_ADD_FLEETS_PANEL_RIGHT = self.XResolution - self.X_ADD_FLEETS_PANEL - self.W_ADD_FLEETS_PANEL

		self.X_MIDDLE_AREA_FLEETS_PANEL = self.X_ADD_FLEETS_PANEL + self.W_ADD_FLEETS_PANEL
		self.Y_MIDDLE_AREA_FLEETS_PANEL = self.Y_FLEETS_PANEL
		self.W_MIDDLE_AREA_FLEETS_PANEL = self.XResolution - 2*(self.X_ADD_FLEETS_PANEL + self.W_ADD_FLEETS_PANEL) - self.xSize(5)
		self.H_MIDDLE_AREA_FLEETS_PANEL = self.H_ADD_FLEETS_PANEL

		self.W_SEAWAY_PANEL = self.xSize(720)
		self.H_SEAWAY_PANEL = self.ySize(480)
		self.X_SEAWAY_PANEL = self.XResolution/2 - self.W_SEAWAY_PANEL / 2 # CENTERED PICTURE
		self.Y_SEAWAY_PANEL = self.YResolution/2 - self.H_SEAWAY_PANEL / 2 # CENTERED PICTURE

		self.H_SEAWAY_ROW = self.ySize(24)
		self.NUM_SEAWAYS_BY_PAGE = 7 # Number of seaways by page
		self.X_SEAWAY_ROW = self.xSize(345)
		self.Y_SEAWAY_ROW = self.ySize(140) + (10 - self.NUM_SEAWAYS_BY_PAGE) * self.H_SEAWAY_ROW

		self.W_SEAWAY_ROW_SEPARATION = self.xSize(220)
		self.H_SEAWAY_ROW_SEPARATION = self.ySize(4)
		self.W_SEAWAY_ARROW = self.xSize(25)
		self.H_SEAWAY_ARROW = self.ySize(20)
		self.SEAWAY_ICON_SIZE = self.minSize(20)


		self.CLOSE_BUTTON_SIZE = self.minSize(50)
		self.ICON_ON_SHIP = self.ySize(38)

		self.W_MINIMAP = self.xSize(210)
		self.H_MINIMAP = self.ySize(280)
		self.X_MINIMAP_START = self.X_SEAWAY_PANEL + self.xSize(80)
		self.X_MINIMAP_END = self.X_MINIMAP_START + self.W_MINIMAP
		self.Y_MINIMAP_START = self.Y_SEAWAY_PANEL + self.ySize(115)
		self.Y_MINIMAP_END = self.Y_MINIMAP_START + self.H_MINIMAP
		self.Z_CONTROLS = -2.3 # Need to spend more time on this variable

		#Navigation page of seaway
		self.X_SEAWAY_PAGINATION = self.X_SEAWAY_ROW + self.W_SEAWAY_ROW_SEPARATION / 2
		self.W_SEAWAY_ARROW = self.xSize(31)
		self.H_SEAWAY_ARROW = self.ySize(20)
		self.Y_SEAWAY_ARROW = self.ySize(380)
		self.X_SEAWAY_ARROW_LEFT = self.X_SEAWAY_PAGINATION - self.W_SEAWAY_ARROW * 5 /4
		self.X_SEAWAY_ARROW_RIGHT = self.X_SEAWAY_PAGINATION + self.W_SEAWAY_ARROW / 4

		self.Y_SEAWAY_TITLE = self.ySize(70)
		self.Y_MULTILINE_SEAWAY_DESCRIPTION = self.Y_SEAWAY_TITLE + self.ySize(13)
		self.H_MULTILINE_SEAWAY_DESCRIPTION = self.Y_SEAWAY_ROW - self.Y_MULTILINE_SEAWAY_DESCRIPTION - self.ySize(5)
		self.H_MULTILINE_SEAWAY_SELECTED_DESCRIPTION = self.ySize(40)
		self.Y_MULTILINE_SEAWAY_DESCRIPTION_OTHER = self.Y_MULTILINE_SEAWAY_DESCRIPTION + self.H_MULTILINE_SEAWAY_SELECTED_DESCRIPTION + self.H_SEAWAY_ROW_SEPARATION + self.RADIO_SIZE
		self.H_MULTILINE_SEAWAY_SELECTED_DESCRIPTION_OTHER = self.ySize(40)

		self.X_ICON_TRANSPORT_TYPE = self.W_TRADE_ROUTES - self.xSize(20)
		self.Y_ICON_TRANSPORT_TYPE = self.ySize(5)
		self.SMALL_ICON_TRANSPORT_TYPE_SIZE = self.minSize(25)

		self.NUM_TRADE_ROUTES_BY_PAGE = 10
		self.X_TRADE_ROUTE_PAGINATION = self.W_TRADE_ROUTES / 2
		self.W_TRADE_ROUTE_ARROW = self.W_SEAWAY_ARROW
		self.H_TRADE_ROUTE_ARROW = self.H_SEAWAY_ARROW
		self.Y_TRADE_ROUTE_ARROW = self.H_TRADE_ROUTES - 2 * self.H_TRADE_ROUTE_ARROW
		self.X_TRADE_ROUTE_ARROW_LEFT = self.X_TRADE_ROUTE_PAGINATION - self.W_TRADE_ROUTE_ARROW * 5 /4
		self.X_TRADE_ROUTE_ARROW_RIGHT = self.X_TRADE_ROUTE_PAGINATION + self.W_TRADE_ROUTE_ARROW / 4

		self.CHECKBOX_SIZE = self.minSize(35)
		self.X_KEPT_AUTO_IN_WARTIME = self.X_MID_VIEW + self.xSize(10)
		self.Y_KEPT_AUTO_IN_WARTIME = self.Y_DESCRIPTION_PANEL_SIZE + self.H_DESCRIPTION_PANEL_SIZE - self.ySize(5)

		self.W_IMP_EXP_YIELD = self.minSize(32)
		self.X_IMP_EXP_PANEL = self.xSize(65)
		self.Y_IMP_EXP_PANEL = self.ySize(35)

		self.CHANGE_MIN_GOLD_TO_CONSERVE_ICON_SIZE = self.minSize(25)
		self.X_OUTSIDE_CHANGE_MIN_GOLD_TO_CONSERVE_MARGIN = self.xSize(42)
		self.Y_OUTSIDE_CHANGE_MIN_GOLD_TO_CONSERVE_MARGIN = self.ySize(12)


		# self.X_SLIDER = self.X_MID_VIEW
		# self.Y_SLIDER = self.Y_TRADE_ROUTES + self.H_DESC_CREATE_ROUTE + 10
		# self.W_SLIDER = self.xSize(100)
		# self.H_SLIDER = self.ySize(15)

		self.UKNOWN_VALUE = "--"

	def minSize(self, val):
		return min(self.xSize(val), self.ySize(val))

	def xSize(self, val):
		return val*self.XResolution/1024

	def ySize(self, val):
		return val*self.YResolution/768

	def orderCitiesByTradeRoutes(self):
		pPlayer = self.pPlayer

		self.ColonyList = []
		(pCity, iter) = pPlayer.firstCity(false)
		while (pCity):
			numTradeRoutes = iter
			self.ColonyList.append((numTradeRoutes, pCity))
			(pCity, iter) = pPlayer.nextCity(iter, false)
			
		if len(self.ColonyList) > 0:
			self.ColonyList.sort()
			#self.ColonyList.reverse()

	def getSeaways(self):
		if self.lOrderedSeaways != None:
			return self.lOrderedSeaways
		self.orderSeawaysByStepDistance()
		return self.lOrderedSeaways

	def orderSeawaysByStepDistance(self):
		pPlayer = self.pPlayer

		self.lOrderedSeaways = []
		iNumSeaways = pPlayer.getNumSeaways()
		pCity = self.getCityOfTradeRoute()

		if not pCity:
			return

		pPlotCity = pCity.plot()

		for index in range(iNumSeaways):
			loopSeaway = pPlayer.getSeaway(index)
			iStepDistance = loopSeaway.stepDistanceToPlot(pPlotCity)
			if iStepDistance > 0:
				self.lOrderedSeaways.append((iStepDistance - 1, loopSeaway))
		if len(self.lOrderedSeaways) > 0:
			self.lOrderedSeaways.sort()

	def mainColor(self, szText):
		return localText.changeTextColor(szText, self.MainColor)

	def activeColor(self, szText):
		return u"<color=85,108,19>" + szText + u"</color>"
	
	def blackColor(self, szText):
		return u"<color=0,0,0>" + szText + u"</color>"
	
	def unactiveColor(self, szText):
		return u"<color=168,138,90>" + szText + u"</color>"

	def descColor(self, szText):
		return u"<color=85,108,19>" + szText + u"</color>"

	def warningColor(self, szText):
		return u"<color=255,230,0>" + szText + u"</color>"
		
	def setCurrentTradeRouteId(self, currentId):
		self.RouteID = currentId
		self.SelectedRoute = currentId
		self.View = self.EDIT_ROUTE_VIEW
		self.drawContents()

	def setSelectedYield(self, iYield, eTrade):
		if eTrade != TradeTypes.NO_TRADE:
			self.ImpExpYield = iYield
		else:
			self.ImpExpYield = YieldTypes.NO_YIELD
		self.drawContents()

	def setLastGroupAssigned(self, idGroup):
		if not self.getScreen().isActive():
			return

		pPlayer = self.pPlayer
		pGroup = pPlayer.getSelectionGroup(idGroup)
		if pGroup:
			szText = ""
			if pGroup.getNumUnits() > 1:
				if(pGroup.getDomainType() == DomainTypes.DOMAIN_SEA):
					szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_LAST_GROUP_ASSIGNED_MANY_SHIPS", (pGroup.getNumUnits(), ))
				else :
					szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_LAST_GROUP_ASSIGNED_MANY_WAGONS", (pGroup.getNumUnits(), ))
			else :
				pUnit = pGroup.getMostPowerfulUnit()
				if pUnit:
					szText = localText.getText("TXT_KEY_TRADE_ROUTES_SCREEN_LAST_GROUP_ASSIGNED_ONE", (pUnit.getName().lower(), ))
			self.LastAreaUnitsText = self.descColor(szText)
			self.drawContents()
