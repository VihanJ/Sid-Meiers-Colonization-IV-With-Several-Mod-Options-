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

class CvIncomeAndExpendituresRecord:

	def __init__(self):
		self.WIDGET_ID = "IncomeAndExpendituresRecordWidget"
		
		self.nWidgetCount = 0

		self.INCOME_EXPENDITURES_BONUS_HELP = 1
		self.INCOME_EXPENDITURES_MERCHANT_CREWS_HELP = 2
		self.INCOME_EXPENDITURES_MILITARY_CREWS_HELP = 3
		self.INCOME_EXPENDITURES_UNEMPLOYED_HELP = 4
		self.INCOME_EXPENDITURES_DEBT_HELP = 5
		self.INCOME_EXPENDITURES_INFORMATION_HELP = 6
		
	def getScreen(self):
		return CyGInterfaceScreen("incomeAndExpendituresRecord", CvScreenEnums.INCOME_AND_EXPENDITURES_RECORD)

	def interfaceScreen(self):
	
		screen = self.getScreen()
		if screen.isActive():
			return
		
		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		self.player = pPlayer
		
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.calculateSizesAndPositions()
		self.initColors()
		self.initTexts()
		
		screen.addDDSGFC("IncomeAndExpendituresRecordBackground", ArtFileMgr.getInterfaceArtInfo("INTERFACE_INCOME_AND_EXPENDITURES_RECORD").getPath(), self.X_POS_POPUP, self.Y_POS_POPUP, self.X_SIZE_POPUP, self.Y_SIZE_POPUP, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		self.PopupPanel = self.getNextWidgetName()
		screen.addPanel(self.PopupPanel , "", "", True, True, self.X_POS_POPUP, self.Y_POS_POPUP, self.X_SIZE_POPUP, self.Y_SIZE_POPUP, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.setImageButtonAt(self.getNextWidgetName(), self.PopupPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_ICON_SEAWAY_CLOSE").getPath(), self.X_SIZE_POPUP - self.SIZE_ICON - self.OFFSET_ICON, self.OFFSET_ICON, self.SIZE_ICON, self.SIZE_ICON, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)
		
		screen.addDDSGFCAt(self.getNextWidgetName(), self.PopupPanel, ArtFileMgr.getCivilizationArtInfo(gc.getCivilizationInfo(pPlayer.getCivilizationType()).getArtDefineTag()).getButton(), self.X_CIVILIZATION_FLAG, self.Y_CIVILIZATION_FLAG, self.CIVILIZATION_FLAG_SIZE, self.CIVILIZATION_FLAG_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

		self.displayTitles()

		if pPlayer.getNumCities() > 0:

			self.displayIncomeElements()

			self.displayExpenditureElements()

			self.displayTotalElements()

		else : 
			self.displayNoRecordMessage()

	def displayTitles(self):
		screen = self.getScreen()
		
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_TITLE, CvUtil.FONT_CENTER_JUSTIFY, self.X_INCOME_EXPENDITURES_TITLE, self.Y_INCOME_EXPENDITURES_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.INCOME_EXPENDITURES_INFORMATION_HELP, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_SUBTITLE, CvUtil.FONT_CENTER_JUSTIFY, self.X_INCOME_EXPENDITURES_SUBTITLE, self.Y_INCOME_EXPENDITURES_SUBTITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.INCOME_EXPENDITURES_INFORMATION_HELP, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_SUBTITLE_THEME, CvUtil.FONT_CENTER_JUSTIFY, self.X_INCOME_EXPENDITURES_SUBTITLE_THEME, self.Y_INCOME_EXPENDITURES_SUBTITLE_THEME, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.INCOME_EXPENDITURES_INFORMATION_HELP, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_COLONY_NUMBER, CvUtil.FONT_CENTER_JUSTIFY, self.X_INCOME_EXPENDITURES_COLONY_NUMBER, self.Y_INCOME_EXPENDITURES_COLONY_NUMBER, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.INCOME_EXPENDITURES_INFORMATION_HELP, -1)

	def displayIncomeElements(self):
		screen = self.getScreen()

		# Title
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_INCOME_TITLE, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_INCOME_TITLE, self.Y_INCOME_EXPENDITURES_INCOME_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Rows 
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_COLONISTS_INTO_COLONIES, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_COLONISTS_INTO_COLONIES, self.Y_INCOME_EXPENDITURES_COLONISTS_INTO_COLONIES, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_BONUS, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_BONUS, self.Y_INCOME_EXPENDITURES_BONUS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.INCOME_EXPENDITURES_BONUS_HELP, -1)
		
		# Subtotal
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_SUBTOTAL_INCOME, CvUtil.FONT_RIGHT_JUSTIFY, self.X_INCOME_EXPENDITURES_SUBTOTAL_INCOME, self.Y_INCOME_EXPENDITURES_SUBTOTAL_INCOME, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_POSITIVE_GOLD_PER_TURN, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_POSITIVE_GOLD_PER_TURN, self.Y_INCOME_EXPENDITURES_POSITIVE_GOLD_PER_TURN, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
	def displayExpenditureElements(self):
		screen = self.getScreen()

		# Title
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_EXPENDITURES_TITLE, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_EXPENDITURES_TITLE, self.Y_INCOME_EXPENDITURES_EXPENDITURES_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Rows
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_PIONEER, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_PIONEER, self.Y_INCOME_EXPENDITURES_PIONEER, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_AGRONOMIST, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_AGRONOMIST, self.Y_INCOME_EXPENDITURES_AGRONOMIST, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_SCOUT, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_SCOUT, self.Y_INCOME_EXPENDITURES_SCOUT, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_LAND_FORCES_INSIDE_COLONIES, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_LAND_FORCES_INSIDE_COLONIES, self.Y_INCOME_EXPENDITURES_LAND_FORCES_INSIDE_COLONIES, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_LAND_FORCES_OUTSIDE_COLONIES , CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_LAND_FORCES_OUTSIDE_COLONIES , self.Y_INCOME_EXPENDITURES_LAND_FORCES_OUTSIDE_COLONIES , 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_MERCHANT_CREWS, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_MERCHANT_CREWS, self.Y_INCOME_EXPENDITURES_MERCHANT_CREWS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.INCOME_EXPENDITURES_MERCHANT_CREWS_HELP, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_MILITARY_CREWS, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_MILITARY_CREWS, self.Y_INCOME_EXPENDITURES_MILITARY_CREWS, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.INCOME_EXPENDITURES_MILITARY_CREWS_HELP, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_UNEMPLOYED, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_UNEMPLOYED, self.Y_INCOME_EXPENDITURES_UNEMPLOYED, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.INCOME_EXPENDITURES_UNEMPLOYED_HELP, -1)
		
		# Subtotal
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_SUBTOTAL_EXPENDITURES, CvUtil.FONT_RIGHT_JUSTIFY, self.X_INCOME_EXPENDITURES_SUBTOTAL_EXPENDITURES, self.Y_INCOME_EXPENDITURES_SUBTOTAL_EXPENDITURES, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_GOLD_PER_TURN, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_GOLD_PER_TURN, self.Y_INCOME_EXPENDITURES_GOLD_PER_TURN, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def displayTotalElements(self):
		screen = self.getScreen()

		# Total
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_TOTAL_INCOME_EXPENDITURES, CvUtil.FONT_RIGHT_JUSTIFY, self.X_INCOME_EXPENDITURES_TOTAL_INCOME_EXPENDITURES, self.Y_INCOME_EXPENDITURES_TOTAL_INCOME_EXPENDITURES, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_TOTAL_GOLD, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_TOTAL_GOLD, self.Y_INCOME_EXPENDITURES_TOTAL_GOLD, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Debt
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_DEBT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_INCOME_EXPENDITURES_DEBT, self.Y_INCOME_EXPENDITURES_DEBT, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.INCOME_EXPENDITURES_DEBT_HELP, -1)
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_DEBT_AMOUNT, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_DEBT_AMOUNT, self.Y_INCOME_EXPENDITURES_DEBT_AMOUNT, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Help screen
		screen.setLabelAt(self.getNextWidgetName(), self.PopupPanel, self.INCOME_EXPENDITURES_SCREEN_HELP, CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME_EXPENDITURES_SCREEN_HELP, self.Y_INCOME_EXPENDITURES_SCREEN_HELP, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def displayNoRecordMessage(self):

		screen = self.getScreen()
		
		screen.attachMultilineTextAt(self.PopupPanel, self.getNextWidgetName(), self.INCOME_EXPENDITURES_WITHOUT_COLONIES, self.X_INCOME_EXPENDITURES_WITHOUT_COLONIES, self.Y_INCOME_EXPENDITURES_WITHOUT_COLONIES, self.W_INCOME_EXPENDITURES_WITHOUT_COLONIES, self.H_INCOME_EXPENDITURES_WITHOUT_COLONIES, WidgetTypes.WIDGET_GENERAL, -1, -1,  CvUtil.FONT_CENTER_JUSTIFY)

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

	def handleInput(self, inputClass):
		'Calls function mapped in '
		
		screen = self.getScreen()
		
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):
				return 1
		return 0

	def update(self, fDelta):
		screen = self.getScreen()

	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList
		
		if eWidgetType == WidgetTypes.WIDGET_GENERAL:

			if iData1 == self.INCOME_EXPENDITURES_BONUS_HELP:
				return localText.getText("TXT_INCOME_EXPENDITURES_BONUS_HELP", ())

			if iData1 == self.INCOME_EXPENDITURES_MERCHANT_CREWS_HELP:
				return localText.getText("TXT_INCOME_EXPENDITURES_MERCHANT_CREWS_HELP", ())

			if iData1 == self.INCOME_EXPENDITURES_MILITARY_CREWS_HELP:
				return localText.getText("TXT_INCOME_EXPENDITURES_MILITARY_CREWS_HELP", ())

			if iData1 == self.INCOME_EXPENDITURES_UNEMPLOYED_HELP:
				return localText.getText("TXT_INCOME_EXPENDITURES_UNEMPLOYED_HELP", ())

			if iData1 == self.INCOME_EXPENDITURES_DEBT_HELP:
				return localText.getText("TXT_INCOME_EXPENDITURES_DEBT_HELP", ())

			if iData1 == self.INCOME_EXPENDITURES_INFORMATION_HELP:
				return localText.getText("TXT_INCOME_EXPENDITURES_INFORMATION", ())
				
		return u""

	def initColors(self):
		self.TitleColor = gc.getInfoTypeForString("COLOR_INCOME_AND_EXPENDITURES_TITLE")
		self.RowColor = gc.getInfoTypeForString("COLOR_INCOME_AND_EXPENDITURES_RAW")
		self.GreenColor = gc.getInfoTypeForString("COLOR_INCOME_AND_EXPENDITURES_GREEN")
		self.RedColor = gc.getInfoTypeForString("COLOR_INCOME_AND_EXPENDITURES_RED")

	def initTexts(self):
		pPlayer = self.player 

		# Titles
		self.INCOME_EXPENDITURES_TITLE = self.setTitleColor(u"<font=4b>" + localText.getText("TXT_INCOME_EXPENDITURES_TITLE", ()).upper() + u"</font>")

		self.INCOME_EXPENDITURES_SUBTITLE = self.setTitleColor(u"<font=3b>" + localText.getText("TXT_INCOME_EXPENDITURES_SUBTITLE", ()).upper() + u"</font>")

		self.INCOME_EXPENDITURES_SUBTITLE_THEME = self.setTitleColor(u"<font=3b>" + localText.getText("TXT_INCOME_EXPENDITURES_SUBTITLE_THEME", ()).upper() + u"</font>")

		numColonies = pPlayer.getNumCities()
		self.INCOME_EXPENDITURES_COLONY_NUMBER = self.setTitleColor(u"<font=2>" + localText.getText("TXT_INCOME_EXPENDITURES_COLONY_NUMBER", (numColonies, )) + u"</font>")

		# Income
		self.INCOME_EXPENDITURES_INCOME_TITLE = self.setTitleColor(u"<font=4b>" + localText.getText("TXT_INCOME_EXPENDITURES_INCOME", ()) + u"</font>")

		numColonist = pPlayer.getColonistIntoColoniesAmount()
		incomeByColonist = gc.getHandicapInfo(pPlayer.getHandicapType()).getIncomeByPopulation()
		incomeForColonist = pPlayer.getColonistsIncome()
		self.INCOME_EXPENDITURES_COLONISTS_INTO_COLONIES = self.setRowColor(u"<font=2>" + localText.getText("TXT_INCOME_EXPENDITURES_COLONISTS_INTO_COLONIES", (numColonist, incomeByColonist, incomeForColonist, )) + u"</font>")

		workImprovementPercent = pPlayer.getWorkImprovementPercent()
		incomeForStatemen = pPlayer.getStatemenIncomeIncrease()
		self.INCOME_EXPENDITURES_BONUS = self.setRowColor(u"<font=2>" + localText.getText("TXT_INCOME_EXPENDITURES_BONUS", (workImprovementPercent, incomeForStatemen, )) + u"</font>")

		# Income subtotal
		self.INCOME_EXPENDITURES_SUBTOTAL_INCOME = self.setTitleColor(u"<font=3b>" + localText.getText("TXT_INCOME_EXPENDITURES_SUBTOTAL_INCOME", ()) + u"</font>")

		totalIncome = pPlayer.getTotalIncome()
		self.INCOME_EXPENDITURES_POSITIVE_GOLD_PER_TURN = self.setGreenColor(u"<font=3b>" + localText.getText("TXT_INCOME_EXPENDITURES_POSITIVE_GOLD_PER_TURN", (totalIncome, )) + u"</font>")

		# Expenditures
		self.INCOME_EXPENDITURES_EXPENDITURES_TITLE = self.setTitleColor(u"<font=4b>" + localText.getText("TXT_INCOME_EXPENDITURES_EXPENDITURES_TITLE", ()) + u"</font>")

		numCurrentUnit = pPlayer.getPioneerAmount()
		incomeByCurrentUnit = gc.getEXPENDITURE_BY_PIONEER()
		incomeForCurrentUnit = pPlayer.getPioneerExpenditure()
		self.INCOME_EXPENDITURES_PIONEER = self.setRowColor(u"<font=2>" + localText.getText("TXT_INCOME_EXPENDITURES_PIONEER", (numCurrentUnit, incomeByCurrentUnit, incomeForCurrentUnit, )) + u"</font>")

		numCurrentUnit = pPlayer.getAgronomistAmount()
		incomeByCurrentUnit = gc.getEXPENDITURE_BY_AGRONOMIST()
		incomeForCurrentUnit = pPlayer.getAgronomistExpenditure()
		self.INCOME_EXPENDITURES_AGRONOMIST = self.setRowColor(u"<font=2>" + localText.getText("TXT_INCOME_EXPENDITURES_AGRONOMIST", (numCurrentUnit, incomeByCurrentUnit, incomeForCurrentUnit, )) + u"</font>")

		numCurrentUnit = pPlayer.getScoutAmount()
		incomeByCurrentUnit = gc.getEXPENDITURE_BY_SCOUT()
		incomeForCurrentUnit = pPlayer.getScoutExpenditure()
		self.INCOME_EXPENDITURES_SCOUT = self.setRowColor(u"<font=2>" + localText.getText("TXT_INCOME_EXPENDITURES_SCOUT", (numCurrentUnit, incomeByCurrentUnit, incomeForCurrentUnit, )) + u"</font>")

		numCurrentUnit = pPlayer.getLandForceInsideColoniesAmount()
		incomeByCurrentUnit = gc.getEXPENDITURE_BY_LAND_FORCE_INSIDE_COLONIES()
		incomeForCurrentUnit = pPlayer.getLandForceInsideColoniesExpenditure()
		self.INCOME_EXPENDITURES_LAND_FORCES_INSIDE_COLONIES = self.setRowColor(u"<font=2>" + localText.getText("TXT_INCOME_EXPENDITURES_LAND_FORCES_INSIDE_COLONIES", (numCurrentUnit, incomeByCurrentUnit, incomeForCurrentUnit, )) + u"</font>")

		numCurrentUnit = pPlayer.getLandForceOutsideColoniesAmount()
		incomeByCurrentUnit = gc.getEXPENDITURE_BY_LAND_FORCE_OUTSIDE_COLONIES()
		incomeForCurrentUnit = pPlayer.getLandForceOutsideColoniesExpenditure()
		self.INCOME_EXPENDITURES_LAND_FORCES_OUTSIDE_COLONIES  = self.setRowColor(u"<font=2>" + localText.getText("TXT_INCOME_EXPENDITURES_LAND_FORCES_OUTSIDE_COLONIES", (numCurrentUnit, incomeByCurrentUnit, incomeForCurrentUnit, )) + u"</font>")

		numCurrentUnit = pPlayer.getMerchantShipAmount()
		incomeByCurrentUnit = gc.getEXPENDITURE_BY_MERCHANT_SHIP()
		incomeForCurrentUnit = pPlayer.getMerchantShipExpenditure()
		self.INCOME_EXPENDITURES_MERCHANT_CREWS = self.setRowColor(u"<font=2>" + localText.getText("TXT_INCOME_EXPENDITURES_MERCHANT_CREWS", (numCurrentUnit, incomeByCurrentUnit, incomeForCurrentUnit, )) + u"</font>")

		numCurrentUnit = pPlayer.getMilitaryShipAmount()
		incomeByCurrentUnit = gc.getEXPENDITURE_BY_MILITARY_SHIP()
		incomeForCurrentUnit = pPlayer.getMilitaryShipExpenditure()
		self.INCOME_EXPENDITURES_MILITARY_CREWS = self.setRowColor(u"<font=2>" + localText.getText("TXT_INCOME_EXPENDITURES_MILITARY_CREWS", (numCurrentUnit, incomeByCurrentUnit, incomeForCurrentUnit, )) + u"</font>")

		numCurrentUnit = pPlayer.getUnemployedAmount()
		incomeByCurrentUnit = gc.getEXPENDITURE_BY_UNEMPLOYED()
		incomeForCurrentUnit = pPlayer.getUnemployedExpenditure()
		self.INCOME_EXPENDITURES_UNEMPLOYED = self.setRowColor(u"<font=2>" + localText.getText("TXT_INCOME_EXPENDITURES_UNEMPLOYED", (numCurrentUnit, incomeByCurrentUnit, incomeForCurrentUnit, )) + u"</font>")

		# Expenditure subtotal
		self.INCOME_EXPENDITURES_SUBTOTAL_EXPENDITURES = self.setTitleColor(u"<font=3b>" + localText.getText("TXT_INCOME_EXPENDITURES_SUBTOTAL_EXPENDITURES", ()) + u"</font>")

		totalExpenditures = -pPlayer.getTotalExpenditures()
		self.INCOME_EXPENDITURES_GOLD_PER_TURN = self.setRedColor(u"<font=3b>" + localText.getText("TXT_INCOME_EXPENDITURES_GOLD_PER_TURN", (totalExpenditures, )) + u"</font>")
		
		# Total
		self.INCOME_EXPENDITURES_TOTAL_INCOME_EXPENDITURES = self.setTitleColor(u"<font=4b>" + localText.getText("TXT_INCOME_EXPENDITURES_TOTAL_INCOME_EXPENDITURES", ()) + u"</font>")

		totalIncomeAndExpenditures = pPlayer.getIncomeAndExpendituresRecord()
		if totalIncomeAndExpenditures >= 0:
			self.INCOME_EXPENDITURES_TOTAL_GOLD = self.setGreenColor(u"<font=4>" + localText.getText("TXT_INCOME_EXPENDITURES_POSITIVE_GOLD_PER_TURN", (totalIncomeAndExpenditures, )) + u"</font>")
		else:
			self.INCOME_EXPENDITURES_TOTAL_GOLD = self.setRedColor(u"<font=4>" + localText.getText("TXT_INCOME_EXPENDITURES_GOLD_PER_TURN", (totalIncomeAndExpenditures, )) + u"</font>")

		# Debt 
		self.INCOME_EXPENDITURES_DEBT = self.setTitleColor(u"<font=3b>" + localText.getText("TXT_INCOME_EXPENDITURES_DEBT", ()) + u"</font>")

		europeDebt = -pPlayer.getEuropeLoan()
		self.INCOME_EXPENDITURES_DEBT_AMOUNT = self.setRedColor(u"<font=3B>" + localText.getText("TXT_INCOME_EXPENDITURES_DEBT_AMOUNT", (europeDebt, )) + u"</font>")

		# Screen help

		self.INCOME_EXPENDITURES_SCREEN_HELP = u"<font=2>" + localText.getText("TXT_INCOME_EXPENDITURES_SCREEN_HELP", ()) + u"</font>"

		self.INCOME_EXPENDITURES_WITHOUT_COLONIES = self.setTitleColor(u"<font=4>" + localText.getText("TXT_INCOME_EXPENDITURES_NO_COLONY", ()) + u"</font>")

		self.INCOME_EXPENDITURES_INFORMATION = self.setTitleColor(u"<font=4>" + localText.getText("TXT_INCOME_EXPENDITURES_INFORMATION", ()) + u"</font>")
		
	def calculateSizesAndPositions(self):
		self.X_SCREEN = 0
		self.Y_SCREEN = 0

		screen = self.getScreen()

		self.XResolution = screen.getXResolution()
		self.YResolution = screen.getYResolution()

		self.W_SCREEN = screen.getXResolution()
		self.H_SCREEN = screen.getYResolution()

		self.X_SIZE_POPUP = self.xSize(843)
		self.Y_SIZE_POPUP = self.ySize(512)
		self.X_POS_POPUP = (self.XResolution - self.X_SIZE_POPUP) / 2
		self.Y_POS_POPUP = self.ySize(64)
		self.X_OFFSET_POPUP = self.xSize(40)


		self.CIVILIZATION_FLAG_SIZE = self.minSize(60)
		self.CIVILIZATION_FLAG_OFFSET = self.minSize(60)
		self.X_CIVILIZATION_FLAG = self.X_SIZE_POPUP - self.CIVILIZATION_FLAG_SIZE - self.CIVILIZATION_FLAG_OFFSET
		self.Y_CIVILIZATION_FLAG = self.CIVILIZATION_FLAG_OFFSET
		self.SIZE_ICON = self.minSize(40)
		self.OFFSET_ICON = self.minSize(10)

		# Titles
		
		self.X_INCOME_EXPENDITURES_TITLE = self.X_SIZE_POPUP / 2
		self.Y_INCOME_EXPENDITURES_TITLE = self.ySize(70)
		
		self.X_INCOME_EXPENDITURES_SUBTITLE = self.X_INCOME_EXPENDITURES_TITLE
		self.Y_INCOME_EXPENDITURES_SUBTITLE = self.Y_INCOME_EXPENDITURES_TITLE + self.ySize(20)
		
		self.X_INCOME_EXPENDITURES_SUBTITLE_THEME = self.X_INCOME_EXPENDITURES_SUBTITLE
		self.Y_INCOME_EXPENDITURES_SUBTITLE_THEME = self.Y_INCOME_EXPENDITURES_SUBTITLE + self.ySize(20)
		
		self.X_INCOME_EXPENDITURES_COLONY_NUMBER = self.X_INCOME_EXPENDITURES_SUBTITLE_THEME
		self.Y_INCOME_EXPENDITURES_COLONY_NUMBER = self.Y_INCOME_EXPENDITURES_SUBTITLE_THEME + self.ySize(20)


		self.X_OFFSET_ROW = self.ySize(30)
		self.Y_OFFSET_ROW = self.ySize(20)
		self.Y_OFFSET_TITLE = self.ySize(10)

		self.X_SUBTOTAL_OFFSET = self.X_OFFSET_ROW + self.xSize(130)
		
		#
		# Income
		#

		# Title

		self.X_INCOME_EXPENDITURES_INCOME_TITLE = self.X_OFFSET_POPUP
		self.Y_INCOME_EXPENDITURES_INCOME_TITLE = self.ySize(150)

		# Rows

		self.X_INCOME_EXPENDITURES_COLONISTS_INTO_COLONIES = self.X_OFFSET_POPUP + self.X_OFFSET_ROW
		self.Y_INCOME_EXPENDITURES_COLONISTS_INTO_COLONIES = self.Y_INCOME_EXPENDITURES_INCOME_TITLE + self.Y_OFFSET_ROW + self.Y_OFFSET_TITLE

		self.X_INCOME_EXPENDITURES_BONUS = self.X_OFFSET_POPUP + self.X_OFFSET_ROW
		self.Y_INCOME_EXPENDITURES_BONUS = self.Y_INCOME_EXPENDITURES_COLONISTS_INTO_COLONIES + self.Y_OFFSET_ROW

		# Subtotal

		self.X_INCOME_EXPENDITURES_SUBTOTAL_INCOME = self.X_SIZE_POPUP - self.X_SUBTOTAL_OFFSET
		self.Y_INCOME_EXPENDITURES_SUBTOTAL_INCOME = self.Y_INCOME_EXPENDITURES_BONUS + self.Y_OFFSET_ROW

		self.X_INCOME_EXPENDITURES_POSITIVE_GOLD_PER_TURN = self.X_SIZE_POPUP - self.X_SUBTOTAL_OFFSET
		self.Y_INCOME_EXPENDITURES_POSITIVE_GOLD_PER_TURN = self.Y_INCOME_EXPENDITURES_SUBTOTAL_INCOME 

		#
		# Expenditures
		#

		# Title

		self.X_INCOME_EXPENDITURES_EXPENDITURES_TITLE = self.X_OFFSET_POPUP
		self.Y_INCOME_EXPENDITURES_EXPENDITURES_TITLE = self.Y_INCOME_EXPENDITURES_INCOME_TITLE + self.ySize(80)

		# Rows

		self.X_INCOME_EXPENDITURES_PIONEER = self.X_OFFSET_POPUP + self.X_OFFSET_ROW
		self.Y_INCOME_EXPENDITURES_PIONEER = self.Y_INCOME_EXPENDITURES_EXPENDITURES_TITLE + self.Y_OFFSET_ROW + self.Y_OFFSET_TITLE

		self.X_INCOME_EXPENDITURES_AGRONOMIST = self.X_OFFSET_POPUP + self.X_OFFSET_ROW
		self.Y_INCOME_EXPENDITURES_AGRONOMIST = self.Y_INCOME_EXPENDITURES_PIONEER + self.Y_OFFSET_ROW

		self.X_INCOME_EXPENDITURES_SCOUT = self.X_OFFSET_POPUP + self.X_OFFSET_ROW
		self.Y_INCOME_EXPENDITURES_SCOUT = self.Y_INCOME_EXPENDITURES_AGRONOMIST + self.Y_OFFSET_ROW

		self.X_INCOME_EXPENDITURES_LAND_FORCES_INSIDE_COLONIES = self.X_OFFSET_POPUP + self.X_OFFSET_ROW
		self.Y_INCOME_EXPENDITURES_LAND_FORCES_INSIDE_COLONIES = self.Y_INCOME_EXPENDITURES_SCOUT + self.Y_OFFSET_ROW

		self.X_INCOME_EXPENDITURES_LAND_FORCES_OUTSIDE_COLONIES = self.X_OFFSET_POPUP + self.X_OFFSET_ROW
		self.Y_INCOME_EXPENDITURES_LAND_FORCES_OUTSIDE_COLONIES = self.Y_INCOME_EXPENDITURES_LAND_FORCES_INSIDE_COLONIES + self.Y_OFFSET_ROW

		self.X_INCOME_EXPENDITURES_MERCHANT_CREWS = self.X_OFFSET_POPUP + self.X_OFFSET_ROW
		self.Y_INCOME_EXPENDITURES_MERCHANT_CREWS = self.Y_INCOME_EXPENDITURES_LAND_FORCES_OUTSIDE_COLONIES + self.Y_OFFSET_ROW

		self.X_INCOME_EXPENDITURES_MILITARY_CREWS = self.X_OFFSET_POPUP + self.X_OFFSET_ROW
		self.Y_INCOME_EXPENDITURES_MILITARY_CREWS = self.Y_INCOME_EXPENDITURES_MERCHANT_CREWS + self.Y_OFFSET_ROW

		self.X_INCOME_EXPENDITURES_UNEMPLOYED = self.X_OFFSET_POPUP + self.X_OFFSET_ROW
		self.Y_INCOME_EXPENDITURES_UNEMPLOYED = self.Y_INCOME_EXPENDITURES_MILITARY_CREWS + self.Y_OFFSET_ROW

		# Subtotal

		self.X_INCOME_EXPENDITURES_SUBTOTAL_EXPENDITURES = self.X_SIZE_POPUP - self.X_SUBTOTAL_OFFSET
		self.Y_INCOME_EXPENDITURES_SUBTOTAL_EXPENDITURES = self.Y_INCOME_EXPENDITURES_UNEMPLOYED + self.Y_OFFSET_ROW

		self.X_INCOME_EXPENDITURES_GOLD_PER_TURN = self.X_SIZE_POPUP - self.X_SUBTOTAL_OFFSET
		self.Y_INCOME_EXPENDITURES_GOLD_PER_TURN = self.Y_INCOME_EXPENDITURES_SUBTOTAL_EXPENDITURES 

		# Total

		self.X_INCOME_EXPENDITURES_TOTAL_INCOME_EXPENDITURES = self.X_SIZE_POPUP - self.X_SUBTOTAL_OFFSET
		self.Y_INCOME_EXPENDITURES_TOTAL_INCOME_EXPENDITURES = self.Y_INCOME_EXPENDITURES_GOLD_PER_TURN  + self.Y_OFFSET_ROW

		self.X_INCOME_EXPENDITURES_TOTAL_GOLD = self.X_SIZE_POPUP - self.X_SUBTOTAL_OFFSET
		self.Y_INCOME_EXPENDITURES_TOTAL_GOLD = self.Y_INCOME_EXPENDITURES_TOTAL_INCOME_EXPENDITURES 

		# Debt

		self.X_INCOME_EXPENDITURES_DEBT = self.X_OFFSET_POPUP + self.xSize(340)
		self.Y_INCOME_EXPENDITURES_DEBT = self.Y_INCOME_EXPENDITURES_TOTAL_GOLD + self.Y_OFFSET_TITLE * 2 

		self.X_INCOME_EXPENDITURES_DEBT_AMOUNT = self.X_INCOME_EXPENDITURES_DEBT
		self.Y_INCOME_EXPENDITURES_DEBT_AMOUNT = self.Y_INCOME_EXPENDITURES_DEBT

		# Screen Help 

		self.X_INCOME_EXPENDITURES_SCREEN_HELP = self.X_OFFSET_POPUP
		self.Y_INCOME_EXPENDITURES_SCREEN_HELP = self.Y_SIZE_POPUP - self.Y_OFFSET_ROW

		self.W_INCOME_EXPENDITURES_WITHOUT_COLONIES = self.X_SIZE_POPUP / 2
		self.H_INCOME_EXPENDITURES_WITHOUT_COLONIES = self.Y_SIZE_POPUP / 2
		self.X_INCOME_EXPENDITURES_WITHOUT_COLONIES = self.X_SIZE_POPUP / 2 - self.W_INCOME_EXPENDITURES_WITHOUT_COLONIES / 2
		self.Y_INCOME_EXPENDITURES_WITHOUT_COLONIES = self.ySize(200)
		

	def minSize(self, val):
		return min(self.xSize(val), self.ySize(val))

	def xSize(self, val):
		return val*self.XResolution/1024

	def ySize(self, val):
		return val*self.YResolution/768
	
	def setTitleColor(self, szText):
		return localText.changeTextColor(szText, self.TitleColor)

	def setRowColor(self, szText):
		return localText.changeTextColor(szText, self.RowColor)

	def setGreenColor(self, szText):
		return localText.changeTextColor(szText, self.GreenColor)

	def setRedColor(self, szText):
		return localText.changeTextColor(szText, self.RedColor)
	