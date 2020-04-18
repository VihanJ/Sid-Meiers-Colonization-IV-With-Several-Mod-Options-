## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

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

class CvNewEras:

	def __init__(self):
		self.WIDGET_ID = "NewErasScreenWidget"

		self.nWidgetCount = 0

		self.ERA_DROP_DOWN = "EraDropDown"
		self.CIV_DROP_DOWN = "CivDropDown"

		self.COLONIES_REQUIREMENT = 1
		self.REBELS_REQUIREMENT = 2
		self.MIN_TURN_REQUIREMENT = 3
		self.MIN_GOLD_REQUIREMENT = 4
		self.RAW_MATERIALS_REQUIREMENT = 5
		self.LAND_DISCOVERED_REQUIREMENT = 6
		self.RELIGIOUS_INFLUENCE_REQUIREMENT = 7
		self.DEFENDER_BY_COLONY_REQUIREMENT = 8
		self.CITIZEN_BY_COLONY_REQUIREMENT = 9

		self.ERA_REQUIREMENT = 1

	def getScreen(self):
		return CyGInterfaceScreen("CvNewEras", CvScreenEnums.NEW_ERAS_SCREEN)

	def initText(self):

		###### TEXT ######
		self.SCREEN_TITLE = u"<font=4b>" + localText.getText("TXT_KEY_NEW_ERAS_SCREEN", ()).upper() + u"</font>"
		self.SCREEN_EXIT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"

	def interfaceScreen(self):
		'Use a popup to display the opening text'
		if (CyGame().isPitbossHost()):
			return

		pPlayer = gc.getPlayer(CyGame().getActivePlayer())
		self.pPlayer  = pPlayer

		screen = self.getScreen()
		if screen.isActive():
			return
	
		screen = self.getScreen()

		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		
		# Set the background and exit button, and show the screen
		self.calculateSizesAndPositions()

		self.initText()

		self.EXIT_TEXT = localText.getText("TXT_KEY_SCREEN_CONTINUE", ())

		# Create screen		
		screen.addDDSGFC("DemographicsScreenBackground", ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.XResolution, self.YResolution,  WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("TopPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TITLE").getPath(), 0, 0, self.XResolution, 55, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC("BottomPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TAB_OFF").getPath(), 0, self.YResolution - 55, self.XResolution, 55, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.setDimensions(0, 0, self.XResolution, self.YResolution)
		screen.showWindowBackground(False)
		

		self.SCREEN_TITLE = localText.changeTextColor(self.SCREEN_TITLE, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
		screen.setText("TitleOfScreen", "Background", self.SCREEN_TITLE, CvUtil.FONT_CENTER_JUSTIFY, self.XResolution / 2, 4, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText( "NewErasScreenExit", "Background", self.SCREEN_EXIT, CvUtil.FONT_RIGHT_JUSTIFY, self.XResolution - 30, self.YResolution - 36, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		
		screen.addPanel("DescriptionTextsBackground", "", "", True, True, self.X_ERA_DETAILS_START, self.Y_ERA_DETAILS_START, self.X_ERA_DETAILS_SIZE, self.Y_ERA_DETAILS_SIZE, PanelStyles.PANEL_STYLE_BLUE50, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addScrollPanel("DescriptionTexts", u"", self.X_ERA_DETAILS_START, self.Y_ERA_DETAILS_START + self.Y_ERA_DETAILS_DESC_SIZE, self.X_ERA_DETAILS_SIZE, self.Y_ERA_DETAILS_SIZE - self.Y_ERA_DETAILS_DESC_SIZE, PanelStyles.PANEL_STYLE_MAIN, false, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		debugMode = CyGame().isDebugMode()
		shouldDisplay = debugMode or CyGame().getWinner() != TeamTypes.NO_TEAM

		iCount = 0
		for j in range(gc.getMAX_PLAYERS()):
			loopPlayer = gc.getPlayer(j)
			if shouldDisplay:
				if loopPlayer.isAlive() and not loopPlayer.isEurope() and not loopPlayer.isNative():
					iCount += 1
			elif (loopPlayer.isAlive() and loopPlayer.getTeam() == pPlayer.getTeam()):
				iCount += 1
		if iCount > 1:
			screen.addDropDownBoxGFC(self.CIV_DROP_DOWN, self.XResolution - 2* 220, 3, 200, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.SMALL_FONT )
			screen.setActivation(self.CIV_DROP_DOWN, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )
			screen.addPullDownString(self.CIV_DROP_DOWN, pPlayer.getName(), pPlayer.getID(), pPlayer.getID(), False)
			for j in range(gc.getMAX_PLAYERS()):
				loopPlayer = gc.getPlayer(j)
				if shouldDisplay:
					if (loopPlayer.isAlive() and loopPlayer.getID() != pPlayer.getID() and not loopPlayer.isEurope() and not loopPlayer.isNative()):
						screen.addPullDownString(self.CIV_DROP_DOWN, loopPlayer.getName(), j, j, False )
				elif (loopPlayer.isAlive() and loopPlayer.getID() != pPlayer.getID() and loopPlayer.getTeam() == pPlayer.getTeam()):
					screen.addPullDownString(self.CIV_DROP_DOWN, loopPlayer.getName(), j, j, False)
		else:
			screen.hide(self.CIV_DROP_DOWN)

		self.drawContents();
		

	def drawContents(self):
		screen = self.getScreen()

		player = self.pPlayer

		self.deleteAllWidgets()

		debugMode = CyGame().isDebugMode()
		shouldDisplay = debugMode or CyGame().getWinner() != TeamTypes.NO_TEAM
	
		#Debug PullDown
		if shouldDisplay:
			screen.addDropDownBoxGFC( self.ERA_DROP_DOWN, self.XResolution - 220, 3, 200, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.SMALL_FONT )
			screen.setActivation( self.ERA_DROP_DOWN, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )
			iNewEra = player.getNewEra()
			for j in range(4):
				szEra = u"Era %d" %(j)
				screen.addPullDownString( self.ERA_DROP_DOWN, szEra, j, j, j == iNewEra )
		else:
			screen.hide( self.ERA_DROP_DOWN )

		screen.setText(self.getNextWidgetName(), "Background", u"<font=3b>" + localText.getText("TXT_KEY_NEW_ERAS_SCREEN_CURRENT_ERA", (self.getNextNewEra(),)) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 20, 6, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		
		self.displayErasChanges()
		self.displayTopErasRequirements()
		self.displayBottomErasRequirements()

	def displayErasChanges(self):
		screen = self.getScreen()
		player = self.pPlayer

		
		iNextEra = self.getNextNewEra()
		kNewEra = gc.getNewEraInfo(iNextEra)
		if not kNewEra:
			return

		szText = u"<font=2b>" + localText.getText("TXT_KEY_NEW_ERAS_SCREEN_NEW_DESC_TITLE", ( )) + u"</font>\n"
		
		szText += localText.getText("TXT_KEY_ONLY_STRING", (kNewEra.getStartTextKey(), ))

		screen.addMultilineText(self.getNextWidgetName(), szText, self.X_ERA_DETAILS_START + self.X_ERA_DETAILS_DESC_MARGIN, self.Y_ERA_DETAILS_START + self.X_ERA_DETAILS_MARGIN, self.X_ERA_DETAILS_SIZE - 2*self.X_ERA_DETAILS_DESC_MARGIN, self.Y_ERA_DETAILS_DESC_SIZE - 2*self.X_ERA_DETAILS_MARGIN, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		yOffset = self.Y_ERA_DETAILS_SIZE - self.Y_ERA_DETAILS_DESC_SIZE - 15
		
		yOffset = self.displayYieldsWithPriceDecrease(yOffset)

		yOffset = self.displayNewProfession(yOffset)
		
		yOffset = self.displayNewBuildings(yOffset)

	def displayNewBuildings(self, yOffset):
		screen = self.getScreen()
		player = self.pPlayer
		iNextEra = self.getNextNewEra()
		kNewEra = gc.getNewEraInfo(iNextEra)
		if not kNewEra:
			return
		yStart = -30
		
		width = self.X_ERA_DETAILS_SIZE - 2*self.X_ERA_DETAILS_DESC_MARGIN
		iconSize = 30
		height = iconSize * 5 / 4

		NewBuildings = []
		for iI in range(gc.getNumBuildingClassInfos()):
			eLoopBuilding = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationBuildings(iI)
			if (eLoopBuilding != BuildingTypes.NO_BUILDING):
				iEraAllowed = gc.getBuildingInfo(eLoopBuilding).getEraAllowed()
				if (iEraAllowed == iNextEra):
					NewBuildings.append(eLoopBuilding)
		iCount = len(NewBuildings)
		iColumn = 13
		iRows = iCount/iColumn
		iXPos = 0
		iYPos = 0
		if iCount > 0:
			yOffset += yStart - iRows * height
			szText = u"<font=2b>" + localText.getText("TXT_KEY_NEW_ERAS_SCREEN_NEW_BUILDINGS_TITLE", (iCount, )) + u"</font>"
			screen.setLabelAt(self.getNextWidgetName(), "DescriptionTexts", u"<font=2>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 10,  yOffset - 10, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			
			for iBuilding in range(iCount):
				if iBuilding % iColumn == 0 and iBuilding > 0 :
					iYPos += height
					iXPos = 0
				eBuilding = NewBuildings[iBuilding]
				xBuilOffset = iXPos*height
				screen.addDDSGFCAt(self.getNextWidgetName(), "DescriptionTexts", gc.getBuildingInfo(eBuilding).getButton(), 10 + xBuilOffset, yOffset + iYPos, iconSize, iconSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eBuilding, -1 , False)
				iXPos += 1				

			yOffset += yStart
		return yOffset
					
	def displayNewProfession(self, yOffset):
		screen = self.getScreen()
		player = self.pPlayer

		iNextEra = self.getNextNewEra()

		yStart = -30
		width = self.X_ERA_DETAILS_SIZE - 2*self.X_ERA_DETAILS_DESC_MARGIN
		iconSize = 30
		height = iconSize * 5 / 4
		NewProfessions = []
		
		for iJ in range(gc.getNumProfessionInfos()):
			if gc.getCivilizationInfo(player.getCivilizationType()).isValidProfession(iJ):
				if gc.getProfessionInfo(iJ).getNewEra() == iNextEra:
					NewProfessions.append(iJ)
		iCount = len(NewProfessions) 
		if iCount > 0:
			szText = u"<font=2b>" + localText.getText("TXT_KEY_NEW_ERAS_SCREEN_NEW_PROFESSIONS_TITLE", (iCount, )) + u"</font>"
			screen.setLabelAt(self.getNextWidgetName(), "DescriptionTexts", u"<font=2>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 10, yStart + yOffset - 10, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			for iProfession in range(iCount):
				eProfession = NewProfessions[iProfession]
				szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
				xProfOffset = iProfession*height
				screen.addDDSGFCAt(self.getNextWidgetName(), "DescriptionTexts", gc.getProfessionInfo(eProfession).getButton(), 10 + xProfOffset, yStart + yOffset, iconSize, iconSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROFESSION, eProfession, -1 , False)
			yOffset += yStart - height
		return yOffset

	def displayYieldsWithPriceDecrease(self, yOffset):
		screen = self.getScreen()
		player = self.pPlayer

		iNextEra = self.getNextNewEra()

		yStart = - 30
		width = self.X_ERA_DETAILS_SIZE - 2*self.X_ERA_DETAILS_DESC_MARGIN
		iconSize = 30
		height = iconSize * 5 / 4
		NewYields = []

		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				iDecreasePrice =  gc.getNewEraInfo(iNextEra).getYieldDecreasePrice(iYield)
				if iDecreasePrice > 0:
					NewYields.append(iYield)

		iCount = len(NewYields) 
		if iCount > 0:
			szText = u"<font=2b>" + localText.getText("TXT_KEY_NEW_ERAS_SCREEN_DECREASE_PRICE_TITLE", (iCount, )) + u"</font>"			
			screen.setLabelAt(self.getNextWidgetName(), "DescriptionTexts", u"<font=2>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 10, yOffset + yStart - 10, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			for iYield in range(iCount):
				eYield = NewYields[iYield]
				iDecreasePrice =  gc.getNewEraInfo(iNextEra).getYieldDecreasePrice(eYield)
				szText = localText.getText("TXT_KEY_NEW_ERAS_SCREEN_DECREASE_PRICE", (iDecreasePrice, ))
				szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))
				xYieldOffset = iYield*(height+iconSize+17)
				screen.addDDSGFCAt(self.getNextWidgetName(), "DescriptionTexts", gc.getYieldInfo(eYield).getButton(), 10 + xYieldOffset, yStart + yOffset, iconSize, iconSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_YIELDS, eYield, -1 , False)
				screen.setLabelAt(self.getNextWidgetName(), "DescriptionTexts", u"<font=3b>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 10 + xYieldOffset + iconSize + 5, yStart + yOffset + 13, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			yOffset += yStart - height

		return yOffset

	def displayTopErasRequirements(self):
		screen = self.getScreen()
		player = self.pPlayer
		kTeam = gc.getTeam(player.getTeam())
		
		iNextEra = self.getNextNewEra()
		iTurn = kTeam.getCurrentTurn()
		
		iMaxTurn = kTeam.getRequiredMaxTurn(iNextEra)

		iIdealTurn = kTeam.getIdealTurn(iNextEra)

		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("FATHER_RIGHT_BOX").getPath(), self.X_ERAS_AIMS_START, self.Y_ERAS_AIM1_START, self.X_ERAS_AIMS_SIZE, self.Y_ERAS_AIM1_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if iMaxTurn > 0:			
			szText =  u"<font=2b>" + localText.getText("TXT_KEY_NEW_ERAS_SCREEN_PROGRESS", ()).upper() + u"</font>"
			screen.setLabel(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, self.X_ERAS_AIMS_START + self.X_ERAS_AIMS_SIZE /2, self.Y_ERAS_AIM1_START + self.Y_PROGRESS_BAR_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
			szColor = gc.getInfoTypeForString("COLOR_PLAYER_MIDDLE_GREEN_TEXT")
			if iTurn > iIdealTurn:
				if iTurn > (iIdealTurn + iMaxTurn) /2:
					szColor = gc.getInfoTypeForString("COLOR_RED")
				else :
					szColor = gc.getInfoTypeForString("COLOR_YELLOW")


			szText = localText.getText("TXT_KEY_NEW_ERAS_SCREEN_MAX_TURN", ())
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_ERAS_AIMS_START + self.X_ERAS_AIMS_SIZE /2, self.Y_ERAS_AIM1_START + self.Y_PROGRESS_BAR_TITLE + self.Y_PROGRESS_BAR_DESC, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			# PROGRESS BAR
			screen.addStackedBarGFC("ProgressBar", self.X_ERAS_AIMS_START + self.X_PROGRESS_BAR_OFFSET, self.Y_ERAS_AIM1_START + self.Y_PROGRESS_BAR_TITLE + self.Y_PROGRESS_BAR_DESC + self.Y_PROGRESS_BAR_OFFSET, self.X_ERAS_AIMS_SIZE - self.X_PROGRESS_BAR_OFFSET *2, 25, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setStackedBarColors("ProgressBar", InfoBarTypes.INFOBAR_STORED, szColor)
			screen.setStackedBarColors("ProgressBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
			
			# REBEL BAR FILL PERCENTAGE
			fPercentage = float(iTurn) / float(iMaxTurn)
			screen.setBarPercentage("ProgressBar", InfoBarTypes.INFOBAR_STORED, fPercentage)

			szText = u"%d/%d" %(iTurn, iMaxTurn, )
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=2b>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_ERAS_AIMS_START + self.X_ERAS_AIMS_SIZE /2, self.Y_ERAS_AIM1_START + self.Y_PROGRESS_BAR_TITLE + self.Y_PROGRESS_BAR_DESC + self.Y_PROGRESS_BAR_OFFSET + 3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else :
			szText = localText.changeTextColor(localText.getText("TXT_KEY_NEW_ERAS_SCREEN_NO_MAX_TURN", ()), gc.getInfoTypeForString("COLOR_FONT_CREAM"))
			screen.addMultilineText(self.getNextWidgetName(),  u"<font=3b>" + szText + u"</font>", self.X_ERAS_AIMS_START + self.X_ERAS_AIMS_SIZE*1/10, self.Y_ERAS_AIM1_START + self.Y_ERAS_AIM1_SIZE * 1 / 3, self.X_ERAS_AIMS_SIZE*8/10, self.Y_ERAS_AIM1_SIZE * 3 / 5, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
	
			
	def displayBottomErasRequirements(self):
		screen = self.getScreen()
		player = self.pPlayer
		kTeam = gc.getTeam(player.getTeam())

		iNextEra = self.getNextNewEra()
		self.yErasRequirementsOffSet = 0
		eVictory = gc.getGame().getVictoryTarget()
		
		screen.addDDSGFC(self.getNextWidgetName(), ArtFileMgr.getInterfaceArtInfo("FATHER_RIGHT_BOX").getPath(), self.X_ERAS_AIMS_START, self.Y_ERAS_AIM2_START, self.X_ERAS_AIMS_SIZE, self.Y_ERAS_AIM2_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szText =  u"<font=2b>" + localText.getText("TXT_KEY_NEW_ERAS_SCREEN_REQUIREMENTS", ()).upper() + u"</font>"
		screen.setLabel(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, self.X_ERAS_AIMS_START + self.X_ERAS_AIMS_SIZE /2, self.Y_ERAS_AIM2_START + self.Y_ERAS_AIM2_OFFSET_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# COLONIES REQUIREMENT
		self.requiredValue = kTeam.getRequiredNumCities(iNextEra)
		szText = localText.getText("TXT_KEY_NEW_ERAS_SCREEN_COLONIES_REQUIREMENT", (kTeam.getNumEuropeanCities(), self.requiredValue, ))
		self.addErasRequirementBasic(szText, kTeam.hasReachedNumCitiesRequirement(iNextEra), self.COLONIES_REQUIREMENT)
		
		# REBELS RATE REQUIREMENT
		self.requiredValue = kTeam.getRequiredRebelPercent(iNextEra)
		szText = localText.getText("TXT_KEY_NEW_ERAS_SCREEN_REBELS_REQUIREMENT", (kTeam.getRebelPercent(), self.requiredValue, ))
		self.addErasRequirementBasic(szText, kTeam.hasReacheRebelPercentRequirement(iNextEra), self.REBELS_REQUIREMENT)
		
		# MIN TURN REQUIREMENT
		iTargetNewEra = gc.getVictoryInfo(eVictory).getTargetNewEra()
		if(iTargetNewEra == 0 or iTargetNewEra != iNextEra):
			self.requiredValue = kTeam.getRequiredMinTurn(iNextEra)
			szText = localText.getText("TXT_KEY_NEW_ERAS_SCREEN_MIN_TURN_REQUIREMENT", (kTeam.getCurrentTurn(), self.requiredValue, ))
			self.addErasRequirementBasic(szText, kTeam.hasReachedMinTurnRequirement(iNextEra), self.MIN_TURN_REQUIREMENT)
			
		# MIN GOLD REQUIREMENT
		self.requiredValue = kTeam.getRequiredGold(iNextEra)
		szText = localText.getText("TXT_KEY_NEW_ERAS_SCREEN_MIN_GOLD_REQUIREMENT", (kTeam.getGold(), self.requiredValue, ))
		self.addErasRequirementBasic(szText, kTeam.hasReachedGoldRequirement(iNextEra), self.MIN_GOLD_REQUIREMENT)
		
		# MIN RAW MATERIALS SOLD REQUIREMENT
		self.requiredValue = kTeam.getRequiredRawMaterialsSold(iNextEra)
		szText = localText.getText("TXT_KEY_NEW_ERAS_SCREEN_RAW_MATERIALS_REQUIREMENT", (kTeam.getNewWorldYieldQuantity(), self.requiredValue, ))
		self.addErasRequirementBasic(szText, kTeam.hasReachedRawMaterialsSoldRequirement(iNextEra), self.RAW_MATERIALS_REQUIREMENT)

		# LAND DISCOVERED REQUIREMENT
		self.requiredValue = kTeam.getRequiredLandDiscovered(iNextEra)
		szText = localText.getText("TXT_KEY_NEW_ERAS_SCREEN_LAND_DISCOVERED_REQUIREMENT", (kTeam.getLandDiscovered(), self.requiredValue, ))
		self.addErasRequirementBasic(szText, kTeam.hasReachedLandDiscoveredRequirement(iNextEra), self.LAND_DISCOVERED_REQUIREMENT)

		# RELIGIOUS INFLUENCE REQUIREMENT
		self.requiredValue = kTeam.getRequiredCrossesStored(iNextEra)
		szText = localText.getText("TXT_KEY_NEW_ERAS_SCREEN_RELIGIOUS_INFLUENCE_REQUIREMENT", (kTeam.getCrossesStored(), self.requiredValue, gc.getYieldInfo(YieldTypes.YIELD_CROSSES).getChar(), ))
		self.addErasRequirementBasic(szText, kTeam.hasReachedCrossesStoredRequirement(iNextEra), self.RELIGIOUS_INFLUENCE_REQUIREMENT)

		# DEFENDER BY COLONY REQUIREMENT
		self.requiredValue = kTeam.getRequiredDefendersByColony(iNextEra)
		szText = localText.getText("TXT_KEY_NEW_ERAS_SCREEN_DEFENDER_BY_COLONY_REQUIREMENT", (self.requiredValue, ))
		self.addErasRequirementBasic(szText, kTeam.hasReachedDefendersByColonyRequirement(iNextEra), self.DEFENDER_BY_COLONY_REQUIREMENT)
		
		# CITIZEN BY COLONY REQUIREMENT
		self.requiredValue = kTeam.getRequiredCitizenByColony(iNextEra)
		szText = localText.getText("TXT_KEY_NEW_ERAS_SCREEN_CITIZEN_BY_COLONY_REQUIREMENT", (self.requiredValue, ))
		self.addErasRequirementBasic(szText, kTeam.hasReachedCitizenByColonyRequirement(iNextEra), self.CITIZEN_BY_COLONY_REQUIREMENT)
		
	def addErasRequirementBasic(self, szText, bChecked, widgetParam):
		if self.requiredValue > 0:
			screen = self.getScreen()
			yOffSet = self.yErasRequirementsOffSet
			InterfaceRequirments = ArtFileMgr.getInterfaceArtInfo("INTERFACE_UNIT_COCHE_NO_ACTIVATE").getPath()
				
			if bChecked:
				InterfaceRequirments = ArtFileMgr.getInterfaceArtInfo("INTERFACE_UNIT_COCHE_ACTIVATE").getPath()
				szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_FONT_CREAM"))

			screen.addDDSGFC(self.getNextWidgetName(), InterfaceRequirments, self.X_ERAS_AIMS_START + self.X_ERAS_AIM2_ICON_SIZE, self.Y_ERAS_AIM2_START + self.Y_ERAS_AIM2_OFFSET_TITLE + self.Y_ERAS_AIM2_OFFSET_REQUIREMENTS + yOffSet, self.X_ERAS_AIM2_ICON_SIZE, self.X_ERAS_AIM2_ICON_SIZE, WidgetTypes.WIDGET_GENERAL, self.ERA_REQUIREMENT, widgetParam)
			
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ERAS_AIMS_START + self.X_ERAS_AIM2_ICON_SIZE*2 + 10, self.Y_ERAS_AIM2_START + self.Y_ERAS_AIM2_OFFSET_TITLE + self.Y_ERAS_AIM2_OFFSET_REQUIREMENTS + yOffSet +  self.Y_ERAS_AIM2_OFFSET_REQUIREMENTS / 5, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, self.ERA_REQUIREMENT, widgetParam)
			self.yErasRequirementsOffSet += self.Y_ERAS_AIM2_OFFSET_ROWS

	def getNextNewEra(self):
		player = self.pPlayer
		kTeam = gc.getTeam(player.getTeam())	
		return kTeam.getNextNewEra()

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
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (inputClass.getFunctionName() == self.CIV_DROP_DOWN):				
				self.CivDropDown(inputClass)
			else:
				self.EraDropDown()
		return 0

	def CivDropDown( self, inputClass ):
		screen = self.getScreen()
		iIndex = screen.getSelectedPullDownID(self.CIV_DROP_DOWN)
		self.pPlayer = gc.getPlayer(screen.getPullDownData(self.CIV_DROP_DOWN, iIndex))
		self.drawContents()

	def update(self, fDelta):
		screen = self.getScreen()
		
	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		if eWidgetType == WidgetTypes.WIDGET_GENERAL:
			if iData1 == self.ERA_REQUIREMENT:
				# if iData2 == self.COLONIES_REQUIREMENT:
				# 	return self.getColoniesRequirementHelp()
				# elif iData2 == self.REBELS_REQUIREMENT:
				# 	return localText.getText("TXT_KEY_ECON_GOLD_RESERVE", ())
				# elif iData2 == self.MIN_TURN_REQUIREMENT:
				# 	return localText.getText("TXT_KEY_ECON_GOLD_RESERVE", ())
				# elif iData2 == self.MIN_GOLD_REQUIREMENT:
				# 	return localText.getText("TXT_KEY_ECON_GOLD_RESERVE", ())
				# elif iData2 == self.RAW_MATERIALS_REQUIREMENT:
				# 	return localText.getText("TXT_KEY_ECON_GOLD_RESERVE", ())
				# elif iData2 == self.LAND_DISCOVERED_REQUIREMENT:
				# 	return localText.getText("TXT_KEY_ECON_GOLD_RESERVE", ())
				# elif iData2 == self.RELIGIOUS_INFLUENCE_REQUIREMENT:
				# 	return localText.getText("TXT_KEY_ECON_GOLD_RESERVE", ())
				if iData2 == self.DEFENDER_BY_COLONY_REQUIREMENT:
					return self.getDefendersRequirementHelp()
				elif iData2 == self.CITIZEN_BY_COLONY_REQUIREMENT:
					return self.getCitizenRequirementHelp()
				
		return u""
	

	def calculateSizesAndPositions(self):

		screen = self.getScreen()

		self.XResolution = screen.getXResolution()
		self.YResolution = screen.getYResolution()

		self.W_EXIT = 120
		self.H_EXIT = 30

		self.X_EXIT = self.XResolution - self.W_EXIT 
		self.Y_EXIT = self.YResolution - self.H_EXIT

		self.X_ERAS_AIMS_OFFSET = 40 * self.XResolution / 1024

		self.X_ERAS_AIMS_SIZE = 400 * self.XResolution / 1024
		self.Y_ERAS_AIM1_SIZE = 200 * self.YResolution / 768
		self.X_ERAS_AIMS_START = self.XResolution - self.X_ERAS_AIMS_SIZE - self.X_ERAS_AIMS_OFFSET
		self.Y_ERAS_AIM1_START =  100 * self.YResolution / 768

		self.X_PROGRESS_BAR_OFFSET = 10 * self.XResolution / 1024
		self.Y_PROGRESS_BAR_OFFSET = 40 * self.YResolution / 768
		self.Y_PROGRESS_BAR_TITLE = 20 * self.YResolution / 768
		self.Y_PROGRESS_BAR_DESC = 35 * self.YResolution / 768

		self.Y_ERAS_AIM2_SIZE = self.YResolution - self.Y_ERAS_AIM1_START - self.Y_ERAS_AIM1_SIZE - 2*self.X_ERAS_AIMS_OFFSET - self.H_EXIT/2
		self.Y_ERAS_AIM2_START =  self.Y_ERAS_AIM1_START + self.Y_ERAS_AIM1_SIZE + self.X_ERAS_AIMS_OFFSET
		self.Y_ERAS_AIM2_OFFSET_ROWS = 30 * self.YResolution / 768
		self.Y_ERAS_AIM2_OFFSET_TITLE = 20 * self.YResolution / 768
		self.Y_ERAS_AIM2_OFFSET_REQUIREMENTS = 30 * self.YResolution / 768
		self.X_ERAS_AIM2_ICON_SIZE = 20 * self.XResolution / 768

		self.X_ERA_DETAILS_START = self.X_ERAS_AIMS_OFFSET
		self.Y_ERA_DETAILS_START = self.Y_ERAS_AIM1_START - 3
		self.X_ERA_DETAILS_SIZE = self.XResolution - self.X_ERAS_AIMS_OFFSET*3 - self.X_ERAS_AIMS_SIZE
		self.Y_ERA_DETAILS_SIZE = self.YResolution - self.X_ERA_DETAILS_START - self.X_ERAS_AIMS_OFFSET*2 - self.H_EXIT * 2 - self.X_ERAS_AIMS_OFFSET/2
		self.X_ERA_DETAILS_MARGIN = 30 * self.XResolution / 1024

		self.Y_ERA_DETAILS_DESC_SIZE = self.Y_ERA_DETAILS_SIZE  * 7 / 11
		self.X_ERA_DETAILS_DESC_MARGIN = self.X_ERA_DETAILS_MARGIN / 2

	def EraDropDown( self ):
		screen = self.getScreen()
		iIndex = screen.getSelectedPullDownID(self.ERA_DROP_DOWN)
		eTeam = self.pPlayer.getTeam()
		kTeam = gc.getTeam(eTeam)
		kTeam.setNewEra(iIndex)
		self.drawContents()

	def getDefendersRequirementHelp(self):
		szText = u""
		eTeam = self.pPlayer.getTeam()
		kTeam = gc.getTeam(eTeam)
		iRequired = kTeam.getRequiredDefendersByColony(kTeam.getNextNewEra())
		iPlayerCount = 0
		for j in range(gc.getMAX_PLAYERS()):
			loopPlayer = gc.getPlayer(j)
			
			if loopPlayer.getTeam() == eTeam and loopPlayer.isAlive() and not loopPlayer.isEurope() and not loopPlayer.isNative():
				iAccount = 0
				if iPlayerCount > 0:
					szText += "\n"
				szText += localText.getText("TXT_KEY_PLAYER_DESC_NEW_ERA", (loopPlayer.getName(), )) + "\n" 
				iPlayerCount += 1
				(loopCity, iter) = loopPlayer.firstCity(false)
				while(loopCity):
					iDefenders = loopCity.getNumDefenders()
					color = "COLOR_RED"
					if iDefenders >= iRequired:
						color = "COLOR_GREEN"
					szText += localText.changeTextColor(localText.getText("TXT_KEY_CITY_DESC_NEW_ERA", (loopCity.getName(), iDefenders, )), gc.getInfoTypeForString(color)) + "\n" 
					iAccount += 1
					(loopCity, iter) = loopPlayer.nextCity(iter, false)
				if iAccount == 0:
					szText += localText.getText("TXT_KEY_PLAYER_NO_COLONY_HELP", ())
					szText += "\n"

		return szText
	def getCitizenRequirementHelp(self):
		szText = u""
		eTeam = self.pPlayer.getTeam()
		kTeam = gc.getTeam(eTeam)
		iRequired = kTeam.getRequiredCitizenByColony(kTeam.getNextNewEra())
		iPlayerCount = 0
		for j in range(gc.getMAX_PLAYERS()):
			loopPlayer = gc.getPlayer(j)
			
			if loopPlayer.getTeam() == eTeam and loopPlayer.isAlive() and not loopPlayer.isEurope() and not loopPlayer.isNative():
				iAccount = 0
				if iPlayerCount > 0:
					szText += "\n"
				szText += localText.getText("TXT_KEY_PLAYER_DESC_NEW_ERA", (loopPlayer.getName(), )) + "\n" 
				iPlayerCount += 1
				(loopCity, iter) = loopPlayer.firstCity(false)
				while(loopCity):
					iPopulation = loopCity.getPopulation()
					color = "COLOR_RED"
					if iPopulation >= iRequired:
						color = "COLOR_GREEN"
					szText += localText.changeTextColor(localText.getText("TXT_KEY_CITY_DESC_NEW_ERA", (loopCity.getName(), iPopulation, )), gc.getInfoTypeForString(color)) + "\n" 
					iAccount += 1
					(loopCity, iter) = loopPlayer.nextCity(iter, false)
				if iAccount == 0:
					szText += localText.getText("TXT_KEY_PLAYER_NO_COLONY_HELP", ())
					szText += "\n"

		return szText
