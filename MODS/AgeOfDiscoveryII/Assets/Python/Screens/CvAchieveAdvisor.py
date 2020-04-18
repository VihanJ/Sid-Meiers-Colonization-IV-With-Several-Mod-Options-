## Sid Meier's Civilization 4
## Copyright Firaxis Games 2008

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums

# Achievement Advisor by Dale Kent

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvAchieveAdvisor:
	"Achievement Advisor Screen"

	def __init__(self):
		self.SCREEN_NAME = "AchieveAdvisor"
		self.BACKGROUND_ID = "AchieveAdvisorBackground"

		self.XResolution = 0
		self.YResolution = 0

	def interfaceScreen (self):

		self.player = gc.getPlayer(gc.getGame().getActivePlayer())
		self.team = gc.getTeam(self.player.getTeam())

		screen = self.getScreen()
		if screen.isActive():
			return

		self.MyAchieves = []

		self.XResolution = self.getScreen().getXResolution()
		self.YResolution = self.getScreen().getYResolution()

		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		# Set the background and exit button, and show the screen
		screen.setDimensions(0, 0, self.XResolution, self.YResolution)
		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("INTERFACE_ACHIEVE_BG").getPath(), 0, 0, self.XResolution, self.YResolution, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		screen.addDDSGFC("TopPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_ACHIEVE_SCREEN_TITLE").getPath(), 0, 0, self.XResolution, 55, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("BottomPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_ACHIEVE_SCREEN_TAB_OFF").getPath(), 0, self.YResolution - 55, self.XResolution, 55, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		screen.showWindowBackground(False)

		TitleText = localText.getText("TXT_KEY_ACHIEVE_ADVISOR_TITLE", ()).upper()
		TitleText = localText.changeTextColor(TitleText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))

		screen.setLabel( "Title", "Background", u"<font=4b>" + TitleText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.XResolution / 2, 4, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText( "AchieveScreenExit", "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.XResolution - 30, self.YResolution - 35, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setActivation( "AchieveScreenExit", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

		ArrowButtonSize = 55
		screen.setButtonGFC("ScrollMinus", u"", "", self.XResolution * 3 / 4 - ArrowButtonSize / 2, self.YResolution - 50, ArrowButtonSize, ArrowButtonSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.setButtonGFC("ScrollPlus", u"", "", self.XResolution * 3 / 4, self.YResolution - 50, ArrowButtonSize, ArrowButtonSize, WidgetTypes.WIDGET_GENERAL, 2, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )

		self.AchieveColumn = 0

		self.drawContents()
		return 0

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.ACHIEVE_ADVISOR)
		
	def getActualColumnCount(self):
		return ((len(self.MyAchieves) + 1) / 2)

	def drawContents(self):
		screen = self.getScreen()

		iRow = 0
		self.MaxColumnCount = 2
		self.MaxRowCount = 2
		iRecordHight = 240
		iRecordWidth = 360
		AchievePicWidth = int(iRecordWidth)
		AchievePicHight = int(iRecordHight)
		AchievePicBorder = AchievePicWidth / 20
		iColumn1 = (self.XResolution / 4) - (iRecordWidth / 2)
		iColumn2 = ((self.XResolution / 4) * 3) - (iRecordWidth / 2)
		iColumnX = iColumn1
		iRow1 = (self.YResolution / 4) - (iRecordHight / 2)
		iRow2 = (((self.YResolution / 4) * 3) - iRecordHight) + 50
		iRowY = iRow1

		self.MyAchieves = []
		for iAchieve in range(gc.getNumAchieveInfos()):
			if (self.player.isAchieveGained(iAchieve)):
				self.MyAchieves.append(iAchieve)

		if (self.AchieveColumn == 0) or (self.getActualColumnCount() <= self.MaxColumnCount):
			screen.hide("ScrollMinus")
		else:
			screen.show("ScrollMinus")

		if (self.AchieveColumn == self.getActualColumnCount() - self.MaxColumnCount) or (self.getActualColumnCount() <= self.MaxColumnCount):
			screen.hide("ScrollPlus")
		else:
			screen.show("ScrollPlus")

		AchieveCountText = localText.getText("TXT_KEY_ACHIEVES", (CyGameTextMgr().getInterfaceTimeStr(gc.getGame().getActivePlayer()), len(self.MyAchieves)))
		AchieveCountText = localText.changeTextColor(AchieveCountText, gc.getInfoTypeForString("COLOR_FONT_GOLD"))
		screen.setLabel("AchieveCount", "Background", "<font=4>" + AchieveCountText + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.XResolution / 2, self.YResolution - 35, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iColumn = 0
		for iIndex in range(self.MaxColumnCount * self.MaxRowCount):
			iAchieveIndex = iIndex + (self.AchieveColumn * 2)
			if (iAchieveIndex < len(self.MyAchieves)):
				iAchieve = self.MyAchieves[iIndex + (self.AchieveColumn * 2)]
				iAchieveTurn = self.player.getAchieveYear(iAchieve)
				iAchieveYear = CyGame().getTurnYear(iAchieveTurn)
				screen.addDDSGFCAt("AchievePic" + str(iIndex), "Background", gc.getAchieveInfo(iAchieve).getPictureFileName(), iColumnX, iRowY, AchievePicWidth, AchievePicHight, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
				szAchieveTitle = gc.getAchieveInfo(iAchieve).getDescription() + u" (%d)" %iAchieveYear
				fontSize = "<font=4>"
				szAchieveTitle = localText.changeTextColor(szAchieveTitle, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
				screen.addMultilineText("AchieveName" + str(iIndex), fontSize + szAchieveTitle + "</font>", iColumnX, iRowY + AchievePicHight, AchievePicWidth, (AchievePicHight * 18 / 100), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				if ((iIndex + 1) % 2 == 0):
					iRow = 0
					iColumn += 1
					iColumnX = iColumn2
					iRowY = iRow1
				else:
					iRow += 1
					iRowY = iRow2
			else:
				screen.hide("AchievePic" + str(iIndex))
				screen.hide("AchieveName" + str(iIndex))

	def handleInput(self, inputClass):

		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):

			if (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):

				if(inputClass.getData1() == 1):
					self.AchieveColumn = max(0, self.AchieveColumn - 1)
					self.drawContents()

				elif(inputClass.getData1() == 2):
					self.AchieveColumn = min(self.getActualColumnCount() - self.MaxColumnCount, self.AchieveColumn + 1)
					self.drawContents()

		return 0

	def update(self, fDelta):
		return 0
		
	# Adds Mouse Over Help to General Widgets
	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList
		return u""
