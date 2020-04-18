## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvFoYScreen:

	def interfaceScreen (self, iFoYNum, iType):

		self.X_SCREEN = 0
		self.Y_SCREEN = 0
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 12
		self.BORDER_HEIGHT = 100

		self.X_EXIT = 800
		self.Y_EXIT = 700

		game = CyGame()
		if ( game.isNetworkMultiPlayer() or game.isPitbossHost()):
			return

		self.createMovieScreen(iFoYNum, iType)

	def createMovieScreen(self, iFoYNum, iType):
		screen = CyGInterfaceScreen("FoYScreen", CvScreenEnums.FOY_SCREEN )
		screen.setDimensions(screen.centerX(0), screen.centerY(0), -1, -1)
		screen.setRenderInterfaceOnly(True)
		screen.addDDSGFC("VictoryMovieScreenBackground", ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, -1, -1, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "VictoryMovieTopPanel", u"", u"", False, False, self.X_SCREEN, self.Y_SCREEN, self.W_SCREEN, self.BORDER_HEIGHT, PanelStyles.PANEL_STYLE_TOPBAR, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "VictoryMovieBottomPanel", u"", u"", False, False, self.X_SCREEN, self.H_SCREEN-(self.BORDER_HEIGHT+3), self.W_SCREEN, self.BORDER_HEIGHT+3, PanelStyles.PANEL_STYLE_BOTTOMBAR, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.showWindowBackground( False )
		screen.enableWorldSounds( false )

		# Show the screen
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		# Play intro movie
		PicFile = gc.getCutsceneInfo(iFoYNum).getPictureFileName()
		iPicWidth = gc.getCutsceneInfo(iFoYNum).getPictureX()
		iPicHeight = gc.getCutsceneInfo(iFoYNum).getPictureY()
		iPicX = (self.W_SCREEN / 2) - (iPicWidth / 2)
		iPicY = 110
		iTitleHeight = iPicY + iPicHeight + 20

		# Header & Exit text
		TitleText = gc.getCutsceneInfo(iFoYNum).getDescription()
		TitleText = localText.changeTextColor(TitleText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.addMultilineText("Title", u"<font=4b>" + TitleText + u"</font>", 25, iTitleHeight, self.W_SCREEN - 50, 125, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
		# Show the cutscene
		if (iFoYNum == 0):
                    self.iSoundID = CyAudioGame().Play2DSound('AS2D_AODFOY')
                    screen.setSoundId(self.iSoundID)
                    CyAudioGame().Set2DSoundVolume(self.iSoundID, 1.0)
                screen.addDDSGFC("FoY", PicFile, iPicX, iPicY, iPicWidth, iPicHeight, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Exit
		screen.setText( "FoYScreenExit", "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.W_SCREEN - 30, self.H_SCREEN - 35, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

	def closeScreen(self):
		screen = CyGInterfaceScreen( "FoYScreen", CvScreenEnums.FOY_SCREEN )
		screen.hideScreen()

	def hideScreen(self):
		screen = CyGInterfaceScreen( "FoYScreen", CvScreenEnums.FOY_SCREEN )
		screen.hideScreen()

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		screen = CyGInterfaceScreen( "FoYScreen", CvScreenEnums.FOY_SCREEN )
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_MOVIE_DONE or inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED or inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
			return self.hideScreen()
		return 0

	def update(self, fDelta):
		return

