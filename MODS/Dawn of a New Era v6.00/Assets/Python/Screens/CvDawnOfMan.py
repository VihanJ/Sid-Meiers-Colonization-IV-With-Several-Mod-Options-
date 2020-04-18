## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

import CvUtil
import ScreenInput
from CvPythonExtensions import *

ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()
gc = CyGlobalContext()

class CvDawnOfMan:
	"Dawn of man screen"
	def __init__(self, iScreenID):
		self.iScreenID = iScreenID
		self.CHOOSE_SPECIALIST = 1
		
		self.WIDGET_ID = "DawnOfManScreenWidget"
		self.nWidgetCount = 0

	def getScreen(self):
		return CyGInterfaceScreen( "CvDawnOfMan", self.iScreenID )
		
	def interfaceScreen(self):
		'Use a popup to display the opening text'
		if ( CyGame().isPitbossHost() ):
			return

		self.calculateSizesAndPositions()

		self.player = gc.getPlayer(gc.getGame().getActivePlayer())

		# Create screen
		screen = self.getScreen()
		screen.setCloseOnEscape(False)
		screen.showScreen(PopupStates.POPUPSTATE_QUEUED, False)
		screen.showWindowBackground( False )
		screen.setDimensions(self.X_SCREEN, screen.centerY(self.Y_SCREEN), self.W_SCREEN, self.H_SCREEN)
		screen.enableWorldSounds( false )

		# Create panels

		# Main
		szMainPanel = "DawnOfManMainPanel"
		screen.addPanel("DawnBackGroundPanel", "", "", true, true, self.X_MAIN_PANEL - 50, self.Y_MAIN_PANEL - 50, self.W_MAIN_PANEL + 100, self.H_MAIN_PANEL + 100, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("DawnBackGroundPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_ROYAL_CHARTER_BG").getPath(), self.X_MAIN_PANEL - 50, self.Y_MAIN_PANEL - 50, self.W_MAIN_PANEL + 100, self.H_MAIN_PANEL + 100, WidgetTypes.WIDGET_GENERAL, -1, -1 )
	
		screen.addPanel( szMainPanel, "", "", true, true, self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Top
		szHeaderPanel = "DawnOfManHeaderPanel"
		screen.addPanel( szHeaderPanel, "", "", true, false, self.X_HEADER_PANEL, self.Y_HEADER_PANEL, self.W_HEADER_PANEL, self.H_HEADER_PANEL, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Bottom
		szTextPanel = "DawnOfManTextPanel"
		screen.addPanel( szTextPanel, "", "", true, true, self.X_TEXT_PANEL, self.Y_TEXT_PANEL, self.W_TEXT_PANEL, self.H_TEXT_PANEL, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Add contents

		# Leaderhead graphic
		szLeaderPanel = "DawnOfManLeaderPanel"
		screen.addPanel( szLeaderPanel, "", "", true, false, self.X_LEADER_ICON - 3, self.Y_LEADER_ICON - 5, self.W_LEADER_ICON + 6, self.H_LEADER_ICON + 8, PanelStyles.PANEL_STYLE_DAWNTOP, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addLeaderheadGFC("LeaderHead", self.player.getLeaderType(), AttitudeTypes.ATTITUDE_PLEASED, self.X_LEADER_ICON + 5, self.Y_LEADER_ICON + 5, self.W_LEADER_ICON - 10, self.H_LEADER_ICON - 10, WidgetTypes.WIDGET_GENERAL, -1, -1)

		szNameText = u"<font=4b>"
		szNameText += gc.getLeaderHeadInfo(self.player.getLeaderType()).getDescription() + u"</font>"
		szNameText += "\n- " + self.player.getCivilizationDescription(0) + " -\n"
		szNameText += u"<font=2>" + CyGameTextMgr().parseLeaderTraits(self.player.getLeaderType(), self.player.getCivilizationType(), True, False) + u"</font>"

		screen.addMultilineText( "NameText", szNameText, self.X_LEADER_TITLE_TEXT, self.Y_LEADER_TITLE_TEXT, self.W_LEADER_TITLE_TEXT, self.H_LEADER_TITLE_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

		
		screen.addMultilineText( "StartingUnitText", localText.getText("TXT_KEY_DAWN_OF_MAN_SCREEN_STARTING_UNITS", ()), self.X_LEADER_ICON, self.Y_STATS_TEXT + 5 + self.H_CIV_PANEL + 104, self.W_STATS_TEXT - (self.iMarginSpace * 3), self.H_STATS_TEXT - (self.iMarginSpace * 4), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		# Fancy icon things
		screen.addDDSGFC( "IconLeft", ArtFileMgr.getCivilizationArtInfo(gc.getCivilizationInfo(self.player.getCivilizationType()).getArtDefineTag()).getButton(), self.X_FANCY_ICON1 , self.Y_FANCY_ICON , self.WH_FANCY_ICON, self.WH_FANCY_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		#screen.addDDSGFC( "IconRight", ArtFileMgr.getCivilizationArtInfo(gc.getCivilizationInfo(self.player.getCivilizationType()).getArtDefineTag()).getButton(), self.X_FANCY_ICON2 , self.Y_FANCY_ICON , self.WH_FANCY_ICON, self.WH_FANCY_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Main Body text
		szDawnTitle = u"<font=4>" + localText.getText("TXT_KEY_ROYAL_CHARTER_TITLE", ()).upper() + u"</font>"
		screen.setLabel("DawnTitle", "Background", szDawnTitle, CvUtil.FONT_CENTER_JUSTIFY, self.X_TEXT_PANEL + (self.W_TEXT_PANEL / 2), self.Y_TEXT_PANEL + 15, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		eKingPlayer = self.player.getParent()
		if (eKingPlayer != PlayerTypes.NO_PLAYER):
			kingPlayer = gc.getPlayer(eKingPlayer)
		else:
			kingPlayer = self.player
		bodyString = localText.getText("TXT_KEY_ROYAL_CHARTER_BODY_2", (CyGameTextMgr().getTimeStr(gc.getGame().getGameTurn(), false), kingPlayer.getCivilizationShortDescriptionKey(), self.player.getNameKey()))
		screen.addMultilineText( "BodyText", bodyString, self.X_TEXT_PANEL + self.iMarginSpace, self.Y_TEXT_PANEL + self.iMarginSpace + self.iTEXT_PANEL_MARGIN, self.W_TEXT_PANEL - (self.iMarginSpace * 2), self.H_TEXT_PANEL - (self.iMarginSpace * 2) - 75, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		pActivePlayer = gc.getPlayer(CyGame().getActivePlayer())
		pLeaderHeadInfo = gc.getLeaderHeadInfo(pActivePlayer.getLeaderType())
		screen.setSoundId(CyAudioGame().Play2DSoundWithId(pLeaderHeadInfo.getDiploPeaceMusicScriptIds(0)))

		self.drawContents()

	def drawContents(self):
	
		player = self.player

		self.deleteAllWidgets()

		screen = self.getScreen()

		screen.setButtonGFC(self.getNextWidgetName(), localText.getText("TXT_KEY_SCREEN_CONTINUE", ()), "", self.X_EXIT, self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )

		# Starting Units
		pPlot = player.getStartingPlot()

		iUnit = 0
		(unit, iter) = player.firstUnit()
		while(unit):
			screen.setImageButton(self.getNextWidgetName(), gc.getUnitInfo(unit.getUnitType()).getButton(), self.X_LEADER_ICON + 2*(self.WH_FANCY_ICON * iUnit)/3, self.Y_STATS_TEXT + 30 + self.H_CIV_PANEL + 104, 2*(self.WH_FANCY_ICON)/3, 2*(self.WH_FANCY_ICON)/3, WidgetTypes.WIDGET_GENERAL, self.CHOOSE_SPECIALIST, unit.getID())
			iUnit += 1
			(unit, iter) = player.nextUnit(iter)	

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

	def handleInput( self, inputClass ):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):
				if (inputClass.getData1() == self.CHOOSE_SPECIALIST):
					pPlayer = self.player
					pUnit = pPlayer.getUnit(inputClass.getData2())
					if not gc.getUnitInfo(pUnit.getUnitType()).isMechUnit():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_CHOOSE_START_SPECIALIST)
						popupInfo.setData1(inputClass.getData2())
						CyInterface().addPopup(popupInfo, CyGame().getActivePlayer(), true, true)
		return 0

	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList

		if eWidgetType == WidgetTypes.WIDGET_GENERAL:
			if iData1 == self.CHOOSE_SPECIALIST:
				pPlayer = self.player
				pUnit = pPlayer.getUnit(iData2)
				if not gc.getUnitInfo(pUnit.getUnitType()).isMechUnit():
					unit_description = u"<font=2b>" + gc.getUnitInfo(pUnit.getUnitType()).getDescription() + u"</font>"
					unit_description = localText.changeTextColor(unit_description, gc.getInfoTypeForString("COLOR_UNIT_TEXT"))
					return  unit_description + u"\n" + localText.getText("TXT_KEY_MODIFY_UNIT_TYPE", ())
		return u""

	def update(self, fDelta):
		if (CyInterface().isDirty(InterfaceDirtyBits.DawnOfMan_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.DawnOfMan_DIRTY_BIT, False)
			# draw the contents
			self.drawContents()

	def onClose(self):
		CyInterface().setSoundSelectionReady(true)
		return 0

	def calculateSizesAndPositions(self):
		self.X_SCREEN = 0
		self.Y_SCREEN = 0

		screen = CyGInterfaceScreen("CvDawnOfMan", self.iScreenID)

		self.W_SCREEN = screen.getXResolution()
		self.H_SCREEN = screen.getYResolution()

		self.H_CIV_PANEL = 80
		self.W_MAIN_PANEL = 750

		self.H_MAIN_PANEL = 525
		self.X_MAIN_PANEL = (self.W_SCREEN/2) - (self.W_MAIN_PANEL/2)

		self.Y_MAIN_PANEL = 70

		self.iMarginSpace = 15

		self.X_HEADER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_HEADER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
		self.W_HEADER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
		self.H_HEADER_PANEL = int(self.H_MAIN_PANEL * (2.0 / 5.0)) + 60

		self.X_LEADER_ICON = self.X_HEADER_PANEL + self.iMarginSpace
		self.Y_LEADER_ICON = self.Y_HEADER_PANEL + self.iMarginSpace
		self.H_LEADER_ICON = self.H_HEADER_PANEL - (15 * 2)
		self.W_LEADER_ICON = int(self.H_LEADER_ICON / 1.272727)


		self.WH_FANCY_ICON = 64
		self.X_FANCY_ICON1 = self.X_LEADER_ICON + self.W_LEADER_ICON + self.iMarginSpace
		self.X_FANCY_ICON2 = self.X_LEADER_ICON + (self.W_HEADER_PANEL - (self.iMarginSpace * 2) - self.WH_FANCY_ICON)
		self.Y_FANCY_ICON = (self.Y_HEADER_PANEL + self.iMarginSpace + 6) - 6

		self.X_LEADER_TITLE_TEXT = (self.X_FANCY_ICON1+self.WH_FANCY_ICON)+((self.X_FANCY_ICON2 - (self.X_FANCY_ICON1+self.WH_FANCY_ICON))/2) - ((self.W_HEADER_PANEL / 3)/2) - 25

		self.Y_LEADER_TITLE_TEXT = self.Y_HEADER_PANEL + self.iMarginSpace + 6
		self.W_LEADER_TITLE_TEXT = self.W_HEADER_PANEL / 3 + 50
		self.H_LEADER_TITLE_TEXT = self.H_HEADER_PANEL / 3

		self.X_STATS_TEXT = self.X_FANCY_ICON1

		self.Y_STATS_TEXT = self.Y_LEADER_TITLE_TEXT + 60
		self.W_STATS_TEXT = int(self.W_HEADER_PANEL * (5 / 7.0)) + (self.iMarginSpace * 2)
		self.H_STATS_TEXT = int(self.H_HEADER_PANEL * (3 / 5.0)) - (self.iMarginSpace * 2)

		self.X_TEXT_PANEL = self.X_HEADER_PANEL + self.W_LEADER_ICON + self.iMarginSpace
		self.Y_TEXT_PANEL = self.Y_HEADER_PANEL + self.H_LEADER_TITLE_TEXT
		self.W_TEXT_PANEL = 2 * self.W_HEADER_PANEL / 3 + self.iMarginSpace
		self.H_TEXT_PANEL = self.H_MAIN_PANEL - self.H_LEADER_TITLE_TEXT + 5
		self.iTEXT_PANEL_MARGIN = 35

		self.W_EXIT = 170
		self.H_EXIT = 30

		#self.X_EXIT = (self.W_SCREEN/2) - (self.W_EXIT/2)
		self.X_EXIT = self.X_HEADER_PANEL + self.iMarginSpace + 15
		self.Y_EXIT = self.H_MAIN_PANEL - 30
