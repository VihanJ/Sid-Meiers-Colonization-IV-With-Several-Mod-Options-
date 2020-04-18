## DoaNE
## Copyright M07 2010

##########################################################################################################
########## Europe Screen 1: Ships management screen ######################################################
##########################################################################################################

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvEuropeC1Screen:

	def __init__(self):
		self.WIDGET_ID = "EuropeC1ScreenWidget"
		self.TABLE_ID = "EuropeC1ScreenTable"
		self.nWidgetCount = 0
		
		self.TREASURY_ID = 1
		self.ICON_RESUPPLY = 2
		self.ICON_REPAIR = 3
		self.ICON_UNLOAD_CREW = 4
		self.ICON_LOAD_CREW = 5
		self.ICON_RENAME_UNIT = 6
		self.ICON_SELL = 7
		self.ICON_PRIVATEER = 8
		self.ICON_ESCORT = 9
		self.ICON_SHADOW = 10
		self.ICON_STOP_REPAIR = 11
		self.REMOVE_SELL_SHIP_LIST = 12
		self.CHANGE_SELL_SHIP_PRICE = 13
		self.ICON_PURCHASE_BID = 14
		self.ICON_FLECHE = 15
		self.HIDE_MARKET_PRICE = 16
		self.EUROPE_1 = 17
		self.COMMAND_PROMOTE = 18
		
		self.selectedPlayerList = []
		self.EuropeUnitsList = []
		
	def getScreen(self):
		return CyGInterfaceScreen("europeC1Screen", CvScreenEnums.EUROPE_C1_SCREEN)

	def interfaceScreen(self):
	
		if ( CyGame().isPitbossHost() ):
			return

		if gc.getPlayer(gc.getGame().getActivePlayer()).getParent() == PlayerTypes.NO_PLAYER:
			return
	
		screen = self.getScreen()
		if screen.isActive():
			return
			
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		
		self.Y_TITLE = 4
		self.I_SELECTED_SHIP = -1
		self.calculateSizesAndPositions()
		
		self.EuropeUnitsList = []
		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		self.pPlayer = pPlayer
		
		self.initEuropeShipsList()

		# Set the background and exit button, and show the screen
		screen.setDimensions(0, 0, self.XResolution, self.YResolution)
		screen.showWindowBackground(False)
		
		screen.addDDSGFC("EuropeScreenUp", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BANDEAU_MARRON").getPath(), 0, 0, self.XResolution, 40, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("EuropeScreenDown", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BANDEAU_MARRON").getPath(), 0, self.YResolution - 86, self.XResolution, 86, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addDDSGFC("EuropeScreenBackground", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BACKGROUND_SHIP").getPath(), 0, 40, self.XResolution, self.YResolution - 86, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("TopPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TITLE").getPath(), 0, 0, self.XResolution, 55, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Header...
		screen.setLabel("EuropeScreenWidgetHeader", "Background", u"<font=4b>" + localText.getText("TXT_KEY_EUROPE_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.XResolution / 2, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Icon Ship
		#Start
		screen.addDDSGFC("EuropeScreenIconShip", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_PANCARTES_ICON_SHIP").getPath(), self.X_POS_ICON_PANCARTE, self.Y_POS_ICON_PANCARTE, self.X_SIZE_ICON_PANCARTE, self.Y_SIZE_ICON_PANCARTE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Equipages disponibles
		screen.addDDSGFC("EuropeScreenCrewDockHeader", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), 5, self.YResolution*5/10 - 10, self.XResolution/3 , 35, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("EuropeScreenCrewDock", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), 5, self.YResolution*5/10 + 30, self.XResolution/3,  self.CARGO_ICON_SIZE * 2 + 15, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addScrollPanel("DockList", u"", 15, self.YResolution*5/10 + 28, self.XResolution/3 - 15,  self.CARGO_ICON_SIZE * 1 + 30, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_DOCK, -1, -1 )
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_AVAILABLE_CREWS", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setLabel("EuropeScreenDockText", "background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.XResolution/6, self.YResolution*5/10, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		#infos tactique
		screen.addDDSGFC("EuropeScreeninfosTactiqueHeaderImage", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_INFO_TACT_HEAD, self.Y_POS_INFO_TACT_HEAD, self.X_SIZE_INFO_TACT_HEAD, self.Y_SIZE_INFO_TACT_HEAD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("EuropeScreeninfosTactiqueImage", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_INFO_TACT_HEAD, self.YResolution*3/20, self.X_SIZE_INFO_TACT_HEAD, self.YResolution*5/24+5, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setLabel("EuropeScreenInfosTactiqueText", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_INFO_TACT_HEAD + self.X_SIZE_INFO_TACT_HEAD/2, self.Y_POS_INFO_TACT_HEAD + self.Y_SIZE_INFO_TACT_HEAD/4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Recrutement Equipages
		screen.addDDSGFC("EuropeScreenCrewRecruitmentHeader", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), 5, self.YResolution*7/10 - 10, self.XResolution/3 , 35, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("EuropeScreenCrewRecruitment", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), 5, self.YResolution*7/10 + 30, self.XResolution/3,  self.CARGO_ICON_SIZE * 2 + 15, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addScrollPanel("DockList1", u"", 15, self.YResolution*7/10 + 28, self.XResolution/3 - 15,  self.CARGO_ICON_SIZE * 1 + 30, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_RECRUIT_CREW, -1, pPlayer.getID() )
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_CREWS_RECRUITMENT", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setLabel("EuropeScreenRecruitmentText", "background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.XResolution/6, self.YResolution*7/10, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		#Trade Ship
		
		#Trade Text
		screen.addDDSGFC("EuropeScreenShipTradeHeaderImage", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_TRADE_SHIP_HEAD, self.Y_POS_TRADE_SHIP_HEAD, self.X_SIZE_TRADE_SHIP_HEAD, self.Y_SIZE_TRADE_SHIP_HEAD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_TRADE_SHIP", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setLabel("EuropeScreenShipTradeText", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TRADE_SHIP_HEAD + self.X_SIZE_TRADE_SHIP_HEAD/2, self.Y_POS_TRADE_SHIP_HEAD + self.Y_SIZE_TRADE_SHIP_HEAD/4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		#Trade Image de fond
		screen.addDDSGFC("EuropeScreenShipTradeBox", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_BOX").getPath(), self.X_POS_TRADE_SHIP_PICT, self.Y_POS_TRADE_SHIP_PICT, self.X_SIZE_TRADE_SHIP_PICT, self.Y_SIZE_TRADE_SHIP_PICT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		#Trade Buying Used Ship Texte
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_TITLE_BUYING_USED", ()).upper(), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
		screen.setLabel("EuropeScreenBuyingUsedText", "background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TRADE_TEXT1, self.Y_POS_TRADE_TEXTS, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		#Trade Buying new Ship Texte
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_TITLE_BUYING_NEW_SHIPS", ()).upper(), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
		screen.setLabel("EuropeScreenBuyingNewText", "background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TRADE_TEXT2, self.Y_POS_TRADE_TEXTS, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		#Trade Sell Ship Texte
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_TITLE_SELL_SHIP_PRICE", ()).upper(), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
		screen.setLabel("EuropeScreenSellShipText", "background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TRADE_TEXT3, self.Y_POS_TRADE_TEXTS, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setImageButton("EuropeScreenIconFleche", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_FLECHE").getPath(), self.X_POS_TRADE_TEXT3 + 55, self.Y_POS_TRADE_TEXTS, 25, 20,  WidgetTypes.WIDGET_GENERAL, self.ICON_FLECHE, -1)
		
		
		self.drawTable()
		# draw the contents
		self.drawTabs()
		self.setTab(1, True)		
		self.drawContents()
		
	def drawTabs(self):

		screen = self.getScreen()

		Tabs = [localText.getObjectText("TXT_KEY_MAIN_MENU_EUROPE_0", 0), localText.getObjectText("TXT_KEY_MAIN_MENU_EUROPE_1", 0), localText.getObjectText("TXT_KEY_MAIN_MENU_EUROPE_2", 0), localText.getObjectText("TXT_KEY_IMMIGRATION_TITLE", 0)]
		Tabs1 = [gc.getControlInfo(ControlTypes.CONTROL_EUROPE_SCREEN).getActionInfoIndex(), gc.getControlInfo(ControlTypes.CONTROL_EUROPE_C1_SCREEN).getActionInfoIndex(), gc.getControlInfo(ControlTypes.CONTROL_EUROPE_C2_SCREEN).getActionInfoIndex(), gc.getControlInfo(ControlTypes.CONTROL_EUROPE_C3_SCREEN).getActionInfoIndex()]
		NumTabs = len(Tabs)
		TabWidth = self.W_SCREEN / (NumTabs + 1)

		for iTab in range(NumTabs):
			OnTabName = "OnTab" + str(iTab)
			EdgeWidth = 25
			BottomPanelHight = 55
			screen.addPanel(OnTabName + "Left", "", "", False, False, TabWidth * iTab, self.H_SCREEN - BottomPanelHight, EdgeWidth, BottomPanelHight, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addPanel(OnTabName + "Center", "", "", False, False, (TabWidth * iTab) + EdgeWidth, self.H_SCREEN - BottomPanelHight, TabWidth - (EdgeWidth * 2), BottomPanelHight, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addPanel(OnTabName + "Right", "", "", False, False, (TabWidth * iTab) + TabWidth - EdgeWidth, self.H_SCREEN - BottomPanelHight, EdgeWidth, BottomPanelHight, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)

			screen.addDrawControl(OnTabName + "Left", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_START").getPath(), TabWidth * iTab, self.H_SCREEN - BottomPanelHight, EdgeWidth, BottomPanelHight, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDrawControl(OnTabName + "Center", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_ON").getPath(), (TabWidth * iTab) + EdgeWidth, self.H_SCREEN - BottomPanelHight, TabWidth - (EdgeWidth * 2), BottomPanelHight, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDrawControl(OnTabName + "Right", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_END").getPath(), (TabWidth * iTab) + TabWidth - EdgeWidth, self.H_SCREEN - BottomPanelHight, EdgeWidth, BottomPanelHight, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			TabText = Tabs[iTab]
			TabText = localText.changeTextColor(TabText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))

			screen.setTextAt("OnTabTitle" + str(iTab), OnTabName + "Center", u"<font=4>" + TabText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, 0 , 33, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.hide(OnTabName + "Left")
			screen.hide(OnTabName + "Center")
			screen.hide(OnTabName + "Right")

			OffTabName = "OffTab" + str(iTab)
			screen.addPanel(OffTabName, "", "", False, False, TabWidth * iTab, self.H_SCREEN - BottomPanelHight, TabWidth, BottomPanelHight, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, 1111, iTab)
			screen.addDrawControl(OffTabName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_OFF").getPath(), TabWidth * iTab, self.H_SCREEN - BottomPanelHight, TabWidth, BottomPanelHight, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setTextAt("OffTabTitle" + str(iTab), OffTabName, u"<font=4>" + TabText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, EdgeWidth , 33, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_ACTION, Tabs1[iTab], 2*iTab+1)

		screen.addPanel("ExitTab", "", "", False, False, TabWidth * NumTabs, self.H_SCREEN - BottomPanelHight, TabWidth, BottomPanelHight, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addDrawControl("ExitTab", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_OFF").getPath(), TabWidth * NumTabs, self.H_SCREEN - BottomPanelHight, TabWidth, BottomPanelHight, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setTextAt("ExitTabTitle", "ExitTab", u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, TabWidth - 30 , BottomPanelHight - 18, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)
		
	def setTab(self, iTab, State):
		screen = self.getScreen()
		OnTabName = "OnTab" + str(iTab)

		if (State):
			screen.show(OnTabName + "Left")
			screen.show(OnTabName + "Center")
			screen.show(OnTabName + "Right")
			screen.hide("OffTab" + str(iTab))
		else:
			screen.hide(OnTabName + "Left")
			screen.hide(OnTabName + "Center")
			screen.hide(OnTabName + "Right")
			screen.show("OffTab" + str(iTab))
			
	def drawContents(self):
	
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		playerEurope = gc.getPlayer(player.getParent())

		self.deleteAllWidgets()

		screen = self.getScreen()

		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_TREASURY", (player.getGold(), )).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.W_TEXT_MARGIN, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.TREASURY_ID, -1 )
		
		# Units waiting on Docks
		XLocation = 0
		YLocation = 0

		iSailors = 0
		for i in range(player.getNumEuropeUnits()):
			loopUnit = player.getEuropeUnit(i)
			if loopUnit.getProfession() != -1:
				if loopUnit.getProfession() == ProfessionTypes.PROFESSION_SAILOR:
					screen.addDragableButtonAt("DockList", self.getNextWidgetName(), loopUnit.getFullLengthIcon(), "", XLocation, YLocation, self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE * 2, WidgetTypes.WIDGET_ONLY_INFO_UNIT, loopUnit.getID(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
					if loopUnit.getCrewFormationTurn() > 0:
						screen.setImageButtonAt(self.getNextWidgetName(), "DockList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICONE_FORMATION_NAVALE_BASIQUE").getPath(), XLocation + self.CARGO_ICON_SIZE*3/5, YLocation, 20, 20, WidgetTypes.WIDGET_DOCK, loopUnit.getID(), player.getID())
					if ((iSailors + 1) % 6) == 0:
						XLocation = 0
						YLocation += (self.CARGO_ICON_SIZE * 2)
					else:
						XLocation += self.CARGO_ICON_SIZE
					iSailors = iSailors + 1
		XLocation = 0
		YLocation = 0

		iCountSailor = 0
		(tempUnit, iter) = player.firstTempUnit() #Iterate all temp units
		while (tempUnit):
			if tempUnit.getProfession() == ProfessionTypes.PROFESSION_SAILOR:
				screen.setImageButtonAt(self.getNextWidgetName(), "DockList1", tempUnit.getFullLengthIcon(), XLocation, YLocation, self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE * 2, WidgetTypes.WIDGET_RECRUIT_CREW, tempUnit.getID(), player.getID())
				if tempUnit.requestTraining():
					screen.setImageButtonAt(self.getNextWidgetName(), "DockList1", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICONE_FORMATION_NAVALE_BASIQUE").getPath(), XLocation + self.CARGO_ICON_SIZE*3/5, YLocation, 20, 20, WidgetTypes.WIDGET_RECRUIT_CREW, tempUnit.getID(), player.getID())
				if ((iCountSailor + 1) % 6) == 0:
					XLocation = 0
					YLocation += (self.CARGO_ICON_SIZE * 2)
				else:
					XLocation += self.CARGO_ICON_SIZE
				iCountSailor = iCountSailor + 1
			(tempUnit, iter) = player.nextTempUnit(iter)
		(tempUnit, iter) = player.firstTempUnit() #Iterate all temp units
		iPos = 0
		while (tempUnit):
			if (gc.getUnitInfo(tempUnit.getUnitType()).isMechUnit() and gc.getUnitInfo(tempUnit.getUnitType()).getEuropeCost() > 0):
				screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_PURCHASE_BID").getPath(), self.X_POS_USED_SHIPS, self.Y_POS_SHIPS + iPos*self.Y_DECAL_SHIPS, 20, 20,  WidgetTypes.WIDGET_BUY_SHIP_USED, tempUnit.getID(), -1)
				szText = localText.changeTextColor(localText.getText("TXT_KEY_POPUP_SELL_UNIT_INFO2", (gc.getUnitInfo(tempUnit.getUnitType()).getTextKey(), )), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
				screen.setText(self.getNextWidgetName(), "background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_POS_USED_SHIPS + self.X_DECAL_TEXT_SHIPS, self.Y_POS_SHIPS + iPos*self.Y_DECAL_SHIPS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = localText.changeTextColor(localText.getText("TXT_KEY_POPUP_SELL_UNIT_INFO", (tempUnit.getPrice(), )), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
				screen.setText(self.getNextWidgetName(), "", u"<font=2>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_POS_USED_SHIPS + self.X_DECAL_PRICE_SHIPS, self.Y_POS_SHIPS + iPos*self.Y_DECAL_SHIPS, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iPos += 1
			(tempUnit, iter) = player.nextTempUnit(iter)
		
		(unit, iter) = player.firstUnit()
		iPos = 0
		while (unit):
			if (not unit.isCargo() and not unit.isDelayedDeath()):
				if (unit.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE):
					if unit.getShipSellPrice() != 0:
						if unit.isHasPurchaseBid():
							screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_PURCHASE_BID").getPath(), self.X_POS_SELL_SHIPS, self.Y_POS_SHIPS + iPos*self.Y_DECAL_SHIPS, 20, 20,  WidgetTypes.WIDGET_GENERAL, self.ICON_PURCHASE_BID, unit.getID())
						
						szText = localText.changeTextColor(localText.getText("TXT_KEY_POPUP_SELL_UNIT_INFO2", (gc.getUnitInfo(unit.getUnitType()).getTextKey(), )), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
						screen.setText(self.getNextWidgetName(), "background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_POS_SELL_SHIPS + self.X_DECAL_TEXT_SHIPS, self.Y_POS_SHIPS + iPos*self.Y_DECAL_SHIPS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.REMOVE_SELL_SHIP_LIST, unit.getID() )
						szText = localText.changeTextColor(localText.getText("TXT_KEY_POPUP_SELL_UNIT_INFO", (unit.getShipSellPrice(), )), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
						screen.setText(self.getNextWidgetName(), "", u"<font=2>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_POS_SELL_SHIPS + self.X_DECAL_PRICE_SHIPS, self.Y_POS_SHIPS + iPos*self.Y_DECAL_SHIPS, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, self.CHANGE_SELL_SHIP_PRICE, unit.getID() )
						iPos += 1
			(unit, iter) = player.nextUnit(iter)
		
		iPos = -1
		for iUnitClass in range(gc.getNumUnitClassInfos()):
			iUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iUnitClass)
			if iUnitType != UnitTypes.NO_UNIT:
				UnitInfo = gc.getUnitInfo(iUnitType)
				if player.canBuyEuropeNewShip(iUnitType):
					iPos +=1
					iGold = player.getEuropeUnitBuyPrice(iUnitType)
					iGold += iGold*playerEurope.getUnitMarketPrice(iUnitClass)/100
					if player.getUnitTurnRemaining(iUnitClass) > 0:
						screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_PURCHASE_BID").getPath(), self.X_POS_NEW_SHIPS, self.Y_POS_SHIPS + iPos*self.Y_DECAL_SHIPS, 20, 20,  WidgetTypes.WIDGET_GENERAL, -1, -1)
					szText = localText.changeTextColor(localText.getText("TXT_KEY_POPUP_SELL_UNIT_INFO2", (gc.getUnitInfo(iUnitType).getTextKey(), )), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
					screen.setText(self.getNextWidgetName(), "background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_POS_NEW_SHIPS + self.X_DECAL_TEXT_SHIPS, self.Y_POS_SHIPS + iPos*self.Y_DECAL_SHIPS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_BUY_NEW_SHIP, iUnitType, -1)
					szText = localText.changeTextColor(localText.getText("TXT_KEY_POPUP_SELL_UNIT_INFO", (iGold, )), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
					screen.setText(self.getNextWidgetName(), "", u"<font=2>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_POS_NEW_SHIPS + self.X_DECAL_PRICE_SHIPS, self.Y_POS_SHIPS + iPos*self.Y_DECAL_SHIPS, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		self.infosTactique()
		
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
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = 0

	# Will handle the input for this screen...
	def handleInput(self, inputClass):
		'Calls function mapped in EuropeScreenInputMap'
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			self.updateUnitSelected()
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):
				if (inputClass.getData1() == self.ICON_RESUPPLY 
				or inputClass.getData1() == self.ICON_REPAIR
				or inputClass.getData1() == self.ICON_STOP_REPAIR
				or inputClass.getData1() == self.ICON_LOAD_CREW
				or inputClass.getData1() == self.ICON_SELL
				or inputClass.getData1() == self.ICON_PRIVATEER
				or inputClass.getData1() == self.ICON_ESCORT
				or inputClass.getData1() == self.ICON_UNLOAD_CREW):
					self.iconProcess(inputClass.getData1())
				if inputClass.getData1() == self.REMOVE_SELL_SHIP_LIST:
					CyMessageControl().sendDoCommand(inputClass.getData2(), CommandTypes.COMMAND_STOP_SELL_SHIP, -1, -1, false) 
				if inputClass.getData1() == self.ICON_PURCHASE_BID:
					CyMessageControl().sendDoCommand(inputClass.getData2(), CommandTypes.COMMAND_PURCHASE_BID_SHIP, -1, -1, false) 
				if inputClass.getData1() == self.CHANGE_SELL_SHIP_PRICE:
					CyMessageControl().sendDoCommand(inputClass.getData2(), CommandTypes.COMMAND_CHANGE_SELL_SHIP_PRICE, -1, -1, false)
				if inputClass.getData1() == self.ICON_FLECHE:
					self.showMarketPrice()
				if inputClass.getData1() == self.HIDE_MARKET_PRICE:
					self.hideMarketPrice()
				if inputClass.getData1() == self.COMMAND_PROMOTE:
					self.promoteUnit(inputClass.getData2())
					
		return 0
	def promoteUnit(self, unitId):
		CyMessageControl().sendDoCommand(unitId, CommandTypes.COMMAND_PROMOTE, 1, -1, False)

	def updateUnitSelected(self):
		screen = self.getScreen()
		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		iRows = screen.getTableNumRows(self.TABLE_ID)
		if (not screen.isRowSelected(self.TABLE_ID, iRows)):
			bShipSelected = false
			for iRow in range(len(self.EuropeUnitsList)):
				if (screen.isRowSelected(self.TABLE_ID, iRow)):
					bShipSelected = true
					if self.I_SELECTED_SHIP != iRow:
						self.I_SELECTED_SHIP = iRow
			if not bShipSelected:
				if self.I_SELECTED_SHIP != -1:
					self.I_SELECTED_SHIP = -1
		self.fillTable(true)
		self.drawContents()
	def getUnitPriceMarket(self, iUnitClass):
		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		playerEurope = gc.getPlayer(pPlayer.getParent())
		iUnitType = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(iUnitClass)
		UnitInfo = gc.getUnitInfo(iUnitType)
		
		iGold = UnitInfo.getEuropeCost();
		iGold /= 2;
		iGold += iGold*playerEurope.getUnitMarketPrice(iUnitClass)/100;
		iGold -= iGold*pPlayer.getTaxRate()/100;
		
		return iGold
		
	def showMarketPrice(self):
		screen = self.getScreen()		
		
		iHauteur = self.YResolution/2 - 30
		iLargeur = self.XResolution/3 - 45
		iPositionY = self.YResolution/2 - 37
		iPositionX = 25
		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		
		screen.addDDSGFC("MarketPriceFond", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ZI").getPath(), iPositionX, iPositionY, iLargeur, iHauteur, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_ICON_FLECHE", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setLabel("MarketPriceHeader", "", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, iPositionX + iLargeur/2, iPositionY + 20, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iPos = -1
		for iUnitClass in range(gc.getNumUnitClassInfos()):
			iUnitType = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(iUnitClass)
			if iUnitType != UnitTypes.NO_UNIT:
				UnitInfo = gc.getUnitInfo(iUnitType)
				if UnitInfo.isMechUnit() and pPlayer.getEuropeUnitBuyPrice(iUnitType) > 0 and iUnitType != UnitTypes.UNIT_PRIVATEER:
					iPos +=1
					screen.setImageButton(self.getNextWidgetName(), pPlayer.getUnitButton(iUnitType), iPositionX + 20, iPositionY + 55 + iPos*40, 30, 30,  WidgetTypes.WIDGET_GENERAL, -1, -1)
					szText = localText.changeTextColor(localText.getText("TXT_KEY_POPUP_SELL_UNIT_INFO2", (UnitInfo.getTextKey(), )), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
					screen.setText(self.getNextWidgetName(), "", u"<font=2>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iPositionX + 70, iPositionY + 60 + iPos*40, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					szText = localText.changeTextColor(localText.getText("TXT_KEY_POPUP_SELL_UNIT_INFO", (self.getUnitPriceMarket(iUnitClass), )), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
					screen.setText(self.getNextWidgetName(), "", u"<font=2>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, iPositionX + iLargeur - 10, iPositionY + 60 + iPos*40, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText("MarketPriceExit", "", u"<font=3>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, iLargeur, iHauteur + iPositionY - 50, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.HIDE_MARKET_PRICE, -1 )
	
	def hideMarketPrice(self):
		screen = self.getScreen()		
		screen.hide("MarketPriceFond")
		screen.hide("MarketPriceHeader")
		screen.hide("MarketPriceExit")
		
		self.fillTable(true)
		self.drawContents()
		return
		
	def update(self, fDelta):
		screen = self.getScreen()		
		if (CyInterface().isDirty(InterfaceDirtyBits.EuropeC1Screen_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.EuropeC1Screen_DIRTY_BIT, False)
			screen.hide("MarketPriceFond")
			screen.hide("MarketPriceHeader")
			screen.hide("MarketPriceExit")
			self.fillTable(true)
			self.drawContents()			
		if (CyInterface().isDirty(InterfaceDirtyBits.EuropeC1Screen2_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.EuropeC1Screen2_DIRTY_BIT, False)
			self.drawContents()
			screen.hide("MarketPriceFond")
			screen.hide("MarketPriceHeader")
			screen.hide("MarketPriceExit")
			bInfoTactique = false
			iRows = screen.getTableNumRows(self.TABLE_ID)
			if (not screen.isRowSelected(self.TABLE_ID, iRows)):
				for iRow in range(len(self.EuropeUnitsList)):
					if (screen.isRowSelected(self.TABLE_ID, iRow)):
						bInfoTactique = true
				
			self.EuropeUnitsList = []
			iPlayer = CyGame().getActivePlayer()
			pPlayer = gc.getPlayer(iPlayer)
			
			(unit, iter) = pPlayer.firstUnit()
			while (unit):
				if (not unit.isCargo() and not unit.isDelayedDeath()):
					if (unit.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE):
						if unit.getShipSellPrice() == 0:
							self.EuropeUnitsList.append(unit)
				(unit, iter) = pPlayer.nextUnit(iter)
			self.drawTable()
			

	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList

		if eWidgetType == WidgetTypes.WIDGET_GENERAL:
			if  iData1 == self.TREASURY_ID:
				return localText.getText("TXT_KEY_ECON_GOLD_RESERVE", ())
			elif  iData1 == self.ICON_RESUPPLY:
				return localText.getText("TXT_KEY_EUROPE_ICON_RESUPPLY", ())
			elif  iData1 == self.ICON_REPAIR:
				return localText.getText("TXT_KEY_EUROPE_ICON_REPAIR", ())
			elif  iData1 == self.ICON_STOP_REPAIR:
				return localText.getText("TXT_KEY_EUROPE_ICON_STOP_REPAIR", ())
			elif  iData1 == self.ICON_UNLOAD_CREW:
				return localText.getText("TXT_KEY_EUROPE_ICON_UNLOAD_CREW", ())
			elif  iData1 == self.ICON_SELL:
				return localText.getText("TXT_KEY_EUROPE_ICON_SELL_SHIP", ())
			elif  iData1 == self.ICON_PRIVATEER:
				return localText.getText("TXT_KEY_EUROPE_ICON_PRIVATEER", ())
			elif  iData1 == self.ICON_ESCORT:
				return localText.getText("TXT_KEY_EUROPE_ICON_ESCORT", ())
			elif  iData1 == self.ICON_SHADOW:
				return localText.getText("TXT_KEY_EUROPE_ICON_SHADOW", ())
			elif  iData1 == self.ICON_LOAD_CREW:
				return localText.getText("TXT_KEY_EUROPE_ICON_LOAD_CREW", ())
			elif  iData1 == self.REMOVE_SELL_SHIP_LIST:
				return localText.getText("TXT_KEY_EUROPE_REMOVE_SELL_SHIP_LIST", ())
			elif  iData1 == self.CHANGE_SELL_SHIP_PRICE:
				return localText.getText("TXT_KEY_EUROPE_CHANGE_SELL_SHIP_PRICE", ())
			elif  iData1 == self.ICON_PURCHASE_BID:
				return localText.getText("TXT_KEY_EUROPE_ICON_PURCHASE_BID", ())
			elif  iData1 == self.ICON_FLECHE:
				return localText.getText("TXT_KEY_EUROPE_ICON_FLECHE", ())
			elif  iData1 == self.COMMAND_PROMOTE:
				return localText.getText("TXT_KEY_COMMAND_PROMOTION_HELP", ())
		return u""
	
	def getSelectUnit(self):
		i = 0
		for pLoopUnit in self.EuropeUnitsList:
			if self.I_SELECTED_SHIP == i:
				return pLoopUnit
			i = i + 1
		return None
	
	def drawTable(self):
		screen = self.getScreen()
		
		screen.addDDSGFC("EuropeScreenShipQuayImage", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_DOCK, self.Y_POS_DOCK, self.X_SIZE_DOCK, self.Y_SIZE_DOCK, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_SHIPS_QUAY", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setLabel("EuropeScreenShipQuayText", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_DOCK + self.X_SIZE_DOCK/2, self.Y_POS_DOCK + self.Y_SIZE_DOCK/4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.addDDSGFC("EuropeScreenShipQuayFond", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_DOCK, self.YResolution*3/20 - 2, self.X_SIZE_DOCK, self.YResolution*5/24+5 + 4, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addTableControlGFC(self.TABLE_ID, 3, 25, self.YResolution*3/20, self.XResolution/3 - 45, self.YResolution*5/24+5, false, false, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader(self.TABLE_ID, 0, u"", (self.XResolution/3 - 45)/6) # Total graph width is 430
		screen.setTableColumnHeader(self.TABLE_ID, 1, u"", (self.XResolution/3-45)*10/17)
		screen.setStyle(self.TABLE_ID, "Table_EmptyScroll_Style")
		self.fillTable(false)	
		screen.selectRow(self.TABLE_ID, 0, True)
		self.updateUnitSelected()
		
	def fillTable(self, bUdate):
		screen = self.getScreen()
		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		iRow = -1
		pSelectedUnit = self.getSelectUnit()
		
		for pLoopUnit in self.EuropeUnitsList:
			iRow += 1
			pLoopGroup = pLoopUnit.getGroup()
			if not bUdate:
				screen.appendTableRow(self.TABLE_ID)
				screen.setTableRowHeight(self.TABLE_ID, iRow, self.YResolution*5/96)
			
			iColumn = -1

			 # Assign/Unassign Button
			iColumn += 1
			screen.setTableText(self.TABLE_ID, iColumn, iRow, u"", pPlayer.getUnitButton(pLoopUnit.getUnitType()), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				
			# Transport Name
			iColumn += 1
			sText = pLoopUnit.getName()
			
			fRealForce = (float(pLoopUnit.baseCombatStr() * pLoopUnit.currHitPoints())) / (float(pLoopUnit.maxHitPoints()))
			iBaseForce = float(pLoopUnit.baseOriginCombatStr())
			if fRealForce != iBaseForce :
				sText = localText.changeTextColor(sText, gc.getInfoTypeForString("COLOR_RED"))
			else :
				iMaxAmmunition = gc.getUnitInfo(pLoopUnit.getUnitType()).getMaxMunition()
				if iMaxAmmunition != -1 :
					if pLoopUnit.getMunition() <= iMaxAmmunition/2 :
						sText = localText.changeTextColor(sText, gc.getInfoTypeForString("COLOR_RED"))
				
			if pSelectedUnit != None and bUdate:
				pGroup = pSelectedUnit.getGroup()
				if (pLoopGroup.getID() == pGroup.getID()):
					eColor = "COLOR_CYAN"
					if pGroup.getNumUnits() == 1:
						eColor = "COLOR_YELLOW"
					sText = localText.changeTextColor(sText, gc.getInfoTypeForString(eColor))
			
			screen.setTableText(self.TABLE_ID, iColumn, iRow, u"<font=3>" + sText + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
			iColumn += 1
			
			if not pLoopUnit.isInEuropeDrydock() and pLoopUnit.hasCrew():
				screen.setTableText(self.TABLE_ID, iColumn, iRow, u"", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_STATUT_UNIT_OPERATIVE").getPath(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			else :
				screen.setTableText(self.TABLE_ID, iColumn, iRow, u"", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_STATUT_UNIT_INOPERATIVE").getPath(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
		
		while iRow < 4 and not bUdate:
			iRow += 1
			screen.appendTableRow(self.TABLE_ID)
			screen.setTableRowHeight(self.TABLE_ID, iRow, self.YResolution*5/96)
		
	def iconProcess(self, iMode):
		screen = self.getScreen()	
		
		i = 0						
		for pLoopUnit in self.EuropeUnitsList:
			if self.I_SELECTED_SHIP == i:
				if iMode == self.ICON_RESUPPLY:
					CyMessageControl().sendDoCommand(pLoopUnit.getID(), CommandTypes.COMMAND_RESUPPLY_SHIPS, -1, -1, false)
					return 
				elif iMode == self.ICON_REPAIR:
					CyMessageControl().sendDoCommand(pLoopUnit.getID(), CommandTypes.COMMAND_REPAIR_SHIPS, False, -1, false) 
				elif iMode == self.ICON_STOP_REPAIR:
					CyMessageControl().sendDoCommand(pLoopUnit.getID(), CommandTypes.COMMAND_STOP_REPAIR_SHIP, -1, -1, false) 
				elif iMode == self.ICON_UNLOAD_CREW:
					CyMessageControl().sendDoCommand(pLoopUnit.getID(), CommandTypes.COMMAND_UNLOAD_CREW, -1, -1, false) 
				elif iMode == self.ICON_LOAD_CREW:
					CyMessageControl().sendDoCommand(pLoopUnit.getID(), CommandTypes.COMMAND_LOAD_CREW, -1, -1, false) 
				elif iMode == self.ICON_SELL:
					CyMessageControl().sendDoCommand(pLoopUnit.getID(), CommandTypes.COMMAND_SELL_SHIP, -1, -1, false) 
			i += 1
		
	def allIconShadows(self):
		screen = self.getScreen()
		screen.addDDSGFC("EuropeScreenIconSell", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SELL_SHADOW").getPath(), self.X_POS_ICON_PANCARTE + self.X_ICON_1, self.Y_POS_ICON_PANCARTE + self.Y_ICON_DECAL, self.SIZE_ICON_PANCARTE, self.SIZE_ICON_PANCARTE, WidgetTypes.WIDGET_GENERAL, self.ICON_SHADOW, -1 )
		screen.addDDSGFC("EuropeScreenIconChange", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_FLAG_PRIVATEER_SHADOW").getPath(), self.X_POS_ICON_PANCARTE + self.X_ICON_2, self.Y_POS_ICON_PANCARTE + self.Y_ICON_DECAL, self.SIZE_ICON_PANCARTE, self.SIZE_ICON_PANCARTE, WidgetTypes.WIDGET_GENERAL, self.ICON_SHADOW, -1 )
		screen.addDDSGFC("EuropeScreenIconUnloadAndLoadCrew", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_UNLOAD_CREW_SHADOW").getPath(), self.X_POS_ICON_PANCARTE + self.X_ICON_3, self.Y_POS_ICON_PANCARTE + self.Y_ICON_DECAL, self.SIZE_ICON_PANCARTE, self.SIZE_ICON_PANCARTE, WidgetTypes.WIDGET_GENERAL, self.ICON_SHADOW, -1 )
		screen.addDDSGFC("EuropeScreenIconResupply", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_RESUPPLY_SHADOW").getPath(), self.X_POS_ICON_PANCARTE + self.X_ICON_4, self.Y_POS_ICON_PANCARTE + self.Y_ICON_DECAL, self.SIZE_ICON_PANCARTE, self.SIZE_ICON_PANCARTE, WidgetTypes.WIDGET_GENERAL, self.ICON_SHADOW, -1 )
		screen.addDDSGFC("EuropeScreenIconRepair", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_REPAIR_SHADOW").getPath(), self.X_POS_ICON_PANCARTE + self.X_ICON_5, self.Y_POS_ICON_PANCARTE + self.Y_ICON_DECAL, self.SIZE_ICON_PANCARTE, self.SIZE_ICON_PANCARTE, WidgetTypes.WIDGET_GENERAL, self.ICON_SHADOW, -1 )
	
	def infosTactique(self):
		screen = self.getScreen()
		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		
		self.allIconShadows()
		
		i = 0
		bProcess = false
		for pLoopUnit in self.EuropeUnitsList:
			if self.I_SELECTED_SHIP == i:
				bProcess = true
				if pLoopUnit.getSelectedPicture():
					screen.setTableText(self.TABLE_ID, 0, i, u"", pLoopUnit.getSelectedPicture(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				else:
					screen.setTableText(self.TABLE_ID, 0, i, u"", pPlayer.getUnitButton(pLoopUnit.getUnitType()), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				pSelectUnit = pLoopUnit
			else:
				screen.setTableText(self.TABLE_ID, 0, i, u"", pPlayer.getUnitButton(pLoopUnit.getUnitType()), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			i += 1
			
		if bProcess:
			fRealForce = (float(pSelectUnit.baseCombatStr() * pSelectUnit.currHitPoints())) / (float(pSelectUnit.maxHitPoints()))
			fRealForce2 = (float(pSelectUnit.baseOriginCombatStr() * pSelectUnit.currHitPoints())) / (float(pSelectUnit.maxHitPoints()))
			iBaseForce = float(pSelectUnit.baseOriginCombatStr())
			iMaxAmmunition = gc.getUnitInfo(pSelectUnit.getUnitType()).getMaxMunition()
			
			#Icon du Navire
			screen.setImageButton(self.getNextWidgetName(), pSelectUnit.getEuropePicture(), self.XResolution/3 + 20, self.YResolution/5 - 20, self.XResolution*65/512 , self.YResolution*65/384, WidgetTypes.WIDGET_RENAME_SHIP, pSelectUnit.getID(), -1 )
			
			#Icon Sell
			if pSelectUnit.canSell():
				screen.setImageButton("EuropeScreenIconSell", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SELL").getPath(), self.X_POS_ICON_PANCARTE + self.X_ICON_1, self.Y_POS_ICON_PANCARTE + self.Y_ICON_DECAL, self.SIZE_ICON_PANCARTE, self.SIZE_ICON_PANCARTE,  WidgetTypes.WIDGET_GENERAL, self.ICON_SELL, -1)
		
			#Icon Drapeau
			# iRefUnit =
			# if iRefUnit == 9:
				# screen.setImageButton("EuropeScreenIconChange", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_FLAG_PRIVATEER").getPath(), self.X_POS_ICON_PANCARTE + self.X_INIT_DECAL_ICON_PANCARTE + self.X_ICON_DECAL, self.Y_POS_ICON_PANCARTE + self.Y_ICON_DECAL, self.SIZE_ICON_PANCARTE, self.SIZE_ICON_PANCARTE,  WidgetTypes.WIDGET_GENERAL, self.ICON_PRIVATEER, -1)
			# if iRefUnit == 7:
				# screen.setImageButton("EuropeScreenIconChange", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_FLAG_ESCORT").getPath(), self.X_POS_ICON_PANCARTE + self.X_INIT_DECAL_ICON_PANCARTE + self.X_ICON_DECAL, self.Y_POS_ICON_PANCARTE + self.Y_ICON_DECAL, self.SIZE_ICON_PANCARTE, self.SIZE_ICON_PANCARTE,  WidgetTypes.WIDGET_GENERAL, self.ICON_ESCORT, -1)
						
			#Icon Equipage
			if pSelectUnit.hasCrew():
				screen.setImageButton("EuropeScreenIconUnloadAndLoadCrew", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_UNLOAD_CREW").getPath(), self.X_POS_ICON_PANCARTE + self.X_ICON_3, self.Y_POS_ICON_PANCARTE + self.Y_ICON_DECAL, self.SIZE_ICON_PANCARTE, self.SIZE_ICON_PANCARTE,  WidgetTypes.WIDGET_GENERAL, self.ICON_UNLOAD_CREW, -1)
			else :
				screen.setImageButton("EuropeScreenIconUnloadAndLoadCrew", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_LOAD_CREW").getPath(), self.X_POS_ICON_PANCARTE + self.X_ICON_3, self.Y_POS_ICON_PANCARTE + self.Y_ICON_DECAL, self.SIZE_ICON_PANCARTE, self.SIZE_ICON_PANCARTE,  WidgetTypes.WIDGET_GENERAL, self.ICON_LOAD_CREW, -1)
			#Icon Resupply
			if iMaxAmmunition != -1 :
				screen.setImageButton("EuropeScreenIconResupply", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_RESUPPLY").getPath(), self.X_POS_ICON_PANCARTE + self.X_ICON_4, self.Y_POS_ICON_PANCARTE + self.Y_ICON_DECAL, self.SIZE_ICON_PANCARTE, self.SIZE_ICON_PANCARTE, WidgetTypes.WIDGET_GENERAL, self.ICON_RESUPPLY, -1)
		
			#Icon Repair
			if not pSelectUnit.isInEuropeDrydock() and pSelectUnit.isHurt():
				screen.setImageButton("EuropeScreenIconRepair", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_REPAIR").getPath(), self.X_POS_ICON_PANCARTE + self.X_ICON_5, self.Y_POS_ICON_PANCARTE + self.Y_ICON_DECAL, self.SIZE_ICON_PANCARTE, self.SIZE_ICON_PANCARTE,  WidgetTypes.WIDGET_GENERAL, self.ICON_REPAIR, -1)
			if pSelectUnit.isInEuropeDrydock():
				screen.setImageButton("EuropeScreenIconRepair", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_STOP_REPAIR").getPath(), self.X_POS_ICON_PANCARTE + self.X_ICON_5, self.Y_POS_ICON_PANCARTE + self.Y_ICON_DECAL, self.SIZE_ICON_PANCARTE, self.SIZE_ICON_PANCARTE,  WidgetTypes.WIDGET_GENERAL, self.ICON_STOP_REPAIR, -1)
			#Class du Navire
			szText = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_UNITCLASS", (gc.getUnitInfo(pSelectUnit.getUnitType()).getTextKey(), ))
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.XResolution/2, self.YResolution/5 - 28, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			#Force du Navire
			szText = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_POWER", ())
			if fRealForce != iBaseForce and fRealForce != 0:
				szRightBuffer = u" %.1f/%d" %(fRealForce, iBaseForce)
			else :
				szRightBuffer = u" %d/%d" %(fRealForce, iBaseForce)
			
			szText = szText + szRightBuffer
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.XResolution*2/3+20, self.YResolution/5 - 28, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
			#Mouvement du Navire
			szText = localText.getText("INTERFACE_PANE_MOVEMENT", ())
			szRightBuffer = u" %d" %(pSelectUnit.baseMoves())
			szText = szText + szRightBuffer
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.XResolution*4/5 + 20, self.YResolution/5 - 28, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
			#Soutes du Navire
			szText = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_CARGO_SPACE", ())
			iCargo = pSelectUnit.cargoSpace()
			if iCargo == 0:
				szRightBuffer = u" 0"
			else :
				szRightBuffer = u" %d/%d" %(pSelectUnit.getCargo(), iCargo)
			szText = szText + szRightBuffer				
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.XResolution/2, self.YResolution/5 - 28 + 25, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			#Canons du Navire
			szText = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_CANNONS", ())
			iMaxCannon = gc.getUnitInfo(pSelectUnit.getUnitType()).getMaxCannon()
			if iMaxCannon == -1:
				szRightBuffer = u" 0"
			else :
				szRightBuffer = u" %d/%d" %(pSelectUnit.getNbCannon(), iMaxCannon)
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			if pSelectUnit.getNbCannon() < iMaxCannon:
				szRightBuffer = localText.changeTextColor(szRightBuffer, gc.getInfoTypeForString("COLOR_RED"))
			else :
				szRightBuffer = localText.changeTextColor(szRightBuffer, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			szText = szText + szRightBuffer				
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.XResolution*2/3+20, self.YResolution/5 - 28 + 25, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			#Munition du navire
			szText = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_AMMUNITIONS", ())
			if iMaxAmmunition == -1 :
				szRightBuffer = u" 0"
			else :
				szRightBuffer = u" %d/%d" %(pSelectUnit.getMunition(), iMaxAmmunition)
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			if pSelectUnit.getMunition() <= iMaxAmmunition/2 :
				szRightBuffer = localText.changeTextColor(szRightBuffer, gc.getInfoTypeForString("COLOR_RED"))
			else :
				szRightBuffer = localText.changeTextColor(szRightBuffer, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			szText = szText + szRightBuffer				
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.XResolution*4/5 + 20, self.YResolution/5 - 28 + 25, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			#Etat du Navire
			szText = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_STATE_SHIP", ())
			iEtat = 100
			if iBaseForce != 0 :
				iEtat = fRealForce2*100/iBaseForce
				if iEtat == 0 :
					szRightBuffer = u" < 0.1/100"
				else :
					szRightBuffer = u" %d/100" %(iEtat)
			else :
				szRightBuffer = u" 0"
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			if iEtat < 100 :
				szRightBuffer = localText.changeTextColor(szRightBuffer, gc.getInfoTypeForString("COLOR_RED"))
			else :
				szRightBuffer = localText.changeTextColor(szRightBuffer, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			szText = szText + szRightBuffer				
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.XResolution/2, self.YResolution/5 - 28 + 25*2, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			#Statut du Navire
			szText = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_STATUS", ())
			
			if pSelectUnit.isInEuropeDrydock() :
				szRightBuffer = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_STATUS_DRY_DOCK_START", (pSelectUnit.healTurns(), ))
				szRightBuffer +=  u" " + localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_STATUS_DRY_DOCK_END", (pSelectUnit.healTurns(), ))
			else :
				szRightBuffer = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_STATUS_DOCKSIDE", ())
			szText = szText + u" " + szRightBuffer
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))								
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.XResolution*2/3+20, self.YResolution/5 - 28 + 25*2, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			#Equipage du Navire
			szText = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_CREW", ())
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))	
			if pSelectUnit.hasCrew() :
				pSailorType = pSelectUnit.getUnitSailorType()
				if pSailorType != -1 and pSailorType == UnitTypes.UNIT_SAILOR_EXPERT:
					szRightBuffer = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_CREW_EXPERIENCED", ())
				else :
					szRightBuffer = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_CREW_BEGINNER", ())
				szRightBuffer = localText.changeTextColor(szRightBuffer, gc.getInfoTypeForString("COLOR_FONT_CREAM"))	
			else :
				szRightBuffer = localText.getText("TXT_KEY_UNIT_HELP_IS_NOT_EQUIPED_SAILOR", ())
			szText = szText + u" " + szRightBuffer											
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.XResolution/2, self.YResolution/5 - 28 + 25*3, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			#Exp Navig du Navire
			iLevel = pSelectUnit.getLevelExploAndNavigation()
			if iLevel > 2 :
				iLevel = 2
			iExp = pSelectUnit.getExperienceExploAndNavigation()
			iExpLevel = 50*(2*(iLevel+1)-1+iLevel/2)#todo Hard code BADD
			szText = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_EXP_NAVIG", (iExp, iExpLevel, ))
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))	
			szPromoBuffer = u"   "
			for i in range(gc.getNumPromotionInfos()):
				if (pSelectUnit.isHasPromotion(i) and not gc.getPromotionInfo(i).isGraphicalOnly() and gc.getPromotionInfo(i).isExploAndNavigation()):
					szPromoBuffer += "<img=%s size=16></img>" % (gc.getPromotionInfo(i).getButton(), )
			szText = szText + szPromoBuffer
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.XResolution/2, self.YResolution/5 - 28 + 25*4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			#Exp Mil du Navire
			szText = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_EXP_MILIT", ())
			iExp = pSelectUnit.getExperience()
			
			if(iExp % 10 == 0) :
				szText += u" %d/%d" %(iExp/10, pSelectUnit.experienceNeeded()/10)
			else :
				szText += u" %.1f/%d" %((float(iExp)/float(10)), pSelectUnit.experienceNeeded()/10)

			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))	
			szPromoBuffer = u"   "
			for i in range(gc.getNumPromotionInfos()):
				if (pSelectUnit.isHasPromotion(i) and not gc.getPromotionInfo(i).isGraphicalOnly() and not gc.getPromotionInfo(i).isExploAndNavigation()):
					szPromoBuffer += "<img=%s size=16></img>" % (gc.getPromotionInfo(i).getButton(), )
			szText = szText + szPromoBuffer
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.XResolution/2, self.YResolution/5 - 28 + 25*5, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

			if pSelectUnit.canDoCommand(CommandTypes.COMMAND_PROMOTE, 1, -1, False):
				screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_COMMAND_PROMOTE").getPath(), self.X_OUTSIDE_PROMOTION_ICON_MARGIN, self.Y_PROMOTION_ICON, self.X_SIZE_PROMOTION_ICON, self.X_SIZE_PROMOTION_ICON, WidgetTypes.WIDGET_GENERAL, self.COMMAND_PROMOTE, pSelectUnit.getID() )
				
	def initEuropeShipsList(self) :
		EuropeUnitsList = []
		pPlayer = self.pPlayer

		EuropeGroupsList = []
		pGroup, Iterator = pPlayer.firstSelectionGroup(false)
		while (pGroup != None):
			iSpace = pGroup.getCargoSpace(True)
			if iSpace > 0:
				EuropeGroupsList.append((iSpace, pGroup))
			pGroup, Iterator = pPlayer.nextSelectionGroup(Iterator, false)
		
		if len(EuropeGroupsList) > 0:
			EuropeGroupsList.sort()
			EuropeGroupsList.reverse()
			for iGroup in range(len(EuropeGroupsList)):
				pGroup = EuropeGroupsList[iGroup][1]
				UnitsOfGroupsList = []
				for iUnit in range(pGroup.getNumUnits()):
					pShip = pGroup.getUnitAt(iUnit)
					if pShip.canTradeInEurope(True, False):
						UnitsOfGroupsList.append((pShip.cargoSpace(), pShip))
				if len(UnitsOfGroupsList) > 0:
					UnitsOfGroupsList.sort()
					UnitsOfGroupsList.reverse()
					for iOrderUnit in range(len(UnitsOfGroupsList)):
						pOrderUnit = UnitsOfGroupsList[iOrderUnit][1]
						self.EuropeUnitsList.append(pOrderUnit)

	def calculateSizesAndPositions(self):
		self.X_SCREEN = 0
		self.Y_SCREEN = 0

		screen = self.getScreen()

		self.XResolution = screen.getXResolution()
		self.YResolution = screen.getYResolution()
		self.W_SCREEN = screen.getXResolution()
		self.H_SCREEN = screen.getYResolution()

		self.Y_EXIT = self.YResolution - 36
		self.X_EXIT = self.XResolution - 30
		
		self.X_POS_DOCK = 8
		self.Y_POS_DOCK = self.YResolution/10 - 15
		self.X_SIZE_DOCK = self.XResolution/3 - 5
		self.Y_SIZE_DOCK = 45
		
		self.X_POS_INFO_TACT_HEAD = self.XResolution/3 - 20
		self.Y_POS_INFO_TACT_HEAD = self.Y_POS_DOCK
		self.X_SIZE_INFO_TACT_HEAD = self.XResolution*2/3 + 40
		self.Y_SIZE_INFO_TACT_HEAD = self.Y_SIZE_DOCK
		
		self.X_POS_TRADE_SHIP_HEAD = self.X_POS_INFO_TACT_HEAD
		self.Y_POS_TRADE_SHIP_HEAD = self.YResolution*4/10 - 20
		self.X_SIZE_TRADE_SHIP_HEAD = self.X_SIZE_INFO_TACT_HEAD
		self.Y_SIZE_TRADE_SHIP_HEAD = self.Y_SIZE_DOCK
		
		self.X_POS_TRADE_SHIP_PICT = self.XResolution/3 + 20
		self.Y_POS_TRADE_SHIP_PICT = self.Y_POS_TRADE_SHIP_HEAD + self.Y_SIZE_DOCK + 15
		self.X_SIZE_TRADE_SHIP_PICT = self.XResolution*2/3 - 40
		self.Y_SIZE_TRADE_SHIP_PICT = self.YResolution*11/24
		
		self.X_POS_TRADE_TEXT1 = self.X_POS_TRADE_SHIP_PICT + self.X_SIZE_TRADE_SHIP_PICT*35/214
		self.X_POS_TRADE_TEXT2 = self.X_POS_TRADE_SHIP_PICT + self.X_SIZE_TRADE_SHIP_PICT*52/107
		self.X_POS_TRADE_TEXT3 = self.X_POS_TRADE_SHIP_PICT + self.X_SIZE_TRADE_SHIP_PICT*5/6
		self.Y_POS_TRADE_TEXTS = self.Y_POS_TRADE_SHIP_PICT + self.Y_SIZE_TRADE_SHIP_PICT*17/352
		
		self.X_POS_USED_SHIPS = self.X_POS_TRADE_SHIP_PICT + self.X_SIZE_TRADE_SHIP_PICT*5/321
		self.X_POS_SELL_SHIPS = self.X_POS_TRADE_SHIP_PICT + self.X_SIZE_TRADE_SHIP_PICT*443/642
		self.X_POS_NEW_SHIPS = self.X_POS_TRADE_SHIP_PICT + self.X_SIZE_TRADE_SHIP_PICT*36/107
		self.X_DECAL_TEXT_SHIPS = self.X_SIZE_TRADE_SHIP_PICT*25/642
		self.X_DECAL_PRICE_SHIPS = self.X_SIZE_TRADE_SHIP_PICT*200/642
		self.Y_POS_SHIPS = self.Y_POS_TRADE_SHIP_PICT + self.Y_SIZE_TRADE_SHIP_PICT*47/352
		self.Y_DECAL_SHIPS = self.Y_SIZE_TRADE_SHIP_PICT*25/352
		
		self.X_POS_ICON_PANCARTE = self.xSize(18)
		self.Y_POS_ICON_PANCARTE = self.ySize(290)
		self.X_SIZE_ICON_PANCARTE = self.xSize(320)
		self.Y_SIZE_ICON_PANCARTE = self.ySize(80)
		
		self.X_INIT_DECAL_ICON_PANCARTE = self.X_SIZE_ICON_PANCARTE*3/62
		self.SIZE_ICON_PANCARTE = self.xSize(50)
		
		self.X_ICON_PANCARTE_MARGIN = self.xSize(8)
		self.X_OUTSIDE_ICON_PANCARTE_MARGIN = self.xSize(17)
		self.X_ICON_1 = self.calculatePanelIconPosition(1)
		self.X_ICON_2 = self.calculatePanelIconPosition(2)
		self.X_ICON_3 = self.calculatePanelIconPosition(3)
		self.X_ICON_4 = self.calculatePanelIconPosition(4)
		self.X_ICON_5 = self.calculatePanelIconPosition(5)
		self.Y_ICON_DECAL = self.Y_SIZE_ICON_PANCARTE * 13 / 84
		
		self.CARGO_ICON_SIZE = self.XResolution / 25
		self.W_TEXT_MARGIN = self.XResolution / 30

		self.Y_PROMOTION_ICON = self.ySize(220)
		self.X_SIZE_PROMOTION_ICON = self.minSize(60)
		self.X_OUTSIDE_PROMOTION_ICON_MARGIN = self.W_SCREEN - self.xSize(40) - self.X_SIZE_PROMOTION_ICON
		

	def calculatePanelIconPosition(self, index):
		return self.X_OUTSIDE_ICON_PANCARTE_MARGIN + (self.SIZE_ICON_PANCARTE + self.X_ICON_PANCARTE_MARGIN) * (index - 1)

	def minSize(self, val):
		return min(self.xSize(val), self.ySize(val))

	def xSize(self, val):
		return val*self.XResolution/1024

	def ySize(self, val):
		return val*self.YResolution/768

