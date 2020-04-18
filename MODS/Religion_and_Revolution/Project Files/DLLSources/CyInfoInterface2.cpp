#include "CvGameCoreDLL.h"
#include "CvInfos.h"
//
// Python interface for info classes (formerly structs)
// These are simple enough to be exposed directly - no wrappers
//
void CyInfoPythonInterface2()
{
	OutputDebugString("Python Extension Module - CyInfoPythonInterface2\n");
	python::class_<CvBuildingClassInfo, python::bases<CvInfoBase> >("CvBuildingClassInfo")
		.def("getDefaultBuildingIndex", &CvBuildingClassInfo::getDefaultBuildingIndex, "int ()")
		// Arrays
		.def("getVictoryThreshold", &CvBuildingClassInfo::getVictoryThreshold, "int (int i)")
		;
	python::class_<CvRouteModelInfo, python::bases<CvInfoBase> >("CvRouteModelInfo")
		.def("getModelFile", &CvRouteModelInfo::getModelFile, "string ()")
		.def("setModelFile", &CvRouteModelInfo::setModelFile, "void (string)")
		.def("getConnectString", &CvRouteModelInfo::getConnectString, "string ()")
		.def("getModelConnectString", &CvRouteModelInfo::getModelConnectString, "string ()")
		.def("getRotateString", &CvRouteModelInfo::getRotateString, "string ()")
		;
	python::class_<CvCivilizationInfo, python::bases<CvInfoBase> >("CvCivilizationInfo")
		.def("getDefaultPlayerColor", &CvCivilizationInfo::getDefaultPlayerColor, "int ()")
		.def("getArtStyleType", &CvCivilizationInfo::getArtStyleType, "int ()")
		//Androrc UnitArtStyles
		.def("getUnitArtStyleType", &CvCivilizationInfo::getUnitArtStyleType, "int ()")
		//Androrc End
		.def("getNumCityNames", &CvCivilizationInfo::getNumCityNames, "int ()")
		.def("getNumLeaders", &CvCivilizationInfo::getNumLeaders, "int ()")
		.def("getSelectionSoundScriptId", &CvCivilizationInfo::getSelectionSoundScriptId)
		.def("getActionSoundScriptId", &CvCivilizationInfo::getActionSoundScriptId)
		.def("getAdvancedStartPoints", &CvCivilizationInfo::getAdvancedStartPoints, "int ()")
		.def("getAreaMultiplier", &CvCivilizationInfo::getAreaMultiplier, "int ()")
		.def("getDensityMultiplier", &CvCivilizationInfo::getDensityMultiplier, "int ()")
		.def("getTreasure", &CvCivilizationInfo::getTreasure, "int ()")
		.def("getFavoredTerrain", &CvCivilizationInfo::getFavoredTerrain, "int ()")
		.def("getCapturedCityUnitClass", &CvCivilizationInfo::getCapturedCityUnitClass, "int ()")
		.def("getDefaultProfession", &CvCivilizationInfo::getDefaultProfession, "int ()")
		.def("getMissionaryChar", &CvCivilizationInfo::getMissionaryChar, "int ()")
		.def("isAIPlayable", &CvCivilizationInfo::isAIPlayable, "bool ()")
		.def("isPlayable", &CvCivilizationInfo::isPlayable, "bool ()")
		.def("isWaterStart", &CvCivilizationInfo::isWaterStart, "bool ()")
		.def("isOpenBorders", &CvCivilizationInfo::isOpenBorders, "bool ()")
		.def("isWaterWorks", &CvCivilizationInfo::isWaterWorks, "bool ()")
		.def("isEurope", &CvCivilizationInfo::isEurope, "bool ()")
		.def("isNative", &CvCivilizationInfo::isNative, "bool ()")
		.def("getShortDescription", &CvCivilizationInfo::pyGetShortDescription, "wstring ()")
		.def("getShortDescriptionKey", &CvCivilizationInfo::pyGetShortDescriptionKey, "wstring ()")
		.def("getAdjective", &CvCivilizationInfo::pyGetAdjective, "wstring ()")
		.def("getFlagTexture", &CvCivilizationInfo::getFlagTexture, "string ()")
		.def("getArtDefineTag", &CvCivilizationInfo::getArtDefineTag, "string ()")
		.def("getButton", &CvCivilizationInfo::getButton, "string ()")
		.def("getDerivativeCiv", &CvCivilizationInfo::getDerivativeCiv, "int ()")
		// Arrays
		.def("getCivilizationBuildings", &CvCivilizationInfo::getCivilizationBuildings, "int (int i)")
		.def("getCivilizationUnits", &CvCivilizationInfo::getCivilizationUnits, "int (int i)")
		.def("getNumCivilizationFreeUnits", &CvCivilizationInfo::getNumCivilizationFreeUnits, "int ()")
		.def("getCivilizationFreeUnitsClass", &CvCivilizationInfo::getCivilizationFreeUnitsClass, "int (index)")
		.def("getCivilizationFreeUnitsProfession", &CvCivilizationInfo::getCivilizationFreeUnitsProfession, "int (index)")
		.def("getCivilizationInitialCivics", &CvCivilizationInfo::getCivilizationInitialCivics, "int (int i)")
		.def("getFreeYields", &CvCivilizationInfo::getFreeYields, "int (int i)")
		.def("getTeachUnitClassWeight", &CvCivilizationInfo::getTeachUnitClassWeight, "int (int i)")
		.def("isLeaders", &CvCivilizationInfo::isLeaders, "bool (int i)")
		.def("isCivilizationFreeBuildingClass", &CvCivilizationInfo::isCivilizationFreeBuildingClass, "bool (int i)")
		.def("isValidProfession", &CvCivilizationInfo::isValidProfession, "bool (int i)")
		.def("hasTrait", &CvCivilizationInfo::hasTrait, "bool (int i)")
		.def("getCityNames", &CvCivilizationInfo::getCityNames, "string (int i)")
		;
	python::class_<CvVictoryInfo, python::bases<CvInfoBase> >("CvVictoryInfo")
		.def("getPopulationPercentLead", &CvVictoryInfo::getPopulationPercentLead, "int ()")
		.def("getLandPercent", &CvVictoryInfo::getLandPercent, "int ()")
		.def("getMinLandPercent", &CvVictoryInfo::getMinLandPercent, "int ()")
		.def("getCityCulture", &CvVictoryInfo::getCityCulture, "int ()")
		.def("getNumCultureCities", &CvVictoryInfo::getNumCultureCities, "int ()")
		.def("getTotalCultureRatio", &CvVictoryInfo::getTotalCultureRatio, "int ()")
		.def("getDefault", &CvVictoryInfo::getDefault, "bool ()")
		.def("isTargetScore", &CvVictoryInfo::isTargetScore, "bool ()")
		.def("isEndEurope", &CvVictoryInfo::isEndEurope, "bool ()")
		.def("isEndScore", &CvVictoryInfo::isEndScore, "bool ()")
		.def("isConquest", &CvVictoryInfo::isConquest, "bool ()")
		.def("isPermanent", &CvVictoryInfo::isPermanent, "bool ()")
		.def("isRevolution", &CvVictoryInfo::isRevolution, "bool ()")
		.def("getTotalProductionRate", &CvVictoryInfo::getTotalProductionRate, "int ()") // PatchMod: Victorys START
		.def("getMovie", &CvVictoryInfo::getMovie, "string ()")
		;
	python::class_<CvHurryInfo, python::bases<CvInfoBase> >("CvHurryInfo")
		.def("getGoldPerProduction", &CvHurryInfo::getGoldPerProduction, "int ()")
		.def("getProductionPerPopulation", &CvHurryInfo::getProductionPerPopulation, "int ()")
		.def("getGoldPerCross", &CvHurryInfo::getGoldPerCross, "int ()")
		.def("getYieldCostEuropePercent", &CvHurryInfo::getYieldCostEuropePercent, "int ()")
		.def("getProductionYieldConsumed", &CvHurryInfo::getProductionYieldConsumed, "int ()")
		.def("getProductionYieldPercent", &CvHurryInfo::getProductionYieldPercent, "int ()")
		.def("getFlatGold", &CvHurryInfo::getFlatGold, "int ()")
		.def("isStarting", &CvHurryInfo::isStarting, "bool ()")
		.def("isCity", &CvHurryInfo::isCity, "bool ()")
		;
	python::class_<CvHandicapInfo, python::bases<CvInfoBase> >("CvHandicapInfo")
		.def("getStartingGold", &CvHandicapInfo::getStartingGold, "int ()")
		.def("getFatherPercent", &CvHandicapInfo::getFatherPercent, "int ()")
		.def("getAttitudeChange", &CvHandicapInfo::getAttitudeChange, "int ()")
		.def("getStartingDefenseUnits", &CvHandicapInfo::getStartingDefenseUnits, "int ()")
		.def("getStartingWorkerUnits", &CvHandicapInfo::getStartingWorkerUnits, "int ()")
		.def("getStartingExploreUnits", &CvHandicapInfo::getStartingExploreUnits, "int ()")
		.def("getAIStartingUnitMultiplier", &CvHandicapInfo::getAIStartingUnitMultiplier, "int ()")
		.def("getAIStartingDefenseUnits", &CvHandicapInfo::getAIStartingDefenseUnits, "int ()")
		.def("getAIStartingWorkerUnits", &CvHandicapInfo::getAIStartingWorkerUnits, "int ()")
		.def("getAIStartingExploreUnits", &CvHandicapInfo::getAIStartingExploreUnits, "int ()")
		.def("getAIDeclareWarProb", &CvHandicapInfo::getAIDeclareWarProb, "int ()")
		.def("getAIWorkRateModifier", &CvHandicapInfo::getAIWorkRateModifier, "int ()")
		.def("getAINativeCombatModifier", &CvHandicapInfo::getAINativeCombatModifier, "int ()")
		.def("getAIKingCombatModifier", &CvHandicapInfo::getAIKingCombatModifier, "int ()")
		.def("getAIRebelModifier", &CvHandicapInfo::getAIRebelModifier, "int ()")
		.def("getAIGrowthPercent", &CvHandicapInfo::getAIGrowthPercent, "int ()")
		.def("getAITrainPercent", &CvHandicapInfo::getAITrainPercent, "int ()")
		.def("getAIConstructPercent", &CvHandicapInfo::getAIConstructPercent, "int ()")
		.def("getAIUnitUpgradePercent", &CvHandicapInfo::getAIUnitUpgradePercent, "int ()")
		.def("getAIHurryPercent", &CvHandicapInfo::getAIHurryPercent, "int ()")
		.def("getAIExtraTradePercent", &CvHandicapInfo::getAIExtraTradePercent, "int ()")
		.def("getAIPerEraModifier", &CvHandicapInfo::getAIPerEraModifier, "int ()")
		.def("getAIAdvancedStartPercent", &CvHandicapInfo::getAIAdvancedStartPercent, "int ()")
		.def("getAIKingUnitThresholdPercent", &CvHandicapInfo::getAIKingUnitThresholdPercent, "int ()")
		// < JAnimals Mod Start >
		.def("getAIAnimalLandMaxPercent", &CvHandicapInfo::getAIAnimalLandMaxPercent, "int ()")
		.def("getAIAnimalSeaMaxPercent", &CvHandicapInfo::getAIAnimalSeaMaxPercent, "int ()")
		.def("getAIAnimalLandNumTurnsNoSpawn", &CvHandicapInfo::getAIAnimalLandNumTurnsNoSpawn, "int ()")
		.def("getAIAnimalSeaNumTurnsNoSpawn", &CvHandicapInfo::getAIAnimalSeaNumTurnsNoSpawn, "int ()")
		// < JAnimals Mod End >
		.def("getNumGoodies", &CvHandicapInfo::getNumGoodies, "int ()")
		.def("getEuropePriceThresholdMultiplier", &CvHandicapInfo::getEuropePriceThresholdMultiplier, "int ()")
		.def("getNativePacifismPercent", &CvHandicapInfo::getNativePacifismPercent, "int ()")
		.def("getMissionFailureThresholdPercent", &CvHandicapInfo::getMissionFailureThresholdPercent, "int ()")
		.def("getKingNumUnitMultiplier", &CvHandicapInfo::getKingNumUnitMultiplier, "int ()")
		// TAC - AI Revolution - koma13 - START
		.def("getWaveTurns", &CvHandicapInfo::getWaveTurns, "int (int i)")
		.def("getNumWaves", &CvHandicapInfo::getNumWaves, "int (int i)")
		.def("getWaves", &CvHandicapInfo::getWaves, "int (int i)")
		// TAC - AI Revolution - koma13 - END
		// Arrays
		.def("getGoodies", &CvHandicapInfo::getGoodies, "int (int i)")
		;
	python::class_<CvGameSpeedInfo, python::bases<CvInfoBase> >("CvGameSpeedInfo")
		.def("getGrowthPercent", &CvGameSpeedInfo::getGrowthPercent, "int ()")
		.def("getStoragePercent", &CvGameSpeedInfo::getStoragePercent, "int ()")
		.def("getTrainPercent", &CvGameSpeedInfo::getTrainPercent, "int ()")
		.def("getConstructPercent", &CvGameSpeedInfo::getConstructPercent, "int ()")
		.def("getFatherPercent", &CvGameSpeedInfo::getFatherPercent, "int ()")
		.def("getGreatGeneralPercent", &CvGameSpeedInfo::getGreatGeneralPercent, "int ()")
		.def("getNumTurnIncrements", &CvGameSpeedInfo::getNumTurnIncrements, "int ()")
		.def("getGameTurnInfo", &CvGameSpeedInfo::getGameTurnInfo, python::return_value_policy<python::reference_existing_object>(), "GameTurnInfo ()")
		;
	python::class_<CvTurnTimerInfo, python::bases<CvInfoBase> >("CvTurnTimerInfo")
		.def("getBaseTime", &CvTurnTimerInfo::getBaseTime, "int ()")
		.def("getCityBonus", &CvTurnTimerInfo::getCityBonus, "int ()")
		.def("getUnitBonus", &CvTurnTimerInfo::getUnitBonus, "int ()")
		.def("getFirstTurnMultiplier", &CvTurnTimerInfo::getFirstTurnMultiplier, "int ()")
		;
	python::class_<CvBuildInfo, python::bases<CvInfoBase> >("CvBuildInfo")
		.def("getTime", &CvBuildInfo::getTime, "int ()")
		.def("getCost", &CvBuildInfo::getCost, "int ()")
		.def("getImprovement", &CvBuildInfo::getImprovement, "int ()")
		.def("getRoute", &CvBuildInfo::getRoute, "int ()")
		.def("getEntityEvent", &CvBuildInfo::getEntityEvent, "int ()")
		.def("getMissionType", &CvBuildInfo::getMissionType, "int ()")
		.def("isKill", &CvBuildInfo::isKill, "bool ()")
		// Arrays
		.def("getFeatureTime", &CvBuildInfo::getFeatureTime, "int (int i)")
		.def("getFeatureYield", &CvBuildInfo::getFeatureYield, "int (int iFeature, iYield)")
		.def("isFeatureRemove", &CvBuildInfo::isFeatureRemove, "bool (int i)")
		;
	python::class_<CvGoodyInfo, python::bases<CvInfoBase> >("CvGoodyInfo")
		.def("getGold", &CvGoodyInfo::getGold, "int ()")
		.def("getGoldRand1", &CvGoodyInfo::getGoldRand1, "int ()")
		.def("getGoldRand2", &CvGoodyInfo::getGoldRand2, "int ()")
		.def("getImmigration", &CvGoodyInfo::getImmigration, "int ()") // R&R, ray, Goody Enhancement
		.def("getMapOffset", &CvGoodyInfo::getMapOffset, "int ()")
		.def("getMapRange", &CvGoodyInfo::getMapRange, "int ()")
		.def("getMapProb", &CvGoodyInfo::getMapProb, "int ()")
		.def("getExperience", &CvGoodyInfo::getExperience, "int ()")
		.def("getHealing", &CvGoodyInfo::getHealing, "int ()")
		.def("getDamagePrereq", &CvGoodyInfo::getDamagePrereq, "int ()")
		.def("getCityGoodyWeight", &CvGoodyInfo::getCityGoodyWeight, "int ()")
		.def("getUnitClassType", &CvGoodyInfo::getUnitClassType, "int ()")
		.def("getTeachUnitClassType", &CvGoodyInfo::getTeachUnitClassType, "int ()")
		.def("isBad", &CvGoodyInfo::isBad, "bool ()")
		.def("isWaterGoody", &CvGoodyInfo::isWaterGoody, "bool ()") // R&R, ray, Goodies on Water
		.def("isUnique", &CvGoodyInfo::isUnique, "bool ()") // R&R, ray, Goody Enhancement
		;
	python::class_<CvRouteInfo, python::bases<CvInfoBase> >("CvRouteInfo")
		.def("getValue", &CvRouteInfo::getValue, "int ()")
		.def("getMovementCost", &CvRouteInfo::getMovementCost, "int ()")
		.def("getFlatMovementCost", &CvRouteInfo::getFlatMovementCost, "int ()")
		// Arrays
		.def("getYieldChange", &CvRouteInfo::getYieldChange, "int (int i)")
		;
	python::class_<CvImprovementBonusInfo, python::bases<CvInfoBase> >("CvImprovementBonusInfo")
		.def("getDiscoverRand", &CvImprovementBonusInfo::getDiscoverRand, "int ()")
		.def("isBonusMakesValid", &CvImprovementBonusInfo::isBonusMakesValid, "bool ()")
		// Arrays
		.def("getYieldChange", &CvImprovementBonusInfo::getYieldChange, "int (int i)")
		;
	python::class_<CvImprovementInfo, python::bases<CvInfoBase> >("CvImprovementInfo")
		.def("getTilesPerGoody", &CvImprovementInfo::getTilesPerGoody, "int ()")
		.def("getGoodyUniqueRange", &CvImprovementInfo::getGoodyUniqueRange, "int ()")
		.def("getFeatureGrowthProbability", &CvImprovementInfo::getFeatureGrowthProbability, "int ()")
		.def("getUpgradeTime", &CvImprovementInfo::getUpgradeTime, "int ()")
		.def("getDefenseModifier", &CvImprovementInfo::getDefenseModifier, "int ()")
		.def("getPillageGold", &CvImprovementInfo::getPillageGold, "int ()")
		.def("getImprovementPillage", &CvImprovementInfo::getImprovementPillage, "int ()")
		.def("getImprovementUpgrade", &CvImprovementInfo::getImprovementUpgrade, "int ()")
		.def("isActsAsCity", &CvImprovementInfo::isActsAsCity, "bool ()")
		.def("isHillsMakesValid", &CvImprovementInfo::isHillsMakesValid, "bool ()")
		.def("isRiverSideMakesValid", &CvImprovementInfo::isRiverSideMakesValid, "bool ()")
		.def("isRequiresFlatlands", &CvImprovementInfo::isRequiresFlatlands, "bool ()")
		.def("isRequiresRiverSide", &CvImprovementInfo::isRequiresRiverSide, "bool ()")
		.def("isRequiresFeature", &CvImprovementInfo::isRequiresFeature, "bool ()")
		.def("isWater", &CvImprovementInfo::isWater, "bool ()")
		.def("isGoody", &CvImprovementInfo::isGoody, "bool ()")
		.def("isPermanent", &CvImprovementInfo::isPermanent, "bool ()")
		.def("isOutsideBorders", &CvImprovementInfo::isOutsideBorders, "bool ()")
		.def("getArtDefineTag", &CvImprovementInfo::getArtDefineTag, "string ()")
		// Arrays
		.def("getPrereqNatureYield", &CvImprovementInfo::getPrereqNatureYield, "int (int i)")
		.def("getYieldIncrease", &CvImprovementInfo::getYieldIncrease, "int (int i)")
		.def("getRiverSideYieldChange", &CvImprovementInfo::getRiverSideYieldChange, "int (int i)")
		.def("getHillsYieldChange", &CvImprovementInfo::getHillsYieldChange, "int (int i)")
		.def("getTerrainMakesValid", &CvImprovementInfo::getTerrainMakesValid, "bool (int i)")
		.def("getFeatureMakesValid", &CvImprovementInfo::getFeatureMakesValid, "bool (int i)")
		.def("getImprovementBonusYield", &CvImprovementInfo::getImprovementBonusYield, "int (int i, int j)")
		.def("isImprovementBonusMakesValid", &CvImprovementInfo::isImprovementBonusMakesValid, "bool (int i)")
		.def("getImprovementBonusDiscoverRand", &CvImprovementInfo::getImprovementBonusDiscoverRand, "int (int i)")
		.def("getRouteYieldChanges", &CvImprovementInfo::getRouteYieldChanges, "int (int i, int j)")
		;
	python::class_<CvBonusInfo, python::bases<CvInfoBase> >("CvBonusInfo")
		.def("getChar", &CvBonusInfo::getChar, "int ()")
		.def("getAIObjective", &CvBonusInfo::getAIObjective, "int ()")
		.def("getMinAreaSize", &CvBonusInfo::getMinAreaSize, "int ()")
		.def("getMinLatitude", &CvBonusInfo::getMinLatitude, "int ()")
		.def("getMaxLatitude", &CvBonusInfo::getMaxLatitude, "int ()")
		.def("getPlacementOrder", &CvBonusInfo::getPlacementOrder, "int ()")
		.def("getConstAppearance", &CvBonusInfo::getConstAppearance, "int ()")
		.def("getRandAppearance1", &CvBonusInfo::getRandAppearance1, "int ()")
		.def("getRandAppearance2", &CvBonusInfo::getRandAppearance2, "int ()")
		.def("getRandAppearance3", &CvBonusInfo::getRandAppearance3, "int ()")
		.def("getRandAppearance4", &CvBonusInfo::getRandAppearance4, "int ()")
		.def("getPercentPerPlayer", &CvBonusInfo::getPercentPerPlayer, "int ()")
		.def("getTilesPer", &CvBonusInfo::getTilesPer, "int ()")
		.def("getMinLandPercent", &CvBonusInfo::getMinLandPercent, "int ()")
		.def("getUniqueRange", &CvBonusInfo::getUniqueRange, "int ()")
		.def("getGroupRange", &CvBonusInfo::getGroupRange, "int ()")
		.def("getGroupRand", &CvBonusInfo::getGroupRand, "int ()")
		.def("isOneArea", &CvBonusInfo::isOneArea, "bool ()")
		.def("isHills", &CvBonusInfo::isHills, "bool ()")
		 //TAC Whaling, ray
		.def("isOcean", &CvBonusInfo::isOcean, "bool ()")
		.def("isWhalingboatWorkable", &CvBonusInfo::isWhalingboatWorkable, "bool ()")
		//End TAC Whaling, ray
		.def("isFishingboatWorkable", &CvBonusInfo::isFishingboatWorkable, "bool ()") // R&R, ray, High Sea Fishing
		.def("isFlatlands", &CvBonusInfo::isFlatlands, "bool ()")
		.def("isNoRiverSide", &CvBonusInfo::isNoRiverSide, "bool ()")
		.def("getArtDefineTag", &CvBonusInfo::getArtDefineTag, "string ()")
		// Arrays
		.def("getYieldChange", &CvBonusInfo::getYieldChange, "int (int i)")
		.def("isTerrain", &CvBonusInfo::isTerrain, "bool (int i)")
		.def("isFeature", &CvBonusInfo::isFeature, "bool (int i)")
		.def("isFeatureTerrain", &CvBonusInfo::isFeatureTerrain, "bool (int i)")
		.def("getButton", &CvBonusInfo::getButton, "string ()")
		.def("getArtInfo", &CvBonusInfo::getArtInfo,  python::return_value_policy<python::reference_existing_object>(), "CvArtInfoBonus ()")
		;
	python::class_<CvFeatureInfo, python::bases<CvInfoBase> >("CvFeatureInfo")
		.def("getMovementCost", &CvFeatureInfo::getMovementCost, "int ()")
		.def("getSeeThroughChange", &CvFeatureInfo::getSeeThroughChange, "int ()")
		.def("getAppearanceProbability", &CvFeatureInfo::getAppearanceProbability, "int ()")
		.def("getDisappearanceProbability", &CvFeatureInfo::getDisappearanceProbability, "int ()")
		.def("getGrowthProbability", &CvFeatureInfo::getGrowthProbability, "int ()")
		// R&R, Robert Surcouf, Damage on Storm plots, Start
		.def("getTurnDamage", &CvFeatureInfo::getTurnDamage, "int ()")
		.def("isGeneratedEveryRound", &CvFeatureInfo::isGeneratedEveryRound, "bool ()")
		// R&R, Robert Surcouf, Damage on Storm plots, End
		.def("getDefenseModifier", &CvFeatureInfo::getDefenseModifier, "int ()")
		.def("getAdvancedStartRemoveCost", &CvFeatureInfo::getAdvancedStartRemoveCost, "int ()")
		.def("isNoCoast", &CvFeatureInfo::isNoCoast, "bool ()")
		.def("isNoRiver", &CvFeatureInfo::isNoRiver, "bool ()")
		.def("isNoAdjacent", &CvFeatureInfo::isNoAdjacent, "bool ()")
		.def("isRequiresFlatlands", &CvFeatureInfo::isRequiresFlatlands, "bool ()")
		.def("isRequiresRiver", &CvFeatureInfo::isRequiresRiver, "bool ()")
		.def("isImpassable", &CvFeatureInfo::isImpassable, "bool ()")
		.def("isNoCity", &CvFeatureInfo::isNoCity, "bool ()")
		.def("isNoImprovement", &CvFeatureInfo::isNoImprovement, "bool ()")
		.def("isVisibleAlways", &CvFeatureInfo::isVisibleAlways, "bool ()")
		// Arrays
		.def("getYieldChange", &CvFeatureInfo::getYieldChange, "int (int i)")
		.def("getRiverYieldIncrease", &CvFeatureInfo::getRiverYieldIncrease, "int (int i)")
		.def("isTerrain", &CvFeatureInfo::isTerrain, "bool (int i)")
		.def("getNumVarieties", &CvFeatureInfo::getNumVarieties, "int ()")
		;
}
