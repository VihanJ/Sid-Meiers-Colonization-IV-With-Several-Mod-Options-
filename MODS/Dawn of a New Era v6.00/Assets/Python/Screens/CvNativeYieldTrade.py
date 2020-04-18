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

TableHumanYields = []
TableNativeYields = []

class CvNativeYieldTrade:

	def __init__(self):
		self.WIDGET_ID = "NativeYieldTradeWidget"
		self.TABLE1_ID = "NativeYieldTradeTable1"
		self.TABLE2_ID = "NativeYieldTradeTable2"
		
		self.nWidgetCount = 0
		
		self.DELETE_PROPOSITION_1 = 1
		self.DELETE_PROPOSITION_2 = 2
		self.YIELD_HELP = 3
		self.YIELD_DESIRED_HELP = 4
		self.VALID_PROPOSITION_FINALE = 5
		self.CHANGE_TRADE_MODE = 6
		self.ASK_PROPOSITION = 7
		self.NEW_AGREEMENT = 8
		self.REMOVE_ASSIGNED_UNIT = 9
		self.YIELD_ALREADY_TRADED_HELP = 10
		self.AUTOMATIC_RENEWAL_POPUP = 11
		
	def getScreen(self):
		return CyGInterfaceScreen("nativeYieldTrade", CvScreenEnums.NATIVE_YIELD_TRADE)

	def interfaceScreen(self, m_iMode, m_iId):
	
		if ( CyGame().isPitbossHost() ):
			return

		if gc.getPlayer(gc.getGame().getActivePlayer()).getParent() == PlayerTypes.NO_PLAYER:
			return
	
		screen = self.getScreen()
		if screen.isActive():
			return
			
		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		self.player = pPlayer
		iUnit = m_iId
		pUnit = pPlayer.getUnit(iUnit)
		self.unit = pUnit
		self.m_iD = -1
		pPlot = pUnit.plot()
		if not pPlot:
			return
		pCity = pPlot.getPlotCity()
		self.city = pCity
		if not pCity:
			return
		
		global TableHumanYields
		global TableNativeYields
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				TableHumanYields.append(0)
				TableNativeYields.append(0)		
		
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.enableWorldSounds( false )
		pNativePlayer =  gc.getPlayer(pCity.getOwner())
		self.pNativePlayer = pNativePlayer
		pLeaderHeadInfo = gc.getLeaderHeadInfo(pNativePlayer.getLeaderType())
		screen.setSoundId(CyAudioGame().Play2DSoundWithId(pLeaderHeadInfo.getDiploPeaceMusicScriptIds(0)))
		
		self.XResolution = screen.getXResolution()
		self.YResolution = screen.getYResolution()

		self.X_SIZE_ADD_POPPUP = self.XResolution*5/32
		self.X_SIZE_POPUP = self.XResolution*2/3 + self.X_SIZE_ADD_POPPUP
		self.Y_SIZE_POPUP = self.YResolution*2/3
		self.X_POS_POPUP = (self.XResolution - self.X_SIZE_POPUP)/2
		self.Y_POS_POPUP = self.YResolution/12
		
		self.X_SIZE_PICTURE = self.XResolution/7
		self.Y_SIZE_PICTURE = self.YResolution/14
		
		self.X_DECAL_PICTURE = self.XResolution/102
		
		self.X_POS_PICTURE = self.X_POS_POPUP + self.X_SIZE_POPUP - self.X_SIZE_PICTURE - self.X_DECAL_PICTURE
		self.Y_POS_PICTURE1 = self.Y_POS_POPUP + self.X_DECAL_PICTURE + 2
		self.Y_POS_PICTURE2 = self.Y_POS_POPUP + self.Y_SIZE_POPUP/2 + self.X_DECAL_PICTURE - 3
		
		self.LONG_DEROUL = 120
		self.LARG_CASE = 35
		self.LARG_ARROW = 14		
		self.TRADE_MODE = m_iMode
				
		screen.addDDSGFC("NativeYieldTradeBackground", ArtFileMgr.getInterfaceArtInfo("INTERFACE_NATIVE_YIELD_TRADE").getPath(), self.X_POS_POPUP, self.Y_POS_POPUP, self.X_SIZE_POPUP, self.Y_SIZE_POPUP, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_NATIVE_YIELD_TRADE_NATIVE_NAME", (pNativePlayer.getCivilizationShortDescriptionKey(), pNativePlayer.getName(), )), gc.getInfoTypeForString("COLOR_CITY_BROWN"))
		screen.setLabel("NomDuChef", "Background", u"<font=3b>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_POS_POPUP + 120, self.Y_POS_POPUP + 30, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		szText = localText.changeTextColor(localText.getText("TXT_KEY_NATIVE_YIELD_TRADE_CITY_NAME", (pCity.getNameKey(), )), gc.getInfoTypeForString("COLOR_CITY_BROWN"))
		screen.setLabel("NomDeLaTribut", "Background", u"<font=3b>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_POS_POPUP + self.X_SIZE_POPUP - 50 - self.X_SIZE_ADD_POPPUP, self.Y_POS_POPUP + 30, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		szText = localText.changeTextColor(localText.getText("TXT_KEY_NATIVE_DESIRED_RESOURCES", ()), gc.getInfoTypeForString("COLOR_CITY_BROWN"))
		screen.setLabel("RessourcesDesires", "Background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_POS_POPUP + 120, self.Y_POS_POPUP + 55, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		self.showResources()	

		szText = localText.changeTextColor(localText.getText("TXT_KEY_NEW_CARGO_CORPS", ()), gc.getInfoTypeForString("COLOR_WHITE"))
		screen.setLabel("RessourcesVillage", "Background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_POS_PICTURE, self.Y_POS_PICTURE1 + self.Y_SIZE_PICTURE, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel("RessourcesHumain", "Background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_POS_PICTURE, self.Y_POS_PICTURE2 + self.Y_SIZE_PICTURE, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.addDDSGFC("TONNEAU1", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_TONNEAU").getPath(), self.X_POS_POPUP + self.X_SIZE_POPUP - 24, self.Y_POS_PICTURE2 + self.Y_SIZE_PICTURE, 17, 17, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addDDSGFC( "TributIcon", ArtFileMgr.getCivilizationArtInfo(gc.getCivilizationInfo(pNativePlayer.getCivilizationType()).getArtDefineTag()).getButton(), self.X_POS_POPUP + 50, self.Y_POS_POPUP + 40, 50, 50, WidgetTypes.WIDGET_CONTACT_CIV, pCity.getOwner(), 1)
		
		if gc.getPlayer(pCity.getOwner()).isNative():
			screen.addDDSGFC("NativeYieldTradePopup1Background", ArtFileMgr.getInterfaceArtInfo("INTERFACE_NATIVE_YIELD_TRADE_POPUP_INDIEN").getPath(), self.X_POS_PICTURE, self.Y_POS_PICTURE1, self.X_SIZE_PICTURE, self.Y_SIZE_PICTURE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		else:			
			screen.addDDSGFC("NativeYieldTradePopup1Background", ArtFileMgr.getInterfaceArtInfo("INTERFACE_NATIVE_YIELD_TRADE_POPUP_EUROPEAN").getPath(), self.X_POS_PICTURE, self.Y_POS_PICTURE1, self.X_SIZE_PICTURE, self.Y_SIZE_PICTURE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		if gc.getUnitInfo(pUnit.getUnitType()).isMechUnit():
			screen.addDDSGFC("NativeYieldTradePopup2Background", ArtFileMgr.getInterfaceArtInfo("INTERFACE_NATIVE_YIELD_TRADE_POPUP_SHIP").getPath(), self.X_POS_PICTURE, self.Y_POS_PICTURE2, self.X_SIZE_PICTURE, self.Y_SIZE_PICTURE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		else:
			screen.addDDSGFC("NativeYieldTradePopup2Background", ArtFileMgr.getInterfaceArtInfo("INTERFACE_NATIVE_YIELD_TRADE_POPUP_CHARIOT").getPath(), self.X_POS_PICTURE, self.Y_POS_PICTURE2, self.X_SIZE_PICTURE, self.Y_SIZE_PICTURE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		self.X_POS_1 = self.X_POS_POPUP + self.X_SIZE_POPUP/2 + 30
		self.Y_POS_1 = self.Y_POS_POPUP + self.Y_SIZE_POPUP / 3
		
		self.X_POS_2 = self.X_POS_POPUP + self.X_SIZE_POPUP/4 - 10
		self.Y_POS_2 = self.Y_POS_POPUP + self.Y_SIZE_POPUP / 3
		
		self.resetTradeProposition()
		# draw the contents
		self.drawContents()
		self.drawTables()

	def drawContents(self):
		self.deleteAllWidgets()

		screen = self.getScreen()
		pUnit = self.unit
		pPlayer = self.player
		
		xDecalMode = self.X_SIZE_POPUP/14
		yDecalMode = -10
		szText = localText.getText("TXT_KEY_TRANSACTIONS", ())
		if self.TRADE_MODE == 0:
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_PLAYER_DARK_YELLOW"))
			screen.setText("TradeModeTroc1", "Background", u"<font=3b>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_POPUP + xDecalMode, self.Y_POS_POPUP + self.Y_SIZE_POPUP / 2 + yDecalMode, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		else :
			screen.setText("TradeModeTroc1", "Background", u"<font=3b>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_POPUP + xDecalMode, self.Y_POS_POPUP + self.Y_SIZE_POPUP / 2 + yDecalMode, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.CHANGE_TRADE_MODE, 0 )
		
		szText = localText.getText("TXT_KEY_AGREEMENT", ())
		if self.TRADE_MODE == 1:
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_PLAYER_DARK_YELLOW"))
			screen.setText("TradeModeTroc", "Background", u"<font=3b>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_POPUP + xDecalMode, self.Y_POS_POPUP + self.Y_SIZE_POPUP / 2 + yDecalMode + 30, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		else :
			screen.setText("TradeModeTroc", "Background", u"<font=3b>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_POPUP + xDecalMode, self.Y_POS_POPUP + self.Y_SIZE_POPUP / 2 + yDecalMode + 30, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.CHANGE_TRADE_MODE, 1 )
		
		
		screen.setText("EuropeScreenExitWidget", "Background", u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_POPUP + xDecalMode, self.Y_POS_POPUP + self.Y_SIZE_POPUP / 2 + yDecalMode + 60, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		
	
		#Affichage du stock de notre navire
		szText = u"<font=2>%d/%d</font>" % (pUnit.getNewCargo(), gc.getUnitInfo(pUnit.getUnitType()).getCargoNewSpace())
		szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_WHITE"))
		screen.setLabel("RessourcesHumainStock", "Background", szText, CvUtil.FONT_RIGHT_JUSTIFY, self.X_POS_POPUP + self.X_SIZE_POPUP - 26, self.Y_POS_PICTURE2 + self.Y_SIZE_PICTURE, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		pCity = self.city
		pNativePlayer = self.pNativePlayer
		if pCity.getBanTurnTo(CyGame().getActivePlayer()) > 0:
			self.RefuseDiscuss()
		else:
			if self.TRADE_MODE == 0:
				self.NegociationPart()
			if self.TRADE_MODE == 1:
				if pNativePlayer.getRelationTradeTo(CyGame().getActivePlayer()) > 0:
					self.AgreementPart()
				else :
					self.Refuse2Discuss()
		
		return 0
	
	def Refuse2Discuss(self):
		screen = self.getScreen()
		pPlayer = self.player
		
		xText1 = self.X_POS_POPUP + self.X_SIZE_POPUP/5 + 20
		yText = self.Y_POS_POPUP + self.Y_SIZE_POPUP/4
		yDecal = 30
		yNumDecal = 1
		xTab = 30
		iAfficheYieldX = self.X_POS_POPUP + self.X_SIZE_POPUP/2 + 10
		iAfficheYieldY = self.Y_POS_POPUP + (self.Y_SIZE_POPUP/4 + self.Y_SIZE_POPUP/3)/2 + 10
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_NATIVE_DO_NOT_WANT_TO_TRADE_TITLE", ()), gc.getInfoTypeForString("COLOR_WHITE"))
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4b>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, iAfficheYieldX - 20, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		yNumDecal = yNumDecal + 2
		screen.addMultilineText(self.getNextWidgetName(), u"<font=3>" + localText.getText("TXT_KEY_NATIVE_DO_NOT_WANT_TO_TRADE_BODY", ()) + u"</font>", xText1 + xTab - 25, yText + yNumDecal*yDecal, self.X_SIZE_POPUP/2 + 35, self.Y_SIZE_POPUP/3, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def RefuseDiscuss(self):
		screen = self.getScreen()
		pPlayer = self.player
		
		xText1 = self.X_POS_POPUP + self.X_SIZE_POPUP/5 + 20
		yText = self.Y_POS_POPUP + self.Y_SIZE_POPUP/4
		yDecal = 30
		yNumDecal = 1
		xTab = 30
		iAfficheYieldX = self.X_POS_POPUP + self.X_SIZE_POPUP/2 + 10
		iAfficheYieldY = self.Y_POS_POPUP + (self.Y_SIZE_POPUP/4 + self.Y_SIZE_POPUP/3)/2 + 10
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_NATIVE_BOYCOTT_US_TITLE", ()), gc.getInfoTypeForString("COLOR_WHITE"))
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4b>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, iAfficheYieldX - 20, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		yNumDecal = yNumDecal + 2
		screen.addMultilineText(self.getNextWidgetName(), u"<font=3>" + localText.getText("TXT_KEY_NATIVE_REFUSE_DISCUSS", ()) + u"</font>", xText1 + xTab - 25, yText + yNumDecal*yDecal, self.X_SIZE_POPUP/2 + 35, self.Y_SIZE_POPUP/3, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def AgreementPart(self):
		screen = self.getScreen()
		pPlayer = self.player
		pCity = self.city
		
		xText1 = self.X_POS_POPUP + self.X_SIZE_POPUP/5 + 20
		yText = self.Y_POS_POPUP + self.Y_SIZE_POPUP/4
		yDecal = 30
		yNumDecal = 0
		xTab = 30
		xTextButton = xText1
		iAfficheYieldX = self.X_POS_POPUP + self.X_SIZE_POPUP/2 + 10
		iAfficheYieldY = self.Y_POS_POPUP + (self.Y_SIZE_POPUP/4 + self.Y_SIZE_POPUP/3)/2 + 10
		
		if pCity.getNativeYieldProduce() == -1:			
			szText = localText.getText("TXT_KEY_NATIVE_CAN_NOT_HAVE_AGREEMENT_TITLE", ())
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4b>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, iAfficheYieldX - 20, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			yNumDecal = yNumDecal + 2
			
			szText = localText.getText("TXT_KEY_NATIVE_CAN_NOT_HAVE_AGREEMENT", ())
			screen.addMultilineText(self.getNextWidgetName(), u"<font=3>" + szText + u"</font>", xText1 + xTab - 25, yText + yNumDecal*yDecal, self.X_SIZE_POPUP/2 + 35, self.Y_SIZE_POPUP/3, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			return 0
			
		iD = pPlayer.getAgreementOfCity(pCity);
		if iD != -1 :
			self.m_iD = iD
			pAgreement = pPlayer.getAgreement(iD)
			
			eYieldProduce = pAgreement.getImportYield()
			eYieldWanted = pAgreement.getExportYield()
			
			iNumYieldActual = pAgreement.getActualAmount(eYieldProduce)
			iNumYieldMax = pAgreement.getOriginalAmount(eYieldProduce)
			
			iNumYieldActual2 = pAgreement.getActualAmount(eYieldWanted)
			iNumYieldMax2 = pAgreement.getOriginalAmount(eYieldWanted)
			
			szCityName1 = pAgreement.getDestinationCityName()
			szCityName2 = pAgreement.getSourceCityName()
			
			iStartTurns = pAgreement.getTurnMax()
			iRemainingTurns = pAgreement.getTurnCreated() + iStartTurns - gc.getGame().getGameTurn()
		
			szText = localText.changeTextColor(localText.getText("TXT_KEY_AGREEMENT_ACTUAL", ()), gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4b>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, iAfficheYieldX - 20, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			yNumDecal = yNumDecal + 1
			
			szText = localText.changeTextColor(localText.getText("TXT_KEY_AGREEMENT_INFO_CITIES", (szCityName1, szCityName2, )), gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, iAfficheYieldX - 20, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			yNumDecal = yNumDecal + 1
			
			xDecal = 295
			xAlignement = 80
			
			szText = localText.changeTextColor(localText.getText("TXT_KEY_AGREEMENT_NATURE_CONTRAT_TITRE", ()), gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3b>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xText1, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			szText = localText.changeTextColor(localText.getText("TXT_KEY_AGREEMENT_SOLDE_TITRE", ()), gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3b>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, xText1 + xDecal, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			yNumDecal = yNumDecal + 1			
			
			szText = localText.changeTextColor(localText.getText("TXT_KEY_AGREEMENT_INFO_SOURCE1", (gc.getYieldInfo(eYieldProduce).getTextKey(), )), gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xText1 + xTab, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			szText = localText.changeTextColor(localText.getText("TXT_KEY_AGREEMENT_INFO_SOURCE", (iNumYieldMax, )), gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xText1 + xTab + xAlignement, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			szText = u"%s%c" %(iNumYieldMax - iNumYieldActual, gc.getYieldInfo(eYieldProduce).getChar())
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, xText1 + xDecal, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			yNumDecal = yNumDecal + 1
			
			szText = localText.changeTextColor(localText.getText("TXT_KEY_AGREEMENT_INFO_SOURCE1", (gc.getYieldInfo(eYieldWanted).getTextKey(), )), gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xText1 + xTab, yText + yNumDecal*yDecal - yDecal/3, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			szText = localText.changeTextColor(localText.getText("TXT_KEY_AGREEMENT_INFO_SOURCE", (iNumYieldMax2, )), gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xText1 + xTab + xAlignement, yText + yNumDecal*yDecal - yDecal/3, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			szText = u"%s%c" %(iNumYieldMax2 - iNumYieldActual2, gc.getYieldInfo(eYieldWanted).getChar())
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, xText1 + xDecal, yText + yNumDecal*yDecal - yDecal/3, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			yNumDecal = yNumDecal + 1
			
			szText = localText.changeTextColor(localText.getText("TXT_KEY_AGREEMENT_DUREE_CONTRAT_TITRE", ()), gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3b>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xText1, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			xDecal1 = xDecal/2
			szText = localText.changeTextColor(localText.getText("TXT_KEY_AGREEMENT_DUREE_CONTRAT_TURN", (iStartTurns, )), gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xText1 + xDecal1, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			xDecal1 = xDecal*3/4
			szText = localText.changeTextColor(localText.getText("TXT_KEY_POPUP_AGREEMENT_HELP_4", (iRemainingTurns, )), gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xText1 + xDecal1, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			yNumDecal = yNumDecal + 1
			
			szText = localText.changeTextColor(localText.getText("TXT_KEY_AGREEMENT_AFFECTED_TRANSPORT", ()), gc.getInfoTypeForString("COLOR_WHITE"))
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3b>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xText1, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			yNumDecal = yNumDecal + 1			
			
			iI = 0
			(unit, iter) = pPlayer.firstUnit()
			while (unit):
				pGroup = unit.getGroup()
				if not pGroup.isNone():
					if pGroup.isAssignedAgreement(iD):
						szText = localText.changeTextColor(localText.getText("TXT_KEY_AGREEMENT_AFFECTED_TRANSPORT_NAME", (unit.getNameKey(), )), gc.getInfoTypeForString("COLOR_WHITE"))
						screen.setText(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xText1 + xTab, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, self.REMOVE_ASSIGNED_UNIT, unit.getID())
						yNumDecal = yNumDecal + 1
						iI = iI + 1
				(unit, iter) = pPlayer.nextUnit(iter)
			
			if iI == 0:
				szText = localText.changeTextColor(localText.getText("TXT_KEY_AGREEMENT_NO_AFFECTED_TRANSPORT", ()), gc.getInfoTypeForString("COLOR_WHITE"))
				screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xText1 + xTab, yText + yNumDecal*yDecal, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				yNumDecal = yNumDecal + 1
				
		else :
			eYieldProduce = pCity.getNativeYieldProduce() 
			eTradePlayer = pCity.tradeProducedYieldWith()
			if (eTradePlayer >= 0 and  eTradePlayer < gc.getMAX_PLAYERS()):
				yNumDecal = yNumDecal + 1
				pTradePlayer = gc.getPlayer(eTradePlayer)
				screen.addMultilineText(self.getNextWidgetName(), u"<font=3>" + localText.getText("TXT_KEY_AGREEMENT_WITH_OTHERS_INFO", (pPlayer.getNameKey(), pTradePlayer.getNameKey(), gc.getYieldInfo(eYieldProduce).getTextKey(), )) + u"</font>", xText1 + xTab - 25, yText + yNumDecal*yDecal, self.X_SIZE_POPUP/2 + 35, self.Y_SIZE_POPUP/3, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			else:
				eYieldWanted = pCity.getWantedYield()
				yNumDecal = yNumDecal + 1
				screen.addMultilineText(self.getNextWidgetName(), u"<font=3>" + localText.getText("TXT_KEY_NO_AGREEMENT_INFO", (pPlayer.getNameKey(), gc.getYieldInfo(eYieldWanted).getTextKey(), gc.getYieldInfo(eYieldProduce).getTextKey(), )) + u"</font>", xText1 + xTab - 25, yText + yNumDecal*yDecal, self.X_SIZE_POPUP/2 + 35, self.Y_SIZE_POPUP/3, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iValidButtonX = self.X_POS_POPUP + self.X_SIZE_POPUP*4/9
				iValidButtonY = yText + yNumDecal*yDecal + self.Y_SIZE_POPUP/3
				#Validation de la transaction
				screen.setButtonGFC(self.getNextWidgetName(), localText.getText("TXT_KEY_NATIVE_NEW_AGREEMENT", ()), "", iValidButtonX, iValidButtonY, 250, 30, WidgetTypes.WIDGET_GENERAL, self.NEW_AGREEMENT, -1, ButtonStyles.BUTTON_STYLE_STANDARD )

		iAutomaticRenewButtonX = self.X_POS_POPUP + self.X_SIZE_POPUP / 3
		iAutomaticRenewButtonY = self.Y_SIZE_POPUP
		screen.setButtonGFC(self.getNextWidgetName(), localText.getText("TXT_KEY_BUTTONPOPUP_AUTOMATIC_AGREEMENT_BY_YIELDS_HEADER", ()), "", iAutomaticRenewButtonX, iAutomaticRenewButtonY, 350, 30, WidgetTypes.WIDGET_GENERAL, self.AUTOMATIC_RENEWAL_POPUP, -1, ButtonStyles.BUTTON_STYLE_STANDARD )

	def NegociationPart(self):
		screen = self.getScreen()
		pUnit = self.unit
		iPosX = self.X_POS_1
		iPosY = self.Y_POS_1
		iLargCase = self.LARG_CASE
		pPlayer = self.player
		
		global TableHumanYields
		global TableNativeYields
		
		bHumanProposal = False
		bIAProposal = False
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				TableNativeYields[iYield] = pPlayer.getIATradeProposition(iYield)
				TableHumanYields[iYield] = pPlayer.getHumanTradeProposition(iYield)
				if (TableNativeYields[iYield] > 0):
					bIAProposal = True
				if (TableHumanYields[iYield] > 0):
					bHumanProposal = True

				
		iAfficheYieldX = self.X_POS_POPUP + self.X_SIZE_POPUP/2 + 10
		iAfficheYieldY = self.Y_POS_POPUP + (self.Y_SIZE_POPUP/4 + self.Y_SIZE_POPUP/3)/2 + 10
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_TRANSACTIONS", ()), gc.getInfoTypeForString("COLOR_WHITE"))
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4b>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, iAfficheYieldX - 20, iAfficheYieldY - 30, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		xSepa = iAfficheYieldX - 20
		ySepa = iAfficheYieldY + 30
		wSepa = 2
		zSepa = 150
		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_SEPARATEUR_DIALOGUE_COMMERCE_VERTICAL").getPath(), xSepa, ySepa, wSepa, zSepa, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		iAfficheYieldX = iPosX + 20
		iAfficheYieldY = iPosY + 45
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_WHAT_YOU_PROPOSE", ()), gc.getInfoTypeForString("COLOR_WHITE"))
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3b>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iAfficheYieldX - 20, iAfficheYieldY - 30, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				if TableHumanYields[iYield] > 0:
					szText = localText.getText("TXT_KEY_LIST_OF_YIELDS", (gc.getYieldInfo(iYield).getTextKey(), TableHumanYields[iYield], ))
					screen.setText(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iAfficheYieldX, iAfficheYieldY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, self.DELETE_PROPOSITION_1, iYield)
					iAfficheYieldY += 25
		
		#Native part
		iPosX = self.X_POS_2
		iPosY = self.Y_POS_2
		
		iQuantiteUp = 0
		iQuantiteDown = 0
		pCity = self.city		
			
		iAfficheYieldX = iPosX + 20
		iAfficheYieldY = iPosY + 45
		
		iValidButtonX = self.X_POS_POPUP + self.X_SIZE_POPUP*5/8
		iValidButtonY = self.Y_POS_POPUP + self.Y_SIZE_POPUP*3/4 - 25
		validateBtnName = self.getNextWidgetName()
		#Validation de la transaction
		screen.setButtonGFC(validateBtnName, localText.getText("TXT_KEY_VALIDATE", ()), "", iValidButtonX, iValidButtonY, 120, 30, WidgetTypes.WIDGET_GENERAL, self.VALID_PROPOSITION_FINALE, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		if (not bHumanProposal and not bIAProposal):
			screen.enable(validateBtnName, False)
		iValidButtonX -= 145

		askBtnName = self.getNextWidgetName()
		#Demande ce qu'il veux
		screen.setButtonGFC(askBtnName, localText.getText("TXT_KEY_PROPOSAL", ()), "", iValidButtonX, iValidButtonY, 120, 30, WidgetTypes.WIDGET_GENERAL, self.ASK_PROPOSITION, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		if (bHumanProposal and bIAProposal):
			screen.enable(askBtnName, False)
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_WHAT_YOU_WISH", ()), gc.getInfoTypeForString("COLOR_WHITE"))
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3b>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iAfficheYieldX-20, iAfficheYieldY - 30, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				if TableNativeYields[iYield] > 0:
					szText = localText.getText("TXT_KEY_LIST_OF_YIELDS", (gc.getYieldInfo(iYield).getTextKey(), TableNativeYields[iYield], ))
					screen.setText(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iAfficheYieldX, iAfficheYieldY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, self.DELETE_PROPOSITION_2, iYield)
					iAfficheYieldY += 25		
		return 0
	def showResources(self):
		screen = self.getScreen()
		pCity = self.city
		pPlayer = self.player 
		iI = 0
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				screen.deleteWidget("RessourceDesire" + str(iI))	
				iI += 1
		iI = 0		
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				if pCity.getYieldDesired(iYield) > 0 and not pPlayer.isHasYieldUnknown(iYield):
					szName = "RessourceDesire" + str(iI)
					screen.addDDSGFC(szName, gc.getYieldInfo(iYield).getIcon(), self.X_POS_POPUP + 120 + 22*iI, self.Y_POS_POPUP + 65 + 7, 22, 22, WidgetTypes.WIDGET_GENERAL, self.YIELD_DESIRED_HELP, iYield)
					iI += 1
		
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
		'Calls function mapped in '
		
		screen = self.getScreen()
		
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):
				if (inputClass.getData1() == self.DELETE_PROPOSITION_1) :
					self.deleteProposition(inputClass.getData2(), 1)
					self.drawContents()
				elif (inputClass.getData1() == self.DELETE_PROPOSITION_2) :
					self.deleteProposition(inputClass.getData2(), 2)
					self.drawContents()
				elif (inputClass.getData1() == self.NEW_AGREEMENT) :
					pUnit = self.unit
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_NEW_AGREEMENT)
					popupInfo.setData1(pUnit.getID())
					CyInterface().addPopup(popupInfo, gc.getGame().getActivePlayer(), true, false)
				elif (inputClass.getData1() == self.AUTOMATIC_RENEWAL_POPUP):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_AUTOMATIC_AGREEMENT_BY_YIELDS)
					CyInterface().addPopup(popupInfo, gc.getGame().getActivePlayer(), true, false)
				elif (inputClass.getData1() == self.REMOVE_ASSIGNED_UNIT) :
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_REMOVE_ASSIGNED_UNIT)
					popupInfo.setData1(inputClass.getData2())
					popupInfo.setData2(self.m_iD)
					CyInterface().addPopup(popupInfo, gc.getGame().getActivePlayer(), true, false)				
				elif (inputClass.getData1() == self.VALID_PROPOSITION_FINALE) :
					pUnit = self.unit
					CyMessageControl().sendDoCommand(pUnit.getID(), CommandTypes.COMMAND_TRADE_PROPOSITION, 0, -1, false) 					
				elif (inputClass.getData1() == self.ASK_PROPOSITION) :
					pUnit = self.unit
					CyMessageControl().sendDoCommand(pUnit.getID(), CommandTypes.COMMAND_TRADE_PROPOSITION, 1, -1, false) 					
				elif (inputClass.getData1() == self.CHANGE_TRADE_MODE) :
					self.TRADE_MODE = inputClass.getData2()
					self.drawTables()
					self.drawContents()
		return 0
	def resetTradeProposition(self):
		global TableHumanYields
		global TableNativeYields
		pPlayer = self.player
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				pPlayer.setHumanTradeProposition(iYield, 0)
				pPlayer.setIATradeProposition(iYield, 0)
				TableHumanYields[iYield] = 0
				TableNativeYields[iYield] = 0
		
	def deleteProposition(self, iYield, iMode):
		global TableHumanYields			
		global TableNativeYields			
		pPlayer = self.player
		
		if iMode == 1:		
			if iYield != -1:
				TableHumanYields[iYield] = 0
				pPlayer.setHumanTradeProposition(iYield, 0)
		elif iMode == 2:
			if iYield != -1:
				TableNativeYields[iYield] = 0
				pPlayer.setIATradeProposition(iYield, 0)
		
	def getNumYieldsProposition(self, iMode):
		global TableHumanYields
		global TableNativeYields
			
		iNum = 0
		if iMode == 1:
			for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				if gc.getYieldInfo(iYield).isCargo():
					if TableHumanYields[iYield] > 0:
						iNum += 1
		elif iMode == 2:
			for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				if gc.getYieldInfo(iYield).isCargo():
					if TableNativeYields[iYield] > 0:
						iNum += 1
		return iNum
				
		
	def resetAllTrade(self):
		global TableHumanYields
		global TableNativeYields
		pPlayer = self.player
		self.deleteAllWidgets()
		
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():				
				TableHumanYields[iYield] = 0
				pPlayer.setHumanTradeProposition(iYield, 0)
				TableNativeYields[iYield] = 0
				pPlayer.setIATradeProposition(iYield, 0)	
	def update(self, fDelta):
		screen = self.getScreen()
		if (CyInterface().isDirty(InterfaceDirtyBits.NativeYieldTrade_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.NativeYieldTrade_DIRTY_BIT, False)
			self.drawTables()
			self.drawContents()
		if (CyInterface().isDirty(InterfaceDirtyBits.NativeYieldTradeResetTrade_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.NativeYieldTradeResetTrade_DIRTY_BIT, False)
			self.resetAllTrade()
			self.showResources()
			self.drawTables()
			self.drawContents()
		

	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList
		
		if eWidgetType == WidgetTypes.WIDGET_GENERAL:
			if iData1 == self.DELETE_PROPOSITION_1:
				return localText.getText("TXT_KEY_MISC_CLICK_TO_CANCEL", ());
			if iData1 == self.DELETE_PROPOSITION_2:
				return localText.getText("TXT_KEY_MISC_CLICK_TO_CANCEL", ());
			if iData1 == self.REMOVE_ASSIGNED_UNIT:
				return localText.getText("TXT_KEY_MISC_CLICK_TO_REMOVE_ASSIGNEMENT", ());
			if iData1 == self.YIELD_HELP:
				return localText.getText("TXT_KEY_NATIVE_QUANTITY_YIELD_HELP", (gc.getYieldInfo(iData2).getTextKey(), self.city.getYieldStored(iData2)));
			if iData1 == self.YIELD_DESIRED_HELP:
				return localText.getText("TXT_KEY_NATIVE_QUANTITY_YIELD_HELP", (gc.getYieldInfo(iData2).getTextKey(), self.city.getYieldDesired(iData2)));
			if iData1 == self.YIELD_ALREADY_TRADED_HELP:
				return localText.getText("TXT_KEY_YIELD_ALREADY_TRADED_HELP", ());
		return u""
	
	def canTradeYield(self, eYield):
		pCity = self.city		
		eYieldProduce = pCity.getNativeYieldProduce()
		if eYield != eYieldProduce:
			return True
			
		eTradePlayer = pCity.tradeProducedYieldWith()
		return (eTradePlayer < 0 or  eTradePlayer >= gc.getMAX_PLAYERS())
		
	def drawTables(self):
		screen = self.getScreen()
		
		screen.addTableControlGFC(self.TABLE1_ID, 2, self.X_POS_PICTURE, self.Y_POS_PICTURE1 + self.Y_SIZE_PICTURE + 20, self.X_SIZE_PICTURE + 2, self.Y_SIZE_POPUP/2 - self.Y_SIZE_PICTURE - 40, false, false, 12, 12, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader(self.TABLE1_ID, 0, u"", self.X_SIZE_PICTURE/5) # Total graph width is 430
		screen.setTableColumnHeader(self.TABLE1_ID, 1, u"", self.X_SIZE_PICTURE*4/5)
		screen.setStyle(self.TABLE1_ID, "Table_EmptyScroll_Style")
		
		screen.addTableControlGFC(self.TABLE2_ID, 2, self.X_POS_PICTURE, self.Y_POS_PICTURE2 + self.Y_SIZE_PICTURE + 20, self.X_SIZE_PICTURE + 2, self.Y_SIZE_POPUP/2 - self.Y_SIZE_PICTURE - 40, false, false, 12, 12, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader(self.TABLE2_ID, 0, u"", self.X_SIZE_PICTURE/5) # Total graph width is 430
		screen.setTableColumnHeader(self.TABLE2_ID, 1, u"", self.X_SIZE_PICTURE*4/5)
		screen.setStyle(self.TABLE2_ID, "Table_EmptyScroll_Style")
		
		self.fillTable()
		
	def fillTable(self):
		screen = self.getScreen()
		iRow1 = -1
		iRow2 = -1
		
		pCity = self.city
		pPlayer = self.player
		pUnit = self.unit
		iI = 0
		
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				if pCity.getYieldStored(iYield) > 0 and not pPlayer.isHasYieldUnknown(iYield):
					iRow1 +=1
					iColumn1 = 0
					screen.appendTableRow(self.TABLE1_ID)
					screen.setTableRowHeight(self.TABLE1_ID, iRow1, 20)
					if self.canTradeYield(iYield):
						if self.TRADE_MODE == 0:
							screen.setTableText(self.TABLE1_ID, iColumn1, iRow1, u"<font=2>%c</font>" % gc.getYieldInfo(iYield).getChar(), "", WidgetTypes.WIDGET_CHOOSE_QUANTITY_TRADE_IN_CITY, iYield, pUnit.getID(), CvUtil.FONT_CENTER_JUSTIFY)
						else :
							screen.setTableText(self.TABLE1_ID, iColumn1, iRow1, u"<font=2>%c</font>" % gc.getYieldInfo(iYield).getChar(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
					else :
						screen.setTableText(self.TABLE1_ID, iColumn1, iRow1, u"<font=2>%c</font>" % gc.getYieldInfo(iYield).getChar(), "", WidgetTypes.WIDGET_GENERAL, self.YIELD_ALREADY_TRADED_HELP, -1, CvUtil.FONT_CENTER_JUSTIFY)	
					
					
					iColumn1 += 1
					szText = localText.getText("TXT_KEY_NATIVE_TRADE_RESOURCES_LIST", (pCity.getYieldStored(iYield), gc.getYieldInfo(iYield).getTextKey()));
					if self.canTradeYield(iYield):
						if self.TRADE_MODE == 0:
							screen.setTableText(self.TABLE1_ID, iColumn1, iRow1, u"<font=2>" + szText + u"</font>", "", WidgetTypes.WIDGET_CHOOSE_QUANTITY_TRADE_IN_CITY, iYield, pUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						else :
							screen.setTableText(self.TABLE1_ID, iColumn1, iRow1, u"<font=2>" + szText + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					else :
						szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_RED"))
						screen.setTableText(self.TABLE1_ID, iColumn1, iRow1, u"<font=2>" + szText + u"</font>", "", WidgetTypes.WIDGET_GENERAL, self.YIELD_ALREADY_TRADED_HELP, -1, CvUtil.FONT_LEFT_JUSTIFY)
				if pUnit.getNewCargoYield(iYield) > 0:
					iRow2 +=1
					iColumn2 = 0
					screen.appendTableRow(self.TABLE2_ID)
					screen.setTableRowHeight(self.TABLE2_ID, iRow2, 20)
					if self.TRADE_MODE == 0:		
						screen.setTableText(self.TABLE2_ID, iColumn2, iRow2, u"<font=2>%c</font>" % gc.getYieldInfo(iYield).getChar(), "", WidgetTypes.WIDGET_CHOOSE_QUANTITY_TRADE_IN_UNIT, iYield, pUnit.getID(), CvUtil.FONT_CENTER_JUSTIFY)
					else :
						screen.setTableText(self.TABLE2_ID, iColumn2, iRow2, u"<font=2>%c</font>" % gc.getYieldInfo(iYield).getChar(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
					iColumn2 += 1
					szText = localText.getText("TXT_KEY_NATIVE_TRADE_RESOURCES_LIST", (pUnit.getNewCargoYield(iYield), gc.getYieldInfo(iYield).getTextKey()));
					if self.TRADE_MODE == 0:		
						screen.setTableText(self.TABLE2_ID, iColumn2, iRow2, u"<font=2>" + szText + u"</font>", "", WidgetTypes.WIDGET_CHOOSE_QUANTITY_TRADE_IN_UNIT, iYield, pUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
					else :
						screen.setTableText(self.TABLE2_ID, iColumn2, iRow2, u"<font=2>" + szText + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		while iRow1 < 10:
			iRow1 += 1
			screen.appendTableRow(self.TABLE1_ID)
			screen.setTableRowHeight(self.TABLE1_ID, iRow1, 20)
		while iRow2 < 10 and iRow2 >= 0:
			iRow2 += 1
			screen.appendTableRow(self.TABLE2_ID)
			screen.setTableRowHeight(self.TABLE2_ID, iRow2, 20)