## DoaNE
## Copyright M07 2011

##########################################################################################################
########## Europe Screen 2: Trade screen #################################################################
##########################################################################################################

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvEuropeC2Screen:

	def __init__(self):
		self.WIDGET_ID = "EuropeC2ScreenWidget"
		self.TABLE_ID = "EuropeC2ScreenTable"
		self.nWidgetCount = 0
		
		self.m_tabCtrlEdit = 0
		
		self.TREASURY_ID = 1
		self.NO_SHIP_SELECTED = 2
		self.CHANGE_PAGE = 3
		self.CHANGE_MODE_PRICE = 4
		self.CHANGE_QUANTITY = 5
		self.YIELD_PRICE = 6
		self.CHANGE_QUANTITY_SHIP_UP = 7
		self.CHANGE_QUANTITY_SHIP_DOWN = 8
		self.TOTAL_CHANGE_SHIP = 9
		self.TOTAL_CHANGE_EUROPE = 10
		self.VALID_SELL = 11
		self.VALID_BUY = 12
		self.CHANGE_QUANTITY_EUROPE_UP = 13
		self.CHANGE_QUANTITY_EUROPE_DOWN = 14
		self.CHANGE_MODE = 15
		self.VALID_TRANSFERT_1 = 16
		self.VALID_TRANSFERT_2 = 17
		self.CHANGE_QUANTITY_WAREHOUSE_UP = 18
		self.CHANGE_QUANTITY_WAREHOUSE_DOWN = 19
		self.TOTAL_CHANGE_WAREHOUSE = 20
		self.TAX_HELP = 21
		self.UNLOAD_ALL = 22
		self.CHANGE_CURRENT_AGREEMENT = 23
		self.REMOVE_SELECTED_YIELD = 24
		self.PIN_SELECTED_YIELD = 25

		self.selectedPlayerList = []
		self.EuropeUnitsList = []
		self.ShipGoods = []
		self.PinGoods = []
		self.SelectedGoods = []
		self.EuropeGoods = []
		self.WarehouseGoods = []
		
	def getScreen(self):
		return CyGInterfaceScreen("europeC2Screen", CvScreenEnums.EUROPE_C2_SCREEN)

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

		self.XResolution = screen.getXResolution()
		self.YResolution = screen.getYResolution()
		self.W_SCREEN = screen.getXResolution()
		self.H_SCREEN = screen.getYResolution()

		self.Y_EXIT = self.YResolution - 36
		self.X_EXIT = self.XResolution - 30

		self.CARGO_ICON_SIZE = self.XResolution / 25
		self.W_TEXT_MARGIN = self.XResolution / 30
		self.Y_TITLE = 4
		self.CARGO_SPACING  = self.CARGO_ICON_SIZE + 2
		
		self.I_SELECTED_SHIP = -1
		self.IN_PORT_PANE_WIDTH = self.XResolution/3
		
		self.X_POS_DOCK_SHIP = 8
		self.Y_POS_DOCK_SHIP = self.YResolution/10 - 15
		self.X_SIZE_DOCK_SHIP = self.XResolution/3 - 5
		self.Y_SIZE_DOCK_SHIP = 45
		self.X_POS_CONTENTS_SHIP_TITLE = 12
		self.X_SIZE_CONTENTS_SHIP_TITLE = self.XResolution/3 - 15
		self.Y_POS_CONTENTS_SHIP_TITLE = self.YResolution/2 - 10
		self.Y_SIZE_CONTENTS_SHIP_TITLE = 28
		self.X_POS_CONTENTS_SHIP = 25
		self.X_SIZE_CONTENTS_SHIP = self.XResolution*145/512
		self.Y_POS_CONTENTS_SHIP_FOND = self.Y_POS_CONTENTS_SHIP_TITLE + self.Y_SIZE_CONTENTS_SHIP_TITLE + 3
		self.Y_SIZE_CONTENTS_SHIP_FOND = self.YResolution*25/128
		
		self.X_SIZE_GOODS_TITLE = self.XResolution*67/512
		self.Y_SIZE_GOODS_TITLE = self.XResolution*7/192
		self.X_POS_GOODS_TITLE = self.XResolution - self.X_SIZE_GOODS_TITLE + 10
		self.Y_POS_GOODS_TITLE = self.Y_POS_DOCK_SHIP - 10
		
		self.X_SIZE_GOODS = self.XResolution*41/256
		self.Y_SIZE_GOODS = self.YResolution*2/3 + self.XResolution*75/1024
		self.X_POS_GOODS = self.X_POS_GOODS_TITLE - 10
		self.Y_POS_GOODS = self.Y_POS_GOODS_TITLE + self.Y_SIZE_GOODS_TITLE + 20
		
		self.X_POS_TRADE_BOOK = self.XResolution*153/512
		self.Y_POS_TRADE_BOOK = self.YResolution*55/768
		self.X_SIZE_TRADE_BOOK = self.XResolution*75/128
		self.Y_SIZE_TRADE_BOOK = self.YResolution*185/384
		
		self.X_POS_CONTRACT_BOOK = self.X_POS_TRADE_BOOK + 40
		self.Y_POS_CONTRACT_BOOK = self.Y_POS_TRADE_BOOK + self.Y_SIZE_TRADE_BOOK
		self.X_SIZE_CONTRACT_BOOK = self.X_SIZE_TRADE_BOOK - 30
		self.Y_SIZE_CONTRACT_BOOK = self.Y_SIZE_TRADE_BOOK * 4 / 5
		
		self.X_POS_TITLE_LEFT_TRADE_BOOK = self.X_POS_TRADE_BOOK + self.XResolution*105/512
		self.X_POS_TITLE_RIGHT_TRADE_BOOK = self.X_POS_TRADE_BOOK + self.X_SIZE_TRADE_BOOK - self.XResolution*75/512
		self.Y_POS_TITLE_TRADE_BOOK = self.Y_POS_TRADE_BOOK + self.YResolution*13/768
		
		self.X_POS_QUANTITY_SCREEN = self.X_POS_TRADE_BOOK + self.XResolution*245/1024
		self.Y_POS_QUANTITY_SCREEN = self.Y_POS_TRADE_BOOK + self.Y_SIZE_TRADE_BOOK - self.YResolution*3/32
		self.X_SIZE_QUANTITY_SCREEN = self.XResolution*91/512
		self.Y_SIZE_QUANTITY_SCREEN = self.YResolution*3/128
		
		self.X_POS_LEFT_BOOK_GOODS = self.X_POS_TRADE_BOOK + self.XResolution*25/256
		self.Y_POS_LEFT_BOOK_GOODS = self.Y_POS_TRADE_BOOK + self.YResolution*29/384
		self.X_SIZE_LEFT_BOOK_GOODS = self.XResolution*29/128
		self.Y_SIZE_LEFT_BOOK_GOODS = self.YResolution/6
		
		self.X_POS_RIGHT_BOOK_GOODS = self.X_POS_TRADE_BOOK + self.XResolution*85/256
		self.Y_POS_RIGHT_BOOK_GOODS = self.Y_POS_LEFT_BOOK_GOODS
		self.X_SIZE_RIGHT_BOOK_GOODS = self.X_SIZE_LEFT_BOOK_GOODS
		self.Y_SIZE_RIGHT_BOOK_GOODS = self.Y_SIZE_LEFT_BOOK_GOODS
		
		self.X_POS_MESSAGE = 25
		self.Y_POS_MESSAGE = self.Y_POS_CONTENTS_SHIP_FOND + self.Y_SIZE_CONTENTS_SHIP_FOND + 10
		self.X_SIZE_MESSAGE = self.XResolution/3 - 50
		self.Y_SIZE_MESSAGE = self.YResolution/7 + 28
				
		self.iMode = 1
		self.bPrices = 1
		self.iPage = 0
		self.iAgreementMode = 1
		self.iCurrentAgreement = 1
		self.EuropeUnitsList = []
		iPlayer = CyGame().getActivePlayer()
		self.pPlayer = gc.getPlayer(iPlayer)
		pPlayer = self.pPlayer
		self.iQuantity = pPlayer.getSelectQuantity()
		
		self.initEuropeShipsList()

		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			self.ShipGoods.append(0)
			isPinned = pPlayer.hasPinnedYieldInEurope(iYield)
			self.PinGoods.append(isPinned)
			self.SelectedGoods.append(isPinned)
			self.EuropeGoods.append(0)
			self.WarehouseGoods.append(0)
			
		# Set the background and exit button, and show the screen
		screen.setDimensions(0, 0, self.XResolution, self.YResolution)
		screen.showWindowBackground(False)
		
		screen.addDDSGFC("EuropeScreenUp", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BANDEAU_MARRON").getPath(), 0, 0, self.XResolution, 40, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("EuropeScreenDown", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BANDEAU_MARRON").getPath(), 0, self.YResolution - 86, self.XResolution, 86, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addDDSGFC("EuropeScreenBackground", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_COMMERCIAL_BACKGROUND").getPath(), 0, 40, self.XResolution, self.YResolution - 86, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("TopPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TITLE").getPath(), 0, 0, self.XResolution, 55, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Header...
		screen.setLabel("EuropeScreenWidgetHeader", "Background", u"<font=4b>" + localText.getText("TXT_KEY_EUROPE_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.XResolution / 2, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Globals Cargos
		screen.addScrollPanel("LoadingList", u"", 15, self.YResolution/3 + 20, self.XResolution/3 - 15, self.CARGO_ICON_SIZE * 2 + 5, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Detailed cargos
		screen.addDDSGFC("ContentsShipTitle", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_CONTENTS_SHIP_TITLE, self.Y_POS_CONTENTS_SHIP_TITLE, self.X_SIZE_CONTENTS_SHIP_TITLE, self.Y_SIZE_CONTENTS_SHIP_TITLE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_CONTENTS_SHIP_TITLE", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setLabel("ContentsShipTitleText", "background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_CONTENTS_SHIP_TITLE + self.X_SIZE_CONTENTS_SHIP_TITLE/2, self.Y_POS_CONTENTS_SHIP_TITLE + self.Y_SIZE_CONTENTS_SHIP_TITLE/4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.addDDSGFC("ContentsShipFond",  ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_IN_PORT_BOX2").getPath(), self.X_POS_CONTENTS_SHIP, self.Y_POS_CONTENTS_SHIP_FOND, self.X_SIZE_CONTENTS_SHIP, self.Y_SIZE_CONTENTS_SHIP_FOND, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
		screen.addScrollPanel("ContentsShip", u"", self.X_POS_DOCK_SHIP, self.Y_POS_CONTENTS_SHIP_FOND, self.X_SIZE_DOCK_SHIP-25, self.Y_SIZE_CONTENTS_SHIP_FOND-25, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Resources
		screen.addDDSGFC("GoodsTitle", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_SHADOW_BOX").getPath(), self.X_POS_GOODS_TITLE, self.Y_POS_GOODS_TITLE, self.X_SIZE_GOODS_TITLE, self.Y_SIZE_GOODS_TITLE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ()).upper(), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setLabel("GoodsTitleText", "background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_GOODS_TITLE + self.X_SIZE_GOODS_TITLE/2, self.Y_POS_GOODS_TITLE + self.Y_SIZE_GOODS_TITLE/4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.addScrollPanel("Goods", u"", self.X_POS_GOODS, self.Y_POS_GOODS, self.X_SIZE_GOODS, self.Y_SIZE_GOODS, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.setLabel("TaxRate", "Background", u"<font=4>" + localText.getText("TXT_KEY_MISC_TAX_RATE", (pPlayer.getTaxRate()+pPlayer.getEuropeLoanPercent(), )) + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT - self.Y_TITLE, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.TAX_HELP, -1 )
		
		# Trade Book
		screen.addDDSGFC("TradeBook", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_BOOK").getPath(), self.X_POS_TRADE_BOOK, self.Y_POS_TRADE_BOOK, self.X_SIZE_TRADE_BOOK, self.Y_SIZE_TRADE_BOOK, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Agreements
		screen.addDDSGFC("AgreementBook", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_PARCHEMIN_AGREEMENT_EUROPE").getPath(), self.X_POS_CONTRACT_BOOK, self.Y_POS_CONTRACT_BOOK, self.X_SIZE_CONTRACT_BOOK, self.Y_SIZE_CONTRACT_BOOK, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addScrollPanel("AgreementsList", u"", self.X_POS_CONTRACT_BOOK + self.X_SIZE_CONTRACT_BOOK*8/10, self.Y_POS_CONTRACT_BOOK + self.Y_SIZE_CONTRACT_BOOK/10, self.X_SIZE_CONTRACT_BOOK*7/40, self.Y_SIZE_CONTRACT_BOOK*7/10, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Europe Needs
		screen.addScrollPanel("EuropeNeeds", u"", self.X_POS_CONTRACT_BOOK, self.Y_POS_CONTRACT_BOOK, self.X_SIZE_CONTRACT_BOOK, self.Y_SIZE_CONTRACT_BOOK, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Message
		screen.addListBoxGFC("MessageList", "", self.X_POS_MESSAGE, self.Y_POS_MESSAGE, self.X_SIZE_MESSAGE, self.Y_SIZE_MESSAGE, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect("MessageList", False)		
		
		self.drawTabs()
		self.setTab(2, True)
		self.drawTable()

		self.resetPanelsBook()
		
		# draw the contents
		self.drawContents()

	def resetPanelsBook(self):
		screen = self.getScreen()
		screen.addScrollPanel("LeftBookGoods", u"", self.X_POS_LEFT_BOOK_GOODS, self.Y_POS_LEFT_BOOK_GOODS, self.X_SIZE_LEFT_BOOK_GOODS, self.Y_SIZE_LEFT_BOOK_GOODS, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addScrollPanel("RightBookGoods", u"", self.X_POS_RIGHT_BOOK_GOODS, self.Y_POS_RIGHT_BOOK_GOODS, self.X_SIZE_RIGHT_BOOK_GOODS, self.Y_SIZE_RIGHT_BOOK_GOODS, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
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
			
		self.showCargaison()
		self.showContentsShip()
		self.showGoods()
		self.showButtonsRessources()
		self.showQuantityButtons()
		# self.agreements()
		self.showEuropeNeeds()
		
		iMode = self.iMode
		
		xPosTextMode = self.X_POS_TRADE_BOOK + self.XResolution*15/256
		yPosTextMode = self.Y_POS_TRADE_BOOK + self.Y_SIZE_TRADE_BOOK/5
		yDecal = self.YResolution*5/96
		iNumDecal = 0
		szSize = u"<font=2>"
		if self.XResolution/1280 >= 1:
			szSize = u"<font=3>"
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_SHIP_EUROPE", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setText(self.getNextWidgetName(), "background", szSize + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, xPosTextMode, yPosTextMode + iNumDecal*yDecal, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.CHANGE_MODE, 1)
		iNumDecal += 1
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_SHIP_WAREHOUSE", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setText(self.getNextWidgetName(), "background", szSize + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, xPosTextMode, yPosTextMode + iNumDecal*yDecal, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.CHANGE_MODE, 2)
		iNumDecal += 1
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_WAREHOUSE_EUROPE", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setText(self.getNextWidgetName(), "background", szSize + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, xPosTextMode, yPosTextMode + iNumDecal*yDecal, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.CHANGE_MODE, 3)
		
		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_IN_PORT_BOX").getPath(), xPosTextMode - self.XResolution*29/1024, yPosTextMode + (iMode-1) * yDecal, self.XResolution*15/256, self.YResolution*5/192, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		if iMode == 1:
			self.showShipEuropeInterface() 
		if iMode == 2:
			self.showShipWarehouseInterface() 
		if iMode == 3:
			self.showWarehouseEuropeInterface() 
		
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4>" + localText.getText("TXT_KEY_FINANCIAL_ADVISOR_TREASURY", (player.getGold(), )).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.W_TEXT_MARGIN, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.TREASURY_ID, -1 )
		
		screen.clearListBoxGFC("MessageList")
		for i in range(player.getNumEuropeTradeMessages()):
			screen.prependListBoxString("MessageList",  u"<font=2>" + player.getEuropeTradeMessage(i) + u"</font>", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		i = 0
		for pLoopUnit in self.EuropeUnitsList:
			if self.I_SELECTED_SHIP == i:
				if pLoopUnit.getSelectedPicture():
					screen.setTableText(self.TABLE_ID, 0, i, u"", pLoopUnit.getSelectedPicture(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				else:
					screen.setTableText(self.TABLE_ID, 0, i, u"", player.getUnitButton(pLoopUnit.getUnitType()), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			else:
				screen.setTableText(self.TABLE_ID, 0, i, u"", player.getUnitButton(pLoopUnit.getUnitType()), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			i += 1
		return 0
	
	def showWarehouseEuropeInterface(self):
		screen = self.getScreen()
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		playerEurope = gc.getPlayer(player.getParent())
		
		self.showEuropeInterface(false) #affichage de la partie europe
		
		iCapacity = player.getEuropeWarehouseCapacity()
		iSpace = self.getWarehouseSpace()
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_WAREHOUSE", (iCapacity-iSpace, iCapacity, )), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TITLE_LEFT_TRADE_BOOK, self.Y_POS_TITLE_TRADE_BOOK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_TITLE", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TITLE_RIGHT_TRADE_BOOK, self.Y_POS_TITLE_TRADE_BOOK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		iStartX = 5
		iDecalY = 5
		iPosY = 0
		iSpacingY = 5
		iSize = self.CARGO_ICON_SIZE*3/4			
		xPosBox = iStartX + iSize*3 - 5
		xSizeBox = iSize*2 + 10
		xTotal = 0
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			kYield = gc.getYieldInfo(iYield)
			if kYield.isCargo():
				if player.getEuropeWarehouseYield(iYield) > 0:
					screen.addDDSGFCAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), iStartX, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
					screen.setImageButtonAt(self.getNextWidgetName(), "LeftBookGoods", gc.getYieldInfo(iYield).getIcon(), iStartX, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.TOTAL_CHANGE_WAREHOUSE, iYield)
					screen.addDDSGFCAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), iStartX + iSize, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
					szQuantity = u"<font=2>%d</font>" % (self.WarehouseGoods[iYield])
					screen.setLabelAt(self.getNextWidgetName(), "LeftBookGoods", szQuantity, CvUtil.FONT_CENTER_JUSTIFY, iStartX + iSize*3/2, iPosY*(iSize+iSpacingY) + (iSize+iSpacingY)*5/12 + 2 + iDecalY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					screen.setImageButtonAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_PLUS").getPath(), iStartX + iSize*2, iPosY*(iSize+iSpacingY) + iDecalY, iSize*2/3, iSize/2 + 3, WidgetTypes.WIDGET_GENERAL, self.CHANGE_QUANTITY_WAREHOUSE_UP, iYield)
					screen.setImageButtonAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_MOINS").getPath(), iStartX + iSize*2, iPosY*(iSize+iSpacingY) + iDecalY + iSize/2-2, iSize*2/3, iSize/2 + 3, WidgetTypes.WIDGET_GENERAL, self.CHANGE_QUANTITY_WAREHOUSE_DOWN, iYield)
					screen.addDDSGFCAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), xPosBox, iPosY*(iSize+iSpacingY) + iDecalY, xSizeBox, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
					screen.addDDSGFCAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("SCREEN_GOLD_PILE").getPath(), xPosBox + xSizeBox - iSize*3/4, iPosY*(iSize+iSpacingY) + iDecalY + iSize/6, iSize*3/4, iSize*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
					iPriceEstimate = player.getSellPriceForYield(iYield, self.WarehouseGoods[iYield])
					szPrices = u"<font=2>%d</font>" % (iPriceEstimate)
					screen.setLabelAt(self.getNextWidgetName(), "LeftBookGoods", szPrices, CvUtil.FONT_RIGHT_JUSTIFY, xPosBox + xSizeBox - iSize*3/4 - 2, iPosY*(iSize+iSpacingY) + iDecalY + iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					xTotal += iPriceEstimate
					screen.addDDSGFCAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), xPosBox+ xSizeBox, iPosY*(iSize+iSpacingY) + iDecalY, xSizeBox/2, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
					szQuantityMax = u"<font=2>%d</font>" % (player.getEuropeWarehouseYield(iYield))
					screen.setLabelAt(self.getNextWidgetName(), "LeftBookGoods", szQuantityMax, CvUtil.FONT_RIGHT_JUSTIFY, xPosBox + xSizeBox/2 + 17 - iSize*3/4 + xSizeBox, iPosY*(iSize+iSpacingY) + iDecalY + iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					iPosY += 1
		if iPosY > 0:
			#including tax
			yDecalDown = 20
			xDecalBox = 12
			xPosSellResult = self.X_POS_LEFT_BOOK_GOODS + 20
			yPosSellResult = self.Y_POS_LEFT_BOOK_GOODS + self.Y_SIZE_LEFT_BOOK_GOODS + 20
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_TRADE_SELL_RESULT", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPosSellResult, yPosSellResult + iSize/4 + yDecalDown, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), xPosSellResult - xDecalBox + xPosBox, yPosSellResult + yDecalDown, xSizeBox, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1)
			szPrices = u"<font=2>%d</font>" % (xTotal)
			screen.setLabel(self.getNextWidgetName(), "background", szPrices, CvUtil.FONT_RIGHT_JUSTIFY, xPosSellResult - xDecalBox + xPosBox + xSizeBox - iSize*3/4 - 2, yPosSellResult + iSize/4 + yDecalDown, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("SCREEN_GOLD_PILE").getPath(), xPosSellResult - xDecalBox + xPosBox + xSizeBox - iSize*3/4, yPosSellResult + iSize/6 + yDecalDown, iSize*3/4, iSize*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_QUANTITY").getPath(), xPosSellResult + xPosBox + xSizeBox - 3, self.Y_POS_LEFT_BOOK_GOODS - iSize/2, iSize*3/4, iSize*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1)
					
			#Valider
			iValidButtonX = xPosSellResult - 5
			iValidButtonY = self.Y_POS_QUANTITY_SCREEN - 5
			screen.setButtonGFC(self.getNextWidgetName(), u"<font=2>" + localText.getText("TXT_KEY_VALIDATE", ()) + u"</font>", "", iValidButtonX, iValidButtonY, 80, 25, WidgetTypes.WIDGET_GENERAL, self.VALID_SELL, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		else:
			xPosNoGoods = self.X_POS_LEFT_BOOK_GOODS + 20
			yPosNoGoods = self.Y_POS_LEFT_BOOK_GOODS + 20			
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_TRADE_WAREHOUSE_NO_RESOURCES", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=1b>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPosNoGoods, yPosNoGoods, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
	
	def showShipWarehouseInterface(self):
		screen = self.getScreen()
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		playerEurope = gc.getPlayer(player.getParent())

		iCapacity = player.getEuropeWarehouseCapacity()
		iSpace = self.getWarehouseSpace()
		
		i = 0
		bSelectedShip = false
		for pShip in self.EuropeUnitsList:
			if self.I_SELECTED_SHIP == i:
				bSelectedShip = true
				break
			i += 1
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_WAREHOUSE", (iCapacity-iSpace, iCapacity, )), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TITLE_RIGHT_TRADE_BOOK, self.Y_POS_TITLE_TRADE_BOOK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		iStartX = 5
		iDecalY = 5
		iPosY = 0
		iSpacingY = 5
		iSize = self.CARGO_ICON_SIZE*3/4			
		xPosBox = iStartX + iSize*3 - 5
		xSizeBox = iSize*2 + 10
			
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if player.getEuropeWarehouseYield(iYield) > 0:
				screen.addDDSGFCAt(self.getNextWidgetName(), "RightBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), iStartX, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
				screen.setImageButtonAt(self.getNextWidgetName(), "RightBookGoods", gc.getYieldInfo(iYield).getIcon(), iStartX, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.TOTAL_CHANGE_EUROPE, iYield)
				screen.addDDSGFCAt(self.getNextWidgetName(), "RightBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), iStartX + iSize, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
				szQuantity = u"<font=2>%d</font>" % (self.WarehouseGoods[iYield])
				screen.setLabelAt(self.getNextWidgetName(), "RightBookGoods", szQuantity, CvUtil.FONT_CENTER_JUSTIFY, iStartX + iSize*3/2, iPosY*(iSize+iSpacingY) + (iSize+iSpacingY)*5/12 + 2 + iDecalY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setImageButtonAt(self.getNextWidgetName(), "RightBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_PLUS").getPath(), iStartX + iSize*2, iPosY*(iSize+iSpacingY) + iDecalY, iSize*2/3, iSize/2 + 3, WidgetTypes.WIDGET_GENERAL, self.CHANGE_QUANTITY_WAREHOUSE_UP, iYield)
				screen.setImageButtonAt(self.getNextWidgetName(), "RightBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_MOINS").getPath(), iStartX + iSize*2, iPosY*(iSize+iSpacingY) + iDecalY + iSize/2-2, iSize*2/3, iSize/2 + 3, WidgetTypes.WIDGET_GENERAL, self.CHANGE_QUANTITY_WAREHOUSE_DOWN, iYield)
				screen.addDDSGFCAt(self.getNextWidgetName(), "RightBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), xPosBox, iPosY*(iSize+iSpacingY) + iDecalY, xSizeBox, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
				screen.addDDSGFCAt(self.getNextWidgetName(), "RightBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_QUANTITY").getPath(), xPosBox + xSizeBox - iSize*3/4, iPosY*(iSize+iSpacingY) + iDecalY + iSize/6, iSize*3/4, iSize*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
				szQuantityMax = u"<font=2>%d</font>" % (player.getEuropeWarehouseYield(iYield))
				screen.setLabelAt(self.getNextWidgetName(), "RightBookGoods", szQuantityMax, CvUtil.FONT_RIGHT_JUSTIFY, xPosBox + xSizeBox - iSize*3/4 - 2, iPosY*(iSize+iSpacingY) + iDecalY + iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iPosY += 1
		if iPosY > 0:
			#Valider
			xPosSellResult = self.X_POS_RIGHT_BOOK_GOODS + 20
			iValidButtonX = xPosSellResult + 100
			iValidButtonY = self.Y_POS_QUANTITY_SCREEN - 5
			screen.setButtonGFC(self.getNextWidgetName(), u"<font=2>" + localText.getText("TXT_KEY_VALIDATE", ()) + u"</font>", "", iValidButtonX, iValidButtonY, 80, 25, WidgetTypes.WIDGET_GENERAL, self.VALID_TRANSFERT_2, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		else:
			xPosNoGoods = self.X_POS_RIGHT_BOOK_GOODS + 20
			yPosNoGoods = self.Y_POS_RIGHT_BOOK_GOODS + 20			
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_TRADE_WAREHOUSE_NO_RESOURCES", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=1b>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPosNoGoods, yPosNoGoods, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		yDecalDown = 20
		xDecalBox = 12
		xPosSellResult = self.X_POS_RIGHT_BOOK_GOODS + 20
		yPosSellResult = self.Y_POS_RIGHT_BOOK_GOODS + self.Y_SIZE_RIGHT_BOOK_GOODS + 20
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_WAREHOUSE_FREE_SPACE", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPosSellResult, yPosSellResult + iSize/4 + yDecalDown, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), xPosSellResult - xDecalBox + xPosBox, yPosSellResult + yDecalDown, xSizeBox, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1)
		szSpaceMax = u"<font=2>%d</font>" % (self.getWarehouseSpace())
		screen.setLabel(self.getNextWidgetName(), "background", szSpaceMax, CvUtil.FONT_RIGHT_JUSTIFY, xPosSellResult - xDecalBox + xPosBox + xSizeBox - iSize*3/4 - 2, yPosSellResult + iSize/4 + yDecalDown, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_QUANTITY").getPath(), xPosSellResult - xDecalBox + xPosBox + xSizeBox - iSize*3/4, yPosSellResult + iSize/6 + yDecalDown, iSize*3/4, iSize*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		if bSelectedShip:
			szText = pShip.getName() + u" (%d/%d)" % (pShip.getNewCargo(), gc.getUnitInfo(pShip.getUnitType()).getCargoNewSpace())
			szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TITLE_LEFT_TRADE_BOOK, self.Y_POS_TITLE_TRADE_BOOK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			iStartX = 5
			iDecalY = 5
			iPosY = 0
			iSpacingY = 5
			iSize = self.CARGO_ICON_SIZE*3/4			
			xPosBox = iStartX + iSize*3 - 5
			xSizeBox = iSize*2 + 10
			xTotal = 0
			for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				kYield = gc.getYieldInfo(iYield)
				if kYield.isCargo():
					if pShip.getNewCargoYield(iYield) > 0:
						screen.addDDSGFCAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), iStartX, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
						screen.setImageButtonAt(self.getNextWidgetName(), "LeftBookGoods", gc.getYieldInfo(iYield).getIcon(), iStartX, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.TOTAL_CHANGE_SHIP, iYield)
						screen.addDDSGFCAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), iStartX + iSize, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
						szQuantity = u"<font=2>%d</font>" % (self.ShipGoods[iYield])
						screen.setLabelAt(self.getNextWidgetName(), "LeftBookGoods", szQuantity, CvUtil.FONT_CENTER_JUSTIFY, iStartX + iSize*3/2, iPosY*(iSize+iSpacingY) + (iSize+iSpacingY)*5/12 + 2 + iDecalY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setImageButtonAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_PLUS").getPath(), iStartX + iSize*2, iPosY*(iSize+iSpacingY) + iDecalY, iSize*2/3, iSize/2 + 3, WidgetTypes.WIDGET_GENERAL, self.CHANGE_QUANTITY_SHIP_UP, iYield)
						screen.setImageButtonAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_MOINS").getPath(), iStartX + iSize*2, iPosY*(iSize+iSpacingY) + iDecalY + iSize/2-2, iSize*2/3, iSize/2 + 3, WidgetTypes.WIDGET_GENERAL, self.CHANGE_QUANTITY_SHIP_DOWN, iYield)
						screen.addDDSGFCAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), xPosBox, iPosY*(iSize+iSpacingY) + iDecalY, xSizeBox, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
						screen.addDDSGFCAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_QUANTITY").getPath(), xPosBox + xSizeBox - iSize*3/4, iPosY*(iSize+iSpacingY) + iDecalY + iSize/6, iSize*3/4, iSize*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
						szMaxQuantity = u"<font=2>%d</font>" % (pShip.getNewCargoYield(iYield))
						screen.setLabelAt(self.getNextWidgetName(), "LeftBookGoods", szMaxQuantity, CvUtil.FONT_RIGHT_JUSTIFY, xPosBox + xSizeBox - iSize*3/4 - 2, iPosY*(iSize+iSpacingY) + iDecalY + iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						iPosY += 1
			if iPosY > 0:
				yDecalDown = 20
				xDecalBox = 12
				xPosSellResult = self.X_POS_LEFT_BOOK_GOODS + 20
				yPosSellResult = self.Y_POS_LEFT_BOOK_GOODS + self.Y_SIZE_LEFT_BOOK_GOODS + 20
				szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_WAREHOUSE_FREE_SPACE", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
				screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPosSellResult, yPosSellResult + iSize/4 + yDecalDown, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), xPosSellResult - xDecalBox + xPosBox, yPosSellResult + yDecalDown, xSizeBox, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szSpace = u"<font=2>%d</font>" % (gc.getUnitInfo(pShip.getUnitType()).getCargoNewSpace()-pShip.getNewCargo())
				screen.setLabel(self.getNextWidgetName(), "background", szSpace, CvUtil.FONT_RIGHT_JUSTIFY, xPosSellResult - xDecalBox + xPosBox + xSizeBox - iSize*3/4 - 2, yPosSellResult + iSize/4 + yDecalDown, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_QUANTITY").getPath(), xPosSellResult - xDecalBox + xPosBox + xSizeBox - iSize*3/4, yPosSellResult + iSize/6 + yDecalDown, iSize*3/4, iSize*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1)
				#Valider
				iValidButtonX = xPosSellResult - 5
				iValidButtonY = self.Y_POS_QUANTITY_SCREEN - 5
				screen.setButtonGFC(self.getNextWidgetName(), u"<font=2>" + localText.getText("TXT_KEY_VALIDATE", ()) + u"</font>", "", iValidButtonX, iValidButtonY, 80, 25, WidgetTypes.WIDGET_GENERAL, self.VALID_TRANSFERT_1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
			else:
				xPosNoGoods = self.X_POS_LEFT_BOOK_GOODS + 20
				yPosNoGoods = self.Y_POS_LEFT_BOOK_GOODS + 20			
				szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_TRADE_SELL_NO_RESSOURCES", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
				screen.setLabel(self.getNextWidgetName(), "background", u"<font=1b>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPosNoGoods, yPosNoGoods, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_TRADE_NO_SHIPS", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TITLE_LEFT_TRADE_BOOK, self.Y_POS_TITLE_TRADE_BOOK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
	def getWarehouseSpace(self):
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		
		iSpace = player.getEuropeWarehouseCapacity()
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			iSpace -= player.getEuropeWarehouseYield(iYield)
		return iSpace
		
	def showQuantityButtons(self):
		screen = self.getScreen()
		iQuantity = self.iQuantity
		TabQ = [1, 5, 10, 15, 30]
		TabA = ["INTERFACE_EUROPE_TRADE_COEF001", "INTERFACE_EUROPE_TRADE_COEF010", "INTERFACE_EUROPE_TRADE_COEF030", "INTERFACE_EUROPE_TRADE_COEF100", "INTERFACE_EUROPE_TRADE_COEF250"]
		TabN = [u"", u"", u"", u"", u""]
		for iTab in range(len(TabQ)):
			TabN[iTab] = localText.changeTextColor(u"%d" % (TabQ[iTab]), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
			if iQuantity == TabQ[iTab]:
				szArtFile = ArtFileMgr.getInterfaceArtInfo(TabA[iTab]).getPath()
				TabN[iTab] = localText.changeTextColor(u"%d" % (TabQ[iTab]), gc.getInfoTypeForString("COLOR_FONT_CREAM"))		
				
		screen.addDDSGFC(self.getNextWidgetName(), szArtFile, self.X_POS_QUANTITY_SCREEN, self.Y_POS_QUANTITY_SCREEN, self.X_SIZE_QUANTITY_SCREEN, self.Y_SIZE_QUANTITY_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		iDecalY = 2
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + TabN[0] + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_QUANTITY_SCREEN + self.XResolution*23/1024, self.Y_POS_QUANTITY_SCREEN + iDecalY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + TabN[1] + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_QUANTITY_SCREEN + self.XResolution*56/1024, self.Y_POS_QUANTITY_SCREEN + iDecalY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + TabN[2] + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_QUANTITY_SCREEN + self.XResolution*90/1024, self.Y_POS_QUANTITY_SCREEN + iDecalY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + TabN[3] + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_QUANTITY_SCREEN + self.XResolution*125/1024, self.Y_POS_QUANTITY_SCREEN + iDecalY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + TabN[4] + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_QUANTITY_SCREEN + self.XResolution*159/1024, self.Y_POS_QUANTITY_SCREEN + iDecalY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		for iTab in range(len(TabQ)):
			screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_TRANSFERT_INVISIBLE").getPath(), self.X_POS_QUANTITY_SCREEN + self.X_SIZE_QUANTITY_SCREEN*iTab/5, self.Y_POS_QUANTITY_SCREEN, self.X_SIZE_QUANTITY_SCREEN/5, self.Y_SIZE_QUANTITY_SCREEN, WidgetTypes.WIDGET_GENERAL, self.CHANGE_QUANTITY, TabQ[iTab] )
		
	
	def showShipEuropeInterface(self):
		screen = self.getScreen()
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		playerEurope = gc.getPlayer(player.getParent())

		i = 0
		bSelectedShip = false
		self.showEuropeInterface(true)	# J'affiche la page de l'Europe
		for pShip in self.EuropeUnitsList:
			if self.I_SELECTED_SHIP == i:
				bSelectedShip = true
				break
			i += 1
			
		szSize = u"<font=3>"
		if self.XResolution/1280 >= 1:
			szSize = u"<font=4>"
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_SCREEN_TITLE", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", szSize + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TITLE_RIGHT_TRADE_BOOK, self.Y_POS_TITLE_TRADE_BOOK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
		if bSelectedShip:
			szText = localText.changeTextColor(pShip.getName(), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
			screen.setLabel(self.getNextWidgetName(), "background", szSize + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TITLE_LEFT_TRADE_BOOK, self.Y_POS_TITLE_TRADE_BOOK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			iStartX = 5
			iDecalY = 5
			iPosY = 0
			iSpacingY = 5
			iSize = self.CARGO_ICON_SIZE*3/4			
			xPosBox = iStartX + iSize*3 - 5
			xSizeBox = iSize*2 + 10
			xTotal = 0
			for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				kYield = gc.getYieldInfo(iYield)
				if kYield.isCargo():
					if pShip.getNewCargoYield(iYield) > 0:
						screen.addDDSGFCAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), iStartX, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
						screen.setImageButtonAt(self.getNextWidgetName(), "LeftBookGoods", gc.getYieldInfo(iYield).getIcon(), iStartX, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.TOTAL_CHANGE_SHIP, iYield)
						screen.addDDSGFCAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), iStartX + iSize, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
						szQuantity = u"<font=2>%d</font>" % (self.ShipGoods[iYield])
						screen.setLabelAt(self.getNextWidgetName(), "LeftBookGoods", szQuantity, CvUtil.FONT_CENTER_JUSTIFY, iStartX + iSize*3/2, iPosY*(iSize+iSpacingY) + (iSize+iSpacingY)*5/12 + 2 + iDecalY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setImageButtonAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_PLUS").getPath(), iStartX + iSize*2, iPosY*(iSize+iSpacingY) + iDecalY, iSize*2/3, iSize/2 + 3, WidgetTypes.WIDGET_GENERAL, self.CHANGE_QUANTITY_SHIP_UP, iYield)
						screen.setImageButtonAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_MOINS").getPath(), iStartX + iSize*2, iPosY*(iSize+iSpacingY) + iDecalY + iSize/2-2, iSize*2/3, iSize/2 + 3, WidgetTypes.WIDGET_GENERAL, self.CHANGE_QUANTITY_SHIP_DOWN, iYield)
						screen.addDDSGFCAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), xPosBox, iPosY*(iSize+iSpacingY) + iDecalY, xSizeBox, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
						screen.addDDSGFCAt(self.getNextWidgetName(), "LeftBookGoods", ArtFileMgr.getInterfaceArtInfo("SCREEN_GOLD_PILE").getPath(), xPosBox + xSizeBox - iSize*3/4, iPosY*(iSize+iSpacingY) + iDecalY + iSize/6, iSize*3/4, iSize*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
						iPriceEstimate = player.getSellPriceForYield(iYield, self.ShipGoods[iYield])
						szPrices = u"<font=2>%d</font>" % (iPriceEstimate)
						screen.setLabelAt(self.getNextWidgetName(), "LeftBookGoods", szPrices, CvUtil.FONT_RIGHT_JUSTIFY, xPosBox + xSizeBox - iSize*3/4 - 2, iPosY*(iSize+iSpacingY) + iDecalY + iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						xTotal += iPriceEstimate
						iPosY += 1
			if iPosY > 0:
				#including tax
				yDecalDown = 20
				xDecalBox = 12
				xPosSellResult = self.X_POS_LEFT_BOOK_GOODS + 20
				yPosSellResult = self.Y_POS_LEFT_BOOK_GOODS + self.Y_SIZE_LEFT_BOOK_GOODS + 20
				szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_TRADE_SELL_RESULT", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
				screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPosSellResult, yPosSellResult + iSize/4 + yDecalDown, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), xPosSellResult - xDecalBox + xPosBox, yPosSellResult + yDecalDown, xSizeBox, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szPrices = u"<font=2>%d</font>" % (xTotal)
				screen.setLabel(self.getNextWidgetName(), "background", szPrices, CvUtil.FONT_RIGHT_JUSTIFY, xPosSellResult - xDecalBox + xPosBox + xSizeBox - iSize*3/4 - 2, yPosSellResult + iSize/4 + yDecalDown, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("SCREEN_GOLD_PILE").getPath(), xPosSellResult - xDecalBox + xPosBox + xSizeBox - iSize*3/4, yPosSellResult + iSize/6 + yDecalDown, iSize*3/4, iSize*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
				screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_UNLOAD_UNIT").getPath(), xPosSellResult - xDecalBox + xPosBox + xSizeBox, yPosSellResult + yDecalDown - 11, iSize*5/3, iSize*5/3, WidgetTypes.WIDGET_GENERAL, self.UNLOAD_ALL, -1)

				#Valider
				iValidButtonX = xPosSellResult - 5
				iValidButtonY = self.Y_POS_QUANTITY_SCREEN - 5
				screen.setButtonGFC(self.getNextWidgetName(), u"<font=2>" + localText.getText("TXT_KEY_VALIDATE", ()) + u"</font>", "", iValidButtonX, iValidButtonY, 80, 25, WidgetTypes.WIDGET_GENERAL, self.VALID_SELL, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
			else:
				xPosNoGoods = self.X_POS_LEFT_BOOK_GOODS + 20
				yPosNoGoods = self.Y_POS_LEFT_BOOK_GOODS + 20			
				szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_TRADE_SELL_NO_RESSOURCES", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
				screen.setLabel(self.getNextWidgetName(), "background", u"<font=1b>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPosNoGoods, yPosNoGoods, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_TRADE_NO_SHIPS", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
			screen.setLabel(self.getNextWidgetName(), "background", szSize + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_TITLE_LEFT_TRADE_BOOK, self.Y_POS_TITLE_TRADE_BOOK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			xPosSellResult = self.X_POS_LEFT_BOOK_GOODS + 20
			yPosSellResult = self.Y_POS_LEFT_BOOK_GOODS + 20
			#screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TACHE").getPath(), xPosSellResult, yPosSellResult, self.X_SIZE_LEFT_BOOK_GOODS*4/5, self.X_SIZE_LEFT_BOOK_GOODS*4/5, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
	def showEuropeInterface(self, bShip):
		screen = self.getScreen()
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		playerEurope = gc.getPlayer(player.getParent())
		
		iStartX = 5
		iDecalY = 5
		iPosY = 0
		iSpacingY = 5
		iSize = self.CARGO_ICON_SIZE*3/4			
		xPosBox = iStartX + iSize*3 - 5
		xSizeBox = iSize*2 + 10
		xTotal = 0
		
		szSize = u"<font=1b>"
		if self.XResolution/1280 >= 1:
			szSize = u"<font=2b>"
			
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if self.ifYieldSelected(iYield):
				screen.addDDSGFCAt(self.getNextWidgetName(), "RightBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), iStartX, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
				screen.setImageButtonAt(self.getNextWidgetName(), "RightBookGoods", gc.getYieldInfo(iYield).getIcon(), iStartX, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.TOTAL_CHANGE_EUROPE, iYield)
				screen.addDDSGFCAt(self.getNextWidgetName(), "RightBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), iStartX + iSize, iPosY*(iSize+iSpacingY) + iDecalY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
				szQuantity = u"<font=2>%d</font>" % (self.EuropeGoods[iYield])
				screen.setLabelAt(self.getNextWidgetName(), "RightBookGoods", szQuantity, CvUtil.FONT_CENTER_JUSTIFY, iStartX + iSize*3/2, iPosY*(iSize+iSpacingY) + (iSize+iSpacingY)*5/12 + 2 + iDecalY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setImageButtonAt(self.getNextWidgetName(), "RightBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_PLUS").getPath(), iStartX + iSize*2, iPosY*(iSize+iSpacingY) + iDecalY, iSize*2/3, iSize/2 + 3, WidgetTypes.WIDGET_GENERAL, self.CHANGE_QUANTITY_EUROPE_UP, iYield)
				screen.setImageButtonAt(self.getNextWidgetName(), "RightBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_MOINS").getPath(), iStartX + iSize*2, iPosY*(iSize+iSpacingY) + iDecalY + iSize/2-2, iSize*2/3, iSize/2 + 3, WidgetTypes.WIDGET_GENERAL, self.CHANGE_QUANTITY_EUROPE_DOWN, iYield)
				screen.addDDSGFCAt(self.getNextWidgetName(), "RightBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), xPosBox, iPosY*(iSize+iSpacingY) + iDecalY, xSizeBox, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
				screen.addDDSGFCAt(self.getNextWidgetName(), "RightBookGoods", ArtFileMgr.getInterfaceArtInfo("SCREEN_GOLD_PILE").getPath(), xPosBox + xSizeBox - iSize*3/4, iPosY*(iSize+iSpacingY) + iDecalY + iSize/6, iSize*3/4, iSize*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
				iPriceEstimate = player.getBuyPriceForYield(iYield, self.EuropeGoods[iYield])
				szPrices = u"<font=2>%d</font>" % (iPriceEstimate)
				screen.setLabelAt(self.getNextWidgetName(), "RightBookGoods", szPrices, CvUtil.FONT_RIGHT_JUSTIFY, xPosBox + xSizeBox - iSize*3/4 - 2, iPosY*(iSize+iSpacingY) + iDecalY + iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setImageButtonAt(self.getNextWidgetName(), "RightBookGoods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_REMOVE").getPath(), xPosBox + xSizeBox - 2, iPosY*(iSize+iSpacingY) + iDecalY + iSize/8, iSize*3/4, iSize*3/4, WidgetTypes.WIDGET_GENERAL, self.REMOVE_SELECTED_YIELD, iYield)
				pinArt =  ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_PIN_YIELDS").getPath()
				if self.PinGoods[iYield] == 1:
					pinArt =  ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_HIGHLIGHT_PIN_YIELDS").getPath()				
				screen.setImageButtonAt(self.getNextWidgetName(), "RightBookGoods", pinArt, xPosBox + xSizeBox + iSize*3/5, iPosY*(iSize+iSpacingY) + iDecalY + iSize/5, iSize*5/8, iSize*5/8, WidgetTypes.WIDGET_GENERAL, self.PIN_SELECTED_YIELD, iYield)
				xTotal += iPriceEstimate
				iPosY += 1
		if iPosY > 0:
			yDecalDown = 20
			xDecalBox = 12
			xPosSellResult = self.X_POS_RIGHT_BOOK_GOODS + 20
			yPosSellResult = self.Y_POS_RIGHT_BOOK_GOODS + self.Y_SIZE_RIGHT_BOOK_GOODS + 20
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_TRADE_PURCHASE_RESULT", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
			screen.setLabel(self.getNextWidgetName(), "background", u"<font=1>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPosSellResult, yPosSellResult + iSize/4 + yDecalDown, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), xPosSellResult - xDecalBox + xPosBox, yPosSellResult + yDecalDown, xSizeBox, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1)
			szPrices = u"<font=2>%d</font>" % (xTotal)
			screen.setLabel(self.getNextWidgetName(), "background", szPrices, CvUtil.FONT_RIGHT_JUSTIFY, xPosSellResult - xDecalBox + xPosBox + xSizeBox - iSize*3/4 - 2, yPosSellResult + iSize/4 + yDecalDown, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("SCREEN_GOLD_PILE").getPath(), xPosSellResult - xDecalBox + xPosBox + xSizeBox - iSize*3/4, yPosSellResult + iSize/6 + yDecalDown, iSize*3/4, iSize*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1)
			#Valider
			iValidButtonX = xPosSellResult + 100
			iValidButtonY = self.Y_POS_QUANTITY_SCREEN - 5
			screen.setButtonGFC(self.getNextWidgetName(), u"<font=2>" + localText.getText("TXT_KEY_VALIDATE", ()) + u"</font>", "", iValidButtonX, iValidButtonY, 80, 25, WidgetTypes.WIDGET_GENERAL, self.VALID_BUY, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		else:
			xPosNoGoods = self.X_POS_RIGHT_BOOK_GOODS + 20
			yPosNoGoods = self.Y_POS_RIGHT_BOOK_GOODS + 20			
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_TRADE_SELECTED_DESIRED_RESOURCES", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
			screen.setLabel(self.getNextWidgetName(), "background", szSize + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPosNoGoods, yPosNoGoods, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def ifYieldSelected(self, iYield):
		if self.PinGoods[iYield] == 1:
			return True

		return self.SelectedGoods[iYield] > 0

	def showButtonsRessources(self):
		screen = self.getScreen()
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		bPrices = self.bPrices
		iPosXGold = self.X_POS_GOODS_TITLE + 5
		iPosy = self.Y_POS_GOODS_TITLE + self.Y_SIZE_GOODS_TITLE - 2
		iPosXQuantity = iPosXGold + 40
		
		xSize = self.XResolution*125/1024
		ySize = self.YResolution*13/256
		iPosXOnglet = self.X_POS_GOODS_TITLE + 1
		iPosYOnglet = iPosy - 5
		screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ONGLET_MARCHANDISE").getPath(), iPosXOnglet, iPosYOnglet, xSize, ySize, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		iPosy -= 1
		xSizeIcon = 50
		ySizeIcon = 31
		if bPrices:
			screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_QUANTITY").getPath(), iPosXQuantity, iPosy, xSizeIcon, ySizeIcon, WidgetTypes.WIDGET_GENERAL, self.CHANGE_MODE_PRICE, 0)
			screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_HIGHLIGHT_GOLD").getPath(), iPosXGold, iPosy, xSizeIcon, ySizeIcon, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_HIGHLIGHT_QUANTITY").getPath(), iPosXQuantity, iPosy, xSizeIcon, ySizeIcon, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setImageButton(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_TRADE_GOLD").getPath(), iPosXGold, iPosy, xSizeIcon, ySizeIcon, WidgetTypes.WIDGET_GENERAL, self.CHANGE_MODE_PRICE, 1)
		
	def getNbPages(self):
		iTotal = 0
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			kYield = gc.getYieldInfo(iYield)
			if kYield.isCargo() and not player.isHasYieldUnknown(iYield):
				iTotal += 1
		return iTotal/17
	
	def showGoods(self):
		screen = self.getScreen()
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		playerEurope = gc.getPlayer(player.getParent())
		
		xSize = self.XResolution*125/1024
		ySize = self.YResolution*11/256
		iStartX = self.XResolution*3/1024
		iStartY = 0
		iSpacingY = ySize
		xPosArrowLeft = self.XResolution*15/1024
		xPosArrowRight = self.XResolution*5/64	
		iPosY = 0
		iNb = 0
		yDecal = self.XResolution/192
		
		page = self.iPage
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			kYield = gc.getYieldInfo(iYield)
			if kYield.isCargo() and not player.isHasYieldUnknown(iYield):
				if iNb >= 17*page and iNb < 17*(page+1):
					screen.setImageButtonAt(self.getNextWidgetName(), "Goods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ONGLET_MARCHANDISE").getPath(), iStartX, iStartY + iPosY*iSpacingY, xSize, ySize, WidgetTypes.WIDGET_GENERAL, -1, -1)
					screen.setImageButtonAt(self.getNextWidgetName(), "Goods", gc.getYieldInfo(iYield).getIcon(), xSize - 34, iStartY - 3 + iPosY*iSpacingY, 30, 30,  WidgetTypes.WIDGET_GENERAL, -1, -1)
					if self.bPrices:
						szValue = u"<font=2>%d/%d</font>" % (player.getSellPriceForYield(iYield, 1), player.getBuyPriceForYield(iYield, 1))
					else:
						szValue = u"<font=2>%d</font>" % (playerEurope.getEuropeWarehouseYield(iYield))
					szValue = localText.changeTextColor(szValue, gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
					screen.setLabelAt(self.getNextWidgetName(), "Goods", szValue, CvUtil.FONT_CENTER_JUSTIFY, iStartX+xPosArrowRight - 30, iStartY + 2 + iPosY*iSpacingY+yDecal+10, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					screen.setImageButtonAt(self.getNextWidgetName(), "Goods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_TRANSFERT_INVISIBLE").getPath(), iStartX, iStartY + iPosY*iSpacingY, xSize, ySize, WidgetTypes.WIDGET_GENERAL, self.YIELD_PRICE, iYield)
					iPosY += 1
				iNb += 1 
		
		while iPosY < 17:
			screen.setImageButtonAt(self.getNextWidgetName(), "Goods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ONGLET_MARCHANDISE").getPath(), iStartX, iStartY + iPosY*iSpacingY, xSize, ySize, WidgetTypes.WIDGET_GENERAL, -1, -1)
			iPosY += 1
		
		screen.setImageButtonAt(self.getNextWidgetName(), "Goods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ONGLET_MARCHANDISE").getPath(), iStartX, iStartY + iPosY*iSpacingY, xSize, ySize, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iNbPage = self.getNbPages()
		xArrowSize = self.XResolution*31/1024
		yArrowSize = self.YResolution*20/768
		iStartY = 2
		if page != 0:
			screen.setImageButtonAt(self.getNextWidgetName(), "Goods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_LEFT").getPath(), iStartX+xPosArrowLeft, iStartY + iPosY*iSpacingY +yDecal, xArrowSize, yArrowSize, WidgetTypes.WIDGET_GENERAL, self.CHANGE_PAGE, -1)
		else:
			screen.setImageButtonAt(self.getNextWidgetName(), "Goods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_LEFT_SHADOW").getPath(), iStartX+xPosArrowLeft, iStartY + iPosY*iSpacingY+yDecal, xArrowSize, yArrowSize, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if page != iNbPage:
			screen.setImageButtonAt(self.getNextWidgetName(), "Goods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_RIGHT").getPath(), iStartX+xPosArrowRight, iStartY + iPosY*iSpacingY+yDecal, xArrowSize, yArrowSize, WidgetTypes.WIDGET_GENERAL, self.CHANGE_PAGE, 1)
		else:
			screen.setImageButtonAt(self.getNextWidgetName(), "Goods", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ARROW_RIGHT_SHADOW").getPath(), iStartX+xPosArrowRight, iStartY + iPosY*iSpacingY+yDecal, xArrowSize, yArrowSize, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szPage = u"<font=3b>%d</font>" % (page+1)
		szPage = localText.changeTextColor(szPage, gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabelAt(self.getNextWidgetName(), "Goods", szPage, CvUtil.FONT_CENTER_JUSTIFY, iStartX+xPosArrowRight - self.XResolution*17/1024, iPosY*iSpacingY+yDecal+12, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def showCargaison(self):
		screen = self.getScreen()
		
		iUnit = self.I_SELECTED_SHIP
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		
		ShipPanelWidth = self.IN_PORT_PANE_WIDTH - (self.W_TEXT_MARGIN * 3 / 2)			
		ShipPanelHight = self.CARGO_ICON_SIZE * 2 - 5
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

			screen.addDDSGFCAt("In_Port_Box", "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_IN_PORT_BOX").getPath(), 0, 5, ShipPanelWidth, ShipPanelHight, WidgetTypes.WIDGET_SHIP_CARGO, pUnitShip.getID(), -1, False)
			screen.setLabelAt(self.getNextWidgetName(), szShipPane, "<font=3>" + pUnitShip.getName().upper() + "</font>", CvUtil.FONT_LEFT_JUSTIFY, (self.CARGO_SPACING / 4) + 5, (self.CARGO_SPACING / 4) + 5 + 5, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_SHIP_CARGO, pUnitShip.getID(), pUnitShip.getID())

			for i in range(pUnitShip.cargoSpace()):
				screen.addDDSGFCAt(self.getNextWidgetName(), "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_CARGO").getPath(), ((self.CARGO_SPACING * 2 / 3) * (i)) + (self.CARGO_SPACING / 4) + 5,  5 + (ShipPanelHight / 2) - (self.CARGO_ICON_SIZE / 6), self.CARGO_ICON_SIZE * 2 / 3, self.CARGO_ICON_SIZE * 2 / 3, WidgetTypes.WIDGET_ONLY_INFO_UNIT, pUnitShip.getID(), -1, False)
			
			iSpaceCargo = pUnitShip.getOnlyNewCargo()
			j = pUnitShip.cargoSpace() - 1
			while j >= 0:
				if iSpaceCargo > 0:
					screen.addDDSGFCAt(self.getNextWidgetName(), "LoadingList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_CARGO_FULL").getPath(), ((self.CARGO_SPACING * 2 / 3) * (j)) + (self.CARGO_SPACING / 4) + 5,  5 + (ShipPanelHight / 2) - (self.CARGO_ICON_SIZE / 6), self.CARGO_ICON_SIZE * 2 / 3, self.CARGO_ICON_SIZE * 2 / 3, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					if iSpaceCargo < 30:
						szCargo = u"%d" %(iSpaceCargo)
					else:
						szCargo = u"30"
					screen.setLabelAt(self.getNextWidgetName(), "LoadingList", "<font=1>" + szCargo + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, ((self.CARGO_SPACING * 2 / 3) * (j)) + (self.CARGO_SPACING / 4) + 7 + 12,  5 + (ShipPanelHight / 2) - (self.CARGO_ICON_SIZE / 6) + self.CARGO_ICON_SIZE / 5, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_ONLY_INFO_UNIT, pUnitShip.getID(), -1)
					szCargo = u"30"
					screen.setLabelAt(self.getNextWidgetName(), "LoadingList", "<font=1>" + szCargo + "</font>", CvUtil.FONT_LEFT_JUSTIFY, ((self.CARGO_SPACING * 2 / 3) * (j)) + (self.CARGO_SPACING / 2) + 7,  5 + (ShipPanelHight / 2) - (self.CARGO_ICON_SIZE / 6) + self.CARGO_ICON_SIZE / 2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_ONLY_INFO_UNIT, pUnitShip.getID(), -1)
					iSpaceCargo -= 30
				j -= 1
			iCargoCount = 0
			plot = pUnitShip.plot()
			for i in range(plot.getNumUnits()):
				loopUnit = plot.getUnit(i)
				transportUnit = loopUnit.getTransportUnit()
				if (not transportUnit.isNone() and transportUnit.getID() == pUnitShip.getID() and transportUnit.getOwner() == pUnitShip.getOwner()):
					screen.setImageButtonAt(self.getNextWidgetName(), "LoadingList", loopUnit.getButton(), ((self.CARGO_SPACING * 2 / 3) * (iCargoCount)) + (self.CARGO_SPACING / 4) + 5, 5 + (ShipPanelHight / 2) - (self.CARGO_ICON_SIZE / 6), self.CARGO_ICON_SIZE * 2 / 3, self.CARGO_ICON_SIZE * 2 / 3, WidgetTypes.WIDGET_SHIP_CARGO, loopUnit.getID(), transportUnit.getID())
					iCargoCount = iCargoCount + 1
	
	def showContentsShip(self):
		screen = self.getScreen()
		iUnit = self.I_SELECTED_SHIP
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		iStartX = 15
		iPosX = 0
		iPosY = 0
		iDecal = 2*self.CARGO_SPACING + 6
		iDecalY = 1
		iSpacingY = 7
		i = 0
		bProcess = false
		for pUnit in self.EuropeUnitsList:
			if iUnit == i:
				bProcess = true
				break
			i += 1
		if bProcess:
			for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				kYield = gc.getYieldInfo(iYield)
				if kYield.isCargo():
					if pUnit.getNewCargoYield(iYield) > 0:
						screen.addDDSGFCAt(self.getNextWidgetName(), "ContentsShip", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), iStartX+iPosX*iDecal, iPosY*(self.CARGO_ICON_SIZE+iSpacingY) + iDecalY, self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
						screen.setImageButtonAt(self.getNextWidgetName(), "ContentsShip", gc.getYieldInfo(iYield).getIcon(), iStartX+iPosX*iDecal, iPosY*(self.CARGO_ICON_SIZE+iSpacingY) + iDecalY, self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.addDDSGFCAt(self.getNextWidgetName(), "ContentsShip", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), iStartX+iPosX*iDecal + self.CARGO_ICON_SIZE - 4, iPosY*(self.CARGO_ICON_SIZE+iSpacingY) + iDecalY, self.CARGO_ICON_SIZE, self.CARGO_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, false)
						szQuantity = u"<font=3>%d</font>" % (pUnit.getNewCargoYield(iYield))
						screen.setLabelAt(self.getNextWidgetName(), "ContentsShip", szQuantity, CvUtil.FONT_CENTER_JUSTIFY, iStartX+iPosX*iDecal + self.CARGO_ICON_SIZE*3/2 - 4, iPosY*(self.CARGO_ICON_SIZE+iSpacingY) + (self.CARGO_ICON_SIZE+iSpacingY)*5/12 + iDecalY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						iPosX += 1
						if iPosX == 3:
							iPosX = 0
							iPosY += 1
					
	def updateUnitSelected(self):
		screen = self.getScreen()
		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		iRows = screen.getTableNumRows(self.TABLE_ID)

		if (not screen.isRowSelected(self.TABLE_ID, iRows)):
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
									self.resetShipGoods()
									self.resetEuropeGoods()
									self.resetWarehouseGoods()
						i += 1
			if not bShipSelected:
				if self.I_SELECTED_SHIP != -1:
					self.I_SELECTED_SHIP = -1
					self.resetShipGoods()
					self.resetEuropeGoods()
					self.resetWarehouseGoods()
		self.fillTable(true)
		self.drawContents()
	
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
			self.updateUnitSelected()
		elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
			if inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL:
				if inputClass.getData1() == self.CHANGE_PAGE:
					self.iPage += inputClass.getData2() 
				if inputClass.getData1() == self.CHANGE_MODE_PRICE:
					self.bPrices = inputClass.getData2() 
				if inputClass.getData1() == self.CHANGE_MODE:
					self.changeMode(inputClass.getData2())
				if inputClass.getData1() == self.CHANGE_QUANTITY:
					self.iQuantity = inputClass.getData2()
					player = self.pPlayer
					player.setSelectQuantity(self.iQuantity)
				if inputClass.getData1() == self.CHANGE_QUANTITY_SHIP_UP:
					self.changeQuantityShipUp(inputClass.getData2())
				if inputClass.getData1() == self.CHANGE_QUANTITY_SHIP_DOWN:
					self.changeQuantityShipDown(inputClass.getData2())
				if inputClass.getData1() == self.TOTAL_CHANGE_SHIP:
					self.totalChangeQuantityShip(inputClass.getData2())
				if inputClass.getData1() == self.TOTAL_CHANGE_EUROPE:
					self.totalChangeQuantityEurope(inputClass.getData2())
				if inputClass.getData1() == self.TOTAL_CHANGE_WAREHOUSE:
					self.totalChangeQuantityWarehouse(inputClass.getData2())
				if inputClass.getData1() == self.UNLOAD_ALL:
					self.takeEverything()
				if inputClass.getData1() == self.VALID_SELL:
					self.validSell()
				if inputClass.getData1() == self.VALID_BUY:
					self.validBuy()
				if inputClass.getData1() == self.VALID_TRANSFERT_1:
					self.validTransfert1()
				if inputClass.getData1() == self.VALID_TRANSFERT_2:
					self.validTransfert2()
				if inputClass.getData1() == self.CHANGE_QUANTITY_EUROPE_UP:
					self.changeQuantityEuropeUp(inputClass.getData2())
				if inputClass.getData1() == self.CHANGE_QUANTITY_EUROPE_DOWN:
					self.changeQuantityEuropeDown(inputClass.getData2())
				if inputClass.getData1() == self.CHANGE_QUANTITY_WAREHOUSE_UP:
					self.changeQuantityWarehouseUp(inputClass.getData2())
				if inputClass.getData1() == self.CHANGE_QUANTITY_WAREHOUSE_DOWN:
					self.changeQuantityWarehouseDown(inputClass.getData2())
				if inputClass.getData1() == self.YIELD_PRICE:
					self.SelectedGoods[inputClass.getData2()] = (self.SelectedGoods[inputClass.getData2()]+1)%2
				if inputClass.getData1() == self.REMOVE_SELECTED_YIELD:
					self.SelectedGoods[inputClass.getData2()] = (self.SelectedGoods[inputClass.getData2()]+1)%2
					self.setPinGoods(inputClass.getData2(), 0)
				if inputClass.getData1() == self.PIN_SELECTED_YIELD:
					self.inversePinGoods(inputClass.getData2())
				if inputClass.getData1() == self.CHANGE_CURRENT_AGREEMENT:
					self.iCurrentAgreement = inputClass.getData2()
				self.drawContents()
		return 0

	def inversePinGoods(self, iYield):
		iNewValue = (self.PinGoods[iYield]+1)%2
		self.setPinGoods(iYield, iNewValue)

	def setPinGoods(self, iYield, bValue):
		player = self.pPlayer
		self.PinGoods[iYield] = bValue
		CyMessageControl().sendPlayerAction(player.getID(), PlayerActionTypes.PLAYER_ACTION_PIN_YIELD_IN_EUROPE, iYield, bValue, -1)
					
	def takeEverything(self):
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			self.ShipGoods[iYield] = 0
			self.totalChangeQuantityShip(iYield)
	
	def changeMode(self, iMode):
		player = self.pPlayer
		iCapacity = player.getEuropeWarehouseCapacity()
		
		if iMode == 2 or iMode == 3:
			if iCapacity != 0:
				self.iMode = iMode
			return
		self.resetEuropeGoods()
		self.resetWarehouseGoods()
		self.iMode = iMode
	def	totalChangeQuantityWarehouse(self, iYield):
		player = self.pPlayer
		
		if self.iMode == 3:
			if self.WarehouseGoods[iYield] == 0:
				self.WarehouseGoods[iYield] = player.getEuropeWarehouseYield(iYield)
			else:
				self.WarehouseGoods[iYield] = 0 
	def	changeQuantityWarehouseUp(self, iYield):		
		player = self.pPlayer
		iQuantity = self.iQuantity
		if self.iMode == 2:
			if self.I_SELECTED_SHIP == -1:
				return
			i = 0
			for pShip in self.EuropeUnitsList:
				if self.I_SELECTED_SHIP == i:
					break
				i += 1
			iShipCapacity = gc.getUnitInfo(pShip.getUnitType()).getCargoNewSpace()
			iShipStock = pShip.getNewCargo()
			iWantedStock = 0
			iPriceEstimate = 0
			for iYield2 in range(YieldTypes.NUM_YIELD_TYPES):
				if self.SelectedGoods[iYield2]>0:
					iWantedStock += self.WarehouseGoods[iYield2]
		
			iPlace = iShipCapacity-iShipStock-iWantedStock
			if iQuantity > iPlace:
				iQuantity = iPlace
			
			if player.getEuropeWarehouseYield(iYield) >= self.WarehouseGoods[iYield] + iQuantity:
				self.WarehouseGoods[iYield] += iQuantity
			else:
				self.WarehouseGoods[iYield] = player.getEuropeWarehouseYield(iYield)
		if self.iMode == 3:
			if player.getEuropeWarehouseYield(iYield) >= self.WarehouseGoods[iYield] + self.iQuantity:
				self.WarehouseGoods[iYield] += self.iQuantity
			else:
				self.WarehouseGoods[iYield] = player.getEuropeWarehouseYield(iYield)
	
	def	changeQuantityWarehouseDown(self, iYield):
		
		if self.WarehouseGoods[iYield] - self.iQuantity > 0:
			self.WarehouseGoods[iYield] -= self.iQuantity
		else:
			self.WarehouseGoods[iYield] = 0 
		
	def getIDSelectedShip(self):
		i = 0
		for pUnit in self.EuropeUnitsList:
			if self.I_SELECTED_SHIP == i:
				return pUnit.getID()
			i += 1
		return -1
		
	def validTransfert1(self):
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if self.ShipGoods[iYield]>0:
				CyMessageControl().sendDoCommand(self.getIDSelectedShip(), CommandTypes.COMMAND_TRANSFERT_WAREHOUSE_TO_SHIP, iYield, -self.ShipGoods[iYield], false) 
				self.ShipGoods[iYield] = 0
				
	def validTransfert2(self):
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if self.WarehouseGoods[iYield]>0:
				CyMessageControl().sendDoCommand(self.getIDSelectedShip(), CommandTypes.COMMAND_TRANSFERT_WAREHOUSE_TO_SHIP, iYield, self.WarehouseGoods[iYield], false) 
				self.WarehouseGoods[iYield] = 0
				
	def validSell(self):
		player = self.pPlayer
		if self.iMode == 1:
			for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				if self.ShipGoods[iYield]>0:
					CyMessageControl().sendDoCommand(self.getIDSelectedShip(), CommandTypes.COMMAND_TRANSFERT_EUROPE_TO_SHIP, iYield, -self.ShipGoods[iYield], false) 
					self.ShipGoods[iYield] = 0
		if self.iMode == 3:
			for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				if self.WarehouseGoods[iYield]>0:
					CyMessageControl().sendPlayerAction(player.getID(), PlayerActionTypes.PLAYER_ACTION_TRANSFERT_EUROPE_TO_WAREHOUSE, iYield, -self.WarehouseGoods[iYield], -1)
					self.WarehouseGoods[iYield] = 0
		
	def validBuy(self):
		player = self.pPlayer
		if self.iMode == 1:
			for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				if self.SelectedGoods[iYield]>0 and self.EuropeGoods[iYield]>0:
					CyMessageControl().sendDoCommand(self.getIDSelectedShip(), CommandTypes.COMMAND_TRANSFERT_EUROPE_TO_SHIP, iYield, self.EuropeGoods[iYield], false) 
					if self.PinGoods[iYield] == 0:
						self.SelectedGoods[iYield] = 0
					self.EuropeGoods[iYield] = 0
		if self.iMode == 3:
			for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				if self.SelectedGoods[iYield]>0 and self.EuropeGoods[iYield]>0:
					CyMessageControl().sendPlayerAction(player.getID(), PlayerActionTypes.PLAYER_ACTION_TRANSFERT_EUROPE_TO_WAREHOUSE, iYield, self.EuropeGoods[iYield], -1)
					if self.PinGoods[iYield] == 0:
						self.SelectedGoods[iYield] = 0
					self.EuropeGoods[iYield] = 0

	def resetWarehouseGoods(self):
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			self.WarehouseGoods[iYield] = 0
			
	def resetShipGoods(self):
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			self.ShipGoods[iYield] = 0
			
	def resetEuropeGoods(self):
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			self.EuropeGoods[iYield] = 0
			
	def	totalChangeQuantityEurope(self, iYield):
		player = self.pPlayer
		playerEurope = gc.getPlayer(player.getParent())
		iQuantity = 0
		
		if self.iMode == 1:		
			if self.I_SELECTED_SHIP == -1:
				return
			if self.EuropeGoods[iYield] > 0:
				self.EuropeGoods[iYield] = 0
				return
			self.EuropeGoods[iYield] = 0
		if self.iMode == 2:
			if self.I_SELECTED_SHIP == -1:
				return
			if self.WarehouseGoods[iYield] > 0:
				self.WarehouseGoods[iYield] = 0
				return
			self.WarehouseGoods[iYield] = 0
	
		if self.iMode == 3:
			if self.EuropeGoods[iYield] > 0:
				self.EuropeGoods[iYield] = 0
				return
			self.EuropeGoods[iYield] = 0
	
		iWantedStock = 0
		if self.iMode == 1:
			i = 0
			for pShip in self.EuropeUnitsList:
				if self.I_SELECTED_SHIP == i:
					break
				i += 1
			iShipCapacity = gc.getUnitInfo(pShip.getUnitType()).getCargoNewSpace()
			iShipStock = pShip.getNewCargo()
			iPriceEstimate = 0
			for iYield2 in range(YieldTypes.NUM_YIELD_TYPES):
				if self.SelectedGoods[iYield2]>0:
					iWantedStock += self.EuropeGoods[iYield2]
					iPriceEstimate += player.getBuyPriceForYield(iYield2, self.EuropeGoods[iYield2])
			
			iQuantity = iShipCapacity-iShipStock-iWantedStock
			if not pShip.isOnlyDefensive():
				iQuantity = 0 # Avoid to war ship to buy yields
			if playerEurope.getEuropeWarehouseYield(iYield) < iQuantity:
				iQuantity = playerEurope.getEuropeWarehouseYield(iYield)
			iPriceEstimate += player.getBuyPriceForYield(iYield, iQuantity)
			
			if player.getGold() < iPriceEstimate:
				iQuantity = self.calculateBetterPrice(iYield, iPriceEstimate, iQuantity)
			self.EuropeGoods[iYield] = iQuantity	
		if self.iMode == 2:
			i = 0
			for pShip in self.EuropeUnitsList:
				if self.I_SELECTED_SHIP == i:
					break
				i += 1
			iShipCapacity = gc.getUnitInfo(pShip.getUnitType()).getCargoNewSpace()
			iShipStock = pShip.getNewCargo()
			for iYield2 in range(YieldTypes.NUM_YIELD_TYPES):
				iWantedStock += self.WarehouseGoods[iYield2]
				
			iQuantity = iShipCapacity-iShipStock-iWantedStock
			if not pShip.isOnlyDefensive():
				iQuantity = 0 # Avoid to war ship to buy yields
			if player.getEuropeWarehouseYield(iYield) < iQuantity:
				iQuantity = player.getEuropeWarehouseYield(iYield)
			
			self.WarehouseGoods[iYield] = iQuantity	
		if self.iMode == 3:
			iPriceEstimate = 0
			for iYield2 in range(YieldTypes.NUM_YIELD_TYPES):
				if self.SelectedGoods[iYield2] > 0:
					iWantedStock += self.EuropeGoods[iYield2]
					iPriceEstimate += player.getBuyPriceForYield(iYield2, self.EuropeGoods[iYield2])
			
			iQuantity = self.getWarehouseSpace() - iWantedStock
			if playerEurope.getEuropeWarehouseYield(iYield) < iQuantity:
				iQuantity = playerEurope.getEuropeWarehouseYield(iYield)
			iPriceEstimate += player.getBuyPriceForYield(iYield, iQuantity)
			
			if player.getGold() < iPriceEstimate:
				iQuantity = self.calculateBetterPrice(iYield, iPriceEstimate, iQuantity)
			self.EuropeGoods[iYield] = iQuantity	
		
	def	totalChangeQuantityShip(self, iYield):
		i = 0
		bSelectedShip = false
		for pShip in self.EuropeUnitsList:
			if self.I_SELECTED_SHIP == i:
				bSelectedShip = true
				break
			i += 1
		if bSelectedShip:
			if self.ShipGoods[iYield] > 0:
				self.ShipGoods[iYield] = 0
			else:
				if self.iMode == 2:
					iSpace = self.getWarehouseSpace()
					for iYield2 in range(YieldTypes.NUM_YIELD_TYPES):
						iSpace -= self.ShipGoods[iYield2]
					iQuantity = pShip.getNewCargoYield(iYield)
					if iSpace < iQuantity:
						iQuantity = iSpace
					self.ShipGoods[iYield] = iQuantity
				else:
					self.ShipGoods[iYield] = pShip.getNewCargoYield(iYield)
			
	def	changeQuantityEuropeUp(self, iYield):
		player = self.pPlayer
		playerEurope = gc.getPlayer(player.getParent())
		iQuantity = self.iQuantity
		if self.iMode == 1:
			if self.I_SELECTED_SHIP == -1:
				return
			i = 0
			for pShip in self.EuropeUnitsList:
				if self.I_SELECTED_SHIP == i:
					break
				i += 1
			iShipCapacity = gc.getUnitInfo(pShip.getUnitType()).getCargoNewSpace()
			iShipStock = pShip.getNewCargo()
			iWantedStock = 0
			iPriceEstimate = 0
			for iYield2 in range(YieldTypes.NUM_YIELD_TYPES):
				if self.SelectedGoods[iYield2]>0:
					iWantedStock += self.EuropeGoods[iYield2]
					iQuantityToBuy = self.EuropeGoods[iYield2]
					if iYield == iYield2:
						iQuantityToBuy += iQuantity
					iPriceEstimate += player.getBuyPriceForYield(iYield2, iQuantityToBuy)
			
			if player.getGold() < iPriceEstimate:
				iQuantity = self.calculateBetterPrice(iYield, iPriceEstimate, iQuantity)
			
			iPlace = iShipCapacity-iShipStock-iWantedStock
			if iQuantity > iPlace:
				iQuantity = iPlace
			if not pShip.isOnlyDefensive():
				iQuantity = 0 # Avoid to war ship to buy yields				
		if self.iMode == 3:
			iWantedStock = 0
			iPriceEstimate = 0
			for iYield2 in range(YieldTypes.NUM_YIELD_TYPES):
				if self.SelectedGoods[iYield2]>0:
					iWantedStock += self.EuropeGoods[iYield2]
					iQuantityToBuy = self.EuropeGoods[iYield2]
					if iYield == iYield2:
						iQuantityToBuy += iQuantity
					iPriceEstimate += player.getBuyPriceForYield(iYield2, iQuantityToBuy)
			if player.getGold() < iPriceEstimate:
				iQuantity = self.calculateBetterPrice(iYield, iPriceEstimate, iQuantity)
			
			iPlace = self.getWarehouseSpace()-iWantedStock
			if iQuantity > iPlace:
				iQuantity = iPlace
		if playerEurope.getEuropeWarehouseYield(iYield) >= self.EuropeGoods[iYield] + iQuantity:
			self.EuropeGoods[iYield] += iQuantity
		else:
			self.EuropeGoods[iYield] = playerEurope.getEuropeWarehouseYield(iYield)
	
	def calculateBetterPrice(self, iYield, iPriceEstimate, iQuantity):
		player = self.pPlayer
		iPlayerGold = player.getGold()
		iStartQuantity = self.EuropeGoods[iYield] + iQuantity
		iStartPrice = iPriceEstimate - player.getBuyPriceForYield(iYield, iStartQuantity)
		
		for x in range(iQuantity+1):
			iPrice = player.getBuyPriceForYield(iYield, self.EuropeGoods[iYield] + x)
			if iPlayerGold < iStartPrice + iPrice:
				break
		return (x-1)
		
	def	changeQuantityEuropeDown(self, iYield):
		
		if self.EuropeGoods[iYield] - self.iQuantity > 0:
			self.EuropeGoods[iYield] -= self.iQuantity
		else:
			self.EuropeGoods[iYield] = 0 
		
	def	changeQuantityShipUp(self, iYield):
		i = 0
		bSelectedShip = false
		for pShip in self.EuropeUnitsList:
			if self.I_SELECTED_SHIP == i:
				bSelectedShip = true
				break
			i += 1
		if bSelectedShip:
			if self.iMode == 2:
				iSpace = self.getWarehouseSpace()
				for iYield2 in range(YieldTypes.NUM_YIELD_TYPES):
					iSpace -= self.ShipGoods[iYield2]
				iQuantity = self.iQuantity
				if iSpace < iQuantity:
					iQuantity = iSpace
				if pShip.getNewCargoYield(iYield) >= self.ShipGoods[iYield] + iQuantity:
					self.ShipGoods[iYield] += iQuantity
				else:
					self.ShipGoods[iYield] = pShip.getNewCargoYield(iYield) 
			else:
				if pShip.getNewCargoYield(iYield) >= self.ShipGoods[iYield] + self.iQuantity:
					self.ShipGoods[iYield] += self.iQuantity
				else:
					self.ShipGoods[iYield] = pShip.getNewCargoYield(iYield) 
			
	def	changeQuantityShipDown(self, iYield):
		i = 0
		bSelectedShip = false
		for pShip in self.EuropeUnitsList:
			if self.I_SELECTED_SHIP == i:
				bSelectedShip = true
				break
			i += 1
		if bSelectedShip:
			if self.ShipGoods[iYield] - self.iQuantity > 0:
				self.ShipGoods[iYield] -= self.iQuantity
			else:
				self.ShipGoods[iYield] = 0 
		
	def update(self, fDelta):
		screen = self.getScreen()		
		if (CyInterface().isDirty(InterfaceDirtyBits.EuropeC2Screen_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.EuropeC2Screen_DIRTY_BIT, False)
			self.resetPanelsBook()
			self.drawContents()
			
		return

	def taxeHelp(self):
		pPlayer = self.pPlayer
		
		szText = localText.getText("TXT_KEY_MISC_MAIN_TAX", (pPlayer.getTaxRate(), ))
		szText += u"\n"
		szText += localText.getText("TXT_KEY_MISC_LOAN_TAX", (pPlayer.getEuropeLoanPercent(), ))
		
		return szText
		
	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		if eWidgetType == WidgetTypes.WIDGET_GENERAL:
			if  iData1 == self.TREASURY_ID:
				return localText.getText("TXT_KEY_ECON_GOLD_RESERVE", ())
			if  iData1 == self.NO_SHIP_SELECTED:
				return localText.getText("TXT_KEY_ECON_NO_SHIP_SELECTED", ())
			if iData1 == self.TOTAL_CHANGE_SHIP or iData1 == self.TOTAL_CHANGE_EUROPE or iData1 == self.TOTAL_CHANGE_WAREHOUSE:
				return localText.getText("TXT_KEY_HELP_ICON_YIELD", ())
			if iData1 == self.TAX_HELP:
				return self.taxeHelp()
			if iData1 == self.UNLOAD_ALL:
				return localText.getText("TXT_KEY_HELP_TAKE_EVERYTHING_YIELD", ())
			if iData1 == self.REMOVE_SELECTED_YIELD:
				return localText.getText("TXT_KEY_HELP_REMOVE_SELECTED_YIELD", ())
			if iData1 == self.YIELD_PRICE:
				return self.YieldMessage(iData2)
			if iData1 == self.PIN_SELECTED_YIELD:
				return self.getPinYieldMessage(iData2)
			if iData1 == self.CHANGE_MODE and self.iMode != iData2:
				if iData2 == 1:
					return localText.getText("TXT_KEY_HELP_SHIP_EUROPE", ())
				if iData2 == 2:
					iCapacity = player.getEuropeWarehouseCapacity()
					if iCapacity == 0:
						return localText.getText("TXT_KEY_HELP_NO_WAREHOUSE", ())
					else:
						return localText.getText("TXT_KEY_HELP_SHIP_WAREHOUSE", ())
				if iData2 == 3:
					iCapacity = player.getEuropeWarehouseCapacity()
					if iCapacity == 0:
						return localText.getText("TXT_KEY_HELP_NO_WAREHOUSE", ())
					else:
						return localText.getText("TXT_KEY_HELP_WAREHOUSE_EUROPE", ())
				
		return u""
	
	def getPinYieldMessage(self, eYield):
		if(self.PinGoods[eYield] == 1):
			return localText.getText("TXT_KEY_HELP_UNPIN_YIELD", ())
		else:
			return localText.getText("TXT_KEY_HELP_PIN_YIELD", ())
			
	def YieldMessage(self, eYield):
		player = self.pPlayer
		playerEurope = gc.getPlayer(player.getParent())
		
		szBuffer = u"%s\n" % (gc.getYieldInfo(eYield).getDescription())
		szBuffer = localText.changeTextColor(szBuffer, gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"))
		
		szBuffer += localText.getText("TXT_KEY_BUY_AND_SELL_YIELD", (player.getSellPriceForYield(eYield, 1), player.getBuyPriceForYield(eYield, 1)))
		szBuffer += u"\n" + localText.getText("TXT_KEY_EUROPE_QUANTITY", (playerEurope.getEuropeWarehouseYield(eYield), ))
		
		if (gc.getYieldInfo(eYield).isRawMaterial()):
			iEuropeNeeds = playerEurope.getEuropeNeeds(eYield)
			szEuropeNeeds = localText.getText("TXT_KEY_EUROPE_NEEDS_FOR_YIELD", (iEuropeNeeds, ))
			szBuffer += u"\n" + localText.changeTextColor(szEuropeNeeds, gc.getInfoTypeForString(self.getEuropeNeedsColor(iEuropeNeeds)))

		szBuffer += u"\n-----------------------"

		for eProfession in range(gc.getNumProfessionInfos()):
			if (player.isProfessionValid(eProfession, UnitTypes.NO_UNIT)):
				iNumRequired = player.getYieldEquipmentAmount(eProfession, eYield)
				if (iNumRequired > 0):
					szBuffer += u"\n"
					szBuffer += localText.getText("TXT_KEY_YIELD_NEEDED_FOR_PROFESSION", (iNumRequired, gc.getProfessionInfo(eProfession).getTextKey()))
		
		return szBuffer
	
	def getEuropeNeedsColor(self, iEuropeNeeds):
		if (iEuropeNeeds >= 65):
			return "COLOR_GREEN"
		if (iEuropeNeeds > 35):
			return "COLOR_PLAYER_ORANGE_TEXT"
		return "COLOR_RED"

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
	
	def showEuropeNeeds(self):
		screen = self.getScreen()
		player = self.pPlayer
		europePlayer = gc.getPlayer(player.getParent())
		neededYields = []

		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isRawMaterial() and not player.isHasYieldUnknown(iYield):
				neededYields.append((europePlayer.getEuropeNeeds(iYield), iYield))
		neededYields.sort()
		numMostNeededYield = max(min(len(neededYields) - 1, 3), 0)
		numLessNeededYield = max(min(len(neededYields) - numMostNeededYield, 3), 0)

		xPos =  self.xSize(50)
		yPos = self.ySize(50)
		iconSize = self.minSize(35)
		xOffset = self.xSize(15)
		xYieldsOffset = self.xSize(30)
		yYieldsOffset = self.ySize(25)

		mostNeededYields = neededYields[-numMostNeededYield:]
		szMostNeededYieldsText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_MOST_NEEDED_YIELDS", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabelAt(self.getNextWidgetName(), "EuropeNeeds", u"<font=3>" + szMostNeededYieldsText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPos, yPos, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
	
		mostNeededYields.reverse()
		for iLoop in range(len(mostNeededYields)):
			mostNeededYield = mostNeededYields[iLoop][1]
			screen.setImageButtonAt(self.getNextWidgetName(), "EuropeNeeds", gc.getYieldInfo(mostNeededYield).getIcon(), xPos + iLoop * (iconSize + xOffset) + xYieldsOffset, yPos + yYieldsOffset, iconSize, iconSize, WidgetTypes.WIDGET_HELP_YIELD, mostNeededYield, -1)

		yPos += self.ySize(100)
		lessNeededYields = neededYields[:numLessNeededYield]
		szLessNeededYieldsText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_LESS_NEEDED_YIELDS", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabelAt(self.getNextWidgetName(), "EuropeNeeds", u"<font=3>" + szLessNeededYieldsText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPos, yPos, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
	
		for iLoop in range(len(lessNeededYields)):
			lessNeededYield = lessNeededYields[iLoop][1]
			screen.setImageButtonAt(self.getNextWidgetName(), "EuropeNeeds", gc.getYieldInfo(lessNeededYield).getIcon(), xPos + iLoop * (iconSize + xOffset) + xYieldsOffset, yPos + yYieldsOffset, iconSize, iconSize, WidgetTypes.WIDGET_HELP_YIELD, lessNeededYield, -1)

	def agreements(self):
		screen = self.getScreen()
		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)

		iTempAgreement = 1
		if self.iAgreementMode == 1:
			xSize = self.X_SIZE_CONTRACT_BOOK/10
			ySize = self.Y_SIZE_CONTRACT_BOOK/10
			iSpacingY = 10
			(loopAgreement, iter) = pPlayer.firstAgreement()
			while(loopAgreement):
				#Only European agreements
				if loopAgreement.getDestinationCity().iID == -1 :
					if self.iCurrentAgreement == iTempAgreement:
						self.printAgreement(loopAgreement)
						screen.setImageButtonAt(self.getNextWidgetName(), "AgreementsList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_CONTRAT_COMMERCIAL_EUROPE_ON").getPath(), 0, (iTempAgreement-1)*(ySize+iSpacingY)+15, xSize, ySize, WidgetTypes.WIDGET_GENERAL, -1, -1)
					else:
						screen.setImageButtonAt(self.getNextWidgetName(), "AgreementsList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_CONTRAT_COMMERCIAL_EUROPE_OFF").getPath(), 0, (iTempAgreement-1)*(ySize+iSpacingY)+15, xSize, ySize, WidgetTypes.WIDGET_GENERAL, self.CHANGE_CURRENT_AGREEMENT, iTempAgreement)
					iTempAgreement += 1
				(loopAgreement, iter) = pPlayer.nextAgreement(iter)
		while iTempAgreement < 6:
			screen.setImageButtonAt(self.getNextWidgetName(), "AgreementsList", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_CONTRAT_COMMERCIAL_EUROPE_OFF").getPath(), 0, (iTempAgreement-1)*(ySize+iSpacingY)+15, xSize, ySize, WidgetTypes.WIDGET_GENERAL, -1, -1)
			iTempAgreement += 1
	
	def printAgreement(self, pAgreement):
		screen = self.getScreen()
		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		
		xPos = self.X_POS_CONTRACT_BOOK + self.X_SIZE_CONTRACT_BOOK*10/100
		yPos = self.Y_POS_CONTRACT_BOOK + self.Y_SIZE_CONTRACT_BOOK*20/100
		yDecal = self.CARGO_ICON_SIZE * 9 /10
		iSize = self.CARGO_ICON_SIZE
		
		eYield = pAgreement.getExportYield()
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_MERCHANT_AGREEMENTS", (pAgreement.getMerchantName(), )), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=4>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_POS_CONTRACT_BOOK + self.X_SIZE_CONTRACT_BOOK/2, self.Y_POS_CONTRACT_BOOK + self.Y_SIZE_CONTRACT_BOOK/10, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setImageButton(self.getNextWidgetName(), gc.getCivilizationInfo(pPlayer.getCivilizationType()).getButton(), xPos, yPos - iSize/2, iSize*3/2, iSize*3/2, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szText = u" \t"
		szText += localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_MERCHANT_NAME", (pAgreement.getMerchantName(), )), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPos + iSize, yPos + iSize/4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		yPos += yDecal
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_MERCHANT_YIELD_OBJECTIF", (pAgreement.getOriginalAmount(eYield), gc.getYieldInfo(eYield).getChar(), )), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		szText += u" \t"
		szText += localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_MERCHANT_YIELD_QUANTITY_ACTUAL", (pAgreement.getActualAmount(eYield), gc.getYieldInfo(eYield).getChar(), )), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPos, yPos + iSize/4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		yPos += yDecal
		
		szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_MERCHANT_YIELD_PRICE", (pAgreement.getFixedPrice(), )), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		szText += u" \t"
		szText += localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_MERCHANT_PRIME", (pAgreement.getPrime(), )), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPos, yPos + iSize/4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		yPos += yDecal
		
		iTurnLeft = pAgreement.getTurnLeft()
		if iTurnLeft >= 0:
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_MERCHANT_TURN_REMAINING", (iTurnLeft, )), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		else:
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_MERCHANT_NO_TURN", (iTurnLeft, )), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPos, yPos + iSize/4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		yPos += yDecal
		
		if 1==1:#pAgreement.isAuto():
			szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_MERCHANT_TRANSPORT_AUTO", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		else:
			if pAgreement.getNumAssignedGroups() > 0:
				szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_MERCHANT_TRANSPORT_OK", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
			else:
				szText = localText.changeTextColor(localText.getText("TXT_KEY_EUROPE_MERCHANT_TRANSPORT_PB", ()), gc.getInfoTypeForString("COLOR_BROWN_TEXT"))
		screen.setLabel(self.getNextWidgetName(), "background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, xPos, yPos + iSize/4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
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

	def minSize(self, val):
		return min(self.xSize(val), self.ySize(val))

	def xSize(self, val):
		return val*self.XResolution/1024

	def ySize(self, val):
		return val*self.YResolution/768
