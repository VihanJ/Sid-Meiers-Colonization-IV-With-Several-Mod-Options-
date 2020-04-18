## DoaNE
## Copyright M07 2011

##########################################################################################################
########## Europe Screen 3: Docks and Recruitment screen #################################################
##########################################################################################################

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvEuropeC3Screen:

	def __init__(self):
		self.WIDGET_ID = "EuropeC3ScreenWidget"
		self.TABLE_ID = "EuropeC3ScreenTable"
		self.CIV_DROP_DOWN = "CivDropDown"
		self.nWidgetCount = 0

		self.TREASURY_ID = 1
		self.CHANGE_MODE = 2
		self.LOAD_ALL = 3
		self.UNLOAD_ALL = 4
		self.HELP_SHIP = 5
		self.CHANGE_TRANSIT_MODE = 6
		self.NO_SHIP_SELECTED = 7
		self.HELP_CHANGE_PROFESSION = 8
		self.HELP_DESTINATIONCITY = 9
		self.SHOW_SAILORS = 10
		self.HELP_DESTINATION_CITY = 11
		self.ADD_BUILDER_PACK = 12
		self.REMOVE_BUILDER_PACK = 13
		self.ASK_USE_RELATION_POINTS_FOR_IMMIGRATION = 14

		self.selectedPlayerList = []
		self.EuropeUnitsList = []
		
	def getScreen(self):
		return CyGInterfaceScreen("europeC3Screen", CvScreenEnums.EUROPE_C3_SCREEN)

	def interfaceScreen(self):
	
		if ( CyGame().isPitbossHost() ):
			return
		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		self.pPlayer  = pPlayer

		if pPlayer.getParent() == PlayerTypes.NO_PLAYER:
			return
	
		screen = self.getScreen()
		if screen.isActive():
			return
			
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.XResolution = screen.getXResolution()
		self.YResolution = screen.getYResolution()
		self.W_SCREEN = screen.getXResolution()
		self.H_SCREEN = screen.getYResolution()

		self.Y_EXIT = self.YResolution - 36
		self.X_EXIT = self.XResolution - 30

		self.CARGO_ICON_SIZE = self.XResolution / 25
		self.Y_CARGO_ICON_SIZE = self.YResolution * 19 / 181

		self.H_LOADING_LIST = self.Y_CARGO_ICON_SIZE + 5

		self.W_TEXT_MARGIN = self.XResolution / 30
		self.CARGO_SPACING  = self.CARGO_ICON_SIZE + 2
		self.Y_TITLE = 4
		
		self.X_POS_DOCK_SHIP = 8
		self.Y_POS_DOCK_SHIP = self.YResolution/10 - 15
		self.X_SIZE_DOCK_SHIP = self.XResolution/3 - 5
		self.Y_SIZE_DOCK_SHIP = 45
		
		self.X_SIZE_ENROLEMENT = self.XResolution/3 - 5
		self.Y_SIZE_MAIN_ENROLEMENT = (self.YResolution/4 + self.YResolution/3)/2 +2
		self.X_POS_ENROLEMENT = self.XResolution - 8 - self.X_SIZE_ENROLEMENT
		self.Y_POS_MAIN_ENROLEMENT = self.YResolution/4
		self.Y_POS_HEADER_ENROLEMENT = self.YResolution*3/20 - 2
		
		self.X_POS_PARCHEMIN = self.XResolution/3 + 3
		self.Y_POS_PARCHEMIN = self.YResolution/10 - 25
		self.X_SIZE_PARCHEMIN = self.XResolution/3 - 5
		self.Y_SIZE_PARCHEMIN = self.YResolution/10 + 15
		
		self.Y_POS_TITLE_PARCHEMIN = self.Y_SIZE_PARCHEMIN*15/91
		self.Y_POS_INFO1_PARCHEMIN = self.Y_SIZE_PARCHEMIN*35/91
		self.Y_POS_INFO2_PARCHEMIN = self.Y_SIZE_PARCHEMIN*50/91
		self.Y_POS_INFO3_PARCHEMIN = self.Y_SIZE_PARCHEMIN*65/91
		
		self.Y_SIZE_TRANSIT = self.Y_POS_MAIN_ENROLEMENT + self.Y_SIZE_MAIN_ENROLEMENT + 33 - (self.Y_POS_PARCHEMIN + self.Y_SIZE_PARCHEMIN + 45 + 50)
		self.X_POS_INFOS_TITLE = self.X_POS_PARCHEMIN - 30
		self.Y_POS_INFOS_TITLE = self.Y_POS_PARCHEMIN + self.Y_SIZE_PARCHEMIN + 95 + self.Y_SIZE_TRANSIT + 10
		self.X_SIZE_INFOS_TITLE = self.XResolution*2/3 + 35
		self.Y_SIZE_INFOS_TITLE = 35
		self.X_POS_INFOS = self.X_POS_INFOS_TITLE + 30
		self.Y_POS_INFOS = self.Y_POS_INFOS_TITLE + self.Y_SIZE_INFOS_TITLE + 10
		self.Y_SIZE_INFOS = self.YResolution/4
		self.X_SIZE_INFOS = self.XResolution*2/3 - 30
		
		self.X_POS_DOCK = 8
		self.Y_POS_DOCK = self.YResolution/2 - 12
		self.X_SIZE_DOCK = self.XResolution/3 - 5
		self.Y_SIZE_DOCK = 35
		self.Y_SIZE_DOCK_BODY = self.YResolution/5
		self.X_SIZE_DOCK_BODY = self.X_SIZE_DOCK - 10
		self.Y_OFFSET_DOCK = 15
		self.X_CHECKBOX_SIZE = 20 * self.XResolution / 768

		
		self.X_POS_MESSAGE = 25
		self.Y_POS_MESSAGE = self.Y_POS_DOCK + self.Y_SIZE_DOCK + self.Y_SIZE_DOCK_BODY + 10
		self.X_SIZE_MESSAGE = self.XResolution/3 - 35
		self.Y_SIZE_MESSAGE = self.YResolution/7 + 18

		self.CHANGE_PROFESSION_HELP_ICON_SIZE = 50 
		
		self.IN_PORT_PANE_WIDTH = self.XResolution/3
		self.I_SELECTED_SHIP = -1
		
		self.iEnrolMode = 1
		self.iTransitMode = 1
		
		# Set the background and exit button, and show the screen
		screen.setDimensions(0, 0, self.XResolution, self.YResolution)
		screen.showWindowBackground(False)
		
		screen.addDDSGFC("EuropeScreenShipQuayImage", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), 8, self.YResolution/10 - 15, self.XResolution/3 - 5, 45, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addDDSGFC("EuropeScreenUp", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BANDEAU_MARRON").getPath(), 0, 0, self.XResolution, 40, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("EuropeScreenDown", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BANDEAU_MARRON").getPath(), 0, self.YResolution - 86, self.XResolution, 86, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addDDSGFC("EuropeScreenBackground", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_IMMIGRATION_BACKGROUND").getPath(), 0, 40, self.XResolution, self.YResolution - 86, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("TopPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TITLE").getPath(), 0, 0, self.XResolution, 55, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Header...
		screen.setLabel("EuropeScreenWidgetHeader", "Background", u"<font=4b>" + localText.getText("TXT_KEY_EUROPE_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.XResolution / 2, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setImageButton("E3SEnrolementTitleShadow", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_ENROLEMENT, self.Y_POS_HEADER_ENROLEMENT - 50, self.X_SIZE_ENROLEMENT, 45, WidgetTypes.WIDGET_GENERAL, self.CHANGE_MODE, 0)
				
		screen.addDDSGFC("E3SEnrolementMainShadow", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_ENROLEMENT, self.Y_POS_MAIN_ENROLEMENT + 7, self.X_SIZE_ENROLEMENT, self.Y_SIZE_MAIN_ENROLEMENT + 25, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addScrollPanel("EnrolList", u"", self.X_POS_ENROLEMENT, self.Y_POS_MAIN_ENROLEMENT, self.X_SIZE_ENROLEMENT, self.Y_SIZE_MAIN_ENROLEMENT, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Zone de Transit
		iAgrandis = 15
		iLargeurTransit = self.Y_POS_MAIN_ENROLEMENT + self.Y_SIZE_MAIN_ENROLEMENT + 33 - (self.Y_POS_PARCHEMIN + self.Y_SIZE_PARCHEMIN + 45 + 50)
		screen.addDDSGFC("EuropeScreenZoneDeTransitHeader", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_PARCHEMIN - iAgrandis, self.Y_POS_PARCHEMIN + self.Y_SIZE_PARCHEMIN + 10, self.X_SIZE_PARCHEMIN + 2*iAgrandis, 35, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_RECUITMENT_AREA", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setLabel("EuropeScreenZoneDeTransitHeaderText", "background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_PARCHEMIN + self.X_SIZE_PARCHEMIN/2, self.Y_POS_PARCHEMIN + self.Y_SIZE_PARCHEMIN + 20, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
		screen.addDDSGFC("EuropeScreenZoneDeTransitShadow", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_PARCHEMIN - iAgrandis, self.Y_POS_PARCHEMIN + self.Y_SIZE_PARCHEMIN + 45 + 50, self.X_SIZE_PARCHEMIN + 2*iAgrandis,  self.Y_SIZE_TRANSIT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addScrollPanel("ZoneDeTransit", u"", self.X_POS_PARCHEMIN - iAgrandis, self.Y_POS_PARCHEMIN + self.Y_SIZE_PARCHEMIN + 45 + 50, self.X_SIZE_PARCHEMIN + 2*iAgrandis,  self.Y_SIZE_TRANSIT - 25, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Informations immigrations
		screen.addDDSGFC("EuropeScreenTipsToRecruitImmigrantsHeader", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_INFOS_TITLE , self.Y_POS_INFOS_TITLE, self.X_SIZE_INFOS_TITLE, self.Y_SIZE_INFOS_TITLE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_TIPS_TO_RECRUIT_IMMIGRANTS", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setLabel("EuropeScreenTipsToRecruitImmigrantsText", "background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_INFOS_TITLE + self.X_SIZE_INFOS_TITLE/2, self.Y_POS_INFOS_TITLE + self.Y_SIZE_INFOS_TITLE*7/24, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.addDDSGFC("E3STipsToRecruitImmigrantsMainShadow", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_INFOS - 25, self.Y_POS_INFOS, self.X_SIZE_INFOS + 50, self.Y_SIZE_INFOS + 25, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addScrollPanel("TipsToRecruitImmigrants", u"", self.X_POS_INFOS, self.Y_POS_INFOS - 10, self.X_SIZE_INFOS, self.Y_SIZE_INFOS, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Dock
		screen.addDDSGFC("EuropeScreenDockHeader", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_DOCK, self.Y_POS_DOCK, self.X_SIZE_DOCK, self.Y_SIZE_DOCK, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_DOCKS", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setLabel("EuropeScreenDockText", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_DOCK + self.X_SIZE_DOCK/2, self.Y_POS_DOCK + self.Y_SIZE_DOCK/4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.addDDSGFC("EuropeScreenDock", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_DOCK, self.Y_POS_DOCK + self.Y_SIZE_DOCK + self.Y_OFFSET_DOCK, self.X_SIZE_DOCK, self.Y_SIZE_DOCK_BODY, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addScrollPanel("DockList", u"", 15, self.Y_POS_DOCK + self.Y_SIZE_DOCK + self.Y_OFFSET_DOCK, self.X_SIZE_DOCK_BODY, self.Y_SIZE_DOCK_BODY - 30, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_DOCK, -1, -1 )
		
		screen.addDDSGFC("EuropeScreenDockHelpChangeProfession", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CHANGE_PROFESSION_IN_EUROPE_HELP").getPath(), self.X_POS_DOCK + self.X_SIZE_DOCK - self.CHANGE_PROFESSION_HELP_ICON_SIZE - 15, self.Y_POS_DOCK - 5, self.CHANGE_PROFESSION_HELP_ICON_SIZE, self.CHANGE_PROFESSION_HELP_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, self.HELP_CHANGE_PROFESSION, -1 )
		screen.addDDSGFC("EuropeScreenDockHelpDestinationCity", ArtFileMgr.getInterfaceArtInfo("INTERFACE_DESTINATION_IN_EUROPE_HELP").getPath(), self.X_POS_DOCK + self.X_SIZE_DOCK - self.CHANGE_PROFESSION_HELP_ICON_SIZE * 2 - 15, self.Y_POS_DOCK - 5, self.CHANGE_PROFESSION_HELP_ICON_SIZE, self.CHANGE_PROFESSION_HELP_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, self.HELP_DESTINATIONCITY, -1 )
		
		# Message
		
		screen.addListBoxGFC("MessageList2", "", self.X_POS_MESSAGE, self.Y_POS_MESSAGE, self.X_SIZE_MESSAGE, self.Y_SIZE_MESSAGE, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect("MessageList2", False)		
		
		#Soutes		
		screen.addScrollPanel("LoadingList", u"", 15, self.YResolution/3 + 20, self.XResolution/3 - 15, self.H_LOADING_LIST, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_MOVE_CARGO_TO_TRANSPORT, -1, -1 )
			
		bShowEnrolUnit = false
		for i in range(gc.getNumUnitInfos()):
			UnitInfo = gc.getUnitInfo(i)					
			if pPlayer.getEnrolUnitType(UnitInfo.getUnitClassType()):
				bShowEnrolUnit = true
				break
		if bShowEnrolUnit:
			self.iEnrolMode = 0

		#Debug PullDown
		if CyGame().isDebugMode():
			xSize = 192
			screen.addDropDownBoxGFC(self.CIV_DROP_DOWN, self.XResolution/2 - xSize*3/2, 0, xSize, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.SMALL_FONT )
			screen.setActivation(self.CIV_DROP_DOWN, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

			for j in range(gc.getMAX_PLAYERS()):
				loopPlayer = gc.getPlayer(j)
				if (loopPlayer.isAlive() and not loopPlayer.isEurope() and not loopPlayer.isNative()):
					screen.addPullDownString(self.CIV_DROP_DOWN, loopPlayer.getName(), j, j, False )
		else:
			screen.hide(self.CIV_DROP_DOWN)
				
		self.initEuropeShipsList()
		self.drawTabs()
		self.setTab(3, True)
		self.drawTable()
		# draw the contents
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
	
		player = self.pPlayer
		playerEurope = gc.getPlayer(player.getParent())

		self.deleteAllWidgets()
		
		screen = self.getScreen()
		
		self.showCargaison()
		self.showTransitOnglet()
		self.showEnrolOnglet()
		self.showTipsToRecruitImmigrants()
		# Units waiting on Docks
		XLocation = 0
		YLocation = 0

		# Parchemin Notoriety
		self.displayNotorietyInfo()
		self.displayCheckBoxForSailors()

		iUnit = 0
		#We display all units except sailors
		for i in range(player.getNumEuropeUnits()):
			loopUnit = player.getEuropeUnit(i)
			if loopUnit.getCrewFormationTurn() == 0 and loopUnit.getProfession() != ProfessionTypes.PROFESSION_SAILOR:
				screen.addDragableButtonAt("DockList", self.getNextWidgetName(), loopUnit.getFullLengthIcon(), "", XLocation, YLocation, self.CARGO_ICON_SIZE, self.Y_CARGO_ICON_SIZE, WidgetTypes.WIDGET_DOCK, loopUnit.getID(), player.getID(), ButtonStyles.BUTTON_STYLE_LABEL )
				if loopUnit.getDestinationCity() >= 0:
					screen.addDDSGFCAt(self.getNextWidgetName(), "DockList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_AUTOMATIC_TRANSPORT_IMMIGRATION").getPath(), XLocation + self.CARGO_ICON_SIZE * 3 / 4, YLocation, 20, 20, WidgetTypes.WIDGET_GENERAL, self.HELP_DESTINATION_CITY, loopUnit.getID(), False )
				if ((iUnit + 1) % 6) == 0:
					XLocation = 0
					YLocation += self.Y_CARGO_ICON_SIZE
				else:
					XLocation += self.CARGO_ICON_SIZE
				iUnit = iUnit + 1

		displaySailorWithoutDestinationCity = player.isSecondaryOption(SecondaryPlayerOptionTypes.SECONDARYPLAYEROPTION_SHOW_SAILORS_IN_IMMIGRATION)	
		#We display sailors now
		for i in range(player.getNumEuropeUnits()):
			loopUnit = player.getEuropeUnit(i)
			if loopUnit.getCrewFormationTurn() == 0 and loopUnit.getProfession() == ProfessionTypes.PROFESSION_SAILOR and (displaySailorWithoutDestinationCity or loopUnit.getDestinationCity() >= 0):
				screen.addDragableButtonAt("DockList", self.getNextWidgetName(), loopUnit.getFullLengthIcon(), "", XLocation, YLocation, self.CARGO_ICON_SIZE, self.Y_CARGO_ICON_SIZE, WidgetTypes.WIDGET_DOCK, loopUnit.getID(), player.getID(), ButtonStyles.BUTTON_STYLE_LABEL )
			
				if loopUnit.getDestinationCity() >= 0:
					screen.addDDSGFCAt(self.getNextWidgetName(), "DockList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_AUTOMATIC_TRANSPORT_IMMIGRATION").getPath(), XLocation + self.CARGO_ICON_SIZE * 3 / 4, YLocation, 20, 20, WidgetTypes.WIDGET_GENERAL, self.HELP_DESTINATION_CITY, loopUnit.getID(), False )
				
				if ((iUnit + 1) % 6) == 0:
					XLocation = 0
					YLocation += self.Y_CARGO_ICON_SIZE
				else:
					XLocation += self.CARGO_ICON_SIZE
				iUnit = iUnit + 1
			
		i = 0
		for pLoopUnit in self.EuropeUnitsList:
			if self.I_SELECTED_SHIP == i and pLoopUnit.getSelectedPicture():
				screen.setTableText(self.TABLE_ID, 0, i, u"", pLoopUnit.getSelectedPicture(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			else:
				screen.setTableText(self.TABLE_ID, 0, i, u"", player.getUnitButton(pLoopUnit.getUnitType()), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			i += 1
				
		self.showTransitUnits()
		
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_TREASURY", (player.getGold(), )).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.W_TEXT_MARGIN, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.TREASURY_ID, -1 )
		
		self.replaceAllEnrolUnits()
		
		screen.clearListBoxGFC("MessageList")
		for i in range(player.getNumEventEuropeMessages()):
			screen.prependListBoxString("MessageList", u"<font=1>" + player.getEventEuropeMessage(i) + u"</font>", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
		screen.clearListBoxGFC("MessageList2")
		for i in range(player.getNumTradeMessages()):
			screen.prependListBoxString("MessageList2",  u"<font=1>" + player.getTradeMessage(i) + u"</font>", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		return 0

	def displayNotorietyInfo(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer
		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_NOTORIETY").getPath(), self.X_POS_PARCHEMIN, self.Y_POS_PARCHEMIN - 10, self.X_SIZE_PARCHEMIN, self.Y_SIZE_PARCHEMIN + 20, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_NOTRIETY_TITLE", ()).upper(), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_PARCHEMIN + self.X_SIZE_PARCHEMIN/2 ,self.Y_POS_PARCHEMIN + self.Y_POS_TITLE_PARCHEMIN, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_OVERALL_TREND", (pPlayer.generalAttraction(), )), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_POS_PARCHEMIN + self.X_SIZE_PARCHEMIN/10 ,self.Y_POS_PARCHEMIN + self.Y_POS_INFO1_PARCHEMIN, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_WEAK_POINT", (pPlayer.weaknessAttraction(), )), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_POS_PARCHEMIN + self.X_SIZE_PARCHEMIN/10 ,self.Y_POS_PARCHEMIN + self.Y_POS_INFO2_PARCHEMIN, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_STRONG_POINT", (pPlayer.strongPointAttraction(), )), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_POS_PARCHEMIN + self.X_SIZE_PARCHEMIN - self.X_SIZE_PARCHEMIN/10 ,self.Y_POS_PARCHEMIN + self.Y_POS_INFO2_PARCHEMIN, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_IMMIGRATION_RELATION_POINTS", (pPlayer.getImmigrationRelationPoints(), )), gc.getInfoTypeForString("COLOR_EUROPE_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_POS_PARCHEMIN + self.X_SIZE_PARCHEMIN/10 ,self.Y_POS_PARCHEMIN + self.Y_POS_INFO3_PARCHEMIN, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_TRANSFERT_INVISIBLE").getPath(), self.X_POS_PARCHEMIN, self.Y_POS_PARCHEMIN - 10, self.X_SIZE_PARCHEMIN, self.Y_SIZE_PARCHEMIN + 20, WidgetTypes.WIDGET_NOTORIETY, pPlayer.getID(), -1 )
		
	def displayCheckBoxForSailors(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer

		InterfaceActive = ArtFileMgr.getInterfaceArtInfo("INTERFACE_UNIT_COCHE_ACTIVATE").getPath()
		InterfaceNoActive = ArtFileMgr.getInterfaceArtInfo("INTERFACE_UNIT_COCHE_NO_ACTIVATE").getPath()

		InterfaceRequirments = InterfaceNoActive
		if(pPlayer.isSecondaryOption(SecondaryPlayerOptionTypes.SECONDARYPLAYEROPTION_SHOW_SAILORS_IN_IMMIGRATION)):
			InterfaceRequirments = InterfaceActive
		screen.setImageButton(self.getNextWidgetName(), InterfaceRequirments, self.X_POS_DOCK + 10, self.Y_POS_DOCK + self.Y_SIZE_DOCK - 3, self.X_CHECKBOX_SIZE, self.X_CHECKBOX_SIZE, WidgetTypes.WIDGET_GENERAL, self.SHOW_SAILORS, -1)
		
		szText =  u"<font=1>" + localText.getText("TXT_KEY_CHEXK_BOX_SHOW_SAILORS", ()) + u"</font>"
		screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_POS_DOCK + 10 + self.X_CHECKBOX_SIZE, self.Y_POS_DOCK + self.Y_SIZE_DOCK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.SHOW_SAILORS, -1)
				
	def inverseShowSailorOption(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer

		CyMessageControl().sendPlayerAction(pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_SEND_SECONDARYPLAYER_OPTION, SecondaryPlayerOptionTypes.SECONDARYPLAYEROPTION_SHOW_SAILORS_IN_IMMIGRATION, not pPlayer.isSecondaryOption(SecondaryPlayerOptionTypes.SECONDARYPLAYEROPTION_SHOW_SAILORS_IN_IMMIGRATION), -1)
		
	def showTipsToRecruitImmigrants(self):
		screen = self.getScreen()
		
		pPlayer = self.pPlayer

		xStartCityText = 15*self.XResolution/1024
		xImmigrantsOffset = 150*self.XResolution/1024
		yDecalCityText = 50*self.YResolution/768

		xSizeImmigrant = 25*self.XResolution/1024
		ySizeImmigrant = xSizeImmigrant*2
		yImmigrantOffset = ySizeImmigrant/2
		yStartCityText = ySizeImmigrant/2 + 10
		
		maxImmigrantsByRows = 9

		iProfession = gc.getUnitInfo(0).getDefaultProfession()

		ImmigrantsNeededList = []
		(loopCity, iter) = pPlayer.firstCity(false)
		while(loopCity):
			iUnit = 0
			ImmigrantsNeededForCityList = []
			for i in range(gc.getNumUnitInfos()):
				iUnitInfo = gc.getNumUnitInfos() - (i+1)
				UnitInfo = gc.getUnitInfo(iUnitInfo)
					
				iImmigrantNeeded =  loopCity.getNumNeededEnrolUnitType(UnitInfo.getUnitClassType())
				if (iImmigrantNeeded > 0) :
					ImmigrantsNeededForCityList.append((iImmigrantNeeded, UnitInfo.getUnitClassType()))
					iUnit += iImmigrantNeeded
			if iUnit > 0:
				ImmigrantsNeededList.append((iUnit, loopCity.getID(), ImmigrantsNeededForCityList))
			
			(loopCity, iter) = pPlayer.nextCity(iter, false)
		
		if len(ImmigrantsNeededList) > 0:
			ImmigrantsNeededList.sort()
			#ImmigrantsNeededList.reverse()
			for iCity in range(len(ImmigrantsNeededList)):
				loopCity = pPlayer.getCity(ImmigrantsNeededList[iCity][1])
				ImmigrantsNeededForCityList = ImmigrantsNeededList[iCity][2]

				screen.setTextAt(self.getNextWidgetName(), "TipsToRecruitImmigrants", u"<font=2b>" + loopCity.getName()+ "</font>", CvUtil.FONT_LEFT_JUSTIFY, xStartCityText, yStartCityText + iCity*yDecalCityText, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				for iUnit in range(len(ImmigrantsNeededForCityList)):
					iImmigrantNeeded = ImmigrantsNeededForCityList[iUnit][0]
					eUnitClassType = ImmigrantsNeededForCityList[iUnit][1]
					iUnitType = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(eUnitClassType)
					if iUnitType != UnitTypes.NO_UNIT:
						UnitInfo = gc.getUnitInfo(iUnitType)
						xPosEnrol = xImmigrantsOffset + iUnit*( xSizeImmigrant * 2)
						yPosEnrol = yStartCityText - yImmigrantOffset + iCity*yDecalCityText

						szText = u"x%d" %(iImmigrantNeeded)
					
						szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
						screen.setLabelAt(self.getNextWidgetName(), "TipsToRecruitImmigrants", u"<font=2>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPosEnrol + xSizeImmigrant, yPosEnrol + ySizeImmigrant/2, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

						screen.setImageButtonAt(self.getNextWidgetName(), "TipsToRecruitImmigrants", UnitInfo.getArtInfo(0, iProfession).getFullLengthIcon(), xPosEnrol, yPosEnrol, xSizeImmigrant, ySizeImmigrant, WidgetTypes.WIDGET_TIPS_ENROL_UNIT_TYPE, iUnitType, pPlayer.getID())
						iUnit += 1
						if(iUnit == maxImmigrantsByRows) :
							break
						
	def showTransitUnits(self):
		screen = self.getScreen()
		
		player = self.pPlayer
		iTransitMode = self.iTransitMode
		XLocation = 10
		YLocation = 5

		iProfession = gc.getUnitInfo(0).getDefaultProfession()

		iUnit = 0
		(tempUnit, iter) = player.firstTempUnit() #Iterate all temp units
		while (tempUnit):
			if tempUnit.getProfession() != -1 and tempUnit.getProfession() != ProfessionTypes.PROFESSION_SAILOR:
				if iTransitMode == 1 or  (iTransitMode == 2 and tempUnit.getImmigrationType() != ImmigrationTypes.IMMIGRATION_CONTRACT) or (iTransitMode == 3 and tempUnit.getImmigrationType() == ImmigrationTypes.IMMIGRATION_CONTRACT):
					tempUnit.getFullLengthIcon()
					screen.setImageButtonAt(self.getNextWidgetName(), "ZoneDeTransit", gc.getUnitInfo(tempUnit.getUnitType()).getArtInfo(0, iProfession).getFullLengthIcon(), XLocation, YLocation, self.CARGO_ICON_SIZE, self.Y_CARGO_ICON_SIZE, WidgetTypes.WIDGET_DO_PROPOSAL_TO_IMMIGRANT, tempUnit.getID(), player.getID())
					if tempUnit.getImmigrationType() == ImmigrationTypes.IMMIGRATION_CONTRACT:
						screen.setImageButtonAt(self.getNextWidgetName(), "ZoneDeTransit", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_PURCHASE_BID").getPath(), XLocation + self.CARGO_ICON_SIZE, YLocation, 20, 20,  WidgetTypes.WIDGET_DO_PROPOSAL_TO_IMMIGRANT, tempUnit.getID(), player.getID())
					elif tempUnit.getImmigrationType() == ImmigrationTypes.IMMIGRATION_FOOD:
						screen.setImageButtonAt(self.getNextWidgetName(), "ZoneDeTransit", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_FAMINE").getPath(), XLocation + self.CARGO_ICON_SIZE, YLocation, 20, 20,  WidgetTypes.WIDGET_DO_PROPOSAL_TO_IMMIGRANT, tempUnit.getID(), player.getID())
					elif tempUnit.getImmigrationType() == ImmigrationTypes.IMMIGRATION_ECONOMIC:
						screen.setImageButtonAt(self.getNextWidgetName(), "ZoneDeTransit", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_PAUVRETE").getPath(), XLocation + self.CARGO_ICON_SIZE, YLocation, 20, 20,  WidgetTypes.WIDGET_DO_PROPOSAL_TO_IMMIGRANT, tempUnit.getID(), player.getID())
					elif tempUnit.getImmigrationType() == ImmigrationTypes.IMMIGRATION_RELIGIOUS:
						screen.setImageButtonAt(self.getNextWidgetName(), "ZoneDeTransit", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_RELIGION").getPath(), XLocation + self.CARGO_ICON_SIZE, YLocation, 20, 20,  WidgetTypes.WIDGET_DO_PROPOSAL_TO_IMMIGRANT, tempUnit.getID(), player.getID())
					if ((iUnit + 1) % 6) == 0:
						XLocation = 10
						YLocation += self.Y_CARGO_ICON_SIZE
					else:
						XLocation += self.CARGO_ICON_SIZE + 10
					iUnit = iUnit + 1
			(tempUnit, iter) = player.nextTempUnit(iter)
		
	def showEnrolOnglet(self):
		screen = self.getScreen()
		
		iEnrolMode = self.iEnrolMode
		
		iDepEnrTit = 8
		iYSizeEnrolTitle = 35
	
		iDecal = iYSizeEnrolTitle/3
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_APPEL_IMMIGRATION", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setText("E3SEnrolementTitleText", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_ENROLEMENT + self.X_SIZE_ENROLEMENT/2, self.Y_POS_HEADER_ENROLEMENT - 50 + iDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, self.CHANGE_MODE, 0)
		
		iDecal = iYSizeEnrolTitle/6
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_ENROLEMENT_EXTERNE", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setText("E3SEnrolementTitle1Text", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_ENROLEMENT + iDepEnrTit + self.X_SIZE_ENROLEMENT/4 - 1, self.Y_POS_HEADER_ENROLEMENT + iDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_ENROLEMENT_INTERNE", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setText("E3SEnrolementTitle2Text", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_ENROLEMENT + self.X_SIZE_ENROLEMENT/2 - iDepEnrTit + self.X_SIZE_ENROLEMENT/4 - 1, self.Y_POS_HEADER_ENROLEMENT + iDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_ENROLEMENT_MILITARY", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setText("E3SEnrolementTitle3Text", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_ENROLEMENT + iDepEnrTit + self.X_SIZE_ENROLEMENT/4 - 1, self.Y_POS_HEADER_ENROLEMENT + iDecal + iYSizeEnrolTitle, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_ENROLEMENT_OTHER", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setText("E3SEnrolementTitle4Text", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_ENROLEMENT + self.X_SIZE_ENROLEMENT/2 - iDepEnrTit + self.X_SIZE_ENROLEMENT/4 - 1, self.Y_POS_HEADER_ENROLEMENT + iDecal + iYSizeEnrolTitle, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setImageButton("E3SEnrolementTitle1Shadow", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_ENROLEMENT + iDepEnrTit, self.Y_POS_HEADER_ENROLEMENT, self.X_SIZE_ENROLEMENT/2 - 2, iYSizeEnrolTitle, WidgetTypes.WIDGET_GENERAL, self.CHANGE_MODE, 1)
		screen.setImageButton("E3SEnrolementTitle2Shadow", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_ENROLEMENT + self.X_SIZE_ENROLEMENT/2 - iDepEnrTit, self.Y_POS_HEADER_ENROLEMENT, self.X_SIZE_ENROLEMENT/2 - 2, iYSizeEnrolTitle, WidgetTypes.WIDGET_GENERAL, self.CHANGE_MODE, 2)
		screen.setImageButton("E3SEnrolementTitle3Shadow", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_ENROLEMENT + iDepEnrTit, self.Y_POS_HEADER_ENROLEMENT + iYSizeEnrolTitle, self.X_SIZE_ENROLEMENT/2 - 2, iYSizeEnrolTitle, WidgetTypes.WIDGET_GENERAL, self.CHANGE_MODE, 3)
		screen.setImageButton("E3SEnrolementTitle4Shadow", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_ENROLEMENT + self.X_SIZE_ENROLEMENT/2 - iDepEnrTit, self.Y_POS_HEADER_ENROLEMENT + iYSizeEnrolTitle, self.X_SIZE_ENROLEMENT/2 - 2, iYSizeEnrolTitle, WidgetTypes.WIDGET_GENERAL, self.CHANGE_MODE, 4)
		
		if iEnrolMode == 1:
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_ENROLEMENT_EXTERNE", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			screen.setLabel("E3SEnrolementTitle1Text", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_ENROLEMENT + iDepEnrTit + self.X_SIZE_ENROLEMENT/4 - 1, self.Y_POS_HEADER_ENROLEMENT + iDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if iEnrolMode == 2:
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_ENROLEMENT_INTERNE", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			screen.setLabel("E3SEnrolementTitle2Text", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_ENROLEMENT + self.X_SIZE_ENROLEMENT/2 - iDepEnrTit + self.X_SIZE_ENROLEMENT/4 - 1, self.Y_POS_HEADER_ENROLEMENT + iDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if iEnrolMode == 3:
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_ENROLEMENT_MILITARY", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			screen.setLabel("E3SEnrolementTitle3Text", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_ENROLEMENT + iDepEnrTit + self.X_SIZE_ENROLEMENT/4 - 1, self.Y_POS_HEADER_ENROLEMENT + iDecal + iYSizeEnrolTitle, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)	
		if iEnrolMode == 4:
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_ENROLEMENT_OTHER", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			screen.setLabel("E3SEnrolementTitle4Text", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_ENROLEMENT + self.X_SIZE_ENROLEMENT/2 - iDepEnrTit + self.X_SIZE_ENROLEMENT/4 - 1, self.Y_POS_HEADER_ENROLEMENT + iDecal + iYSizeEnrolTitle, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
	
	def showTransitOnglet(self):
		screen = self.getScreen()
		iTransitMode = self.iTransitMode
		self.Y_SIZE_TRANSIT_ONGLET = 35
		self.X_SIZE_TRANSIT_ONGLET = self.X_SIZE_PARCHEMIN / 3 
		self.X_POS_TRANSIT_ONGLET1 = self.X_POS_PARCHEMIN
		self.X_POS_TRANSIT_ONGLET2 = self.X_POS_TRANSIT_ONGLET1 + self.X_SIZE_TRANSIT_ONGLET
		self.X_POS_TRANSIT_ONGLET3 = self.X_POS_TRANSIT_ONGLET2 + self.X_SIZE_TRANSIT_ONGLET
		self.Y_POS_TRANSIT_ONGLET = self.Y_POS_PARCHEMIN + self.Y_SIZE_PARCHEMIN + 35 + 20
		szText = localText.changeTextColor(localText.getText("TXT_KEY_DOMESTIC_ADVISOR_STATE_GENERAL", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setText("E3TransitOngletText1", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TRANSIT_ONGLET1 + self.X_SIZE_TRANSIT_ONGLET/2, self.Y_POS_TRANSIT_ONGLET + 5, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_VOLUNTARY", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setText("E3TransitOngletText2", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TRANSIT_ONGLET2 + self.X_SIZE_TRANSIT_ONGLET/2, self.Y_POS_TRANSIT_ONGLET + 5, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_ASKED", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setText("E3TransitOngletText3", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TRANSIT_ONGLET3 + self.X_SIZE_TRANSIT_ONGLET/2, self.Y_POS_TRANSIT_ONGLET + 5, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		
		screen.setImageButton("E3TransitOngletTextShadow1", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_TRANSIT_ONGLET1, self.Y_POS_TRANSIT_ONGLET, self.X_SIZE_TRANSIT_ONGLET, self.Y_SIZE_TRANSIT_ONGLET, WidgetTypes.WIDGET_GENERAL, self.CHANGE_TRANSIT_MODE, 1)
		screen.setImageButton("E3TransitOngletTextShadow2", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_TRANSIT_ONGLET2, self.Y_POS_TRANSIT_ONGLET, self.X_SIZE_TRANSIT_ONGLET, self.Y_SIZE_TRANSIT_ONGLET, WidgetTypes.WIDGET_GENERAL, self.CHANGE_TRANSIT_MODE, 2)
		screen.setImageButton("E3TransitOngletTextShadow3", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_TRANSIT_ONGLET3, self.Y_POS_TRANSIT_ONGLET, self.X_SIZE_TRANSIT_ONGLET, self.Y_SIZE_TRANSIT_ONGLET, WidgetTypes.WIDGET_GENERAL, self.CHANGE_TRANSIT_MODE, 3)
		
		if iTransitMode == 1:
			szText = localText.changeTextColor(localText.getText("TXT_KEY_DOMESTIC_ADVISOR_STATE_GENERAL", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			screen.setText("E3TransitOngletText1", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TRANSIT_ONGLET1 + self.X_SIZE_TRANSIT_ONGLET/2, self.Y_POS_TRANSIT_ONGLET + 5, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if iTransitMode == 2:
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_VOLUNTARY", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			screen.setText("E3TransitOngletText2", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TRANSIT_ONGLET2 + self.X_SIZE_TRANSIT_ONGLET/2, self.Y_POS_TRANSIT_ONGLET + 5, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if iTransitMode == 3:
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_ASKED", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			screen.setText("E3TransitOngletText3", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TRANSIT_ONGLET3 + self.X_SIZE_TRANSIT_ONGLET/2, self.Y_POS_TRANSIT_ONGLET + 5, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
	def showCargaison(self):
		screen = self.getScreen()
		
		iUnit = self.I_SELECTED_SHIP
		player = self.pPlayer
		
		ShipPanelWidth = self.IN_PORT_PANE_WIDTH - (self.W_TEXT_MARGIN * 3 / 2)			
		ShipPanelHight = self.Y_CARGO_ICON_SIZE - 5
		yLocation_ToEurope = 0
		yLocation_FromEurope = 0
		yCenterCorrection = (self.CARGO_ICON_SIZE / 2)
		screen.addDDSGFCAt("In_Port_Box", "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_IN_PORT_BOX").getPath(), 0, 5, ShipPanelWidth, ShipPanelHight, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
		if iUnit == -1:
			screen.addDDSGFCAt("In_Port_Box_No_Selected_Ship", "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_IN_PORT_BOX_NO_SELECTED_SHIP").getPath(), 5, 10, ShipPanelWidth-10, ShipPanelHight-10, WidgetTypes.WIDGET_GENERAL, self.NO_SHIP_SELECTED, -1, False)
		else:
			screen.hide("In_Port_Box_No_Selected_Ship")
			i = 0
			for pUnitShip in self.EuropeUnitsList:
				if iUnit == i:
					break
				i += 1
			
			szText = u"<font=3>" + pUnitShip.getName() + u"</font>"
			szShipPane = self.getNextWidgetName()
			screen.attachPanelAt("LoadingList", szShipPane, "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY, 0, 0, ShipPanelWidth, ShipPanelHight, WidgetTypes.WIDGET_SHIP_CARGO, pUnitShip.getID(), -1)

			screen.addDDSGFCAt("In_Port_Box", "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_IN_PORT_BOX").getPath(), 0, 5, ShipPanelWidth, ShipPanelHight, WidgetTypes.WIDGET_ONE_SHIP, pUnitShip.getID(), player.getID(), False)
			screen.setLabelAt(self.getNextWidgetName(), szShipPane, "<font=3>" + pUnitShip.getName().upper() + "</font>", CvUtil.FONT_LEFT_JUSTIFY, (self.CARGO_SPACING / 4) + 5, (self.CARGO_SPACING / 4) + 5 + 5, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_SHIP_CARGO, pUnitShip.getID(), pUnitShip.getID())

			for i in range(pUnitShip.cargoSpace()):
				screen.addDDSGFCAt(self.getNextWidgetName(), "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_CARGO").getPath(), ((self.CARGO_SPACING * 2 / 3) * (i)) + (self.CARGO_SPACING / 4) + 5,  5 + (ShipPanelHight / 2) - (self.CARGO_ICON_SIZE / 6), self.CARGO_ICON_SIZE * 2 / 3, self.CARGO_ICON_SIZE * 2 / 3, WidgetTypes.WIDGET_SHIP_CARGO, pUnitShip.getID(), -1, False)
			
			iSpaceCargo = pUnitShip.getOnlyNewCargo()
			j = pUnitShip.cargoSpace() - 1
			while j >= 0:
				if iSpaceCargo > 0:
					screen.addDDSGFCAt(self.getNextWidgetName(), "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_CARGO_FULL").getPath(), ((self.CARGO_SPACING * 2 / 3) * (j)) + (self.CARGO_SPACING / 4) + 5,  5 + (ShipPanelHight / 2) - (self.CARGO_ICON_SIZE / 6), self.CARGO_ICON_SIZE * 2 / 3, self.CARGO_ICON_SIZE * 2 / 3, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					if iSpaceCargo < 30:
						szCargo = u"%d" %(iSpaceCargo)
					else:
						szCargo = u"30"
					screen.setLabelAt(self.getNextWidgetName(), "LoadingList", "<font=1>" + szCargo + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, ((self.CARGO_SPACING * 2 / 3) * (j)) + (self.CARGO_SPACING / 4) + 7 + 12,  5 + (ShipPanelHight / 2) - (self.CARGO_ICON_SIZE / 6) + self.CARGO_ICON_SIZE / 5, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_SHIP_CARGO, pUnitShip.getID(), pUnitShip.getID())
					szCargo = u"30"
					screen.setLabelAt(self.getNextWidgetName(), "LoadingList", "<font=1>" + szCargo + "</font>", CvUtil.FONT_LEFT_JUSTIFY, ((self.CARGO_SPACING * 2 / 3) * (j)) + (self.CARGO_SPACING / 2) + 7,  5 + (ShipPanelHight / 2) - (self.CARGO_ICON_SIZE / 6) + self.CARGO_ICON_SIZE / 2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_SHIP_CARGO, pUnitShip.getID(), pUnitShip.getID())
					iSpaceCargo -= 30
				j -= 1
			iCargoCount = 0
			plot = pUnitShip.plot()
			for i in range(plot.getNumUnits()):
				loopUnit = plot.getUnit(i)
				transportUnit = loopUnit.getTransportUnit()
				if (not transportUnit.isNone() and transportUnit.getID() == pUnitShip.getID() and transportUnit.getOwner() == pUnitShip.getOwner()):
					screen.addDragableButtonAt("LoadingList", self.getNextWidgetName(), loopUnit.getButton(), "", ((self.CARGO_SPACING * 2 / 3) * (iCargoCount)) + (self.CARGO_SPACING / 4) + 5, 5 + (ShipPanelHight / 2) - (self.CARGO_ICON_SIZE / 6), self.CARGO_ICON_SIZE * 2 / 3, self.CARGO_ICON_SIZE * 2 / 3, WidgetTypes.WIDGET_SHIP_CARGO, loopUnit.getID(), transportUnit.getID(), ButtonStyles.BUTTON_STYLE_LABEL)
					iCargoCount = iCargoCount + 1
					
			if (not pUnitShip.isFull() and player.getNumEuropeUnits() > 0):
				if gc.getUnitInfo(pUnitShip.getUnitType()).getCargoNewSpace() - pUnitShip.getNewCargo() >= 30:
					if pUnitShip.isOnlyDefensive():								
						screen.setImageButtonAt(self.getNextWidgetName(), "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_LOAD_UNIT").getPath(), ShipPanelWidth - (self.CARGO_ICON_SIZE) + 5, 0, self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, self.LOAD_ALL, pUnitShip.getID())

			if (iCargoCount > 0):
				screen.setImageButtonAt(self.getNextWidgetName(), "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_UNLOAD_UNIT").getPath(), ShipPanelWidth - (self.CARGO_ICON_SIZE) + 5, self.H_LOADING_LIST - self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, self.UNLOAD_ALL, pUnitShip.getID())
			
			if pUnitShip.isHaveFoundPack():
				screen.setImageButtonAt(self.getNextWidgetName(), "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BUILD_PACK_DOWN").getPath(), ShipPanelWidth - (self.CARGO_ICON_SIZE) * 2, self.H_LOADING_LIST - self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, self.REMOVE_BUILDER_PACK, pUnitShip.getID())
			else:
				screen.setImageButtonAt(self.getNextWidgetName(), "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BUILD_PACK_UP").getPath(), ShipPanelWidth - (self.CARGO_ICON_SIZE) * 2, self.H_LOADING_LIST - self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, self.ADD_BUILDER_PACK, pUnitShip.getID())
			
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
		screen = self.getScreen()	
		
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (inputClass.getFunctionName() == self.CIV_DROP_DOWN):				
				self.CivDropDown(inputClass)
			else:
				self.updateUnitSelected(False)
		elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
			if inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL:
				if inputClass.getData1() == self.CHANGE_MODE:
					self.changeEnrolMode(inputClass.getData2())
				elif inputClass.getData1() == self.CHANGE_TRANSIT_MODE:
					self.changeTransitMode(inputClass.getData2())
				elif (inputClass.getData1() == self.LOAD_ALL):
					self.loadAll(inputClass.getData2())
				elif (inputClass.getData1() == self.UNLOAD_ALL):
					self.unloadAll(inputClass.getData2())
				elif (inputClass.getData1() == self.ADD_BUILDER_PACK):
					self.addBuilderPack(inputClass.getData2())
				elif (inputClass.getData1() == self.REMOVE_BUILDER_PACK):
					self.removeBuilderPack(inputClass.getData2())
				elif (inputClass.getData1() == self.SHOW_SAILORS):
					self.inverseShowSailorOption()
				elif (inputClass.getData1() == self.ASK_USE_RELATION_POINTS_FOR_IMMIGRATION):
					self.askToUseRelationPointsForImmigration(inputClass.getData2())
		return 0

	def askToUseRelationPointsForImmigration(self, eUnitType):
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_ASK_USE_RELATION_POINTS_FOR_IMMIGRATION)
		popupInfo.setData1(eUnitType)
		CyInterface().addPopup(popupInfo, self.pPlayer.getID(), true, true)

	def loadAll(self, iUnitID):
		player = self.pPlayer
		transport = player.getUnit(iUnitID)
		if(transport.isNone() or transport.getUnitTravelState() != UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE) :
			return

		for i in range(player.getNumEuropeUnits()):
			loopUnit = player.getEuropeUnit(i)
			if (loopUnit.getProfession() != ProfessionTypes.PROFESSION_SAILOR and not transport.isFull()):
				CyMessageControl().sendPlayerAction(player.getID(), PlayerActionTypes.PLAYER_ACTION_LOAD_UNIT_FROM_EUROPE, loopUnit.getID(), iUnitID, -1)
		
		if(player.isSecondaryOption(SecondaryPlayerOptionTypes.SECONDARYPLAYEROPTION_SHOW_SAILORS_IN_IMMIGRATION)):
			#We load after sailors
			for i in range(player.getNumEuropeUnits()):
				loopUnit = player.getEuropeUnit(i)
				if (loopUnit.getProfession() == ProfessionTypes.PROFESSION_SAILOR and not transport.isFull()):
					CyMessageControl().sendPlayerAction(player.getID(), PlayerActionTypes.PLAYER_ACTION_LOAD_UNIT_FROM_EUROPE, loopUnit.getID(), iUnitID, -1)
	
	def unloadAll(self, iUnitID):
		player = self.pPlayer
		transport = player.getUnit(iUnitID)
		plot = transport.plot()
		if(transport.isNone() or transport.getUnitTravelState() != UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE) :
			return

		for i in range(plot.getNumUnits()):
			loopUnit = plot.getUnit(i)
			transportUnit = loopUnit.getTransportUnit()
			if (transportUnit.getID() == transport.getID() and transportUnit.getOwner() == transport.getOwner()):
				CyMessageControl().sendPlayerAction(player.getID(), PlayerActionTypes.PLAYER_ACTION_UNLOAD_UNIT_TO_EUROPE, loopUnit.getID(), -1, -1)
	
	def addBuilderPack(self, iUnitID):
		popupInfo = CyPopupInfo()
		popupInfo.setData1(iUnitID)
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_RESUPPLY_BUILDER_PACK)
		CyInterface().addPopup(popupInfo, CyGame().getActivePlayer(), true, true)

	def removeBuilderPack(self, iUnitID):
		popupInfo = CyPopupInfo()
		CyMessageControl().sendPlayerAction(self.pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_RESUPPLY_BUILDER_PACK, iUnitID, False, -1);

	def CivDropDown( self, inputClass ):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
			screen = self.getScreen()
			iIndex = screen.getSelectedPullDownID(self.CIV_DROP_DOWN)
			self.pPlayer = gc.getPlayer(screen.getPullDownData(self.CIV_DROP_DOWN, iIndex))
			self.initEuropeShipsList()
			self.updateUnitSelected(True)
			self.drawTable()

	def updateUnitSelected(self, bForced):
		screen = self.getScreen()
		pPlayer = self.pPlayer
		iRows = screen.getTableNumRows(self.TABLE_ID)
		if (not screen.isRowSelected(self.TABLE_ID, iRows) or bForced):
			bShipSelected = false
			for iRow in range(len(self.EuropeUnitsList)):
				if (screen.isRowSelected(self.TABLE_ID, iRow)):
					i = 0
					for pLoopUnit in self.EuropeUnitsList:
						if( i == iRow):
							if not pLoopUnit.isInEuropeDrydock() and pLoopUnit.hasCrew():
								bShipSelected = true
								if self.I_SELECTED_SHIP != iRow:
									self.I_SELECTED_SHIP = iRow
						i += 1
			if not bShipSelected:
				if self.I_SELECTED_SHIP != -1:
					self.I_SELECTED_SHIP = -1
		self.fillTable(true)
		self.drawContents()
		
	def replaceAllEnrolUnits(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer 
		iMode = self.iEnrolMode
		iProfession = gc.getUnitInfo(0).getDefaultProfession()
					
		if iMode == 0:
			iUnit = 0		
			for eUnitType in range(gc.getNumUnitInfos()):
				UnitInfo = gc.getUnitInfo(eUnitType)					
				if UnitInfo.getEnrolType() > 0:
					iEnrolValue =  pPlayer.getEnrolUnitType(UnitInfo.getUnitClassType())
					if iEnrolValue != 0:
						xPosEnrol = (iUnit%4)*(self.X_SIZE_ENROLEMENT - 30)/4 + 10
						yPosEnrol = (iUnit/4)*(self.CARGO_ICON_SIZE*2 - 5) + 10
						screen.setImageButtonAt(self.getNextWidgetName(), "EnrolList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_PURCHASE_BID").getPath(), xPosEnrol + self.CARGO_ICON_SIZE, yPosEnrol, 20, 20,  WidgetTypes.WIDGET_GENERAL, self.ASK_USE_RELATION_POINTS_FOR_IMMIGRATION, eUnitType)
						screen.setImageButtonAt(self.getNextWidgetName(), "EnrolList", UnitInfo.getArtInfo(0, iProfession).getFullLengthIcon(), xPosEnrol, yPosEnrol, self.CARGO_ICON_SIZE, self.Y_CARGO_ICON_SIZE, WidgetTypes.WIDGET_ENROL_UNIT_TYPE, eUnitType, pPlayer.getID())
						szText = u""
						if iEnrolValue > 0:
							szText = u"%d" %(iEnrolValue)
						if iEnrolValue == -1:
							szText = u"inf"				
						szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
						screen.setLabelAt(self.getNextWidgetName(), "EnrolList", u"<font=1>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, xPosEnrol + self.CARGO_ICON_SIZE + 1, yPosEnrol + 8, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, self.ASK_USE_RELATION_POINTS_FOR_IMMIGRATION, eUnitType)
						iUnit += 1
		else:
			iUnit = 0
			if pPlayer.getNumCities() == 0:
				return

			for eUnitType in range(gc.getNumUnitInfos()):
				UnitInfo = gc.getUnitInfo(eUnitType)
					
				if UnitInfo.getEnrolType() == iMode and (UnitInfo.getAllowEra() <= 0 or UnitInfo.getAllowEra() <= pPlayer.getNewEra()):
					
					bContinue = true
					for iYield in range(YieldTypes.NUM_YIELD_TYPES):
						if UnitInfo.getYieldModifier(iYield) > 0:
							if pPlayer.isHasYieldUnknown(iYield):
								bContinue = false
					if bContinue:
						xPosEnrol = (iUnit%4)*(self.X_SIZE_ENROLEMENT - 30)/4 + 10
						yPosEnrol = (iUnit/4)*(self.Y_CARGO_ICON_SIZE - 5) + 10
						iEnrolValue =  pPlayer.getEnrolUnitType(UnitInfo.getUnitClassType())
						if iEnrolValue != 0:
							screen.setImageButtonAt(self.getNextWidgetName(), "EnrolList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_PURCHASE_BID").getPath(), xPosEnrol + self.CARGO_ICON_SIZE, yPosEnrol, 20, 20,  WidgetTypes.WIDGET_GENERAL, self.ASK_USE_RELATION_POINTS_FOR_IMMIGRATION, eUnitType)
							szText = u""
							if iEnrolValue > 0:
								szText = u"%d" %(iEnrolValue)
							if iEnrolValue == -1:
								szText = u"inf"
							szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
							screen.setLabelAt(self.getNextWidgetName(), "EnrolList", u"<font=1>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, xPosEnrol + self.CARGO_ICON_SIZE + 3, yPosEnrol + 8, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, self.ASK_USE_RELATION_POINTS_FOR_IMMIGRATION, eUnitType)

						screen.setImageButtonAt(self.getNextWidgetName(), "EnrolList", UnitInfo.getArtInfo(0, iProfession).getFullLengthIcon(), xPosEnrol, yPosEnrol, self.CARGO_ICON_SIZE, self.Y_CARGO_ICON_SIZE, WidgetTypes.WIDGET_ENROL_UNIT_TYPE, eUnitType, pPlayer.getID())
						iUnit += 1

	def changeEnrolMode(self, iMode):
		self.iEnrolMode = iMode			
		self.drawContents()	
	
	def changeTransitMode(self, iMode):
		screen = self.getScreen()		
		
		iOldMode = self.iTransitMode
		if iMode != iOldMode:
			self.iTransitMode = iMode
			self.drawContents()
			
	def update(self, fDelta):
		screen = self.getScreen()		
		if (CyInterface().isDirty(InterfaceDirtyBits.EuropeC3Screen_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.EuropeC3Screen_DIRTY_BIT, False)
			self.drawContents()
		if (CyInterface().isDirty(InterfaceDirtyBits.EuropeC3Screen_Enrol_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.EuropeC3Screen_Enrol_DIRTY_BIT, False)
			self.iEnrolMode = 0
			self.drawContents()
		
		return		

	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList

		if eWidgetType == WidgetTypes.WIDGET_GENERAL:
			if iData1 == self.TREASURY_ID:
				return localText.getText("TXT_KEY_ECON_GOLD_RESERVE", ())
			elif iData1 == self.LOAD_ALL:
				return localText.getText("TXT_KEY_LOAD_ALL_EUROPE", ())
			elif iData1 == self.HELP_CHANGE_PROFESSION:
				return localText.getText("TXT_KEY_HELP_CHANGE_PROFESSION", ())
			elif iData1 == self.HELP_DESTINATIONCITY:
				return localText.getText("TXT_KEY_HELP_DESTINATION_CITY_BUTTON", ())
			elif iData1 == self.UNLOAD_ALL:
				return localText.getText("TXT_KEY_UNLOAD_UNITS_EUROPE", ())
			elif iData1 == self.ADD_BUILDER_PACK:
				return localText.getText("TXT_KEY_RESUPPLY_BUILDER_PACK_COMMAND", ())
			elif iData1 == self.REMOVE_BUILDER_PACK:
				return localText.getText("TXT_KEY_DELETE_BUILDER_PACK_COMMAND", ())
			elif  iData1 == self.NO_SHIP_SELECTED:
				return localText.getText("TXT_KEY_ECON_NO_SHIP_SELECTED", ())
			elif  iData1 == self.ASK_USE_RELATION_POINTS_FOR_IMMIGRATION:
				return localText.getText("TXT_KEY_EUROPE_RELATION_POINT_BUTTON_HELP", ())
			elif iData1 == self.HELP_SHIP:
				pPlayer = self.pPlayer
				pUnit = pPlayer.getUnit(iData2)
				if pUnit.isInEuropeDrydock() or not pUnit.hasCrew():
					return localText.getText("TXT_KEY_INDISPONIBLE_UNITS_EUROPE", ())
			elif iData1 == self.HELP_DESTINATION_CITY:
				return self.getHelpDestinationCity(iData2)
		return u""
		
	def getHelpDestinationCity(self, iUnitId):
		pPlayer = self.pPlayer
		pUnit = pPlayer.getEuropeUnitById(iUnitId)
		if pUnit.getDestinationCity() > 0:
			pCity = pPlayer.getCity(pUnit.getDestinationCity())
			return localText.getText("TXT_KEY_HELP_DESTINATION_CITY", (gc.getUnitInfo(pUnit.getUnitType()).getDescription().lower(), pCity.getName(), ))
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
		
		screen.addDDSGFC("EuropeScreenShipQuayImage", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_DOCK_SHIP, self.Y_POS_DOCK_SHIP, self.X_SIZE_DOCK_SHIP, self.Y_SIZE_DOCK_SHIP, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_SHIPS_QUAY", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setLabel("EuropeScreenShipQuayText", "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_DOCK_SHIP + self.X_SIZE_DOCK_SHIP/2, self.Y_POS_DOCK_SHIP + self.Y_SIZE_DOCK_SHIP/4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.addDDSGFC("EuropeScreenShipQuayFond", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_DOCK_SHIP, self.YResolution*3/20 - 2, self.X_SIZE_DOCK_SHIP, self.YResolution*5/24+5 + 4, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addTableControlGFC(self.TABLE_ID, 3, 25, self.YResolution*3/20, self.XResolution/3 - 45, self.YResolution*5/24+5, false, false, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader(self.TABLE_ID, 0, u"", (self.XResolution/3 - 45)/6) # Total graph width is 430
		screen.setTableColumnHeader(self.TABLE_ID, 1, u"", (self.XResolution/3-45)*10/17)
		screen.setStyle(self.TABLE_ID, "Table_EmptyScroll_Style")
		self.fillTable(false)
		screen.selectRow(self.TABLE_ID, 0, True)
		self.updateUnitSelected(False)
		
	def fillTable(self, bUdate):
		screen = self.getScreen()
		pPlayer = self.pPlayer
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
			if not bUdate:
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
			
			screen.setTableText(self.TABLE_ID, iColumn, iRow, u"<font=3>" + sText + u"</font>", "", WidgetTypes.WIDGET_GENERAL, self.HELP_SHIP, pLoopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
			
			iColumn += 1
			
			if not pLoopUnit.isInEuropeDrydock() and pLoopUnit.hasCrew():
				screen.setTableText(self.TABLE_ID, iColumn, iRow, u"", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_STATUT_UNIT_OPERATIVE").getPath(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			else :
				screen.setTableText(self.TABLE_ID, iColumn, iRow, u"", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_STATUT_UNIT_INOPERATIVE").getPath(), WidgetTypes.WIDGET_GENERAL, self.HELP_SHIP, pLoopUnit.getID(), CvUtil.FONT_CENTER_JUSTIFY)
		
		while iRow < 4 and not bUdate:
			iRow += 1
			screen.appendTableRow(self.TABLE_ID)
			screen.setTableRowHeight(self.TABLE_ID, iRow, self.YResolution*5/96)
	
	def initEuropeShipsList(self) :
		self.EuropeUnitsList = []
		pPlayer = self.pPlayer

		EuropeGroupsList = []
		pGroup, Iterator = pPlayer.firstSelectionGroup(false)
		while (pGroup != None):
			iSpace = pGroup.getCargoSpace(False)
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
					if pShip.canTradeInEurope(False, False):
						UnitsOfGroupsList.append((pShip.cargoSpace(), pShip))
				if len(UnitsOfGroupsList) > 0:
					UnitsOfGroupsList.sort()
					UnitsOfGroupsList.reverse()
					for iOrderUnit in range(len(UnitsOfGroupsList)):
						pOrderUnit = UnitsOfGroupsList[iOrderUnit][1]
						self.EuropeUnitsList.append(pOrderUnit)