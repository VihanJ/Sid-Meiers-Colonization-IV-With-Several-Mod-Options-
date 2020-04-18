## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

##########################################################################################################
########## Europe Screen 0: Initial Europe Screen ########################################################
##########################################################################################################

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvMainInterface

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

m_pCurrentUnit = -1

class CvEuropeC0Screen:

	def __init__(self):
		self.WIDGET_ID = "EuropeScreenWidget"
		self.CIV_DROP_DOWN = "CivDropDown"
		
		self.EDIT_SEAWAY_NAME = 2

		self.nWidgetCount = 0
		self.EUROPE_ID = -2

		self.UNIT_BUTTON_ID = 1
		self.UNIT_CARGO_BUTTON_ID = 2
		self.BUY_YIELD_BUTTON_ID = 3
		self.YIELD_CARGO_BUTTON_ID = 4
		self.COME_BACK_INTO_EUROPE = 5
		self.DOCK_BUTTON_ID = 6
		self.SAIL_TO_NEW_WORLD = 7
		self.HELP_CROSS_RATE = 10
		self.TREASURY_ID = 11
		self.EJECT_UNIT_TO_GROUP = 12
		######################
		#### SEAWAY START ####
		######################
		self.VIEW_SEAWAYS = 13
		self.EXIT_VIEW_SEAWAYS = 14	
		self.NO_SEAWAYS = 15
		self.CHOOSE_SEAWAY = 16
		self.REMOVE_SEAWAY = 17
		self.RENAME_SEAWAY = 18
		self.CHANGE_SEAWAY_PAGE = 19
		######################
		##### SEAWAY END #####
		######################

		self.CHOOSE_TRADE_ROUTE = 20
		self.STOP_TRADE_ROUTE = 21
		self.REPAIR_SHIP = 22
		
		self.Z_BACKGROUND = -2.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		
		self.selectedPlayerList = []
		
	def getScreen(self):
		return CyGInterfaceScreen("EuropeScreen", CvScreenEnums.EUROPE_SCREEN)

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
		
		self.INTERFACE_EUROPE_IN_PORT_BOX_SQUARE_GRAY = ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_IN_PORT_BOX_SQUARE_GRAY").getPath()
		self.INTERFACE_EUROPE_IN_PORT_BOX_SQUARE = ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_IN_PORT_BOX_SQUARE").getPath()
		self.INTERFACE_EUROPE_BOX_CARGO = ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_CARGO").getPath()
		self.INTERFACE_EUROPE_BOX_CARGO_FULL = ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_CARGO_FULL").getPath()
		self.INTERFACE_TRADE_ROUTES_BUTTON = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_BUTTON").getPath()
		self.INTERFACE_STOP_TRADE_ROUTES_BUTTON = ArtFileMgr.getInterfaceArtInfo("INTERFACE_STOP_TRADE_ROUTES_BUTTON").getPath()
		self.INTERFACE_EJECT_UNIT_TO_GROUP = ArtFileMgr.getInterfaceArtInfo("INTERFACE_EJECT_UNIT_TO_GROUP").getPath()
		self.INTERFACE_WHICH_SEAWAYS = ArtFileMgr.getInterfaceArtInfo("INTERFACE_WHICH_SEAWAYS").getPath()
		self.INTERFACE_NO_WHICH_SEAWAYS = ArtFileMgr.getInterfaceArtInfo("INTERFACE_NO_WHICH_SEAWAYS").getPath()
		self.INTERFACE_EUROPE_SAIL = ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SAIL").getPath()
		self.INTERFACE_GENERAL_AFFECT_TRADE_ROUTE = ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_AFFECT_TRADE_ROUTE").getPath()
		self.INTERFACE_REPAIR_SHIP = ArtFileMgr.getInterfaceArtInfo("INTERFACE_REPAIR_SHIP").getPath()

		self.COLOR_FONT_CREAM = gc.getInfoTypeForString("COLOR_FONT_CREAM")
		self.COLOR_RED = gc.getInfoTypeForString("COLOR_RED")
		self.COLOR_ORANGE = gc.getInfoTypeForString("COLOR_PLAYER_ORANGE")
		self.COLOR_YELLOW = gc.getInfoTypeForString("COLOR_YELLOW")

		self.XResolution = screen.getXResolution()
		self.YResolution = screen.getYResolution()
		self.W_SCREEN = screen.getXResolution()
		self.H_SCREEN = screen.getYResolution()

		self.Y_EXIT = self.YResolution - 36
		self.X_EXIT = self.XResolution - 30
		
		self.Y_RATES = (self.YResolution - 55) * 36 / 40

		self.IN_PORT_PANE_WIDTH = self.XResolution * 9 / 20
		self.X_IN_PORT = self.XResolution * 3 / 10
		self.PANE_HEIGHT = (self.YResolution - 120)
		self.X_DOCK = self.XResolution * 7 / 10

		
		self.SHIP_ICON_SIZE = self.YResolution / 14
		self.CARGO_ICON_SIZE = self.XResolution / 25
		self.CARGO_SPACING  = self.CARGO_ICON_SIZE + 2
		self.ICON_ON_SHIP = self.YResolution * 38 / 768;

		self.H_TEXT_MARGIN = self.YResolution / 30
		self.W_TEXT_MARGIN = self.XResolution / 30

		self.Y_PANEL_MARGIN = self.ySize(15)
		self.X_PANEL_MARGIN = self.xSize(10)
		self.X_OUTSIDE_PANEL_MARGIN = self.xSize(30)
		self.Y_OUTSIDE_PANEL_MARGIN = self.ySize(20)

		self.Y_CARGO_MARGIN = self.ySize(10)
		self.X_CARGO_MARGIN = self.xSize(3)
		self.X_OUTSIDE_CARGO_MARGIN = self.xSize(5)

		self.X_OUTSIDE_TOP_OPTION_BUTTON_MARGIN = 0
		self.X_TOP_OPTION_BUTTON_MARGIN = self.xSize(-7)
		self.Y_OUTSIDE_TOP_OPTION_BUTTON_MARGIN = self.ySize(15)
		self.TOP_OPTION_BUTTON_SIZE = self.minSize(30)

		self.OPERATIONAL_SHIP_ICON_SIZE = self.minSize(73)

		self.X_SHIPS_COUNTER_MARGIN = self.xSize(5)
		self.Y_SHIPS_COUNTER_MARGIN = self.ySize(17)

		self.X_OUTSIDE_SHIP_STATISTICS_TEXT_MARGIN = self.xSize(6)
		self.Y_SHIP_STATISTICS_TEXT_MARGIN = self.ySize(14)

		self.X_OUTSIDE_SHIP_PROMOTION_MARGIN = self.xSize(3)
		self.X_SHIP_PROMOTION_MARGIN = self.xSize(1)
		self.Y_SHIP_PROMOTION_MARGIN = self.ySize(1)

		self.X_NON_OPERATIONAL = self.X_IN_PORT + self.IN_PORT_PANE_WIDTH - 10
		self.X_SIZE_NON_OPERATIONAL = self.XResolution * 5 / 20
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

		self.COME_BACK_BTN_SIZE = 36 * self.XResolution / 1024

		self.NUM_PROMOTIONS_BY_ROW = 2
		self.MAX_PROMOTIONS_ROWS = 3
		self.PROMOTION_PICTURE_SIZE = self.minSize(14)
		

		######################
		#### SEAWAY START ####
		######################
		
		self.CURRENT_SEAWAY_PAGE = 0 # The current page of seaways book
		self.NUM_SEAWAYS_BY_PAGE = 10 # Number of seaways by page

		self.CHOOSE_SEAWAY_VIEW = False # Allow to know if we have to show the seaway view
		self.printedSeawaysList = [] # Allow to remove all the seaways name when we change pages

		self.currentSeawayPos = -1
		
		######################
		##### SEAWAY END #####
		######################
		
		# Set the background and exit button, and show the screen
		screen.setDimensions(0, 0, self.XResolution, self.YResolution)
		screen.showWindowBackground(False)
		
		screen.addDDSGFC("EuropeScreenUp", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BANDEAU_MARRON").getPath(), 0, 0, self.XResolution, 40, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("EuropeScreenDown", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BANDEAU_MARRON").getPath(), 0, self.YResolution - 86, self.XResolution, 86, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addDDSGFC("EuropeScreenBackground", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BACKGROUND_CAPITAINERIE").getPath(), 0, 40, self.XResolution, self.YResolution - 86, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("TopPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TITLE").getPath(), 0, 0, self.XResolution, 55, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Header...
		screen.setLabel("EuropeScreenWidgetHeader", "Background", u"<font=4b>" + localText.getText("TXT_KEY_EUROPE_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.XResolution / 2, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		#init panels name
		self.operationalFleetsPanelName = "OperationalFleetsPanelName"
		
		# InBound
		screen.addDDSGFC("EuropeScreenInboundImage", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), - self.W_TEXT_MARGIN, self.Y_UPPER_EDGE, self.PANE_WIDTH, (self.PANE_HEIGHT - self.H_TEXT_MARGIN) / 2, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		szText = localText.changeTextColor(localText.getText("TXT_KEY_IN_BOUND", ()).upper(), self.COLOR_FONT_CREAM)
		screen.setLabel("EuropeScreenInboundText", "Background",  u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, (self.PANE_WIDTH * 3 / 7), self.Y_UPPER_EDGE - (self.H_TEXT_MARGIN / 2), 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addScrollPanel("InBoundList", u"", self.W_TEXT_MARGIN / 2, self.Y_UPPER_EDGE + self.H_TEXT_MARGIN - 10, self.W_SLIDER + self.COME_BACK_BTN_SIZE/2, ((self.PANE_HEIGHT - self.H_TEXT_MARGIN) / 2) - (self.H_TEXT_MARGIN * 3) + 20, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# OutBound
		screen.addDDSGFC("EuropeScreenOutboundImage", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), - self.W_TEXT_MARGIN, self.Y_BOUND, self.PANE_WIDTH, (self.PANE_HEIGHT - self.H_TEXT_MARGIN) / 2, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		szText = localText.changeTextColor(localText.getText("TXT_KEY_OUTBOUND", ()).upper(), self.COLOR_FONT_CREAM)
		screen.setLabel("EuropeScreenOutboundText", "Background",  u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, (self.PANE_WIDTH * 3 / 7), self.Y_BOUND - (self.H_TEXT_MARGIN / 2), 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, self.SAIL_TO_NEW_WORLD, -1 )
		screen.addScrollPanel("OutBoundList", u"", self.W_TEXT_MARGIN / 2, self.Y_BOUND + self.H_TEXT_MARGIN , self.W_SLIDER + self.COME_BACK_BTN_SIZE/2, ((self.PANE_HEIGHT - self.H_TEXT_MARGIN) / 2) - (self.H_TEXT_MARGIN * 3) + 20, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_SAIL, UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE, -1 )

		# In Port
		screen.addDDSGFC("EuropeScreenPortImage", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_IN_PORT, self.Y_UPPER_EDGE, self.IN_PORT_PANE_WIDTH, self.PANE_HEIGHT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		szText = localText.changeTextColor(localText.getText("TXT_KEY_IN_PORT", ()).upper(), self.COLOR_FONT_CREAM)
		screen.setLabel("EuropeScreenPortText", "Background",  u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_IN_PORT + (self.IN_PORT_PANE_WIDTH / 2), self.Y_UPPER_EDGE - (self.H_TEXT_MARGIN / 2), 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addScrollPanel(self.operationalFleetsPanelName, u"", self.X_IN_PORT, self.Y_UPPER_EDGE + 10, self.IN_PORT_PANE_WIDTH, self.PANE_HEIGHT - (self.H_TEXT_MARGIN * 3) + 20, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_MOVE_CARGO_TO_TRANSPORT, -1, -1 )
		
		# non-operational
		screen.addDDSGFC("EuropeScreenNonOperationalImage", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_NON_OPERATIONAL, self.Y_UPPER_EDGE, self.X_SIZE_NON_OPERATIONAL, self.PANE_HEIGHT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		szText = localText.changeTextColor(localText.getText("TXT_KEY_NON_OPERATIONAL", ()).upper(), self.COLOR_FONT_CREAM)
		screen.setLabel("EuropeScreenNonOperationalText", "Background",  u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_NON_OPERATIONAL + (self.X_SIZE_NON_OPERATIONAL / 2), self.Y_UPPER_EDGE - (self.H_TEXT_MARGIN / 2), 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addScrollPanel("NonOperationalList", u"", self.X_NON_OPERATIONAL + self.W_TEXT_MARGIN, self.Y_UPPER_EDGE - 10, self.X_SIZE_NON_OPERATIONAL - (self.W_TEXT_MARGIN * 3 / 2), self.PANE_HEIGHT - (self.H_TEXT_MARGIN * 3) + 45, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		#Seaway Panel
		screen.addPanel("EmptySeawayPanel", u"", u"", True, False, 0, 0, self.XResolution, self.YResolution, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)		
		screen.addDrawControl("SeawayPanel",  ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SEAWAY_BOX").getPath(), self.XResolution / 2 - 360, self.YResolution / 6, 720, 480, WidgetTypes.WIDGET_GENERAL, -1, -1)		

		self.drawTabs()
		self.setTab(0, True)

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
		# draw the contents
		self.drawContents()
		
		# MINIMAP INITIALIZATION
		screen.initMinimap(self.XResolution / 2 - 280, self.XResolution / 2 - 70, self.YResolution/6 + 115, self.YResolution/6 + 395, self.Z_CONTROLS, false )
		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_MILITARY)
		
		CvMainInterface.CvMainInterface().appendtoHideState(screen, "_FXS_Screen_Bogus_Minimap_Name", CvMainInterface.HIDE_TYPE_MAP, CvMainInterface.HIDE_LEVEL_ALL)
		CvMainInterface.CvMainInterface().appendtoHideState(screen, "_FXS_Screen_Bogus_Minimap_Name", CvMainInterface.HIDE_TYPE_CITY, CvMainInterface.HIDE_LEVEL_ALL)
		CvMainInterface.CvMainInterface().appendtoHideState(screen, "_FXS_Screen_Bogus_Minimap_Name", CvMainInterface.HIDE_TYPE_GLOBAL, CvMainInterface.HIDE_LEVEL_ALL)
		
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
			TabText = localText.changeTextColor(TabText, self.COLOR_FONT_CREAM)

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

	def showEuropeIcons(self):
		screen = self.getScreen()
		iSize = 40
		xPosBtn = self.X_IN_PORT + self.IN_PORT_PANE_WIDTH - iSize*4
		yPosBtn =  self.Y_UPPER_EDGE - iSize/2		
		
		if not self.pPlayer.mustShowIconInfo(1):
			screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_WARNING_SHIP").getPath(), xPosBtn, yPosBtn, iSize, iSize, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_EUROPE_C1_SCREEN).getActionInfoIndex(), 3 )
		else :
			screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_WARNING_HIGHLIGHT_SHIP").getPath(), xPosBtn, yPosBtn, iSize, iSize, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_EUROPE_C1_SCREEN).getActionInfoIndex(), 4 )
		
		xPosBtn += iSize
		if not self.pPlayer.mustShowIconInfo(2):
			screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_WARNING_TRADE").getPath(), xPosBtn, yPosBtn, iSize, iSize, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_EUROPE_C2_SCREEN).getActionInfoIndex(), 5 )
		else :
			screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_WARNING_HIGHLIGHT_TRADE").getPath(), xPosBtn, yPosBtn, iSize, iSize, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_EUROPE_C2_SCREEN).getActionInfoIndex(), 6 )
		
		xPosBtn += iSize
		if not self.pPlayer.mustShowIconInfo(3):
			screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_WARNING_IMMIGRATION").getPath(), xPosBtn, yPosBtn, iSize, iSize, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_EUROPE_C3_SCREEN).getActionInfoIndex(), 7 )
		else :
			screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_WARNING_HIGHLIGHT_IMMIGRATION").getPath(), xPosBtn, yPosBtn, iSize, iSize, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_EUROPE_C3_SCREEN).getActionInfoIndex(), 8 )
		
			
	def drawContents(self):
	
		player = self.pPlayer
		playerEurope = gc.getPlayer(player.getParent())

		self.deleteAllWidgets()

		screen = self.getScreen()
		self.IN_PORT_PANE_WIDTH = self.XResolution * 9 / 20
		
		self.UnorderEuropeUnitsList = []
		InNonOperationalList = []
		InboundUnitsList = []
		OutboundUnitsList = []

		self.showEuropeIcons()

		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_TREASURY", (player.getGold(), )).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.W_TEXT_MARGIN, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.TREASURY_ID, -1 )

		sizeIcon = self.ICON_ON_SHIP * 2 / 3
		
		iSize = 40
		xPosBtn = self.X_IN_PORT + self.IN_PORT_PANE_WIDTH - iSize*4
		yPosBtn =  self.Y_UPPER_EDGE - iSize/2
		if (player.getNumSeaways() > 0):
			szName = self.getNextWidgetName()
			screen.setImageButton(szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_WHICH_SEAWAYS").getPath(), self.X_IN_PORT + self.IN_PORT_PANE_WIDTH*1/20, yPosBtn, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.VIEW_SEAWAYS, -1)
			screen.overlayButtonGFC(szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath())
		else:
			screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_NO_WHICH_SEAWAYS").getPath(), self.X_IN_PORT + self.IN_PORT_PANE_WIDTH*1/20, yPosBtn, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.NO_SEAWAYS, -1)
		
		(unit, iter) = player.firstUnit()
		while (unit):
			if (not unit.isCargo() and not unit.isDelayedDeath() and gc.getUnitInfo(unit.getUnitType()).isMechUnit()):
				pGroup = unit.getGroup()
				isInGroup = pGroup.getMostPowerfulUnit().getID() == unit.getID()
				if (unit.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE):
					if unit.getShipSellPrice() == 0 and not unit.isInEuropeDrydock() and unit.hasCrew() and (not unit.isAutomated() or not pGroup.isHurt()):
						if isInGroup:
							self.UnorderEuropeUnitsList.append(unit)
					else:
						InNonOperationalList.append(unit)
				elif (unit.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_TO_EUROPE):
					if isInGroup:
						InboundUnitsList.append(unit)
				if (unit.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE):
					if isInGroup:
						OutboundUnitsList.append(unit)
			
			(unit, iter) = player.nextUnit(iter)

		self.displayOperationalFleetsInEurope()
		
		ShipPanelHight = self.YResolution / 12
		ShipPanelWidth = (self.IN_PORT_PANE_WIDTH - (self.W_TEXT_MARGIN * 3))/2		

		# ********************** InNonOperationalList ************************
		iNumShip = 0		
		yDecal = 60
		pictureSize = 50
		for unit in InNonOperationalList:			
			pGroup = unit.getGroup()
			screen.setImageButtonAt(self.getNextWidgetName(), "NonOperationalList", player.getUnitButton(unit.getUnitType()), 0, yDecal*(iNumShip+1) + (ShipPanelHight / 9), pictureSize, pictureSize, WidgetTypes.WIDGET_NON_OPERATIONAL_SHIP, unit.getID(), unit.getID())
			screen.setLabelAt(self.getNextWidgetName(), "NonOperationalList", "<font=3>" + unit.getName() + "</font>", CvUtil.FONT_LEFT_JUSTIFY, pictureSize + 5, yDecal*(iNumShip+1) + (ShipPanelHight / 9) + pictureSize/5, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_NON_OPERATIONAL_SHIP, unit.getID(), unit.getID())
			if unit.getShipSellPrice() > 0:
				screen.setLabelAt(self.getNextWidgetName(), "NonOperationalList", "<font=2>" + localText.getText("TXT_KEY_UNIT_HELP_ON_SALE", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, pictureSize + 5, yDecal*(iNumShip+1) + (ShipPanelHight / 9) + pictureSize*3/5, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_NON_OPERATIONAL_SHIP, unit.getID(), unit.getID())
			elif unit.isInEuropeDrydock() or (unit.isAutomated() and pGroup != None and pGroup.isHurt()):
				iTurn = unit.healTurns()
				if iTurn > 0:
					screen.setLabelAt(self.getNextWidgetName(), "NonOperationalList", "<font=2>" + localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_STATUS_DRY_DOCK_START", ()), self.COLOR_RED) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, pictureSize + 5, yDecal*(iNumShip+1) + (ShipPanelHight / 9) + pictureSize*3/5 -4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_NON_OPERATIONAL_SHIP, unit.getID(), unit.getID())
					screen.setLabelAt(self.getNextWidgetName(), "NonOperationalList", "<font=2>" + localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_STATUS_DRY_DOCK_END", (iTurn, )), self.COLOR_RED) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, pictureSize + 5, yDecal*(iNumShip+1) + (ShipPanelHight / 9) + pictureSize*4/5, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_NON_OPERATIONAL_SHIP, unit.getID(), unit.getID())
				else :
					screen.setLabelAt(self.getNextWidgetName(), "NonOperationalList", "<font=2>" + localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_STATUS_DRY_DOCK_START_REPAIRED", ()), gc.getInfoTypeForString("COLOR_CYAN")) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, pictureSize + 5, yDecal*(iNumShip+1) + (ShipPanelHight / 9) + pictureSize*3/5 -4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_NON_OPERATIONAL_SHIP, unit.getID(), unit.getID())
			elif not unit.hasCrew():
				screen.setLabelAt(self.getNextWidgetName(), "NonOperationalList", "<font=2>" + localText.getText("TXT_KEY_UNIT_HELP_IS_NOT_EQUIPED_SAILOR", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, pictureSize + 5, yDecal*(iNumShip+1) + (ShipPanelHight / 9) + pictureSize*3/5, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_NON_OPERATIONAL_SHIP, unit.getID(), unit.getID())
			
			iNumShip += 1
		

		yLocation_ToEurope = 0
		yLocation_FromEurope = 0

		# ********************** InboundUnitsList ************************
		for unit in InboundUnitsList:		
			szText = localText.getText("TXT_KEY_ARRIVALS_IN", (unit.getName(), unit.getUnitTravelTimer()))
			pGroup = unit.getGroup()
			screen.addDDSGFCAt(self.getNextWidgetName(), "InBoundList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_IN_BOUND_BOX").getPath(), 0, yLocation_ToEurope + (self.SHIP_ICON_SIZE / 3), self.W_SLIDER - self.W_TEXT_MARGIN, self.SHIP_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
			screen.setLabelAt( self.getNextWidgetName(), "InBoundList", "<font=1>" + unit.getName() + " : " + szText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, 20 , yLocation_ToEurope + ShipPanelHight, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

			if not pGroup.isNone() and pGroup.getMostPowerfulUnit().getID() == unit.getID() and pGroup.getNumUnits() > 1:
				szText = u"x%d" %(pGroup.getNumUnits())
				szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_YELLOW"))
				screen.setLabelAt( self.getNextWidgetName(), "InBoundList", "<font=4b>" + szText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, ShipPanelWidth*4/5 + 3, yLocation_ToEurope + ShipPanelHight/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
			for i in range(unit.cargoSpace()):
				screen.addDDSGFCAt(self.getNextWidgetName(), "InBoundList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_CARGO").getPath(), (self.W_TEXT_MARGIN / 2) + ((self.CARGO_SPACING / 2) * (i)), yLocation_ToEurope + (self.SHIP_ICON_SIZE / 3) + (self.SHIP_ICON_SIZE / 2) - (self.CARGO_ICON_SIZE/4), self.CARGO_ICON_SIZE / 2, self.CARGO_ICON_SIZE / 2, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

			iSpaceCargo = unit.getOnlyNewCargo()
			j = unit.cargoSpace() - 1
			while j >= 0:
				if iSpaceCargo > 0:
					screen.addDDSGFCAt(self.getNextWidgetName(), "InBoundList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_CARGO_FULL_ONLY").getPath(), (self.W_TEXT_MARGIN / 2) + ((self.CARGO_SPACING / 2) * (j)), yLocation_ToEurope + (self.SHIP_ICON_SIZE / 3) + (self.SHIP_ICON_SIZE / 2) - (self.CARGO_ICON_SIZE/4), self.CARGO_ICON_SIZE / 2, self.CARGO_ICON_SIZE / 2, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					iSpaceCargo -= 30
				j -= 1
			
			screen.addDDSGFCAt(self.getNextWidgetName(), "InBoundList", unit.getFullLengthReverseIcon(), self.W_SLIDER - (self.W_TEXT_MARGIN * 2) - self.SHIP_ICON_SIZE, yLocation_ToEurope - (self.SHIP_ICON_SIZE / 12), self.SHIP_ICON_SIZE * 4 / 3, self.SHIP_ICON_SIZE * 4 / 3, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
			screen.setImageButtonAt(self.getNextWidgetName(), "InBoundList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_TRANSFERT_INVISIBLE").getPath(),  0, yLocation_ToEurope + (self.SHIP_ICON_SIZE / 3), self.W_SLIDER - self.W_TEXT_MARGIN, self.SHIP_ICON_SIZE, WidgetTypes.WIDGET_GROUP_SHIP, unit.getID(), player.getID())
			
			# We display contents of ship afer INTERFACE_EUROPE_ICON_TRANSFERT_INVISIBLE to let them have help texts
			
			iCargoCount = 0
			plot = unit.plot()
			for i in range(plot.getNumUnits()):
				loopUnit = plot.getUnit(i)
				transportUnit = loopUnit.getTransportUnit()
				if (not transportUnit.isNone() and transportUnit.getID() == unit.getID() and transportUnit.getOwner() == unit.getOwner()):
					screen.setImageButtonAt( self.getNextWidgetName(), "InBoundList", loopUnit.getButton(),  (self.W_TEXT_MARGIN / 2) + ((self.CARGO_SPACING / 2) * (iCargoCount)), yLocation_ToEurope + (self.SHIP_ICON_SIZE / 3) + (self.SHIP_ICON_SIZE / 2) - (self.CARGO_ICON_SIZE / 4), self.CARGO_ICON_SIZE / 2, self.CARGO_ICON_SIZE / 2, WidgetTypes.WIDGET_SHIP_CARGO, loopUnit.getID(), -1)
					iCargoCount += 1

			if unit.isAutomated():
				screen.setImageButtonAt(self.getNextWidgetName(), "InBoundList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_BUTTON").getPath(), 5, yLocation_ToEurope, self.ICON_ON_SHIP, self.ICON_ON_SHIP, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TRADE_ROUTE_SCREEN).getActionInfoIndex(), pGroup.getID())
			yLocation_ToEurope += ShipPanelHight

		# ********************** OutboundUnitsList ************************
		for unit in OutboundUnitsList:
			szText = localText.getText("TXT_KEY_ARRIVALS_IN", (unit.getName(), unit.getUnitTravelTimer()))

			pGroup = unit.getGroup()
			widgetType = WidgetTypes.WIDGET_GROUP_SHIP
			
			screen.addDDSGFCAt(self.getNextWidgetName(), "OutBoundList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_OUT_BOUND_BOX").getPath(), 0, yLocation_FromEurope + (self.SHIP_ICON_SIZE / 3), self.W_SLIDER - self.W_TEXT_MARGIN, self.SHIP_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
			screen.setLabelAt(self.getNextWidgetName(), "OutBoundList", "<font=1>" + unit.getName() + " : " + szText + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.W_SLIDER - self.W_TEXT_MARGIN - 10, yLocation_FromEurope + ShipPanelHight, -0.1, FontTypes.SMALL_FONT,  WidgetTypes.WIDGET_GENERAL, -1, -1)

			if not pGroup.isNone() and pGroup.getMostPowerfulUnit().getID() == unit.getID() and pGroup.getNumUnits() > 1:
				szText = u"x%d" %(pGroup.getNumUnits())
				szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_YELLOW"))
				screen.setLabelAt( self.getNextWidgetName(), "OutBoundList", "<font=4b>" + szText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, ShipPanelWidth/2 - 3, yLocation_FromEurope + ShipPanelHight/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
	
			for i in range(unit.cargoSpace()):
				screen.addDDSGFCAt(self.getNextWidgetName(), "OutBoundList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_CARGO").getPath(), self.W_SLIDER - (self.W_TEXT_MARGIN * 2) - ((self.CARGO_SPACING / 2) * (i)), yLocation_FromEurope + (self.SHIP_ICON_SIZE / 3) + (self.SHIP_ICON_SIZE / 2) - (self.CARGO_ICON_SIZE/4), self.CARGO_ICON_SIZE / 2, self.CARGO_ICON_SIZE / 2, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

			iSpaceCargo = unit.getOnlyNewCargo()
			j = 0
			while j < unit.cargoSpace():
				if iSpaceCargo > 0:
					screen.addDDSGFCAt(self.getNextWidgetName(), "OutBoundList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_CARGO_FULL_ONLY").getPath(), self.W_SLIDER - (self.W_TEXT_MARGIN * 2) - ((self.CARGO_SPACING / 2) * (j)), yLocation_FromEurope + (self.SHIP_ICON_SIZE / 3) + (self.SHIP_ICON_SIZE / 2) - (self.CARGO_ICON_SIZE/4), self.CARGO_ICON_SIZE / 2, self.CARGO_ICON_SIZE / 2,  WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					iSpaceCargo -= 30
				j += 1
			
			screen.addDDSGFCAt( self.getNextWidgetName(), "OutBoundList", unit.getFullLengthIcon(), 10, yLocation_FromEurope - (self.SHIP_ICON_SIZE / 12), self.SHIP_ICON_SIZE * 4 / 3, self.SHIP_ICON_SIZE * 4 / 3, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
			screen.setImageButtonAt(self.getNextWidgetName(), "OutBoundList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_TRANSFERT_INVISIBLE").getPath(), 0, yLocation_FromEurope + (self.SHIP_ICON_SIZE / 3), self.W_SLIDER - self.W_TEXT_MARGIN, self.SHIP_ICON_SIZE, WidgetTypes.WIDGET_GROUP_SHIP, unit.getID(), player.getID())
			
			# We display contents of ship afer INTERFACE_EUROPE_ICON_TRANSFERT_INVISIBLE to let them have help texts
			
			iCargoCount = unit.cargoSpace() - 1
			plot = unit.plot()
			for i in range(plot.getNumUnits()):
				loopUnit = plot.getUnit(i)
				transportUnit = loopUnit.getTransportUnit()
				if (not transportUnit.isNone() and transportUnit.getID() == unit.getID() and transportUnit.getOwner() == unit.getOwner()):
					screen.setImageButtonAt( self.getNextWidgetName(), "OutBoundList", loopUnit.getButton(), self.W_SLIDER - (self.W_TEXT_MARGIN * 2) - ((self.CARGO_SPACING / 2) * iCargoCount), yLocation_FromEurope + (self.SHIP_ICON_SIZE / 3) + (self.SHIP_ICON_SIZE / 2) - (self.CARGO_ICON_SIZE / 4), self.CARGO_ICON_SIZE / 2, self.CARGO_ICON_SIZE / 2, WidgetTypes.WIDGET_SHIP_CARGO, loopUnit.getID(), -1)
					iCargoCount -= 1

			if unit.canComeBackInToEurope():
				screen.setImageButtonAt( self.getNextWidgetName(), "OutBoundList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_COME_BACK_INTO_EUROPE").getPath(), self.W_SLIDER - self.W_TEXT_MARGIN - self.COME_BACK_BTN_SIZE/2, yLocation_FromEurope + (self.SHIP_ICON_SIZE/2), self.COME_BACK_BTN_SIZE, self.COME_BACK_BTN_SIZE, WidgetTypes.WIDGET_GENERAL, self.COME_BACK_INTO_EUROPE, unit.getID())
			if unit.isAutomated():
				screen.setImageButtonAt(self.getNextWidgetName(), "OutBoundList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_BUTTON").getPath(), self.W_SLIDER - self.W_TEXT_MARGIN - self.ICON_ON_SHIP, yLocation_FromEurope, self.ICON_ON_SHIP, self.ICON_ON_SHIP, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TRADE_ROUTE_SCREEN).getActionInfoIndex(), pGroup.getID())
			
			yLocation_FromEurope += ShipPanelHight

		self.updateSeawaysView()
		
		return 0

	def displayOperationalFleetsInEurope(self):
		screen = self.getScreen()
		player = self.pPlayer

		self.orderEuropeUnitsList()
		fleetCount = len(self.EuropeUnitsList)
		fleetByRow = 3

		# Initialize the size of the box for each unit. Width + Height
		minShipPanelHeight = 60
		self.wFleetPanel = self.calculateFleetPanelWidth(fleetByRow)
		self.hFleetPanel = max(self.wFleetPanel, minShipPanelHeight)

		for index in range(fleetCount): 
			# Init ship specific variables
			pShip = self.EuropeUnitsList[index]
			pGroup = pShip.getGroup()
			widgetType = self.getFleetWidgetType(pGroup)
			shipPanelName = self.getNextWidgetName()

			# Set the ship panel
			xPosition, yPosition = self.getTopLeftPositionOfShipPanel(index, fleetByRow, self.wFleetPanel, self.hFleetPanel)
			screen.attachPanelAt(self.operationalFleetsPanelName, shipPanelName, "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY, xPosition, yPosition, self.wFleetPanel, self.hFleetPanel, widgetType, pShip.getID(), player.getID())
			
			# Set the box square
			artBoxSquare = self.getArtBoxSquare(pShip)
			screen.addDDSGFCAt(self.getNextWidgetName(), self.operationalFleetsPanelName, artBoxSquare, xPosition, yPosition, self.wFleetPanel, self.hFleetPanel, widgetType, pShip.getID(), player.getID(), False)
			
			# Display ship icon
			screen.addDragableButtonAt(self.operationalFleetsPanelName, self.getNextWidgetName(), pShip.getFullLengthIcon(), "", xPosition, yPosition, self.OPERATIONAL_SHIP_ICON_SIZE, self.OPERATIONAL_SHIP_ICON_SIZE, widgetType, pShip.getID(), player.getID(), ButtonStyles.BUTTON_STYLE_LABEL)
			
			# Set the top option buttons
			self.diplayTheShipTopOptionButtons(pShip, xPosition, yPosition)

			# Display the ships count in the fleet
			self.diplayTheShipsCountInTheFleet(pShip, shipPanelName, widgetType)

			# Display ship name
			xTextInfoPos, yTextInfoPos = self.calculateShipStatisticsTextPosition(1)
			screen.setLabelAt(self.getNextWidgetName(), shipPanelName, u"<font=1b>" +  self.getShipName(pShip) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xTextInfoPos, yTextInfoPos, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

			if self.shouldDisplayShipCargo(pShip):
				self.displayShipCargo(pShip, xPosition, yPosition, widgetType)
			else:
				self.displayMilitaryStatistics(pShip, shipPanelName)
				self.displayShipPromotions(pShip, shipPanelName)

	def diplayTheShipsCountInTheFleet(self, pShip, shipPanelName, widgetType):
		screen = self.getScreen()
		player = self.pPlayer

		if self.isFleet(pShip):
			pGroup = pShip.getGroup()
			szText = u"x%d" %(pGroup.getNumUnits())
			szText = self.applyColorIfRequired(pShip, szText)
			szText = localText.changeTextColor(szText, self.COLOR_YELLOW) # This command don't erase the text color if it was already set. Like in applyColorIfRequired method
			xCounterPosition, yCounterPosition = self.calculateShipsCounterPosition()

			screen.setLabelAt( self.getNextWidgetName(), shipPanelName, "<font=3b>" + szText + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, xCounterPosition, yCounterPosition, -0.1, FontTypes.SMALL_FONT, widgetType, pShip.getID(), player.getID())
	
	def calculateShipsCounterPosition(self):
		xCounterPosition = self.wFleetPanel - self.X_SHIPS_COUNTER_MARGIN 
		yCounterPosition = self.Y_SHIPS_COUNTER_MARGIN 

		return xCounterPosition, yCounterPosition

	def diplayTheShipTopOptionButtons(self, pShip, xPosition, yPosition) :
		if pShip.isAutomated():
			self.diplayTopOptionButtonsForAutomatedShip(pShip, xPosition, yPosition)
		else:
			self.diplayTopOptionButtonsForNonAutomatedShip(pShip, xPosition, yPosition)

	def calculateTopOptionButtonPosition(self, xPosition, yPosition):
		xOptionButtonPos = xPosition + self.X_OUTSIDE_TOP_OPTION_BUTTON_MARGIN + (self.topOptionButtonCount - 1) * (self.TOP_OPTION_BUTTON_SIZE + self.X_TOP_OPTION_BUTTON_MARGIN)
		yOptionButtonPos = yPosition - self.Y_OUTSIDE_TOP_OPTION_BUTTON_MARGIN

		self.topOptionButtonCount += 1

		return xOptionButtonPos, yOptionButtonPos

	def diplayTopOptionButtonsForNonAutomatedShip(self, pShip, xPosition, yPosition):
		screen = self.getScreen()
		
		# Initialise top option button count. Allow us to know where to put the button in the game
		self.topOptionButtonCount = 1

		# Display the Seaway button
		xOptionButtonPos, yOptionButtonPos = self.calculateTopOptionButtonPosition(xPosition, yPosition)
		if pShip.canChooseSeaway():	
			screen.setImageButtonAt(self.getNextWidgetName(), self.operationalFleetsPanelName, self.INTERFACE_WHICH_SEAWAYS, xOptionButtonPos, yOptionButtonPos, self.TOP_OPTION_BUTTON_SIZE, self.TOP_OPTION_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, self.VIEW_SEAWAYS, pShip.getID())
		else:
			screen.setImageButtonAt(self.getNextWidgetName(), self.operationalFleetsPanelName, self.INTERFACE_NO_WHICH_SEAWAYS, xOptionButtonPos, yOptionButtonPos, self.TOP_OPTION_BUTTON_SIZE, self.TOP_OPTION_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, self.NO_SEAWAYS, -1)
		
		# Display the europe sail button
		xOptionButtonPos, yOptionButtonPos = self.calculateTopOptionButtonPosition(xPosition, yPosition)
		screen.setImageButtonAt(self.getNextWidgetName(), self.operationalFleetsPanelName, self.INTERFACE_EUROPE_SAIL, xOptionButtonPos, yOptionButtonPos, self.TOP_OPTION_BUTTON_SIZE, self.TOP_OPTION_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, self.SAIL_TO_NEW_WORLD, pShip.getID())
		
		if self.isFleet(pShip):
			# Display the eject button
			xOptionButtonPos, yOptionButtonPos = self.calculateTopOptionButtonPosition(xPosition, yPosition)
			screen.setImageButtonAt(self.getNextWidgetName(), self.operationalFleetsPanelName, self.INTERFACE_EJECT_UNIT_TO_GROUP, xOptionButtonPos, yOptionButtonPos, self.TOP_OPTION_BUTTON_SIZE, self.TOP_OPTION_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, self.EJECT_UNIT_TO_GROUP, pShip.getID())
			
		# Display the affect trade route button
		xOptionButtonPos, yOptionButtonPos = self.calculateTopOptionButtonPosition(xPosition, yPosition) 
		screen.setImageButtonAt(self.getNextWidgetName(), self.operationalFleetsPanelName, self.INTERFACE_GENERAL_AFFECT_TRADE_ROUTE, xOptionButtonPos, yOptionButtonPos, self.TOP_OPTION_BUTTON_SIZE, self.TOP_OPTION_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, self.CHOOSE_TRADE_ROUTE, pShip.getID())
		
		if self.isHurt(pShip, True):
			xOptionButtonPos, yOptionButtonPos = self.calculateTopOptionButtonPosition(xPosition, yPosition) 
			screen.setImageButtonAt(self.getNextWidgetName(), self.operationalFleetsPanelName, self.INTERFACE_REPAIR_SHIP, xOptionButtonPos, yOptionButtonPos, self.TOP_OPTION_BUTTON_SIZE, self.TOP_OPTION_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, self.REPAIR_SHIP, pShip.getID())

	def isHurt(self, pShip, includeGroup):
		if includeGroup and self.isFleet(pShip):
			pGroup = pShip.getGroup()
			return pGroup.isHurt()
		return pShip.isHurt()

	def hasToBeResupplied(self, pShip, includeGroup, testAmmunition, testCannon):
		if includeGroup and self.isFleet(pShip):
			pGroup = pShip.getGroup()
			return pGroup.hasToBeResupplied(testAmmunition, testCannon)
		return pShip.hasToBeResupplied(testAmmunition, testCannon)
			
	def isFleet(self, pShip):
		pGroup = pShip.getGroup()
		return not pGroup.isNone() and pGroup.getNumUnits() > 1

	def diplayTopOptionButtonsForAutomatedShip(self, pShip, xPosition, yPosition):
		screen = self.getScreen()
		pGroup = pShip.getGroup()

		# Initialise top option button count. Allow us to know where to put the button in the game
		self.topOptionButtonCount = 1

		# Display the trade route button
		xOptionButtonPos, yOptionButtonPos = self.calculateTopOptionButtonPosition(xPosition, yPosition)
		screen.setImageButtonAt(self.getNextWidgetName(), self.operationalFleetsPanelName, self.INTERFACE_TRADE_ROUTES_BUTTON, xOptionButtonPos, yOptionButtonPos, self.TOP_OPTION_BUTTON_SIZE, self.TOP_OPTION_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TRADE_ROUTE_SCREEN).getActionInfoIndex(), pGroup.getID())
		
		# Display the stop automation button
		xOptionButtonPos, yOptionButtonPos = self.calculateTopOptionButtonPosition(xPosition, yPosition)
		screen.setImageButtonAt(self.getNextWidgetName(), self.operationalFleetsPanelName, self.INTERFACE_STOP_TRADE_ROUTES_BUTTON, xOptionButtonPos, yOptionButtonPos, self.TOP_OPTION_BUTTON_SIZE, self.TOP_OPTION_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, self.STOP_TRADE_ROUTE, pShip.getID())
		
		if self.isFleet(pShip):
			# Display the eject button
			xOptionButtonPos, yOptionButtonPos = self.calculateTopOptionButtonPosition(xPosition, yPosition)
			screen.setImageButtonAt(self.getNextWidgetName(), self.operationalFleetsPanelName, self.INTERFACE_EJECT_UNIT_TO_GROUP, xOptionButtonPos, yOptionButtonPos, self.TOP_OPTION_BUTTON_SIZE, self.TOP_OPTION_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, self.EJECT_UNIT_TO_GROUP, pShip.getID())
			
	def getShipName(self, pShip):
		szUnitName = pShip.getName()
		return self.applyColorIfRequired(pShip, szUnitName)

	def applyColorIfRequired(self, pShip, text):
		if self.isHurt(pShip, True):
			text = localText.changeTextColor(text, self.COLOR_RED)
		if self.hasToBeResupplied(pShip, True, True, True):
			text = localText.changeTextColor(text, self.COLOR_ORANGE)
		return text

	def displayMilitaryStatistics(self, pShip, shipPanelName):
		screen = self.getScreen()
		player = self.pPlayer
		
		iMaxCannon = gc.getUnitInfo(pShip.getUnitType()).getMaxCannon()
		if iMaxCannon > 0:
			# Display cannon amount
			szLeftText = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_CANNONS", ())
			szLeftText = localText.changeTextColor(szLeftText, self.COLOR_FONT_CREAM)
			szText = szLeftText + self.getQuantityValueText(pShip.getNbCannon(), iMaxCannon, iMaxCannon)
			xTextInfoPos, yTextInfoPos = self.calculateShipStatisticsTextPosition(2)			
			screen.setLabelAt(self.getNextWidgetName(), shipPanelName, u"<font=1>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xTextInfoPos, yTextInfoPos, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iMaxAmmunition = gc.getUnitInfo(pShip.getUnitType()).getMaxMunition()
		if iMaxAmmunition > 0:
			#Display ship ammunition
			szLeftText = localText.getText("TXT_KEY_EUROPE_SCREEN_TACTICAL_INFORMATION_AMMUNITIONS", ())
			szLeftText = localText.changeTextColor(szLeftText, self.COLOR_FONT_CREAM)
			szText = szLeftText + self.getQuantityValueText(pShip.getMunition(), iMaxAmmunition, iMaxAmmunition)
			xTextInfoPos, yTextInfoPos = self.calculateShipStatisticsTextPosition(3)
			screen.setLabelAt(self.getNextWidgetName(), shipPanelName, u"<font=1>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xTextInfoPos, yTextInfoPos, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
	def displayShipPromotions(self, pShip, shipPanelName):
		screen = self.getScreen()
		player = self.pPlayer

		iMaxCannon = gc.getUnitInfo(pShip.getUnitType()).getMaxCannon()
		iPromotionCount = 0

		if iMaxCannon > 0:
			for index in range(gc.getNumPromotionInfos()):
				if self.shouldDisplayPromotion(pShip, index, iPromotionCount):
					szPromotion = "<img=%s size=%d></img>" % (gc.getPromotionInfo(index).getButton(), self.PROMOTION_PICTURE_SIZE)
					xPromotionsPos, yPromotionsPos = self.calculateShipPromotionPosition(iPromotionCount)
					screen.setLabelAt(self.getNextWidgetName(), shipPanelName, szPromotion, CvUtil.FONT_RIGHT_JUSTIFY, xPromotionsPos, yPromotionsPos, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					iPromotionCount += 1
	
	def calculateShipPromotionPosition(self, iPromotionCount):
		row = iPromotionCount / self.NUM_PROMOTIONS_BY_ROW
		col = iPromotionCount % self.NUM_PROMOTIONS_BY_ROW

		xPromotionsPos = self.wFleetPanel - self.X_OUTSIDE_SHIP_PROMOTION_MARGIN - (self.X_SHIP_PROMOTION_MARGIN + self.PROMOTION_PICTURE_SIZE) * col
		yPromotionsPos = self.hFleetPanel * 7 / 24 + row * (self.Y_SHIP_PROMOTION_MARGIN + self.PROMOTION_PICTURE_SIZE)

		return xPromotionsPos, yPromotionsPos 
	
	def shouldDisplayPromotion(self, pShip, index, iPromotionCount):
		# We are limiting the number of promotion to display. The player will understand that its military ship is overstuffed
		if iPromotionCount > self.NUM_PROMOTIONS_BY_ROW * self.MAX_PROMOTIONS_ROWS:
			return False

		return pShip.isHasPromotion(index) and not gc.getPromotionInfo(index).isGraphicalOnly()

	def calculateShipStatisticsTextPosition(self, row):
		return self.X_OUTSIDE_SHIP_STATISTICS_TEXT_MARGIN, self.hFleetPanel * 2 / 3 + (row - 1) * self.Y_SHIP_STATISTICS_TEXT_MARGIN

	def getQuantityValueText(self, iCurrent, iMax, iMin):
		szText = u" %d/%d" %(iCurrent, iMax)

		color = self.COLOR_FONT_CREAM
		if iCurrent < iMin:
			color = self.COLOR_ORANGE
		
		return localText.changeTextColor(szText, color)	

	def calculateCargoSize(self):
		#Init variable
		maxCargoInShip = 6

		return (self.wFleetPanel - self.X_CARGO_MARGIN * (maxCargoInShip - 1) - self.X_OUTSIDE_CARGO_MARGIN) / maxCargoInShip

	def calculateCargoPosition(self, index, xPosition, yPosition, cargoSize):
		#Init positions
		xCargoPosition = xPosition + (cargoSize + self.X_CARGO_MARGIN) * index + self.X_OUTSIDE_CARGO_MARGIN

		yCargoPosition = yPosition + self.hFleetPanel - cargoSize - self.Y_CARGO_MARGIN

		return xCargoPosition, yCargoPosition

	def displayShipCargo(self, pShip, xPosition, yPosition, widgetType):
		screen = self.getScreen()
		player = self.pPlayer

		cargoSize = self.calculateCargoSize()

		# We display empty cargo boxes
		for index in range(pShip.cargoSpace()):
			# Init cargo variable
			xCargoPosition, yCargoPosition = self.calculateCargoPosition(index, xPosition, yPosition, cargoSize)
			screen.addDDSGFCAt(self.getNextWidgetName(), self.operationalFleetsPanelName, self.INTERFACE_EUROPE_BOX_CARGO, xCargoPosition, yCargoPosition, cargoSize, cargoSize, widgetType, pShip.getID(), player.getID(), False)

		# We display unit inside the specified ship
		cargoCount = 0
		pPlot = pShip.plot()
		for index in range(pPlot.getNumUnits()):
			pLoopUnit = pPlot.getUnit(index)
			pTransportUnit = pLoopUnit.getTransportUnit()
			if (not pTransportUnit.isNone() and pTransportUnit.getID() == pShip.getID() and pTransportUnit.getOwner() == pShip.getOwner()):
				# Init cargo variable
				xCargoPosition, yCargoPosition = self.calculateCargoPosition(cargoCount, xPosition, yPosition, cargoSize)
				screen.setImageButtonAt(self.getNextWidgetName(), self.operationalFleetsPanelName, pLoopUnit.getButton(), xCargoPosition, yCargoPosition, cargoSize, cargoSize, WidgetTypes.WIDGET_SHIP_CARGO, pLoopUnit.getID(), pTransportUnit.getID())
				cargoCount = cargoCount + 1

		# We display goods inside the specified ship
		goodsForOneCargo = 30
		countGoodsInShip = pShip.getOnlyNewCargo()
		index = pShip.cargoSpace() - 1
		while index >= 0:
			if countGoodsInShip > 0:
				xCargoPosition, yCargoPosition = self.calculateCargoPosition(index, xPosition, yPosition, cargoSize)
				screen.addDDSGFCAt(self.getNextWidgetName(), self.operationalFleetsPanelName, self.INTERFACE_EUROPE_BOX_CARGO_FULL, xCargoPosition, yCargoPosition, cargoSize, cargoSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
				szCargoCount = u"<font=1>%d</font>" %(min(countGoodsInShip, goodsForOneCargo))
				screen.setLabelAt(self.getNextWidgetName(), self.operationalFleetsPanelName, szCargoCount, CvUtil.FONT_CENTER_JUSTIFY, xCargoPosition + cargoSize / 2, yCargoPosition + cargoSize / 2, -0.1, FontTypes.SMALL_FONT, widgetType, pShip.getID(), player.getID())
				countGoodsInShip -= goodsForOneCargo
			index -= 1

	def shouldDisplayShipCargo(self, pShip):
		return pShip.getNewCargo() > 0  or pShip.isOnlyDefensive() 

	def getArtBoxSquare(self, pShip):
		if pShip.isAutomated():
			return self.INTERFACE_EUROPE_IN_PORT_BOX_SQUARE
		else:
			return self.INTERFACE_EUROPE_IN_PORT_BOX_SQUARE_GRAY 

	def calculateFleetPanelWidth(self, fleetByRow):
		return (self.IN_PORT_PANE_WIDTH - self.X_PANEL_MARGIN * (fleetByRow + 1) - 2 * self.X_OUTSIDE_PANEL_MARGIN) / fleetByRow

	def getTopLeftPositionOfShipPanel(self, index, fleetByRow, wFleetPanel, hFleetPanel):
		column = index % fleetByRow
		row = index / fleetByRow
		
		
		xPosition = self.X_OUTSIDE_PANEL_MARGIN + column * (wFleetPanel + self.X_PANEL_MARGIN)
		yPosition = self.Y_OUTSIDE_PANEL_MARGIN + row * (hFleetPanel + self.Y_PANEL_MARGIN)

		return xPosition, yPosition

	def getFleetWidgetType(self, pGroup):
		if pGroup.getNumUnits() == 1:
			return WidgetTypes.WIDGET_ONE_SHIP
		else:
			return WidgetTypes.WIDGET_GROUP_SHIP

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
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):
				bRedraw = True
				if (inputClass.getData1() == self.SAIL_TO_NEW_WORLD) :
					transport = self.pPlayer.getUnit(inputClass.getData2())
					if (not transport.isNone()) and transport.getUnitTravelState() != UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE:
						CyMessageControl().sendDoCommand(inputClass.getData2(), CommandTypes.COMMAND_SAIL_TO_EUROPE, UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE, -1, false)

				elif (inputClass.getData1() == self.EJECT_UNIT_TO_GROUP) :
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_EJECT_UNIT_TO_GROUP)
					popupInfo.setData1(inputClass.getData2())
					CyInterface().addPopup(popupInfo, self.pPlayer.getID(), true, true)

				elif (inputClass.getData1() == self.STOP_TRADE_ROUTE) :
					CyMessageControl().sendDoCommand(inputClass.getData2(), CommandTypes.COMMAND_STOP_AUTOMATION, -1, -1, false)

				elif (inputClass.getData1() == self.COME_BACK_INTO_EUROPE) :
					CyMessageControl().sendDoCommand(inputClass.getData2(), CommandTypes.COMMAND_COME_BACK_INTO_EUROPE, -1, -1, false)

				elif (inputClass.getData1() == self.REPAIR_SHIP) :
					CyMessageControl().sendDoCommand(inputClass.getData2(), CommandTypes.COMMAND_REPAIR_SHIPS, True, -1, false)

				elif (inputClass.getData1() == self.CHOOSE_TRADE_ROUTE) :
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_CHOOSE_TRADE_ROUTES)
					popupInfo.setData1(inputClass.getData2())
					popupInfo.setData2(self.EUROPE_ID)#-2 for Europe only, -1 for all, >= 0 for only one city (Id of city)
					CyInterface().addPopup(popupInfo, self.pPlayer.getID(), true, true)
					bRedraw = False
					
				###################################################
				################### SEAWAY START ##################
				###################################################
				elif (inputClass.getData1() == self.VIEW_SEAWAYS) :
					self.CURRENT_UNIT_ID = inputClass.getData2()
					self.CHOOSE_SEAWAY_VIEW = True

				elif (inputClass.getData1() == self.EXIT_VIEW_SEAWAYS) :
					self.CHOOSE_SEAWAY_VIEW = False

				elif (inputClass.getData1() == self.CHOOSE_SEAWAY) :
					CyMessageControl().sendDoCommand(self.CURRENT_UNIT_ID, CommandTypes.COMMAND_SAIL_TO_EUROPE, UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE, inputClass.getData2(), false)
					self.CHOOSE_SEAWAY_VIEW = False

				elif (inputClass.getData1() == self.REMOVE_SEAWAY) :
					CyMessageControl().sendPlayerAction(self.pPlayer.getID(), PlayerActionTypes.PLAYER_ACTION_REMOVE_SEAWAY, inputClass.getData2(), -1, -1)

				elif (inputClass.getData1() == self.RENAME_SEAWAY) :
					CyMessageControl().sendModNetMessage(self.EDIT_SEAWAY_NAME, gc.getGame().getActivePlayer(), inputClass.getData2(), -1, -1)

				elif inputClass.getData1() == self.CHANGE_SEAWAY_PAGE:
					self.CURRENT_SEAWAY_PAGE += inputClass.getData2()
				###################################################
				################### SEAWAY END ##################
				###################################################
				if bRedraw:
					self.drawContents()
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON) :
			if (inputClass.getFunctionName() == "SelectSeaway") :
				screen = self.getScreen()
				iColor = gc.getPlayerColorInfo( self.pPlayer.getPlayerColor()).getColorTypePrimary()
				iPosSeaway = inputClass.getID()
				pSeaway =  self.pPlayer.getSeaway(iPosSeaway)
				pPlot = pSeaway.plot()
				if pPlot:
					szColor = gc.getInfoTypeForString("COLOR_WHITE")
					screen.minimapFlashPlot(pPlot.getX(), pPlot.getY(), szColor, -1)
					
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF) :
			if (inputClass.getFunctionName() == "SelectSeaway") :
				screen = self.getScreen()
				screen.minimapClearAllFlashingTiles()
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (inputClass.getFunctionName() == self.CIV_DROP_DOWN):				
				self.CivDropDown(inputClass)
			
		return 0

	def CivDropDown( self, inputClass ):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
			screen = self.getScreen()
			iIndex = screen.getSelectedPullDownID(self.CIV_DROP_DOWN)
			self.pPlayer = gc.getPlayer(screen.getPullDownData(self.CIV_DROP_DOWN, iIndex))
			self.drawContents()
	
	def update(self, fDelta):
		if (CyInterface().isDirty(InterfaceDirtyBits.EuropeScreen_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.EuropeScreen_DIRTY_BIT, False)
			pPlayer = self.pPlayer
			if(pPlayer.getNumSeaways() == 0) :
				self.CHOOSE_SEAWAY_VIEW = False
			else:
				curPage = self.CURRENT_SEAWAY_PAGE
				numByPage = self.NUM_SEAWAYS_BY_PAGE
				iNumSeaways = pPlayer.getNumSeaways()
				iNumPages = (iNumSeaways-1)/numByPage
				if curPage > iNumPages:
					self.CURRENT_SEAWAY_PAGE = curPage - 1
		
			self.drawContents()

	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList

		if eWidgetType == WidgetTypes.WIDGET_GENERAL:
			if iData1 == self.SAIL_TO_NEW_WORLD:
				return localText.getText("TXT_KEY_SAIL", ())
			elif iData1 == self.VIEW_SEAWAYS:
				if iData2 != -1:
					return localText.getText("TXT_KEY_WHICH_SEAWAYS", ())
				else :
					return localText.getText("TXT_KEY_SEAWAYS_MANAGEMENT", ())
			elif iData1 == self.NO_SEAWAYS:
				return localText.getText("TXT_KEY_NO_WHICH_SEAWAYS", ())
			elif iData1 == self.TREASURY_ID:
				return localText.getText("TXT_KEY_ECON_GOLD_RESERVE", ())
			elif iData1 == self.EJECT_UNIT_TO_GROUP:
				return localText.getText("TXT_KEY_EJECT_UNIT_TO_GROUP", ())
			elif iData1 == self.STOP_TRADE_ROUTE:
				return localText.getText("TXT_KEY_COMMAND_STOP_AUTOMATION", ())
			elif iData1 == self.HELP_CROSS_RATE:
				player = self.pPlayer
				return localText.getText("TXT_KEY_YIELD_RATE", (player.getYieldRate(YieldTypes.YIELD_CROSSES), gc.getYieldInfo(YieldTypes.YIELD_CROSSES).getChar()))
			elif iData1 == self.CHOOSE_SEAWAY:
				if self.getCurrentSeawayId() == iData2:
					return localText.getText("TXT_KEY_TRAVEL_SEAWAY_COME_BACK", ())
			elif iData1 == self.COME_BACK_INTO_EUROPE:
				return self.getComeBackIntoEuropeHelp(iData2)
			elif iData1 == self.CHOOSE_TRADE_ROUTE:
				return localText.getText("TXT_KEY_CHOOSE_TRADE_ROUTE", ())
			elif iData1 == self.REPAIR_SHIP:
				return localText.getText("TXT_KEY_EUROPE_ICON_REPAIR", ())
		return u""

	def  getComeBackIntoEuropeHelp(self, unitId):
		pPlayer = self.pPlayer
		pShip = pPlayer.getUnit(unitId)
		pGroup = pShip.getGroup()				
		if not pGroup.isNone() and pGroup.getNumUnits() > 1:
			return localText.getText("TXT_KEY_UNIT_HELP_FLEET_CAN_COME_BACK_INTO_EUROPE", ())
		else :
			return localText.getText("TXT_KEY_UNIT_HELP_CAN_COME_BACK_INTO_EUROPE", ())

	def updateSeawaysView(self):
		screen = self.getScreen()

		for seawayId in self.printedSeawaysList:
			screen.deleteWidget("SelectSeaway" + str(seawayId))

		if self.CHOOSE_SEAWAY_VIEW:
			screen.show("EmptySeawayPanel")
			screen.show("SeawayPanel")
			self.addMinimap()
			self.showChooseSeaway()
		else :
			screen.hide("EmptySeawayPanel")
			screen.hide("SeawayPanel")
			screen.hide("_FXS_Screen_Bogus_Minimap_Name")

	def getCurrentSeawayId(self):
		pPlayer = self.pPlayer

		if self.CURRENT_UNIT_ID != -1:
			pShip = pPlayer.getUnit(self.CURRENT_UNIT_ID)
			return pPlayer.findSeaway(pShip.plot()).getID()
		return -1

	def showChooseSeaway(self):
		screen = self.getScreen()
		pPlayer = self.pPlayer
		currentSeawayID = self.getCurrentSeawayId()
		self.currentSeawayPos = -1

		chooseSeawayAction = -1
		szSeawayHeader =  u"%s" % localText.getText("TXT_KEY_EUROPE_SEAWAYS_MANAGEMENT_HEADER", ())
		if self.CURRENT_UNIT_ID != -1:
			chooseSeawayAction = self.CHOOSE_SEAWAY
			szSeawayHeader =  u"%s" % localText.getText("TXT_KEY_EUROPE_DESTINATION_HEADER", ())
		

		screen.setLabelAt(self.getNextWidgetName(), "SeawayPanel", u"<font=4><color=158,111,51>" + szSeawayHeader + u"</color></font>", CvUtil.FONT_CENTER_JUSTIFY, 460, 95, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		curPage = self.CURRENT_SEAWAY_PAGE
		numByPage = self.NUM_SEAWAYS_BY_PAGE
		iNumSeaways = pPlayer.getNumSeaways()
		iNumPages = (iNumSeaways-1)/numByPage
		iMinSeaway = numByPage*curPage
		iMaxSeaway =  min(numByPage*(curPage+1), iNumSeaways)
		iNumSewayOnPage = iMaxSeaway - iMinSeaway
		iOffset = 24
		iOffsetAlone = 0
		if (iNumSeaways == 1):
			iOffsetAlone = -18

		iCloseOffset = 8
		iCloseSize = 50
		bShowArrow = iNumSeaways > 1

		xStartRow = 345
		xStartArrow = xStartRow - 5
		xRowSize = 220

		
		self.printedSeawaysList = []

		screen.setImageButtonAt(self.getNextWidgetName(), "SeawayPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_CLOSE").getPath(), 720 - iCloseSize - iCloseOffset , iCloseOffset, iCloseSize, iCloseSize, WidgetTypes.WIDGET_GENERAL, self.EXIT_VIEW_SEAWAYS, -1)

		for index in range(iNumSewayOnPage):
			iPosSeaway = index+iMinSeaway
			loopSeaway = pPlayer.getSeaway(iPosSeaway)
			szSeaway = loopSeaway.getName()
			if currentSeawayID == loopSeaway.getID():
			 	szSeaway = localText.changeTextColor(szSeaway, gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
			 	self.currentSeawayPos = iPosSeaway
			screen.addDDSGFCAt(self.getNextWidgetName(), "SeawayPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_ROW_SEPARATION").getPath(), xStartRow, 140 + index*iOffset, xRowSize, 4, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
			if bShowArrow:
				if (iPosSeaway == 0):
					screen.setImageButtonAt(self.getNextWidgetName(), "SeawayPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_ARROW_DOWN").getPath(), xStartArrow, 120 + index*iOffset, 25, 20, WidgetTypes.WIDGET_CHANGE_SEAWAY_POSITION, iPosSeaway, 0)
				elif (iPosSeaway == (iNumSeaways - 1)):
					screen.setImageButtonAt(self.getNextWidgetName(), "SeawayPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_ARROW_UP").getPath(), xStartArrow, 120 + index*iOffset, 25, 20, WidgetTypes.WIDGET_CHANGE_SEAWAY_POSITION, iPosSeaway, 1)
				else:
					screen.setImageButtonAt(self.getNextWidgetName(), "SeawayPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_ARROW_DOWN_UP").getPath(), xStartArrow, 120 + index*iOffset, 25, 20, WidgetTypes.WIDGET_CHANGE_SEAWAY_POSITION, iPosSeaway, 2)
			
			screen.setTextAt("SelectSeaway" + str(iPosSeaway), "SeawayPanel", u"<font=3>" + szSeaway + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xStartRow + 19 + iOffsetAlone, 130 + index*iOffset, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, chooseSeawayAction, iPosSeaway)
			screen.setImageButtonAt(self.getNextWidgetName(), "SeawayPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_REMOVE").getPath(), xStartRow + xRowSize - 20 , 120 + index*iOffset, 20, 20, WidgetTypes.WIDGET_GENERAL, self.REMOVE_SEAWAY, iPosSeaway)
			screen.setImageButtonAt(self.getNextWidgetName(), "SeawayPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_RENAME").getPath(), xStartRow + xRowSize - 20*2 , 120 + index*iOffset + 2, 20, 20, WidgetTypes.WIDGET_GENERAL, self.RENAME_SEAWAY, iPosSeaway)
	
			self.printedSeawaysList.append(iPosSeaway)

		#Navigation page of seaway

		iStartX = 380
		iStartY = 380
		xArrowSize = self.XResolution*31/1024
		yArrowSize = self.YResolution*20/768
		xPosArrowLeft = self.XResolution*15/1024
		xPosArrowRight = self.XResolution*5/64
		
		if curPage != 0:
			screen.setImageButtonAt(self.getNextWidgetName(), "SeawayPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_LEFT").getPath(), iStartX+xPosArrowLeft, iStartY, xArrowSize, yArrowSize, WidgetTypes.WIDGET_GENERAL, self.CHANGE_SEAWAY_PAGE, -1)
		else:
			screen.setImageButtonAt(self.getNextWidgetName(), "SeawayPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_LEFT_SHADOW").getPath(), iStartX+xPosArrowLeft, iStartY, xArrowSize, yArrowSize, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if curPage != iNumPages:
			screen.setImageButtonAt(self.getNextWidgetName(), "SeawayPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_RIGHT").getPath(), iStartX+xPosArrowRight, iStartY, xArrowSize, yArrowSize, WidgetTypes.WIDGET_GENERAL, self.CHANGE_SEAWAY_PAGE, 1)
		else:
			screen.setImageButtonAt(self.getNextWidgetName(), "SeawayPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_RIGHT_SHADOW").getPath(), iStartX+xPosArrowRight, iStartY, xArrowSize, yArrowSize, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szPage = u"<font=3b>%d</font>" % (curPage+1)
		szPage = localText.changeTextColor(szPage, gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabelAt(self.getNextWidgetName(), "SeawayPanel", szPage, CvUtil.FONT_CENTER_JUSTIFY, iStartX+xPosArrowRight - self.XResolution*17/1024, iStartY + 9, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
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

	def orderEuropeUnitsList(self):
		pPlayer = self.pPlayer
		self.EuropeUnitsList = []

		EuropeGroupsList = []
		for pShip in self.UnorderEuropeUnitsList:
			pGroup = pShip.getGroup()
			iOrderValue = pGroup.getOrderValue()
			EuropeGroupsList.append((iOrderValue, pShip))
			
		if len(EuropeGroupsList) > 0:
			EuropeGroupsList.sort()
			EuropeGroupsList.reverse()
			for iShip in range(len(EuropeGroupsList)):
				pShip = EuropeGroupsList[iShip][1]
				self.EuropeUnitsList.append(pShip)


	def xSize(self, val):
		return val * self.XResolution / 1024

	def ySize(self, val):
		return val * self.YResolution / 768

	def minSize(self, val):
		return min(self.xSize(val), self.ySize(val))
