## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
#
# for error reporting
import traceback

# for file ops
import os
import sys
import time

# For Civ game code access
from CvPythonExtensions import *

# For exception handling
SHOWEXCEPTIONS = 1

# for C++ compatibility
false=False
true=True

# globals
gc = CyGlobalContext()
FontIconMap = {}
localText = CyTranslator()

############################################
##DOANE Globals
############################################

##Profile: Enable/Disable profilling for some DoaNE functions. Print to "PythonDbg.log" file.
bProfilePP = False #CvPediaProfession
bProfileWBS = False #CvWorldBuilderScreen
bProfileDMGU = False #DoaneMapGeneratorUtil
bProfileMGU = True #CvMapGeneratorUtil
##

##Debug: Enable/Disable DoaNE debug messages in "PythonDbg.log" file
bDoDebugWBS = True #CvWorldBuilderScreen 
bDoDebugEM = True #CvEventManager
bDoDebugMGU = False #CvMapGeneratorUtil ---> Basic
bDoDebugAdvMGU = False #CvMapGeneratorUtil ---> Advanced: it enables log for useless & not critical points.  NOT RECOMMENDED
bDoDebugEC0S = True #CvEuropeC0Screen
bDoDebugDU = True #DoaneUtil
bDoDebugDMGU = True #DoaneMapGeneratorUtil
bDoDebugPP = True #CvPediaProfession
##

##DLL Python Checker: dictionary of DLL fuctions exposed to python to check
functionsDict = {
				'getBUILDER_PACK_YIELD_COST_PERCENT':				gc.getBUILDER_PACK_YIELD_COST_PERCENT(),
				'getBuilderPackToolCost':							gc.getBuilderPackToolCost(),
				'getBuilderPackLumberCost':							gc.getBuilderPackLumberCost(),
				'getSURVIVORS_ON_TRANSPORT_SINKING_PROBABILITY':	gc.getSURVIVORS_ON_TRANSPORT_SINKING_PROBABILITY(),
				'_setDefineBOOL':									gc.setDefineBOOL("bool", True, False),
				'getDefineBOOL':									gc.getDefineBOOL("bool"),
				'getDefineRemBOOL':									gc.getDefineRemBOOL("bool", False),
				# '_setDefineSCHAR':									gc.setDefineSCHAR("schar", -123, False),
				'getDefineSCHAR':									gc.getDefineSCHAR("schar"),
				'getDefineRemSCHAR':								gc.getDefineRemSCHAR("schar", 0),
				'_setDefineUCHAR':									gc.setDefineUCHAR("uchar", 255, False),
				'getDefineUCHAR':									gc.getDefineUCHAR("uchar"),
				'getDefineRemUCHAR':								gc.getDefineRemUCHAR("uchar", 0),
				'_setDefineSSHORT':									gc.setDefineSSHORT("sshort", -2000, False),
				'getDefineSSHORT':									gc.getDefineSSHORT("sshort"),
				'getDefineRemSSHORT':								gc.getDefineRemSSHORT("sshort", 0),
				'_setDefineUSHORT':									gc.setDefineUSHORT("ushort", 2000, False),
				'getDefineUSHORT':									gc.getDefineUSHORT("ushort"),
				'getDefineRemUSHORT':								gc.getDefineRemUSHORT("ushort",0),
				'_setDefineSINT':									gc.setDefineSINT("sint", -5000, False),
				'getDefineRemSINT':									gc.getDefineRemSINT("sint", 0),
				'_setDefineUINT':									gc.setDefineUINT("uint", 5000, False),
				'getDefineUINT':									gc.getDefineUINT("uint"),
				'getDefineRemUINT':									gc.getDefineRemUINT("uint", 0),
				}

##Worldbuilder:
#Unit Unique Name Generator
iNameGenMethDef = 1 #This is default value, functions may still use other values as arguments... It can be 0,1 or 2.  NOT RECOMMENDED ANY VALUE OTHER THAN 1
iNameGenMeth = 2 #Value used in game. It can be 0,1 or 2. It enables different methods. No unique name (0),  Recommended (2), if getting errors try (1).
##

##Event Manager:
#Multiplayer
bDoPbem = True #Enable/disable some DoaNE  features for Play-by-Mail Game
##

##Map Generator:
#Features placement
bDesertLogicJungle = True #Checks if there are deserts adjacent to the plot where the map generator would add the Jungle and adjust that placement according to that.
bDesertLogicLightForest = True #Checks if there are deserts adjacent to the plot where the map generator would add the Light Forest and adjust that placement according to that.
bDesertLogicForest = True #Checks if there are deserts adjacent to the plot where the map generator would add the Forest and adjust that placement according to that.
iNumDesertJungle = 1 #Between 1 and 8. Nummber of desert plots adjacents not allowed. In this case having only 1 plot with desert adjacent to pPlot will prevent the function to generate  the Jungle.
iNumDesertLightForest = 5 #Between 1 and 8. Nummber of desert plots adjacents  not allowed. In this case having 5 plots (or more)  with desert adjacent to pPlot will prevent the function to generate  the Light Forest.
iNumDesertForest = 2 #Between 1 and 8. Nummber of desert plots adjacents  not allowed. In this case having 2 plots (or more)  with desert adjacent to pPlot will prevent the function to generate  the Forest.
bFeaturePlacement = False #Adjust Feature Placement & Variations according to climate and region !!!!!!NOT IMPLEMENTED YET!!!!!!!
#Bonuses Placement
bRandomizeBonuses = False #Force the game to randomize bonuses following Doane Map Generation instead of the placement of the map/map scripts
#Goodies Placement
bRandomizeGoodies = False #Force the game to randomize goodies following Doane Map Generation instead of the placement of the map/map scripts
##

##Europe Screen:

##

##Civilopedia:
#Elite and Standard Units in Civilopedia:
bDoubleMode = True #Enable a Double Animation Mode in the profession screen, it will show the standard unit along the veteran unit animations
VeteranPromotion = "PROMOTION_CIVILOPEDIA_VETERAN" #Set which promotion will be used to display veteran variation of the profession
noSecUnitAllowList = ["PROFESSION_BRAVE", 
					  "PROFESSION_ARMED_BRAVE", 
					  "PROFESSION_MOUNTED_BRAVE",
					  "PROFESSION_ARMED_MOUNTED_BRAVE",
					  "PROFESSION_MARAUDEUR",
					  "PROFESSION_ARTILLERYMAN",
					  "PROFESSION_PATRIOTS"
					 ] #Black list of professions not allowed in Double Mode: 
					    #Put here the profession type and that profession will work like vanilla Single Mode...

############################################
############################################

#
# Popup context enums, values greater than 999 are reserved for events
#

# DEBUG TOOLS
PopupTypeEntityEventTest = 4
PopupTypeEffectViewer = 5

# HELP SCREENS
PopupTypeMilitaryAdvisor = 103
PopupTypePlayerSelect = 104

# WORLD BUILDER
PopupTypeWBContextStart = 200
PopupTypeWBEditCity = PopupTypeWBContextStart
PopupTypeWBEditUnit = 201
PopupTypeWBContextEnd	= 299

# EVENT ID VALUES (also used in popup contexts)
EventEditCityName = 5000
EventEditCity = 5001
EventPlaceObject = 5002
EventAwardGold = 5003
EventEditUnitName = 5006
EventCityWarning = 5007
EventWBAllPlotsPopup = 5008
EventWBLandmarkPopup = 5009
EventWBScriptPopup = 5010
EventWBStartYearPopup = 5011
EventShowWonder = 5012
EventCreateTradeRoute = 5013
EventEditTradeRoute = 5014

#DOANE: 
EventAoDCheatMenu = 6000
EventEditSeawayName = 6001
EventCreateSeaway = 6002
#END DOANE

EventLButtonDown=1
EventLcButtonDblClick=2
EventRButtonDown=3
EventBack=4
EventForward=5
EventKeyDown=6
EventKeyUp=7

#DOANE VANILLA:
# List of unreported Events
#SilentEvents = [EventEditCityName, EventEditUnitName, EventCreateTradeRoute, EventEditTradeRoute]
#END DOANE

# DOANE:  DLL Python Checker
# List of unreported Events
SilentEvents = [EventEditCityName, EventEditUnitName, EventCreateTradeRoute, EventEditTradeRoute, EventAoDCheatMenu, EventEditSeawayName, EventCreateSeaway]
# END DOANE

# Popup defines (TODO: Expose these from C++)
FONT_CENTER_JUSTIFY=1<<2
FONT_RIGHT_JUSTIFY=1<<1
FONT_LEFT_JUSTIFY=1<<0

def convertToUnicode(s):
	"if the string is non unicode, convert it to unicode by decoding it using 8859-1, latin_1"
	if (isinstance(s, str)):
		return s.decode("latin_1")
	return s

def convertToStr(s):
	"if the string is unicode, convert it to str by encoding it using 8859-1, latin_1"
	if (isinstance(s, unicode)):
		return s.encode("latin_1")
	return s

class Profile:
	def __init__(self):
		self.timeStack = []
	
	def reset(self):
		self.timeStack = []

	def startTime(self):
		fTime = time.clock()
		self.timeStack.append(fTime)
	
	def endTime(self, text):
		fEndTime = time.clock()
		fStartTime = self.timeStack.pop(len(self.timeStack) - 1)
		strIndent = ""
		for i in range(len(self.timeStack) - 1):
			strIndent += "  "
		print "%s%s: %.3fs" % (strIndent, text, fEndTime - fStartTime)
		
class RedirectDebug:
	"""Send Debug Messages to Civ Engine"""
	def __init__(self):
		self.m_PythonMgr = CyPythonMgr()
	def write(self, stuff):
		# if str is non unicode and contains encoded unicode data, supply the right encoder to encode it into a unicode object
		if (isinstance(stuff, unicode)):
			self.m_PythonMgr.debugMsgWide(stuff)
		else:
			self.m_PythonMgr.debugMsg(stuff)

class RedirectError:
	"""Send Error Messages to Civ Engine"""
	def __init__(self):
		self.m_PythonMgr = CyPythonMgr()
	def write(self, stuff):
		# if str is non unicode and contains encoded unicode data, supply the right encoder to encode it into a unicode object
		if (isinstance(stuff, unicode)):
			self.m_PythonMgr.errorMsgWide(stuff)
		else:
			self.m_PythonMgr.errorMsg(stuff)

def myExceptHook(type, value, tb):
	lines=traceback.format_exception(type, value, tb)
	#pre= "---------------------Traceback lines-----------------------\n"
	mid="\n".join(lines)
	#post="-----------------------------------------------------------"
	#total = pre+mid+post
	total=mid
	if SHOWEXCEPTIONS:
		sys.stderr.write(total)
	else:
		sys.stdout.write(total)

def pyPrint(stuff):
	stuff = 'PY:' + stuff + "\n"
	sys.stdout.write(stuff)

def pyAssert(cond, msg):
	if (cond==False):
		sys.stderr.write(msg)
	assert(cond, msg)

def getScoreComponent(iRawScore, iInitial, iMax, iFactor, bExponential, bFinal, bVictory):

	if gc.getGame().getEstimateEndTurn() == 0:
		return 0

	if bFinal and bVictory:
		fTurnRatio = float(gc.getGame().getGameTurn()) / float(gc.getGame().getEstimateEndTurn())
		if bExponential and (iInitial != 0):
			fRatio = iMax / iInitial
			iMax = iInitial * pow(fRatio, fTurnRatio)
		else:
			iMax = iInitial + fTurnRatio * (iMax - iInitial)

	iFree = (gc.getDefineINT("SCORE_FREE_PERCENT") * iMax) / 100
	if (iFree + iMax) != 0:
		iScore = (iFactor * (iRawScore + iFree)) / (iFree + iMax)
	else:
		iScore = iFactor

	if bVictory:
		iScore = ((100 + gc.getDefineINT("SCORE_VICTORY_PERCENT")) * iScore) / 100

	if bFinal:
		iScore = ((100 + gc.getDefineINT("SCORE_HANDICAP_PERCENT_OFFSET") + (gc.getGame().getHandicapType() * gc.getDefineINT("SCORE_HANDICAP_PERCENT_PER"))) * iScore) / 100

	return int(iScore)

def shuffle(num, rand):
	"returns a tuple of size num of shuffled numbers"
	piShuffle = [0]*num
	shuffleList(num, rand, piShuffle)	# implemented in C for speed
	return piShuffle

def findInfoTypeNum(typeStr):
	if (typeStr == 'NONE'):
		return -1
	idx = gc.getInfoTypeForString(typeStr)
	pyAssert(idx != -1, "Can't find type enum for type tag %s" %(typeStr,))
	return idx

def AdjustBuilding(add, all, BuildingIdx, pCity): # adds/removes buildings from a city
	"Function for toggling buildings in cities"
	if (BuildingIdx!= -1):
		if (all):                #Add/Remove ALL
			for i in range(BuildingIdx):
				pCity.setHasRealBuilding(i,add)
		else:
			pCity.setHasRealBuilding(BuildingIdx,add)
	return 0

def getIcon(iconEntry):						# returns Font Icons
	global FontIconMap

	iconEntry = iconEntry.lower()
	if (FontIconMap.has_key(iconEntry)):
		return 	FontIconMap.get(iconEntry)
	else:
		return (u"%c" %(191,))

def combatDetailMessageBuilder(cdUnit, ePlayer, iChange):
	if (cdUnit.iExtraCombatPercent != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_EXTRA_COMBAT_PERCENT",(cdUnit.iExtraCombatPercent * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iNativeCombatModifierTB != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_NATIVE_COMBAT",(cdUnit.iNativeCombatModifierTB * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iNativeCombatModifierAB != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_NATIVE_COMBAT",(cdUnit.iNativeCombatModifierAB * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iPlotDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_PLOT_DEFENSE",(cdUnit.iPlotDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iFortifyModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_FORTIFY",(cdUnit.iFortifyModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iCityDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CITY_DEFENSE",(cdUnit.iCityDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iHillsAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_HILLS_ATTACK",(cdUnit.iHillsAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iHillsDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_HILLS",(cdUnit.iHillsDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iFeatureAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_FEATURE_ATTACK",(cdUnit.iFeatureAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iFeatureDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_FEATURE",(cdUnit.iFeatureDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iTerrainAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_TERRAIN_ATTACK",(cdUnit.iTerrainAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iTerrainDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_TERRAIN",(cdUnit.iTerrainDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iCityAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CITY_ATTACK",(cdUnit.iCityAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iDomainDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CITY_DOMAIN_DEFENSE",(cdUnit.iDomainDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iClassDefenseModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_DEFENSE",(cdUnit.iClassDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iClassAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_ATTACK",(cdUnit.iClassAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iCombatModifierT != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_COMBAT",(cdUnit.iCombatModifierT * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iCombatModifierA != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_COMBAT",(cdUnit.iCombatModifierA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iDomainModifierA != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_DOMAIN",(cdUnit.iDomainModifierA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iDomainModifierT != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_DOMAIN",(cdUnit.iDomainModifierT * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iRiverAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_RIVER_ATTACK",(cdUnit.iRiverAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iAmphibAttackModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_AMPHIB_ATTACK",(cdUnit.iAmphibAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if (cdUnit.iRebelPercentModifier != 0):
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_REBEL_SENTIMENT",(cdUnit.iRebelPercentModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

def combatMessageBuilder(cdAttacker, cdDefender, iCombatOdds):

	if (cdAttacker.eVisualOwner != PlayerTypes.UNKNOWN_PLAYER):
		combatMessage = "%s's %s (%.2f)" %(gc.getPlayer(cdAttacker.eVisualOwner).getName(),cdAttacker.sUnitName,cdAttacker.iCurrCombatStr/100.0,)
	else:
		combatMessage = "%s (%.2f)" %(cdAttacker.sUnitName,cdAttacker.iCurrCombatStr/100.0,)
	combatMessage += " " + localText.getText("TXT_KEY_COMBAT_MESSAGE_VS", ()) + " "
	if (cdDefender.eVisualOwner != PlayerTypes.UNKNOWN_PLAYER):
		combatMessage += "%s's %s (%.2f)" %(gc.getPlayer(cdDefender.eOwner).getName(),cdDefender.sUnitName,cdDefender.iCurrCombatStr/100.0,)
	else:
		combatMessage += "%s (%.2f)" %(cdDefender.sUnitName,cdDefender.iCurrCombatStr/100.0,)
	CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
	CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
	combatMessage = "%s %.1f%%" %(localText.getText("TXT_KEY_COMBAT_MESSAGE_ODDS", ()),iCombatOdds/10.0,)
	CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
	CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
	combatDetailMessageBuilder(cdAttacker,cdAttacker.eOwner,-1)
	combatDetailMessageBuilder(cdDefender,cdAttacker.eOwner,1)
	combatDetailMessageBuilder(cdAttacker,cdDefender.eOwner,-1)
	combatDetailMessageBuilder(cdDefender,cdDefender.eOwner,1)

def initDynamicFontIcons():
	global FontIconMap

	info = ""
	desc = ""
	# add Yield Icons
	for i in range(YieldTypes.NUM_YIELD_TYPES):
		info = gc.getYieldInfo(i)
		desc = info.getDescription().lower()
		addIconToMap(info.getChar, desc)
	for key in OtherFontIcons.keys():
		#print key
		FontIconMap[key] = (u"%c" % CyGame().getSymbolID(OtherFontIcons.get(key)))

	#print FontIconMap

def addIconToMap(infoChar, desc):
	global FontIconMap
	desc = convertToStr(desc)
	print "%s - %s" %(infoChar(), desc)
	uc = infoChar()
	if (uc>=0):
		FontIconMap[desc] = u"%c" %(uc,)

OtherFontIcons = { 'happy' : FontSymbols.HAPPY_CHAR,
				'unhappy' : FontSymbols.UNHAPPY_CHAR,
				'healthy' : FontSymbols.HEALTHY_CHAR,
				'unhealthy' : FontSymbols.UNHEALTHY_CHAR,
				'bullet' : FontSymbols.BULLET_CHAR,
				'strength' : FontSymbols.STRENGTH_CHAR,
				'moves' : FontSymbols.MOVES_CHAR,
				'religion' : FontSymbols.RELIGION_CHAR,
				'star' : FontSymbols.STAR_CHAR,
				'silver star' : FontSymbols.SILVER_STAR_CHAR,
				'trade' : FontSymbols.TRADE_CHAR,
				'defense' : FontSymbols.DEFENSE_CHAR,
				'greatpeople' : FontSymbols.GREAT_PEOPLE_CHAR,
				'badgold' : FontSymbols.BAD_GOLD_CHAR,
				'badfood' : FontSymbols.BAD_FOOD_CHAR,
				'eatenfood' : FontSymbols.EATEN_FOOD_CHAR,
				'goldenage' : FontSymbols.GOLDEN_AGE_CHAR,
				'angrypop' : FontSymbols.ANGRY_POP_CHAR,
				'openBorders' : FontSymbols.OPEN_BORDERS_CHAR,
				'defensivePact' : FontSymbols.DEFENSIVE_PACT_CHAR,
				'map' : FontSymbols.MAP_CHAR,
				'occupation' : FontSymbols.OCCUPATION_CHAR,
				'rebel' : FontSymbols.REBEL_CHAR,
				'gold' : FontSymbols.GOLD_CHAR,
				'power' : FontSymbols.POWER_CHAR,
				'unknownYield' : FontSymbols.UNKNOWN_YIELD_CHAR,
				}

GlobalInfosMap = {	'bonus': {'NUM': gc.getNumBonusInfos, 'GET': gc.getBonusInfo},
					'improvement': {'NUM': gc.getNumImprovementInfos, 'GET': gc.getImprovementInfo},
					'yield': {'NUM': YieldTypes.NUM_YIELD_TYPES, 'GET': gc.getYieldInfo},
					'unit': {'NUM': gc.getNumUnitInfos, 'GET': gc.getUnitInfo},
					'civic': {'NUM': gc.getNumCivicInfos, 'GET': gc.getCivicInfo},
					'building': {'NUM': gc.getNumBuildingInfos, 'GET': gc.getBuildingInfo},
					'terrain': {'NUM': gc.getNumTerrainInfos, 'GET': gc.getTerrainInfo},
					'trait': {'NUM': gc.getNumTraitInfos, 'GET': gc.getTraitInfo},
					'feature' : {'NUM': gc.getNumFeatureInfos, 'GET': gc.getFeatureInfo},
					'route': {'NUM': gc.getNumRouteInfos, 'GET': gc.getRouteInfo},
					'promotion': {'NUM':gc.getNumPromotionInfos, 'GET': gc.getPromotionInfo},
				}