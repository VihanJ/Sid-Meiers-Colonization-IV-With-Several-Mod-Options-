## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Europe Screen 5 beta3 - AOD2
## by koma13


from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import sdToolKit

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvEuropeScreen:

	def __init__(self):
		self.WIDGET_ID = "EuropeScreenWidget"
		self.nWidgetCount = 0

		self.UNIT_BUTTON_ID = 1
		self.UNIT_CARGO_BUTTON_ID = 2
		self.BUY_YIELD_BUTTON_ID = 3
		self.YIELD_CARGO_BUTTON_ID = 4
		self.BUY_UNIT_BUTTON_ID = 5
		self.DOCK_BUTTON_ID = 6
		self.SAIL_TO_NEW_WORLD = 7
		self.SELL_ALL = 8
		self.LOAD_ALL = 9
		self.HELP_CROSS_RATE = 10
		self.TREASURY_ID = 11
		self.TRAVEL_INFO = 12
		self.TRADE_LOG = 13
		self.SAIL_EXEC = 14
		self.SELL_SHIP = 15
		self.SELL_SHIP_EXEC = 16
		self.PREVIEW_MODE = 17
		self.RECALL = 18
		
	def getScreen(self):
		return CyGInterfaceScreen("EuropeScreen", CvScreenEnums.EUROPE_SCREEN)

	def interfaceScreen(self):

		if ( CyGame().isPitbossHost() ):
			return

		if gc.getPlayer(gc.getGame().getActivePlayer()).getParent() == PlayerTypes.NO_PLAYER:
			return

		screen = self.getScreen()
		if screen.isActive():
			return

		## Europe Screen Configuration START
		# To disable a feature set value to 0

		self.iWinterScreen = 9			# min turns between 2 winter screens
		self.iSellShip = 0#8				# base factor for ship selling price (0 to 12)
		self.iVideo = 6					# show sea gulls every x turns
		self.iPlotDebug = 0     	    # show plot coordinates in transport tool tips
	
		## Europe Screen Configuration END
	
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		self.Pirates = player.isPirates()
		self.iThisWinter = 0
		self.iSoundID = 0
		self.szVersion = "5b3-AOD2"
	
		if (not sdToolKit.sdEntityExists( 'komaScreens', player.getName())): 
			sdToolKit.sdEntityInit('komaScreens', player.getName(), { 'TradeBox': 0, 'LastWinter': 0, 'PreviewMode': 1 })

		if self.Pirates:
			self.iWinterScreen = 0
	
		self.EuropeUnitsList = []
		self.OutboundUnitsList = []
		self.EuropePlotList = []
		self.PreviewPlotList = []
	
		# Winter
		if self.iWinterScreen > 0:
			iCurrentTurn = CyGame().getGameTurn()
			szDate = CyGameTextMgr().getTimeStr(iCurrentTurn, true)

			January = localText.getText("TXT_KEY_MONTH_JANUARY", ())
			February = localText.getText("TXT_KEY_MONTH_FEBRUARY", ())
			December = localText.getText("TXT_KEY_MONTH_DECEMBER", ())

			if (gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGameTurnInfo(0).iMonthIncrement != 12):
				if (January in szDate or February in szDate or December in szDate):
					iLastWinterDiff = iCurrentTurn - sdToolKit.sdGetVal('komaScreens', player.getName(), 'LastWinter')
					if (iLastWinterDiff >= self.iWinterScreen or iLastWinterDiff == 0) and (iCurrentTurn != 0):
						self.iThisWinter = 1
						sdToolKit.sdSetVal('komaScreens', player.getName(), 'LastWinter', iCurrentTurn)

			elif (iCurrentTurn % self.iWinterScreen == 0) and (iCurrentTurn != 0):
				self.iThisWinter = 1

		#

		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.XResolution = screen.getXResolution()
		self.YResolution = screen.getYResolution()

		self.Y_EXIT = self.YResolution - 36
		self.X_EXIT = self.XResolution - 30

		self.Y_RATES = (self.YResolution - 55) * 36 / 40

		self.IN_PORT_PANE_WIDTH = self.XResolution * 9 / 20
		self.X_IN_PORT = self.XResolution * 3 / 10
		self.PANE_HEIGHT = (self.YResolution - 55) * 31 / 40
		self.X_DOCK = self.XResolution * 7 / 10

		self.SHIP_ICON_SIZE = self.YResolution / 10
		self.CARGO_ICON_SIZE = self.XResolution / 25
		self.CARGO_SPACING  = self.CARGO_ICON_SIZE + 2

		self.H_TEXT_MARGIN = self.YResolution / 30
		self.W_TEXT_MARGIN = self.XResolution / 30

		self.X_RECRUIT_PANE = self.X_IN_PORT + self.IN_PORT_PANE_WIDTH + (self.W_TEXT_MARGIN / 2)
		self.PANE_WIDTH = self.XResolution * 7 / 20
		self.W_SLIDER = self.PANE_WIDTH - (self.W_TEXT_MARGIN * 2)
		self.H_LOADING_SLIDER = self.YResolution * 7 / 10
		self.Y_UPPER_EDGE = self.YResolution / 10
		self.RECRUIT_PANE_HEIGHT = self.YResolution / 7

		self.Y_RECRUIT_OFFSET = 25
		self.Y_TITLE = 4
		self.Y_BOUND = self.Y_UPPER_EDGE + (self.PANE_HEIGHT / 2)
		self.Y_DOCKS_OFFSET = 50
		self.H_DOCK = (self.PANE_HEIGHT - (self.H_TEXT_MARGIN * 2)) * 35 / 100
	
		Y_INPORT = self.YResolution - self.YResolution * 4 / 23 - self.YResolution * 44 / 96
	
		self.EUROPE_EAST = CvUtil.findInfoTypeNum('EUROPE_EAST')
		self.EUROPE_WEST = CvUtil.findInfoTypeNum('EUROPE_WEST')
	
		screen.setDimensions(0, 0, self.XResolution, self.YResolution)
		screen.showWindowBackground(False)
	
		# Water Animation
		screen.addUnitGraphicGFC("WaterAnim_Widget", gc.getInfoTypeForString("UNIT_CARAVEL"), -1, 0, 0, self.XResolution, self.XResolution, WidgetTypes.WIDGET_UNIT_MODEL, -1, -1, 0, 0, 0, true)			
	
		# show background
		if self.Pirates:
			screen.addDDSGFC("EuropeScreenBackground", "Art/Interface/Screens/Europe/PirateBackground.dds", 0, 0, self.XResolution, self.YResolution, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			if CyGame().getGameTurn() % 2 == 0:
				screen.addBonusGraphicGFC("Crabs", gc.getInfoTypeForString("BONUS_CRAB"), self.XResolution * 4 / 5, self.YResolution / 2 + self.YResolution / 25, self.XResolution / 5, self.YResolution / 10, WidgetTypes.WIDGET_GENERAL, -1, -1, 0, 0, 0.75, false)
			else:
				screen.addBonusGraphicGFC("Fish", gc.getInfoTypeForString("BONUS_FISH"), self.XResolution * 3 / 5, self.YResolution / 3, self.XResolution / 5, self.YResolution / 10, WidgetTypes.WIDGET_GENERAL, -1, -1, 0, 0, 0.75, false)

		elif not self.iThisWinter:
			if self.iVideo > 0 and iCurrentTurn % self.iVideo == 0 and not iCurrentTurn == 0 and not CyUserProfile().getGraphicOption(gc.getInfoTypeForString("GRAPHICOPTION_NO_MOVIES")):
				screen.playMovie("Art/Interface/Screens/Europe/intro.bik", 0, 0, self.XResolution, self.YResolution * 10 / 43, 0)
				screen.addDDSGFC("EuropeScreenBackground", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BACKGROUND").getPath(), 0, 0, self.XResolution, self.YResolution, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			else:
				screen.addDDSGFC("EuropeScreenBackground", "Art/Interface/Screens/Europe/FullBackground.dds", 0, 0, self.XResolution, self.YResolution, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		else:
			screen.addDDSGFC("EuropeScreenBackground", "Art/Interface/Screens/Europe/BackgroundWinter.dds", 0, 0, self.XResolution, self.YResolution, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# InBound
		if (self.Pirates):
			screen.addScrollPanel("InBoundList", u"", self.W_TEXT_MARGIN / 2, self.YResolution * 56 / 320, self.W_SLIDER * 3 / 2, self.YResolution / 14, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		else:
			screen.addScrollPanel("InBoundList", u"", self.W_TEXT_MARGIN / 2, self.YResolution * 61 / 320, self.W_SLIDER * 3 / 2, self.YResolution / 14, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# OutBound
		if (self.Pirates):
			screen.addScrollPanel("OutBoundList", u"", self.W_TEXT_MARGIN / 4, self.YResolution / 4, self.W_SLIDER * 2, self.SHIP_ICON_SIZE * 3 + 20, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_SAIL, UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE, -1 )
		else:
			screen.addScrollPanel("OutBoundList", u"", self.W_TEXT_MARGIN / 4, self.YResolution * 9 / 40, self.W_SLIDER * 2, self.SHIP_ICON_SIZE * 3 + 20, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_SAIL, UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE, -1 )
	
		# In Port
		if (self.Pirates):
			screen.addScrollPanel("LoadingList", u"", -5, Y_INPORT + self.YResolution / 10, self.XResolution + 10, self.YResolution - Y_INPORT - 23, PanelStyles.PANEL_STYLE_MAIN, True, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addScrollPanel("OutBoundListOverlay", u"", self.W_TEXT_MARGIN / 4, self.YResolution / 4, self.W_SLIDER * 2, self.SHIP_ICON_SIZE * 34 / 16, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_SAIL, UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE, -1 )
		else:
			screen.addScrollPanel("LoadingList", u"", -5, Y_INPORT, self.XResolution + 10, self.YResolution - Y_INPORT - 23, PanelStyles.PANEL_STYLE_MAIN, True, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addScrollPanel("OutBoundListOverlay", u"", self.W_TEXT_MARGIN / 4, self.YResolution * 9 / 40, self.W_SLIDER * 2, self.SHIP_ICON_SIZE * 34 / 16, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_SAIL, UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE, -1 )
	
		# Dock
		if (self.Pirates):
			screen.addScrollPanel("DockList", u"", self.X_IN_PORT - self.CARGO_ICON_SIZE * 2, self.YResolution / 4 - self.CARGO_ICON_SIZE * 3 / 2 - 3, self.XResolution * 2 / 7, self.CARGO_ICON_SIZE * 5 / 2, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_DOCK, -1, -1 )
		else:
			screen.addScrollPanel("DockList", u"", self.X_IN_PORT + self.IN_PORT_PANE_WIDTH * 35 / 48, self.YResolution * 2 / 5 - self.CARGO_ICON_SIZE * 2, self.XResolution * 2 / 7, self.CARGO_ICON_SIZE * 5 / 2, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_DOCK, -1, -1 )
	
		# Messages
		screen.setImageButton("TradeButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_TURNLOG_ICON").getPath(), self.W_TEXT_MARGIN / 5, self.YResolution - 17 - self.CARGO_ICON_SIZE * 3 / 4 - (self.YResolution * 2 / 23 * 6 / 7) / 2, self.CARGO_ICON_SIZE * 3 / 2, self.CARGO_ICON_SIZE * 3 / 2, WidgetTypes.WIDGET_GENERAL, self.TRADE_LOG, -1)
		screen.addPanel("TradeMessagePanel", u"", "shows trade messages", True, False, self.W_TEXT_MARGIN / 5, self.YResolution - self.YResolution / 3 - 7, self.XResolution / 5 + self.W_TEXT_MARGIN / 2 + 10, self.YResolution / 4 - 7, PanelStyles.PANEL_STYLE_FLAT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.attachListBoxGFC ("TradeMessagePanel", "MessageList", "shows trade messages", TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect("MessageList", False)
	
		# Purchase
		if (gc.getPlayer(gc.getGame().getActivePlayer()).canTradeWithEurope()):
			screen.setImageButton("HireButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_PURCHASE_UNIT").getPath(), self.XResolution - self.CARGO_ICON_SIZE * 3 / 2 - self.W_TEXT_MARGIN / 5, self.YResolution - 17 - self.CARGO_ICON_SIZE * 3 / 4 - (self.YResolution * 2 / 23 * 6 / 7) / 2, self.CARGO_ICON_SIZE * 3 / 2,self.CARGO_ICON_SIZE * 3 / 2, WidgetTypes.WIDGET_GENERAL, self.BUY_UNIT_BUTTON_ID, -1)
	
		# draw the contents
		self.drawContents()

	def drawContents(self):

		player = gc.getPlayer(gc.getGame().getActivePlayer())
		playerEurope = gc.getPlayer(player.getParent())
		screen = self.getScreen()

		self.deleteAllWidgets()
		self.makeSound("initSound")
	
		if self.iThisWinter:
			hudColor = "[COLOR_FONT_GOLD]"
		else:
			hudColor = "[COLOR_WHITE]"
	
		screen.setText(self.getNextWidgetName(), "Background", u"<font=4>" + localText.getText(hudColor, ()) + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_TREASURY", (player.getGold(), )).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.W_TEXT_MARGIN / 2, self.Y_TITLE + self.YResolution / 60, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.TREASURY_ID, -1 )
		screen.setText("EuropeScreenExitWidget", "Background", u"<font=4>" + localText.getText(hudColor, ()) + localText.getText("EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT + self.XResolution / 75 - 15, self.Y_TITLE + self.YResolution / 60, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setText(self.getNextWidgetName(), "Background", u"<font=4>" + localText.getText(hudColor, ()) + localText.getText("TXT_KEY_MISC_TAX_RATE", (player.getTaxRate(), ())).upper() + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.XResolution - self.W_TEXT_MARGIN / 2 - self.CARGO_ICON_SIZE * 3 / 2 - 15, self.Y_TITLE + self.YResolution / 60, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		if (sdToolKit.sdGetVal('komaScreens', player.getName(), 'TradeBox') == 1):
			screen.show("TradeMessagePanel")
		else:
			screen.hide("TradeMessagePanel")
	
		#Units
		InboundUnitsList = []
		iSeaUnitCount = 0
	
		(unit, iter) = player.firstUnit()
		while (unit):
			if (not unit.isCargo() and not unit.isDelayedDeath()):
				if (unit.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE):
					if not unit.getID() in self.EuropeUnitsList:
						self.EuropeUnitsList.append(unit.getID())
				elif (unit.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE):
					if not unit.getID() in self.OutboundUnitsList:
						self.OutboundUnitsList.append(unit.getID())
				elif (unit.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_TO_EUROPE):
					InboundUnitsList.append(unit)
				
				if (gc.getUnitInfo(unit.getUnitType()).getDomainType() == DomainTypes.DOMAIN_SEA):
					iSeaUnitCount += 1
	
			(unit, iter) = player.nextUnit(iter)

		InboundUnitsList.sort(lambda y, x: cmp(player.getUnit(x.getID()).getUnitTravelTimer(), player.getUnit(y.getID()).getUnitTravelTimer()))

		ShipPanelWidth = self.IN_PORT_PANE_WIDTH - (self.W_TEXT_MARGIN * 3)			
		ShipPanelHight = self.YResolution / 10
		if (ShipPanelHight < 90):
			ShipPanelHight = 90
		yLocation_InPort = 0
		yLocation_ToEurope = 0
		yLocation_FromEurope = 0
		yCenterCorrection = (self.SHIP_ICON_SIZE / 2) - (self.CARGO_ICON_SIZE / 2)
	
		xLocation_InPort = self.XResolution / 2 - self.SHIP_ICON_SIZE * 11 / 8
	
		#in port
		for iUnit in self.EuropeUnitsList:
			unit = player.getUnit(iUnit)

			YieldOnBoard = False
			iCargoCount = 0
			plot = unit.plot()

			screen.setImageButtonAt(self.getNextWidgetName(), "LoadingList", unit.getFullLengthIcon(), xLocation_InPort, yLocation_InPort, self.SHIP_ICON_SIZE * 14 / 4, self.SHIP_ICON_SIZE * 24 / 4, WidgetTypes.WIDGET_SHIP_CARGO, unit.getID(), -1)

			for i in range(unit.cargoSpace()):
				screen.addDDSGFCAt(self.getNextWidgetName(), "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_CARGO").getPath(), xLocation_InPort + ((self.SHIP_ICON_SIZE * 15 / 4) / 2) - ((self.CARGO_SPACING * unit.cargoSpace()) / 2) + (self.CARGO_SPACING * i) , self.SHIP_ICON_SIZE * 29 / 8, self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE, WidgetTypes.WIDGET_SHIP_CARGO, unit.getID(), -1, False)

			for i in range(plot.getNumUnits()):
				loopUnit = plot.getUnit(i)
				transportUnit = loopUnit.getTransportUnit()
				if (not transportUnit.isNone() and transportUnit.getID() == unit.getID() and transportUnit.getOwner() == unit.getOwner()):
					if loopUnit.isGoods():
						szText = u"<font=2>%s</font>" % loopUnit.getYieldStored()
						iWidgetId = self.YIELD_CARGO_BUTTON_ID
						YieldOnBoard = True
					else:
						szText = ""
						iWidgetId = self.UNIT_CARGO_BUTTON_ID

					screen.addDragableButtonAt("LoadingList", self.getNextWidgetName(), loopUnit.getButton(), "", xLocation_InPort + ((self.SHIP_ICON_SIZE * 15 / 4) / 2) - ((self.CARGO_SPACING * unit.cargoSpace()) / 2) + (self.CARGO_SPACING * iCargoCount) , self.SHIP_ICON_SIZE * 29 / 8, self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE, WidgetTypes.WIDGET_SHIP_CARGO, loopUnit.getID(), transportUnit.getID(), ButtonStyles.BUTTON_STYLE_LABEL)
					iCargoCount = iCargoCount + 1

			if (YieldOnBoard):
				screen.setImageButtonAt(self.getNextWidgetName(), "LoadingList", gc.getActionInfo(gc.getInfoTypeForString("COMMAND_YIELD_TRADE")).getButton(), xLocation_InPort + self.SHIP_ICON_SIZE * 13 / 4 - self.CARGO_ICON_SIZE * 5 / 4, yLocation_InPort +  self.SHIP_ICON_SIZE * 22 / 8, self.CARGO_ICON_SIZE * 5 / 4, self.CARGO_ICON_SIZE * 5 / 4, WidgetTypes.WIDGET_GENERAL, self.SELL_ALL, unit.getID())
			if (not unit.isFull() and player.getNumEuropeUnits() > 0 and not unit.getUnitType() == gc.getInfoTypeForString("UNIT_PRIVATEER")):
				screen.setImageButtonAt(self.getNextWidgetName(), "LoadingList", gc.getActionInfo(gc.getInfoTypeForString("COMMAND_LOAD")).getButton(), xLocation_InPort + self.SHIP_ICON_SIZE * 13 / 4 - self.CARGO_ICON_SIZE * 34 / 16, yLocation_InPort +  self.SHIP_ICON_SIZE * 22 / 8, self.CARGO_ICON_SIZE * 5 / 4, self.CARGO_ICON_SIZE * 5 / 4, WidgetTypes.WIDGET_GENERAL, self.LOAD_ALL, unit.getID())
			if (iCargoCount == 0) and (gc.getUnitInfo(unit.getUnitType()).getEuropeCost() != -1) and (iSeaUnitCount > 1) and (self.iSellShip > 0):
				screen.setImageButtonAt(self.getNextWidgetName(), "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_PURCHASE_UNIT").getPath(), xLocation_InPort + self.SHIP_ICON_SIZE * 13 / 4 - self.CARGO_ICON_SIZE * 5 / 4, yLocation_InPort +  self.SHIP_ICON_SIZE * 22 / 8, self.CARGO_ICON_SIZE * 5 / 4, self.CARGO_ICON_SIZE * 5 / 4, WidgetTypes.WIDGET_GENERAL, self.SELL_SHIP, unit.getID())

			screen.setImageButtonAt(self.getNextWidgetName(), "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SAIL").getPath(), xLocation_InPort + self.SHIP_ICON_SIZE * 2 / 4, yLocation_InPort +  self.SHIP_ICON_SIZE * 22 / 8, self.CARGO_ICON_SIZE * 5 / 4, self.CARGO_ICON_SIZE * 5 / 4, WidgetTypes.WIDGET_GENERAL, self.SAIL_TO_NEW_WORLD, unit.getID())

			xLocation_InPort += self.XResolution * 4 / 13
	
		#inbound
		ShipPanelHight = self.YResolution / 12
		xLocation_ToEurope = 0

		self.InboundCargoDictionary = {}

		for unit in InboundUnitsList:
			plot = unit.plot()

			for i in range(plot.getNumUnits()):
				loopUnit = plot.getUnit(i)
				transportUnit = loopUnit.getTransportUnit()

				if (loopUnit.isCargo()):
					if (not transportUnit.isNone() and transportUnit.getID() == unit.getID() and transportUnit.getOwner() == unit.getOwner()):
						iCargoStored = 0

						if not loopUnit.getTransportUnit().getID() in self.InboundCargoDictionary:
							self.InboundCargoDictionary[loopUnit.getTransportUnit().getID()] = {}
						if loopUnit.getUnitType() in self.InboundCargoDictionary[loopUnit.getTransportUnit().getID()]:
							iCargoStored = int(self.InboundCargoDictionary[loopUnit.getTransportUnit().getID()][loopUnit.getUnitType()])
						if loopUnit.isGoods():
							self.InboundCargoDictionary[loopUnit.getTransportUnit().getID()][loopUnit.getUnitType()] = loopUnit.getYieldStored() + iCargoStored
						else:
							self.InboundCargoDictionary[loopUnit.getTransportUnit().getID()][loopUnit.getUnitType()] = iCargoStored + 1

			screen.addDDSGFCAt(self.getNextWidgetName(), "InBoundList", unit.getFullLengthIcon().rstrip(".dds") + "_inbound.dds", xLocation_ToEurope + self.XResolution / 55, yLocation_ToEurope, 12 * self.SHIP_ICON_SIZE / 40, 21 * self.SHIP_ICON_SIZE / 40, WidgetTypes.WIDGET_GENERAL, self.TRAVEL_INFO, unit.getID(), False)
			xLocation_ToEurope += (self.SHIP_ICON_SIZE * 4 / (len(InboundUnitsList) + 1)) * 4 / 3
	
		#outbound
		iNumOutbound = len(self.OutboundUnitsList)

		if (iNumOutbound < 5): 
			iNumOutbound = 5

		xLocation_FromEurope = 0
		xLocation_Space = 2 * ShipPanelHight / iNumOutbound * 4
		SHIP_HEIGHT = self.YResolution / 10
		Y_OVERLAY = self.YResolution / 50
		OVERLAY_HEIGHT = SHIP_HEIGHT * 31 / 32	
	
		self.OutboundCargoDictionary = {}
	
		for iUnit in self.OutboundUnitsList:
			unit = player.getUnit(iUnit)	

			if self.OutboundUnitsList.index(iUnit)% 2 == 1:
				xLocation_FromEurope += xLocation_Space / 2
				yLocation_FromEurope = SHIP_HEIGHT * 3 / 5
				SHIP_HEIGHT += 25
				Y_OVERLAY = yLocation_FromEurope * 15 / 8
				OVERLAY_HEIGHT = SHIP_HEIGHT * 14 / 16

			elif self.OutboundUnitsList.index(iUnit) % 2 == 0 and not self.OutboundUnitsList.index(iUnit) == 0:
				xLocation_FromEurope += xLocation_Space / 3
				yLocation_FromEurope = 0
				SHIP_HEIGHT -= 25
				Y_OVERLAY = self.YResolution / 50
				OVERLAY_HEIGHT = SHIP_HEIGHT * 31 / 32

			plot = unit.plot()

			for i in range(plot.getNumUnits()):
				loopUnit = plot.getUnit(i)
				transportUnit = loopUnit.getTransportUnit()
				if (loopUnit.isCargo()):
					if (not transportUnit.isNone() and transportUnit.getID() == unit.getID() and transportUnit.getOwner() == unit.getOwner()):
						iCargoStored = 0

						if not loopUnit.getTransportUnit().getID() in self.OutboundCargoDictionary:
							self.OutboundCargoDictionary[loopUnit.getTransportUnit().getID()] = {}
						if loopUnit.getUnitType() in self.OutboundCargoDictionary[loopUnit.getTransportUnit().getID()]:
							iCargoStored = int(self.OutboundCargoDictionary[loopUnit.getTransportUnit().getID()][loopUnit.getUnitType()])
						if loopUnit.isGoods():
							self.OutboundCargoDictionary[loopUnit.getTransportUnit().getID()][loopUnit.getUnitType()] = loopUnit.getYieldStored() + iCargoStored
						else:
							self.OutboundCargoDictionary[loopUnit.getTransportUnit().getID()][loopUnit.getUnitType()] = iCargoStored + 1

			OutboundIcon = self.getNextWidgetName()
			screen.addDDSGFCAt(OutboundIcon, "OutBoundList", unit.getFullLengthIcon(), xLocation_FromEurope * 7 / 4, yLocation_FromEurope, SHIP_HEIGHT * 5 / 4, SHIP_HEIGHT * 8 / 4, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
			if (yLocation_FromEurope == 0):
				screen.moveBackward(OutboundIcon)

			iTravelTimer = player.getUnit(unit.getID()).getUnitTravelTimer()
			iMaxTravelTimer = self.getMaxTravelTimer(unit.plot())
			if (iMaxTravelTimer - iTravelTimer > 0):
				screen.addDDSGFCAt(self.getNextWidgetName(), "OutBoundListOverlay", "", xLocation_FromEurope * 7 / 4, Y_OVERLAY, SHIP_HEIGHT * 5 / 4, OVERLAY_HEIGHT, WidgetTypes.WIDGET_GENERAL, self.TRAVEL_INFO, unit.getID(), False)
			else:
				screen.addDDSGFCAt(self.getNextWidgetName(), "OutBoundListOverlay", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SAIL").getPath(), xLocation_FromEurope * 7 / 4 + SHIP_HEIGHT * 5 / 8, Y_OVERLAY + OVERLAY_HEIGHT * 1 / 3, self.CARGO_ICON_SIZE * 3 / 4, self.CARGO_ICON_SIZE * 3 / 4, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
				screen.setImageButtonAt(self.getNextWidgetName(), "OutBoundListOverlay", "", xLocation_FromEurope * 7 / 4, Y_OVERLAY, SHIP_HEIGHT * 5 / 4, OVERLAY_HEIGHT, WidgetTypes.WIDGET_GENERAL, self.RECALL, unit.getID())

		# Units waiting on Docks
		xLocation = 0
		iNumDocks = player.getNumEuropeUnits()
		if (iNumDocks < 5):
			iNumDocks = 5
	
		for i in range(player.getNumEuropeUnits()):
			loopUnit = player.getEuropeUnit(i)
			yLocation = 0
			UNIT_WIDTH = self.CARGO_ICON_SIZE
			UNIT_HEIGHT = self.CARGO_ICON_SIZE * 2

			if (loopUnit.getUnitType() == gc.getInfoTypeForString("UNIT_CRIMINAL")):
				yLocation = -5
				UNIT_WIDTH = self.CARGO_ICON_SIZE * 11 / 10
				UNIT_HEIGHT = self.CARGO_ICON_SIZE * 22 / 10
			elif (loopUnit.getUnitType() == gc.getInfoTypeForString("UNIT_VETERAN")) and (loopUnit.getProfession() == gc.getInfoTypeForString("PROFESSION_DRAGOON")):
				yLocation = -(self.YResolution / 40)
				UNIT_WIDTH = self.CARGO_ICON_SIZE * 13 / 10
				UNIT_HEIGHT = self.CARGO_ICON_SIZE * 30 / 10
			elif (loopUnit.getProfession() == gc.getInfoTypeForString("PROFESSION_SOLDIER")):
				if (loopUnit.getUnitType() == gc.getInfoTypeForString("UNIT_VETERAN")):
					UNIT_WIDTH = self.CARGO_ICON_SIZE * 13 / 11
					UNIT_HEIGHT = self.CARGO_ICON_SIZE * 26 / 11
				else:
					UNIT_WIDTH = self.CARGO_ICON_SIZE * 13 / 11
					UNIT_HEIGHT = self.CARGO_ICON_SIZE * 23 / 11
				yLocation = -8
			elif (loopUnit.getUnitType() == gc.getInfoTypeForString("UNIT_FARMER")):
				yLocation = -6
				UNIT_WIDTH = self.CARGO_ICON_SIZE * 12 / 11
				UNIT_HEIGHT = self.CARGO_ICON_SIZE * 24 / 11
			elif (loopUnit.getUnitType() == gc.getInfoTypeForString("UNIT_CANNON")):
				yLocation = -12
				UNIT_WIDTH = self.CARGO_ICON_SIZE * 13 / 10
				UNIT_HEIGHT = self.CARGO_ICON_SIZE * 26 / 10
			elif (loopUnit.getUnitType() == gc.getInfoTypeForString("UNIT_STATESMAN")):
				yLocation = 5
				UNIT_WIDTH = self.CARGO_ICON_SIZE * 18 / 20
				UNIT_HEIGHT = self.CARGO_ICON_SIZE * 19 / 10
	
			if (self.Pirates):
				if (loopUnit.getUnitType() == gc.getInfoTypeForString("UNIT_PIRATEVETERAN")):
					yLocation = 3
					UNIT_WIDTH = self.CARGO_ICON_SIZE * 19 / 20
					UNIT_HEIGHT = self.CARGO_ICON_SIZE * 2

				screen.addDragableButtonAt("DockList", self.getNextWidgetName(), loopUnit.getFullLengthIcon(), "", xLocation, yLocation, UNIT_WIDTH * 4 / 5, UNIT_HEIGHT * 4 / 5, WidgetTypes.WIDGET_DOCK, loopUnit.getID(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
			else:
				screen.addDragableButtonAt("DockList", self.getNextWidgetName(), loopUnit.getFullLengthIcon(), "", xLocation, yLocation, UNIT_WIDTH, UNIT_HEIGHT, WidgetTypes.WIDGET_DOCK, loopUnit.getID(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
	
			xLocation += (self.CARGO_ICON_SIZE * 6 / iNumDocks)
	
		# Units to Recruit
		iUnitHeight = 100 + ((self.YResolution - 768) / 11)

		if (self.Pirates):
			iStartX = self.XResolution * 2 / 3
			iY = self.YResolution / 6 - 8
		else:
			iStartX = self.XResolution * 91 / 112
			iY = self.YResolution - self.YResolution * 2 / 21 - iUnitHeight
	
		addUnitScale1 = [ "UNIT_CRIMINAL", "UNIT_VETERAN" ]
		addUnitScale2 = [ "UNIT_INDENTURED_SERVANT", "UNIT_PIONEER", "UNIT_COLONIST", "UNIT_SCOUT" ]
	
		for i in range (gc.getDefineINT("DOCKS_NEXT_UNITS")):
			if player.getDocksNextUnit(i) != UnitTypes.NO_UNIT:
				UnitInfo = gc.getUnitInfo(player.getDocksNextUnit(i))
				if (self.Pirates):
					iX = i * self.X_RECRUIT_PANE * 2 / 21
				else:
					iX = i * self.X_RECRUIT_PANE * 1 / 21

				fUnitScale = 1.0				
				if (UnitInfo.getType() in addUnitScale1) and not self.Pirates:
					fUnitScale += 0.05
				if (UnitInfo.getType() in addUnitScale2):
					fUnitScale += 0.1
				screen.addUnitGraphicGFC(self.getNextWidgetName(), player.getDocksNextUnit(i), UnitInfo.getDefaultProfession(), iStartX + iX + self.X_RECRUIT_PANE / 22, iY, self.RECRUIT_PANE_HEIGHT * 1 / 3, iUnitHeight, WidgetTypes.WIDGET_PLAYER_HURRY, gc.getInfoTypeForString("HURRY_IMMIGRANT"), i, 0, 0, fUnitScale, false)			
				
				if (self.Pirates):
					iY += self.YResolution / 75

		# Trade Messages
		screen.clearListBoxGFC("MessageList")
		for i in range(player.getNumTradeMessages()):
			screen.prependListBoxString("MessageList", player.getTradeMessage(i), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Yield Rates
		self.YieldList = []
	
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			kYield = gc.getYieldInfo(iYield)
			if kYield.isCargo():
				self.YieldList.append(iYield)
	
		YieldAreaWidth = (self.XResolution / 20) * len(self.YieldList)
		xLocation = 0
		BOX_WIDTH = self.XResolution / len(self.YieldList)
		BOX_HEIGHT = self.YResolution * 2 / 21
		Yield_space = (self.XResolution - (BOX_WIDTH * 6 / 7 * len(self.YieldList))) / 2
	
		for iYield in self.YieldList:
			kYield = gc.getYieldInfo(iYield)
			iSellPrice = playerEurope.getYieldSellPrice(iYield)
			iBuyPrice = playerEurope.getYieldBuyPrice(iYield)
			screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), xLocation + Yield_space, self.YResolution - BOX_HEIGHT * 6 / 7 - 17, BOX_WIDTH * 6 / 7, BOX_HEIGHT * 6 / 7, WidgetTypes.WIDGET_MOVE_CARGO_TO_TRANSPORT, iYield, -1 )
			screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), xLocation + Yield_space, self.YResolution - BOX_HEIGHT * 6 / 7 - 17, BOX_WIDTH * 6 / 7, BOX_HEIGHT * 6 / 7, WidgetTypes.WIDGET_MOVE_CARGO_TO_TRANSPORT, iYield, -1 )
			szPrices = u"<font=3>%d/%d</font>" % (iBuyPrice, iSellPrice)

			if not player.isYieldEuropeTradable(iYield):
				szPrices = u"<color=255,0,0>" + szPrices + u"</color>"

			screen.addDragableButton(self.getNextWidgetName(), gc.getYieldInfo(iYield).getIcon(), "", xLocation + BOX_WIDTH / 10 + Yield_space, self.YResolution - (self.YResolution * 2 / 23) * 2 / 3 - 17, BOX_WIDTH * 2 / 3, (self.YResolution * 2 / 23) * 2 / 3, WidgetTypes.WIDGET_MOVE_CARGO_TO_TRANSPORT, iYield, -1, ButtonStyles.BUTTON_STYLE_IMAGE )
	
			screen.setLabel("EuropePrices" + str(iYield), "Background", szPrices, CvUtil.FONT_CENTER_JUSTIFY, xLocation + self.XResolution / 38 + Yield_space, self.YResolution - self.YResolution * 3 / 46 - 25, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_MOVE_CARGO_TO_TRANSPORT, iYield, -1)
			screen.moveBackward("EuropePrices" + str(iYield))
	
			xLocation += BOX_WIDTH * 6 / 7
	
		#Immigration Bar
		if (not self.Pirates):
			szWidget = self.getNextWidgetName()

			screen.addStackedBarGFC(szWidget, self.XResolution / 2 - self.XResolution / 12, self.Y_TITLE + self.YResolution / 75, self.XResolution / 6, 30, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, self.HELP_CROSS_RATE, -1)
			screen.setStackedBarColors(szWidget, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_WATER_TEXT"))
			screen.setStackedBarColors(szWidget, InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_CITY_BLUE"))
			screen.setStackedBarColors(szWidget, InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setStackedBarColors(szWidget, InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
			fStoredPercent = float(player.getCrossesStored()) / float(player.immigrationThreshold())
			screen.setBarPercentage(szWidget, InfoBarTypes.INFOBAR_STORED, fStoredPercent)
			if (fStoredPercent < 1.0):
				fRatePercent = float(player.getYieldRate(YieldTypes.YIELD_CROSSES)) / float(player.immigrationThreshold()) / (1 - fStoredPercent)
				screen.setBarPercentage(szWidget, InfoBarTypes.INFOBAR_RATE, fRatePercent)
			screen.setLabel(self.getNextWidgetName(), "", u"<font=3>" + localText.getText("TXT_KEY_IMMIGRATION_BAR", (player.getCrossesStored(), player.immigrationThreshold(), gc.getYieldInfo(YieldTypes.YIELD_CROSSES).getChar())) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.XResolution / 2, self.Y_TITLE + self.YResolution / 50, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, self.HELP_CROSS_RATE, -1)

		return 0

	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def deleteAllWidgets(self):
		screen = self.getScreen()
		i = self.nWidgetCount - 1
	
		while (i >= 0):
			self.nWidgetCount = i
			if (self.getNextWidgetName() != "Immigrant_Widget") or (self.getNextWidgetName() != "WaterAnim_Widget"):
				screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = 0
	
	def handleInput(self, inputClass):
		screen = self.getScreen()
	
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		playerEurope = gc.getPlayer(player.getParent())

		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_PLAYER_HURRY):
				self.makeSound("unitsSelectSound")

			if (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):
				if (inputClass.getData1() == self.BUY_UNIT_BUTTON_ID) :
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PURCHASE_EUROPE_UNIT)
					CyInterface().addPopup(popupInfo, gc.getGame().getActivePlayer(), true, false)

				elif (inputClass.getData1() == self.SAIL_TO_NEW_WORLD) :
					self.dialogBox(inputClass.getData2(), localText.getText("TXT_KEY_EU_SAIL", ()), u"", self.SAIL_EXEC)

				elif (inputClass.getData1() == self.SAIL_EXEC) :
					transport = player.getUnit(inputClass.getData2())
					index = inputClass.getID()

					if (inputClass.getFunctionName() == "DialogSelection") :
						if (not transport.isNone()) and transport.getUnitTravelState() != UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE:
							if index == 0:		#sail East
								pBestPlot = self.pPlotEast
							elif index == 1:	#sail West
								pBestPlot = self.pPlotWest
							elif index >= 2:	#sail to city
								pCity = self.CityPlotList[index - 2][0]
								pBestPlot = self.CityPlotList[index - 2][1]

								if pBestPlot == None:
									pBestPlot = self.getBestCityPlot(pCity.plot()) 
									self.CityPlotList[index - 2] = [pCity, pBestPlot]

								#transport.getGroup().clearMissionQueue ()
								#transport.getGroup().pushMoveToMission(pCity.plot().getX(), pCity.plot().getY())
							
							if index >= 2:
								CyMessageControl().sendApplyEvent(CvUtil.EventDoEuropeScreen, EventContextTypes.EVENTCONTEXT_ALL, (1, transport.getID(), pBestPlot.getX(), pBestPlot.getY(), pCity.plot().getX(), pCity.plot().getY(), -1))
							else:
								CyMessageControl().sendApplyEvent(CvUtil.EventDoEuropeScreen, EventContextTypes.EVENTCONTEXT_ALL, (2, transport.getID(), pBestPlot.getX(), pBestPlot.getY(), -1, -1, -1))
							#transport.setXY(pBestPlot.getX(), pBestPlot.getY(), true, false, false)
							CyMessageControl().sendDoCommand(transport.getID(), CommandTypes.COMMAND_SAIL_TO_EUROPE, UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE, -1, false)

							self.EuropeUnitsList.remove(transport.getID())
							self.makeSound("unitsOrderSound")

					self.hideDialogBox(index)
					for iYield in self.YieldList :
						screen.show("EuropePrices" + str(iYield))

				elif (inputClass.getData1() == self.SELL_ALL) :
					player = gc.getPlayer(gc.getGame().getActivePlayer())
					transport = player.getUnit(inputClass.getData2())

					(unit, iter) = player.firstUnit()
					while (unit):
						if (unit.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE and unit.isCargo() and unit.isGoods()):
							if (unit.getTransportUnit().getID() == transport.getID()):
								CyMessageControl().sendPlayerAction(player.getID(), PlayerActionTypes.PLAYER_ACTION_SELL_YIELD_UNIT, 0, unit.getYieldStored(), unit.getID())
						(unit, iter) = player.nextUnit(iter)
					screen.setSoundId(CyAudioGame().Play2DSound("AS2D_BUILD_BANK"))

				elif (inputClass.getData1() == self.LOAD_ALL) :
					player = gc.getPlayer(gc.getGame().getActivePlayer())
					transport = player.getUnit(inputClass.getData2())
					for i in range(player.getNumEuropeUnits()):
						loopUnit = player.getEuropeUnit(i)
						if (not transport.isNone() and transport.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE and not transport.isFull()):
							CyMessageControl().sendPlayerAction(player.getID(), PlayerActionTypes.PLAYER_ACTION_LOAD_UNIT_FROM_EUROPE, loopUnit.getID(), inputClass.getData2(), -1)
					screen.setSoundId(CyAudioGame().Play2DSound("AS2D_REVOLTEND"))

				elif (inputClass.getData1() == self.RECALL) :
					transport = player.getUnit(inputClass.getData2())
					if (not transport.isNone()) and transport.getUnitTravelState() != UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE:
						#transport.setUnitTravelState(1,false)
						#transport.getGroup().clearMissionQueue()	
						CyMessageControl().sendApplyEvent(CvUtil.EventDoEuropeScreen, EventContextTypes.EVENTCONTEXT_ALL, (3, transport.getID(), -1, -1, -1, -1, -1))
						self.OutboundUnitsList.remove(transport.getID())
						screen.setSoundId(CyAudioGame().Play2DSound("AS2D_REVOLTSTART"))
						#if (CyInterface().isDirty(InterfaceDirtyBits.EuropeScreen_DIRTY_BIT)):
						#	CyInterface().setDirty(InterfaceDirtyBits.EuropeScreen_DIRTY_BIT, False)
						#self.drawContents()
						
				elif (inputClass.getData1() == self.TRADE_LOG) :
					if (sdToolKit.sdGetVal('komaScreens', player.getName(), 'TradeBox') == 1):
						sdToolKit.sdSetVal('komaScreens', player.getName(), 'TradeBox', 0)
					else:
						sdToolKit.sdSetVal('komaScreens', player.getName(), 'TradeBox', 1)
	
					if (CyInterface().isDirty(InterfaceDirtyBits.EuropeScreen_DIRTY_BIT)):
						CyInterface().setDirty(InterfaceDirtyBits.EuropeScreen_DIRTY_BIT, False)
					self.drawContents()

				elif (inputClass.getData1() == self.SELL_SHIP) :
					transport = player.getUnit(inputClass.getData2())
					textMessage = localText.getText("TXT_KEY_EU_SELL_MESSAGE", (transport.getName(), self.getShipSellPrice(inputClass.getData2())))
					self.dialogBox(inputClass.getData2(), localText.getText("TXT_KEY_EU_SELL_LABEL", ()), textMessage, self.SELL_SHIP_EXEC)
					screen.addUnitGraphicGFC ("DialogImage" + str(0), transport.getUnitType(), -1, self.XResolution / 2 - 217, self.YResolution / 6 + 61, 192, 130, WidgetTypes.WIDGET_GENERAL, -1, -1, 0, 0, 0.85, true)
					for i in range(4):
						screen.moveBackward("DialogImage" + str(0))
					screen.setLabelAt("Price", "DialogMainPanel", localText.getText("%d1[ICON_GOLD]", (self.getShipSellPrice(inputClass.getData2()), ())), CvUtil.FONT_CENTER_JUSTIFY, 136, 205, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)			
	
				elif (inputClass.getData1() == self.SELL_SHIP_EXEC) :
					transport = player.getUnit(inputClass.getData2())
					iSellPrice = self.getShipSellPrice(inputClass.getData2())
					if (not transport.isNone() and not iSellPrice == -1):
						transport.kill(false)
						player.changeGold(iSellPrice)
						self.EuropeUnitsList.remove(transport.getID())
						screen.setSoundId(CyAudioGame().Play2DSound("AS2D_BUILD_BANK"))
						if (CyInterface().isDirty(InterfaceDirtyBits.EuropeScreen_DIRTY_BIT)):
							CyInterface().setDirty(InterfaceDirtyBits.EuropeScreen_DIRTY_BIT, False)
						self.drawContents()
					self.hideDialogBox(0)

				elif (inputClass.getData1() == self.PREVIEW_MODE) :
					if (sdToolKit.sdGetVal('komaScreens', player.getName(), 'PreviewMode') == 0):
						sdToolKit.sdSetVal('komaScreens', player.getName(), 'PreviewMode', 1)
						szTexture = "INTERFACE_DOMESTIC_ADVISOR"
					else:
						sdToolKit.sdSetVal('komaScreens', player.getName(), 'PreviewMode', 0)
						szTexture = "INTERFACE_FOREIGN_ADVISOR"
					screen.setImageButtonAt("PreviewMode", "DialogMainPanel", ArtFileMgr.getInterfaceArtInfo(szTexture).getPath(), 206, 200, 40, 40, WidgetTypes.WIDGET_GENERAL, self.PREVIEW_MODE, sdToolKit.sdGetVal('komaScreens', player.getName(), 'PreviewMode'))
				
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON) :
			if (inputClass.getFunctionName() == "DialogSelection") :
				screen = self.getScreen()
				index = inputClass.getID()

				if index == 0:			#Sail east info
					screen.addDrawControl("DialogMap", "Art/Interface/Screens/Europe/DialogMapAtlantic.dds", self.XResolution / 2 - 217, self.YResolution / 6 + 31, 192, 192, WidgetTypes.WIDGET_GENERAL, self.SAIL_EXEC, 0)
					for i in range(3):
						screen.moveBackward("DialogMap")
					screen.hide("DialogLabel")
					screen.setLabelAt("SailToLabel", "DialogMainPanel", localText.getText("TXT_KEY_EU_SAIL_EAST", ()), CvUtil.FONT_CENTER_JUSTIFY, 136, 45, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				elif index == 1:		#Sail west info
					screen.addDrawControl("DialogMap", "Art/Interface/Screens/Europe/DialogMapPacific.dds", self.XResolution / 2 - 217, self.YResolution / 6 + 31, 192, 192, WidgetTypes.WIDGET_GENERAL, self.SAIL_EXEC, 1)
					for i in range(3):
						screen.moveBackward("DialogMap")
					screen.hide("DialogLabel")
					screen.setLabelAt("SailToLabel", "DialogMainPanel", localText.getText("TXT_KEY_EU_SAIL_WEST", ()), CvUtil.FONT_CENTER_JUSTIFY, 136, 45, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				elif index >= 2:		#Sail to city info
					pTransport = player.getUnit(inputClass.getData2())
					self.getCityInfo(index, pTransport)

		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF) :
			if (inputClass.getFunctionName() == "DialogSelection"):
				screen.hide("DialogImage" + str(inputClass.getID()))
				screen.hide("ProductionView")
				screen.hide("DestinationInfoPanel")
				screen.hide("OldCityMap")
				screen.hide("ProductionInfo")
				screen.hide("SailToLabel")
				for iYield in self.YieldList :
					screen.show("EuropePrices" + str(iYield))
				screen.show("DialogLabel")
				screen.show("DialogMap")
				screen.addDrawControl("DialogMap", "Art/Interface/Screens/Europe/DialogMapAmerica.dds", self.XResolution / 2 - 217, self.YResolution / 6 + 31, 192, 192, WidgetTypes.WIDGET_GENERAL, self.SAIL_EXEC, 0)
				for i in range(3):
					screen.moveBackward("DialogMap")

		return 0

	def update(self, fDelta):
		if (CyInterface().isDirty(InterfaceDirtyBits.EuropeScreen_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.EuropeScreen_DIRTY_BIT, False)
			self.drawContents()

	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList
		player = gc.getPlayer(gc.getGame().getActivePlayer())
	
		if eWidgetType == WidgetTypes.WIDGET_GENERAL:
			if iData1 == self.SAIL_TO_NEW_WORLD:
				return localText.getText("TXT_KEY_SAIL", ())
			elif iData1 == self.SELL_ALL:
				return localText.getText("TXT_KEY_SELL_ALL", ())
			elif iData1 == self.LOAD_ALL:
				return localText.getText("TXT_KEY_LOAD_ALL_EUROPE", ())
			elif iData1 == self.BUY_UNIT_BUTTON_ID:
				return localText.getText("TXT_KEY_PURCHASE_EUROPE", ())
			elif iData1 == self.TREASURY_ID:
				return localText.getText("TXT_KEY_ECON_GOLD_RESERVE" , ())
			elif iData1 == self.HELP_CROSS_RATE:
				return localText.getText("TXT_KEY_YIELD_RATE", (player.getYieldRate(YieldTypes.YIELD_CROSSES), gc.getYieldInfo(YieldTypes.YIELD_CROSSES).getChar()))
			elif iData1 == self.TRAVEL_INFO or iData1 == self.RECALL:
				return self.cargoMessage(iData2)
			elif iData1 == self.TRADE_LOG:
				return localText.getText("TXT_KEY_EU_VERSION", (self.szVersion, ()))
			#elif iData1 == self.SELL_SHIP:
			#	return localText.getText("TXT_KEY_EU_SELL_SHORT", (player.getUnit(iData2).getName(), self.getShipSellPrice(iData2)))
			elif iData1 == self.PREVIEW_MODE:
				return localText.getText("TXT_KEY_EU_PREVIEW_MODE", ())
				
		return u""
	
	def dialogBox(self, iUnit, dialogHeader, textMessage, callButton):
		screen = self.getScreen()
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		transport = player.getUnit(iUnit)
	
		screen.addPanel ("DestinationInfoPanel", u"", u"", True, False, 0, 0, self.XResolution, self.YResolution, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setImageButton("DialogExitLayer", "", 0, 50, self.XResolution, self.YResolution - 50, WidgetTypes.WIDGET_GENERAL, callButton, -1)
		screen.addPanel ("DialogMainPanel", u"", u"", True, False, self.XResolution / 2 - 256 , self.YResolution / 6, 512, 256, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addDrawControl("DialogMainPanel", "Art/Interface/Screens/Europe/DialogBox.dds", self.XResolution / 2 - 256, self.YResolution / 6, 512, 256, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setLabelAt("DialogLabel", "DialogMainPanel", u"%s" % dialogHeader, CvUtil.FONT_CENTER_JUSTIFY, 136, 45, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel ("DialogBodyPanel", u"", u"", True, False, self.XResolution / 2, self.YResolution / 6 + 32, 225, 113, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)

		#GoTo Mode
		if callButton == self.SAIL_EXEC:
			if self.EuropePlotList == []:
				self.getPlotLists(transport)

			screen.addPanel ("DialogMap", u"", u"", True, False, self.XResolution / 2 - 217, self.YResolution / 6 + 31, 192, 192, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addDrawControl("DialogMap", "Art/Interface/Screens/Europe/DialogMapAmerica.dds", self.XResolution / 2 - 217, self.YResolution / 6 + 31, 192, 192, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.moveBackward("DialogMap")
			screen.moveBackward("DialogMap")
			
			if len(self.EuropePlotListEast) > 0:		#east button
				screen.setImageButtonAt("DialogSelection" + str(0), "DialogMainPanel", "", 135, 31, 96, 192, WidgetTypes.WIDGET_GENERAL, self.SAIL_EXEC, iUnit)
			if len(self.EuropePlotListWest) > 0:		#west button
				screen.setImageButtonAt("DialogSelection" + str(1), "DialogMainPanel", "", 39, 31, 96, 192, WidgetTypes.WIDGET_GENERAL, self.SAIL_EXEC, iUnit)
			if len(self.CityPlotList) > 0:				#city buttons
				iPreviewMode = sdToolKit.sdGetVal('komaScreens', player.getName(), 'PreviewMode')
				if iPreviewMode:
					szTexture = "INTERFACE_DOMESTIC_ADVISOR"
				else:
					szTexture = "INTERFACE_FOREIGN_ADVISOR"
				screen.setImageButtonAt("PreviewMode", "DialogMainPanel", ArtFileMgr.getInterfaceArtInfo(szTexture).getPath(), 206, 200, 40, 40, WidgetTypes.WIDGET_GENERAL, self.PREVIEW_MODE, iPreviewMode)

				screen.addScrollPanel("CityListPanel", u"", self.XResolution / 2 - 14, self.YResolution / 6 + 23, 232, 187, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				for i in range(len(self.CityPlotList)):
					pCity = self.CityPlotList[i][0]
					screen.setTextAt("DialogSelection" + str(i + 2), "CityListPanel", u"<font=3>" + localText.getText("%s1", (pCity.getName(), ())) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, 116, 10 + 21 * i, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, self.SAIL_EXEC, iUnit)

		#'ship selling' dialog
		else:
			screen.addPanel ("DialogMap", u"", u"", True, False, self.XResolution / 2 - 217, self.YResolution / 6 + 31, 192, 192, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addDrawControl("DialogMap", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_BG_LEFT").getPath(), self.XResolution / 2 - 217, self.YResolution / 6 + 31, 192, 192, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			for i in range(4):
				screen.moveBackward("DialogMap")

			screen.attachMultilineText ("DialogBodyPanel", "DialogBodyText", u"%s" % textMessage, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			for i in range(2) :
				screen.addDDSGFCAt("DialogButtonBackground" + str(i), "DialogMainPanel", ArtFileMgr.getInterfaceArtInfo("SCREEN_DATE_BOX").getPath(), 250, 128 + i * 36, 232, 66, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
		
			screen.setTextAt("DialogAccept", "DialogMainPanel", u"<font=3>" + localText.getText("TXT_KEY_EU_DIALOG_ACCEPT", ()) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, 368, 160, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, callButton, iUnit)
			screen.setTextAt("DialogDecline", "DialogMainPanel", u"<font=3>" + localText.getText("TXT_KEY_EU_DIALOG_DECLINE", ()) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, 368, 196, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, callButton, -1 )
	
	def hideDialogBox (self, index):
		screen = self.getScreen()
	
		screen.hide("DialogMainPanel")
		screen.hide("DialogExitLayer")
		screen.hide("DialogMap")
		screen.hide("DialogBodyPanel")
		screen.hide("CityListPanel")
		screen.hide("ProductionView")
		screen.hide("ProductionInfo")
		screen.hide("DialogImage" + str(index))
		screen.hide("DestinationInfoPanel")
	
	def getCityInfo(self, index, pTransport) :
		screen = self.getScreen()
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		pCity = self.CityPlotList[index - 2][0]
		iX = 0
		iBoxWidth = self.XResolution / len(self.YieldList)
		iBoxHeight = self.YResolution * 2 / 21
		iYieldSpace = (self.XResolution - (iBoxWidth * 6 / 7 * len(self.YieldList))) / 2
	
		screen.show("DestinationInfoPanel")

		#get yield stored in city warehouse
		for iYield in self.YieldList :
			screen.hide("EuropePrices" + str(iYield))

		for iYield in self.YieldList :
			szYieldColor = u"<color=160,160,160>"
			szNumStorage = u"%d</color></font>" % (pCity.getYieldStored(iYield))

			if (pCity.getYieldStored(iYield) > 0):
				szYieldColor = u"<color=0,255,0>"

				if (pCity.getMaxYieldCapacity() * 2 / 3 <= pCity.getYieldStored(iYield)) and not iYield == 0:
					szYieldColor = u"<color=255,255,0>"
				if (pCity.getMaxYieldCapacity() * 5 / 6 <= pCity.getYieldStored(iYield)) and not iYield == 0:
					szYieldColor = u"<color=255,0,0>"
	
			screen.setLabelAt("CityWarehouse" + str(iYield), "DestinationInfoPanel", u"<font=3>" + szYieldColor + szNumStorage, CvUtil.FONT_CENTER_JUSTIFY, iX + self.XResolution / 38 + iYieldSpace, self.YResolution - self.YResolution * 3 / 46 - 18, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

			iX += iBoxWidth * 6 / 7
	
		screen.setLabelAt("CityWarehouseLabel", "DestinationInfoPanel", u"<font=4>" + localText.getText("TXT_KEY_EU_WAREHOUSE_INFO", (pCity.getName(), pCity.getMaxYieldCapacity())) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 30, self.YResolution - (self.YResolution * 2 / 21) * 6 / 7 - 17 - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1) 
	
		#city preview	
		iPreviewMode = sdToolKit.sdGetVal('komaScreens', player.getName(), 'PreviewMode')

		if iPreviewMode:
			screen.hide("DialogMap")
		
			if not ("DialogImage" + str(index)) in self.PreviewPlotList:
				screen.addPlotGraphicGFC("DialogImage" + str(index), self.XResolution / 2 - 217, self.YResolution / 6 + 31, 192, 192, pCity.plot(), 350, true, WidgetTypes.WIDGET_GENERAL, -1, -1)
				for i in range(4):
					screen.moveBackward("DialogImage" + str(index))
			
				self.PreviewPlotList.append("DialogImage" + str(index))
			else:
				screen.show("DialogImage" + str(index))
		else:
			screen.addDrawControl("DialogMap", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_BG_LEFT").getPath(), self.XResolution / 2 - 217, self.YResolution / 6 + 31, 192, 192, WidgetTypes.WIDGET_GENERAL, self.SAIL_EXEC, -1)
			for i in range(4):
				screen.moveBackward("DialogMap")

			screen.addDDSGFCAt("OldCityMap", "DialogMap", "Art/Interface/Screens/Europe/DialogMapCity.dds", 0, 28, 192, 130, WidgetTypes.WIDGET_GENERAL, -1, -1, False)		

	def getPlotLists (self, unit) :
		player = gc.getPlayer(gc.getGame().getActivePlayer())
	
		#Europe plot list
		self.EuropePlotListEast = []
		self.EuropePlotListWest = []
	
		for i in range(CyMap().numPlots()):
			pLoopPlot = CyMap().plotByIndex(i)
			if CyMap().isPlot(pLoopPlot.getX(), pLoopPlot.getY()):
				if pLoopPlot.isRevealed(player.getTeam(), false):
					if pLoopPlot.isEurope():
						if pLoopPlot.getX() >= CyMap().getGridWidth() / 2:
							self.EuropePlotListEast.append(pLoopPlot)
						else:
							self.EuropePlotListWest.append(pLoopPlot)

		pCenterPlot = self.getCenterPlot()
		
		self.pPlotEast = self.getNextOceanPlot(pCenterPlot, self.EuropePlotListEast)
		self.pPlotWest = self.getNextOceanPlot(pCenterPlot, self.EuropePlotListWest)
		
		self.EuropePlotList = self.EuropePlotListEast + self.EuropePlotListWest
	
		#City list
		self.CityPlotList = []
		plotEast = self.pPlotEast
		plotWest = self.pPlotWest
		
		if plotEast == None:
			plotEast = self.getNextOceanPlot(pCenterPlot, self.EuropePlotList)
		if plotWest == None:
			plotWest = self.getNextOceanPlot(pCenterPlot, self.EuropePlotList)
			
		(city, iter) = player.firstCity(false)

		while (city):
			if city.isCoastal(1) and not city.waterArea().isLake():
				if unit.getGroup().generatePath(plotEast, city.plot(), 0, false, None):
					self.CityPlotList.append([city, None])
				elif unit.getGroup().generatePath(plotWest, city.plot(), 0, false, None):
					self.CityPlotList.append([city, None])
			(city, iter) = player.nextCity(iter, false)
	
	def getCenterPlot (self):
		player = gc.getPlayer(gc.getGame().getActivePlayer())
	
		pCenterPlot = player.getStartingPlot()
		iCenterX, iCenterY, iCityCount = 0, 0, 0
	
		(city, iter) = player.firstCity(false)
		while (city):
			iCenterX += city.plot().getX()
			iCenterY += city.plot().getY()
			iCityCount += 1
			(city, iter) = player.nextCity(iter, false)
	
		if iCityCount > 0:
			iCenterX /= iCityCount
			iCenterY /= iCityCount
			pCenterPlot = CyMap().plot(iCenterX, iCenterY)
	
		return pCenterPlot
	
	def getBestCityPlot (self, pCityPlot) :

		pBestPlot = self.getNextOceanPlot(pCityPlot, self.EuropePlotList)
		iPath = self.getPathDistance(pBestPlot, pCityPlot)
		
		if iPath <= CyMap().getGridWidth() / 2:
			return pBestPlot
	
		if len(self.EuropePlotListEast) > 0:
			iPathEast = self.getPathDistance(self.pPlotEast, pCityPlot)
			if iPathEast < iPath:
				iPath = iPathEast
				pBestPlot = self.pPlotEast
	
		if len(self.EuropePlotListWest) > 0:
			iPathWest = self.getPathDistance(self.pPlotWest, pCityPlot)
			if iPathWest < iPath:
				pBestPlot = self.pPlotWest
	
		return pBestPlot

	def getNextOceanPlot (self, pPlot, EuropePlotSide) :

		pBestPlot = None
		iBestDistance = 1000

		for pLoopPlot in EuropePlotSide:
			iDistance = plotDistance(pLoopPlot.getX(), pLoopPlot.getY(), pPlot.getX(), pPlot.getY())
			if iDistance < iBestDistance:
				iBestDistance = iDistance
				pBestPlot = pLoopPlot
	
		return pBestPlot
	
	def getPathDistance (self, pPlot, pCityPlot):
	
		iXCity = pCityPlot.getX()
		iYCity = pCityPlot.getY()
		bestPathDistance = 1000
	
		for i in range(3):
			iX = iXCity - 1
			iY = iYCity + i - 1

			for j in range(3):
				pPathPlot = CyMap().plot(iX, iY)
				if pPathPlot.isWater():
					iPathDistance = CyMap().calculatePathDistance(pPlot, pPathPlot)
					if not iPathDistance == -1:
						if iPathDistance < bestPathDistance:
							bestPathDistance = iPathDistance
				iX += 1	
	
		return bestPathDistance
	
	def cargoMessage(self, iUnit):
		#cargo info
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		transport = player.getUnit(iUnit)

		if (transport.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE):
			currentCargoDictionary = self.OutboundCargoDictionary
		else:
			currentCargoDictionary = self.InboundCargoDictionary		

		szText = localText.getText("[COLOR_HIGHLIGHT_TEXT]%s1[COLOR_REVERT][NEWLINE]", (transport.getName(),""))
		szText += localText.getText("TXT_KEY_ARRIVALS_IN", ("",transport.getUnitTravelTimer()))
	
		for iCargoUnit in currentCargoDictionary:
			if iCargoUnit == transport.getID():
				for cargo in currentCargoDictionary[iCargoUnit]:
					szCargoName = gc.getUnitInfo(cargo).getDescription()
					if currentCargoDictionary[iCargoUnit][cargo] > 1:
						szCargoName = gc.getUnitInfo(cargo).getDescriptionForm(1)

					szText += localText.getText("[NEWLINE][COLOR_BUILDING_TEXT][ICON_BULLET]", ())
					szText += u"<font=2>%d %s</font>" % (currentCargoDictionary[iCargoUnit][cargo], szCargoName)
					szText += localText.getText("[COLOR_REVERT]", ())
		
		szText += self.travelMessage(iUnit)

		return szText
	
	def travelMessage(self, iUnit):
		#destination info
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		plot = player.getUnit(iUnit).plot()
		nextCityName = localText.getText("%s1", (CyMap().findCity (plot.getX(), plot.getY(), player.getID(), -1, true, true, -1, -1, plot.getPlotCity()).getName(), ()))
	
		if (plot.getX() >= CyMap().getGridWidth() / 2):
			direction = localText.getText("TXT_KEY_EU_SAIL_EAST", ())
		else:
			direction = localText.getText("TXT_KEY_EU_SAIL_WEST", ())
		if (nextCityName == ""):
			nextCity = u""
		elif player.getUnit(iUnit).getGroup().getLengthMissionQueue() >= 1 :
			nextCityName = localText.getText("%s1", (player.getUnit(iUnit).getGroup().lastMissionPlot().getPlotCity().getName(), ()))
			nextCity = localText.getText("TXT_KEY_EU_TO_CITY", (nextCityName, ()))
		else:
			nextCity = localText.getText("TXT_KEY_EU_NEAR_CITY", (nextCityName, ()))
			direction = localText.getText("[COLOR_YELLOW]", ()) + direction + localText.getText("[COLOR_REVERT]", ())
		if self.iPlotDebug:
			direction += u" (%d, %d)" % (plot.getX(), plot.getY())
	
		return localText.getText("TXT_KEY_EU_ROUTE", (direction, nextCity))
	
	def playSound(self, SoundName):
		self.iSoundID = CyAudioGame().Play2DSound(SoundName)
		return self.iSoundID
	
	def makeSound(self, SoundType):
		screen = self.getScreen()
		iCivilization = gc.getPlayer(gc.getGame().getActivePlayer()).getCivilizationType()
		
		if SoundType == "initSound":
			if (self.iSoundID != 0):
				CyAudioGame().Destroy2DSound(self.iSoundID)

			if self.iThisWinter:
				unitsVolume = 1.0
				screen.setSoundId(self.playSound("AS2D_SS_TUNDRALOOP"))
			else:
				unitsVolume = 0.75
				screen.setSoundId(self.playSound("AS2D_SS_COASTLOOP"))

			CyAudioGame().Set2DSoundVolume(self.iSoundID, unitsVolume)

		elif SoundType == "unitsSelectSound":
			iSelectionSound = gc.getCivilizationInfo(iCivilization).getSelectionSoundScriptId()
			screen.setSoundId(CyAudioGame().Play3DSoundWithId(iSelectionSound, -1, -1, -1))
	
		elif SoundType == "unitsOrderSound":
			iActionSound = gc.getCivilizationInfo(iCivilization).getActionSoundScriptId()
			screen.setSoundId(CyAudioGame().Play3DSoundWithId(iActionSound, -1, -1, -1))
	
	def getShipSellPrice(self, iUnit):
		if not iUnit == -1:
			player = gc.getPlayer(gc.getGame().getActivePlayer())
			iTrainPercent = gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getTrainPercent()
			iSellPrice = self.iSellShip * gc.getUnitInfo(player.getUnit(iUnit).getUnitType()).getEuropeCost() * iTrainPercent / 1200
			iSellPrice -= iSellPrice * player.getTaxRate() / 100

			return iSellPrice
		return 0
	
	def getMaxTravelTimer(self, transportPlot):
		player = gc.getPlayer(gc.getGame().getActivePlayer())
	
		if gc.getCivilizationInfo(player.getCivilizationType()).isFromWest():
			iMaxTravelTimer = (gc.getEuropeInfo(transportPlot.getEurope()).getWestTripLength() * gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getGrowthPercent()) / 100
		else:
			iMaxTravelTimer = (gc.getEuropeInfo(transportPlot.getEurope()).getTripLength() * gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getGrowthPercent()) / 100
	
		for i in range(gc.getNumTraitInfos()):
			if player.hasTrait(i):
				if (gc.getTraitInfo(i).getEuropeTravelTimeModifier() != 0):
					iMaxTravelTimer *= 100 + gc.getTraitInfo(i).getEuropeTravelTimeModifier()
					iMaxTravelTimer /= 100
	
		return iMaxTravelTimer



