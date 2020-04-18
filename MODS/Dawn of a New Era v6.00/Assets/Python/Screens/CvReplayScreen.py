## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import time
import re
import CvScreensInterface

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvReplayScreen:
	"Replay Screen for end of game"

	def __init__(self, screenId):
		self.screenId = screenId
		self.REPLAY_SCREEN_NAME = "ReplayScreen"
		self.WIDGET_ID = "ReplayScreenWidget"
		self.EXIT_ID = "ReplayScreenExitWidget"
		self.BACKGROUND_ID = "ReplayScreenBackground"
		self.replayInfo = None
		self.bPlaying = False

		self.REPLAY_SCREEN_ID = 1
		self.IMMIGRATION_SCREEN_ID = 2
		self.LEGEND_LINE = 3

		self.LINE_ID   = "DemoLine"

	def setReplayInfo(self, replayInfo):
		self.replayInfo = replayInfo

	def getScreen(self):
		return CyGInterfaceScreen(self.REPLAY_SCREEN_NAME, self.screenId)

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()

	# Screen construction function
	def showScreen(self, bFromHallOfFame):

		self.Z_BACKGROUND = -6.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2

		screen = self.getScreen()
		
		self.X_SCREEN = 500
		self.Y_SCREEN = 396

		self.W_SCREEN = screen.getXResolution()
		self.H_SCREEN = screen.getYResolution()
		self.Y_TITLE = 8
		self.BORDER_WIDTH = 4
		self.W_HELP_AREA = 200

		self.X_EXIT = self.W_SCREEN - 30
		self.Y_EXIT = self.H_SCREEN - 35

		self.X_PLAY = 50
		self.Y_PLAY = self.H_SCREEN - 85

		self.X_FORWARD = 200
		self.Y_FORWARD = self.H_SCREEN - 85

		self.X_SPEED = self.W_SCREEN - 350
		self.Y_SPEED = self.H_SCREEN - 100

		self.X_SLIDER = self.W_SCREEN - 310 #475
		self.Y_SLIDER = self.H_SCREEN - 100
		self.W_SLIDER = 100
		self.H_SLIDER = 25
		self.NUM_SLIDER_STOPS = 5

		self.nWidgetCount = 0
		self.nLineCount = 0

		self.X_MAP = 50
		self.Y_MAP = 100
		self.W_MAP = self.W_SCREEN - 580
		self.H_MAP_MAX = self.W_SCREEN - 400

		self.X_TEXT = self.W_SCREEN - 460 #625
		self.Y_TEXT = 100
		self.W_TEXT = 390
		self.H_TEXT = self.H_SCREEN - 220 #580

		if (self.H_MAP_MAX > self.H_TEXT):
			self.H_MAP_MAX = self.H_TEXT

		self.TIME_STEP = (1.0, 0.5, 0.25, 0.125, 0.0625)

		# Create a new screen
		screen = self.getScreen()
		if screen.isActive():
			return
			
		screen.enableWorldSounds( false )
		# CyInterface().stopAdvisorSound()
		# CyInterface().playAdvisorSound("AS2D_VICTORY")
		
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.PLAY_TEXT = u"<font=4>" + localText.getText("TXT_KEY_REPLAY_SCREEN_PLAY", ()).upper() + u"</font>"
		self.FORWARD_TEXT = u"<font=4>" + localText.getText("TXT_KEY_REPLAY_SCREEN_NEXT", ()).upper() + u"</font>"
		self.STOP_TEXT = u"<font=4>" + localText.getText("TXT_KEY_REPLAY_SCREEN_STOP", ()).upper() + u"</font>"
		self.SPEED_TEXT = localText.getText("TXT_KEY_REPLAY_SCREEN_SPEED", ())
		self.IMMIGRATION_TEXT = localText.getText("TXT_KEY_IMMIGRATION_TITLE", ())
		self.REPLAY_TEXT = localText.getText("TXT_KEY_REPLAY_TITLE", ())

		self.szForwardId = ""
		self.szPlayId = ""
		self.bPlaying = False
		self.fLastUpdate = 0.
		self.iSpeed = 2
		self.iLastTurnShown = -1
		self.bFromHallOfFame = bFromHallOfFame
		self.bDone = False

		################################################## GRAPH ###################################################

		self.X_MARGIN	= 15
		self.Y_MARGIN	= 70
		self.H_DROPDOWN	= 35

		self.X_DEMO_DROPDOWN	= self.X_MARGIN
		self.Y_DEMO_DROPDOWN	= self.Y_MARGIN
		self.W_DEMO_DROPDOWN	= 200

		self.X_ZOOM_DROPDOWN	= self.X_DEMO_DROPDOWN
		self.Y_ZOOM_DROPDOWN	= self.Y_DEMO_DROPDOWN + self.H_DROPDOWN
		self.W_ZOOM_DROPDOWN	= self.W_DEMO_DROPDOWN

		self.X_LEGEND		= self.X_DEMO_DROPDOWN
		self.W_LEGEND		= self.W_DEMO_DROPDOWN + 20

		self.X_GRAPH = self.X_DEMO_DROPDOWN + self.W_DEMO_DROPDOWN + 30
		self.Y_GRAPH = self.Y_MARGIN
		self.W_GRAPH = self.W_SCREEN - self.X_GRAPH - self.X_MARGIN
		self.H_GRAPH = self.H_SCREEN / 2

		self.W_LEFT_BUTTON  = 20
		self.H_LEFT_BUTTON  = 20
		self.X_LEFT_BUTTON  = self.X_GRAPH
		self.Y_LEFT_BUTTON  = self.Y_GRAPH + self.H_GRAPH

		self.W_RIGHT_BUTTON  = self.W_LEFT_BUTTON
		self.H_RIGHT_BUTTON  = self.H_LEFT_BUTTON
		self.X_RIGHT_BUTTON  = self.X_GRAPH + self.W_GRAPH - self.W_RIGHT_BUTTON
		self.Y_RIGHT_BUTTON  = self.Y_LEFT_BUTTON

		self.X_LEFT_LABEL   = self.X_LEFT_BUTTON + self.W_LEFT_BUTTON + 10
		self.X_RIGHT_LABEL  = self.X_RIGHT_BUTTON - 10
		self.Y_LABEL		= self.Y_GRAPH + self.H_GRAPH + 3

		self.H_LEGEND = 0
		self.X_LEGEND_MARGIN = 10
		self.Y_LEGEND_MARGIN = 5
		self.X_LEGEND_LINE = self.X_LEGEND_MARGIN
		self.Y_LEGEND_LINE = self.Y_LEGEND_MARGIN + 9  # to center it relative to the text
		self.W_LEGEND_LINE = 30
		self.X_LEGEND_TEXT = self.X_LEGEND_LINE + self.W_LEGEND_LINE - 3
		self.Y_LEGEND_TEXT = self.Y_LEGEND_MARGIN
		self.H_LEGEND_TEXT = 16
		self.LEGEND_PANEL_ID = ""
		self.LEGEND_CANVAS_ID = ""
		
		self.GRAPH_H_LINE = "GraphHLine"
		self.GRAPH_V_LINE = "GraphVLine"

		self.Y_UNIT_ANIMATION = self.Y_DEMO_DROPDOWN + self.H_DROPDOWN * 2
		self.W_UNIT_ANIMATION = self.W_LEGEND * 2 / 5
		self.H_UNIT_ANIMATION = self.W_UNIT_ANIMATION * 7 / 4
		self.X_UNIT_ANIMATION = self.X_DEMO_DROPDOWN + self.W_DEMO_DROPDOWN / 2 - self.W_UNIT_ANIMATION / 2
		
		self.X_ROTATION_UNIT_ANIMATION = -20
		self.Z_ROTATION_UNIT_ANIMATION = 30
		self.SCALE_ANIMATION = 1.0
		
		################################################## TABLE ###################################################
		self.X_CHART = self.X_MARGIN
		self.Y_CHART = self.Y_GRAPH + self.H_GRAPH + self.Y_MARGIN / 2
		self.W_CHART = self.W_SCREEN - 2 * self.X_MARGIN
		self.H_CHART = self.H_SCREEN - self.Y_CHART - self.Y_MARGIN

		self.TEXT_LEADER_NAME = CyTranslator().getText("TXT_KEY_LEADER_NAME", ())
		self.TEXT_TOTAL_RECRUIT_TURN = CyTranslator().getText("TXT_KEY_TOTAL_RECRUIT_TURN", ())
		self.TEXT_TOTAL_PROPOSITION = CyTranslator().getText("TXT_KEY_TOTAL_PROPOSITION", ())
		self.TEXT_MAX_TURNS_WITHOUT_PROPOSITION = CyTranslator().getText("TXT_KEY_MAX_TURNS_WITHOUT_PROPOSITION", ())
		self.TEXT_PROBABILTY_TO_GET_THE_FIRST_UNIT = CyTranslator().getText("TXT_KEY_PROBABILTY_TO_GET_THE_FIRST_UNIT", ())
		self.TEXT_PROBABILTY_AVERAGE_TO_GET_THE_UNIT = CyTranslator().getText("TXT_KEY_PROBABILTY_AVERAGE_TO_GET_THE_UNIT", ())

		self.TEXT_COLOR_POSITIVE = CyTranslator().getText("TXT_KEY_COLOR_POSITIVE", ())
		self.TEXT_COLOR_NEGATIVE = CyTranslator().getText("TXT_KEY_COLOR_NEGATIVE", ())
		self.TEXT_COLOR_REVERT = CyTranslator().getText("TXT_KEY_COLOR_REVERT", ())

		self.xSelPt = 0
		self.ySelPt = 0

		if not bFromHallOfFame:
			self.replayInfo = CyGame().getReplayInfo()
			if self.replayInfo.isNone():
				self.replayInfo = CyReplayInfo()
				self.replayInfo.createInfo(gc.getGame().getActivePlayer())

		self.iTurn = self.replayInfo.getInitialTurn()
		self.showReplayScreen()

		return

	def drawTabs(self):

		screen = self.getScreen()
		
		self.Tabs = [self.REPLAY_TEXT, self.IMMIGRATION_TEXT]
		ActionTabs = [self.REPLAY_SCREEN_ID, self.IMMIGRATION_SCREEN_ID]
		NumTabs = len(self.Tabs)
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

			TabText = self.Tabs[iTab]
			TabText = localText.changeTextColor(TabText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))

			screen.setTextAt("OnTabTitle" + str(iTab), OnTabName + "Center", u"<font=4>" + TabText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, 0 , 33, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL,-1, -1)
			screen.hide(OnTabName + "Left")
			screen.hide(OnTabName + "Center")
			screen.hide(OnTabName + "Right")

			OffTabName = "OffTab" + str(iTab)
			screen.addPanel(OffTabName, "", "", False, False, TabWidth * iTab, self.H_SCREEN - BottomPanelHight, TabWidth, BottomPanelHight, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, 1111, iTab)
			screen.addDrawControl(OffTabName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_OFF").getPath(), TabWidth * iTab, self.H_SCREEN - BottomPanelHight, TabWidth, BottomPanelHight, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setTextAt("OffTabTitle" + str(iTab), OffTabName, u"<font=4>" + TabText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, EdgeWidth , 33, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, ActionTabs[iTab], -1)

		self.szExitTab = self.getNextWidgetName()
		screen.addPanel(self.szExitTab, "", "", False, False, TabWidth * NumTabs, self.H_SCREEN - BottomPanelHight, TabWidth, BottomPanelHight, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addDrawControl(self.szExitTab, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_OFF").getPath(), TabWidth * NumTabs, self.H_SCREEN - BottomPanelHight, TabWidth, BottomPanelHight, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setTextAt(self.getNextWidgetName(), self.szExitTab, u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, TabWidth - 30 , BottomPanelHight - 18, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

	def setTab(self, iTab, State):
		screen = self.getScreen()
		OnTabName = "OnTab" + str(iTab)
		if (State):
			self.disableAllTabs()
			screen.show(OnTabName + "Left")
			screen.show(OnTabName + "Center")
			screen.show(OnTabName + "Right")
			screen.hide("OffTab" + str(iTab))
		else:
			screen.hide(OnTabName + "Left")
			screen.hide(OnTabName + "Center")
			screen.hide(OnTabName + "Right")
			screen.show("OffTab" + str(iTab))

	def disableAllTabs(self):
		NumTabs = len(self.Tabs)
		for iTab in range(NumTabs):
			self.setTab(iTab, False)

	####################################################################################
	####################################################################################
	###	ShowReplayScreen
	####################################################################################
	####################################################################################

	def showReplayScreen(self):
		self.displayBackground()
		screen = self.getScreen()
		self.setTab(0, True)

		# Controls
		self.szForwardId = self.getNextWidgetName()
		self.szPlayId = self.getNextWidgetName()

		# Header...
		self.szHeader = self.getNextWidgetName()
		screen.setLabel(self.szHeader, "Background", u"<font=4b>" + localText.getText("TXT_KEY_REPLAY_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W_SCREEN / 2, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Minimap initialization
		self.H_MAP = (self.W_MAP * self.replayInfo.getMapHeight()) / self.replayInfo.getMapWidth()
		if (self.H_MAP > self.H_MAP_MAX):
			self.W_MAP = (self.H_MAP_MAX * self.replayInfo.getMapWidth()) / self.replayInfo.getMapHeight()
			self.H_MAP = self.H_MAP_MAX

		screen.setMinimapMap(self.replayInfo, self.X_MAP, self.X_MAP + self.W_MAP, self.Y_MAP, self.Y_MAP + self.H_MAP, self.Z_CONTROLS, false)
		screen.updateMinimapSection(True)
		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_REPLAY)
		screen.moveBackward(self.screnBackground)
		# add pane for text
		#mainPanelName = self.getNextWidgetName()
		#screen.addPanel(mainPanelName, "", "", True, True, self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_IN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.szAreaId = self.getNextWidgetName()
		screen.addListBoxGFC(self.szAreaId, "", self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.szAreaId, False)

		# Forward
		screen.setText(self.szForwardId, "Background", self.FORWARD_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_FORWARD, self.Y_FORWARD, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Play
		screen.setText(self.szPlayId, "Background", self.PLAY_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_PLAY, self.Y_PLAY, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, -1 )

		# Speed Slider
		self.szSliderTextId = self.getNextWidgetName()
		screen.setLabel(self.szSliderTextId, "Background", "<font=4>" + self.SPEED_TEXT + "<font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SPEED, self.Y_SPEED, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.szSliderId = self.getNextWidgetName()
		screen.addSlider(self.szSliderId, self.X_SLIDER, self.Y_SLIDER, self.W_SLIDER, self.H_SLIDER, self.iSpeed - 1, 0, self.NUM_SLIDER_STOPS-1, WidgetTypes.WIDGET_GENERAL, -1, -1, False);

		self.showEvents(self.iTurn, False)
		self.setTab(0, True)

		return

	####################################################################################
	####################################################################################
	###	ShowImmigrationScreen
	####################################################################################
	####################################################################################

	def showImmigrationScreen(self):
		screen = self.getScreen()
		self.displayBackground()
		self.setTab(1, True)

		self.szHeader = self.getNextWidgetName()
		screen.setLabel(self.szHeader, "Background", u"<font=4b>" + self.IMMIGRATION_TEXT.upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W_SCREEN / 2, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		

		info = self.replayInfo
		self.EuropeanPlayers = []
		self.aiPlayerToggle = []

		iNumPlayer = info.getNumPlayers()
		for iPlayer in range(iNumPlayer):
			if info.isEuropeanPlayer(iPlayer):
				self.EuropeanPlayers.append(iPlayer)
				self.aiPlayerToggle.append(True)
		
		self.iNumPlayers = len(self.EuropeanPlayers)
		self.drawGraphTab()
		self.displayImmigrationTable()
		
		return

	def displayImmigrationTable(self):
		screen = self.getScreen()
		# Create Table

		szTable = self.getNextLineName()
		iColumnCount = 6
		screen.addTableControlGFC(szTable, iColumnCount, self.X_CHART, self.Y_CHART, self.W_CHART, self.H_CHART, true, true, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader(szTable, 0, self.TEXT_LEADER_NAME, (self.W_CHART / iColumnCount) * 4 / 5)
		screen.setTableColumnHeader(szTable, 1, self.TEXT_TOTAL_RECRUIT_TURN, self.W_CHART/iColumnCount)
		screen.setTableColumnHeader(szTable, 2, self.TEXT_TOTAL_PROPOSITION, self.W_CHART/iColumnCount)
		screen.setTableColumnHeader(szTable, 3, self.TEXT_MAX_TURNS_WITHOUT_PROPOSITION, self.W_CHART/iColumnCount)
		screen.setTableColumnHeader(szTable, 4, self.TEXT_PROBABILTY_TO_GET_THE_FIRST_UNIT, self.W_CHART/iColumnCount)
		screen.setTableColumnHeader(szTable, 5, self.TEXT_PROBABILTY_AVERAGE_TO_GET_THE_UNIT, (self.W_CHART / iColumnCount) * 6 / 5)

		info = self.replayInfo

		for iPlayer in range(self.iNumPlayers):
			iRow = iPlayer
			p = self.EuropeanPlayers[iPlayer]
			screen.appendTableRow(szTable)
			textColorR = info.getPlayerTextColorR(p)
			textColorG = info.getPlayerTextColorG(p)
			textColorB = info.getPlayerTextColorB(p)
			textColorA = info.getPlayerTextColorA(p)
			name = info.getPlayerName(p)
			strPlayer = u"<color=%d,%d,%d,%d>%s</color>" %(textColorR, textColorG, textColorB, textColorA, name)
			maxTurn = info.getMaxTurnWithoutPropositionForUnit(p, self.selectedUnitTypes)
			totalImmigration = info.getTotalImmigrationAskedForUnit(p, self.selectedUnitTypes)
			if maxTurn == 0:
				maxTurn = totalImmigration
			firstUnitProba = info.getPlayerFirstUnitImmigrationProbabilityForUnit(p, self.selectedUnitTypes)
			averageImmigrationProba = info.getPlayerAverageImmigrationProbabilityForUnit(p, self.selectedUnitTypes)
			szFirstUnitProba = u"<font=2>%.2f</font>"%((1-firstUnitProba)*100)
			szAverageImmigrationProba = u"<font=2>%.2f</font>"%((1-averageImmigrationProba)*100)
			if(firstUnitProba == 0):
				szFirstUnitProba = u"<font=2>-</font>"
				szAverageImmigrationProba = u"<font=2>-</font>"
			else:
				if firstUnitProba >= 0.6:
					szFirstUnitProba = self.TEXT_COLOR_POSITIVE + szFirstUnitProba + self.TEXT_COLOR_REVERT 
				elif firstUnitProba < 0.4:
					szFirstUnitProba = self.TEXT_COLOR_NEGATIVE + szFirstUnitProba + self.TEXT_COLOR_REVERT

				if averageImmigrationProba >= 0.6:
					szAverageImmigrationProba = self.TEXT_COLOR_POSITIVE + szAverageImmigrationProba + self.TEXT_COLOR_REVERT 
				elif averageImmigrationProba < 0.4:
					szAverageImmigrationProba = self.TEXT_COLOR_NEGATIVE + szAverageImmigrationProba + self.TEXT_COLOR_REVERT 
		
			screen.setTableText(szTable, 0, iRow, strPlayer, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText(szTable, 1, iRow, u"<font=2>%d</font>"%(totalImmigration), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText(szTable, 2, iRow, u"<font=2>%d</font>"%(info.getPlayerTotalImmigrationForUnit(p, self.selectedUnitTypes)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText(szTable, 3, iRow, u"<font=2>%d</font>"%(maxTurn), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText(szTable, 4, iRow, szFirstUnitProba, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText(szTable, 5, iRow, szAverageImmigrationProba, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					
	def updateUnitAnimation(self):
		screen = self.getScreen()
		self.eUnitGraphicGFC = self.getNextWidgetName()
		bShowBackground = False
		#screen.addUnitGraphicGFC(self.eUnitGraphicGFC, self.selectedUnitTypes, -1, self.X_UNIT_ANIMATION, self.Y_UNIT_ANIMATION, self.W_UNIT_ANIMATION, self.H_UNIT_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_UNIT_ANIMATION, self.Z_ROTATION_UNIT_ANIMATION, self.SCALE_ANIMATION, bShowBackground)
		unitInfo = gc.getUnitInfo(self.selectedUnitTypes)
		iProfession = unitInfo.getDefaultProfession()
		screen.setImageButton(self.eUnitGraphicGFC, unitInfo.getArtInfo(0, iProfession).getFullLengthIcon(), self.X_UNIT_ANIMATION, self.Y_UNIT_ANIMATION, self.W_UNIT_ANIMATION, self.H_UNIT_ANIMATION,  WidgetTypes.WIDGET_GENERAL, -1, -1)
						
	def drawGraphTab(self):

		info = self.replayInfo
		self.iTurn = info.getInitialTurn()
		
		self.graphEnd		= info.getFinalTurn() - 1
		self.graphZoom		= self.graphEnd - self.iTurn

		self.selectedUnitTypes = UnitTypes.UNIT_STATESMAN 

		self.drawPermanentGraphWidgets()
		self.drawGraph()

	def drawPermanentGraphWidgets(self):

		screen = self.getScreen()
		info = self.replayInfo
		
		self.H_LEGEND = 2 * self.Y_LEGEND_MARGIN + self.iNumPlayers * self.H_LEGEND_TEXT + 3
		self.Y_LEGEND = self.Y_GRAPH + self.H_GRAPH - self.H_LEGEND
		
		self.LEGEND_PANEL_ID = self.getNextWidgetName()
		screen.addPanel(self.LEGEND_PANEL_ID, "", "", true, true, self.X_LEGEND, self.Y_LEGEND, self.W_LEGEND, self.H_LEGEND, PanelStyles.PANEL_STYLE_IN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.LEGEND_CANVAS_ID = self.getNextWidgetName()

		self.drawLegend()

		self.graphLeftButtonID = self.getNextWidgetName()
		screen.setButtonGFC( self.graphLeftButtonID, u"", "", self.X_LEFT_BUTTON, self.Y_LEFT_BUTTON, self.W_LEFT_BUTTON, self.H_LEFT_BUTTON, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		self.graphRightButtonID = self.getNextWidgetName()
		screen.setButtonGFC( self.graphRightButtonID, u"", "", self.X_RIGHT_BUTTON, self.Y_RIGHT_BUTTON, self.W_RIGHT_BUTTON, self.H_RIGHT_BUTTON, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.enable(self.graphLeftButtonID, False)
		screen.enable(self.graphRightButtonID, False)

		# Dropdown Box
		self.szGraphDropdownWidget = self.getNextWidgetName()
		screen.addDropDownBoxGFC(self.szGraphDropdownWidget, self.X_DEMO_DROPDOWN, self.Y_DEMO_DROPDOWN, self.W_DEMO_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		
		numUnitInfos = gc.getNumUnitInfos()
		for unitType in range(numUnitInfos - 1, 0, -1):
			UnitInfo = gc.getUnitInfo(unitType)
			if UnitInfo.getProbaImmigration() > 0 and self.hasStatisticsForUnitType(unitType):			
				screen.addPullDownString(self.szGraphDropdownWidget, UnitInfo.getDescription(), unitType, unitType, False )

		self.dropDownTurns = []
		self.szTurnsDropdownWidget = self.getNextWidgetName()
		screen.addDropDownBoxGFC(self.szTurnsDropdownWidget, self.X_ZOOM_DROPDOWN, self.Y_ZOOM_DROPDOWN, self.W_ZOOM_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		
		start = info.getInitialTurn()
		now   = info.getFinalTurn() 
		nTurns = now - start - 1
		screen.addPullDownString(self.szTurnsDropdownWidget, localText.getText("TXT_KEY_INFO_ENTIRE_HISTORY", ()), 0, 0, False)
		self.dropDownTurns.append(nTurns)
		iCounter = 1
		last = 50
		while (last < nTurns):
			screen.addPullDownString(self.szTurnsDropdownWidget, localText.getText("TXT_KEY_INFO_NUM_TURNS", (last,)), iCounter, iCounter, False)
			self.dropDownTurns.append(last)
			iCounter += 1
			last += 50

		self.updateUnitAnimation()

	def updateGraphButtons(self):
		screen = self.getScreen()
		screen.enable(self.graphLeftButtonID, self.graphEnd - self.graphZoom > CyGame().getStartTurn())
		screen.enable(self.graphRightButtonID, self.graphEnd < CyGame().getGameTurn() - 1)

	def checkGraphBounds(self):
		start = CyGame().getStartTurn()
		end   = CyGame().getGameTurn() - 1
		if (self.graphEnd - self.graphZoom < start):
			self.graphEnd = start + self.graphZoom
		if (self.graphEnd > end):
			self.graphEnd = end

	def zoomGraph(self, zoom):
		self.graphZoom = zoom
		self.checkGraphBounds()
		self.updateGraphButtons()

	def slideGraph(self, right):
		self.graphEnd += right
		self.checkGraphBounds()
		self.updateGraphButtons()

	def hasStatisticsForUnitType(self, unit):
		info = self.replayInfo
		iInitialTurn = info.getInitialTurn()
		iFinalTurn = info.getFinalTurn()
			
		for i in range(self.iNumPlayers):
			iPlayer = self.EuropeanPlayers[i]
			for iTurn in range(iInitialTurn, iFinalTurn + 1):
				score = info.getPlayerImmigrationForUnit(iPlayer, iTurn, unit)
				if (score > 0):
					return True
		return False

	def drawGraphYLabels(self, iMin, iMax):
		screen = self.getScreen()
		yStart = (self.Y_GRAPH + self.H_GRAPH) - 15
		xLabel  = self.X_RIGHT_LABEL + 20
		iIncrement = self.getIncrementValue(iMax)
		iGap = (iMax - iMin)
		iNumLabels = int(iGap / iIncrement) + 1
		if iGap == 0:
			return
		
		for iLabelPosition in range(iNumLabels):
			iValue = iMin + iLabelPosition*iIncrement
			yPosition = yStart - int(((iValue - iMin) * self.H_GRAPH)/ (iGap))
			screen.setLabel( self.getNextLineName(), "", u"<font=2>%d</font>"%(iValue), CvUtil.FONT_RIGHT_JUSTIFY, xLabel, yPosition, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			if(iLabelPosition > 0):
				screen.addDDSGFC(self.getNextLineName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ROUTES_SMALL_LINE").getPath(), self.X_LEFT_LABEL - 50, yPosition + 14, self.W_GRAPH, 3,  WidgetTypes.WIDGET_GENERAL, -1, -1 )
	
	def getIncrementValue(self, iMax):
		levels = [0, 10, 50, 100, 500, 1000, 2000, 5000, 10000, 50000]
		numLevels = len(levels)
		for iLevel in range(numLevels):
			if iMax <= levels[iLevel]:
				return levels[iLevel]/10
		return 10000

	def drawGraph(self):

		screen = self.getScreen()
		self.deleteAllLines()
	
		# Draw the graph widget
		self.GRAPH_CANVAS_ID = self.getNextLineName()
		xOffset = 5
		yOffset = 5
		screen.addDrawControl(self.GRAPH_CANVAS_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG").getPath(), self.X_GRAPH - xOffset, self.Y_GRAPH - yOffset, self.W_GRAPH + 2*xOffset, self.H_GRAPH + 2*yOffset, WidgetTypes.WIDGET_GENERAL, -1, -1)
		info = self.replayInfo

		# Compute max score
		iMax = 0
		thisTurn = info.getFinalTurn()
		startTurn = info.getInitialTurn()

		if (self.graphZoom == 0 or self.graphEnd == 0):
			firstTurn = startTurn
		else:
			firstTurn = self.graphEnd - self.graphZoom

		if (self.graphEnd == 0):
			lastTurn  = thisTurn #- 1 # all civs haven't neccessarily got a score for the current turn
		else:
			lastTurn  = self.graphEnd

		self.drawGraphLines()

		xLabelOffset = 10
		
		# Draw x-labels
		self.drawXLabel( screen, firstTurn, self.X_LEFT_LABEL + xLabelOffset,  CvUtil.FONT_LEFT_JUSTIFY  )
		self.drawXLabel( screen, lastTurn,  self.X_RIGHT_LABEL, CvUtil.FONT_RIGHT_JUSTIFY )

		# Don't draw anything the first turn
		if (firstTurn >= lastTurn):
			return
				
		# Compute iMax and iMin
		iMax = 1
		iMin = 0

		iInitialTurn = info.getInitialTurn()
		iFinalTurn = info.getFinalTurn()
			
		for i in range(self.iNumPlayers):
			iPlayer = self.EuropeanPlayers[i]
			for iTurn in range(firstTurn, lastTurn + 1):
				score = info.getPlayerImmigrationForUnit(iPlayer, iTurn, self.selectedUnitTypes)
				if (iMax < score):
					iMax = score
				if (iMin > score):
					iMin = score

		yFactor = (1.0 * self.H_GRAPH / (1.01 * (iMax - iMin)))
		xFactor = (1.0 * self.W_GRAPH / (1.05 * (lastTurn - firstTurn)))

		if (lastTurn - firstTurn > 10):
			turn = (firstTurn + lastTurn) / 2
			self.drawXLabel ( screen, turn, self.X_GRAPH + int(xFactor * (turn - firstTurn) + xLabelOffset) )
		if (lastTurn - firstTurn > 20):
			turn = firstTurn + (lastTurn - firstTurn) / 4
			self.drawXLabel ( screen, turn, self.X_GRAPH + int(xFactor * (turn - firstTurn) + xLabelOffset) )
			turn = firstTurn + 3 * (lastTurn - firstTurn) / 4
			self.drawXLabel ( screen, turn, self.X_GRAPH + int(xFactor * (turn - firstTurn) + xLabelOffset) )

		self.drawGraphYLabels(iMin, iMax)
		
		# Draw the lines
		for p in range(self.iNumPlayers):
			iPlayer = self.EuropeanPlayers[p]
			if (self.aiPlayerToggle[p]):
				color = info.getColor(iPlayer)
				oldX = -1
				oldY = self.H_GRAPH
				turn = lastTurn

				while (turn >= firstTurn):

					score = info.getPlayerImmigrationForUnit(iPlayer, turn - startTurn, self.selectedUnitTypes)
					y = self.H_GRAPH - int(yFactor * (score - iMin))
					x = int(xFactor * (turn - firstTurn)) + xLabelOffset

					if (x < oldX):
						if (y != self.H_GRAPH or oldY != self.H_GRAPH): # don't draw if score is constant zero
							self.drawLine(screen, self.GRAPH_CANVAS_ID, oldX, oldY, x, y, color)
						oldX = x
						oldY = y
					elif (oldX == -1):
						oldX = x
						oldY = y

					turn -= 1

		return

	def drawLegend(self):
		screen = self.getScreen()

		yLine = self.Y_LEGEND_LINE
		yText = self.Y_LEGEND + self.Y_LEGEND_TEXT

		self.H_LEGEND = 2 * self.Y_LEGEND_MARGIN + self.iNumPlayers * self.H_LEGEND_TEXT + 3
		self.Y_LEGEND = self.Y_GRAPH + self.H_GRAPH - self.H_LEGEND
		info = self.replayInfo

		screen.addDrawControl(self.LEGEND_CANVAS_ID, None, self.X_LEGEND, self.Y_LEGEND, self.W_LEGEND_LINE, self.H_LEGEND, WidgetTypes.WIDGET_GENERAL, -1, -1)

		for iPlayer in range(self.iNumPlayers):
			p = self.EuropeanPlayers[iPlayer]
			lineColor = info.getColor(p)
			textColorR = info.getPlayerTextColorR(p)
			textColorG = info.getPlayerTextColorG(p)
			textColorB = info.getPlayerTextColorB(p)
			textColorA = info.getPlayerTextColorA(p)
			name = info.getPlayerName(p)

			if (self.aiPlayerToggle[iPlayer]):
				self.drawLine(screen, self.LEGEND_CANVAS_ID, self.X_LEGEND_LINE, yLine, self.X_LEGEND_LINE + self.W_LEGEND_LINE, yLine, lineColor)
			
			str = u"<color=%d,%d,%d,%d>%s</color>" %(textColorR, textColorG, textColorB, textColorA, name[:22])
			szTitle = self.getNextWidgetName()
			screen.setText(szTitle, "", u"<font=2>" + str + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_LEGEND + self.X_LEGEND_TEXT, yText, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.LEGEND_LINE, iPlayer)

			yLine += self.H_LEGEND_TEXT
			yText += self.H_LEGEND_TEXT

	def drawGraphLines(self):
		screen = self.getScreen()

		if (self.xSelPt != 0 or self.ySelPt != 0):
			screen.addLineGFC(self.GRAPH_CANVAS_ID, self.GRAPH_H_LINE, 0, self.ySelPt, self.W_GRAPH, self.ySelPt, gc.getInfoTypeForString("COLOR_GREY"))
			screen.addLineGFC(self.GRAPH_CANVAS_ID, self.GRAPH_V_LINE, self.xSelPt, 0, self.xSelPt, self.H_GRAPH, gc.getInfoTypeForString("COLOR_GREY"))
		else:
			screen.addLineGFC(self.GRAPH_CANVAS_ID, self.GRAPH_H_LINE, -1, -1, -1, -1, gc.getInfoTypeForString("COLOR_GREY"))
			screen.addLineGFC(self.GRAPH_CANVAS_ID, self.GRAPH_V_LINE, -1, -1, -1, -1, gc.getInfoTypeForString("COLOR_GREY"))


	def drawXLabel(self, screen, turn, x, just = CvUtil.FONT_CENTER_JUSTIFY):
		screen.setLabel( self.getNextLineName(), "", u"<font=2>" + self.getTurnDate(turn) + u"</font>", just , x , self.Y_LABEL, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
	
	def getTurnDate(self,turn):

		year = self.replayInfo.getTurnYear(turn)

		if (year < 0):
			return localText.getText("TXT_KEY_TIME_BC", (-year,))
		else:
			return localText.getText("TXT_KEY_TIME_AD", (year,))

	def drawLine (self, screen, canvas, x0, y0, x1, y1, color):
		screen.addLineGFC(canvas, self.getNextLineName(), x0, y0 + 1, x1, y1 + 1, color)
		screen.addLineGFC(canvas, self.getNextLineName(), x0 + 1, y0, x1 + 1, y1, color)
		screen.addLineGFC(canvas, self.getNextLineName(), x0, y0, x1, y1, color)


	def displayBackground(self):
		screen = self.getScreen()
		self.deleteAllWidgets()
		self.deleteAllLines()
		self.setPlaying(False)
		
		screen.setDimensions(0, 0, self.W_SCREEN, self.H_SCREEN)
		self.screnBackground = self.getNextWidgetName();
		screen.addDDSGFC(self.screnBackground, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TITLE").getPath(), 0, 0, self.W_SCREEN, 55, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.showWindowBackground(False)
		
		self.drawTabs()
		
		return

	def showEvents(self, iTurn, bSilent):

		self.iTurn = iTurn
		screen = self.getScreen()

		if (iTurn < self.replayInfo.getInitialTurn()):
			self.iTurn = self.replayInfo.getInitialTurn()
			self.iLastTurnShown = -1
			return
		elif iTurn > self.replayInfo.getFinalTurn():
			self.iTurn = self.replayInfo.getInitialTurn()
			self.iLastTurnShown = -1
			self.resetData()
			self.showEvents(self.iTurn, False)
			return


		szTurnDate = CyGameTextMgr().getDateStr(self.iTurn, false, self.replayInfo.getCalendar(), self.replayInfo.getStartYear(), self.replayInfo.getGameSpeed())
		screen.deleteWidget(self.szHeader)
		screen.setLabel(self.szHeader, "Background", u"<font=4b>" + szTurnDate + u"<font>", CvUtil.FONT_CENTER_JUSTIFY, self.W_SCREEN / 2, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		events = []
		bFound = False
		bDone = False
		i = 0
		while (i < self.replayInfo.getNumReplayMessages() and not bDone):
			if 	(self.replayInfo.getReplayMessageTurn(i) <= iTurn and self.replayInfo.getReplayMessageTurn(i) > self.iLastTurnShown):
				events.append(i)
				bFound = True
			else:
				if (bFound):
					bDone = True
			i += 1

		for iLoopEvent in events:

			szEventDate = CyGameTextMgr().getDateStr(self.replayInfo.getReplayMessageTurn(iLoopEvent), false, self.replayInfo.getCalendar(), self.replayInfo.getStartYear(), self.replayInfo.getGameSpeed())

			szText = self.replayInfo.getReplayMessageText(iLoopEvent)
			iX = self.replayInfo.getReplayMessagePlotX(iLoopEvent)
			iY = self.replayInfo.getReplayMessagePlotY(iLoopEvent)
			eMessageType = self.replayInfo.getReplayMessageType(iLoopEvent)
			eColor = self.replayInfo.getReplayMessageColor(iLoopEvent)


			if (szText != "" and not bSilent):
				szTextNoColor = re.sub("<color=.*?>", "", szText)
				szText = re.sub("</color>", "", szTextNoColor)

				szText =  u"<font=2>" + szEventDate + u": " + szText + u"</font>"
				szText =localText.changeTextColor(szText, eColor)
				screen.prependListBoxString(self.szAreaId, szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

			if (eMessageType == ReplayMessageTypes.REPLAY_MESSAGE_PLOT_OWNER_CHANGE):
				iPlayer = self.replayInfo.getReplayMessagePlayer(iLoopEvent)
				if iPlayer != -1:
					screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_REPLAY, iX, iY, self.replayInfo.getColor(iPlayer), 0.6)
				else:
					screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_REPLAY, iX, iY, gc.getInfoTypeForString("COLOR_CLEAR"), 0.6)
			else:
				if (iX > -1 and iY > -1 and not bSilent):
					screen.minimapFlashPlot(iX, iY, gc.getInfoTypeForString("COLOR_WHITE"), 10)
		if (self.yMessage > self.H_TEXT):
			screen.scrollableAreaScrollToBottom(self.szAreaId)

		self.iLastTurnShown = iTurn

	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def deleteAllWidgets(self, iNumPermanentWidgets = 0):
		if(iNumPermanentWidgets == 0):
			self.deleteAllLines()
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while (i >= iNumPermanentWidgets):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = iNumPermanentWidgets
		self.yMessage = 5

	def lineName(self,i):
		return self.LINE_ID + str(i)

	def getNextLineName(self):
		name = self.lineName(self.nLineCount)
		self.nLineCount += 1
		return name

	def deleteAllLines(self):
		screen = self.getScreen()
		i = 0
		while (i < self.nLineCount):
			screen.deleteWidget(self.lineName(i))
			i += 1
		self.nLineCount = 0

	def resetMinimapColor(self):
		screen = self.getScreen()
		for iX in range(self.replayInfo.getMapWidth()):
			for iY in range(self.replayInfo.getMapHeight()):
				screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_REPLAY, iX, iY, gc.getInfoTypeForString("COLOR_CLEAR"), 0.6)

	def resetData(self):
		screen = self.getScreen()
		self.resetMinimapColor()
		screen.clearListBoxGFC(self.szAreaId)

	def setPlaying(self, bPlaying):
		if bPlaying != self.bPlaying:
			self.bPlaying = bPlaying
			screen = self.getScreen()
			if (self.bPlaying):
				screen.hide(self.szForwardId)
				screen.modifyString(self.szPlayId, self.STOP_TEXT, 0)
				screen.show(self.szSliderId)
				screen.show(self.szSliderTextId)
			else:
				screen.show(self.szForwardId)
				screen.modifyString(self.szPlayId, self.PLAY_TEXT, 0)
				screen.hide(self.szSliderId)
				screen.hide(self.szSliderTextId)

	# handle the input for this screen...
	def handleInput (self, inputClass):

		szWidgetName = inputClass.getFunctionName() + str(inputClass.getID())
		code = inputClass.getNotifyCode()
		if (code == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):
				if (inputClass.getData1() == self.REPLAY_SCREEN_ID):
					self.showReplayScreen()
				elif(inputClass.getData1() == self.IMMIGRATION_SCREEN_ID):
					self.showImmigrationScreen()
				elif inputClass.getData1() == self.LEGEND_LINE:
					playerIndex = inputClass.getData2()
					self.aiPlayerToggle[playerIndex] = not self.aiPlayerToggle[playerIndex]
					self.drawLegend()
					self.drawGraph()

			if (inputClass.getFunctionName() == self.EXIT_ID):
				screen = self.getScreen()
				screen.hideScreen()

			elif (szWidgetName == self.szPlayId):
				self.setPlaying(not self.bPlaying)
				if self.bPlaying:
					if self.iTurn >= self.replayInfo.getFinalTurn():
						self.resetData()
						self.showEvents(self.replayInfo.getInitialTurn()-1, False)
					else:
						self.showEvents(self.iTurn + 1, False)
			elif (szWidgetName == self.szForwardId):
				if (not self.bPlaying):
					self.showEvents(self.iTurn + 1, False)
			# Slide graph
			elif (szWidgetName == self.graphLeftButtonID):
				self.slideGraph(- 2 * self.graphZoom / 5)
				self.drawGraph()

			elif (szWidgetName == self.graphRightButtonID):
				self.slideGraph(2 * self.graphZoom / 5)
				self.drawGraph()
			
		elif (code == NotifyCode.NOTIFY_SLIDER_NEWSTOP):
			if (szWidgetName == self.szSliderId):
				screen = self.getScreen()
				self.iSpeed = inputClass.getData() + 1
		elif (code == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (szWidgetName == self.szGraphDropdownWidget):
				screen = self.getScreen()
				iIndex = screen.getSelectedPullDownID(szWidgetName)
				self.selectedUnitTypes = screen.getPullDownData(szWidgetName, iIndex)
				screen.deleteWidget(self.eUnitGraphicGFC)
				self.updateUnitAnimation()
				self.drawGraph()
				self.displayImmigrationTable()
			elif (szWidgetName == self.szTurnsDropdownWidget):
				self.zoomGraph(self.dropDownTurns[inputClass.getData()])
				self.drawGraph()

		return 0

	def update(self, fDelta):

		screen = self.getScreen()

		screen.updateMinimap(fDelta)

		if self.bPlaying:
			if self.iTurn < self.replayInfo.getFinalTurn():
				self.fLastUpdate += max(fDelta, 0.02)
				iTurnJump = int(self.fLastUpdate / self.TIME_STEP[self.iSpeed - 1])
	
				if (iTurnJump > 0):
					iTurnJump = 1  # we used to allow showing multiple turns at once, but it didn't work very well
					self.fLastUpdate = 0.0
					self.showEvents(self.iTurn + iTurnJump, False)

			elif self.iTurn >= self.replayInfo.getFinalTurn():
				self.setPlaying(False)
				self.fLastUpdate = 0.0

