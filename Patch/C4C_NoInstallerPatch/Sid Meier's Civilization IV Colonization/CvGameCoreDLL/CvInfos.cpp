//  $Header:
//------------------------------------------------------------------------------------------------
//
//  FILE:    CvInfos.cpp
//
//
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2003 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------
#include "CvGameCoreDLL.h"
#include "CvInfos.h"
#include "CvGlobals.h"
#include "CvArtFileMgr.h"
#include "CvXMLLoadUtility.h"
#include "CvDLLXMLIFaceBase.h"
#include "CvGameTextMgr.h"
#include "CvGameCoreUtils.h"

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CInfoBase()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvInfoBase::CvInfoBase() :
m_bGraphicalOnly(false)
{
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CInfoBase()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvInfoBase::~CvInfoBase()
{
}

void CvInfoBase::read(FDataStreamBase* pStream)
{
	m_szCachedText.clear();
	m_szCachedCivilopedia.clear();
	m_szCachedHelp.clear();
	m_szCachedStrategy.clear();
	m_aszExtraXMLforPass3.clear();

	pStream->Read(&m_bGraphicalOnly);
	pStream->ReadString(m_szType);
	pStream->ReadString(m_szCivilopediaKey);
	pStream->ReadString(m_szHelpKey);
	pStream->ReadString(m_szStrategyKey);
	pStream->ReadString(m_szButton);
	pStream->ReadString(m_szTextKey);

	int iSize;
	pStream->Read(&iSize);
	m_aszExtraXMLforPass3.resize(iSize);
	for(int i=0;i<iSize;i++)
	{
		pStream->ReadString(m_aszExtraXMLforPass3[i]);
	}
}

void CvInfoBase::write(FDataStreamBase* pStream)
{
	pStream->Write(m_bGraphicalOnly);
	pStream->WriteString(m_szType);
	pStream->WriteString(m_szCivilopediaKey);
	pStream->WriteString(m_szHelpKey);
	pStream->WriteString(m_szStrategyKey);
	pStream->WriteString(m_szButton);
	pStream->WriteString(m_szTextKey);

	pStream->Write((int)m_aszExtraXMLforPass3.size());
	for(int i=0;i<(int)m_aszExtraXMLforPass3.size();i++)
	{
		pStream->WriteString(m_aszExtraXMLforPass3[i]);
	}
}

void CvInfoBase::reset()
{
	//clear cache
	m_aCachedDescriptions.clear();
	m_szCachedText.clear();
	m_szCachedCivilopedia.clear();
	m_szCachedHelp.clear();
	m_szCachedStrategy.clear();
}

bool CvInfoBase::isGraphicalOnly() const
{
	return m_bGraphicalOnly;
}

const char* CvInfoBase::getType() const
{
	if(m_szType.empty())
	{
		return NULL;
	}

	return m_szType;
}

const char* CvInfoBase::getButton() const
{
	return m_szButton;
}

const wchar* CvInfoBase::getTextKeyWide() const
{
	return m_szTextKey;
}

const wchar* CvInfoBase::getDescription(uint uiForm) const
{
	while(m_aCachedDescriptions.size() <= uiForm)
	{
		m_aCachedDescriptions.push_back(gDLL->getObjectText(m_szTextKey, m_aCachedDescriptions.size()));
	}

	return m_aCachedDescriptions[uiForm];
}

const wchar* CvInfoBase::getText() const
{
	// used instead of getDescription for Info entries that are not objects
	// so they do not have gender/plurality/forms defined in the Translator system
	if (m_szCachedText.empty())
	{
		m_szCachedText = gDLL->getText(m_szTextKey);
	}

	return m_szCachedText;
}

const wchar* CvInfoBase::getCivilopedia() const
{
	if (m_szCachedCivilopedia.empty())
	{
		m_szCachedCivilopedia = gDLL->getText(m_szCivilopediaKey);
	}

	return m_szCachedCivilopedia;
}

const wchar*  CvInfoBase::getHelp() const
{
	if (m_szCachedHelp.empty())
	{
		m_szCachedHelp = gDLL->getText(m_szHelpKey);
	}

	return m_szCachedHelp;
}

const wchar* CvInfoBase::getStrategy() const
{
	if (m_szCachedStrategy.empty())
	{
		m_szCachedStrategy = gDLL->getText(m_szStrategyKey);
	}

	return m_szCachedStrategy;
}

bool CvInfoBase::isMatchForLink(std::wstring szLink, bool bKeysOnly) const
{
	if (szLink == CvWString(getType()).GetCString())
	{
		return true;
	}

	if (!bKeysOnly)
	{
		uint iNumForms = gDLL->getNumForms(getTextKeyWide());
		for (uint i = 0; i < iNumForms; i++)
		{
			if (szLink == getDescription(i))
			{
				return true;
			}
		}
	}

	return false;
}

//
// read from XML
// TYPE, DESC, BUTTON
//
bool CvInfoBase::read(CvXMLLoadUtility* pXML)
{
	// Skip any comments and stop at the next value we might want
	if (!pXML->SkipToNextVal())
	{
		return false;
	}

	pXML->MapChildren();	// try to hash children for fast lookup by name

	// GRAPHICAL ONLY
	pXML->GetChildXmlValByName(&m_bGraphicalOnly, "bGraphicalOnly");

	// TYPE
	pXML->GetChildXmlValByName(m_szType, "Type");

	// DESCRIPTION
	pXML->GetChildXmlValByName(m_szTextKey, "Description");

	// CIVILOPEDIA
	pXML->GetChildXmlValByName(m_szCivilopediaKey, "Civilopedia");

	// HELP
	pXML->GetChildXmlValByName(m_szHelpKey, "Help");

	// STRATEGY
	pXML->GetChildXmlValByName(m_szStrategyKey, "Strategy");

	// BUTTON
	pXML->GetChildXmlValByName(m_szButton, "Button");

	return true;
}

//======================================================================================================
//					CvScalableInfo
//======================================================================================================
bool CvScalableInfo::read(CvXMLLoadUtility* pXML)
{
	float fScale;
	pXML->GetChildXmlValByName(&fScale, "fScale");
	setScale(fScale);
	pXML->GetChildXmlValByName(&fScale, "fInterfaceScale", 1.0f);
	setInterfaceScale(fScale);
	return true;
}

float CvScalableInfo::getScale() const
{
	return m_fScale;
}

void CvScalableInfo::setScale(float fScale)
{
	m_fScale = fScale;
}

float CvScalableInfo::getInterfaceScale() const
{
	return m_fInterfaceScale;
}

void CvScalableInfo::setInterfaceScale(float fInterfaceScale)
{
	m_fInterfaceScale = fInterfaceScale;
}


//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvHotkeyInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvHotkeyInfo::CvHotkeyInfo() :
m_iActionInfoIndex(-1),
m_iHotKeyVal(-1),
m_iHotKeyPriority(-1),
m_iHotKeyValAlt(-1),
m_iHotKeyPriorityAlt(-1),
m_iOrderPriority(0),
m_bAltDown(false),
m_bShiftDown(false),
m_bCtrlDown(false),
m_bAltDownAlt(false),
m_bShiftDownAlt(false),
m_bCtrlDownAlt(false)
{
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvHotkeyInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvHotkeyInfo::~CvHotkeyInfo()
{
}

bool CvHotkeyInfo::read(CvXMLLoadUtility* pXML)
{
	int iVal;
	bool bVal;
	CvString szTextVal;

	if (!CvInfoBase::read(pXML))
	{
		return false;
	}

	if (pXML->GetChildXmlValByName(szTextVal, "HotKey"))
	{
		setHotKey(szTextVal);
	}
	else
	{
		setHotKey("");
	}
	iVal = pXML->GetHotKeyInt(szTextVal);
	setHotKeyVal(iVal);
  if (pXML->GetChildXmlValByName(&iVal, "iHotKeyPriority"))
	{
		setHotKeyPriority(iVal);
	}
	else
	{
		setHotKeyPriority(-1);
	}

	if (pXML->GetChildXmlValByName(szTextVal, "HotKeyAlt"))
	{
		iVal = pXML->GetHotKeyInt(szTextVal);
	}
	else
	{
		iVal = pXML->GetHotKeyInt("");
	}
	setHotKeyValAlt(iVal);
	if (pXML->GetChildXmlValByName(&iVal, "iHotKeyPriorityAlt"))
	{
		setHotKeyPriorityAlt(iVal);
	}
	else
	{
		setHotKeyPriorityAlt(-1);
	}

	if (pXML->GetChildXmlValByName(&bVal, "bAltDown"))
	{
		setAltDown(bVal);
	}
	else
	{
		setAltDown(false);
	}
	if (pXML->GetChildXmlValByName(&bVal, "bShiftDown"))
	{
		setShiftDown(bVal);
	}
	else
	{
		setShiftDown(false);
	}
	if (pXML->GetChildXmlValByName(&bVal, "bCtrlDown"))
	{
		setCtrlDown(bVal);
	}
	else
	{
		setCtrlDown(false);
	}

	if (pXML->GetChildXmlValByName(&bVal, "bAltDownAlt"))
	{
		setAltDownAlt(bVal);
	}
	else
	{
		setAltDownAlt(false);
	}
	if (pXML->GetChildXmlValByName(&bVal, "bShiftDownAlt"))
	{
		setShiftDownAlt(bVal);
	}
	else
	{
		setShiftDownAlt(false);
	}
	if (pXML->GetChildXmlValByName(&bVal, "bCtrlDownAlt"))
	{
		setCtrlDownAlt(bVal);
	}
	else
	{
		setCtrlDownAlt(false);
	}
	if (pXML->GetChildXmlValByName(&iVal, "iOrderPriority"))
	{
		setOrderPriority(iVal);
	}
	else
	{
		setOrderPriority(5);
	}

	setHotKeyDescription(getTextKeyWide(), NULL, pXML->CreateHotKeyFromDescription(getHotKey(), m_bShiftDown, m_bAltDown, m_bCtrlDown));

	return true;
}

void CvHotkeyInfo::read(FDataStreamBase* pStream)
{
	CvInfoBase::read(pStream);

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iHotKeyVal);
	pStream->Read(&m_iHotKeyPriority);
	pStream->Read(&m_iHotKeyValAlt);
	pStream->Read(&m_iHotKeyPriorityAlt);
	pStream->Read(&m_iOrderPriority);
	pStream->Read(&m_bAltDown);
	pStream->Read(&m_bShiftDown);
	pStream->Read(&m_bCtrlDown);
	pStream->Read(&m_bAltDownAlt);
	pStream->Read(&m_bShiftDownAlt);
	pStream->Read(&m_bCtrlDownAlt);
	pStream->ReadString(m_szHotKey);
	pStream->ReadString(m_szHotKeyDescriptionKey);
	pStream->ReadString(m_szHotKeyAltDescriptionKey);
	pStream->ReadString(m_szHotKeyString);
}

void CvHotkeyInfo::write(FDataStreamBase* pStream)
{
	CvInfoBase::write(pStream);

	uint uiFlag = 0;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iHotKeyVal);
	pStream->Write(m_iHotKeyPriority);
	pStream->Write(m_iHotKeyValAlt);
	pStream->Write(m_iHotKeyPriorityAlt);
	pStream->Write(m_iOrderPriority);
	pStream->Write(m_bAltDown);
	pStream->Write(m_bShiftDown);
	pStream->Write(m_bCtrlDown);
	pStream->Write(m_bAltDownAlt);
	pStream->Write(m_bShiftDownAlt);
	pStream->Write(m_bCtrlDownAlt);
	pStream->WriteString(m_szHotKey);
	pStream->WriteString(m_szHotKeyDescriptionKey);
	pStream->WriteString(m_szHotKeyAltDescriptionKey);
	pStream->WriteString(m_szHotKeyString);
}

int CvHotkeyInfo::getActionInfoIndex() const
{
	return m_iActionInfoIndex;
}

void CvHotkeyInfo::setActionInfoIndex(int i)
{
	m_iActionInfoIndex = i;
}

int CvHotkeyInfo::getHotKeyVal() const
{
	return m_iHotKeyVal;
}

void CvHotkeyInfo::setHotKeyVal(int i)
{
	m_iHotKeyVal = i;
}

int CvHotkeyInfo::getHotKeyPriority() const
{
	return m_iHotKeyPriority;
}

void CvHotkeyInfo::setHotKeyPriority(int i)
{
	m_iHotKeyPriority = i;
}

int CvHotkeyInfo::getHotKeyValAlt() const
{
	return m_iHotKeyValAlt;
}

void CvHotkeyInfo::setHotKeyValAlt(int i)
{
	m_iHotKeyValAlt = i;
}

int CvHotkeyInfo::getHotKeyPriorityAlt() const
{
	return m_iHotKeyPriorityAlt;
}

void CvHotkeyInfo::setHotKeyPriorityAlt(int i)
{
	m_iHotKeyPriorityAlt = i;
}

int CvHotkeyInfo::getOrderPriority() const
{
	return m_iOrderPriority;
}

void CvHotkeyInfo::setOrderPriority(int i)
{
	m_iOrderPriority = i;
}

bool CvHotkeyInfo::isAltDown() const
{
	return m_bAltDown;
}

void CvHotkeyInfo::setAltDown(bool b)
{
	m_bAltDown = b;
}

bool CvHotkeyInfo::isShiftDown() const
{
	return m_bShiftDown;
}

void CvHotkeyInfo::setShiftDown(bool b)
{
	m_bShiftDown = b;
}

bool CvHotkeyInfo::isCtrlDown() const
{
	return m_bCtrlDown;
}

void CvHotkeyInfo::setCtrlDown(bool b)
{
	m_bCtrlDown = b;
}

bool CvHotkeyInfo::isAltDownAlt() const
{
	return m_bAltDownAlt;
}

void CvHotkeyInfo::setAltDownAlt(bool b)
{
	m_bAltDownAlt = b;
}

bool CvHotkeyInfo::isShiftDownAlt() const
{
	return m_bShiftDownAlt;
}

void CvHotkeyInfo::setShiftDownAlt(bool b)
{
	m_bShiftDownAlt = b;
}

bool CvHotkeyInfo::isCtrlDownAlt() const
{
	return m_bCtrlDownAlt;
}

void CvHotkeyInfo::setCtrlDownAlt(bool b)
{
	m_bCtrlDownAlt = b;
}

const char* CvHotkeyInfo::getHotKey() const
{
	return m_szHotKey;
}

void CvHotkeyInfo::setHotKey(const char* szVal)
{
	m_szHotKey = szVal;
}

std::wstring CvHotkeyInfo::getHotKeyDescription() const
{
	CvWString szTemp;

	if (!m_szHotKeyAltDescriptionKey.empty())
	{
		szTemp.Format(L"%s (%s)", gDLL->getObjectText(m_szHotKeyAltDescriptionKey, 0).GetCString(), gDLL->getObjectText(m_szHotKeyDescriptionKey, 0).GetCString());
	}
	else
	{
		szTemp = gDLL->getObjectText(m_szHotKeyDescriptionKey, 0);
	}

	if (!m_szHotKeyString.empty())
	{
		szTemp += m_szHotKeyString;
	}

	return szTemp;
}

void CvHotkeyInfo::setHotKeyDescription(const wchar* szHotKeyDescKey, const wchar* szHotKeyAltDescKey, const wchar* szHotKeyString)
{
	m_szHotKeyDescriptionKey = szHotKeyDescKey;
	m_szHotKeyAltDescriptionKey = szHotKeyAltDescKey;
	m_szHotKeyString = szHotKeyString;
}

//======================================================================================================
//					CvDiplomacyResponse
//======================================================================================================

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvDiplomacyResponse()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvDiplomacyResponse::CvDiplomacyResponse() :
m_iNumDiplomacyText(0),
m_abCivilizationTypes(NULL),
m_abLeaderHeadTypes(NULL),
m_abAttitudeTypes(NULL),
m_abDiplomacyPowerTypes(NULL),
m_paszDiplomacyText(NULL)
{
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvDiplomacyResponse()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvDiplomacyResponse::~CvDiplomacyResponse()
{
	SAFE_DELETE_ARRAY(m_abCivilizationTypes);
	SAFE_DELETE_ARRAY(m_abLeaderHeadTypes);
	SAFE_DELETE_ARRAY(m_abAttitudeTypes);
	SAFE_DELETE_ARRAY(m_abDiplomacyPowerTypes);
	SAFE_DELETE_ARRAY(m_paszDiplomacyText);
}

int CvDiplomacyResponse::getNumDiplomacyText()
{
	return m_iNumDiplomacyText;
}

void CvDiplomacyResponse::setNumDiplomacyText(int i)
{
	m_iNumDiplomacyText = i;
}

bool CvDiplomacyResponse::getCivilizationTypes(int i)
{
	FAssertMsg(i < GC.getNumCivilizationInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abCivilizationTypes[i];
}

bool* CvDiplomacyResponse::getCivilizationTypes() const
{
	return m_abCivilizationTypes;
}

void CvDiplomacyResponse::setCivilizationTypes(int i, bool bVal)
{
	FAssertMsg(i < GC.getNumCivilizationInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	m_abCivilizationTypes[i] = bVal;
}

bool CvDiplomacyResponse::getLeaderHeadTypes(int i)
{
	FAssertMsg(i < GC.getNumLeaderHeadInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abLeaderHeadTypes[i];
}

bool* CvDiplomacyResponse::getLeaderHeadTypes() const
{
	return m_abLeaderHeadTypes;
}

void CvDiplomacyResponse::setLeaderHeadTypes(int i, bool bVal)
{
	FAssertMsg(i < GC.getNumLeaderHeadInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	m_abLeaderHeadTypes[i] = bVal;
}

bool CvDiplomacyResponse::getAttitudeTypes(int i) const
{
	FAssertMsg(i < NUM_ATTITUDE_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abAttitudeTypes[i];
}

bool* CvDiplomacyResponse::getAttitudeTypes() const
{
	return m_abAttitudeTypes;
}

void CvDiplomacyResponse::setAttitudeTypes(int i, bool bVal)
{
	FAssertMsg(i < NUM_ATTITUDE_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	m_abAttitudeTypes[i] = bVal;
}

bool CvDiplomacyResponse::getDiplomacyPowerTypes(int i)
{
	FAssertMsg(i < NUM_DIPLOMACYPOWER_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abDiplomacyPowerTypes[i];
}

bool* CvDiplomacyResponse::getDiplomacyPowerTypes() const
{
	return m_abDiplomacyPowerTypes;
}

void CvDiplomacyResponse::setDiplomacyPowerTypes(int i, bool bVal)
{
	FAssertMsg(i < NUM_DIPLOMACYPOWER_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	m_abDiplomacyPowerTypes[i] = bVal;
}

const char* CvDiplomacyResponse::getDiplomacyText(int i) const
{
	return m_paszDiplomacyText[i];
}

const CvString* CvDiplomacyResponse::getDiplomacyText() const
{
	return m_paszDiplomacyText;
}

void CvDiplomacyResponse::setDiplomacyText(int i, CvString szText)
{
	FAssertMsg(i < getNumDiplomacyText(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	m_paszDiplomacyText[i] = szText;
}

void CvDiplomacyResponse::read(FDataStreamBase* stream)
{
	uint uiFlag=0;
	stream->Read(&uiFlag);		// flag for expansion

	stream->Read(&m_iNumDiplomacyText);

	SAFE_DELETE_ARRAY(m_abCivilizationTypes);
	m_abCivilizationTypes = new bool[GC.getNumCivilizationInfos()];
	stream->Read(GC.getNumCivilizationInfos(), m_abCivilizationTypes);

	SAFE_DELETE_ARRAY(m_abLeaderHeadTypes);
	m_abLeaderHeadTypes = new bool[GC.getNumLeaderHeadInfos()];
	stream->Read(GC.getNumLeaderHeadInfos(), m_abLeaderHeadTypes);

	SAFE_DELETE_ARRAY(m_abAttitudeTypes);
	m_abAttitudeTypes = new bool[NUM_ATTITUDE_TYPES];
	stream->Read(NUM_ATTITUDE_TYPES, m_abAttitudeTypes);

	SAFE_DELETE_ARRAY(m_abDiplomacyPowerTypes);
	m_abDiplomacyPowerTypes = new bool[NUM_DIPLOMACYPOWER_TYPES];
	stream->Read(NUM_DIPLOMACYPOWER_TYPES, m_abDiplomacyPowerTypes);

	SAFE_DELETE_ARRAY(m_paszDiplomacyText);
	m_paszDiplomacyText = new CvString[m_iNumDiplomacyText];
	stream->ReadString(m_iNumDiplomacyText, m_paszDiplomacyText);
}

void CvDiplomacyResponse::write(FDataStreamBase* stream)
{
	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion

	stream->Write(m_iNumDiplomacyText);

	stream->Write(GC.getNumCivilizationInfos(), m_abCivilizationTypes);
	stream->Write(GC.getNumLeaderHeadInfos(), m_abLeaderHeadTypes);
	stream->Write(NUM_ATTITUDE_TYPES, m_abAttitudeTypes);
	stream->Write(NUM_DIPLOMACYPOWER_TYPES, m_abDiplomacyPowerTypes);
	stream->WriteString(m_iNumDiplomacyText, m_paszDiplomacyText);
}

bool CvDiplomacyResponse::read(CvXMLLoadUtility* pXML)
{
	pXML->SetVariableListTagPair(&m_abCivilizationTypes, "Civilizations", GC.getNumCivilizationInfos(), false);
	// Leaders
	pXML->SetVariableListTagPair(&m_abLeaderHeadTypes, "Leaders", GC.getNumLeaderHeadInfos(), false);
	// AttitudeTypes
	pXML->SetVariableListTagPair(&m_abAttitudeTypes, "Attitudes", NUM_ATTITUDE_TYPES, false);
	// PowerTypes
	pXML->SetVariableListTagPair(&m_abDiplomacyPowerTypes, "DiplomacyPowers", NUM_DIPLOMACYPOWER_TYPES, false);
	// DiplomacyText
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"DiplomacyText"))
	{
		pXML->SetStringList(&m_paszDiplomacyText, &m_iNumDiplomacyText);
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	return true;
}

//======================================================================================================
//					CvPromotionInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvPromotionInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvPromotionInfo::CvPromotionInfo() :
m_iPrereqPromotion(NO_PROMOTION),
m_iPrereqOrPromotion1(NO_PROMOTION),
m_iPrereqOrPromotion2(NO_PROMOTION),
m_iVisibilityChange(0),
m_iMovesChange(0),
m_iMoveDiscountChange(0),
m_iWithdrawalChange(0),
m_iCargoChange(0),
m_iBombardRateChange(0),
m_iEnemyHealChange(0),
m_iNeutralHealChange(0),
m_iFriendlyHealChange(0),
m_iSameTileHealChange(0),
m_iAdjacentTileHealChange(0),
m_iCombatPercent(0),
m_iCityAttackPercent(0),
m_iCityDefensePercent(0),
m_iHillsAttackPercent(0),
m_iHillsDefensePercent(0),
m_iCommandType(NO_COMMAND),
m_iPillageChange(0),
m_iUpgradeDiscount(0),
m_iExperiencePercent(0),
m_bLeader(false),
m_bBlitz(false),
m_bAmphib(false),
m_bRiver(false),
m_bEnemyRoute(false),
m_bAlwaysHeal(false),
m_bHillsDoubleMove(false),
m_aiTerrainAttackPercent(NULL),
m_aiTerrainDefensePercent(NULL),
m_aiFeatureAttackPercent(NULL),
m_aiFeatureDefensePercent(NULL),
m_aiUnitClassAttackModifier(NULL),
m_aiUnitClassDefenseModifier(NULL),
m_aiUnitCombatModifierPercent(NULL),
m_aiDomainModifierPercent(NULL),
m_abTerrainDoubleMove(NULL),
m_abFeatureDoubleMove(NULL),
m_abUnitCombat(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvPromotionInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvPromotionInfo::~CvPromotionInfo()
{
	SAFE_DELETE_ARRAY(m_aiTerrainAttackPercent);
	SAFE_DELETE_ARRAY(m_aiTerrainDefensePercent);
	SAFE_DELETE_ARRAY(m_aiFeatureAttackPercent);
	SAFE_DELETE_ARRAY(m_aiFeatureDefensePercent);
	SAFE_DELETE_ARRAY(m_aiUnitClassAttackModifier);
	SAFE_DELETE_ARRAY(m_aiUnitClassDefenseModifier);
	SAFE_DELETE_ARRAY(m_aiUnitCombatModifierPercent);
	SAFE_DELETE_ARRAY(m_aiDomainModifierPercent);
	SAFE_DELETE_ARRAY(m_abTerrainDoubleMove);
	SAFE_DELETE_ARRAY(m_abFeatureDoubleMove);
	SAFE_DELETE_ARRAY(m_abUnitCombat);
}
int CvPromotionInfo::getPrereqPromotion() const
{
	return m_iPrereqPromotion;
}
void CvPromotionInfo::setPrereqPromotion(int i)
{
	m_iPrereqPromotion = i;
}
int CvPromotionInfo::getPrereqOrPromotion1() const
{
	return m_iPrereqOrPromotion1;
}
void CvPromotionInfo::setPrereqOrPromotion1(int i)
{
	m_iPrereqOrPromotion1 = i;
}
int CvPromotionInfo::getPrereqOrPromotion2() const
{
	return m_iPrereqOrPromotion2;
}
void CvPromotionInfo::setPrereqOrPromotion2(int i)
{
	m_iPrereqOrPromotion2 = i;
}
int CvPromotionInfo::getVisibilityChange() const
{
	return m_iVisibilityChange;
}
int CvPromotionInfo::getMovesChange() const
{
	return m_iMovesChange;
}
int CvPromotionInfo::getMoveDiscountChange() const
{
	return m_iMoveDiscountChange;
}
int CvPromotionInfo::getWithdrawalChange() const
{
	return m_iWithdrawalChange;
}
int CvPromotionInfo::getCargoChange() const
{
	return m_iCargoChange;
}
int CvPromotionInfo::getBombardRateChange() const
{
	return m_iBombardRateChange;
}
int CvPromotionInfo::getEnemyHealChange() const
{
	return m_iEnemyHealChange;
}
int CvPromotionInfo::getNeutralHealChange() const
{
	return m_iNeutralHealChange;
}
int CvPromotionInfo::getFriendlyHealChange() const
{
	return m_iFriendlyHealChange;
}
int CvPromotionInfo::getSameTileHealChange() const
{
	return m_iSameTileHealChange;
}
int CvPromotionInfo::getAdjacentTileHealChange() const
{
	return m_iAdjacentTileHealChange;
}
int CvPromotionInfo::getCombatPercent() const
{
	return m_iCombatPercent;
}
int CvPromotionInfo::getCityAttackPercent() const
{
	return m_iCityAttackPercent;
}
int CvPromotionInfo::getCityDefensePercent() const
{
	return m_iCityDefensePercent;
}
int CvPromotionInfo::getHillsAttackPercent() const
{
	return m_iHillsAttackPercent;
}
int CvPromotionInfo::getHillsDefensePercent() const
{
	return m_iHillsDefensePercent;
}
int CvPromotionInfo::getCommandType() const
{
	return m_iCommandType;
}
void CvPromotionInfo::setCommandType(int iNewType)
{
	m_iCommandType = iNewType;
}
int CvPromotionInfo::getPillageChange() const
{
	return m_iPillageChange;
}
int CvPromotionInfo::getUpgradeDiscount() const
{
	return m_iUpgradeDiscount;
}
int CvPromotionInfo::getExperiencePercent() const
{
	return m_iExperiencePercent;
}
bool CvPromotionInfo::isLeader() const
{
	return m_bLeader;
}
bool CvPromotionInfo::isBlitz() const
{
	return m_bBlitz;
}
bool CvPromotionInfo::isAmphib() const
{
	return m_bAmphib;
}
bool CvPromotionInfo::isRiver() const
{
	return m_bRiver;
}
bool CvPromotionInfo::isEnemyRoute() const
{
	return m_bEnemyRoute;
}
bool CvPromotionInfo::isAlwaysHeal() const
{
	return m_bAlwaysHeal;
}
bool CvPromotionInfo::isHillsDoubleMove() const
{
	return m_bHillsDoubleMove;
}
const char* CvPromotionInfo::getSound() const
{
	return m_szSound;
}
void CvPromotionInfo::setSound(const char* szVal)
{
	m_szSound = szVal;
}
// Arrays
int CvPromotionInfo::getTerrainAttackPercent(int i) const
{
	FAssertMsg(i < GC.getNumTerrainInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiTerrainAttackPercent ? m_aiTerrainAttackPercent[i] : -1;
}
int CvPromotionInfo::getTerrainDefensePercent(int i) const
{
	FAssertMsg(i < GC.getNumTerrainInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiTerrainDefensePercent ? m_aiTerrainDefensePercent[i] : -1;
}
int CvPromotionInfo::getFeatureAttackPercent(int i) const
{
	FAssertMsg(i < GC.getNumFeatureInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiFeatureAttackPercent ? m_aiFeatureAttackPercent[i] : -1;
}
int CvPromotionInfo::getFeatureDefensePercent(int i) const
{
	FAssertMsg(i < GC.getNumFeatureInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiFeatureDefensePercent ? m_aiFeatureDefensePercent[i] : -1;
}
int CvPromotionInfo::getUnitClassAttackModifier(int i) const
{
	FAssertMsg(i < GC.getNumUnitClassInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiUnitClassAttackModifier ? m_aiUnitClassAttackModifier[i] : -1;
}
int CvPromotionInfo::getUnitClassDefenseModifier(int i) const
{
	FAssertMsg(i < GC.getNumUnitClassInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiUnitClassDefenseModifier ? m_aiUnitClassDefenseModifier[i] : -1;
}
int CvPromotionInfo::getUnitCombatModifierPercent(int i) const
{
	FAssertMsg(i < GC.getNumUnitCombatInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiUnitCombatModifierPercent ? m_aiUnitCombatModifierPercent[i] : -1;
}
int CvPromotionInfo::getDomainModifierPercent(int i) const
{
	FAssertMsg(i < NUM_DOMAIN_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiDomainModifierPercent ? m_aiDomainModifierPercent[i] : -1;
}
bool CvPromotionInfo::getTerrainDoubleMove(int i) const
{
	FAssertMsg(i < GC.getNumTerrainInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abTerrainDoubleMove ? m_abTerrainDoubleMove[i] : false;
}
bool CvPromotionInfo::getFeatureDoubleMove(int i) const
{
	FAssertMsg(i < GC.getNumFeatureInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abFeatureDoubleMove ? m_abFeatureDoubleMove[i] : false;
}
bool CvPromotionInfo::getUnitCombat(int i) const
{
	FAssertMsg(i < GC.getNumUnitCombatInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abUnitCombat ? m_abUnitCombat[i] : false;
}

void CvPromotionInfo::read(FDataStreamBase* stream)
{
	CvHotkeyInfo::read(stream);

	uint uiFlag=0;
	stream->Read(&uiFlag);		// flag for expansion
	stream->Read(&m_iPrereqPromotion);
	stream->Read(&m_iPrereqOrPromotion1);
	stream->Read(&m_iPrereqOrPromotion2);

	stream->Read(&m_iVisibilityChange);
	stream->Read(&m_iMovesChange);
	stream->Read(&m_iMoveDiscountChange);
	stream->Read(&m_iWithdrawalChange);
	stream->Read(&m_iCargoChange);
	stream->Read(&m_iBombardRateChange);
	stream->Read(&m_iEnemyHealChange);
	stream->Read(&m_iNeutralHealChange);
	stream->Read(&m_iFriendlyHealChange);
	stream->Read(&m_iSameTileHealChange);
	stream->Read(&m_iAdjacentTileHealChange);
	stream->Read(&m_iCombatPercent);
	stream->Read(&m_iCityAttackPercent);
	stream->Read(&m_iCityDefensePercent);
	stream->Read(&m_iHillsAttackPercent);
	stream->Read(&m_iHillsDefensePercent);
	stream->Read(&m_iCommandType);
	stream->Read(&m_iPillageChange);
	stream->Read(&m_iUpgradeDiscount);
	stream->Read(&m_iExperiencePercent);

	stream->Read(&m_bLeader);
	stream->Read(&m_bBlitz);
	stream->Read(&m_bAmphib);
	stream->Read(&m_bRiver);
	stream->Read(&m_bEnemyRoute);
	stream->Read(&m_bAlwaysHeal);
	stream->Read(&m_bHillsDoubleMove);

	stream->ReadString(m_szSound);

	// Arrays

	SAFE_DELETE_ARRAY(m_aiTerrainAttackPercent);
	m_aiTerrainAttackPercent = new int[GC.getNumTerrainInfos()];
	stream->Read(GC.getNumTerrainInfos(), m_aiTerrainAttackPercent);
	SAFE_DELETE_ARRAY(m_aiTerrainDefensePercent);
	m_aiTerrainDefensePercent = new int[GC.getNumTerrainInfos()];
	stream->Read(GC.getNumTerrainInfos(), m_aiTerrainDefensePercent);
	SAFE_DELETE_ARRAY(m_aiFeatureAttackPercent);
	m_aiFeatureAttackPercent = new int[GC.getNumFeatureInfos()];
	stream->Read(GC.getNumFeatureInfos(), m_aiFeatureAttackPercent);
	SAFE_DELETE_ARRAY(m_aiFeatureDefensePercent);
	m_aiFeatureDefensePercent = new int[GC.getNumFeatureInfos()];
	stream->Read(GC.getNumFeatureInfos(), m_aiFeatureDefensePercent);
	SAFE_DELETE_ARRAY(m_aiUnitClassAttackModifier);
	m_aiUnitClassAttackModifier = new int[GC.getNumUnitClassInfos()];
	stream->Read(GC.getNumUnitClassInfos(), m_aiUnitClassAttackModifier);
	SAFE_DELETE_ARRAY(m_aiUnitClassDefenseModifier);
	m_aiUnitClassDefenseModifier = new int[GC.getNumUnitClassInfos()];
	stream->Read(GC.getNumUnitClassInfos(), m_aiUnitClassDefenseModifier);
	SAFE_DELETE_ARRAY(m_aiUnitCombatModifierPercent);
	m_aiUnitCombatModifierPercent = new int[GC.getNumUnitCombatInfos()];
	stream->Read(GC.getNumUnitCombatInfos(), m_aiUnitCombatModifierPercent);
	SAFE_DELETE_ARRAY(m_aiDomainModifierPercent);
	m_aiDomainModifierPercent = new int[NUM_DOMAIN_TYPES];
	stream->Read(NUM_DOMAIN_TYPES, m_aiDomainModifierPercent);
	SAFE_DELETE_ARRAY(m_abTerrainDoubleMove);
	m_abTerrainDoubleMove = new bool[GC.getNumTerrainInfos()];
	stream->Read(GC.getNumTerrainInfos(), m_abTerrainDoubleMove);
	SAFE_DELETE_ARRAY(m_abFeatureDoubleMove);
	m_abFeatureDoubleMove = new bool[GC.getNumFeatureInfos()];
	stream->Read(GC.getNumFeatureInfos(), m_abFeatureDoubleMove);
	SAFE_DELETE_ARRAY(m_abUnitCombat);
	m_abUnitCombat = new bool[GC.getNumUnitCombatInfos()];
	stream->Read(GC.getNumUnitCombatInfos(), m_abUnitCombat);
}
void CvPromotionInfo::write(FDataStreamBase* stream)
{
	CvHotkeyInfo::write(stream);
	uint uiFlag = 0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_iPrereqPromotion);
	stream->Write(m_iPrereqOrPromotion1);
	stream->Write(m_iPrereqOrPromotion2);

	stream->Write(m_iVisibilityChange);
	stream->Write(m_iMovesChange);
	stream->Write(m_iMoveDiscountChange);
	stream->Write(m_iWithdrawalChange);
	stream->Write(m_iCargoChange);
	stream->Write(m_iBombardRateChange);
	stream->Write(m_iEnemyHealChange);
	stream->Write(m_iNeutralHealChange);
	stream->Write(m_iFriendlyHealChange);
	stream->Write(m_iSameTileHealChange);
	stream->Write(m_iAdjacentTileHealChange);
	stream->Write(m_iCombatPercent);
	stream->Write(m_iCityAttackPercent);
	stream->Write(m_iCityDefensePercent);
	stream->Write(m_iHillsAttackPercent);
	stream->Write(m_iHillsDefensePercent);
	stream->Write(m_iCommandType);
	stream->Write(m_iPillageChange);
	stream->Write(m_iUpgradeDiscount);
	stream->Write(m_iExperiencePercent);
	stream->Write(m_bLeader);
	stream->Write(m_bBlitz);
	stream->Write(m_bAmphib);
	stream->Write(m_bRiver);
	stream->Write(m_bEnemyRoute);
	stream->Write(m_bAlwaysHeal);
	stream->Write(m_bHillsDoubleMove);
	stream->WriteString(m_szSound);
	// Arrays
	stream->Write(GC.getNumTerrainInfos(), m_aiTerrainAttackPercent);
	stream->Write(GC.getNumTerrainInfos(), m_aiTerrainDefensePercent);
	stream->Write(GC.getNumFeatureInfos(), m_aiFeatureAttackPercent);
	stream->Write(GC.getNumFeatureInfos(), m_aiFeatureDefensePercent);
	stream->Write(GC.getNumUnitClassInfos(), m_aiUnitClassAttackModifier);
	stream->Write(GC.getNumUnitClassInfos(), m_aiUnitClassDefenseModifier);
	stream->Write(GC.getNumUnitCombatInfos(), m_aiUnitCombatModifierPercent);
	stream->Write(NUM_DOMAIN_TYPES, m_aiDomainModifierPercent);
	stream->Write(GC.getNumTerrainInfos(), m_abTerrainDoubleMove);
	stream->Write(GC.getNumFeatureInfos(), m_abFeatureDoubleMove);
	stream->Write(GC.getNumUnitCombatInfos(), m_abUnitCombat);
}
bool CvPromotionInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvHotkeyInfo::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "Sound");
	setSound(szTextVal);
	pXML->GetChildXmlValByName(&m_bLeader, "bLeader");
	pXML->GetChildXmlValByName(&m_bBlitz, "bBlitz");
	pXML->GetChildXmlValByName(&m_bAmphib, "bAmphib");
	pXML->GetChildXmlValByName(&m_bRiver, "bRiver");
	pXML->GetChildXmlValByName(&m_bEnemyRoute, "bEnemyRoute");
	pXML->GetChildXmlValByName(&m_bAlwaysHeal, "bAlwaysHeal");
	pXML->GetChildXmlValByName(&m_bHillsDoubleMove, "bHillsDoubleMove");
	pXML->GetChildXmlValByName(&m_iVisibilityChange, "iVisibilityChange");
	pXML->GetChildXmlValByName(&m_iMovesChange, "iMovesChange");
	pXML->GetChildXmlValByName(&m_iMoveDiscountChange, "iMoveDiscountChange");
	pXML->GetChildXmlValByName(&m_iWithdrawalChange, "iWithdrawalChange");
	pXML->GetChildXmlValByName(&m_iCargoChange, "iCargoChange");
	pXML->GetChildXmlValByName(&m_iBombardRateChange, "iBombardRateChange");
	pXML->GetChildXmlValByName(&m_iEnemyHealChange, "iEnemyHealChange");
	pXML->GetChildXmlValByName(&m_iNeutralHealChange, "iNeutralHealChange");
	pXML->GetChildXmlValByName(&m_iFriendlyHealChange, "iFriendlyHealChange");
	pXML->GetChildXmlValByName(&m_iSameTileHealChange, "iSameTileHealChange");
	pXML->GetChildXmlValByName(&m_iAdjacentTileHealChange, "iAdjacentTileHealChange");
	pXML->GetChildXmlValByName(&m_iCombatPercent, "iCombatPercent");
	pXML->GetChildXmlValByName(&m_iCityAttackPercent, "iCityAttack");
	pXML->GetChildXmlValByName(&m_iCityDefensePercent, "iCityDefense");
	pXML->GetChildXmlValByName(&m_iHillsAttackPercent, "iHillsAttack");
	pXML->GetChildXmlValByName(&m_iHillsDefensePercent, "iHillsDefense");
	pXML->GetChildXmlValByName(&m_iPillageChange, "iPillageChange");
	pXML->GetChildXmlValByName(&m_iUpgradeDiscount, "iUpgradeDiscount");
	pXML->GetChildXmlValByName(&m_iExperiencePercent, "iExperiencePercent");
	pXML->SetVariableListTagPair(&m_aiTerrainAttackPercent, "TerrainAttacks", GC.getNumTerrainInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiTerrainDefensePercent, "TerrainDefenses", GC.getNumTerrainInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiFeatureAttackPercent, "FeatureAttacks", GC.getNumFeatureInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiFeatureDefensePercent, "FeatureDefenses", GC.getNumFeatureInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiUnitClassAttackModifier, "UnitClassAttackMods", GC.getNumUnitClassInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiUnitClassDefenseModifier, "UnitClassDefenseMods", GC.getNumUnitClassInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiUnitCombatModifierPercent, "UnitCombatMods", GC.getNumUnitCombatInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiDomainModifierPercent, "DomainMods", NUM_DOMAIN_TYPES, 0);
	pXML->SetVariableListTagPair(&m_abTerrainDoubleMove, "TerrainDoubleMoves", GC.getNumTerrainInfos(), false);
	pXML->SetVariableListTagPair(&m_abFeatureDoubleMove, "FeatureDoubleMoves", GC.getNumFeatureInfos(), false);
	pXML->SetVariableListTagPair(&m_abUnitCombat, "UnitCombats", GC.getNumUnitCombatInfos(), false);
	return true;
}
bool CvPromotionInfo::readPass2(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "PromotionPrereq");
	m_iPrereqPromotion = GC.getInfoTypeForString(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "PromotionPrereqOr1");
	m_iPrereqOrPromotion1 = GC.getInfoTypeForString(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "PromotionPrereqOr2");
	m_iPrereqOrPromotion2 = GC.getInfoTypeForString(szTextVal);
	return true;
}

//======================================================================================================
//					CvProfessionInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvProfessionInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvProfessionInfo::CvProfessionInfo() :
	m_iUnitCombatType(NO_UNITCOMBAT),
	m_iYieldProduced(NO_YIELD),
	m_iYieldConsumed(NO_YIELD),
	m_iSpecialBuilding(NO_SPECIALBUILDING),
	m_iCombatChange(0),
	m_iMovesChange(0),
	m_iWorkRate(0),
	m_iMissionaryRate(0),
	m_iPowerValue(0),
	m_iAssetValue(0),
	m_bWorkPlot(false),
	m_bCitizen(false),
	m_bWater(false),
	m_bScout(false),
	m_bCityDefender(false),
	m_bCanFound(false),
	m_bUnarmed(false),
	m_bNoDefensiveBonus(false),
	m_abFreePromotions(NULL),
	m_iDefaultUnitAIType(NO_UNITAI)
{
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvProfessionInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvProfessionInfo::~CvProfessionInfo()
{
	SAFE_DELETE_ARRAY(m_abFreePromotions);
}
int CvProfessionInfo::getUnitCombatType() const
{
	return m_iUnitCombatType;
}
int CvProfessionInfo::getYieldProduced() const
{
	return m_iYieldProduced;
}
int CvProfessionInfo::getYieldConsumed() const
{
	return m_iYieldConsumed;
}
int CvProfessionInfo::getSpecialBuilding() const
{
	return m_iSpecialBuilding;
}
int CvProfessionInfo::getCombatChange() const
{
	return m_iCombatChange;
}
int CvProfessionInfo::getMovesChange() const
{
	return m_iMovesChange;
}
int CvProfessionInfo::getWorkRate() const
{
	return m_iWorkRate;
}
int CvProfessionInfo::getMissionaryRate() const
{
	return m_iMissionaryRate;
}
int CvProfessionInfo::getPowerValue() const
{
	return m_iPowerValue;
}
int CvProfessionInfo::getAssetValue() const
{
	return m_iAssetValue;
}
bool CvProfessionInfo::isWorkPlot() const
{
	return m_bWorkPlot;
}
bool CvProfessionInfo::isCitizen() const
{
	return m_bCitizen;
}
bool CvProfessionInfo::isWater() const
{
	return m_bWater;
}
bool CvProfessionInfo::isScout() const
{
	return m_bScout;
}
bool CvProfessionInfo::isCityDefender() const
{
	return m_bCityDefender;
}
bool CvProfessionInfo::canFound() const
{
	return m_bCanFound;
}
bool CvProfessionInfo::isUnarmed() const
{
	return m_bUnarmed;
}
bool CvProfessionInfo::isNoDefensiveBonus() const
{
	return m_bNoDefensiveBonus;
}
int CvProfessionInfo::getYieldEquipmentAmount(int iYield) const
{
	for (uint i = 0; i < m_aYieldEquipments.size(); ++i)
	{
		const YieldEquipment& kYieldEquipment = m_aYieldEquipments[i];
		if (kYieldEquipment.iYieldType == iYield)
		{
			return kYieldEquipment.iYieldAmount;
		}
	}
	return 0;
}

bool CvProfessionInfo::isFreePromotion(int i) const
{
	FAssertMsg(i < GC.getNumPromotionInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abFreePromotions ? m_abFreePromotions[i] : false;
}

int CvProfessionInfo::getDefaultUnitAIType() const
{
    return m_iDefaultUnitAIType;
}

void CvProfessionInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);		// flag for expansion
	stream->Read(&m_iUnitCombatType);
	stream->Read(&m_iDefaultUnitAIType);
	stream->Read(&m_iYieldProduced);
	stream->Read(&m_iYieldConsumed);
	stream->Read(&m_iSpecialBuilding);
	stream->Read(&m_iCombatChange);
	stream->Read(&m_iMovesChange);
	stream->Read(&m_iWorkRate);
	stream->Read(&m_iMissionaryRate);
	stream->Read(&m_iPowerValue);
	stream->Read(&m_iAssetValue);
	stream->Read(&m_bWorkPlot);
	stream->Read(&m_bCitizen);
	stream->Read(&m_bWater);
	stream->Read(&m_bScout);
	stream->Read(&m_bCityDefender);
	stream->Read(&m_bCanFound);
	stream->Read(&m_bUnarmed);
	stream->Read(&m_bNoDefensiveBonus);
	m_aYieldEquipments.clear();
	int iYieldEquipmentSize = 0;
	stream->Read(&iYieldEquipmentSize);
	for(int i=0;i<iYieldEquipmentSize;i++)
	{
		YieldEquipment kEquipment;
		stream->Read(&kEquipment.iYieldType);
		stream->Read(&kEquipment.iYieldAmount);
		m_aYieldEquipments.push_back(kEquipment);
	}

	SAFE_DELETE_ARRAY(m_abFreePromotions);
	m_abFreePromotions = new bool[GC.getNumPromotionInfos()];
	stream->Read(GC.getNumPromotionInfos(), m_abFreePromotions);
}
void CvProfessionInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);
	uint uiFlag = 0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_iUnitCombatType);
	stream->Write(m_iDefaultUnitAIType);
	stream->Write(m_iYieldProduced);
	stream->Write(m_iYieldConsumed);
	stream->Write(m_iSpecialBuilding);
	stream->Write(m_iCombatChange);
	stream->Write(m_iMovesChange);
	stream->Write(m_iWorkRate);
	stream->Write(m_iMissionaryRate);
	stream->Write(m_iPowerValue);
	stream->Write(m_iAssetValue);
	stream->Write(m_bWorkPlot);
	stream->Write(m_bCitizen);
	stream->Write(m_bWater);
	stream->Write(m_bScout);
	stream->Write(m_bCityDefender);
	stream->Write(m_bCanFound);
	stream->Write(m_bUnarmed);
	stream->Write(m_bNoDefensiveBonus);
	stream->Write((int)m_aYieldEquipments.size());
	for(int i=0;i<(int)m_aYieldEquipments.size();i++)
	{
		stream->Write(m_aYieldEquipments[i].iYieldType);
		stream->Write(m_aYieldEquipments[i].iYieldAmount);
	}
	stream->Write(GC.getNumPromotionInfos(), m_abFreePromotions);
}
bool CvProfessionInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "Combat");
	m_iUnitCombatType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "DefaultUnitAI");
	m_iDefaultUnitAIType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "YieldProduced");
	m_iYieldProduced = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "YieldConsumed");
	m_iYieldConsumed = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "SpecialBuilding");
	m_aszExtraXMLforPass3.push_back(szTextVal);
	pXML->GetChildXmlValByName(&m_iCombatChange, "iCombatChange");
	pXML->GetChildXmlValByName(&m_iMovesChange, "iMovesChange");
	pXML->GetChildXmlValByName(&m_iWorkRate, "iWorkRate");
	pXML->GetChildXmlValByName(&m_iMissionaryRate, "iMissionaryRate");
	pXML->GetChildXmlValByName(&m_iPowerValue, "iPower");
	pXML->GetChildXmlValByName(&m_iAssetValue, "iAsset");
	pXML->GetChildXmlValByName(&m_bWorkPlot, "bWorkPlot");
	pXML->GetChildXmlValByName(&m_bCitizen, "bCitizen");
	pXML->GetChildXmlValByName(&m_bWater, "bWater");
	pXML->GetChildXmlValByName(&m_bScout, "bScout");
	pXML->GetChildXmlValByName(&m_bCityDefender, "bCityDefender");
	pXML->GetChildXmlValByName(&m_bCanFound, "bCanFound");
	pXML->GetChildXmlValByName(&m_bUnarmed, "bUnarmed");
	pXML->GetChildXmlValByName(&m_bNoDefensiveBonus, "bNoDefensiveBonus");
	m_aYieldEquipments.clear();
	int *aiYieldAmounts;
	pXML->SetVariableListTagPair(&aiYieldAmounts, "YieldEquipedNums", NUM_YIELD_TYPES, 0);
	for (int i = 0; i < NUM_YIELD_TYPES; ++i)
	{
		if (aiYieldAmounts[i] != 0)
		{
			YieldEquipment kYieldEquipment;
			kYieldEquipment.iYieldType = i;
			kYieldEquipment.iYieldAmount = aiYieldAmounts[i];
			m_aYieldEquipments.push_back(kYieldEquipment);
		}
	}
	SAFE_DELETE_ARRAY(aiYieldAmounts);
	pXML->SetVariableListTagPair(&m_abFreePromotions, "FreePromotions", GC.getNumPromotionInfos(), false);
	return true;
}

bool CvProfessionInfo::readPass3()
{
	if (m_aszExtraXMLforPass3.size() < 1)
	{
		FAssert(false);
		return false;
	}
	m_iSpecialBuilding = GC.getInfoTypeForString(m_aszExtraXMLforPass3[0]);
	m_aszExtraXMLforPass3.clear();
	return true;
}

//======================================================================================================
//					CvMissionInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvMissionInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvMissionInfo::CvMissionInfo() :
m_iTime(0),
m_bSound(false),
m_bTarget(false),
m_bBuild(false),
m_bVisible(false),
m_eEntityEvent(ENTITY_EVENT_NONE)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvMissionInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvMissionInfo::~CvMissionInfo()
{
}
int CvMissionInfo::getTime() const
{
	return m_iTime;
}
bool CvMissionInfo::isSound() const
{
	return m_bSound;
}
bool CvMissionInfo::isTarget() const
{
	return m_bTarget;
}
bool CvMissionInfo::isBuild() const
{
	return m_bBuild;
}
bool CvMissionInfo::getVisible() const
{
	return m_bVisible;
}
const char* CvMissionInfo::getWaypoint() const
{
	return m_szWaypoint;
}
EntityEventTypes CvMissionInfo::getEntityEvent() const
{
	return m_eEntityEvent;
}
bool CvMissionInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTmp;
	if (!CvHotkeyInfo::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(m_szWaypoint, "Waypoint");
	pXML->GetChildXmlValByName(&m_iTime, "iTime");
	pXML->GetChildXmlValByName(&m_bSound, "bSound");
	pXML->GetChildXmlValByName(&m_bTarget, "bTarget");
	pXML->GetChildXmlValByName(&m_bBuild, "bBuild");
	pXML->GetChildXmlValByName(&m_bVisible, "bVisible");
	if ( pXML->GetChildXmlValByName(szTmp, "EntityEventType") )
	{
		m_eEntityEvent = (EntityEventTypes)pXML->FindInInfoClass(szTmp);
	}
	else
	{
		m_eEntityEvent = ENTITY_EVENT_NONE;
	}
	return true;
}

//======================================================================================================
//					CvControlInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvControlInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvControlInfo::CvControlInfo()
{
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvControlInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvControlInfo::~CvControlInfo()
{
}
bool CvControlInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvHotkeyInfo::read(pXML))
	{
		return false;
	}
	return true;
}

//======================================================================================================
//					CvCommandInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvCommandInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvCommandInfo::CvCommandInfo() :
m_bConfirmCommand(false),
m_bVisible(false),
m_bAll(false)
{
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvCommandInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvCommandInfo::~CvCommandInfo()
{
}
bool CvCommandInfo::getConfirmCommand() const
{
	return m_bConfirmCommand;
}
bool CvCommandInfo::getVisible() const
{
	return m_bVisible;
}
bool CvCommandInfo::getAll() const
{
	return m_bAll;
}
bool CvCommandInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvHotkeyInfo::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bConfirmCommand, "bConfirmCommand");
	pXML->GetChildXmlValByName(&m_bVisible, "bVisible");
	pXML->GetChildXmlValByName(&m_bAll, "bAll");
	return true;
}
//======================================================================================================
//					CvAutomateInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvAutomateInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvAutomateInfo::CvAutomateInfo() :
m_iCommand(NO_COMMAND),
m_iAutomate(NO_AUTOMATE),
m_bConfirmCommand(false),
m_bVisible(false)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvAutomateInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvAutomateInfo::~CvAutomateInfo()
{
}
int CvAutomateInfo::getCommand() const
{
	return m_iCommand;
}
void CvAutomateInfo::setCommand(int i)
{
	m_iCommand = i;
}
int CvAutomateInfo::getAutomate() const
{
	return m_iAutomate;
}
void CvAutomateInfo::setAutomate(int i)
{
	m_iAutomate = i;
}
bool CvAutomateInfo::getConfirmCommand() const
{
	return m_bConfirmCommand;
}
bool CvAutomateInfo::getVisible() const
{
	return m_bVisible;
}
bool CvAutomateInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvHotkeyInfo::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "Command");
	setCommand(pXML->FindInInfoClass(szTextVal));
	pXML->GetChildXmlValByName(szTextVal, "Automate");
	setAutomate(GC.getInfoTypeForString(szTextVal));
	pXML->GetChildXmlValByName(&m_bConfirmCommand, "bConfirmCommand");
	pXML->GetChildXmlValByName(&m_bVisible, "bVisible");
	return true;
}
//======================================================================================================
//					CvActionInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvActionInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvActionInfo::CvActionInfo() :
m_iOriginalIndex(-1),
m_eSubType(NO_ACTIONSUBTYPE)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvActionInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvActionInfo::~CvActionInfo()
{
}
int CvActionInfo::getMissionData() const
{
	if	(ACTIONSUBTYPE_BUILD == m_eSubType)
	{
		return m_iOriginalIndex;
	}
	return -1;
}
int CvActionInfo::getCommandData() const
{
	int iData = -1;
	switch (m_eSubType)
	{
	case ACTIONSUBTYPE_PROMOTION:
	case ACTIONSUBTYPE_UNIT:
		iData = m_iOriginalIndex;
		break;
	case ACTIONSUBTYPE_COMMAND:
		if (m_iOriginalIndex == COMMAND_SAIL_TO_EUROPE)
		{
			iData = UNIT_TRAVEL_STATE_TO_EUROPE;
		}
		break;
	case ACTIONSUBTYPE_AUTOMATE:
		iData = GC.getAutomateInfo(m_iOriginalIndex).getAutomate();
		break;
	default:
		break;
	}
	return iData;
}
int CvActionInfo::getAutomateType() const
{
	if (ACTIONSUBTYPE_AUTOMATE == m_eSubType)
	{
		return GC.getAutomateInfo(m_iOriginalIndex).getAutomate();
	}
	return NO_AUTOMATE;
}
int CvActionInfo::getInterfaceModeType() const
{
	if (ACTIONSUBTYPE_INTERFACEMODE == m_eSubType)
	{
		return m_iOriginalIndex;
	}
	return NO_INTERFACEMODE;
}
int CvActionInfo::getMissionType() const
{
	if (ACTIONSUBTYPE_BUILD == m_eSubType)
	{
		return GC.getBuildInfo((BuildTypes)m_iOriginalIndex).getMissionType();
	}
	else if (ACTIONSUBTYPE_MISSION == m_eSubType)
	{
		return m_iOriginalIndex;
	}
	return NO_MISSION;
}
int CvActionInfo::getCommandType() const
{
	if (ACTIONSUBTYPE_COMMAND == m_eSubType)
	{
		return m_iOriginalIndex;
	}
	else if (ACTIONSUBTYPE_PROMOTION == m_eSubType)
	{
		return GC.getPromotionInfo((PromotionTypes)m_iOriginalIndex).getCommandType();
	}
	else if (ACTIONSUBTYPE_UNIT == m_eSubType)
	{
		return GC.getUnitInfo((UnitTypes)m_iOriginalIndex).getCommandType();
	}
	else if (ACTIONSUBTYPE_AUTOMATE == m_eSubType)
	{
		return GC.getAutomateInfo(m_iOriginalIndex).getCommand();
	}
	return NO_COMMAND;
}
int CvActionInfo::getControlType() const
{
	if (ACTIONSUBTYPE_CONTROL == m_eSubType)
	{
		return m_iOriginalIndex;
	}
	return -1;
}
int CvActionInfo::getOriginalIndex() const
{
	return m_iOriginalIndex;
}
void CvActionInfo::setOriginalIndex(int i)
{
	m_iOriginalIndex = i;
}
bool CvActionInfo::isConfirmCommand() const
{
	if	(ACTIONSUBTYPE_COMMAND == m_eSubType)
	{
		return GC.getCommandInfo((CommandTypes)m_iOriginalIndex).getConfirmCommand();
	}
	else if (ACTIONSUBTYPE_AUTOMATE == m_eSubType)
	{
		return GC.getAutomateInfo(m_iOriginalIndex).getConfirmCommand();
	}
	return false;
}
bool CvActionInfo::isVisible() const
{
	if (ACTIONSUBTYPE_CONTROL == m_eSubType)
	{
		return false;
	}
	else if	(ACTIONSUBTYPE_COMMAND == m_eSubType)
	{
		return GC.getCommandInfo((CommandTypes)m_iOriginalIndex).getVisible();
	}
	else if (ACTIONSUBTYPE_AUTOMATE == m_eSubType)
	{
		return GC.getAutomateInfo(m_iOriginalIndex).getVisible();
	}
	else if (ACTIONSUBTYPE_MISSION == m_eSubType)
	{
		return GC.getMissionInfo((MissionTypes)m_iOriginalIndex).getVisible();
	}
	else if (ACTIONSUBTYPE_INTERFACEMODE== m_eSubType)
	{
		return GC.getInterfaceModeInfo((InterfaceModeTypes)m_iOriginalIndex).getVisible();
	}
	else if (ACTIONSUBTYPE_PROMOTION == m_eSubType)
	{
		return false;
	}
	return true;
}
ActionSubTypes CvActionInfo::getSubType() const
{
	return m_eSubType;
}
void CvActionInfo::setSubType(ActionSubTypes eSubType)
{
	m_eSubType = eSubType;
}
CvHotkeyInfo* CvActionInfo::getHotkeyInfo() const
{
	switch (getSubType())
	{
		case ACTIONSUBTYPE_INTERFACEMODE:
			return &GC.getInterfaceModeInfo((InterfaceModeTypes)getOriginalIndex());
			break;
		case ACTIONSUBTYPE_COMMAND:
			return &GC.getCommandInfo((CommandTypes)getOriginalIndex());
			break;
		case ACTIONSUBTYPE_BUILD:
			return &GC.getBuildInfo((BuildTypes)getOriginalIndex());
			break;
		case ACTIONSUBTYPE_PROMOTION:
			return &GC.getPromotionInfo((PromotionTypes)getOriginalIndex());
			break;
		case ACTIONSUBTYPE_UNIT:
			return &GC.getUnitInfo((UnitTypes)getOriginalIndex());
			break;
		case ACTIONSUBTYPE_CONTROL:
			return &GC.getControlInfo((ControlTypes)getOriginalIndex());
			break;
		case ACTIONSUBTYPE_AUTOMATE:
			return &GC.getAutomateInfo(getOriginalIndex());
			break;
		case ACTIONSUBTYPE_MISSION:
			return &GC.getMissionInfo((MissionTypes)getOriginalIndex());
			break;
	}
	FAssertMsg((0) ,"Unknown Action Subtype in CvActionInfo::getHotkeyInfo");
	return NULL;
}
const char* CvActionInfo::getType() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getType();
	}
	return NULL;
}
const wchar* CvActionInfo::getDescription() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getDescription();
	}
	return L"";
}
const wchar* CvActionInfo::getCivilopedia() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getCivilopedia();
	}
	return L"";
}
const wchar* CvActionInfo::getHelp() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getHelp();
	}
	return L"";
}
const wchar* CvActionInfo::getStrategy() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getStrategy();
	}
	return L"";
}
const char* CvActionInfo::getButton() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getButton();
	}
	return NULL;
}
const wchar* CvActionInfo::getTextKeyWide() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getTextKeyWide();
	}
	return NULL;
}
int CvActionInfo::getActionInfoIndex() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getActionInfoIndex();
	}
	return -1;
}
int CvActionInfo::getHotKeyVal() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getHotKeyVal();
	}
	return -1;
}
int CvActionInfo::getHotKeyPriority() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getHotKeyPriority();
	}
	return -1;
}
int CvActionInfo::getHotKeyValAlt() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getHotKeyValAlt();
	}
	return -1;
}
int CvActionInfo::getHotKeyPriorityAlt() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getHotKeyPriorityAlt();
	}
	return -1;
}
int CvActionInfo::getOrderPriority() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getOrderPriority();
	}
	return -1;
}
bool CvActionInfo::isAltDown() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->isAltDown();
	}
	return false;
}
bool CvActionInfo::isShiftDown() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->isShiftDown();
	}
	return false;
}
bool CvActionInfo::isCtrlDown() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->isCtrlDown();
	}
	return false;
}
bool CvActionInfo::isAltDownAlt() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->isAltDownAlt();
	}
	return false;
}
bool CvActionInfo::isShiftDownAlt() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->isShiftDownAlt();
	}
	return false;
}
bool CvActionInfo::isCtrlDownAlt() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->isCtrlDownAlt();
	}
	return false;
}
const char* CvActionInfo::getHotKey() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getHotKey();
	}
	return NULL;
}
std::wstring CvActionInfo::getHotKeyDescription() const
{
	if (getHotkeyInfo())
	{
		return getHotkeyInfo()->getHotKeyDescription();
	}
	return L"";
}
//======================================================================================================
//					CvUnitInfo
//======================================================================================================
CvUnitMeshGroup::CvUnitMeshGroup() :
	m_iNumRequired(0)
{
}
CvUnitMeshGroup::CvUnitMeshGroup(int iNumRequired, const CvString &szArtDefineTag) :
	m_iNumRequired(iNumRequired),
	m_szArtDefineTag(szArtDefineTag)
{
}
CvUnitMeshGroup::~CvUnitMeshGroup()
{
}
int CvUnitMeshGroup::getNumRequired() const
{
	return m_iNumRequired;
}
const CvString& CvUnitMeshGroup::getArtDefineTag() const
{
	return m_szArtDefineTag;
}
void CvUnitMeshGroup::read(FDataStreamBase* stream)
{
	stream->Read(&m_iNumRequired);
	stream->ReadString(m_szArtDefineTag);
}
void CvUnitMeshGroup::write(FDataStreamBase* stream)
{
	stream->Write(m_iNumRequired);
	stream->WriteString(m_szArtDefineTag);
}

CvUnitMeshGroups::CvUnitMeshGroups() :
	m_eProfession(NO_PROFESSION),
	m_iMeleeWaveSize(0),
	m_iRangedWaveSize(0),
	m_fMaxSpeed(0),
	m_fPadTime(0)
{
}
CvUnitMeshGroups::CvUnitMeshGroups(ProfessionTypes eProfession, int iMeleeWaveSize, int iRangedWaveSize, float fMaxSpeed, float fPadTime) :
	m_eProfession(eProfession),
	m_iMeleeWaveSize(iMeleeWaveSize),
	m_iRangedWaveSize(iRangedWaveSize),
	m_fMaxSpeed(fMaxSpeed),
	m_fPadTime(fPadTime)
{
}
CvUnitMeshGroups::~CvUnitMeshGroups()
{
}
void CvUnitMeshGroups::addMeshGroup(const CvUnitMeshGroup& kMeshGroup)
{
	m_aMeshGroups.push_back(kMeshGroup);
}
ProfessionTypes CvUnitMeshGroups::getProfession() const
{
	return m_eProfession;
}
int CvUnitMeshGroups::getMeleeWaveSize() const
{
	return m_iMeleeWaveSize;
}
int CvUnitMeshGroups::getRangedWaveSize() const
{
	return m_iRangedWaveSize;
}
float CvUnitMeshGroups::getMaxSpeed() const
{
	return m_fMaxSpeed;
}
float CvUnitMeshGroups::getPadTime() const
{
	return m_fPadTime;
}
int CvUnitMeshGroups::getNumMeshGroups() const
{
	return m_aMeshGroups.size();
}
const CvUnitMeshGroup& CvUnitMeshGroups::getMeshGroup(int index) const
{
	FAssert(index >= 0);
	FAssert(index < (int)m_aMeshGroups.size());
	return m_aMeshGroups[index];
}
void CvUnitMeshGroups::read(FDataStreamBase* stream)
{
	stream->Read((int*)&m_eProfession);
	stream->Read(&m_iMeleeWaveSize);
	stream->Read(&m_iRangedWaveSize);
	stream->Read(&m_fMaxSpeed);
	stream->Read(&m_fPadTime);
	int iNumGroups;
	stream->Read(&iNumGroups);
	m_aMeshGroups.clear();
	for (int i = 0; i < iNumGroups; ++i)
	{
		CvUnitMeshGroup kGroup;
		kGroup.read(stream);
		m_aMeshGroups.push_back(kGroup);
	}
}
void CvUnitMeshGroups::write(FDataStreamBase* stream)
{
	stream->Write(m_eProfession);
	stream->Write(m_iMeleeWaveSize);
	stream->Write(m_iRangedWaveSize);
	stream->Write(m_fMaxSpeed);
	stream->Write(m_fPadTime);
	stream->Write((int)m_aMeshGroups.size());
	for (int i = 0; i < (int)m_aMeshGroups.size(); ++i)
	{
		m_aMeshGroups[i].write(stream);
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvUnitInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvUnitInfo::CvUnitInfo() :
m_iAIWeight(0),
m_iHurryCostModifier(0),
m_iEuropeCost(0),
m_iEuropeCostIncrease(0),
m_iImmigrationWeight(0),
m_iImmigrationWeightDecay(0),
m_iAdvancedStartCost(0),
m_iAdvancedStartCostIncrease(0),
m_iMinAreaSize(0),
m_iMoves(0),
m_iWorkRate(0),
m_iWorkRateModifier(0),
m_iMissionaryRateModifier(0),
m_iCombat(0),
m_iXPValueAttack(0),
m_iXPValueDefense(0),
m_iWithdrawalProbability(0),
m_iCityAttackModifier(0),
m_iCityDefenseModifier(0),
m_iHillsAttackModifier(0),
m_iHillsDefenseModifier(0),
m_iBombardRate(0),
m_iSpecialCargo(0),
m_iDomainCargo(0),
m_iCargoSpace(0),
m_iRequiredTransportSize(0),
m_iAssetValue(0),
m_iPowerValue(0),
m_iUnitClassType(NO_UNITCLASS),
m_iSpecialUnitType(NO_SPECIALUNIT),
m_iUnitCaptureClassType(NO_UNITCLASS),
m_iUnitCombatType(NO_UNITCOMBAT),
m_iDomainType(NO_DOMAIN),
m_iDefaultProfession(NO_PROFESSION),
m_iDefaultUnitAIType(NO_UNITAI),
m_iInvisibleType(NO_INVISIBLE),
m_iPrereqBuilding(NO_BUILDING),
m_iNumUnitNames(0),
m_iCommandType(NO_COMMAND),
m_iLeaderExperience(0),
m_iLearnTime(-1),
m_iStudentWeight(0),
m_iTeacherWeight(0),
m_bNoBadGoodies(false),
m_bOnlyDefensive(false),
m_bNoCapture(false),
m_bQuickCombat(false),
m_bRivalTerritory(false),
m_bMilitaryProduction(false),
m_bFound(false),
m_bInvisible(false),
m_bNoDefensiveBonus(false),
m_bCanMoveImpassable(false),
m_bCanMoveAllTerrain(false),
m_bFlatMovementCost(false),
m_bIgnoreTerrainCost(false),
m_bMechanized(false),
m_bLineOfSight(false),
m_bHiddenNationality(false),
m_bAlwaysHostile(false),
m_bTreasure(false),
m_bCapturesCargo(false),
m_bLandYieldChanges(false),
m_bWaterYieldChanges(false),
m_abUpgradeUnitClass(NULL),
m_abUnitAIType(NULL),
m_abNotUnitAIType(NULL),
m_abBuilds(NULL),
m_abTerrainImpassable(NULL),
m_abFeatureImpassable(NULL),
m_abEvasionBuilding(NULL),
m_aiProductionTraits(NULL),
m_aiTerrainAttackModifier(NULL),
m_aiTerrainDefenseModifier(NULL),
m_aiFeatureAttackModifier(NULL),
m_aiFeatureDefenseModifier(NULL),
m_aiUnitClassAttackModifier(NULL),
m_aiUnitClassDefenseModifier(NULL),
m_aiUnitCombatModifier(NULL),
m_aiDomainModifier(NULL),
m_aiYieldModifier(NULL),
m_aiBonusYieldChange(NULL),
m_aiYieldChange(NULL),
m_aiYieldCost(NULL),
m_abFreePromotions(NULL),
m_abPrereqOrBuilding(NULL),
m_paszUnitNames(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvUnitInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvUnitInfo::~CvUnitInfo()
{
	SAFE_DELETE_ARRAY(m_abUpgradeUnitClass);
	SAFE_DELETE_ARRAY(m_abUnitAIType);
	SAFE_DELETE_ARRAY(m_abNotUnitAIType);
	SAFE_DELETE_ARRAY(m_abBuilds);
	SAFE_DELETE_ARRAY(m_abTerrainImpassable);
	SAFE_DELETE_ARRAY(m_abFeatureImpassable);
	SAFE_DELETE_ARRAY(m_abEvasionBuilding);
	SAFE_DELETE_ARRAY(m_aiProductionTraits);
	SAFE_DELETE_ARRAY(m_aiTerrainAttackModifier);
	SAFE_DELETE_ARRAY(m_aiTerrainDefenseModifier);
	SAFE_DELETE_ARRAY(m_aiFeatureAttackModifier);
	SAFE_DELETE_ARRAY(m_aiFeatureDefenseModifier);
	SAFE_DELETE_ARRAY(m_aiUnitClassAttackModifier);
	SAFE_DELETE_ARRAY(m_aiUnitClassDefenseModifier);
	SAFE_DELETE_ARRAY(m_aiUnitCombatModifier);
	SAFE_DELETE_ARRAY(m_aiDomainModifier);
	SAFE_DELETE_ARRAY(m_aiYieldModifier);
	SAFE_DELETE_ARRAY(m_aiBonusYieldChange);
	SAFE_DELETE_ARRAY(m_aiYieldChange);
	SAFE_DELETE_ARRAY(m_aiYieldCost);
	SAFE_DELETE_ARRAY(m_abFreePromotions);
	SAFE_DELETE_ARRAY(m_abPrereqOrBuilding);
	SAFE_DELETE_ARRAY(m_paszUnitNames);
}
int CvUnitInfo::getAIWeight() const
{
	return m_iAIWeight;
}
int CvUnitInfo::getHurryCostModifier() const
{
	return m_iHurryCostModifier;
}
int CvUnitInfo::getEuropeCost() const
{
	return m_iEuropeCost;
}
int CvUnitInfo::getEuropeCostIncrease() const
{
	return m_iEuropeCostIncrease;
}
int CvUnitInfo::getImmigrationWeight() const
{
	return m_iImmigrationWeight;
}
int CvUnitInfo::getImmigrationWeightDecay() const
{
	return m_iImmigrationWeightDecay;
}
int CvUnitInfo::getAdvancedStartCost() const
{
	return m_iAdvancedStartCost;
}
int CvUnitInfo::getAdvancedStartCostIncrease() const
{
	return m_iAdvancedStartCostIncrease;
}
int CvUnitInfo::getMinAreaSize() const
{
	return m_iMinAreaSize;
}
int CvUnitInfo::getMoves() const
{
	return m_iMoves;
}
int CvUnitInfo::getWorkRate() const
{
	return m_iWorkRate;
}
int CvUnitInfo::getWorkRateModifier() const
{
	return m_iWorkRateModifier;
}
int CvUnitInfo::getMissionaryRateModifier() const
{
	return m_iMissionaryRateModifier;
}
int CvUnitInfo::getCombat() const
{
	return m_iCombat;
}
void CvUnitInfo::setCombat(int iNum)
{
	m_iCombat = iNum;
}
int CvUnitInfo::getXPValueAttack() const
{
	return m_iXPValueAttack;
}
int CvUnitInfo::getXPValueDefense() const
{
	return m_iXPValueDefense;
}
int CvUnitInfo::getWithdrawalProbability() const
{
	return m_iWithdrawalProbability;
}
int CvUnitInfo::getCityAttackModifier() const
{
	return m_iCityAttackModifier;
}
int CvUnitInfo::getCityDefenseModifier() const
{
	return m_iCityDefenseModifier;
}
int CvUnitInfo::getHillsAttackModifier() const
{
	return m_iHillsAttackModifier;
}
int CvUnitInfo::getHillsDefenseModifier() const
{
	return m_iHillsDefenseModifier;
}
int CvUnitInfo::getBombardRate() const
{
	return m_iBombardRate;
}
int CvUnitInfo::getSpecialCargo() const
{
	return m_iSpecialCargo;
}
int CvUnitInfo::getDomainCargo() const
{
	return m_iDomainCargo;
}
int CvUnitInfo::getCargoSpace() const
{
	return m_iCargoSpace;
}
int CvUnitInfo::getRequiredTransportSize() const
{
	return m_iRequiredTransportSize;
}
int CvUnitInfo::getAssetValue() const
{
	return m_iAssetValue;
}
int CvUnitInfo::getPowerValue() const
{
	return m_iPowerValue;
}
int CvUnitInfo::getUnitClassType() const
{
	return m_iUnitClassType;
}
int CvUnitInfo::getSpecialUnitType() const
{
	return m_iSpecialUnitType;
}
int CvUnitInfo::getUnitCaptureClassType() const
{
	return m_iUnitCaptureClassType;
}
int CvUnitInfo::getUnitCombatType() const
{
	return m_iUnitCombatType;
}
int CvUnitInfo::getDomainType() const
{
	return m_iDomainType;
}
int CvUnitInfo::getDefaultProfession() const
{
	return m_iDefaultProfession;
}
int CvUnitInfo::getDefaultUnitAIType() const
{
	return m_iDefaultUnitAIType;
}
int CvUnitInfo::getInvisibleType() const
{
	return m_iInvisibleType;
}
int CvUnitInfo::getSeeInvisibleType(int i) const
{
	FAssert(i < (int)m_aiSeeInvisibleTypes.size());
	return m_aiSeeInvisibleTypes[i];
}
int CvUnitInfo::getNumSeeInvisibleTypes() const
{
	return (int)m_aiSeeInvisibleTypes.size();
}
int CvUnitInfo::getPrereqBuilding() const
{
	return m_iPrereqBuilding;
}
int CvUnitInfo::getGroupSize(int iProfession) const// the initial number of individuals in the unit group
{
	int iSize = 0;
	for (int i = 0; i < getGroupDefinitions(iProfession); i++)
	{
		iSize += getUnitGroupRequired(i, iProfession);
	}
	return iSize;
}
int CvUnitInfo::getGroupDefinitions(int iProfession) const// the number of UnitMeshGroups for this unit
{
	return getProfessionMeshGroup(iProfession).getNumMeshGroups();
}
int CvUnitInfo::getMeleeWaveSize(int iProfession) const
{
	return getProfessionMeshGroup(iProfession).getMeleeWaveSize();
}
int CvUnitInfo::getRangedWaveSize(int iProfession) const
{
	return getProfessionMeshGroup(iProfession).getRangedWaveSize();
}
int CvUnitInfo::getNumUnitNames() const
{
	return m_iNumUnitNames;
}
int CvUnitInfo::getLearnTime() const
{
	return m_iLearnTime;
}
int CvUnitInfo::getStudentWeight() const
{
	return m_iStudentWeight;
}
int CvUnitInfo::getTeacherWeight() const
{
	return m_iTeacherWeight;
}
bool CvUnitInfo::isNoBadGoodies() const
{
	return m_bNoBadGoodies;
}
bool CvUnitInfo::isOnlyDefensive() const
{
	return m_bOnlyDefensive;
}
bool CvUnitInfo::isNoCapture() const
{
	return m_bNoCapture;
}
bool CvUnitInfo::isQuickCombat() const
{
	return m_bQuickCombat;
}
bool CvUnitInfo::isRivalTerritory() const
{
	return m_bRivalTerritory;
}
bool CvUnitInfo::isMilitaryProduction() const
{
	return m_bMilitaryProduction;
}
bool CvUnitInfo::isFound() const
{
	return m_bFound;
}
bool CvUnitInfo::isInvisible() const
{
	return m_bInvisible;
}
void CvUnitInfo::setInvisible(bool bEnable)
{
	m_bInvisible = bEnable;
}
bool CvUnitInfo::isNoDefensiveBonus() const
{
	return m_bNoDefensiveBonus;
}
bool CvUnitInfo::isCanMoveImpassable() const
{
	return m_bCanMoveImpassable;
}
bool CvUnitInfo::isCanMoveAllTerrain() const
{
	return m_bCanMoveAllTerrain;
}
bool CvUnitInfo::isFlatMovementCost() const
{
	return m_bFlatMovementCost;
}
bool CvUnitInfo::isIgnoreTerrainCost() const
{
	return m_bIgnoreTerrainCost;
}
bool CvUnitInfo::isMechUnit() const
{
	return m_bMechanized;
}
bool CvUnitInfo::isLineOfSight() const
{
	return m_bLineOfSight;
}
bool CvUnitInfo::isHiddenNationality() const
{
	return m_bHiddenNationality;
}
bool CvUnitInfo::isAlwaysHostile() const
{
	return m_bAlwaysHostile;
}
bool CvUnitInfo::isTreasure() const
{
	return m_bTreasure;
}
bool CvUnitInfo::isCapturesCargo() const
{
	return m_bCapturesCargo;
}
bool CvUnitInfo::isLandYieldChanges() const
{
	return m_bLandYieldChanges;
}
bool CvUnitInfo::isWaterYieldChanges() const
{
	return m_bWaterYieldChanges;
}
float CvUnitInfo::getUnitMaxSpeed(int iProfession) const
{
	return getProfessionMeshGroup(iProfession).getMaxSpeed();
}
float CvUnitInfo::getUnitPadTime(int iProfession) const
{
	return getProfessionMeshGroup(iProfession).getPadTime();
}
int CvUnitInfo::getCommandType() const
{
	return m_iCommandType;
}
void CvUnitInfo::setCommandType(int iNewType)
{
	m_iCommandType = iNewType;
}

// Arrays
int CvUnitInfo::getProductionTraits(int i) const
{
	FAssertMsg(i < GC.getNumTraitInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiProductionTraits ? m_aiProductionTraits[i] : -1;
}
int CvUnitInfo::getTerrainAttackModifier(int i) const
{
	FAssertMsg(i < GC.getNumTerrainInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiTerrainAttackModifier ? m_aiTerrainAttackModifier[i] : -1;
}
int CvUnitInfo::getTerrainDefenseModifier(int i) const
{
	FAssertMsg(i < GC.getNumTerrainInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiTerrainDefenseModifier ? m_aiTerrainDefenseModifier[i] : -1;
}
int CvUnitInfo::getFeatureAttackModifier(int i) const
{
	FAssertMsg(i < GC.getNumFeatureInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiFeatureAttackModifier ? m_aiFeatureAttackModifier[i] : -1;
}
int CvUnitInfo::getFeatureDefenseModifier(int i) const
{
	FAssertMsg(i < GC.getNumFeatureInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiFeatureDefenseModifier ? m_aiFeatureDefenseModifier[i] : -1;
}
int CvUnitInfo::getUnitClassAttackModifier(int i) const
{
	FAssertMsg(i < GC.getNumUnitClassInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiUnitClassAttackModifier ? m_aiUnitClassAttackModifier[i] : -1;
}
int CvUnitInfo::getUnitClassDefenseModifier(int i) const
{
	FAssertMsg(i < GC.getNumUnitClassInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiUnitClassDefenseModifier ? m_aiUnitClassDefenseModifier[i] : -1;
}
int CvUnitInfo::getUnitCombatModifier(int i) const
{
	FAssertMsg(i < GC.getNumUnitCombatInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiUnitCombatModifier ? m_aiUnitCombatModifier[i] : -1;
}
int CvUnitInfo::getDomainModifier(int i) const
{
	FAssertMsg(i < NUM_DOMAIN_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiDomainModifier ? m_aiDomainModifier[i] : -1;
}
int CvUnitInfo::getYieldModifier(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiYieldModifier ? m_aiYieldModifier[i] : -1;
}
int CvUnitInfo::getBonusYieldChange(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiBonusYieldChange ? m_aiBonusYieldChange[i] : -1;
}
int CvUnitInfo::getYieldChange(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiYieldChange ? m_aiYieldChange[i] : -1;
}
int CvUnitInfo::getYieldCost(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiYieldCost ? m_aiYieldCost[i] : -1;
}
int CvUnitInfo::getUnitGroupRequired(int i, int iProfession) const
{
	return getProfessionMeshGroup(iProfession).getMeshGroup(i).getNumRequired();
}
bool CvUnitInfo::getUpgradeUnitClass(int i) const
{
	FAssertMsg(i < GC.getNumUnitClassInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abUpgradeUnitClass ? m_abUpgradeUnitClass[i] : false;
}
bool CvUnitInfo::getUnitAIType(int i) const
{
	FAssertMsg(i < NUM_UNITAI_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abUnitAIType ? m_abUnitAIType[i] : false;
}
bool CvUnitInfo::getNotUnitAIType(int i) const
{
	FAssertMsg(i < NUM_UNITAI_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abNotUnitAIType ? m_abNotUnitAIType[i] : false;
}
bool CvUnitInfo::getBuilds(int i) const
{
	FAssertMsg(i < GC.getNumBuildInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abBuilds ? m_abBuilds[i] : false;
}
bool CvUnitInfo::getTerrainImpassable(int i) const
{
	FAssertMsg(i < GC.getNumTerrainInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abTerrainImpassable ? m_abTerrainImpassable[i] : false;
}
bool CvUnitInfo::getFeatureImpassable(int i) const
{
	FAssertMsg(i < GC.getNumFeatureInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abFeatureImpassable ? m_abFeatureImpassable[i] : false;
}
bool CvUnitInfo::isEvasionBuilding(int i) const
{
	FAssertMsg(i > -1 && i < GC.getNumBuildingClassInfos(), "Index out of bounds");
	return m_abEvasionBuilding ? m_abEvasionBuilding[i] : false;
}
bool CvUnitInfo::getFreePromotions(int i) const
{
	FAssertMsg(i < GC.getNumPromotionInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abFreePromotions ? m_abFreePromotions[i] : false;
}
bool CvUnitInfo::isPrereqOrBuilding(int i) const
{
	FAssertMsg(i < GC.getNumBuildingClassInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abPrereqOrBuilding ? m_abPrereqOrBuilding[i] : false;
}
int CvUnitInfo::getLeaderPromotion() const
{
	return m_iLeaderPromotion;
}
int CvUnitInfo::getLeaderExperience() const
{
	return m_iLeaderExperience;
}
const char* CvUnitInfo::getArtDefineTag(int index, int iProfession) const
{
	return getProfessionMeshGroup(iProfession).getMeshGroup(index).getArtDefineTag();
}
const char* CvUnitInfo::getUnitNames(int i) const
{
	FAssertMsg(i < getNumUnitNames(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return (m_paszUnitNames) ? m_paszUnitNames[i] : NULL;
}
const char* CvUnitInfo::getFormationType() const
{
	return m_szFormationType;
}
const char* CvUnitInfo::getButton() const
{
	return m_szArtDefineButton;
}
void CvUnitInfo::updateArtDefineButton()
{
	m_szArtDefineButton = getArtInfo(0, NO_PROFESSION)->getButton();
}
const CvArtInfoUnit* CvUnitInfo::getArtInfo(int index, int iProfession) const
{
	return ARTFILEMGR.getUnitArtInfo(getArtDefineTag(index, iProfession));
}
const CvUnitMeshGroups& CvUnitInfo::getProfessionMeshGroup(int iProfession) const
{
	FAssert(m_aProfessionGroups.size() > 0);
	for(int i=0;i<(int)m_aProfessionGroups.size();i++)
	{
		if(m_aProfessionGroups[i].getProfession() == iProfession)
		{
			return m_aProfessionGroups[i];
		}
	}
	for(int i=0;i<(int)m_aProfessionGroups.size();i++)
	{
		if(m_aProfessionGroups[i].getProfession() == NO_PROFESSION)
		{
			return m_aProfessionGroups[i];
		}
	}
	return m_aProfessionGroups[0];
}
void CvUnitInfo::read(FDataStreamBase* stream)
{
	CvHotkeyInfo::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);	// flags for expansion
	stream->Read(&m_iAIWeight);
	stream->Read(&m_iHurryCostModifier);
	stream->Read(&m_iEuropeCost);
	stream->Read(&m_iEuropeCostIncrease);
	stream->Read(&m_iImmigrationWeight);
	stream->Read(&m_iImmigrationWeightDecay);
	stream->Read(&m_iAdvancedStartCost);
	stream->Read(&m_iAdvancedStartCostIncrease);
	stream->Read(&m_iMinAreaSize);
	stream->Read(&m_iMoves);
	stream->Read(&m_iWorkRate);
	stream->Read(&m_iWorkRateModifier);
	stream->Read(&m_iMissionaryRateModifier);
	stream->Read(&m_iCombat);
	stream->Read(&m_iXPValueAttack);
	stream->Read(&m_iXPValueDefense);
	stream->Read(&m_iWithdrawalProbability);
	stream->Read(&m_iCityAttackModifier);
	stream->Read(&m_iCityDefenseModifier);
	stream->Read(&m_iHillsAttackModifier);
	stream->Read(&m_iHillsDefenseModifier);
	stream->Read(&m_iBombardRate);
	stream->Read(&m_iSpecialCargo);
	stream->Read(&m_iDomainCargo);
	stream->Read(&m_iCargoSpace);
	stream->Read(&m_iRequiredTransportSize);
	stream->Read(&m_iAssetValue);
	stream->Read(&m_iPowerValue);
	stream->Read(&m_iUnitClassType);
	stream->Read(&m_iSpecialUnitType);
	stream->Read(&m_iUnitCaptureClassType);
	stream->Read(&m_iUnitCombatType);
	stream->Read(&m_iDomainType);
	stream->Read(&m_iDefaultProfession);
	stream->Read(&m_iDefaultUnitAIType);
	stream->Read(&m_iInvisibleType);
	int iNumInvisibleTypes;
	stream->Read(&iNumInvisibleTypes);
	for(int i=0;i<iNumInvisibleTypes;i++)
	{
		int iSeeInvisibleType;
		stream->Read(&iSeeInvisibleType);
		m_aiSeeInvisibleTypes.push_back(iSeeInvisibleType);
	}
	stream->Read(&m_iPrereqBuilding);
	stream->Read(&m_iNumUnitNames);
	stream->Read(&m_iCommandType);
	stream->Read(&m_iLearnTime);
	stream->Read(&m_iStudentWeight);
	stream->Read(&m_iTeacherWeight);
	stream->Read(&m_bNoBadGoodies);
	stream->Read(&m_bOnlyDefensive);
	stream->Read(&m_bNoCapture);
	stream->Read(&m_bQuickCombat);
	stream->Read(&m_bRivalTerritory);
	stream->Read(&m_bMilitaryProduction);
	stream->Read(&m_bFound);
	stream->Read(&m_bInvisible);
	stream->Read(&m_bNoDefensiveBonus);
	stream->Read(&m_bCanMoveImpassable);
	stream->Read(&m_bCanMoveAllTerrain);
	stream->Read(&m_bFlatMovementCost);
	stream->Read(&m_bIgnoreTerrainCost);
	stream->Read(&m_bMechanized);
	stream->Read(&m_bLineOfSight);
	stream->Read(&m_bHiddenNationality);
	stream->Read(&m_bAlwaysHostile);
	stream->Read(&m_bTreasure);
	stream->Read(&m_bCapturesCargo);
	stream->Read(&m_bLandYieldChanges);
	stream->Read(&m_bWaterYieldChanges);
	int iSize;
	stream->Read(&iSize);
	m_aProfessionGroups.clear();
	for (int i = 0; i < iSize; ++i)
	{
		CvUnitMeshGroups kGroup;
		kGroup.read(stream);
		m_aProfessionGroups.push_back(kGroup);
	}
	SAFE_DELETE_ARRAY(m_aiProductionTraits);
	m_aiProductionTraits = new int[GC.getNumTraitInfos()];
	stream->Read(GC.getNumTraitInfos(), m_aiProductionTraits);
	SAFE_DELETE_ARRAY(m_aiTerrainAttackModifier);
	m_aiTerrainAttackModifier = new int[GC.getNumTerrainInfos()];
	stream->Read(GC.getNumTerrainInfos(), m_aiTerrainAttackModifier);
	SAFE_DELETE_ARRAY(m_aiTerrainDefenseModifier);
	m_aiTerrainDefenseModifier = new int[GC.getNumTerrainInfos()];
	stream->Read(GC.getNumTerrainInfos(), m_aiTerrainDefenseModifier);
	SAFE_DELETE_ARRAY(m_aiFeatureAttackModifier);
	m_aiFeatureAttackModifier = new int[GC.getNumFeatureInfos()];
	stream->Read(GC.getNumFeatureInfos(), m_aiFeatureAttackModifier);
	SAFE_DELETE_ARRAY(m_aiFeatureDefenseModifier);
	m_aiFeatureDefenseModifier = new int[GC.getNumFeatureInfos()];
	stream->Read(GC.getNumFeatureInfos(), m_aiFeatureDefenseModifier);
	SAFE_DELETE_ARRAY(m_aiUnitClassAttackModifier);
	m_aiUnitClassAttackModifier = new int[GC.getNumUnitClassInfos()];
	stream->Read(GC.getNumUnitClassInfos(), m_aiUnitClassAttackModifier);
	SAFE_DELETE_ARRAY(m_aiUnitClassDefenseModifier);
	m_aiUnitClassDefenseModifier = new int[GC.getNumUnitClassInfos()];
	stream->Read(GC.getNumUnitClassInfos(), m_aiUnitClassDefenseModifier);
	SAFE_DELETE_ARRAY(m_aiUnitCombatModifier);
	m_aiUnitCombatModifier = new int[GC.getNumUnitCombatInfos()];
	stream->Read(GC.getNumUnitCombatInfos(), m_aiUnitCombatModifier);
	SAFE_DELETE_ARRAY(m_aiDomainModifier);
	m_aiDomainModifier = new int[NUM_DOMAIN_TYPES];
	stream->Read(NUM_DOMAIN_TYPES, m_aiDomainModifier);
	SAFE_DELETE_ARRAY(m_aiYieldModifier);
	m_aiYieldModifier = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiYieldModifier);
	SAFE_DELETE_ARRAY(m_aiBonusYieldChange);
	m_aiBonusYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiBonusYieldChange);
	SAFE_DELETE_ARRAY(m_aiYieldChange);
	m_aiYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiYieldChange);
	SAFE_DELETE_ARRAY(m_aiYieldCost);
	m_aiYieldCost = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiYieldCost);
	SAFE_DELETE_ARRAY(m_abUpgradeUnitClass);
	m_abUpgradeUnitClass = new bool[GC.getNumUnitClassInfos()];
	stream->Read(GC.getNumUnitClassInfos(), m_abUpgradeUnitClass);
	SAFE_DELETE_ARRAY(m_abUnitAIType);
	m_abUnitAIType = new bool[NUM_UNITAI_TYPES];
	stream->Read(NUM_UNITAI_TYPES, m_abUnitAIType);
	SAFE_DELETE_ARRAY(m_abNotUnitAIType);
	m_abNotUnitAIType = new bool[NUM_UNITAI_TYPES];
	stream->Read(NUM_UNITAI_TYPES, m_abNotUnitAIType);
	SAFE_DELETE_ARRAY(m_abBuilds);
	m_abBuilds = new bool[GC.getNumBuildInfos()];
	stream->Read(GC.getNumBuildInfos(), m_abBuilds);
	SAFE_DELETE_ARRAY(m_abTerrainImpassable);
	m_abTerrainImpassable = new bool[GC.getNumTerrainInfos()];
	stream->Read(GC.getNumTerrainInfos(), m_abTerrainImpassable);
	SAFE_DELETE_ARRAY(m_abFeatureImpassable);
	m_abFeatureImpassable = new bool[GC.getNumFeatureInfos()];
	stream->Read(GC.getNumFeatureInfos(), m_abFeatureImpassable);
	SAFE_DELETE_ARRAY(m_abEvasionBuilding);
	m_abEvasionBuilding = new bool[GC.getNumBuildingClassInfos()];
	stream->Read(GC.getNumBuildingClassInfos(), m_abEvasionBuilding);
	SAFE_DELETE_ARRAY(m_abFreePromotions);
	m_abFreePromotions = new bool[GC.getNumPromotionInfos()];
	stream->Read(GC.getNumPromotionInfos(), m_abFreePromotions);
	SAFE_DELETE_ARRAY(m_abPrereqOrBuilding);
	m_abPrereqOrBuilding = new bool[GC.getNumBuildingClassInfos()];
	stream->Read(GC.getNumBuildingClassInfos(), m_abPrereqOrBuilding);
	stream->Read(&m_iLeaderPromotion);
	stream->Read(&m_iLeaderExperience);
	SAFE_DELETE_ARRAY(m_paszUnitNames);
	m_paszUnitNames = new CvString[m_iNumUnitNames];
	stream->ReadString(m_iNumUnitNames, m_paszUnitNames);
	stream->ReadString(m_szFormationType);
	updateArtDefineButton();
}
void CvUnitInfo::write(FDataStreamBase* stream)
{
	CvHotkeyInfo::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_iAIWeight);
	stream->Write(m_iHurryCostModifier);
	stream->Write(m_iEuropeCost);
	stream->Write(m_iEuropeCostIncrease);
	stream->Write(m_iImmigrationWeight);
	stream->Write(m_iImmigrationWeightDecay);
	stream->Write(m_iAdvancedStartCost);
	stream->Write(m_iAdvancedStartCostIncrease);
	stream->Write(m_iMinAreaSize);
	stream->Write(m_iMoves);
	stream->Write(m_iWorkRate);
	stream->Write(m_iWorkRateModifier);
	stream->Write(m_iMissionaryRateModifier);
	stream->Write(m_iCombat);
	stream->Write(m_iXPValueAttack);
	stream->Write(m_iXPValueDefense);
	stream->Write(m_iWithdrawalProbability);
	stream->Write(m_iCityAttackModifier);
	stream->Write(m_iCityDefenseModifier);
	stream->Write(m_iHillsAttackModifier);
	stream->Write(m_iHillsDefenseModifier);
	stream->Write(m_iBombardRate);
	stream->Write(m_iSpecialCargo);
	stream->Write(m_iDomainCargo);
	stream->Write(m_iCargoSpace);
	stream->Write(m_iRequiredTransportSize);
	stream->Write(m_iAssetValue);
	stream->Write(m_iPowerValue);
	stream->Write(m_iUnitClassType);
	stream->Write(m_iSpecialUnitType);
	stream->Write(m_iUnitCaptureClassType);
	stream->Write(m_iUnitCombatType);
	stream->Write(m_iDomainType);
	stream->Write(m_iDefaultProfession);
	stream->Write(m_iDefaultUnitAIType);
	stream->Write(m_iInvisibleType);
	stream->Write((int)m_aiSeeInvisibleTypes.size());
	for(int i=0;i<(int)m_aiSeeInvisibleTypes.size();i++)
	{
		stream->Write(m_aiSeeInvisibleTypes[i]);
	}
	stream->Write(m_iPrereqBuilding);
	stream->Write(m_iNumUnitNames);
	stream->Write(m_iCommandType);
	stream->Write(m_iLearnTime);
	stream->Write(m_iStudentWeight);
	stream->Write(m_iTeacherWeight);
	stream->Write(m_bNoBadGoodies);
	stream->Write(m_bOnlyDefensive);
	stream->Write(m_bNoCapture);
	stream->Write(m_bQuickCombat);
	stream->Write(m_bRivalTerritory);
	stream->Write(m_bMilitaryProduction);
	stream->Write(m_bFound);
	stream->Write(m_bInvisible);
	stream->Write(m_bNoDefensiveBonus);
	stream->Write(m_bCanMoveImpassable);
	stream->Write(m_bCanMoveAllTerrain);
	stream->Write(m_bFlatMovementCost);
	stream->Write(m_bIgnoreTerrainCost);
	stream->Write(m_bMechanized);
	stream->Write(m_bLineOfSight);
	stream->Write(m_bHiddenNationality);
	stream->Write(m_bAlwaysHostile);
	stream->Write(m_bTreasure);
	stream->Write(m_bCapturesCargo);
	stream->Write(m_bLandYieldChanges);
	stream->Write(m_bWaterYieldChanges);
	stream->Write((int) m_aProfessionGroups.size());
	for (int i = 0; i < (int) m_aProfessionGroups.size(); ++i)
	{
		m_aProfessionGroups[i].write(stream);
	}
	stream->Write(GC.getNumTraitInfos(), m_aiProductionTraits);
	stream->Write(GC.getNumTerrainInfos(), m_aiTerrainAttackModifier);
	stream->Write(GC.getNumTerrainInfos(), m_aiTerrainDefenseModifier);
	stream->Write(GC.getNumFeatureInfos(), m_aiFeatureAttackModifier);
	stream->Write(GC.getNumFeatureInfos(), m_aiFeatureDefenseModifier);
	stream->Write(GC.getNumUnitClassInfos(), m_aiUnitClassAttackModifier);
	stream->Write(GC.getNumUnitClassInfos(), m_aiUnitClassDefenseModifier);
	stream->Write(GC.getNumUnitCombatInfos(), m_aiUnitCombatModifier);
	stream->Write(NUM_DOMAIN_TYPES, m_aiDomainModifier);
	stream->Write(NUM_YIELD_TYPES, m_aiYieldModifier);
	stream->Write(NUM_YIELD_TYPES, m_aiBonusYieldChange);
	stream->Write(NUM_YIELD_TYPES, m_aiYieldChange);
	stream->Write(NUM_YIELD_TYPES, m_aiYieldCost);
	stream->Write(GC.getNumUnitClassInfos(), m_abUpgradeUnitClass);
	stream->Write(NUM_UNITAI_TYPES, m_abUnitAIType);
	stream->Write(NUM_UNITAI_TYPES, m_abNotUnitAIType);
	stream->Write(GC.getNumBuildInfos(), m_abBuilds);
	stream->Write(GC.getNumTerrainInfos(), m_abTerrainImpassable);
	stream->Write(GC.getNumFeatureInfos(), m_abFeatureImpassable);
	stream->Write(GC.getNumBuildingClassInfos(), m_abEvasionBuilding);
	stream->Write(GC.getNumPromotionInfos(), m_abFreePromotions);
	stream->Write(GC.getNumBuildingClassInfos(), m_abPrereqOrBuilding);
	stream->Write(m_iLeaderPromotion);
	stream->Write(m_iLeaderExperience);
	stream->WriteString(m_iNumUnitNames, m_paszUnitNames);
	stream->WriteString(m_szFormationType);
}
//
// read from xml
//
bool CvUnitInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvHotkeyInfo::read(pXML))
	{
		return false;
	}
	int j=0;				//loop counter
	int k=0;				//loop counter
	int iNumSibs=0;				// the number of siblings the current xml node has
	pXML->GetChildXmlValByName(szTextVal, "Class");
	m_iUnitClassType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "Special");
	m_iSpecialUnitType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "Capture");
	m_iUnitCaptureClassType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "Combat");
	m_iUnitCombatType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "Domain");
	m_iDomainType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "DefaultProfession");
	m_iDefaultProfession = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "DefaultUnitAI");
	m_iDefaultUnitAIType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "Invisible");
	m_iInvisibleType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "SeeInvisible");
	std::vector<CvString> tokens;
	szTextVal.getTokens(",", tokens);
	for(int i=0;i<(int)tokens.size();i++)
	{
		int iInvisibleType = pXML->FindInInfoClass(tokens[i]);
		if(iInvisibleType != NO_INVISIBLE)
		{
			m_aiSeeInvisibleTypes.push_back(iInvisibleType);
		}
	}
	pXML->GetChildXmlValByName(&m_iLearnTime, "iNativeLearnTime");
	pXML->GetChildXmlValByName(&m_iStudentWeight, "iStudentWeight");
	pXML->GetChildXmlValByName(&m_iTeacherWeight, "iTeacherWeight");
	pXML->GetChildXmlValByName(&m_bNoBadGoodies, "bNoBadGoodies");
	pXML->GetChildXmlValByName(&m_bOnlyDefensive, "bOnlyDefensive");
	pXML->GetChildXmlValByName(&m_bNoCapture, "bNoCapture");
	pXML->GetChildXmlValByName(&m_bQuickCombat, "bQuickCombat");
	pXML->GetChildXmlValByName(&m_bRivalTerritory, "bRivalTerritory");
	pXML->GetChildXmlValByName(&m_bMilitaryProduction, "bMilitaryProduction");
	pXML->GetChildXmlValByName(&m_bFound, "bFound");
	pXML->GetChildXmlValByName(&m_bInvisible, "bInvisible");
	pXML->GetChildXmlValByName(&m_bNoDefensiveBonus, "bNoDefensiveBonus");
	pXML->GetChildXmlValByName(&m_bCanMoveImpassable, "bCanMoveImpassable");
	pXML->GetChildXmlValByName(&m_bCanMoveAllTerrain, "bCanMoveAllTerrain");
	pXML->GetChildXmlValByName(&m_bFlatMovementCost, "bFlatMovementCost");
	pXML->GetChildXmlValByName(&m_bIgnoreTerrainCost, "bIgnoreTerrainCost");
	pXML->GetChildXmlValByName(&m_bMechanized,"bMechanized",false);
	pXML->GetChildXmlValByName(&m_bLineOfSight,"bLineOfSight",false);
	pXML->GetChildXmlValByName(&m_bHiddenNationality,"bHiddenNationality",false);
	pXML->GetChildXmlValByName(&m_bAlwaysHostile,"bAlwaysHostile",false);
	pXML->GetChildXmlValByName(&m_bTreasure,"bTreasure",false);
	pXML->GetChildXmlValByName(&m_bCapturesCargo,"bCapturesCargo",false);
	pXML->GetChildXmlValByName(&m_bLandYieldChanges,"bLandYieldChanges",true);
	pXML->GetChildXmlValByName(&m_bWaterYieldChanges,"bWaterYieldChanges",true);
	pXML->SetVariableListTagPair(&m_abUpgradeUnitClass, "UnitClassUpgrades", GC.getNumUnitClassInfos(), false);
	pXML->SetVariableListTagPair(&m_abUnitAIType, "UnitAIs", NUM_UNITAI_TYPES, false);
	pXML->SetVariableListTagPair(&m_abNotUnitAIType, "NotUnitAIs", NUM_UNITAI_TYPES, false);
	pXML->SetVariableListTagPair(&m_abBuilds, "Builds", GC.getNumBuildInfos(), false);
	pXML->GetChildXmlValByName(szTextVal, "PrereqBuilding");
	m_iPrereqBuilding = pXML->FindInInfoClass(szTextVal);
	pXML->SetVariableListTagPair(&m_abPrereqOrBuilding, "PrereqOrBuildings", GC.getNumBuildingClassInfos(), false);
	pXML->SetVariableListTagPair(&m_aiProductionTraits, "ProductionTraits", GC.getNumTraitInfos(), 0);
	pXML->GetChildXmlValByName(&m_iAIWeight, "iAIWeight");
	pXML->GetChildXmlValByName(&m_iHurryCostModifier, "iHurryCostModifier");
	pXML->GetChildXmlValByName(&m_iAdvancedStartCost, "iAdvancedStartCost");
	pXML->GetChildXmlValByName(&m_iAdvancedStartCostIncrease, "iAdvancedStartCostIncrease");
	pXML->GetChildXmlValByName(&m_iEuropeCost, "iEuropeCost");
	pXML->GetChildXmlValByName(&m_iEuropeCostIncrease, "iEuropeCostIncrease");
	pXML->GetChildXmlValByName(&m_iImmigrationWeight, "iImmigrationWeight");
	pXML->GetChildXmlValByName(&m_iImmigrationWeightDecay, "iImmigrationWeightDecay");
	pXML->GetChildXmlValByName(&m_iMinAreaSize, "iMinAreaSize");
	pXML->GetChildXmlValByName(&m_iMoves, "iMoves");
	pXML->GetChildXmlValByName(&m_iWorkRate, "iWorkRate");
	pXML->GetChildXmlValByName(&m_iWorkRateModifier, "iWorkRateModifier");
	pXML->GetChildXmlValByName(&m_iMissionaryRateModifier, "iMissionaryRateModifier");
	pXML->SetVariableListTagPair(&m_abTerrainImpassable, "TerrainImpassables", GC.getNumTerrainInfos(), false);
	pXML->SetVariableListTagPair(&m_abFeatureImpassable, "FeatureImpassables", GC.getNumFeatureInfos(), false);
	pXML->SetVariableListTagPair(&m_abEvasionBuilding, "EvasionBuildings", GC.getNumBuildingClassInfos(), false);
	pXML->GetChildXmlValByName(&m_iCombat, "iCombat");
	pXML->GetChildXmlValByName(&m_iXPValueAttack, "iXPValueAttack");
	pXML->GetChildXmlValByName(&m_iXPValueDefense, "iXPValueDefense");
	pXML->GetChildXmlValByName(&m_iWithdrawalProbability, "iWithdrawalProb");
	pXML->GetChildXmlValByName(&m_iCityAttackModifier, "iCityAttack");
	pXML->GetChildXmlValByName(&m_iCityDefenseModifier, "iCityDefense");
	pXML->GetChildXmlValByName(&m_iHillsAttackModifier, "iHillsAttack");
	pXML->GetChildXmlValByName(&m_iHillsDefenseModifier, "iHillsDefense");
	pXML->SetVariableListTagPair(&m_aiTerrainAttackModifier, "TerrainAttacks", GC.getNumTerrainInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiTerrainDefenseModifier, "TerrainDefenses", GC.getNumTerrainInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiFeatureAttackModifier, "FeatureAttacks", GC.getNumFeatureInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiFeatureDefenseModifier, "FeatureDefenses", GC.getNumFeatureInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiUnitClassAttackModifier, "UnitClassAttackMods", GC.getNumUnitClassInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiUnitClassDefenseModifier, "UnitClassDefenseMods", GC.getNumUnitClassInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiUnitCombatModifier, "UnitCombatMods", GC.getNumUnitCombatInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiDomainModifier, "DomainMods", NUM_DOMAIN_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiYieldModifier, "YieldModifiers", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiBonusYieldChange, "BonusYieldChanges", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiYieldChange, "YieldChanges", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiYieldCost, "YieldCosts", NUM_YIELD_TYPES, 0);
	pXML->GetChildXmlValByName(&m_iBombardRate, "iBombardRate");
	pXML->GetChildXmlValByName(szTextVal, "SpecialCargo");
	m_iSpecialCargo = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "DomainCargo");
	m_iDomainCargo = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iCargoSpace, "iCargo");
	pXML->GetChildXmlValByName(&m_iRequiredTransportSize, "iRequiredTransportSize");
	pXML->GetChildXmlValByName(&m_iAssetValue, "iAsset");
	pXML->GetChildXmlValByName(&m_iPowerValue, "iPower");
	// Read the mesh groups elements
	if ( gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"ProfessionMeshGroups") )
	{
		if ( gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"UnitMeshGroups") )
		{
			do
			{
				pXML->GetChildXmlValByName(szTextVal, "ProfessionType");
				ProfessionTypes eProfession = (ProfessionTypes) pXML->FindInInfoClass(szTextVal);
				int iMeleeWaveSize;
                pXML->GetChildXmlValByName( &iMeleeWaveSize, "iMeleeWaveSize" );
				int iRangedWaveSize;
				pXML->GetChildXmlValByName( &iRangedWaveSize, "iRangedWaveSize" );
				float fMaxSpeed;
				pXML->GetChildXmlValByName( &fMaxSpeed, "fMaxSpeed");
				float fPadTime;
				pXML->GetChildXmlValByName( &fPadTime, "fPadTime");
				CvUnitMeshGroups kMeshGroups(eProfession, iMeleeWaveSize, iRangedWaveSize, fMaxSpeed, fPadTime);
				if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "UnitMeshGroup"))
				{
					do
					{
						int iNumRequired;
						pXML->GetChildXmlValByName( &iNumRequired, "iRequired");
						pXML->GetChildXmlValByName( szTextVal, "ArtDefineTag");
						CvUnitMeshGroup kMeshGroup(iNumRequired, szTextVal);
						kMeshGroups.addMeshGroup(kMeshGroup);
					} while(gDLL->getXMLIFace()->NextSibling(pXML->GetXML()));
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
				m_aProfessionGroups.push_back(kMeshGroups);
			} while(gDLL->getXMLIFace()->NextSibling(pXML->GetXML()));
			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	pXML->GetChildXmlValByName(m_szFormationType, "FormationType");
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"UniqueNames"))
	{
		pXML->SetStringList(&m_paszUnitNames, &m_iNumUnitNames);
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	pXML->SetVariableListTagPair(&m_abFreePromotions, "FreePromotions", GC.getNumPromotionInfos(), false);
	pXML->GetChildXmlValByName(szTextVal, "LeaderPromotion");
	m_iLeaderPromotion = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iLeaderExperience, "iLeaderExperience");
	updateArtDefineButton();
	return true;
}
//======================================================================================================
//					CvUnitFormationInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvUnitFormationInfo()
//
//  \brief		Default Constructor
//
//------------------------------------------------------------------------------------------------------
CvUnitFormationInfo::CvUnitFormationInfo()
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvUnitFormationInfo()
//
//  \brief		Destructor
//
//------------------------------------------------------------------------------------------------------
CvUnitFormationInfo::~CvUnitFormationInfo()
{
}
const char* CvUnitFormationInfo::getFormationType() const
{
	return m_szFormationType;
}
const std::vector<EntityEventTypes> & CvUnitFormationInfo::getEventTypes() const
{
	return m_vctEventTypes;
}
int CvUnitFormationInfo::getNumUnitEntries() const
{
	return m_vctUnitEntries.size();
}
const CvUnitEntry &CvUnitFormationInfo::getUnitEntry(int index) const
{
	return m_vctUnitEntries[index];
}
void CvUnitFormationInfo::addUnitEntry(const CvUnitEntry &unitEntry)
{
	m_vctUnitEntries.push_back(unitEntry);
}
int CvUnitFormationInfo::getNumGreatUnitEntries() const
{
	return m_vctGreatUnitEntries.size();
}
const CvUnitEntry &CvUnitFormationInfo::getGreatUnitEntry(int index) const
{
	return m_vctGreatUnitEntries[index];
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvUnitFormationInfo()
//
//  \brief		Reads from XML
//
//------------------------------------------------------------------------------------------------------
bool CvUnitFormationInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	int iIndex;
	bool bNextSibling;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(m_szFormationType, "FormationType");
	if ( gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "EventMaskList" ))
	{
		if ( gDLL->getXMLIFace()->SetToChild( pXML->GetXML() ) )
		{
			pXML->GetXmlVal( szTextVal );
			do
			{
				iIndex = pXML->FindInInfoClass(szTextVal);
				if ( iIndex != -1 )
					m_vctEventTypes.push_back( (EntityEventTypes)iIndex );
				bNextSibling = pXML->GetNextXmlVal( &szTextVal );
			}
			while( bNextSibling );
			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	// Read the entries
	if ( gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "UnitEntry" ) )
	{
		do
		{
			CvUnitEntry unitEntry;
			pXML->GetChildXmlValByName(szTextVal, "UnitEntryType");
			if ( gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "Position" ) )
			{
				pXML->GetChildXmlValByName( &unitEntry.m_position.x, "x");
				pXML->GetChildXmlValByName( &unitEntry.m_position.y, "y");
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
			pXML->GetChildXmlValByName( &unitEntry.m_fRadius, "PositionRadius");
			pXML->GetChildXmlValByName( &unitEntry.m_fFacingDirection, "Direction");
			pXML->GetChildXmlValByName( &unitEntry.m_fFacingVariance, "DirVariation");
			if(szTextVal.CompareNoCase("Unit") == 0)
				m_vctUnitEntries.push_back(unitEntry);
			else if(szTextVal.CompareNoCase("General") == 0)
				m_vctGreatUnitEntries.push_back(unitEntry);
			else
			{
				FAssertMsg(false, "[Jason] Unknown unit formation entry type.");
			}
		}
		while ( gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "UnitEntry"));
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	FAssertMsg(m_vctGreatUnitEntries.size() > 0, "[Jason] Formation missing great general entry.");
	return true;
}

//======================================================================================================
//					CvSpecialUnitInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvSpecialUnitInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvSpecialUnitInfo::CvSpecialUnitInfo() :
m_bValid(false),
m_bCityLoad(false),
m_abCarrierUnitAITypes(NULL),
m_aiProductionTraits(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvSpecialUnitInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvSpecialUnitInfo::~CvSpecialUnitInfo()
{
	SAFE_DELETE_ARRAY(m_abCarrierUnitAITypes);
	SAFE_DELETE_ARRAY(m_aiProductionTraits);
}
bool CvSpecialUnitInfo::isValid() const
{
	return m_bValid;
}
bool CvSpecialUnitInfo::isCityLoad() const
{
	return m_bCityLoad;
}
// Arrays
bool CvSpecialUnitInfo::isCarrierUnitAIType(int i) const
{
	FAssertMsg(i < NUM_UNITAI_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abCarrierUnitAITypes ? m_abCarrierUnitAITypes[i] : -1;
}
int CvSpecialUnitInfo::getProductionTraits(int i) const
{
	FAssertMsg(i < GC.getNumTraitInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiProductionTraits ? m_aiProductionTraits[i] : -1;
}
bool CvSpecialUnitInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bValid, "bValid");
	pXML->GetChildXmlValByName(&m_bCityLoad, "bCityLoad");
	pXML->SetVariableListTagPair(&m_abCarrierUnitAITypes, "CarrierUnitAITypes", NUM_UNITAI_TYPES, false);
	pXML->SetVariableListTagPair(&m_aiProductionTraits, "ProductionTraits", GC.getNumTraitInfos(), 0);
	return true;
}
//======================================================================================================
//					CvCivicInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvCivicInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvCivicInfo::CvCivicInfo() :
m_iCivicOptionType(NO_CIVICOPTION),
m_iAIWeight(0),
m_iGreatGeneralRateModifier(0),
m_iDomesticGreatGeneralRateModifier(0),
m_iFreeExperience(0),
m_iWorkerSpeedModifier(0),
m_iImprovementUpgradeRateModifier(0),
m_iMilitaryProductionModifier(0),
m_iExpInBorderModifier(0),
m_iImmigrationConversion(YIELD_CROSSES),
m_iNativeAttitudeChange(0),
m_iNativeCombatModifier(0),
m_iFatherPointModifier(0),
m_bDominateNativeBorders(false),
m_bRevolutionEuropeTrade(false),
m_aiYieldModifier(NULL),
m_aiCapitalYieldModifier(NULL),
m_aiProfessionCombatChange(NULL),
m_pabHurry(NULL),
m_pabSpecialBuildingNotRequired(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvCivicInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvCivicInfo::~CvCivicInfo()
{
	SAFE_DELETE_ARRAY(m_aiYieldModifier);
	SAFE_DELETE_ARRAY(m_aiCapitalYieldModifier);
	SAFE_DELETE_ARRAY(m_aiProfessionCombatChange);
	SAFE_DELETE_ARRAY(m_pabHurry);
	SAFE_DELETE_ARRAY(m_pabSpecialBuildingNotRequired);
	for (uint iI=0;iI<m_aaiImprovementYieldChanges.size();iI++)
	{
		SAFE_DELETE_ARRAY(m_aaiImprovementYieldChanges[iI]);
	}
}
int CvCivicInfo::getCivicOptionType() const
{
	return m_iCivicOptionType;
}
int CvCivicInfo::getAIWeight() const
{
	return m_iAIWeight;
}
int CvCivicInfo::getGreatGeneralRateModifier() const
{
	return m_iGreatGeneralRateModifier;
}
int CvCivicInfo::getDomesticGreatGeneralRateModifier() const
{
	return m_iDomesticGreatGeneralRateModifier;
}
int CvCivicInfo::getFreeExperience() const
{
	return m_iFreeExperience;
}
int CvCivicInfo::getWorkerSpeedModifier() const
{
	return m_iWorkerSpeedModifier;
}
int CvCivicInfo::getImprovementUpgradeRateModifier() const
{
	return m_iImprovementUpgradeRateModifier;
}
int CvCivicInfo::getMilitaryProductionModifier() const
{
	return m_iMilitaryProductionModifier;
}
int CvCivicInfo::getExpInBorderModifier() const
{
	return m_iExpInBorderModifier;
}
int CvCivicInfo::getImmigrationConversion() const
{
	return m_iImmigrationConversion;
}
int CvCivicInfo::getNativeAttitudeChange() const
{
	return m_iNativeAttitudeChange;
}
int CvCivicInfo::getNativeCombatModifier() const
{
	return m_iNativeCombatModifier;
}
int CvCivicInfo::getFatherPointModifier() const
{
	return m_iFatherPointModifier;
}
bool CvCivicInfo::isDominateNativeBorders() const
{
	return m_bDominateNativeBorders;
}
bool CvCivicInfo::isRevolutionEuropeTrade() const
{
	return m_bRevolutionEuropeTrade;
}
// Arrays
int CvCivicInfo::getYieldModifier(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiYieldModifier ? m_aiYieldModifier[i] : -1;
}
int* CvCivicInfo::getYieldModifierArray() const
{
	return m_aiYieldModifier;
}
int CvCivicInfo::getCapitalYieldModifier(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiCapitalYieldModifier ? m_aiCapitalYieldModifier[i] : -1;
}
int CvCivicInfo::getProfessionCombatChange(int i) const
{
	FAssertMsg(i < GC.getNumProfessionInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiProfessionCombatChange ? m_aiProfessionCombatChange[i] : -1;
}
int* CvCivicInfo::getCapitalYieldModifierArray() const
{
	return m_aiCapitalYieldModifier;
}
bool CvCivicInfo::isHurry(int i) const
{
	FAssertMsg(i < GC.getNumHurryInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_pabHurry ? m_pabHurry[i] : false;
}
bool CvCivicInfo::isSpecialBuildingNotRequired(int i) const
{
	FAssertMsg(i < GC.getNumSpecialBuildingInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_pabSpecialBuildingNotRequired ? m_pabSpecialBuildingNotRequired[i] : false;
}
int CvCivicInfo::getImprovementYieldChanges(int i, int j) const
{
	FAssertMsg(i < GC.getNumImprovementInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_aaiImprovementYieldChanges[i][j];
}
int CvCivicInfo::getNumFreeUnitClasses() const
{
	return m_aFreeUnitClasses.size();
}
int CvCivicInfo::getFreeUnitClass(int i) const
{
	FAssert(i >= 0 && i < getNumFreeUnitClasses());
	return m_aFreeUnitClasses[i];
}
void CvCivicInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);		// flag for expansion
	stream->Read(&m_iCivicOptionType);
	stream->Read(&m_iAIWeight);
	stream->Read(&m_iGreatGeneralRateModifier);
	stream->Read(&m_iDomesticGreatGeneralRateModifier);
	stream->Read(&m_iFreeExperience);
	stream->Read(&m_iWorkerSpeedModifier);
	stream->Read(&m_iImprovementUpgradeRateModifier);
	stream->Read(&m_iMilitaryProductionModifier);
	stream->Read(&m_iExpInBorderModifier);
	stream->Read(&m_iImmigrationConversion);
	stream->Read(&m_iNativeAttitudeChange);
	stream->Read(&m_iNativeCombatModifier);
	stream->Read(&m_iFatherPointModifier);
	stream->Read(&m_bDominateNativeBorders);
	stream->Read(&m_bRevolutionEuropeTrade);
	// Arrays
	SAFE_DELETE_ARRAY(m_aiYieldModifier);
	m_aiYieldModifier = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiYieldModifier);
	SAFE_DELETE_ARRAY(m_aiCapitalYieldModifier);
	m_aiCapitalYieldModifier = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiCapitalYieldModifier);
	SAFE_DELETE_ARRAY(m_aiProfessionCombatChange);
	m_aiProfessionCombatChange = new int[GC.getNumProfessionInfos()];
	stream->Read(GC.getNumProfessionInfos(), m_aiProfessionCombatChange);
	SAFE_DELETE_ARRAY(m_pabHurry);
	m_pabHurry = new bool[GC.getNumHurryInfos()];
	stream->Read(GC.getNumHurryInfos(), m_pabHurry);
	SAFE_DELETE_ARRAY(m_pabSpecialBuildingNotRequired);
	m_pabSpecialBuildingNotRequired = new bool[GC.getNumSpecialBuildingInfos()];
	stream->Read(GC.getNumSpecialBuildingInfos(), m_pabSpecialBuildingNotRequired);
	for (uint iI=0;iI<m_aaiImprovementYieldChanges.size();iI++)
		{
		SAFE_DELETE_ARRAY(m_aaiImprovementYieldChanges[iI]);
		}
	m_aaiImprovementYieldChanges.clear();
	for(int i=0;i<GC.getNumImprovementInfos();i++)
	{
		m_aaiImprovementYieldChanges.push_back(new int[NUM_YIELD_TYPES]);
		stream->Read(NUM_YIELD_TYPES, m_aaiImprovementYieldChanges[i]);
	}

	int iNumFreeUnitClasses;
	stream->Read(&iNumFreeUnitClasses);
	if (iNumFreeUnitClasses > 0)
	{
		m_aFreeUnitClasses.resize(iNumFreeUnitClasses);
		stream->Read(iNumFreeUnitClasses, &m_aFreeUnitClasses[0]);
	}
}
void CvCivicInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_iCivicOptionType);
	stream->Write(m_iAIWeight);
	stream->Write(m_iGreatGeneralRateModifier);
	stream->Write(m_iDomesticGreatGeneralRateModifier);
	stream->Write(m_iFreeExperience);
	stream->Write(m_iWorkerSpeedModifier);
	stream->Write(m_iImprovementUpgradeRateModifier);
	stream->Write(m_iMilitaryProductionModifier);
	stream->Write(m_iExpInBorderModifier);
	stream->Write(m_iImmigrationConversion);
	stream->Write(m_iNativeAttitudeChange);
	stream->Write(m_iNativeCombatModifier);
	stream->Write(m_iFatherPointModifier);
	stream->Write(m_bDominateNativeBorders);
	stream->Write(m_bRevolutionEuropeTrade);
	// Arrays
	stream->Write(NUM_YIELD_TYPES, m_aiYieldModifier);
	stream->Write(NUM_YIELD_TYPES, m_aiCapitalYieldModifier);
	stream->Write(GC.getNumProfessionInfos(), m_aiProfessionCombatChange);
	stream->Write(GC.getNumHurryInfos(), m_pabHurry);
	stream->Write(GC.getNumSpecialBuildingInfos(), m_pabSpecialBuildingNotRequired);
	for(int i=0;i<GC.getNumImprovementInfos();i++)
	{
		stream->Write(NUM_YIELD_TYPES, m_aaiImprovementYieldChanges[i]);
	}

	stream->Write(getNumFreeUnitClasses());
	if (getNumFreeUnitClasses() > 0)
	{
		stream->Write(getNumFreeUnitClasses(), &m_aFreeUnitClasses[0]);
	}
}
bool CvCivicInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "CivicOptionType");
	m_iCivicOptionType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iAIWeight, "iAIWeight");
	pXML->GetChildXmlValByName(&m_iGreatGeneralRateModifier, "iGreatGeneralRateModifier");
	pXML->GetChildXmlValByName(&m_iDomesticGreatGeneralRateModifier, "iDomesticGreatGeneralRateModifier");
	pXML->GetChildXmlValByName(&m_iFreeExperience, "iFreeExperience");
	pXML->GetChildXmlValByName(&m_iWorkerSpeedModifier, "iWorkerSpeedModifier");
	pXML->GetChildXmlValByName(&m_iImprovementUpgradeRateModifier, "iImprovementUpgradeRateModifier");
	pXML->GetChildXmlValByName(&m_iMilitaryProductionModifier, "iMilitaryProductionModifier");
	pXML->GetChildXmlValByName(&m_iExpInBorderModifier, "iExpInBorderModifier");
	pXML->GetChildXmlValByName(szTextVal, "ImmigrationConversion");
	m_iImmigrationConversion = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iNativeAttitudeChange, "iNativeAttitudeChange");
	pXML->GetChildXmlValByName(&m_iNativeCombatModifier, "iNativeCombatModifier");
	pXML->GetChildXmlValByName(&m_iFatherPointModifier, "iFatherPointModifier");
	pXML->GetChildXmlValByName(&m_bDominateNativeBorders, "bDominateNativeBorders");
	pXML->GetChildXmlValByName(&m_bRevolutionEuropeTrade, "bRevolutionEuropeTrade");
	pXML->SetVariableListTagPair(&m_aiYieldModifier, "YieldModifiers", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiCapitalYieldModifier, "CapitalYieldModifiers", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiProfessionCombatChange, "ProfessionCombatChanges", GC.getNumProfessionInfos(), 0);
	pXML->SetVariableListTagPair(&m_pabHurry, "Hurrys", GC.getNumHurryInfos(), false);
	pXML->SetVariableListTagPair(&m_pabSpecialBuildingNotRequired, "SpecialBuildingNotRequireds", GC.getNumSpecialBuildingInfos(), false);
	// initialize the boolean list to the correct size and all the booleans to false
	FAssertMsg((GC.getNumImprovementInfos() > 0) && (NUM_YIELD_TYPES) > 0,"either the number of improvement infos is zero or less or the number of yield types is zero or less");
	pXML->Init2DIntList(m_aaiImprovementYieldChanges, GC.getNumImprovementInfos(), NUM_YIELD_TYPES);
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"ImprovementYieldChanges"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
			{
				if (0 < iNumSibs)
				{
					for (int j=0;j<iNumSibs;j++)
					{
						pXML->GetChildXmlValByName(szTextVal, "ImprovementType");
						int iIndex = pXML->FindInInfoClass(szTextVal);
						if (iIndex > -1)
						{
							// delete the array since it will be reallocated
							SAFE_DELETE_ARRAY(m_aaiImprovementYieldChanges[iIndex]);
							pXML->SetVariableListTagPair(&m_aaiImprovementYieldChanges[iIndex], "ImprovementYields", NUM_YIELD_TYPES, 0);
						}
						if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
						{
							break;
						}
					}
				}
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}

	int* aFreeUnitClasses = NULL;
	pXML->SetVariableListTagPair(&aFreeUnitClasses, "FreeUnitClasses", GC.getNumUnitClassInfos(), 0);
	for (int iUnitClass = 0; iUnitClass < GC.getNumUnitClassInfos(); ++iUnitClass)
	{
		for (int iFree = 0; iFree < aFreeUnitClasses[iUnitClass]; ++iFree)
		{
			m_aFreeUnitClasses.push_back((UnitClassTypes) iUnitClass);
		}
	}
	SAFE_DELETE_ARRAY(aFreeUnitClasses);

	return true;
}
//======================================================================================================
//					CvDiplomacyInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvDiplomacyInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvDiplomacyInfo::CvDiplomacyInfo()
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvDiplomacyInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvDiplomacyInfo::~CvDiplomacyInfo()
{
	uninit();
}
// note - Response member vars allocated by CvXmlLoadUtility
void CvDiplomacyInfo::uninit()
{
	for (std::vector<CvDiplomacyResponse*>::iterator it = m_pResponses.begin(); it != m_pResponses.end(); ++it)
	{
		SAFE_DELETE(*it);
	}
	m_pResponses.clear();
}
const CvDiplomacyResponse& CvDiplomacyInfo::getResponse(int iNum) const
{
	return *(m_pResponses[iNum]);
}
int CvDiplomacyInfo::getNumResponses() const
{
	return m_pResponses.size();
}
bool CvDiplomacyInfo::getCivilizationTypes(int i, int j) const
{
	FAssertMsg(i < getNumResponses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < GC.getNumCivilizationInfos(), "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_pResponses[i]->getCivilizationTypes(j);
}
bool CvDiplomacyInfo::getLeaderHeadTypes(int i, int j) const
{
	FAssertMsg(i < getNumResponses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < GC.getNumLeaderHeadInfos(), "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_pResponses[i]->getLeaderHeadTypes(j);
}
bool CvDiplomacyInfo::getAttitudeTypes(int i, int j) const
{
	FAssertMsg(i < getNumResponses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < NUM_ATTITUDE_TYPES, "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_pResponses[i]->getAttitudeTypes(j);
}
bool CvDiplomacyInfo::getDiplomacyPowerTypes(int i, int j) const
{
	FAssertMsg(i < getNumResponses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < NUM_DIPLOMACYPOWER_TYPES, "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_pResponses[i]->getDiplomacyPowerTypes(j);
}
int CvDiplomacyInfo::getNumDiplomacyText(int i) const
{
	FAssertMsg(i < getNumResponses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_pResponses[i]->getNumDiplomacyText();
}
const char* CvDiplomacyInfo::getDiplomacyText(int i, int j) const
{
	FAssertMsg(i < getNumResponses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < getNumDiplomacyText(i), "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_pResponses[i]->getDiplomacyText(j);
}
void CvDiplomacyInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);		// flag for expansion
	int iNumResponses;
	stream->Read(&iNumResponses);
	// Arrays
	uninit();
	for (int uiIndex = 0; uiIndex < iNumResponses; ++uiIndex)
	{
		CvDiplomacyResponse* pResponse = new CvDiplomacyResponse;
		pResponse->read(stream);
		m_pResponses.push_back(pResponse);
	}
}
void CvDiplomacyInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion
	int iNumResponses = m_pResponses.size();
	stream->Write(iNumResponses);
	// Arrays
	for (int uiIndex = 0; uiIndex < iNumResponses; ++uiIndex)
	{
		m_pResponses[uiIndex]->write(stream);
	}
}
bool CvDiplomacyInfo::read(CvXMLLoadUtility* pXML)
{
	int i;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	uninit();
	if ( gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"Responses") )
	{
		int iNewResponses = gDLL->getXMLIFace()->NumOfChildrenByTagName(pXML->GetXML(), "Response");
		gDLL->getXMLIFace()->SetToChild(pXML->GetXML());
		for (i = 0; i < iNewResponses; i++)
		{
			CvDiplomacyResponse* pNewResponse = new CvDiplomacyResponse;
			pNewResponse->read(pXML);
			m_pResponses.push_back(pNewResponse);
			if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
			{
				break;
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	return true;
}
//======================================================================================================
//					CvUnitClassInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvUnitClassInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvUnitClassInfo::CvUnitClassInfo() :
m_iDefaultUnitIndex(NO_UNIT)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvUnitClassInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvUnitClassInfo::~CvUnitClassInfo()
{
}
int CvUnitClassInfo::getDefaultUnitIndex() const
{
	return m_iDefaultUnitIndex;
}
void CvUnitClassInfo::setDefaultUnitIndex(int i)
{
	m_iDefaultUnitIndex = i;
}
bool CvUnitClassInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "DefaultUnit");
	m_aszExtraXMLforPass3.push_back(szTextVal);
	return true;
}
bool CvUnitClassInfo::readPass3()
{
	if (m_aszExtraXMLforPass3.size() < 1)
	{
		FAssert(false);
		return false;
	}
	m_iDefaultUnitIndex = GC.getInfoTypeForString(m_aszExtraXMLforPass3[0]);
	m_aszExtraXMLforPass3.clear();
	return true;
}

//======================================================================================================
//					CvBuildingInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvBuildingInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvBuildingInfo::CvBuildingInfo() :
m_iBuildingClassType(NO_BUILDINGCLASS),
m_iVictoryPrereq(NO_VICTORY),
m_iFreeStartEra(NO_ERA),
m_iMaxStartEra(NO_ERA),
m_iFreePromotion(NO_PROMOTION),
m_iAIWeight(0),
m_iHurryCostModifier(0),
m_iAdvancedStartCost(0),
m_iAdvancedStartCostIncrease(0),
m_iProfessionOutput(0),
m_iMaxWorkers(0),
m_iMinAreaSize(0),
m_iNumCitiesPrereq(0),
m_iNumTeamsPrereq(0),
m_iUnitLevelPrereq(0),
m_iMinLatitude(0),
m_iMaxLatitude(90),
m_iFreeExperience(0),
m_iFoodKept(0),
m_iMilitaryProductionModifier(0),
m_iAssetValue(0),
m_iPowerValue(0),
m_iYieldStorage(0),
m_iSpecialBuildingType(NO_SPECIALBUILDING),
m_iNextSpecialBuilding(NO_BUILDING),
m_iConquestProbability(0),
m_iHealRateChange(0),
m_iDefenseModifier(0),
m_iBombardDefenseModifier(0),
m_iMissionType(NO_MISSION),
m_iOverflowSellPercent(0),
m_iSpecialBuildingPriority(0),
m_fVisibilityPriority(0.0f),
m_bWorksWater(false),
m_bWater(false),
m_bRiver(false),
m_bCapital(false),
m_bNeverCapture(false),
m_bCenterInCity(false),
m_aiProductionTraits(NULL),
m_aiSeaPlotYieldChange(NULL),
m_aiRiverPlotYieldChange(NULL),
m_aiYieldChange(NULL),
m_aiYieldModifier(NULL),
m_aiUnitCombatFreeExperience(NULL),
m_aiDomainFreeExperience(NULL),
m_aiDomainProductionModifier(NULL),
m_aiPrereqNumOfBuildingClass(NULL),
m_aiYieldCost(NULL),
m_abBuildingClassNeededInCity(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvBuildingInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvBuildingInfo::~CvBuildingInfo()
{
	SAFE_DELETE_ARRAY(m_aiProductionTraits);
	SAFE_DELETE_ARRAY(m_aiSeaPlotYieldChange);
	SAFE_DELETE_ARRAY(m_aiRiverPlotYieldChange);
	SAFE_DELETE_ARRAY(m_aiYieldChange);
	SAFE_DELETE_ARRAY(m_aiYieldModifier);
	SAFE_DELETE_ARRAY(m_aiUnitCombatFreeExperience);
	SAFE_DELETE_ARRAY(m_aiDomainFreeExperience);
	SAFE_DELETE_ARRAY(m_aiDomainProductionModifier);
	SAFE_DELETE_ARRAY(m_aiPrereqNumOfBuildingClass);
	SAFE_DELETE_ARRAY(m_aiYieldCost);
	SAFE_DELETE_ARRAY(m_abBuildingClassNeededInCity);
}
int CvBuildingInfo::getBuildingClassType() const
{
	return m_iBuildingClassType;
}
int CvBuildingInfo::getVictoryPrereq() const
{
	return m_iVictoryPrereq;
}
int CvBuildingInfo::getFreeStartEra() const
{
	return m_iFreeStartEra;
}
int CvBuildingInfo::getMaxStartEra() const
{
	return m_iMaxStartEra;
}
int CvBuildingInfo::getFreePromotion() const
{
	return m_iFreePromotion;
}
int CvBuildingInfo::getAIWeight() const
{
	return m_iAIWeight;
}
int CvBuildingInfo::getHurryCostModifier() const
{
	return m_iHurryCostModifier;
}
int CvBuildingInfo::getAdvancedStartCost() const
{
	return m_iAdvancedStartCost;
}
int CvBuildingInfo::getAdvancedStartCostIncrease() const
{
	return m_iAdvancedStartCostIncrease;
}
int CvBuildingInfo::getProfessionOutput() const
{
	return m_iProfessionOutput;
}
int CvBuildingInfo::getMaxWorkers() const
{
	return m_iMaxWorkers;
}
int CvBuildingInfo::getMinAreaSize() const
{
	return m_iMinAreaSize;
}
int CvBuildingInfo::getNumCitiesPrereq() const
{
	return m_iNumCitiesPrereq;
}
int CvBuildingInfo::getNumTeamsPrereq() const
{
	return m_iNumTeamsPrereq;
}
int CvBuildingInfo::getUnitLevelPrereq() const
{
	return m_iUnitLevelPrereq;
}
int CvBuildingInfo::getMinLatitude() const
{
	return m_iMinLatitude;
}
int CvBuildingInfo::getMaxLatitude() const
{
	return m_iMaxLatitude;
}
int CvBuildingInfo::getFreeExperience() const
{
	return m_iFreeExperience;
}
int CvBuildingInfo::getFoodKept() const
{
	return m_iFoodKept;
}
int CvBuildingInfo::getMilitaryProductionModifier() const
{
	return m_iMilitaryProductionModifier;
}
int CvBuildingInfo::getAssetValue() const
{
	return m_iAssetValue;
}
int CvBuildingInfo::getPowerValue() const
{
	return m_iPowerValue;
}
int CvBuildingInfo::getYieldStorage() const
{
	return m_iYieldStorage;
}
int CvBuildingInfo::getSpecialBuildingType() const
{
	return m_iSpecialBuildingType;
}
int CvBuildingInfo::getNextSpecialBuilding() const
{
	return m_iNextSpecialBuilding;
}
int CvBuildingInfo::getConquestProbability() const
{
	return m_iConquestProbability;
}
int CvBuildingInfo::getHealRateChange() const
{
	return m_iHealRateChange;
}
int CvBuildingInfo::getDefenseModifier() const
{
	return m_iDefenseModifier;
}
int CvBuildingInfo::getBombardDefenseModifier() const
{
	return m_iBombardDefenseModifier;
}
int CvBuildingInfo::getMissionType() const
{
	return m_iMissionType;
}
void CvBuildingInfo::setMissionType(int iNewType)
{
	m_iMissionType = iNewType;
}
int CvBuildingInfo::getOverflowSellPercent() const
{
	return m_iOverflowSellPercent;
}
int CvBuildingInfo::getSpecialBuildingPriority() const
{
	return m_iSpecialBuildingPriority;
}
float CvBuildingInfo::getVisibilityPriority() const
{
	return m_fVisibilityPriority;
}
bool CvBuildingInfo::isWater() const
{
	return m_bWater;
}
bool CvBuildingInfo::isWorksWater() const
{
	return m_bWorksWater;
}
bool CvBuildingInfo::isRiver() const
{
	return m_bRiver;
}
bool CvBuildingInfo::isCapital() const
{
	return m_bCapital;
}
bool CvBuildingInfo::isNeverCapture() const
{
	return m_bNeverCapture;
}
bool CvBuildingInfo::isCenterInCity() const
{
	return m_bCenterInCity;
}
const char* CvBuildingInfo::getConstructSound() const
{
	return m_szConstructSound;
}
void CvBuildingInfo::setConstructSound(const char* szVal)
{
	m_szConstructSound = szVal;
}
const char* CvBuildingInfo::getArtDefineTag() const
{
	return m_szArtDefineTag;
}
void CvBuildingInfo::setArtDefineTag(const char* szVal)
{
	m_szArtDefineTag = szVal;
}
const char* CvBuildingInfo::getMovieDefineTag() const
{
	return m_szMovieDefineTag;
}
void CvBuildingInfo::setMovieDefineTag(const char* szVal)
{
	m_szMovieDefineTag = szVal;
}
// Arrays
int CvBuildingInfo::getYieldChange(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiYieldChange ? m_aiYieldChange[i] : -1;
}
int* CvBuildingInfo::getYieldChangeArray() const
{
	return m_aiYieldChange;
}
int CvBuildingInfo::getYieldModifier(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiYieldModifier ? m_aiYieldModifier[i] : -1;
}
int* CvBuildingInfo::getYieldModifierArray() const
{
	return m_aiYieldModifier;
}
int CvBuildingInfo::getSeaPlotYieldChange(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiSeaPlotYieldChange ? m_aiSeaPlotYieldChange[i] : -1;
}
int* CvBuildingInfo::getSeaPlotYieldChangeArray() const
{
	return m_aiSeaPlotYieldChange;
}
int CvBuildingInfo::getRiverPlotYieldChange(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiRiverPlotYieldChange ? m_aiRiverPlotYieldChange[i] : -1;
}
int* CvBuildingInfo::getRiverPlotYieldChangeArray() const
{
	return m_aiRiverPlotYieldChange;
}
int CvBuildingInfo::getUnitCombatFreeExperience(int i) const
{
	FAssertMsg(i < GC.getNumUnitCombatInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiUnitCombatFreeExperience ? m_aiUnitCombatFreeExperience[i] : -1;
}
int CvBuildingInfo::getDomainFreeExperience(int i) const
{
	FAssertMsg(i < NUM_DOMAIN_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiDomainFreeExperience ? m_aiDomainFreeExperience[i] : -1;
}
int CvBuildingInfo::getDomainProductionModifier(int i) const
{
	FAssertMsg(i < NUM_DOMAIN_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiDomainProductionModifier ? m_aiDomainProductionModifier[i] : -1;
}
int CvBuildingInfo::getProductionTraits(int i) const
{
	FAssertMsg(i < GC.getNumTraitInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiProductionTraits ? m_aiProductionTraits[i] : -1;
}
int CvBuildingInfo::getPrereqNumOfBuildingClass(int i) const
{
	FAssertMsg(i < GC.getNumBuildingClassInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiPrereqNumOfBuildingClass ? m_aiPrereqNumOfBuildingClass[i] : -1;
}
int CvBuildingInfo::getYieldCost(int i) const
{
	FAssert(i < NUM_YIELD_TYPES && i >= 0);
	return m_aiYieldCost ? m_aiYieldCost[i] : -1;
}
bool CvBuildingInfo::isBuildingClassNeededInCity(int i) const
{
	FAssertMsg(i < GC.getNumBuildingClassInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abBuildingClassNeededInCity ? m_abBuildingClassNeededInCity[i] : false;
}
const char* CvBuildingInfo::getButton() const
{
	const CvArtInfoBuilding * pBuildingArtInfo;
	pBuildingArtInfo = getArtInfo();
	if (pBuildingArtInfo != NULL)
	{
		return pBuildingArtInfo->getButton();
	}
	else
	{
		return NULL;
	}
}
const CvArtInfoBuilding* CvBuildingInfo::getArtInfo() const
{
	return ARTFILEMGR.getBuildingArtInfo(getArtDefineTag());
}
const CvArtInfoMovie* CvBuildingInfo::getMovieInfo() const
{
	const char* pcTag = getMovieDefineTag();
	if (NULL != pcTag && 0 != _tcscmp(pcTag, "NONE"))
	{
		return ARTFILEMGR.getMovieArtInfo(pcTag);
	}
	else
	{
		return NULL;
	}
}
const char* CvBuildingInfo::getMovie() const
{
	const CvArtInfoMovie* pArt;
	pArt = getMovieInfo();
	if (pArt != NULL)
	{
		return pArt->getPath();
	}
	else
	{
		return NULL;
	}
}

//
// serialization
//
void CvBuildingInfo::read(FDataStreamBase* stream)
{
	CvHotkeyInfo::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);	// flags for expansion
	stream->Read(&m_iBuildingClassType);
	stream->Read(&m_iVictoryPrereq);
	stream->Read(&m_iFreeStartEra);
	stream->Read(&m_iMaxStartEra);
	stream->Read(&m_iFreePromotion);
	stream->Read(&m_iAIWeight);
	stream->Read(&m_iHurryCostModifier);
	stream->Read(&m_iAdvancedStartCost);
	stream->Read(&m_iAdvancedStartCostIncrease);
	stream->Read(&m_iProfessionOutput);
	stream->Read(&m_iMaxWorkers);
	stream->Read(&m_iMinAreaSize);
	stream->Read(&m_iNumCitiesPrereq);
	stream->Read(&m_iNumTeamsPrereq);
	stream->Read(&m_iUnitLevelPrereq);
	stream->Read(&m_iMinLatitude);
	stream->Read(&m_iMaxLatitude);
	stream->Read(&m_iFreeExperience);
	stream->Read(&m_iFoodKept);
	stream->Read(&m_iMilitaryProductionModifier);
	stream->Read(&m_iAssetValue);
	stream->Read(&m_iPowerValue);
	stream->Read(&m_iYieldStorage);
	stream->Read(&m_iSpecialBuildingType);
	stream->Read(&m_iNextSpecialBuilding);
	stream->Read(&m_iConquestProbability);
	stream->Read(&m_iHealRateChange);
	stream->Read(&m_iDefenseModifier);
	stream->Read(&m_iBombardDefenseModifier);
	stream->Read(&m_iMissionType);
	stream->Read(&m_iOverflowSellPercent);
	stream->Read(&m_iSpecialBuildingPriority);
	stream->Read(&m_fVisibilityPriority);
	stream->Read(&m_bWorksWater);
	stream->Read(&m_bWater);
	stream->Read(&m_bRiver);
	stream->Read(&m_bCapital);
	stream->Read(&m_bNeverCapture);
	stream->Read(&m_bCenterInCity);
	stream->ReadString(m_szConstructSound);
	stream->ReadString(m_szArtDefineTag);
	stream->ReadString(m_szMovieDefineTag);
	SAFE_DELETE_ARRAY(m_aiProductionTraits);
	m_aiProductionTraits = new int[GC.getNumTraitInfos()];
	stream->Read(GC.getNumTraitInfos(), m_aiProductionTraits);
	SAFE_DELETE_ARRAY(m_aiSeaPlotYieldChange);
	m_aiSeaPlotYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiSeaPlotYieldChange);
	SAFE_DELETE_ARRAY(m_aiRiverPlotYieldChange);
	m_aiRiverPlotYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiRiverPlotYieldChange);
	SAFE_DELETE_ARRAY(m_aiYieldChange);
	m_aiYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiYieldChange);
	SAFE_DELETE_ARRAY(m_aiYieldModifier);
	m_aiYieldModifier = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiYieldModifier);
	SAFE_DELETE_ARRAY(m_aiUnitCombatFreeExperience);
	m_aiUnitCombatFreeExperience = new int[GC.getNumUnitCombatInfos()];
	stream->Read(GC.getNumUnitCombatInfos(), m_aiUnitCombatFreeExperience);
	SAFE_DELETE_ARRAY(m_aiDomainFreeExperience);
	m_aiDomainFreeExperience = new int[NUM_DOMAIN_TYPES];
	stream->Read(NUM_DOMAIN_TYPES, m_aiDomainFreeExperience);
	SAFE_DELETE_ARRAY(m_aiDomainProductionModifier);
	m_aiDomainProductionModifier = new int[NUM_DOMAIN_TYPES];
	stream->Read(NUM_DOMAIN_TYPES, m_aiDomainProductionModifier);
	SAFE_DELETE_ARRAY(m_aiPrereqNumOfBuildingClass);
	m_aiPrereqNumOfBuildingClass = new int[GC.getNumBuildingClassInfos()];
	stream->Read(GC.getNumBuildingClassInfos(), m_aiPrereqNumOfBuildingClass);
	SAFE_DELETE_ARRAY(m_aiYieldCost);
	m_aiYieldCost = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiYieldCost);
	SAFE_DELETE_ARRAY(m_abBuildingClassNeededInCity);
	m_abBuildingClassNeededInCity = new bool[GC.getNumBuildingClassInfos()];
	stream->Read(GC.getNumBuildingClassInfos(), m_abBuildingClassNeededInCity);
}
//
// serialization
//
void CvBuildingInfo::write(FDataStreamBase* stream)
{
	CvHotkeyInfo::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_iBuildingClassType);
	stream->Write(m_iVictoryPrereq);
	stream->Write(m_iFreeStartEra);
	stream->Write(m_iMaxStartEra);
	stream->Write(m_iFreePromotion);
	stream->Write(m_iAIWeight);
	stream->Write(m_iHurryCostModifier);
	stream->Write(m_iAdvancedStartCost);
	stream->Write(m_iAdvancedStartCostIncrease);
	stream->Write(m_iProfessionOutput);
	stream->Write(m_iMaxWorkers);
	stream->Write(m_iMinAreaSize);
	stream->Write(m_iNumCitiesPrereq);
	stream->Write(m_iNumTeamsPrereq);
	stream->Write(m_iUnitLevelPrereq);
	stream->Write(m_iMinLatitude);
	stream->Write(m_iMaxLatitude);
	stream->Write(m_iFreeExperience);
	stream->Write(m_iFoodKept);
	stream->Write(m_iMilitaryProductionModifier);
	stream->Write(m_iAssetValue);
	stream->Write(m_iPowerValue);
	stream->Write(m_iYieldStorage);
	stream->Write(m_iSpecialBuildingType);
	stream->Write(m_iNextSpecialBuilding);
	stream->Write(m_iConquestProbability);
	stream->Write(m_iHealRateChange);
	stream->Write(m_iDefenseModifier);
	stream->Write(m_iBombardDefenseModifier);
	stream->Write(m_iMissionType);
	stream->Write(m_iOverflowSellPercent);
	stream->Write(m_iSpecialBuildingPriority);
	stream->Write(m_fVisibilityPriority);
	stream->Write(m_bWorksWater);
	stream->Write(m_bWater);
	stream->Write(m_bRiver);
	stream->Write(m_bCapital);
	stream->Write(m_bNeverCapture);
	stream->Write(m_bCenterInCity);
	stream->WriteString(m_szConstructSound);
	stream->WriteString(m_szArtDefineTag);
	stream->WriteString(m_szMovieDefineTag);
	stream->Write(GC.getNumTraitInfos(), m_aiProductionTraits);
	stream->Write(NUM_YIELD_TYPES, m_aiSeaPlotYieldChange);
	stream->Write(NUM_YIELD_TYPES, m_aiRiverPlotYieldChange);
	stream->Write(NUM_YIELD_TYPES, m_aiYieldChange);
	stream->Write(NUM_YIELD_TYPES, m_aiYieldModifier);
	stream->Write(GC.getNumUnitCombatInfos(), m_aiUnitCombatFreeExperience);
	stream->Write(NUM_DOMAIN_TYPES, m_aiDomainFreeExperience);
	stream->Write(NUM_DOMAIN_TYPES, m_aiDomainProductionModifier);
	stream->Write(GC.getNumBuildingClassInfos(), m_aiPrereqNumOfBuildingClass);
	stream->Write(NUM_YIELD_TYPES, m_aiYieldCost);
	stream->Write(GC.getNumBuildingClassInfos(), m_abBuildingClassNeededInCity);
}
//
// read from XML
//
bool CvBuildingInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvHotkeyInfo::read(pXML))
	{
		return false;
	}
	int j=0;						//loop counter
	int k=0;						//loop counter
	int iNumSibs=0;				// the number of siblings the current xml node has
	pXML->GetChildXmlValByName(szTextVal, "BuildingClass");
	m_iBuildingClassType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "SpecialBuildingType");
	m_iSpecialBuildingType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "ArtDefineTag");
	setArtDefineTag(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "MovieDefineTag");
	setMovieDefineTag(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "VictoryPrereq");
	m_iVictoryPrereq = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "FreeStartEra");
	m_iFreeStartEra = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "MaxStartEra");
	m_iMaxStartEra = pXML->FindInInfoClass(szTextVal);
	pXML->SetVariableListTagPair(&m_aiProductionTraits, "ProductionTraits", GC.getNumTraitInfos(), 0);
	pXML->GetChildXmlValByName(szTextVal, "FreePromotion");
	m_iFreePromotion = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_bWorksWater, "bWorksWater");
	pXML->GetChildXmlValByName(&m_bWater, "bWater");
	pXML->GetChildXmlValByName(&m_bRiver, "bRiver");
	pXML->GetChildXmlValByName(&m_bCapital, "bCapital");
	pXML->GetChildXmlValByName(&m_bNeverCapture, "bNeverCapture");
	pXML->GetChildXmlValByName(&m_bCenterInCity, "bCenterInCity");
	pXML->GetChildXmlValByName(&m_iAIWeight, "iAIWeight");
	pXML->GetChildXmlValByName(&m_iHurryCostModifier, "iHurryCostModifier");
	pXML->GetChildXmlValByName(&m_iAdvancedStartCost, "iAdvancedStartCost");
	pXML->GetChildXmlValByName(&m_iAdvancedStartCostIncrease, "iAdvancedStartCostIncrease");
	pXML->GetChildXmlValByName(&m_iProfessionOutput, "iProfessionOutput");
	pXML->GetChildXmlValByName(&m_iMaxWorkers, "iMaxWorkers");
	pXML->GetChildXmlValByName(&m_iMinAreaSize, "iMinAreaSize");
	pXML->GetChildXmlValByName(&m_iConquestProbability, "iConquestProb");
	pXML->GetChildXmlValByName(&m_iNumCitiesPrereq, "iCitiesPrereq");
	pXML->GetChildXmlValByName(&m_iNumTeamsPrereq, "iTeamsPrereq");
	pXML->GetChildXmlValByName(&m_iUnitLevelPrereq, "iLevelPrereq");
	pXML->GetChildXmlValByName(&m_iMinLatitude, "iMinLatitude");
	pXML->GetChildXmlValByName(&m_iMaxLatitude, "iMaxLatitude");
	pXML->GetChildXmlValByName(&m_iFreeExperience, "iExperience");
	pXML->GetChildXmlValByName(&m_iFoodKept, "iFoodKept");
	pXML->GetChildXmlValByName(&m_iHealRateChange, "iHealRateChange");
	pXML->GetChildXmlValByName(&m_iMilitaryProductionModifier, "iMilitaryProductionModifier");
	pXML->GetChildXmlValByName(&m_iDefenseModifier, "iDefense");
	pXML->GetChildXmlValByName(&m_iBombardDefenseModifier, "iBombardDefense");
	pXML->GetChildXmlValByName(&m_iOverflowSellPercent, "iOverflowSellPercent");
	pXML->GetChildXmlValByName(&m_iSpecialBuildingPriority, "iSpecialBuildingPriority");
	pXML->GetChildXmlValByName(&m_iAssetValue, "iAsset");
	pXML->GetChildXmlValByName(&m_iPowerValue, "iPower");
	pXML->GetChildXmlValByName(&m_iYieldStorage, "iYieldStorage");
	pXML->GetChildXmlValByName(&m_fVisibilityPriority, "fVisibilityPriority");
	pXML->SetVariableListTagPair(&m_aiSeaPlotYieldChange, "SeaPlotYieldChanges", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiRiverPlotYieldChange, "RiverPlotYieldChanges", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiYieldChange, "YieldChanges", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiYieldModifier, "YieldModifiers", NUM_YIELD_TYPES, 0);
	pXML->GetChildXmlValByName(szTextVal, "ConstructSound");
	setConstructSound(szTextVal);
	pXML->SetVariableListTagPair(&m_aiUnitCombatFreeExperience, "UnitCombatFreeExperiences", GC.getNumUnitCombatInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiDomainFreeExperience, "DomainFreeExperiences", NUM_DOMAIN_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiDomainProductionModifier, "DomainProductionModifiers", NUM_DOMAIN_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiPrereqNumOfBuildingClass, "PrereqBuildingClasses", GC.getNumBuildingClassInfos(), 0);
	pXML->SetVariableListTagPair(&m_abBuildingClassNeededInCity, "BuildingClassNeededs", GC.getNumBuildingClassInfos(), false);
	pXML->SetVariableListTagPair(&m_aiYieldCost, "YieldCosts", NUM_YIELD_TYPES, 0);
	return true;
}

bool CvBuildingInfo::readPass2(CvXMLLoadUtility* pXML)
{
	m_iNextSpecialBuilding = GC.getInfoTypeForString(getType());
	if(getSpecialBuildingType() != NO_SPECIALBUILDING)
	{
		for(int i=0;i<GC.getNumBuildingInfos();i++)
		{
			BuildingTypes eLoopBuilding = (BuildingTypes) ((m_iNextSpecialBuilding + i + 1) % GC.getNumBuildingInfos());
			if(GC.getBuildingInfo(eLoopBuilding).getSpecialBuildingType() == getSpecialBuildingType())
			{
				m_iNextSpecialBuilding = eLoopBuilding;
				break;
			}
		}
	}

	return true;
}
//======================================================================================================
//					CvSpecialBuildingInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvSpecialBuildingInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvSpecialBuildingInfo::CvSpecialBuildingInfo() :
m_bValid(false),
m_iChar(0),
m_iFontButtonIndex(0),
m_aiProductionTraits(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvSpecialBuildingInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvSpecialBuildingInfo::~CvSpecialBuildingInfo()
{
	SAFE_DELETE_ARRAY(m_aiProductionTraits);
}
bool CvSpecialBuildingInfo::isValid() const
{
	return m_bValid;
}
int CvSpecialBuildingInfo::getChar() const
{
	return m_iChar;
}
void CvSpecialBuildingInfo::setChar(int i)
{
	m_iChar = i;
}
int CvSpecialBuildingInfo::getFontButtonIndex() const
{
	return m_iFontButtonIndex;
}
// Arrays
int CvSpecialBuildingInfo::getProductionTraits(int i) const
{
	FAssertMsg(i < GC.getNumTraitInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiProductionTraits ? m_aiProductionTraits[i] : -1;
}
bool CvSpecialBuildingInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bValid, "bValid");
	pXML->GetChildXmlValByName(&m_iFontButtonIndex, "FontButtonIndex");
	pXML->SetVariableListTagPair(&m_aiProductionTraits, "ProductionTraits", GC.getNumTraitInfos(), 0);
	return true;
}
//======================================================================================================
//					CvBuildingClassInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvBuildingClassInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvBuildingClassInfo::CvBuildingClassInfo() :
m_iDefaultBuildingIndex(NO_BUILDING),
m_aiVictoryThreshold(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvBuildingClassInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvBuildingClassInfo::~CvBuildingClassInfo()
{
	SAFE_DELETE_ARRAY(m_aiVictoryThreshold);
}
int CvBuildingClassInfo::getDefaultBuildingIndex() const
{
	return m_iDefaultBuildingIndex;
}
void CvBuildingClassInfo::setDefaultBuildingIndex(int i)
{
	m_iDefaultBuildingIndex = i;
}
// Arrays
int CvBuildingClassInfo::getVictoryThreshold(int i) const
{
	FAssertMsg(i < GC.getNumVictoryInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiVictoryThreshold ? m_aiVictoryThreshold[i] : -1;
}
bool CvBuildingClassInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->SetVariableListTagPair(&m_aiVictoryThreshold, "VictoryThresholds", GC.getNumVictoryInfos(), 0);
	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "DefaultBuilding");
	m_aszExtraXMLforPass3.push_back(szTextVal);
	return true;
}
bool CvBuildingClassInfo::readPass3()
{
	if (m_aszExtraXMLforPass3.size() < 1)
	{
		FAssert(false);
		return false;
	}
	m_iDefaultBuildingIndex = GC.getInfoTypeForString(m_aszExtraXMLforPass3[0]);
	m_aszExtraXMLforPass3.clear();
	return true;
}

//======================================================================================================
//					CvRiverModelInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvRiverModelInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvRiverModelInfo::CvRiverModelInfo() :
m_iTextureIndex(0)
{
	m_szDeltaString[0] = '\0';
	m_szConnectString[0] = '\0';
	m_szRotateString[0] = '\0';
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvRiverModelInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvRiverModelInfo::~CvRiverModelInfo()
{
}
const char* CvRiverModelInfo::getModelFile() const
{
	return m_szModelFile;
}
void CvRiverModelInfo::setModelFile(const char* szVal)					// The model filename
{
	m_szModelFile=szVal;
}
const char* CvRiverModelInfo::getBorderFile() const
{
	return m_szBorderFile;
}
void CvRiverModelInfo::setBorderFile(const char* szVal)					// The model filename
{
	m_szBorderFile=szVal;
}
int CvRiverModelInfo::getTextureIndex() const
{
	return m_iTextureIndex;
}
const char* CvRiverModelInfo::getDeltaString() const
{
	return m_szDeltaString;
}
const char* CvRiverModelInfo::getConnectString() const
{
	return m_szConnectString;
}
const char* CvRiverModelInfo::getRotateString() const
{
	return m_szRotateString;
}
bool CvRiverModelInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	if(pXML->GetChildXmlValByName(szTextVal, "ModelFile"))
	{
		setModelFile(szTextVal);
	}
	if(pXML->GetChildXmlValByName(szTextVal, "BorderFile"))
	{
		setBorderFile(szTextVal);
	}
	pXML->GetChildXmlValByName(&m_iTextureIndex, "TextureIndex");
	pXML->GetChildXmlValByName(m_szDeltaString, "DeltaType");
	pXML->GetChildXmlValByName(m_szConnectString, "Connections");
	pXML->GetChildXmlValByName(m_szRotateString, "Rotations");
	return true;
}
//======================================================================================================
//					CvRouteModelInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvRouteModelInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvRouteModelInfo::CvRouteModelInfo() :
m_eRouteType(NO_ROUTE)
{
	m_szConnectString[0] = '\0';
	m_szModelConnectString[0] = '\0';
	m_szRotateString[0] = '\0';
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvRouteModelInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvRouteModelInfo::~CvRouteModelInfo()
{
}
RouteTypes CvRouteModelInfo::getRouteType() const		// The route type
{
	return m_eRouteType;
}
const char* CvRouteModelInfo::getModelFile() const
{
	return m_szModelFile;
}
void CvRouteModelInfo::setModelFile(const char* szVal)				// The model filename
{
	m_szModelFile=szVal;
}
const char* CvRouteModelInfo::getConnectString() const
{
	return m_szConnectString;
}
const char* CvRouteModelInfo::getModelConnectString() const
{
	return m_szModelConnectString;
}
const char* CvRouteModelInfo::getRotateString() const
{
	return m_szRotateString;
}
bool CvRouteModelInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "ModelFile");
	setModelFile(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "RouteType");
	m_eRouteType = (RouteTypes)(pXML->FindInInfoClass(szTextVal));
	pXML->GetChildXmlValByName(m_szConnectString, "Connections");
	pXML->GetChildXmlValByName(m_szModelConnectString, "ModelConnections");
	pXML->GetChildXmlValByName(m_szRotateString, "Rotations");
	return true;
}
//======================================================================================================
//					CvCivilizationInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvCivilizationInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvCivilizationInfo::CvCivilizationInfo():
m_iDefaultPlayerColor(NO_PLAYERCOLOR),
m_iArtStyleType(NO_ARTSTYLE),
m_iNumCityNames(0),
m_iNumLeaders(0),
m_iSelectionSoundScriptId(0),
m_iActionSoundScriptId(0),
m_iDerivativeCiv(NO_CIVILIZATION),
m_iAdvancedStartPoints(0),
m_iAreaMultiplier(0),
m_iDensityMultiplier(0),
m_iTreasure(0),
m_iFavoredTerrain(NO_TERRAIN),
m_iCapturedCityUnitClass(NO_UNITCLASS),
m_iDefaultProfession(NO_PROFESSION),
m_iMissionaryChar(0),
m_bPlayable(false),
m_bAIPlayable(false),
m_bWaterStart(false),
m_bOpenBorders(false),
m_bWaterWorks(false),
m_bEurope(false),
m_bNative(false),
m_aiCivilizationBuildings(NULL),
m_aiCivilizationUnits(NULL),
m_aiCivilizationInitialCivics(NULL),
m_aiFreeYields(NULL),
m_aiTeachUnitClassWeights(NULL),
m_abLeaders(NULL),
m_abCivilizationFreeBuildingClass(NULL),
m_abValidProfessions(NULL),
m_abTraits(NULL),
m_paszCityNames(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvCivilizationInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvCivilizationInfo::~CvCivilizationInfo()
{
	SAFE_DELETE_ARRAY(m_aiCivilizationBuildings);
	SAFE_DELETE_ARRAY(m_aiCivilizationUnits);
	SAFE_DELETE_ARRAY(m_aiCivilizationInitialCivics);
	SAFE_DELETE_ARRAY(m_aiFreeYields);
	SAFE_DELETE_ARRAY(m_aiTeachUnitClassWeights);
	SAFE_DELETE_ARRAY(m_abLeaders);
	SAFE_DELETE_ARRAY(m_abCivilizationFreeBuildingClass);
	SAFE_DELETE_ARRAY(m_abValidProfessions);
	SAFE_DELETE_ARRAY(m_abTraits);
	SAFE_DELETE_ARRAY(m_paszCityNames);
}
void CvCivilizationInfo::reset()
{
	CvInfoBase::reset();
	m_szCachedShortDescription.clear();
	m_szCachedAdjective.clear();
}
int CvCivilizationInfo::getDefaultPlayerColor() const
{
	return m_iDefaultPlayerColor;
}
int CvCivilizationInfo::getArtStyleType() const
{
	return m_iArtStyleType;
}
int CvCivilizationInfo::getNumCityNames() const
{
	return m_iNumCityNames;
}
int CvCivilizationInfo::getNumLeaders() const// the number of leaders the Civ has, this is needed so that random leaders can be generated easily
{
	return m_iNumLeaders;
}
int CvCivilizationInfo::getSelectionSoundScriptId() const
{
	return m_iSelectionSoundScriptId;
}
int CvCivilizationInfo::getActionSoundScriptId() const
{
	return m_iActionSoundScriptId;
}
int CvCivilizationInfo::getAdvancedStartPoints() const
{
	return m_iAdvancedStartPoints;
}
int CvCivilizationInfo::getAreaMultiplier() const
{
	return m_iAreaMultiplier;
}
int CvCivilizationInfo::getDensityMultiplier() const
{
	return m_iDensityMultiplier;
}
int CvCivilizationInfo::getTreasure() const
{
	return m_iTreasure;
}
int CvCivilizationInfo::getFavoredTerrain() const
{
	return m_iFavoredTerrain;
}
int CvCivilizationInfo::getCapturedCityUnitClass() const
{
	return m_iCapturedCityUnitClass;
}
int CvCivilizationInfo::getDefaultProfession() const
{
	return m_iDefaultProfession;
}
int CvCivilizationInfo::getMissionaryChar() const
{
	return m_iMissionaryChar;
}
void CvCivilizationInfo::setMissionaryChar(int iChar)
{
	m_iMissionaryChar = iChar;
}
bool CvCivilizationInfo::isAIPlayable() const
{
	return m_bAIPlayable;
}
bool CvCivilizationInfo::isPlayable() const
{
	return m_bPlayable;
}
bool CvCivilizationInfo::isWaterStart() const
{
	return m_bWaterStart;
}
bool CvCivilizationInfo::isOpenBorders() const
{
	return m_bOpenBorders;
}
bool CvCivilizationInfo::isWaterWorks() const
{
	return m_bWaterWorks;
}
bool CvCivilizationInfo::isEurope() const
{
	return m_bEurope;
}
bool CvCivilizationInfo::isNative() const
{
	return m_bNative;
}
const wchar* CvCivilizationInfo::getShortDescription(uint uiForm)
{
	while (m_szCachedShortDescription.size() <= uiForm)
	{
		m_szCachedShortDescription.push_back(gDLL->getObjectText(m_szShortDescriptionKey, m_szCachedShortDescription.size()));
	}

	return m_szCachedShortDescription[uiForm];
}
const wchar* CvCivilizationInfo::getShortDescriptionKey() const
{
	return m_szShortDescriptionKey;
}
const wchar* CvCivilizationInfo::getAdjective(uint uiForm)
{
	while (m_szCachedAdjective.size() <= uiForm)
	{
		m_szCachedAdjective.push_back(gDLL->getObjectText(m_szAdjectiveKey, m_szCachedAdjective.size()));
	}

	return m_szCachedAdjective[uiForm];
}

const wchar* CvCivilizationInfo::getAdjectiveKey() const
{
	return m_szAdjectiveKey;
}
const char* CvCivilizationInfo::getFlagTexture() const
{
	return ARTFILEMGR.getCivilizationArtInfo( getArtDefineTag() )->getPath();
}
const char* CvCivilizationInfo::getArtDefineTag() const
{
	return m_szArtDefineTag;
}
void CvCivilizationInfo::setArtDefineTag(const char* szVal)
{
	m_szArtDefineTag = szVal;
}
// Arrays
int CvCivilizationInfo::getCivilizationBuildings(int i) const
{
	FAssertMsg(i < GC.getNumBuildingClassInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiCivilizationBuildings ? m_aiCivilizationBuildings[i] : -1;
}
int CvCivilizationInfo::getCivilizationUnits(int i) const
{
	FAssertMsg(i < GC.getNumUnitClassInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiCivilizationUnits ? m_aiCivilizationUnits[i] : -1;
}
int CvCivilizationInfo::getNumCivilizationFreeUnits() const
{
	return m_aCivilizationFreeUnits.size();
}
int CvCivilizationInfo::getCivilizationFreeUnitsClass(int index) const
{
	FAssert(index < (int) m_aCivilizationFreeUnits.size());
	FAssert(index > -1);
	return m_aCivilizationFreeUnits[index].first;
}
int CvCivilizationInfo::getCivilizationFreeUnitsProfession(int index) const
{
	FAssert(index < (int) m_aCivilizationFreeUnits.size());
	FAssert(index > -1);
	return m_aCivilizationFreeUnits[index].second;
}
int CvCivilizationInfo::getCivilizationInitialCivics(int i) const
{
	FAssertMsg(i < GC.getNumCivicOptionInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiCivilizationInitialCivics ? m_aiCivilizationInitialCivics[i] : -1;
}
int CvCivilizationInfo::getFreeYields(int i) const
{
	FAssert(i < NUM_YIELD_TYPES && i >= 0);
	return m_aiFreeYields ? m_aiFreeYields[i] : -1;
}
bool CvCivilizationInfo::isLeaders(int i) const
{
	FAssertMsg(i < GC.getNumLeaderHeadInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abLeaders ? m_abLeaders[i] : false;
}
bool CvCivilizationInfo::isCivilizationFreeBuildingClass(int i) const
{
	FAssertMsg(i < GC.getNumBuildingClassInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abCivilizationFreeBuildingClass ? m_abCivilizationFreeBuildingClass[i] : false;
}
bool CvCivilizationInfo::isValidProfession(int i) const
{
	FAssertMsg(i < GC.getNumProfessionInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abValidProfessions ? m_abValidProfessions[i] : false;
}
bool CvCivilizationInfo::hasTrait(int i) const
{
	FAssertMsg(i < GC.getNumTraitInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abTraits ? m_abTraits[i] : false;
}
int CvCivilizationInfo::getTeachUnitClassWeight(int i) const
{
	FAssertMsg(i < GC.getNumUnitClassInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiTeachUnitClassWeights ? m_aiTeachUnitClassWeights[i] : false;
}
const CvArtInfoCivilization* CvCivilizationInfo::getArtInfo() const
{
	return ARTFILEMGR.getCivilizationArtInfo( getArtDefineTag() );
}
const char* CvCivilizationInfo::getButton() const
{
	return getArtInfo()->getButton();
}
std::string CvCivilizationInfo::getCityNames(int i) const
{
	FAssertMsg(i < getNumCityNames(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_paszCityNames[i];
}
int CvCivilizationInfo::getDerivativeCiv() const
{
	return m_iDerivativeCiv;
}
void CvCivilizationInfo::setDerivativeCiv(int iCiv)
{
	m_iDerivativeCiv = iCiv;
}
void CvCivilizationInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);

	uint uiFlag=0;
	stream->Read(&uiFlag);		// flag for expansion
	stream->Read(&m_iDefaultPlayerColor);
	stream->Read(&m_iArtStyleType);
	stream->Read(&m_iNumCityNames);
	stream->Read(&m_iNumLeaders);
	stream->Read(&m_iSelectionSoundScriptId);
	stream->Read(&m_iActionSoundScriptId);
	stream->Read(&m_iDerivativeCiv);
	stream->Read(&m_iAdvancedStartPoints);
	stream->Read(&m_iAreaMultiplier);
	stream->Read(&m_iDensityMultiplier);
	stream->Read(&m_iTreasure);
	stream->Read(&m_iFavoredTerrain);
	stream->Read(&m_iCapturedCityUnitClass);
	stream->Read(&m_iDefaultProfession);
	stream->Read(&m_iMissionaryChar);
	stream->Read(&m_bAIPlayable);
	stream->Read(&m_bPlayable);
	stream->Read(&m_bWaterStart);
	stream->Read(&m_bOpenBorders);
	stream->Read(&m_bWaterWorks);
	stream->Read(&m_bEurope);
	stream->Read(&m_bNative);
	stream->ReadString(m_szArtDefineTag);
	stream->ReadString(m_szShortDescriptionKey);
	stream->ReadString(m_szAdjectiveKey);
	// Arrays
	SAFE_DELETE_ARRAY(m_aiCivilizationBuildings);
	m_aiCivilizationBuildings = new int[GC.getNumBuildingClassInfos()];
	stream->Read(GC.getNumBuildingClassInfos(), m_aiCivilizationBuildings);
	SAFE_DELETE_ARRAY(m_aiCivilizationUnits);
	m_aiCivilizationUnits = new int[GC.getNumUnitClassInfos()];
	stream->Read(GC.getNumUnitClassInfos(), m_aiCivilizationUnits);
	m_aCivilizationFreeUnits.clear();
	int iSize;
	stream->Read(&iSize);
	for(int i=0;i<iSize;i++)
	{
		int iUnitClass;
		stream->Read(&iUnitClass);
		int iProfession;
		stream->Read(&iProfession);
		m_aCivilizationFreeUnits.push_back(std::make_pair((UnitClassTypes) iUnitClass, (ProfessionTypes) iProfession));
	}

	SAFE_DELETE_ARRAY(m_aiCivilizationInitialCivics);
	m_aiCivilizationInitialCivics = new int[GC.getNumCivicOptionInfos()];
	stream->Read(GC.getNumCivicOptionInfos(), m_aiCivilizationInitialCivics);

	SAFE_DELETE_ARRAY(m_aiFreeYields);
	m_aiFreeYields = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiFreeYields);

	SAFE_DELETE_ARRAY(m_aiTeachUnitClassWeights);
	m_aiTeachUnitClassWeights = new int[GC.getNumUnitClassInfos()];
	stream->Read(GC.getNumUnitClassInfos(), m_aiTeachUnitClassWeights);

	SAFE_DELETE_ARRAY(m_abLeaders);
	m_abLeaders = new bool[GC.getNumLeaderHeadInfos()];
	stream->Read(GC.getNumLeaderHeadInfos(), m_abLeaders);

	SAFE_DELETE_ARRAY(m_abCivilizationFreeBuildingClass);
	m_abCivilizationFreeBuildingClass = new bool[GC.getNumBuildingClassInfos()];
	stream->Read(GC.getNumBuildingClassInfos(), m_abCivilizationFreeBuildingClass);

	SAFE_DELETE_ARRAY(m_abValidProfessions);
	m_abValidProfessions = new bool[GC.getNumProfessionInfos()];
	stream->Read(GC.getNumProfessionInfos(), m_abValidProfessions);

	SAFE_DELETE_ARRAY(m_abTraits);
	m_abTraits = new bool[GC.getNumTraitInfos()];
	stream->Read(GC.getNumTraitInfos(), m_abTraits);

	SAFE_DELETE_ARRAY(m_paszCityNames);
	m_paszCityNames = new CvString[m_iNumCityNames];
	stream->ReadString(m_iNumCityNames, m_paszCityNames);
}
void CvCivilizationInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_iDefaultPlayerColor);
	stream->Write(m_iArtStyleType);
	stream->Write(m_iNumCityNames);
	stream->Write(m_iNumLeaders);
	stream->Write(m_iSelectionSoundScriptId);
	stream->Write(m_iActionSoundScriptId);
	stream->Write(m_iDerivativeCiv);
	stream->Write(m_iAdvancedStartPoints);
	stream->Write(m_iAreaMultiplier);
	stream->Write(m_iDensityMultiplier);
	stream->Write(m_iTreasure);
	stream->Write(m_iFavoredTerrain);
	stream->Write(m_iCapturedCityUnitClass);
	stream->Write(m_iDefaultProfession);
	stream->Write(m_iMissionaryChar);
	stream->Write(m_bAIPlayable);
	stream->Write(m_bPlayable);
	stream->Write(m_bWaterStart);
	stream->Write(m_bOpenBorders);
	stream->Write(m_bWaterWorks);
	stream->Write(m_bEurope);
	stream->Write(m_bNative);
	stream->WriteString(m_szArtDefineTag);
	stream->WriteString(m_szShortDescriptionKey);
	stream->WriteString(m_szAdjectiveKey);
	// Arrays
	stream->Write(GC.getNumBuildingClassInfos(), m_aiCivilizationBuildings);
	stream->Write(GC.getNumUnitClassInfos(), m_aiCivilizationUnits);
	stream->Write((int)m_aCivilizationFreeUnits.size());
	for(int i=0;i<(int)m_aCivilizationFreeUnits.size();i++)
	{
		stream->Write(m_aCivilizationFreeUnits[i].first);
		stream->Write(m_aCivilizationFreeUnits[i].second);
	}
	stream->Write(GC.getNumCivicOptionInfos(), m_aiCivilizationInitialCivics);
	stream->Write(NUM_YIELD_TYPES, m_aiFreeYields);
	stream->Write(GC.getNumUnitClassInfos(), m_aiTeachUnitClassWeights);
	stream->Write(GC.getNumLeaderHeadInfos(), m_abLeaders);
	stream->Write(GC.getNumBuildingClassInfos(), m_abCivilizationFreeBuildingClass);
	stream->Write(GC.getNumProfessionInfos(), m_abValidProfessions);
	stream->Write(GC.getNumTraitInfos(), m_abTraits);
	stream->WriteString(m_iNumCityNames, m_paszCityNames);
}
bool CvCivilizationInfo::read(CvXMLLoadUtility* pXML)
{
	char szClassVal[256];					// holds the text value of the relevant classinfo
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	int j, iNumSibs;
	pXML->GetChildXmlValByName(m_szShortDescriptionKey, "ShortDescription");
	pXML->GetChildXmlValByName(m_szAdjectiveKey, "Adjective");
	pXML->GetChildXmlValByName(szTextVal, "DefaultPlayerColor");
	m_iDefaultPlayerColor = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "ArtDefineTag");
	setArtDefineTag(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "ArtStyleType");
	m_iArtStyleType = GC.getInfoTypeForString(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "CivilizationSelectionSound");
	m_iSelectionSoundScriptId = (szTextVal.GetLength() > 0) ? gDLL->getAudioTagIndex( szTextVal.GetCString(), AUDIOTAG_3DSCRIPT ) : -1;
	pXML->GetChildXmlValByName(szTextVal, "CivilizationActionSound");
	m_iActionSoundScriptId = (szTextVal.GetLength() > 0) ? gDLL->getAudioTagIndex( szTextVal.GetCString(), AUDIOTAG_3DSCRIPT ) : -1;
	pXML->GetChildXmlValByName(&m_iAdvancedStartPoints, "iAdvancedStartPoints");
	pXML->GetChildXmlValByName(&m_iAreaMultiplier, "iAreaMultiplier");
	pXML->GetChildXmlValByName(&m_iDensityMultiplier, "iDensityMultiplier");
	pXML->GetChildXmlValByName(&m_iTreasure, "iTreasure");
	pXML->GetChildXmlValByName(szTextVal, "FavoredTerrain");
	m_iFavoredTerrain = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "CapturedCityUnitClass");
	m_iCapturedCityUnitClass = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "DefaultProfession");
	m_iDefaultProfession = pXML->FindInInfoClass(szTextVal);
	// set the current xml node to it's next sibling and then
	pXML->GetChildXmlValByName(&m_bPlayable, "bPlayable");
	pXML->GetChildXmlValByName(&m_bAIPlayable, "bAIPlayable");
	pXML->GetChildXmlValByName(&m_bWaterStart, "bWaterStart");
	pXML->GetChildXmlValByName(&m_bOpenBorders, "bOpenBorders");
	pXML->GetChildXmlValByName(&m_bWaterWorks, "bWaterWorks");
	pXML->GetChildXmlValByName(&m_bEurope, "bEurope");
	pXML->GetChildXmlValByName(&m_bNative, "bNative");
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"Cities"))
	{
		pXML->SetStringList(&m_paszCityNames, &m_iNumCityNames);
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	// if we can set the current xml node to it's next sibling
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"Buildings"))
	{
		// pXML->Skip any comments and stop at the next value we might want
		if (pXML->SkipToNextVal())
		{
			// call the function that sets the default civilization buildings
			pXML->InitBuildingDefaults(&m_aiCivilizationBuildings);
			// get the total number of children the current xml node has
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			// if the call to the function that sets the current xml node to it's first non-comment
			// child and sets the parameter with the new node's value succeeds
			if ( (0 < iNumSibs) && (gDLL->getXMLIFace()->SetToChild(pXML->GetXML())) )
			{
				int iBuildingClassIndex;
				FAssertMsg((iNumSibs <= GC.getNumBuildingClassInfos()) ,"In SetGlobalCivilizationInfo iNumSibs is greater than GC.getNumBuildingClassInfos()");
				// loop through all the siblings
				for (j=0;j<iNumSibs;j++)
				{
					if (pXML->GetChildXmlVal(szClassVal))
					{
						// get the index into the array based on the building class type
						iBuildingClassIndex = pXML->FindInInfoClass(szClassVal);
						if (-1 < iBuildingClassIndex)
						{
							// get the next value which should be the building type to set this civilization's version of this building class too
							pXML->GetNextXmlVal( &szTextVal);
							// call the find in list function to return either -1 if no value is found
							// or the index in the list the match is found at
							m_aiCivilizationBuildings[iBuildingClassIndex] = pXML->FindInInfoClass(szTextVal);
						}
						else
						{
							FAssertMsg(0,"BuildingClass index is -1 in SetGlobalCivilizationInfo function");
						}
						// set the current xml node to it's parent node
						gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
					}
					// if the call to the function that sets the current xml node to it's first non-comment
					// sibling and sets the parameter with the new node's value does not succeed
					// we will break out of this for loop
					if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
					{
						break;
					}
				}
				// set the current xml node to it's parent node
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
		}
		// set the current xml node to it's parent node
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	// if we can set the current xml node to it's next sibling
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"Units"))
	{
		// pXML->Skip any comments and stop at the next value we might want
		if (pXML->SkipToNextVal())
		{
			// call the function that sets the default civilization buildings
			pXML->InitUnitDefaults(&m_aiCivilizationUnits);
			// get the total number of children the current xml node has
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			// if the call to the function that sets the current xml node to it's first non-comment
			// child and sets the parameter with the new node's value succeeds
			if ( (0 < iNumSibs) && (gDLL->getXMLIFace()->SetToChild(pXML->GetXML())) )
			{
				int iUnitClassIndex;
				FAssertMsg((iNumSibs <= GC.getNumUnitClassInfos()),"In SetGlobalCivilizationInfo iNumSibs is greater than GC.getNumUnitClassInfos()");
				// loop through all the siblings
				for (j=0;j<iNumSibs;j++)
				{
					if (pXML->GetChildXmlVal(szClassVal))
					{
						// set the unit class index
						iUnitClassIndex = pXML->FindInInfoClass(szClassVal);
						if (-1 < iUnitClassIndex)
						{
							// get the next value which should be the building type to set this civilization's version of this building class too
							pXML->GetNextXmlVal( &szTextVal);
							// call the find in list function to return either -1 if no value is found
							// or the index in the list the match is found at
							m_aiCivilizationUnits[iUnitClassIndex] = pXML->FindInInfoClass(szTextVal);
						}
						else
						{
							FAssertMsg(0, "UnitClass index is -1 in SetGlobalCivilizationInfo function");
						}
						// set the current xml node to it's parent node
						gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
					}
					// if the call to the function that sets the current xml node to it's first non-comment
					// sibling and sets the parameter with the new node's value does not succeed
					// we will break out of this for loop
					if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
					{
						break;
					}
				}
				// set the current xml node to it's parent node
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
		}
		// set the current xml node to it's parent node
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	// if we can set the current xml node to it's next sibling
	m_aCivilizationFreeUnits.clear();
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"FreeUnitClasses"))
	{
		if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"FreeUnitClass"))
		{
			do
			{
				pXML->GetChildXmlValByName(szTextVal, "UnitClassType");
				int iUnitClass = pXML->FindInInfoClass(szTextVal);
				pXML->GetChildXmlValByName(szTextVal, "FreeUnitProfession");
				int iProfession = pXML->FindInInfoClass(szTextVal);
				m_aCivilizationFreeUnits.push_back(std::make_pair((UnitClassTypes) iUnitClass, (ProfessionTypes) iProfession));
			} while(gDLL->getXMLIFace()->NextSibling(pXML->GetXML()));
			// set the current xml node to it's parent node
			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		// set the current xml node to it's parent node
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	pXML->SetVariableListTagPair(&m_abCivilizationFreeBuildingClass, "FreeBuildingClasses", GC.getNumBuildingClassInfos(), false);
	pXML->SetVariableListTagPair(&m_abValidProfessions, "Professions", GC.getNumProfessionInfos(), true);
	pXML->SetVariableListTagPair(&m_abTraits, "Traits", GC.getNumTraitInfos(), false);
	pXML->SetVariableListTagPair(&m_aiTeachUnitClassWeights, "TeachUnitClasses", GC.getNumUnitClassInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiFreeYields, "FreeYields", NUM_YIELD_TYPES, 0);
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"InitialCivics"))
	{
		if (pXML->SkipToNextVal())
		{
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			pXML->InitList(&m_aiCivilizationInitialCivics, GC.getNumCivicOptionInfos(), (int)NO_CIVIC);
			if (0 < iNumSibs)
			{
				if (pXML->GetChildXmlVal(szTextVal))
				{
					FAssertMsg((iNumSibs <= GC.getNumCivicOptionInfos()),"For loop iterator is greater than array size");
					for (j=0;j<iNumSibs;j++)
					{
						m_aiCivilizationInitialCivics[j] = pXML->FindInInfoClass(szTextVal);
						if (!pXML->GetNextXmlVal(&szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	pXML->SetVariableListTagPair(&m_abLeaders, "Leaders", GC.getNumLeaderHeadInfos(), false);
	pXML->GetChildXmlValByName(szTextVal, "CivilizationSelectionSound");
	return true;
}
bool CvCivilizationInfo::readPass2(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "DerivativeCiv");
	m_iDerivativeCiv = GC.getInfoTypeForString(szTextVal);
	return true;
}
//======================================================================================================
//					CvVictoryInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvVictoryInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvVictoryInfo::CvVictoryInfo() :
m_iPopulationPercentLead(0),
m_iLandPercent(0),
m_iMinLandPercent(0),
m_iCityCulture(0),
m_iNumCultureCities(0),
m_iTotalCultureRatio(0),
m_bDefault(false),
m_bTargetScore(false),
m_bEndEurope(false),
m_bEndScore(false),
m_bConquest(false),
m_bPermanent(false),
m_bRevolution(false)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvVictoryInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvVictoryInfo::~CvVictoryInfo()
{
}
int CvVictoryInfo::getPopulationPercentLead() const
{
	return m_iPopulationPercentLead;
}
int CvVictoryInfo::getLandPercent() const
{
	return m_iLandPercent;
}
int CvVictoryInfo::getMinLandPercent() const
{
	return m_iMinLandPercent;
}
int CvVictoryInfo::getCityCulture() const
{
	return m_iCityCulture;
}
int CvVictoryInfo::getNumCultureCities() const
{
	return m_iNumCultureCities;
}
int CvVictoryInfo::getTotalCultureRatio() const
{
	return m_iTotalCultureRatio;
}
bool CvVictoryInfo::getDefault() const
{
	return m_bDefault;
}
bool CvVictoryInfo::isTargetScore() const
{
	return m_bTargetScore;
}
bool CvVictoryInfo::isEndEurope() const
{
	return m_bEndEurope;
}
bool CvVictoryInfo::isEndScore() const
{
	return m_bEndScore;
}
bool CvVictoryInfo::isConquest() const
{
	return m_bConquest;
}
bool CvVictoryInfo::isPermanent() const
{
	return m_bPermanent;
}
bool CvVictoryInfo::isRevolution() const
{
	return m_bRevolution;
}
const char* CvVictoryInfo::getMovie() const
{
	return m_szMovie;
}

//
// read from xml
//
bool CvVictoryInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bDefault, "bDefault");
	pXML->GetChildXmlValByName(&m_bTargetScore, "bTargetScore");
	pXML->GetChildXmlValByName(&m_bEndEurope, "bEndEurope");
	pXML->GetChildXmlValByName(&m_bEndScore, "bEndScore");
	pXML->GetChildXmlValByName(&m_bConquest, "bConquest");
	pXML->GetChildXmlValByName(&m_bPermanent, "bPermanent");
	pXML->GetChildXmlValByName(&m_bRevolution, "bRevolution");
	pXML->GetChildXmlValByName(&m_iPopulationPercentLead, "iPopulationPercentLead");
	pXML->GetChildXmlValByName(&m_iLandPercent, "iLandPercent");
	pXML->GetChildXmlValByName(&m_iMinLandPercent, "iMinLandPercent");
	pXML->GetChildXmlValByName(szTextVal, "CityCulture");
	m_iCityCulture = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iNumCultureCities, "iNumCultureCities");
	pXML->GetChildXmlValByName(&m_iTotalCultureRatio, "iTotalCultureRatio");
	pXML->GetChildXmlValByName(m_szMovie, "VictoryMovie");
	return true;
}
//======================================================================================================
//					CvHurryInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvHurryInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvHurryInfo::CvHurryInfo() :
	m_iGoldPerProduction(0),
	m_iProductionPerPopulation(0),
	m_iGoldPerCross(0),
	m_iYieldCostEuropePercent(0),
	m_iProductionYieldConsumed(NO_YIELD),
	m_iProductionYieldPercent(0),
	m_iFlatGold(0),
	m_bStarting(false),
	m_bCity(false)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvHurryInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvHurryInfo::~CvHurryInfo()
{
}
int CvHurryInfo::getGoldPerProduction() const
{
	return m_iGoldPerProduction;
}
int CvHurryInfo::getProductionPerPopulation() const
{
	return m_iProductionPerPopulation;
}
int CvHurryInfo::getGoldPerCross() const
{
	return m_iGoldPerCross;
}
int CvHurryInfo::getYieldCostEuropePercent() const
{
	return m_iYieldCostEuropePercent;
}
int CvHurryInfo::getProductionYieldConsumed() const
{
	return m_iProductionYieldConsumed;
}
int CvHurryInfo::getProductionYieldPercent() const
{
	return m_iProductionYieldPercent;
}
int CvHurryInfo::getFlatGold() const
{
	return m_iFlatGold;
}
bool CvHurryInfo::isStarting() const
{
	return m_bStarting;
}
bool CvHurryInfo::isCity() const
{
	return m_bCity;
}
bool CvHurryInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_iGoldPerProduction, "iGoldPerProduction");
	pXML->GetChildXmlValByName(&m_iProductionPerPopulation, "iProductionPerPopulation");
	pXML->GetChildXmlValByName(&m_iGoldPerCross, "iGoldPerCross");
	pXML->GetChildXmlValByName(&m_iYieldCostEuropePercent, "iYieldCostEuropePercent");
	pXML->GetChildXmlValByName(szTextVal, "ProductionYieldConsumed");
	m_iProductionYieldConsumed = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iProductionYieldPercent, "iProductionYieldPercent");
	pXML->GetChildXmlValByName(&m_iFlatGold, "iFlatGold");
	pXML->GetChildXmlValByName(&m_bStarting, "bStarting");
	pXML->GetChildXmlValByName(&m_bCity, "bCity");
	return true;
}
//======================================================================================================
//					CvHandicapInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvHandicapInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvHandicapInfo::CvHandicapInfo() :
m_iAdvancedStartPointsMod(0),
m_iStartingGold(0),
m_iFatherPercent(0),
m_iAttitudeChange(0),
m_iStartingDefenseUnits(0),
m_iStartingWorkerUnits(0),
m_iStartingExploreUnits(0),
m_iAIStartingUnitMultiplier(0),
m_iAIStartingDefenseUnits(0),
m_iAIStartingWorkerUnits(0),
m_iAIStartingExploreUnits(0),
m_iAIDeclareWarProb(0),
m_iAIWorkRateModifier(0),
m_iAINativeCombatModifier(0),
m_iAIKingCombatModifier(0),
m_iAIRebelModifier(0),
m_iAIGrowthPercent(0),
m_iAITrainPercent(0),
m_iAIConstructPercent(0),
m_iAIUnitUpgradePercent(0),
m_iAIHurryPercent(0),
m_iAIExtraTradePercent(0),
m_iAIPerEraModifier(0),
m_iAIAdvancedStartPercent(0),
m_iAIKingUnitThresholdPercent(0),
m_iKingGoldThresholdPercent(0),
m_iNumGoodies(0),
m_iEuropePriceThresholdMultiplier(0),
m_iNativePacifismPercent(0),
m_iMissionFailureThresholdPercent(0),
m_iKingNumUnitMultiplier(0),
m_aiGoodies(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvHandicapInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvHandicapInfo::~CvHandicapInfo()
{
	SAFE_DELETE_ARRAY(m_aiGoodies);
}
int CvHandicapInfo::getAdvancedStartPointsMod() const
{
	return m_iAdvancedStartPointsMod;
}
int CvHandicapInfo::getStartingGold() const
{
	return m_iStartingGold;
}
int CvHandicapInfo::getFatherPercent() const
{
	return m_iFatherPercent;
}
int CvHandicapInfo::getAttitudeChange() const
{
	return m_iAttitudeChange;
}
int CvHandicapInfo::getStartingDefenseUnits() const
{
	return m_iStartingDefenseUnits;
}
int CvHandicapInfo::getStartingWorkerUnits() const
{
	return m_iStartingWorkerUnits;
}
int CvHandicapInfo::getStartingExploreUnits() const
{
	return m_iStartingExploreUnits;
}
int CvHandicapInfo::getAIStartingUnitMultiplier() const
{
	return m_iAIStartingUnitMultiplier;
}
int CvHandicapInfo::getAIStartingDefenseUnits() const
{
	return m_iAIStartingDefenseUnits;
}
int CvHandicapInfo::getAIStartingWorkerUnits() const
{
	return m_iAIStartingWorkerUnits;
}
int CvHandicapInfo::getAIStartingExploreUnits() const
{
	return m_iAIStartingExploreUnits;
}
int CvHandicapInfo::getAIDeclareWarProb() const
{
	return m_iAIDeclareWarProb;
}
int CvHandicapInfo::getAIWorkRateModifier() const
{
	return m_iAIWorkRateModifier;
}
int CvHandicapInfo::getAINativeCombatModifier() const
{
	return m_iAINativeCombatModifier;
}
int CvHandicapInfo::getAIKingCombatModifier() const
{
	return m_iAIKingCombatModifier;
}
int CvHandicapInfo::getAIRebelModifier() const
{
	return m_iAIRebelModifier;
}
int CvHandicapInfo::getAIGrowthPercent() const
{
	return m_iAIGrowthPercent;
}
int CvHandicapInfo::getAITrainPercent() const
{
	return m_iAITrainPercent;
}
int CvHandicapInfo::getAIConstructPercent() const
{
	return m_iAIConstructPercent;
}
int CvHandicapInfo::getAIUnitUpgradePercent() const
{
	return m_iAIUnitUpgradePercent;
}
int CvHandicapInfo::getAIHurryPercent() const
{
	return m_iAIHurryPercent;
}
int CvHandicapInfo::getAIExtraTradePercent() const
{
	return m_iAIExtraTradePercent;
}
int CvHandicapInfo::getAIPerEraModifier() const
{
	return m_iAIPerEraModifier;
}
int CvHandicapInfo::getAIAdvancedStartPercent() const
{
	return m_iAIAdvancedStartPercent;
}
int CvHandicapInfo::getAIKingUnitThresholdPercent() const
{
	return m_iAIKingUnitThresholdPercent;
}
int CvHandicapInfo::getNumGoodies() const
{
	return m_iNumGoodies;
}
int CvHandicapInfo::getEuropePriceThresholdMultiplier() const
{
	return m_iEuropePriceThresholdMultiplier;
}
int CvHandicapInfo::getNativePacifismPercent() const
{
	return m_iNativePacifismPercent;
}
int CvHandicapInfo::getMissionFailureThresholdPercent() const
{
	return m_iMissionFailureThresholdPercent;
}

int CvHandicapInfo::getKingNumUnitMultiplier() const
{
	return m_iKingNumUnitMultiplier;
}
int CvHandicapInfo::getKingGoldThresholdPercent() const
{
	return m_iKingGoldThresholdPercent;
}

// Arrays
int CvHandicapInfo::getGoodies(int i) const
{
	FAssertMsg(i < getNumGoodies(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiGoodies[i];
}
void CvHandicapInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);		// Flag for Expansion
	stream->Read(&m_iAdvancedStartPointsMod);
	stream->Read(&m_iStartingGold);
	stream->Read(&m_iFatherPercent);
	stream->Read(&m_iAttitudeChange);
	stream->Read(&m_iStartingDefenseUnits);
	stream->Read(&m_iStartingWorkerUnits);
	stream->Read(&m_iStartingExploreUnits);
	stream->Read(&m_iAIStartingUnitMultiplier);
	stream->Read(&m_iAIStartingDefenseUnits);
	stream->Read(&m_iAIStartingWorkerUnits);
	stream->Read(&m_iAIStartingExploreUnits);
	stream->Read(&m_iAIDeclareWarProb);
	stream->Read(&m_iAIWorkRateModifier);
	stream->Read(&m_iAINativeCombatModifier);
	stream->Read(&m_iAIKingCombatModifier);
	stream->Read(&m_iAIRebelModifier);
	stream->Read(&m_iAIGrowthPercent);
	stream->Read(&m_iAITrainPercent);
	stream->Read(&m_iAIConstructPercent);
	stream->Read(&m_iAIUnitUpgradePercent);
	stream->Read(&m_iAIHurryPercent);
	stream->Read(&m_iAIExtraTradePercent);
	stream->Read(&m_iAIPerEraModifier);
	stream->Read(&m_iAIAdvancedStartPercent);
	stream->Read(&m_iAIKingUnitThresholdPercent);
	stream->Read(&m_iKingGoldThresholdPercent);
	stream->Read(&m_iNumGoodies);
	stream->Read(&m_iEuropePriceThresholdMultiplier);
	stream->Read(&m_iNativePacifismPercent);
	stream->Read(&m_iMissionFailureThresholdPercent);
	stream->Read(&m_iKingNumUnitMultiplier);
	stream->ReadString(m_szHandicapName);
	// Arrays
	SAFE_DELETE_ARRAY(m_aiGoodies);
	m_aiGoodies = new int[getNumGoodies()];
	stream->Read(getNumGoodies(), m_aiGoodies);
}
void CvHandicapInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);		// Flag for Expansion
	stream->Write(m_iAdvancedStartPointsMod);
	stream->Write(m_iStartingGold);
	stream->Write(m_iFatherPercent);
	stream->Write(m_iAttitudeChange);
	stream->Write(m_iStartingDefenseUnits);
	stream->Write(m_iStartingWorkerUnits);
	stream->Write(m_iStartingExploreUnits);
	stream->Write(m_iAIStartingUnitMultiplier);
	stream->Write(m_iAIStartingDefenseUnits);
	stream->Write(m_iAIStartingWorkerUnits);
	stream->Write(m_iAIStartingExploreUnits);
	stream->Write(m_iAIDeclareWarProb);
	stream->Write(m_iAIWorkRateModifier);
	stream->Write(m_iAINativeCombatModifier);
	stream->Write(m_iAIKingCombatModifier);
	stream->Write(m_iAIRebelModifier);
	stream->Write(m_iAIGrowthPercent);
	stream->Write(m_iAITrainPercent);
	stream->Write(m_iAIConstructPercent);
	stream->Write(m_iAIUnitUpgradePercent);
	stream->Write(m_iAIHurryPercent);
	stream->Write(m_iAIExtraTradePercent);
	stream->Write(m_iAIPerEraModifier);
	stream->Write(m_iAIAdvancedStartPercent);
	stream->Write(m_iAIKingUnitThresholdPercent);
	stream->Write(m_iKingGoldThresholdPercent);
	stream->Write(m_iNumGoodies);
	stream->Write(m_iEuropePriceThresholdMultiplier);
	stream->Write(m_iNativePacifismPercent);
	stream->Write(m_iMissionFailureThresholdPercent);
	stream->Write(m_iKingNumUnitMultiplier);
	stream->WriteString(m_szHandicapName);
	// Arrays
	stream->Write(getNumGoodies(), m_aiGoodies);
}
bool CvHandicapInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	int j;
	pXML->GetChildXmlValByName(&m_iAdvancedStartPointsMod, "iAdvancedStartPointsMod");
	pXML->GetChildXmlValByName(&m_iStartingGold, "iGold");
	pXML->GetChildXmlValByName(&m_iFatherPercent, "iFatherPercent");
	pXML->GetChildXmlValByName(&m_iAttitudeChange, "iAttitudeChange");
	pXML->GetChildXmlValByName(&m_iStartingDefenseUnits, "iStartingDefenseUnits");
	pXML->GetChildXmlValByName(&m_iStartingWorkerUnits, "iStartingWorkerUnits");
	pXML->GetChildXmlValByName(&m_iStartingExploreUnits, "iStartingExploreUnits");
	pXML->GetChildXmlValByName(&m_iAIStartingUnitMultiplier, "iAIStartingUnitMultiplier");
	pXML->GetChildXmlValByName(&m_iAIStartingDefenseUnits, "iAIStartingDefenseUnits");
	pXML->GetChildXmlValByName(&m_iAIStartingWorkerUnits, "iAIStartingWorkerUnits");
	pXML->GetChildXmlValByName(&m_iAIStartingExploreUnits, "iAIStartingExploreUnits");
	pXML->GetChildXmlValByName(&m_iAIDeclareWarProb, "iAIDeclareWarProb");
	pXML->GetChildXmlValByName(&m_iAIWorkRateModifier, "iAIWorkRateModifier");
	pXML->GetChildXmlValByName(&m_iAINativeCombatModifier, "iAINativeCombatModifier");
	pXML->GetChildXmlValByName(&m_iAIKingCombatModifier, "iAIKingCombatModifier");
	pXML->GetChildXmlValByName(&m_iAIRebelModifier, "iAIRebelModifier");
	pXML->GetChildXmlValByName(&m_iAIGrowthPercent, "iAIGrowthPercent");
	pXML->GetChildXmlValByName(&m_iAITrainPercent, "iAITrainPercent");
	pXML->GetChildXmlValByName(&m_iAIConstructPercent, "iAIConstructPercent");
	pXML->GetChildXmlValByName(&m_iAIUnitUpgradePercent, "iAIUnitUpgradePercent");
	pXML->GetChildXmlValByName(&m_iAIHurryPercent, "iAIHurryPercent");
	pXML->GetChildXmlValByName(&m_iAIExtraTradePercent, "iAIExtraTradePercent");
	pXML->GetChildXmlValByName(&m_iAIPerEraModifier, "iAIPerEraModifier");
	pXML->GetChildXmlValByName(&m_iAIAdvancedStartPercent, "iAIAdvancedStartPercent");
	pXML->GetChildXmlValByName(&m_iAIKingUnitThresholdPercent, "iAIKingUnitThresholdPercent");
	pXML->GetChildXmlValByName(&m_iKingGoldThresholdPercent, "iKingGoldThresholdPercent");
	pXML->GetChildXmlValByName(&m_iEuropePriceThresholdMultiplier, "iEuropePriceThresholdMultiplier");
	pXML->GetChildXmlValByName(&m_iNativePacifismPercent, "iNativePacifismPercent");
	pXML->GetChildXmlValByName(&m_iMissionFailureThresholdPercent, "iMissionFailureThresholdPercent");
	pXML->GetChildXmlValByName(&m_iKingNumUnitMultiplier, "iKingNumUnitMultiplier");
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "Goodies"))
	{
		CvString* pszGoodyNames = NULL;
		pXML->SetStringList(&pszGoodyNames, &m_iNumGoodies);
		if (m_iNumGoodies > 0)
		{
			m_aiGoodies = new int[m_iNumGoodies];
			for (j=0;j<m_iNumGoodies;j++)
			{
				m_aiGoodies[j] = pXML->FindInInfoClass(pszGoodyNames[j]);
			}
		}
		else
		{
			m_aiGoodies = NULL;
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		SAFE_DELETE_ARRAY(pszGoodyNames);
	}
	return true;
}
//======================================================================================================
//					CvGameSpeedInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvGameSpeedInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvGameSpeedInfo::CvGameSpeedInfo() :
m_iGrowthPercent(0),
m_iStoragePercent(0),
m_iTrainPercent(0),
m_iConstructPercent(0),
m_iFatherPercent(0),
m_iGreatGeneralPercent(0),
m_iRevolutionTurns(0),
m_iNumTurnIncrements(0),
m_pGameTurnInfo(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvGameSpeedInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvGameSpeedInfo::~CvGameSpeedInfo()
{
	SAFE_DELETE_ARRAY(m_pGameTurnInfo);
}
int CvGameSpeedInfo::getGrowthPercent() const
{
	return m_iGrowthPercent;
}
int CvGameSpeedInfo::getStoragePercent() const
{
	return m_iStoragePercent;
}
int CvGameSpeedInfo::getTrainPercent() const
{
	return m_iTrainPercent;
}
int CvGameSpeedInfo::getConstructPercent() const
{
	return m_iConstructPercent;
}
int CvGameSpeedInfo::getFatherPercent() const
{
	return m_iFatherPercent;
}
int CvGameSpeedInfo::getGreatGeneralPercent() const
{
	return m_iGreatGeneralPercent;
}
int CvGameSpeedInfo::getRevolutionTurns() const
{
    return m_iRevolutionTurns;
}
int CvGameSpeedInfo::getNumTurnIncrements() const
{
	return m_iNumTurnIncrements;
}
GameTurnInfo& CvGameSpeedInfo::getGameTurnInfo(int iIndex) const
{
	return m_pGameTurnInfo[iIndex];
}
void CvGameSpeedInfo::allocateGameTurnInfos(const int iSize)
{
	m_pGameTurnInfo = new GameTurnInfo[iSize];
}
bool CvGameSpeedInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	int j, iTempVal;
	pXML->GetChildXmlValByName(&m_iGrowthPercent, "iGrowthPercent");
	pXML->GetChildXmlValByName(&m_iStoragePercent, "iStoragePercent");
	pXML->GetChildXmlValByName(&m_iTrainPercent, "iTrainPercent");
	pXML->GetChildXmlValByName(&m_iConstructPercent, "iConstructPercent");
	pXML->GetChildXmlValByName(&m_iFatherPercent, "iFatherPercent");
	pXML->GetChildXmlValByName(&m_iGreatGeneralPercent, "iGreatGeneralPercent");
	pXML->GetChildXmlValByName(&m_iRevolutionTurns, "iRevolutionTurns");
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"GameTurnInfos"))
	{
		m_iNumTurnIncrements = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
		if (gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
		{
			allocateGameTurnInfos(getNumTurnIncrements());
			// loop through each tag
			for (j=0;j<getNumTurnIncrements();j++)
			{
				pXML->GetChildXmlValByName(&iTempVal, "iMonthIncrement");
				getGameTurnInfo(j).iMonthIncrement = iTempVal;
				pXML->GetChildXmlValByName(&iTempVal, "iTurnsPerIncrement");
				getGameTurnInfo(j).iNumGameTurnsPerIncrement = iTempVal;
				// if we cannot set the current xml node to it's next sibling then we will break out of the for loop
				// otherwise we will continue looping
				if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
				{
					break;
				}
			}
			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	return true;
}

//======================================================================================================
//					CvTurnTimerInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvTurnTimerInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvTurnTimerInfo::CvTurnTimerInfo() :
m_iBaseTime(0),
m_iCityBonus(0),
m_iUnitBonus(0),
m_iFirstTurnMultiplier(0)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvTurnTimerInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvTurnTimerInfo::~CvTurnTimerInfo()
{
}
int CvTurnTimerInfo::getBaseTime() const
{
	return m_iBaseTime;
}
int CvTurnTimerInfo::getCityBonus() const
{
	return m_iCityBonus;
}
int CvTurnTimerInfo::getUnitBonus() const
{
	return m_iUnitBonus;
}
int CvTurnTimerInfo::getFirstTurnMultiplier() const
{
	return m_iFirstTurnMultiplier;
}
bool CvTurnTimerInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_iBaseTime, "iBaseTime");
	pXML->GetChildXmlValByName(&m_iCityBonus, "iCityBonus");
	pXML->GetChildXmlValByName(&m_iUnitBonus, "iUnitBonus");
	pXML->GetChildXmlValByName(&m_iFirstTurnMultiplier, "iFirstTurnMultiplier");
	return true;
}
//======================================================================================================
//					CvBuildInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvBuildInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvBuildInfo::CvBuildInfo() :
m_iTime(0),
m_iCost(0),
m_iImprovement(NO_IMPROVEMENT),
m_iRoute(NO_ROUTE),
m_iEntityEvent(ENTITY_EVENT_NONE),
m_iMissionType(NO_MISSION),
m_bKill(false),
m_paiFeatureTime(NULL),
m_pabFeatureRemove(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvBuildInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvBuildInfo::~CvBuildInfo()
{
	SAFE_DELETE_ARRAY(m_paiFeatureTime);
	SAFE_DELETE_ARRAY(m_pabFeatureRemove);
}
int CvBuildInfo::getTime() const
{
	return m_iTime;
}
int CvBuildInfo::getCost() const
{
	return m_iCost;
}
int CvBuildInfo::getImprovement() const
{
	return m_iImprovement;
}
int CvBuildInfo::getRoute() const
{
	return m_iRoute;
}
int CvBuildInfo::getEntityEvent() const
{
	return m_iEntityEvent;
}
int CvBuildInfo::getMissionType() const
{
	return m_iMissionType;
}
void CvBuildInfo::setMissionType(int iNewType)
{
	m_iMissionType = iNewType;
}
bool CvBuildInfo::isKill() const
{
	return m_bKill;
}
// Arrays
int CvBuildInfo::getFeatureTime(int i) const
{
	FAssertMsg(i < GC.getNumFeatureInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_paiFeatureTime ? m_paiFeatureTime[i] : -1;
}
int CvBuildInfo::getFeatureYield(int iFeature, int iYield) const
{
	FAssert(iFeature < GC.getNumFeatureInfos() && iFeature >= 0);
	FAssert(iYield < NUM_YIELD_TYPES && iYield >= 0);
	return m_aaiFeatureYield[iFeature][iYield];
}
bool CvBuildInfo::isFeatureRemove(int i) const
{
	FAssertMsg(i < GC.getNumFeatureInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_pabFeatureRemove ? m_pabFeatureRemove[i] : false;
}
bool CvBuildInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvHotkeyInfo::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_iTime, "iTime");
	pXML->GetChildXmlValByName(&m_iCost, "iCost");
	pXML->GetChildXmlValByName(&m_bKill, "bKill");
	pXML->GetChildXmlValByName(szTextVal, "ImprovementType");
	m_iImprovement = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "RouteType");
	m_iRoute = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "EntityEvent");
	m_iEntityEvent = pXML->FindInInfoClass(szTextVal);
	pXML->SetFeatureStruct(&m_paiFeatureTime, m_aaiFeatureYield, &m_pabFeatureRemove);
	return true;
}
//======================================================================================================
//					CvGoodyInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvGoodyInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvGoodyInfo::CvGoodyInfo() :
m_iGold(0),
m_iGoldRand1(0),
m_iGoldRand2(0),
m_iMapOffset(0),
m_iMapRange(0),
m_iMapProb(0),
m_iExperience(0),
m_iHealing(0),
m_iDamagePrereq(0),
m_iCityGoodyWeight(0),
m_iUnitClassType(NO_UNITCLASS),
	m_iTeachUnitClassType(NO_UNITCLASS),
	m_bBad(false),
	m_bWar(false),
	m_aGoodyWeights(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvGoodyInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvGoodyInfo::~CvGoodyInfo()
{
	SAFE_DELETE_ARRAY(m_aGoodyWeights);
}
int CvGoodyInfo::getGold() const
{
	return m_iGold;
}
int CvGoodyInfo::getGoldRand1() const
{
	return m_iGoldRand1;
}
int CvGoodyInfo::getGoldRand2() const
{
	return m_iGoldRand2;
}
int CvGoodyInfo::getMapOffset() const
{
	return m_iMapOffset;
}
int CvGoodyInfo::getMapRange() const
{
	return m_iMapRange;
}
int CvGoodyInfo::getMapProb() const
{
	return m_iMapProb;
}
int CvGoodyInfo::getExperience() const
{
	return m_iExperience;
}
int CvGoodyInfo::getHealing() const
{
	return m_iHealing;
}
int CvGoodyInfo::getDamagePrereq() const
{
	return m_iDamagePrereq;
}
int CvGoodyInfo::getCityGoodyWeight() const
{
	return m_iCityGoodyWeight;
}
int CvGoodyInfo::getUnitClassType() const
{
	return m_iUnitClassType;
}
int CvGoodyInfo::getTeachUnitClassType() const
{
	return m_iTeachUnitClassType;
}
bool CvGoodyInfo::isBad() const
{
	return m_bBad;
}
bool CvGoodyInfo::isWar() const
{
	return m_bWar;
}
int CvGoodyInfo::getGoodyWeight(int iGoody) const
{
	FAssert(iGoody >= 0 && iGoody < GC.getNumGoodyInfos());
	return m_aGoodyWeights[iGoody];
}
const char* CvGoodyInfo::getSound() const
{
	return m_szSound;
}
void CvGoodyInfo::setSound(const char* szVal)
{
	m_szSound=szVal;
}
const char* CvGoodyInfo::getAnnounceTextKey() const
{
	return m_szAnnounceTextKey;
}
const char* CvGoodyInfo::getChiefTextKey() const
{
	return m_szChiefTextKey;
}
bool CvGoodyInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(m_szSound, "Sound");
	pXML->GetChildXmlValByName(m_szAnnounceTextKey, "AnnounceText");
	pXML->GetChildXmlValByName(m_szChiefTextKey, "ChiefText");
	pXML->GetChildXmlValByName(&m_iGold, "iGold");
	pXML->GetChildXmlValByName(&m_iGoldRand1, "iGoldRand1");
	pXML->GetChildXmlValByName(&m_iGoldRand2, "iGoldRand2");
	pXML->GetChildXmlValByName(&m_iMapOffset, "iMapOffset");
	pXML->GetChildXmlValByName(&m_iMapRange, "iMapRange");
	pXML->GetChildXmlValByName(&m_iMapProb, "iMapProb");
	pXML->GetChildXmlValByName(&m_iExperience, "iExperience");
	pXML->GetChildXmlValByName(&m_iHealing, "iHealing");
	pXML->GetChildXmlValByName(&m_iDamagePrereq, "iDamagePrereq");
	pXML->GetChildXmlValByName(&m_bBad, "bBad");
	pXML->GetChildXmlValByName(&m_bWar, "bWar");
	pXML->GetChildXmlValByName(szTextVal, "UnitClass");
	m_iUnitClassType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "TeachUnitClass");
	m_iTeachUnitClassType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iCityGoodyWeight, "iCityGoodyWeight");
	return true;
}
bool CvGoodyInfo::readPass2(CvXMLLoadUtility* pXML)
{
	pXML->SetVariableListTagPair(&m_aGoodyWeights, "GoodyWeights", GC.getNumGoodyInfos(), 0);
	return true;
}
//======================================================================================================
//					CvRouteInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvRouteInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvRouteInfo::CvRouteInfo() :
m_iAdvancedStartCost(0),
m_iAdvancedStartCostIncrease(0),
m_iValue(0),
m_iMovementCost(0),
m_iFlatMovementCost(0),
m_aiYieldChange(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvRouteInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvRouteInfo::~CvRouteInfo()
{
	SAFE_DELETE_ARRAY(m_aiYieldChange);
}
int CvRouteInfo::getAdvancedStartCost() const
{
	return m_iAdvancedStartCost;
}
int CvRouteInfo::getAdvancedStartCostIncrease() const
{
	return m_iAdvancedStartCostIncrease;
}
int CvRouteInfo::getValue() const
{
	return m_iValue;
}
int CvRouteInfo::getMovementCost() const
{
	return m_iMovementCost;
}
int CvRouteInfo::getFlatMovementCost() const
{
	return m_iFlatMovementCost;
}
// Arrays
int CvRouteInfo::getYieldChange(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiYieldChange ? m_aiYieldChange[i] : -1;
}
bool CvRouteInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_iAdvancedStartCost, "iAdvancedStartCost");
	pXML->GetChildXmlValByName(&m_iAdvancedStartCostIncrease, "iAdvancedStartCostIncrease");
	pXML->GetChildXmlValByName(&m_iValue, "iValue");
	pXML->GetChildXmlValByName(&m_iMovementCost, "iMovement");
	pXML->GetChildXmlValByName(&m_iFlatMovementCost, "iFlatMovement");
	pXML->GetChildXmlValByName(szTextVal, "BonusType");

	pXML->SetVariableListTagPair(&m_aiYieldChange, "Yields", NUM_YIELD_TYPES, 0);
	return true;
}
//======================================================================================================
//					CvImprovementBonusInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvImprovementBonusInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvImprovementBonusInfo::CvImprovementBonusInfo() :
m_iDiscoverRand(0),
m_bBonusMakesValid(false),
m_aiYieldChange(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvImprovementBonusInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvImprovementBonusInfo::~CvImprovementBonusInfo()
{
	SAFE_DELETE_ARRAY(m_aiYieldChange);
}
int CvImprovementBonusInfo::getDiscoverRand() const
{
	return m_iDiscoverRand;
}
bool CvImprovementBonusInfo::isBonusMakesValid() const
{
	return m_bBonusMakesValid;
}
int CvImprovementBonusInfo::getYieldChange(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiYieldChange ? m_aiYieldChange[i] : -1;
}
void CvImprovementBonusInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);		// flag for expansion
	stream->Read(&m_iDiscoverRand);
	stream->Read(&m_bBonusMakesValid);
	// Arrays
	SAFE_DELETE_ARRAY(m_aiYieldChange);
	m_aiYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiYieldChange);
}
void CvImprovementBonusInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_iDiscoverRand);
	stream->Write(m_bBonusMakesValid);
	// Arrays
	stream->Write(NUM_YIELD_TYPES, m_aiYieldChange);
}
//======================================================================================================
//					CvImprovementInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvImprovementInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvImprovementInfo::CvImprovementInfo() :
m_iAdvancedStartCost(0),
m_iAdvancedStartCostIncrease(0),
m_iTilesPerGoody(0),
m_iGoodyUniqueRange(0),
m_iFeatureGrowthProbability(0),
m_iUpgradeTime(0),
m_iDefenseModifier(0),
m_iPillageGold(0),
m_iImprovementPillage(NO_IMPROVEMENT),
m_iImprovementUpgrade(NO_IMPROVEMENT),
m_bActsAsCity(true),
m_bHillsMakesValid(false),
m_bRiverSideMakesValid(false),
m_bRequiresFlatlands(false),
m_bRequiresRiverSide(false),
m_bRequiresFeature(false),
m_bWater(false),
m_bGoody(false),
m_bPermanent(false),
m_bUseLSystem(false),
m_bOutsideBorders(false),
m_iWorldSoundscapeScriptId(0),
m_aiPrereqNatureYield(NULL),
m_aiYieldIncrease(NULL),
m_aiRiverSideYieldChange(NULL),
m_aiHillsYieldChange(NULL),
m_abTerrainMakesValid(NULL),
m_abFeatureMakesValid(NULL),
m_paImprovementBonus(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvImprovementInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvImprovementInfo::~CvImprovementInfo()
{
	SAFE_DELETE_ARRAY(m_aiPrereqNatureYield);
	SAFE_DELETE_ARRAY(m_aiYieldIncrease);
	SAFE_DELETE_ARRAY(m_aiRiverSideYieldChange);
	SAFE_DELETE_ARRAY(m_aiHillsYieldChange);
	SAFE_DELETE_ARRAY(m_abTerrainMakesValid);
	SAFE_DELETE_ARRAY(m_abFeatureMakesValid);
	SAFE_DELETE_ARRAY(m_paImprovementBonus);
	for (uint iI=0;iI<m_aaiRouteYieldChanges.size();iI++)
		{
		SAFE_DELETE_ARRAY(m_aaiRouteYieldChanges[iI]);
	}
}
int CvImprovementInfo::getAdvancedStartCost() const
{
	return m_iAdvancedStartCost;
}
int CvImprovementInfo::getAdvancedStartCostIncrease() const
{
	return m_iAdvancedStartCostIncrease;
}
int CvImprovementInfo::getTilesPerGoody() const
{
	return m_iTilesPerGoody;
}
int CvImprovementInfo::getGoodyUniqueRange() const
{
	return m_iGoodyUniqueRange;
}
int CvImprovementInfo::getFeatureGrowthProbability() const
{
	return m_iFeatureGrowthProbability;
}
int CvImprovementInfo::getUpgradeTime() const
{
	return m_iUpgradeTime;
}
int CvImprovementInfo::getDefenseModifier() const
{
	return m_iDefenseModifier;
}
int CvImprovementInfo::getPillageGold() const
{
	return m_iPillageGold;
}
bool CvImprovementInfo::isOutsideBorders() const
{
	return m_bOutsideBorders;
}
int CvImprovementInfo::getImprovementPillage() const
{
	return m_iImprovementPillage;
}
void CvImprovementInfo::setImprovementPillage(int i)
{
	m_iImprovementPillage = i;
}
int CvImprovementInfo::getImprovementUpgrade() const
{
	return m_iImprovementUpgrade;
}
void CvImprovementInfo::setImprovementUpgrade(int i)
{
	m_iImprovementUpgrade = i;
}
bool CvImprovementInfo::isActsAsCity() const
{
	return m_bActsAsCity;
}
bool CvImprovementInfo::isHillsMakesValid() const
{
	return m_bHillsMakesValid;
}
bool CvImprovementInfo::isRiverSideMakesValid() const
{
	return m_bRiverSideMakesValid;
}
bool CvImprovementInfo::isRequiresFlatlands() const
{
	return m_bRequiresFlatlands;
}
bool CvImprovementInfo::isRequiresRiverSide() const
{
	return m_bRequiresRiverSide;
}
bool CvImprovementInfo::isRequiresFeature() const
{
	return m_bRequiresFeature;
}
bool CvImprovementInfo::isWater() const
{
	return m_bWater;
}
bool CvImprovementInfo::isGoody() const
{
	return m_bGoody;
}
bool CvImprovementInfo::isPermanent() const
{
	return m_bPermanent;
}
bool CvImprovementInfo::useLSystem() const
{
	return m_bUseLSystem;
}
const char* CvImprovementInfo::getArtDefineTag() const
{
	return m_szArtDefineTag;
}
void CvImprovementInfo::setArtDefineTag(const char* szVal)
{
	m_szArtDefineTag = szVal;
}
int CvImprovementInfo::getWorldSoundscapeScriptId() const
{
	return m_iWorldSoundscapeScriptId;
}
// Arrays
int CvImprovementInfo::getPrereqNatureYield(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiPrereqNatureYield ? m_aiPrereqNatureYield[i] : -1;
}
int* CvImprovementInfo::getPrereqNatureYieldArray()
{
	return m_aiPrereqNatureYield;
}
int CvImprovementInfo::getYieldIncrease(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiYieldIncrease ? m_aiYieldIncrease[i] : -1;
}
int* CvImprovementInfo::getYieldIncreaseArray()
{
	return m_aiYieldIncrease;
}
int CvImprovementInfo::getRiverSideYieldChange(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiRiverSideYieldChange ? m_aiRiverSideYieldChange[i] : -1;
}
int* CvImprovementInfo::getRiverSideYieldChangeArray()
{
	return m_aiRiverSideYieldChange;
}
int CvImprovementInfo::getHillsYieldChange(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiHillsYieldChange ? m_aiHillsYieldChange[i] : -1;
}
int* CvImprovementInfo::getHillsYieldChangeArray()
{
	return m_aiHillsYieldChange;
}
bool CvImprovementInfo::getTerrainMakesValid(int i) const
{
	FAssertMsg(i < GC.getNumTerrainInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abTerrainMakesValid ? m_abTerrainMakesValid[i] : false;
}
bool CvImprovementInfo::getFeatureMakesValid(int i) const
{
	FAssertMsg(i < GC.getNumFeatureInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abFeatureMakesValid ? m_abFeatureMakesValid[i] : false;
}
int CvImprovementInfo::getRouteYieldChanges(int i, int j) const
{
	FAssertMsg(i < GC.getNumRouteInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_aaiRouteYieldChanges[i][j];
}
int* CvImprovementInfo::getRouteYieldChangesArray(int i)
{
	return &(m_aaiRouteYieldChanges[i][0]);
}
int CvImprovementInfo::getImprovementBonusYield(int i, int j) const
{
	FAssertMsg(i < GC.getNumBonusInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_paImprovementBonus[i].m_aiYieldChange ? m_paImprovementBonus[i].getYieldChange(j) : -1;
}
bool CvImprovementInfo::isImprovementBonusMakesValid(int i) const
{
	FAssertMsg(i < GC.getNumBonusInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_paImprovementBonus[i].m_bBonusMakesValid;
}
int CvImprovementInfo::getImprovementBonusDiscoverRand(int i) const
{
	FAssertMsg(i < GC.getNumBonusInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_paImprovementBonus[i].m_iDiscoverRand;
}
const char* CvImprovementInfo::getButton() const
{
	const CvArtInfoImprovement * pImprovementArtInfo;
	pImprovementArtInfo = getArtInfo();
	if (pImprovementArtInfo != NULL)
	{
		return pImprovementArtInfo->getButton();
	}
	return NULL;
}
const CvArtInfoImprovement* CvImprovementInfo::getArtInfo() const
{
	return ARTFILEMGR.getImprovementArtInfo(getArtDefineTag());
}
void CvImprovementInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);		// flag for expansion
	stream->Read(&m_iAdvancedStartCost);
	stream->Read(&m_iAdvancedStartCostIncrease);
	stream->Read(&m_iTilesPerGoody);
	stream->Read(&m_iGoodyUniqueRange);
	stream->Read(&m_iFeatureGrowthProbability);
	stream->Read(&m_iUpgradeTime);
	stream->Read(&m_iDefenseModifier);
	stream->Read(&m_iPillageGold);
	stream->Read(&m_iImprovementPillage);
	stream->Read(&m_iImprovementUpgrade);
	stream->Read(&m_bActsAsCity);
	stream->Read(&m_bHillsMakesValid);
	stream->Read(&m_bRiverSideMakesValid);
	stream->Read(&m_bRequiresFlatlands);
	stream->Read(&m_bRequiresRiverSide);
	stream->Read(&m_bRequiresFeature);
	stream->Read(&m_bWater);
	stream->Read(&m_bGoody);
	stream->Read(&m_bPermanent);
	stream->Read(&m_bUseLSystem);
	stream->Read(&m_bOutsideBorders);
	stream->ReadString(m_szArtDefineTag);
	stream->Read(&m_iWorldSoundscapeScriptId);
	// Arrays
	SAFE_DELETE_ARRAY(m_aiPrereqNatureYield);
	m_aiPrereqNatureYield = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiPrereqNatureYield);
	SAFE_DELETE_ARRAY(m_aiYieldIncrease);
	m_aiYieldIncrease = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiYieldIncrease);
	SAFE_DELETE_ARRAY(m_aiRiverSideYieldChange);
	m_aiRiverSideYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiRiverSideYieldChange);
	SAFE_DELETE_ARRAY(m_aiHillsYieldChange);
	m_aiHillsYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiHillsYieldChange);
	SAFE_DELETE_ARRAY(m_abTerrainMakesValid);
	m_abTerrainMakesValid = new bool[GC.getNumTerrainInfos()];
	stream->Read(GC.getNumTerrainInfos(), m_abTerrainMakesValid);
	SAFE_DELETE_ARRAY(m_abFeatureMakesValid);
	m_abFeatureMakesValid = new bool[GC.getNumFeatureInfos()];
	stream->Read(GC.getNumFeatureInfos(), m_abFeatureMakesValid);
	SAFE_DELETE_ARRAY(m_paImprovementBonus);
	m_paImprovementBonus = new CvImprovementBonusInfo[GC.getNumBonusInfos()];
	for (int i = 0; i < GC.getNumBonusInfos(); i++)
	{
		m_paImprovementBonus[i].read(stream);
	}
	for (uint iI=0;iI<m_aaiRouteYieldChanges.size();iI++)
	{
		SAFE_DELETE_ARRAY(m_aaiRouteYieldChanges[iI]);
		}
	m_aaiRouteYieldChanges.clear();

	for(int i=0;i<GC.getNumRouteInfos();i++)
	{
		m_aaiRouteYieldChanges.push_back(new int[NUM_YIELD_TYPES]);
		stream->Read(NUM_YIELD_TYPES, m_aaiRouteYieldChanges[i]);
	}
}
void CvImprovementInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_iAdvancedStartCost);
	stream->Write(m_iAdvancedStartCostIncrease);
	stream->Write(m_iTilesPerGoody);
	stream->Write(m_iGoodyUniqueRange);
	stream->Write(m_iFeatureGrowthProbability);
	stream->Write(m_iUpgradeTime);
	stream->Write(m_iDefenseModifier);
	stream->Write(m_iPillageGold);
	stream->Write(m_iImprovementPillage);
	stream->Write(m_iImprovementUpgrade);
	stream->Write(m_bActsAsCity);
	stream->Write(m_bHillsMakesValid);
	stream->Write(m_bRiverSideMakesValid);
	stream->Write(m_bRequiresFlatlands);
	stream->Write(m_bRequiresRiverSide);
	stream->Write(m_bRequiresFeature);
	stream->Write(m_bWater);
	stream->Write(m_bGoody);
	stream->Write(m_bPermanent);
	stream->Write(m_bUseLSystem);
	stream->Write(m_bOutsideBorders);
	stream->WriteString(m_szArtDefineTag);
	stream->Write(m_iWorldSoundscapeScriptId);
	// Arrays
	stream->Write(NUM_YIELD_TYPES, m_aiPrereqNatureYield);
	stream->Write(NUM_YIELD_TYPES, m_aiYieldIncrease);
	stream->Write(NUM_YIELD_TYPES, m_aiRiverSideYieldChange);
	stream->Write(NUM_YIELD_TYPES, m_aiHillsYieldChange);
	stream->Write(GC.getNumTerrainInfos(), m_abTerrainMakesValid);
	stream->Write(GC.getNumFeatureInfos(), m_abFeatureMakesValid);
	int i;
	for (i = 0; i < GC.getNumBonusInfos(); i++)
	{
		m_paImprovementBonus[i].write(stream);
	}
	for(i=0;i<GC.getNumRouteInfos();i++)
	{
		stream->Write(NUM_YIELD_TYPES, m_aaiRouteYieldChanges[i]);
	}
}
bool CvImprovementInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	int iIndex, j, iNumSibs;
	pXML->GetChildXmlValByName(szTextVal, "ArtDefineTag");
	setArtDefineTag(szTextVal);
	pXML->SetVariableListTagPair(&m_aiPrereqNatureYield, "PrereqNatureYields", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiYieldIncrease, "YieldIncreases", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiRiverSideYieldChange, "RiverSideYieldChanges", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiHillsYieldChange, "HillsYieldChanges", NUM_YIELD_TYPES, 0);
	pXML->GetChildXmlValByName(&m_iAdvancedStartCost, "iAdvancedStartCost");
	pXML->GetChildXmlValByName(&m_iAdvancedStartCostIncrease, "iAdvancedStartCostIncrease");
	pXML->GetChildXmlValByName(&m_bActsAsCity, "bActsAsCity");
	pXML->GetChildXmlValByName(&m_bHillsMakesValid, "bHillsMakesValid");
	pXML->GetChildXmlValByName(&m_bRiverSideMakesValid, "bRiverSideMakesValid");
	pXML->GetChildXmlValByName(&m_bRequiresFlatlands, "bRequiresFlatlands");
	pXML->GetChildXmlValByName(&m_bRequiresRiverSide, "bRequiresRiverSide");
	pXML->GetChildXmlValByName(&m_bRequiresFeature, "bRequiresFeature");
	pXML->GetChildXmlValByName(&m_bWater, "bWater");
	pXML->GetChildXmlValByName(&m_bGoody, "bGoody");
	pXML->GetChildXmlValByName(&m_bPermanent, "bPermanent");
	pXML->GetChildXmlValByName(&m_bUseLSystem, "bUseLSystem");
	pXML->GetChildXmlValByName(&m_iTilesPerGoody, "iTilesPerGoody");
	pXML->GetChildXmlValByName(&m_iGoodyUniqueRange, "iGoodyRange");
	pXML->GetChildXmlValByName(&m_iFeatureGrowthProbability, "iFeatureGrowth");
	pXML->GetChildXmlValByName(&m_iUpgradeTime, "iUpgradeTime");
	pXML->GetChildXmlValByName(&m_iDefenseModifier, "iDefenseModifier");
	pXML->GetChildXmlValByName(&m_iPillageGold, "iPillageGold");
	pXML->GetChildXmlValByName(&m_bOutsideBorders, "bOutsideBorders");
	pXML->SetVariableListTagPair(&m_abTerrainMakesValid, "TerrainMakesValids", GC.getNumTerrainInfos(), false);
	pXML->SetVariableListTagPair(&m_abFeatureMakesValid, "FeatureMakesValids", GC.getNumFeatureInfos(), false);
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"BonusTypeStructs"))
	{
		// call the function that sets the bonus booleans
		pXML->SetImprovementBonuses(&m_paImprovementBonus);
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	else
	{
		// initialize the boolean list to the correct size and all the booleans to false
		pXML->InitImprovementBonusList(&m_paImprovementBonus, GC.getNumBonusInfos());
	}
	// initialize the boolean list to the correct size and all the booleans to false
	FAssertMsg((GC.getNumRouteInfos() > 0) && (NUM_YIELD_TYPES) > 0,"either the number of route infos is zero or less or the number of yield types is zero or less");
	pXML->Init2DIntList(m_aaiRouteYieldChanges, GC.getNumRouteInfos(), NUM_YIELD_TYPES);
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"RouteYieldChanges"))
	{
		if (pXML->SkipToNextVal())
		{
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
			{
				if (0 < iNumSibs)
				{
					for (j=0;j<iNumSibs;j++)
					{
						pXML->GetChildXmlValByName(szTextVal, "RouteType");
						iIndex = pXML->FindInInfoClass(szTextVal);
						if (iIndex > -1)
						{
							// delete the array since it will be reallocated
							SAFE_DELETE_ARRAY(m_aaiRouteYieldChanges[iIndex]);
							pXML->SetVariableListTagPair(&m_aaiRouteYieldChanges[iIndex], "RouteYields", NUM_YIELD_TYPES, 0);
						}
						if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
						{
							break;
						}
					}
				}
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	pXML->GetChildXmlValByName(szTextVal, "WorldSoundscapeAudioScript");
	if ( szTextVal.GetLength() > 0 )
		m_iWorldSoundscapeScriptId = gDLL->getAudioTagIndex( szTextVal.GetCString(), AUDIOTAG_SOUNDSCAPE );
	else
		m_iWorldSoundscapeScriptId = -1;
	return true;
}
bool CvImprovementInfo::readPass2(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "ImprovementPillage");
	m_iImprovementPillage = GC.getInfoTypeForString(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "ImprovementUpgrade");
	m_iImprovementUpgrade = GC.getInfoTypeForString(szTextVal);
	return true;
}
//======================================================================================================
//					CvBonusInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvBonusInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvBonusInfo::CvBonusInfo() :
m_iChar(0),
m_iAIObjective(0),
m_iMinAreaSize(0),
m_iMinLatitude(0),
m_iMaxLatitude(0),
m_iPlacementOrder(0),
m_iConstAppearance(0),
m_iRandAppearance1(0),
m_iRandAppearance2(0),
m_iRandAppearance3(0),
m_iRandAppearance4(0),
m_iPercentPerPlayer(0),
m_iTilesPer(0),
m_iMinLandPercent(0),
m_iUniqueRange(0),
m_iGroupRange(0),
m_iGroupRand(0),
m_iBuilding(0),
m_bOneArea(false),
m_bHills(false),
m_bFlatlands(false),
m_bNoRiverSide(false),
m_bUseLSystem(false),
m_aiYieldChange(NULL),
m_aiImprovementChange(NULL),
m_abTerrain(NULL),
m_abFeature(NULL),
m_abFeatureTerrain(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvBonusInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvBonusInfo::~CvBonusInfo()
{
	SAFE_DELETE_ARRAY(m_aiYieldChange);
	SAFE_DELETE_ARRAY(m_aiImprovementChange);
	SAFE_DELETE_ARRAY(m_abTerrain);
	SAFE_DELETE_ARRAY(m_abFeature);
	SAFE_DELETE_ARRAY(m_abFeatureTerrain);	// free memory - MT
}
int CvBonusInfo::getChar() const
{
	return m_iChar;
}
void CvBonusInfo::setChar(int i)
{
	m_iChar = i;
}
int CvBonusInfo::getAIObjective() const
{
	return m_iAIObjective;
}
int CvBonusInfo::getMinAreaSize() const
{
	return m_iMinAreaSize;
}
int CvBonusInfo::getMinLatitude() const
{
	return m_iMinLatitude;
}
int CvBonusInfo::getMaxLatitude() const
{
	return m_iMaxLatitude;
}
int CvBonusInfo::getPlacementOrder() const
{
	return m_iPlacementOrder;
}
int CvBonusInfo::getConstAppearance() const
{
	return m_iConstAppearance;
}
int CvBonusInfo::getRandAppearance1() const
{
	return m_iRandAppearance1;
}
int CvBonusInfo::getRandAppearance2() const
{
	return m_iRandAppearance2;
}
int CvBonusInfo::getRandAppearance3() const
{
	return m_iRandAppearance3;
}
int CvBonusInfo::getRandAppearance4() const
{
	return m_iRandAppearance4;
}
int CvBonusInfo::getPercentPerPlayer() const
{
	return m_iPercentPerPlayer;
}
int CvBonusInfo::getTilesPer() const
{
	return m_iTilesPer;
}
int CvBonusInfo::getMinLandPercent() const
{
	return m_iMinLandPercent;
}
int CvBonusInfo::getUniqueRange() const
{
	return m_iUniqueRange;
}
int CvBonusInfo::getGroupRange() const
{
	return m_iGroupRange;
}
int CvBonusInfo::getGroupRand() const
{
	return m_iGroupRand;
}
bool CvBonusInfo::isOneArea() const
{
	return m_bOneArea;
}
bool CvBonusInfo::isHills() const
{
	return m_bHills;
}
bool CvBonusInfo::isFlatlands() const
{
	return m_bFlatlands;
}
bool CvBonusInfo::isNoRiverSide() const
{
	return m_bNoRiverSide;
}
bool CvBonusInfo::useLSystem() const
{
	return m_bUseLSystem;
}
const char* CvBonusInfo::getArtDefineTag() const
{
	return m_szArtDefineTag;
}
void CvBonusInfo::setArtDefineTag(const char* szVal)
{
	m_szArtDefineTag = szVal;
}
// Arrays
int CvBonusInfo::getYieldChange(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiYieldChange ? m_aiYieldChange[i] : -1;
}
int* CvBonusInfo::getYieldChangeArray()
{
	return m_aiYieldChange;
}
int CvBonusInfo::getImprovementChange(int i) const
{
	FAssertMsg(i < GC.getNumImprovementInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiImprovementChange ? m_aiImprovementChange[i] : -1;
}
bool CvBonusInfo::isTerrain(int i) const
{
	FAssertMsg(i < GC.getNumTerrainInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abTerrain ?	m_abTerrain[i] : false;
}
bool CvBonusInfo::isFeature(int i) const
{
	FAssertMsg(i < GC.getNumFeatureInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abFeature ? m_abFeature[i] : false;
}
bool CvBonusInfo::isFeatureTerrain(int i) const
{
	FAssertMsg(i < GC.getNumTerrainInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abFeatureTerrain ?	m_abFeatureTerrain[i] : false;
}
const char* CvBonusInfo::getButton() const
{
	const CvArtInfoBonus * pBonusArtInfo;
	pBonusArtInfo = getArtInfo();
	if (pBonusArtInfo != NULL)
	{
		return pBonusArtInfo->getButton();
	}
	else
	{
		return NULL;
	}
}
int CvBonusInfo::getBuilding() const
{
	return m_iBuilding;
}
void CvBonusInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);		// flag for expansion
	stream->Read(&m_iChar);
	stream->Read(&m_iAIObjective);
	stream->Read(&m_iMinAreaSize);
	stream->Read(&m_iMinLatitude);
	stream->Read(&m_iMaxLatitude);
	stream->Read(&m_iPlacementOrder);
	stream->Read(&m_iConstAppearance);
	stream->Read(&m_iRandAppearance1);
	stream->Read(&m_iRandAppearance2);
	stream->Read(&m_iRandAppearance3);
	stream->Read(&m_iRandAppearance4);
	stream->Read(&m_iPercentPerPlayer);
	stream->Read(&m_iTilesPer);
	stream->Read(&m_iMinLandPercent);
	stream->Read(&m_iUniqueRange);
	stream->Read(&m_iGroupRange);
	stream->Read(&m_iGroupRand);
	stream->Read(&m_iBuilding);
	stream->Read(&m_bOneArea);
	stream->Read(&m_bHills);
	stream->Read(&m_bFlatlands);
	stream->Read(&m_bNoRiverSide);
	stream->Read(&m_bUseLSystem);
	stream->ReadString(m_szArtDefineTag);
	// Arrays
	SAFE_DELETE_ARRAY(m_aiYieldChange);
	m_aiYieldChange = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiYieldChange);
	SAFE_DELETE_ARRAY(m_aiImprovementChange);
	m_aiImprovementChange = new int[GC.getNumImprovementInfos()];
	stream->Read(GC.getNumImprovementInfos(), m_aiImprovementChange);
	SAFE_DELETE_ARRAY(m_abTerrain);
	m_abTerrain = new bool[GC.getNumTerrainInfos()];
	stream->Read(GC.getNumTerrainInfos(), m_abTerrain);
	SAFE_DELETE_ARRAY(m_abFeature);
	m_abFeature = new bool[GC.getNumFeatureInfos()];
	stream->Read(GC.getNumFeatureInfos(), m_abFeature);
	SAFE_DELETE_ARRAY(m_abFeatureTerrain);
	m_abFeatureTerrain = new bool[GC.getNumTerrainInfos()];
	stream->Read(GC.getNumTerrainInfos(), m_abFeatureTerrain);
}
void CvBonusInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_iChar);
	stream->Write(m_iAIObjective);
	stream->Write(m_iMinAreaSize);
	stream->Write(m_iMinLatitude);
	stream->Write(m_iMaxLatitude);
	stream->Write(m_iPlacementOrder);
	stream->Write(m_iConstAppearance);
	stream->Write(m_iRandAppearance1);
	stream->Write(m_iRandAppearance2);
	stream->Write(m_iRandAppearance3);
	stream->Write(m_iRandAppearance4);
	stream->Write(m_iPercentPerPlayer);
	stream->Write(m_iTilesPer);
	stream->Write(m_iMinLandPercent);
	stream->Write(m_iUniqueRange);
	stream->Write(m_iGroupRange);
	stream->Write(m_iGroupRand);
	stream->Write(m_iBuilding);
	stream->Write(m_bOneArea);
	stream->Write(m_bHills);
	stream->Write(m_bFlatlands);
	stream->Write(m_bNoRiverSide);
	stream->Write(m_bUseLSystem);
	stream->WriteString(m_szArtDefineTag);
	// Arrays
	stream->Write(NUM_YIELD_TYPES, m_aiYieldChange);
	stream->Write(GC.getNumImprovementInfos(), m_aiImprovementChange);
	stream->Write(GC.getNumTerrainInfos(), m_abTerrain);
	stream->Write(GC.getNumFeatureInfos(), m_abFeature);
	stream->Write(GC.getNumTerrainInfos(), m_abFeatureTerrain);
}
bool CvBonusInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName( szTextVal, "ArtDefineTag");
	setArtDefineTag(szTextVal);
	pXML->GetChildXmlValByName( szTextVal, "BuildingType");
	m_iBuilding = GC.getInfoTypeForString(szTextVal);
	pXML->SetVariableListTagPair(&m_aiYieldChange, "YieldChanges", NUM_YIELD_TYPES, 0);
	pXML->GetChildXmlValByName(&m_iAIObjective, "iAIObjective");
	pXML->GetChildXmlValByName(&m_iMinAreaSize, "iMinAreaSize");
	pXML->GetChildXmlValByName(&m_iMinLatitude, "iMinLatitude");
	pXML->GetChildXmlValByName(&m_iMaxLatitude, "iMaxLatitude");
	pXML->GetChildXmlValByName(&m_iPlacementOrder, "iPlacementOrder");
	pXML->GetChildXmlValByName(&m_iConstAppearance, "iConstAppearance");
	// if we can set the current xml node to it's next sibling
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"Rands"))
	{
		pXML->GetChildXmlValByName(&m_iRandAppearance1, "iRandApp1");
		pXML->GetChildXmlValByName(&m_iRandAppearance2, "iRandApp2");
		pXML->GetChildXmlValByName(&m_iRandAppearance3, "iRandApp3");
		pXML->GetChildXmlValByName(&m_iRandAppearance4, "iRandApp4");
		// set the current xml node to it's parent node
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	pXML->GetChildXmlValByName(&m_iPercentPerPlayer, "iPlayer");
	pXML->GetChildXmlValByName(&m_iTilesPer, "iTilesPer");
	pXML->GetChildXmlValByName(&m_iMinLandPercent, "iMinLandPercent");
	pXML->GetChildXmlValByName(&m_iUniqueRange, "iUnique");
	pXML->GetChildXmlValByName(&m_iGroupRange, "iGroupRange");
	pXML->GetChildXmlValByName(&m_iGroupRand, "iGroupRand");
	pXML->GetChildXmlValByName(&m_bOneArea, "bArea");
	pXML->GetChildXmlValByName(&m_bHills, "bHills");
	pXML->GetChildXmlValByName(&m_bFlatlands, "bFlatlands");
	pXML->GetChildXmlValByName(&m_bNoRiverSide, "bNoRiverSide");
	pXML->GetChildXmlValByName(&m_bUseLSystem, "bUseLSystem");
	pXML->SetVariableListTagPair(&m_abTerrain, "TerrainBooleans", GC.getNumTerrainInfos(), false);
	pXML->SetVariableListTagPair(&m_abFeature, "FeatureBooleans", GC.getNumFeatureInfos(), false);
	pXML->SetVariableListTagPair(&m_abFeatureTerrain, "FeatureTerrainBooleans", GC.getNumTerrainInfos(), false);
	return true;
}
//======================================================================================================
//					CvFeatureInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvFeatureInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvFeatureInfo::CvFeatureInfo() :
m_iMovementCost(0),
m_iSeeThroughChange(0),
m_iAppearanceProbability(0),
m_iDisappearanceProbability(0),
m_iGrowthProbability(0),
m_iDefenseModifier(0),
m_iAdvancedStartRemoveCost(0),
m_bNoCoast(false),
m_bNoRiver(false),
m_bNoAdjacent(false),
m_bRequiresFlatlands(false),
m_bRequiresRiver(false),
m_bImpassable(false),
m_bNoCity(false),
m_bNoImprovement(false),
m_bVisibleAlways(false),
m_iWorldSoundscapeScriptId(0),
m_iEffectProbability(0),
m_aiYieldChange(NULL),
m_aiRiverYieldIncrease(NULL),
m_ai3DAudioScriptFootstepIndex(NULL),
m_abTerrain(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvFeatureInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvFeatureInfo::~CvFeatureInfo()
{
	SAFE_DELETE_ARRAY(m_aiYieldChange);
	SAFE_DELETE_ARRAY(m_aiRiverYieldIncrease);
	SAFE_DELETE_ARRAY(m_ai3DAudioScriptFootstepIndex);
	SAFE_DELETE_ARRAY(m_abTerrain);
}
int CvFeatureInfo::getMovementCost() const
{
	return m_iMovementCost;
}
int CvFeatureInfo::getSeeThroughChange() const
{
	return m_iSeeThroughChange;
}
int CvFeatureInfo::getAppearanceProbability() const
{
	return m_iAppearanceProbability;
}
int CvFeatureInfo::getDisappearanceProbability() const
{
	return m_iDisappearanceProbability;
}
int CvFeatureInfo::getGrowthProbability() const
{
	return m_iGrowthProbability;
}
int CvFeatureInfo::getDefenseModifier() const
{
	return m_iDefenseModifier;
}
int CvFeatureInfo::getAdvancedStartRemoveCost() const
{
	return m_iAdvancedStartRemoveCost;
}
bool CvFeatureInfo::isNoCoast() const
{
	return m_bNoCoast;
}
bool CvFeatureInfo::isNoRiver() const
{
	return m_bNoRiver;
}
bool CvFeatureInfo::isNoAdjacent() const
{
	return m_bNoAdjacent;
}
bool CvFeatureInfo::isRequiresFlatlands() const
{
	return m_bRequiresFlatlands;
}
bool CvFeatureInfo::isRequiresRiver() const
{
	return m_bRequiresRiver;
}
bool CvFeatureInfo::isImpassable() const
{
	return m_bImpassable;
}
bool CvFeatureInfo::isNoCity() const
{
	return m_bNoCity;
}
bool CvFeatureInfo::isNoImprovement() const
{
	return m_bNoImprovement;
}
bool CvFeatureInfo::isVisibleAlways() const
{
	return m_bVisibleAlways;
}
const char* CvFeatureInfo::getOnUnitChangeTo() const
{
	return m_szOnUnitChangeTo;
}
const char* CvFeatureInfo::getArtDefineTag() const
{
	return m_szArtDefineTag;
}
void CvFeatureInfo::setArtDefineTag(const char* szTag)
{
	m_szArtDefineTag = szTag;
}
int CvFeatureInfo::getWorldSoundscapeScriptId() const
{
	return m_iWorldSoundscapeScriptId;
}
const char* CvFeatureInfo::getEffectType() const
{
	return m_szEffectType;
}
int CvFeatureInfo::getEffectProbability() const
{
	return m_iEffectProbability;
}
// Arrays
int CvFeatureInfo::getYieldChange(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiYieldChange ? m_aiYieldChange[i] : -1;
}
int CvFeatureInfo::getRiverYieldIncrease(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiRiverYieldIncrease ? m_aiRiverYieldIncrease[i] : -1;
}
int CvFeatureInfo::get3DAudioScriptFootstepIndex(int i) const
{
	//	FAssertMsg(i < ?, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_ai3DAudioScriptFootstepIndex ? m_ai3DAudioScriptFootstepIndex[i] : -1;
}
bool CvFeatureInfo::isTerrain(int i) const
{
	FAssertMsg(i < GC.getNumTerrainInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abTerrain ? m_abTerrain[i] : false;
}
int CvFeatureInfo::getNumVarieties() const
{
	return getArtInfo()->getNumVarieties();
}
const char* CvFeatureInfo::getButton() const
{
	const CvArtInfoFeature * pFeatureArtInfo;
	pFeatureArtInfo = getArtInfo();
	if (pFeatureArtInfo != NULL)
	{
		return pFeatureArtInfo->getButton();
	}
	else
	{
		return NULL;
	}
}
const CvArtInfoFeature* CvFeatureInfo::getArtInfo() const
{
	return ARTFILEMGR.getFeatureArtInfo( getArtDefineTag());
}
bool CvFeatureInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName( szTextVal, "ArtDefineTag");
	setArtDefineTag(szTextVal);
	pXML->SetVariableListTagPair(&m_aiYieldChange, "YieldChanges", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiRiverYieldIncrease, "RiverYieldIncreases", NUM_YIELD_TYPES, 0);
	pXML->GetChildXmlValByName(&m_iMovementCost, "iMovement");
	pXML->GetChildXmlValByName(&m_iSeeThroughChange, "iSeeThrough");
	pXML->GetChildXmlValByName(&m_iDefenseModifier, "iDefense");
	pXML->GetChildXmlValByName(&m_iAdvancedStartRemoveCost, "iAdvancedStartRemoveCost");
	pXML->GetChildXmlValByName(&m_iAppearanceProbability, "iAppearance");
	pXML->GetChildXmlValByName(&m_iDisappearanceProbability, "iDisappearance");
	pXML->GetChildXmlValByName(&m_iGrowthProbability, "iGrowth");
	pXML->GetChildXmlValByName(&m_bNoCoast, "bNoCoast");
	pXML->GetChildXmlValByName(&m_bNoRiver, "bNoRiver");
	pXML->GetChildXmlValByName(&m_bNoAdjacent, "bNoAdjacent");
	pXML->GetChildXmlValByName(&m_bRequiresFlatlands, "bRequiresFlatlands");
	pXML->GetChildXmlValByName(&m_bRequiresRiver, "bRequiresRiver");
	pXML->GetChildXmlValByName(&m_bImpassable, "bImpassable");
	pXML->GetChildXmlValByName(&m_bNoCity, "bNoCity");
	pXML->GetChildXmlValByName(&m_bNoImprovement, "bNoImprovement");
	pXML->GetChildXmlValByName(&m_bVisibleAlways, "bVisibleAlways");
	pXML->GetChildXmlValByName(m_szOnUnitChangeTo, "OnUnitChangeTo");
	pXML->SetVariableListTagPairForAudioScripts(&m_ai3DAudioScriptFootstepIndex, "FootstepSounds", GC.getNumFootstepAudioTypes());
	pXML->GetChildXmlValByName(szTextVal, "WorldSoundscapeAudioScript");
	if ( szTextVal.GetLength() > 0 )
	{
		m_iWorldSoundscapeScriptId = gDLL->getAudioTagIndex( szTextVal.GetCString(), AUDIOTAG_SOUNDSCAPE );
	}
	else
	{
		m_iWorldSoundscapeScriptId = -1;
	}
	pXML->GetChildXmlValByName(m_szEffectType, "EffectType");
	pXML->GetChildXmlValByName(&m_iEffectProbability, "iEffectProbability");
	pXML->SetVariableListTagPair(&m_abTerrain, "TerrainBooleans", GC.getNumTerrainInfos(), false);
	return true;
}
//======================================================================================================
//					CvYieldInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvYieldInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvYieldInfo::CvYieldInfo() :
m_iChar(0),
m_iBuyPriceLow(0),
m_iBuyPriceHigh(0),
m_iSellPriceDifference(0),
m_iPriceChangeThreshold(0),
m_iPriceCorrectionPercent(0),
m_iNativeBuyPrice(0),
m_iNativeSellPrice(0),
m_iNativeConsumptionPercent(0),
m_iNativeHappy(0),
m_iHillsChange(0),
m_iPeakChange(0),
m_iLakeChange(0),
m_iCityChange(0),
m_iMinCity(0),
m_iAIWeightPercent(0),
m_iAIBaseValue(0),
m_iNativeBaseValue(0),
m_iColorType(NO_COLOR),
m_iUnitClass(NO_UNITCLASS),
m_iTextureIndex(-1),
m_iWaterTextureIndex(-1),
m_iPowerValue(0),
m_iAssetValue(0),
m_bCargo(false)
{
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvYieldInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvYieldInfo::~CvYieldInfo()
{
}
int CvYieldInfo::getChar() const
{
	return m_iChar;
}
void CvYieldInfo::setChar(int i)
{
	m_iChar = i;
}
const char* CvYieldInfo::getIcon() const
{
	return m_szIcon;
}
const char* CvYieldInfo::getHighlightIcon() const
{
	return m_szHightlightIcon;
}
int CvYieldInfo::getBuyPriceLow() const
{
	return m_iBuyPriceLow;
}
int CvYieldInfo::getBuyPriceHigh() const
{
	return m_iBuyPriceHigh;
}
int CvYieldInfo::getSellPriceDifference() const
{
	return m_iSellPriceDifference;
}
int CvYieldInfo::getPriceChangeThreshold() const
{
	return m_iPriceChangeThreshold;
}
int CvYieldInfo::getPriceCorrectionPercent() const
{
	return m_iPriceCorrectionPercent;
}
int CvYieldInfo::getNativeBuyPrice() const
{
	return m_iNativeBuyPrice;
}
int CvYieldInfo::getNativeSellPrice() const
{
	return m_iNativeSellPrice;
}
int CvYieldInfo::getNativeConsumptionPercent() const
{
	return m_iNativeConsumptionPercent;
}
int CvYieldInfo::getNativeHappy() const
{
	return m_iNativeHappy;
}
int CvYieldInfo::getHillsChange() const
{
	return m_iHillsChange;
}
int CvYieldInfo::getPeakChange() const
{
	return m_iPeakChange;
}
int CvYieldInfo::getLakeChange() const
{
	return m_iLakeChange;
}
int CvYieldInfo::getCityChange() const
{
	return m_iCityChange;
}
int CvYieldInfo::getMinCity() const
{
	return m_iMinCity;
}
int CvYieldInfo::getAIWeightPercent() const
{
	return m_iAIWeightPercent;
}
int CvYieldInfo::getAIBaseValue() const
{
	return m_iAIBaseValue;
}
int CvYieldInfo::getNativeBaseValue() const
{
	return m_iNativeBaseValue;
}
int CvYieldInfo::getColorType() const
{
	return m_iColorType;
}
int CvYieldInfo::getUnitClass() const
{
	return m_iUnitClass;
}
int CvYieldInfo::getTextureIndex() const
{
	return m_iTextureIndex;
}
int CvYieldInfo::getWaterTextureIndex() const
{
	return m_iWaterTextureIndex;
}
int CvYieldInfo::getPowerValue() const
{
	return m_iPowerValue;
}
int CvYieldInfo::getAssetValue() const
{
	return m_iAssetValue;
}
bool CvYieldInfo::isCargo() const
{
	return m_bCargo;
}

bool CvYieldInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_iBuyPriceLow, "iBuyPriceLow");
	pXML->GetChildXmlValByName(&m_iBuyPriceHigh, "iBuyPriceHigh");
	pXML->GetChildXmlValByName(&m_iSellPriceDifference, "iSellPriceDifference");
	pXML->GetChildXmlValByName(&m_iPriceChangeThreshold, "iPriceChangeThreshold");
	pXML->GetChildXmlValByName(&m_iPriceCorrectionPercent, "iPriceCorrectionPercent");
	pXML->GetChildXmlValByName(&m_iNativeBuyPrice, "iNativeBuyPrice");
	pXML->GetChildXmlValByName(&m_iNativeSellPrice, "iNativeSellPrice");
	pXML->GetChildXmlValByName(&m_iNativeConsumptionPercent, "iNativeConsumptionPercent");
	pXML->GetChildXmlValByName(&m_iNativeHappy, "iNativeHappy");
	pXML->GetChildXmlValByName(&m_iHillsChange, "iHillsChange");
	pXML->GetChildXmlValByName(&m_iPeakChange, "iPeakChange");
	pXML->GetChildXmlValByName(&m_iLakeChange, "iLakeChange");
	pXML->GetChildXmlValByName(&m_iCityChange, "iCityChange");
	pXML->GetChildXmlValByName(&m_iMinCity, "iMinCity");
	pXML->GetChildXmlValByName(&m_iAIWeightPercent, "iAIWeightPercent");
	pXML->GetChildXmlValByName(&m_iAIBaseValue, "iAIBaseValue");
	pXML->GetChildXmlValByName(&m_iNativeBaseValue, "iNativeBaseValue");
	pXML->GetChildXmlValByName(szTextVal, "ColorType");
	m_iColorType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "UnitClass");
	m_iUnitClass = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iTextureIndex, "iTextureIndex");
	pXML->GetChildXmlValByName(&m_iWaterTextureIndex, "iWaterTextureIndex");
	pXML->GetChildXmlValByName(&m_iPowerValue, "iPower");
	pXML->GetChildXmlValByName(&m_iAssetValue, "iAsset");
	pXML->GetChildXmlValByName(&m_bCargo, "bCargo");
	pXML->GetChildXmlValByName(m_szIcon, "Icon");
	pXML->GetChildXmlValByName(m_szHightlightIcon, "HightlightIcon");

	return true;
}
//======================================================================================================
//					CvTerrainInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvTerrainInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvTerrainInfo::CvTerrainInfo() :
m_iMovementCost(0),
m_iSeeFromLevel(0),
m_iSeeThroughLevel(0),
m_iBuildModifier(0),
m_iDefenseModifier(0),
m_bWater(false),
m_bImpassable(false),
m_bFound(false),
m_bFoundCoast(false),
m_iWorldSoundscapeScriptId(0),
m_aiYields(NULL),
m_aiRiverYieldIncrease(NULL),
m_ai3DAudioScriptFootstepIndex(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvTerrainInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvTerrainInfo::~CvTerrainInfo()
{
	SAFE_DELETE_ARRAY(m_aiYields);
	SAFE_DELETE_ARRAY(m_aiRiverYieldIncrease);
	SAFE_DELETE_ARRAY(m_ai3DAudioScriptFootstepIndex);
}
int CvTerrainInfo::getMovementCost() const
{
	return m_iMovementCost;
}
int CvTerrainInfo::getSeeFromLevel() const
{
	return m_iSeeFromLevel;
}
int CvTerrainInfo::getSeeThroughLevel() const
{
	return m_iSeeThroughLevel;
}
int CvTerrainInfo::getBuildModifier() const
{
	return m_iBuildModifier;
}
int CvTerrainInfo::getDefenseModifier() const
{
	return m_iDefenseModifier;
}
bool CvTerrainInfo::isWater() const
{
	return m_bWater;
}
bool CvTerrainInfo::isImpassable() const
{
	return m_bImpassable;
}
bool CvTerrainInfo::isFound() const
{
	return m_bFound;
}
bool CvTerrainInfo::isFoundCoast() const
{
	return m_bFoundCoast;
}
const char* CvTerrainInfo::getArtDefineTag() const
{
	return m_szArtDefineTag;
}
void CvTerrainInfo::setArtDefineTag(const char* szTag)
{
	m_szArtDefineTag = szTag;
}
int CvTerrainInfo::getWorldSoundscapeScriptId() const
{
	return m_iWorldSoundscapeScriptId;
}
// Arrays
int CvTerrainInfo::getYield(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiYields ? m_aiYields[i] : -1;
}
int CvTerrainInfo::getRiverYieldIncrease(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiRiverYieldIncrease ? m_aiRiverYieldIncrease[i] : -1;
}
int CvTerrainInfo::get3DAudioScriptFootstepIndex(int i) const
{
//	FAssertMsg(i < ?, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_ai3DAudioScriptFootstepIndex ? m_ai3DAudioScriptFootstepIndex[i] : -1;
}
bool CvTerrainInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName( szTextVal, "ArtDefineTag");
	setArtDefineTag(szTextVal);
	pXML->SetVariableListTagPair(&m_aiYields, "Yields", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiRiverYieldIncrease, "RiverYieldIncreases", NUM_YIELD_TYPES, 0);

	pXML->GetChildXmlValByName(&m_bWater, "bWater");
	pXML->GetChildXmlValByName(&m_bImpassable, "bImpassable");
	pXML->GetChildXmlValByName(&m_bFound, "bFound");
	pXML->GetChildXmlValByName(&m_bFoundCoast, "bFoundCoast");
	pXML->GetChildXmlValByName(&m_iMovementCost, "iMovement");
	pXML->GetChildXmlValByName(&m_iSeeFromLevel, "iSeeFrom");
	pXML->GetChildXmlValByName(&m_iSeeThroughLevel, "iSeeThrough");
	pXML->GetChildXmlValByName(&m_iBuildModifier, "iBuildModifier");
	pXML->GetChildXmlValByName(&m_iDefenseModifier, "iDefense");
	pXML->SetVariableListTagPairForAudioScripts(&m_ai3DAudioScriptFootstepIndex, "FootstepSounds", GC.getNumFootstepAudioTypes());
	pXML->GetChildXmlValByName(szTextVal, "WorldSoundscapeAudioScript");
	if ( szTextVal.GetLength() > 0 )
		m_iWorldSoundscapeScriptId = gDLL->getAudioTagIndex( szTextVal.GetCString(), AUDIOTAG_SOUNDSCAPE );
	else
		m_iWorldSoundscapeScriptId = -1;
	return true;
}
const char* CvTerrainInfo::getButton() const
{
	const CvArtInfoTerrain * pTerrainArtInfo;
	pTerrainArtInfo = getArtInfo();
	if (pTerrainArtInfo != NULL)
	{
		return pTerrainArtInfo->getButton();
	}
	else
	{
		return NULL;
	}
}
const CvArtInfoTerrain* CvTerrainInfo::getArtInfo() const
{
	return ARTFILEMGR.getTerrainArtInfo(getArtDefineTag());
}
//======================================================================================================
//					CvInterfaceModeInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvInterfaceModeInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvInterfaceModeInfo::CvInterfaceModeInfo() :
m_iCursorIndex(NO_CURSOR),
m_iMissionType(NO_MISSION),
m_bVisible(false),
m_bGotoPlot(false),
m_bHighlightPlot(false),
m_bSelectType(false),
m_bSelectAll(false)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvInterfaceModeInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvInterfaceModeInfo::~CvInterfaceModeInfo()
{
}
int CvInterfaceModeInfo::getCursorIndex() const
{
	return m_iCursorIndex;
}
int CvInterfaceModeInfo::getMissionType() const
{
	return m_iMissionType;
}
bool CvInterfaceModeInfo::getVisible() const
{
	return m_bVisible;
}
bool CvInterfaceModeInfo::getGotoPlot() const
{
	return m_bGotoPlot;
}
bool CvInterfaceModeInfo::getHighlightPlot() const
{
	return m_bHighlightPlot;
}
bool CvInterfaceModeInfo::getSelectType() const
{
	return m_bSelectType;
}
bool CvInterfaceModeInfo::getSelectAll() const
{
	return m_bSelectAll;
}
bool CvInterfaceModeInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvHotkeyInfo::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "CursorType");
	m_iCursorIndex = pXML->FindInInfoClass( szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "Mission");
	m_iMissionType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_bVisible, "bVisible");
	pXML->GetChildXmlValByName(&m_bGotoPlot, "bGotoPlot");
	pXML->GetChildXmlValByName(&m_bHighlightPlot, "bHighlightPlot");
	pXML->GetChildXmlValByName(&m_bSelectType, "bSelectType");
	pXML->GetChildXmlValByName(&m_bSelectAll, "bSelectAll");
	return true;
}
//======================================================================================================
//					CvLeaderHeadInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvLeaderHeadInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvLeaderHeadInfo::CvLeaderHeadInfo() :
m_iAlarmType(NO_ALARM),
m_iBaseAttitude(0),
m_iNativeAttitude(0),
m_iRefuseToTalkWarThreshold(0),
m_iMaxGoldTradePercent(0),
m_iMaxWarRand(0),
m_iMaxWarNearbyPowerRatio(0),
m_iMaxWarDistantPowerRatio(0),
m_iMaxWarMinAdjacentLandPercent(0),
m_iLimitedWarRand(0),
m_iLimitedWarPowerRatio(0),
m_iDogpileWarRand(0),
m_iMakePeaceRand(0),
m_iDeclareWarTradeRand(0),
m_iDemandRebukedSneakProb(0),
m_iDemandRebukedWarProb(0),
m_iRazeCityProb(0),
m_iBaseAttackOddsChange(0),
m_iAttackOddsChangeRand(0),
m_iCloseBordersAttitudeChange(0),
m_iAlarmAttitudeChange(0),
m_iLostWarAttitudeChange(0),
m_iRebelAttitudeDivisor(0),
m_iAtWarAttitudeDivisor(0),
m_iAtWarAttitudeChangeLimit(0),
m_iAtPeaceAttitudeDivisor(0),
m_iAtPeaceAttitudeChangeLimit(0),
m_iOpenBordersAttitudeDivisor(0),
m_iOpenBordersAttitudeChangeLimit(0),
m_iDefensivePactAttitudeDivisor(0),
m_iDefensivePactAttitudeChangeLimit(0),
m_iShareWarAttitudeChange(0),
m_iShareWarAttitudeDivisor(0),
m_iShareWarAttitudeChangeLimit(0),
m_iDemandTributeAttitudeThreshold(NO_ATTITUDE),
m_iNoGiveHelpAttitudeThreshold(NO_ATTITUDE),
m_iMapRefuseAttitudeThreshold(NO_ATTITUDE),
m_iDeclareWarRefuseAttitudeThreshold(NO_ATTITUDE),
m_iDeclareWarThemRefuseAttitudeThreshold(NO_ATTITUDE),
m_iStopTradingRefuseAttitudeThreshold(NO_ATTITUDE),
m_iStopTradingThemRefuseAttitudeThreshold(NO_ATTITUDE),
m_iOpenBordersRefuseAttitudeThreshold(NO_ATTITUDE),
m_iDefensivePactRefuseAttitudeThreshold(NO_ATTITUDE),
m_iPermanentAllianceRefuseAttitudeThreshold(NO_ATTITUDE),
m_abTraits(NULL),
m_aiContactRand(NULL),
m_aiContactDelay(NULL),
m_aiMemoryDecayRand(NULL),
m_aiMemoryAttitudePercent(NULL),
m_aiNoWarAttitudeProb(NULL),
m_aiUnitAIWeightModifier(NULL),
m_aiImprovementWeightModifier(NULL),
m_aiDiploPeaceMusicScriptIds(NULL),
m_aiDiploWarMusicScriptIds(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvLeaderHeadInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvLeaderHeadInfo::~CvLeaderHeadInfo()
{
	SAFE_DELETE_ARRAY(m_abTraits);
	SAFE_DELETE_ARRAY(m_aiContactRand);
	SAFE_DELETE_ARRAY(m_aiContactDelay);
	SAFE_DELETE_ARRAY(m_aiMemoryDecayRand);
	SAFE_DELETE_ARRAY(m_aiMemoryAttitudePercent);
	SAFE_DELETE_ARRAY(m_aiNoWarAttitudeProb);
	SAFE_DELETE_ARRAY(m_aiUnitAIWeightModifier);
	SAFE_DELETE_ARRAY(m_aiImprovementWeightModifier);
	SAFE_DELETE_ARRAY(m_aiDiploPeaceMusicScriptIds);
	SAFE_DELETE_ARRAY(m_aiDiploWarMusicScriptIds);
}
const char* CvLeaderHeadInfo::getButton() const
{
	const CvArtInfoLeaderhead * pLeaderheadArtInfo;
	pLeaderheadArtInfo = getArtInfo();
	if (pLeaderheadArtInfo != NULL)
	{
		return pLeaderheadArtInfo->getButton();
	}
	else
	{
		return NULL;
	}
}
int CvLeaderHeadInfo::getAlarmType() const
{
	return m_iAlarmType;
}
int CvLeaderHeadInfo::getBaseAttitude() const
{
	return m_iBaseAttitude;
}
int CvLeaderHeadInfo::getNativeAttitude() const
{
	return m_iNativeAttitude;
}
int CvLeaderHeadInfo::getRefuseToTalkWarThreshold() const
{
	return m_iRefuseToTalkWarThreshold;
}
int CvLeaderHeadInfo::getMaxGoldTradePercent() const
{
	return m_iMaxGoldTradePercent;
}
int CvLeaderHeadInfo::getMaxWarRand() const
{
	return m_iMaxWarRand;
}
int CvLeaderHeadInfo::getMaxWarNearbyPowerRatio() const
{
	return m_iMaxWarNearbyPowerRatio;
}
int CvLeaderHeadInfo::getMaxWarDistantPowerRatio() const
{
	return m_iMaxWarDistantPowerRatio;
}
int CvLeaderHeadInfo::getMaxWarMinAdjacentLandPercent() const
{
	return m_iMaxWarMinAdjacentLandPercent;
}
int CvLeaderHeadInfo::getLimitedWarRand() const
{
	return m_iLimitedWarRand;
}
int CvLeaderHeadInfo::getLimitedWarPowerRatio() const
{
	return m_iLimitedWarPowerRatio;
}
int CvLeaderHeadInfo::getDogpileWarRand() const
{
	return m_iDogpileWarRand;
}
int CvLeaderHeadInfo::getMakePeaceRand() const
{
	return m_iMakePeaceRand;
}
int CvLeaderHeadInfo::getDeclareWarTradeRand() const
{
	return m_iDeclareWarTradeRand;
}
int CvLeaderHeadInfo::getDemandRebukedSneakProb() const
{
	return m_iDemandRebukedSneakProb;
}
int CvLeaderHeadInfo::getDemandRebukedWarProb() const
{
	return m_iDemandRebukedWarProb;
}
int CvLeaderHeadInfo::getRazeCityProb() const
{
	return m_iRazeCityProb;
}
int CvLeaderHeadInfo::getBaseAttackOddsChange() const
{
	return m_iBaseAttackOddsChange;
}
int CvLeaderHeadInfo::getAttackOddsChangeRand() const
{
	return m_iAttackOddsChangeRand;
}
int CvLeaderHeadInfo::getCloseBordersAttitudeChange() const
{
	return m_iCloseBordersAttitudeChange;
}
int CvLeaderHeadInfo::getAlarmAttitudeChange() const
{
	return m_iAlarmAttitudeChange;
}
int CvLeaderHeadInfo::getLostWarAttitudeChange() const
{
	return m_iLostWarAttitudeChange;
}
int CvLeaderHeadInfo::getRebelAttitudeDivisor() const
{
	return m_iRebelAttitudeDivisor;
}
int CvLeaderHeadInfo::getAtWarAttitudeDivisor() const
{
	return m_iAtWarAttitudeDivisor;
}
int CvLeaderHeadInfo::getAtWarAttitudeChangeLimit() const
{
	return m_iAtWarAttitudeChangeLimit;
}
int CvLeaderHeadInfo::getAtPeaceAttitudeDivisor() const
{
	return m_iAtPeaceAttitudeDivisor;
}
int CvLeaderHeadInfo::getAtPeaceAttitudeChangeLimit() const
{
	return m_iAtPeaceAttitudeChangeLimit;
}
int CvLeaderHeadInfo::getOpenBordersAttitudeDivisor() const
{
	return m_iOpenBordersAttitudeDivisor;
}
int CvLeaderHeadInfo::getOpenBordersAttitudeChangeLimit() const
{
	return m_iOpenBordersAttitudeChangeLimit;
}
int CvLeaderHeadInfo::getDefensivePactAttitudeDivisor() const
{
	return m_iDefensivePactAttitudeDivisor;
}
int CvLeaderHeadInfo::getDefensivePactAttitudeChangeLimit() const
{
	return m_iDefensivePactAttitudeChangeLimit;
}
int CvLeaderHeadInfo::getShareWarAttitudeChange() const
{
	return m_iShareWarAttitudeChange;
}
int CvLeaderHeadInfo::getShareWarAttitudeDivisor() const
{
	return m_iShareWarAttitudeDivisor;
}
int CvLeaderHeadInfo::getShareWarAttitudeChangeLimit() const
{
	return m_iShareWarAttitudeChangeLimit;
}
int CvLeaderHeadInfo::getDemandTributeAttitudeThreshold() const
{
	return m_iDemandTributeAttitudeThreshold;
}
int CvLeaderHeadInfo::getNoGiveHelpAttitudeThreshold() const
{
	return m_iNoGiveHelpAttitudeThreshold;
}
int CvLeaderHeadInfo::getMapRefuseAttitudeThreshold() const
{
	return m_iMapRefuseAttitudeThreshold;
}
int CvLeaderHeadInfo::getDeclareWarRefuseAttitudeThreshold() const
{
	return m_iDeclareWarRefuseAttitudeThreshold;
}
int CvLeaderHeadInfo::getDeclareWarThemRefuseAttitudeThreshold() const
{
	return m_iDeclareWarThemRefuseAttitudeThreshold;
}
int CvLeaderHeadInfo::getStopTradingRefuseAttitudeThreshold() const
{
	return m_iStopTradingRefuseAttitudeThreshold;
}
int CvLeaderHeadInfo::getStopTradingThemRefuseAttitudeThreshold() const
{
	return m_iStopTradingThemRefuseAttitudeThreshold;
}
int CvLeaderHeadInfo::getOpenBordersRefuseAttitudeThreshold() const
{
	return m_iOpenBordersRefuseAttitudeThreshold;
}
int CvLeaderHeadInfo::getDefensivePactRefuseAttitudeThreshold() const
{
	return m_iDefensivePactRefuseAttitudeThreshold;
}
int CvLeaderHeadInfo::getPermanentAllianceRefuseAttitudeThreshold() const
{
	return m_iPermanentAllianceRefuseAttitudeThreshold;
}
const char* CvLeaderHeadInfo::getArtDefineTag() const
{
	return m_szArtDefineTag;
}
void CvLeaderHeadInfo::setArtDefineTag(const char* szVal)
{
	m_szArtDefineTag = szVal;
}
// Arrays
bool CvLeaderHeadInfo::hasTrait(int i) const
{
	FAssertMsg(i < GC.getNumTraitInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_abTraits ? m_abTraits[i] : false;
}
int CvLeaderHeadInfo::getContactRand(int i) const
{
	FAssertMsg(i < NUM_CONTACT_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiContactRand ? m_aiContactRand[i] : -1;
}
int CvLeaderHeadInfo::getContactDelay(int i) const
{
	FAssertMsg(i < NUM_CONTACT_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiContactDelay ? m_aiContactDelay[i] : -1;
}
int CvLeaderHeadInfo::getMemoryDecayRand(int i) const
{
	FAssertMsg(i < NUM_MEMORY_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiMemoryDecayRand ? m_aiMemoryDecayRand[i] : -1;
}
int CvLeaderHeadInfo::getMemoryAttitudePercent(int i) const
{
	FAssertMsg(i < NUM_MEMORY_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiMemoryAttitudePercent ? m_aiMemoryAttitudePercent[i] : -1;
}
int CvLeaderHeadInfo::getNoWarAttitudeProb(int i) const
{
	FAssertMsg(i < NUM_ATTITUDE_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiNoWarAttitudeProb ? m_aiNoWarAttitudeProb[i] : -1;
}
int CvLeaderHeadInfo::getUnitAIWeightModifier(int i) const
{
	FAssertMsg(i < NUM_UNITAI_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiUnitAIWeightModifier ? m_aiUnitAIWeightModifier[i] : -1;
}
int CvLeaderHeadInfo::getImprovementWeightModifier(int i) const
{
	FAssertMsg(i < GC.getNumImprovementInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiImprovementWeightModifier ? m_aiImprovementWeightModifier[i] : -1;
}
int CvLeaderHeadInfo::getDiploPeaceMusicScriptIds(int i) const
{
	FAssertMsg(i < GC.getNumEraInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiDiploPeaceMusicScriptIds ? m_aiDiploPeaceMusicScriptIds[i] : -1;
}
int CvLeaderHeadInfo::getDiploWarMusicScriptIds(int i) const
{
	FAssertMsg(i < GC.getNumEraInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiDiploWarMusicScriptIds ? m_aiDiploWarMusicScriptIds[i] : -1;
}
const char* CvLeaderHeadInfo::getLeaderHead() const
{
	const CvArtInfoLeaderhead * pLeaderheadArtInfo;
	pLeaderheadArtInfo = getArtInfo();
	if (pLeaderheadArtInfo != NULL)
	{
		return pLeaderheadArtInfo->getNIF();
	}
	else
	{
		return NULL;
	}
}
void CvLeaderHeadInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);		// flag for expansion
	stream->Read(&m_iAlarmType);
	stream->Read(&m_iBaseAttitude);
	stream->Read(&m_iNativeAttitude);
	stream->Read(&m_iRefuseToTalkWarThreshold);
	stream->Read(&m_iMaxGoldTradePercent);
	stream->Read(&m_iMaxWarRand);
	stream->Read(&m_iMaxWarNearbyPowerRatio);
	stream->Read(&m_iMaxWarDistantPowerRatio);
	stream->Read(&m_iMaxWarMinAdjacentLandPercent);
	stream->Read(&m_iLimitedWarRand);
	stream->Read(&m_iLimitedWarPowerRatio);
	stream->Read(&m_iDogpileWarRand);
	stream->Read(&m_iMakePeaceRand);
	stream->Read(&m_iDeclareWarTradeRand);
	stream->Read(&m_iDemandRebukedSneakProb);
	stream->Read(&m_iDemandRebukedWarProb);
	stream->Read(&m_iRazeCityProb);
	stream->Read(&m_iBaseAttackOddsChange);
	stream->Read(&m_iAttackOddsChangeRand);
	stream->Read(&m_iCloseBordersAttitudeChange);
	stream->Read(&m_iAlarmAttitudeChange);
	stream->Read(&m_iLostWarAttitudeChange);
	stream->Read(&m_iRebelAttitudeDivisor);
	stream->Read(&m_iAtWarAttitudeDivisor);
	stream->Read(&m_iAtWarAttitudeChangeLimit);
	stream->Read(&m_iAtPeaceAttitudeDivisor);
	stream->Read(&m_iAtPeaceAttitudeChangeLimit);
	stream->Read(&m_iOpenBordersAttitudeDivisor);
	stream->Read(&m_iOpenBordersAttitudeChangeLimit);
	stream->Read(&m_iDefensivePactAttitudeDivisor);
	stream->Read(&m_iDefensivePactAttitudeChangeLimit);
	stream->Read(&m_iShareWarAttitudeChange);
	stream->Read(&m_iShareWarAttitudeDivisor);
	stream->Read(&m_iShareWarAttitudeChangeLimit);
	stream->Read(&m_iDemandTributeAttitudeThreshold);
	stream->Read(&m_iNoGiveHelpAttitudeThreshold);
	stream->Read(&m_iMapRefuseAttitudeThreshold);
	stream->Read(&m_iDeclareWarRefuseAttitudeThreshold);
	stream->Read(&m_iDeclareWarThemRefuseAttitudeThreshold);
	stream->Read(&m_iStopTradingRefuseAttitudeThreshold);
	stream->Read(&m_iStopTradingThemRefuseAttitudeThreshold);
	stream->Read(&m_iOpenBordersRefuseAttitudeThreshold);
	stream->Read(&m_iDefensivePactRefuseAttitudeThreshold);
	stream->Read(&m_iPermanentAllianceRefuseAttitudeThreshold);
	stream->ReadString(m_szArtDefineTag);
	// Arrays
	SAFE_DELETE_ARRAY(m_abTraits);
	m_abTraits = new bool[GC.getNumTraitInfos()];
	stream->Read(GC.getNumTraitInfos(), m_abTraits);
	SAFE_DELETE_ARRAY(m_aiContactRand);
	m_aiContactRand = new int[NUM_CONTACT_TYPES];
	stream->Read(NUM_CONTACT_TYPES, m_aiContactRand);
	SAFE_DELETE_ARRAY(m_aiContactDelay);
	m_aiContactDelay = new int[NUM_CONTACT_TYPES];
	stream->Read(NUM_CONTACT_TYPES, m_aiContactDelay);
	SAFE_DELETE_ARRAY(m_aiMemoryDecayRand);
	m_aiMemoryDecayRand = new int[NUM_MEMORY_TYPES];
	stream->Read(NUM_MEMORY_TYPES, m_aiMemoryDecayRand);
	SAFE_DELETE_ARRAY(m_aiMemoryAttitudePercent);
	m_aiMemoryAttitudePercent = new int[NUM_MEMORY_TYPES];
	stream->Read(NUM_MEMORY_TYPES, m_aiMemoryAttitudePercent);
	SAFE_DELETE_ARRAY(m_aiNoWarAttitudeProb);
	m_aiNoWarAttitudeProb = new int[NUM_ATTITUDE_TYPES];
	stream->Read(NUM_ATTITUDE_TYPES, m_aiNoWarAttitudeProb);
	SAFE_DELETE_ARRAY(m_aiUnitAIWeightModifier);
	m_aiUnitAIWeightModifier = new int[NUM_UNITAI_TYPES];
	stream->Read(NUM_UNITAI_TYPES, m_aiUnitAIWeightModifier);
	SAFE_DELETE_ARRAY(m_aiImprovementWeightModifier);
	m_aiImprovementWeightModifier = new int[GC.getNumImprovementInfos()];
	stream->Read(GC.getNumImprovementInfos(), m_aiImprovementWeightModifier);
	SAFE_DELETE_ARRAY(m_aiDiploPeaceMusicScriptIds);
	m_aiDiploPeaceMusicScriptIds = new int[GC.getNumEraInfos()];
	stream->Read(GC.getNumEraInfos(), m_aiDiploPeaceMusicScriptIds);
	SAFE_DELETE_ARRAY(m_aiDiploWarMusicScriptIds);
	m_aiDiploWarMusicScriptIds = new int[GC.getNumEraInfos()];
	stream->Read(GC.getNumEraInfos(), m_aiDiploWarMusicScriptIds);
}
void CvLeaderHeadInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_iAlarmType);
	stream->Write(m_iBaseAttitude);
	stream->Write(m_iNativeAttitude);
	stream->Write(m_iRefuseToTalkWarThreshold);
	stream->Write(m_iMaxGoldTradePercent);
	stream->Write(m_iMaxWarRand);
	stream->Write(m_iMaxWarNearbyPowerRatio);
	stream->Write(m_iMaxWarDistantPowerRatio);
	stream->Write(m_iMaxWarMinAdjacentLandPercent);
	stream->Write(m_iLimitedWarRand);
	stream->Write(m_iLimitedWarPowerRatio);
	stream->Write(m_iDogpileWarRand);
	stream->Write(m_iMakePeaceRand);
	stream->Write(m_iDeclareWarTradeRand);
	stream->Write(m_iDemandRebukedSneakProb);
	stream->Write(m_iDemandRebukedWarProb);
	stream->Write(m_iRazeCityProb);
	stream->Write(m_iBaseAttackOddsChange);
	stream->Write(m_iAttackOddsChangeRand);
	stream->Write(m_iCloseBordersAttitudeChange);
	stream->Write(m_iAlarmAttitudeChange);
	stream->Write(m_iLostWarAttitudeChange);
	stream->Write(m_iRebelAttitudeDivisor);
	stream->Write(m_iAtWarAttitudeDivisor);
	stream->Write(m_iAtWarAttitudeChangeLimit);
	stream->Write(m_iAtPeaceAttitudeDivisor);
	stream->Write(m_iAtPeaceAttitudeChangeLimit);
	stream->Write(m_iOpenBordersAttitudeDivisor);
	stream->Write(m_iOpenBordersAttitudeChangeLimit);
	stream->Write(m_iDefensivePactAttitudeDivisor);
	stream->Write(m_iDefensivePactAttitudeChangeLimit);
	stream->Write(m_iShareWarAttitudeChange);
	stream->Write(m_iShareWarAttitudeDivisor);
	stream->Write(m_iShareWarAttitudeChangeLimit);
	stream->Write(m_iDemandTributeAttitudeThreshold);
	stream->Write(m_iNoGiveHelpAttitudeThreshold);
	stream->Write(m_iMapRefuseAttitudeThreshold);
	stream->Write(m_iDeclareWarRefuseAttitudeThreshold);
	stream->Write(m_iDeclareWarThemRefuseAttitudeThreshold);
	stream->Write(m_iStopTradingRefuseAttitudeThreshold);
	stream->Write(m_iStopTradingThemRefuseAttitudeThreshold);
	stream->Write(m_iOpenBordersRefuseAttitudeThreshold);
	stream->Write(m_iDefensivePactRefuseAttitudeThreshold);
	stream->Write(m_iPermanentAllianceRefuseAttitudeThreshold);
	stream->WriteString(m_szArtDefineTag);
	// Arrays
	stream->Write(GC.getNumTraitInfos(), m_abTraits);
	stream->Write(NUM_CONTACT_TYPES, m_aiContactRand);
	stream->Write(NUM_CONTACT_TYPES, m_aiContactDelay);
	stream->Write(NUM_MEMORY_TYPES, m_aiMemoryDecayRand);
	stream->Write(NUM_MEMORY_TYPES, m_aiMemoryAttitudePercent);
	stream->Write(NUM_ATTITUDE_TYPES, m_aiNoWarAttitudeProb);
	stream->Write(NUM_UNITAI_TYPES, m_aiUnitAIWeightModifier);
	stream->Write(GC.getNumImprovementInfos(), m_aiImprovementWeightModifier);
	stream->Write(GC.getNumEraInfos(), m_aiDiploPeaceMusicScriptIds);
	stream->Write(GC.getNumEraInfos(), m_aiDiploWarMusicScriptIds);
}
const CvArtInfoLeaderhead* CvLeaderHeadInfo::getArtInfo() const
{
	return ARTFILEMGR.getLeaderheadArtInfo( getArtDefineTag());
}
bool CvLeaderHeadInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "ArtDefineTag");
	setArtDefineTag(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "AlarmType");
	m_iAlarmType = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iBaseAttitude, "iBaseAttitude");
	pXML->GetChildXmlValByName(&m_iNativeAttitude, "iNativeAttitude");
	pXML->GetChildXmlValByName(&m_iRefuseToTalkWarThreshold, "iRefuseToTalkWarThreshold");
	pXML->GetChildXmlValByName(&m_iMaxGoldTradePercent, "iMaxGoldTradePercent");
	pXML->GetChildXmlValByName(&m_iMaxWarRand, "iMaxWarRand");
	pXML->GetChildXmlValByName(&m_iMaxWarNearbyPowerRatio, "iMaxWarNearbyPowerRatio");
	pXML->GetChildXmlValByName(&m_iMaxWarDistantPowerRatio, "iMaxWarDistantPowerRatio");
	pXML->GetChildXmlValByName(&m_iMaxWarMinAdjacentLandPercent, "iMaxWarMinAdjacentLandPercent");
	pXML->GetChildXmlValByName(&m_iLimitedWarRand, "iLimitedWarRand");
	pXML->GetChildXmlValByName(&m_iLimitedWarPowerRatio, "iLimitedWarPowerRatio");
	pXML->GetChildXmlValByName(&m_iDogpileWarRand, "iDogpileWarRand");
	pXML->GetChildXmlValByName(&m_iMakePeaceRand, "iMakePeaceRand");
	pXML->GetChildXmlValByName(&m_iDeclareWarTradeRand, "iDeclareWarTradeRand");
	pXML->GetChildXmlValByName(&m_iDemandRebukedSneakProb, "iDemandRebukedSneakProb");
	pXML->GetChildXmlValByName(&m_iDemandRebukedWarProb, "iDemandRebukedWarProb");
	pXML->GetChildXmlValByName(&m_iRazeCityProb, "iRazeCityProb");
	pXML->GetChildXmlValByName(&m_iBaseAttackOddsChange, "iBaseAttackOddsChange");
	pXML->GetChildXmlValByName(&m_iAttackOddsChangeRand, "iAttackOddsChangeRand");
	pXML->GetChildXmlValByName(&m_iCloseBordersAttitudeChange, "iCloseBordersAttitudeChange");
	pXML->GetChildXmlValByName(&m_iAlarmAttitudeChange, "iAlarmAttitudeChange");
	pXML->GetChildXmlValByName(&m_iLostWarAttitudeChange, "iLostWarAttitudeChange");
	pXML->GetChildXmlValByName(&m_iRebelAttitudeDivisor, "iRebelAttitudeDivisor");
	pXML->GetChildXmlValByName(&m_iAtWarAttitudeDivisor, "iAtWarAttitudeDivisor");
	pXML->GetChildXmlValByName(&m_iAtWarAttitudeChangeLimit, "iAtWarAttitudeChangeLimit");
	pXML->GetChildXmlValByName(&m_iAtPeaceAttitudeDivisor, "iAtPeaceAttitudeDivisor");
	pXML->GetChildXmlValByName(&m_iAtPeaceAttitudeChangeLimit, "iAtPeaceAttitudeChangeLimit");
	pXML->GetChildXmlValByName(&m_iOpenBordersAttitudeDivisor, "iOpenBordersAttitudeDivisor");
	pXML->GetChildXmlValByName(&m_iOpenBordersAttitudeChangeLimit, "iOpenBordersAttitudeChangeLimit");
	pXML->GetChildXmlValByName(&m_iDefensivePactAttitudeDivisor, "iDefensivePactAttitudeDivisor");
	pXML->GetChildXmlValByName(&m_iDefensivePactAttitudeChangeLimit, "iDefensivePactAttitudeChangeLimit");
	pXML->GetChildXmlValByName(&m_iShareWarAttitudeChange, "iShareWarAttitudeChange");
	pXML->GetChildXmlValByName(&m_iShareWarAttitudeDivisor, "iShareWarAttitudeDivisor");
	pXML->GetChildXmlValByName(&m_iShareWarAttitudeChangeLimit, "iShareWarAttitudeChangeLimit");
	pXML->GetChildXmlValByName(szTextVal, "DemandTributeAttitudeThreshold");
	m_iDemandTributeAttitudeThreshold = pXML->FindInInfoClass( szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "NoGiveHelpAttitudeThreshold");
	m_iNoGiveHelpAttitudeThreshold = pXML->FindInInfoClass( szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "MapRefuseAttitudeThreshold");
	m_iMapRefuseAttitudeThreshold = pXML->FindInInfoClass( szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "DeclareWarRefuseAttitudeThreshold");
	m_iDeclareWarRefuseAttitudeThreshold = pXML->FindInInfoClass( szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "DeclareWarThemRefuseAttitudeThreshold");
	m_iDeclareWarThemRefuseAttitudeThreshold = pXML->FindInInfoClass( szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "StopTradingRefuseAttitudeThreshold");
	m_iStopTradingRefuseAttitudeThreshold = pXML->FindInInfoClass( szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "StopTradingThemRefuseAttitudeThreshold");
	m_iStopTradingThemRefuseAttitudeThreshold = pXML->FindInInfoClass( szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "OpenBordersRefuseAttitudeThreshold");
	m_iOpenBordersRefuseAttitudeThreshold = pXML->FindInInfoClass( szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "DefensivePactRefuseAttitudeThreshold");
	m_iDefensivePactRefuseAttitudeThreshold = pXML->FindInInfoClass( szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "PermanentAllianceRefuseAttitudeThreshold");
	m_iPermanentAllianceRefuseAttitudeThreshold = pXML->FindInInfoClass( szTextVal);
	pXML->SetVariableListTagPair(&m_abTraits, "Traits", GC.getNumTraitInfos(), false);
	pXML->SetVariableListTagPair(&m_aiContactRand, "ContactRands", NUM_CONTACT_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiContactDelay, "ContactDelays", NUM_CONTACT_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiMemoryDecayRand, "MemoryDecays", NUM_MEMORY_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiMemoryAttitudePercent, "MemoryAttitudePercents", NUM_MEMORY_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiNoWarAttitudeProb, "NoWarAttitudeProbs", NUM_ATTITUDE_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiUnitAIWeightModifier, "UnitAIWeightModifiers", NUM_UNITAI_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiImprovementWeightModifier, "ImprovementWeightModifiers", GC.getNumImprovementInfos(), 0);
	pXML->SetVariableListTagPairForAudioScripts(&m_aiDiploPeaceMusicScriptIds, "DiplomacyMusicPeace", GC.getNumEraInfos());
	pXML->SetVariableListTagPairForAudioScripts(&m_aiDiploWarMusicScriptIds, "DiplomacyMusicWar", GC.getNumEraInfos());
	return true;
}
//======================================================================================================
//					CvWorldInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvWorldInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvWorldInfo::CvWorldInfo() :
m_iDefaultPlayers(0),
m_iDefaultNativePlayers(0),
m_iUnitNameModifier(0),
m_iTargetNumCities(0),
m_iBuildingClassPrereqModifier(0),
m_iGridWidth(0),
m_iGridHeight(0),
m_iTerrainGrainChange(0),
m_iFeatureGrainChange(0),
m_iFatherPercent(0),
m_iAdvancedStartPointsMod(0)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvWorldInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvWorldInfo::~CvWorldInfo()
{
}
int CvWorldInfo::getDefaultPlayers() const
{
	return m_iDefaultPlayers;
}
int CvWorldInfo::getDefaultNativePlayers() const
{
	return m_iDefaultNativePlayers;
}
int CvWorldInfo::getUnitNameModifier() const
{
	return m_iUnitNameModifier;
}
int CvWorldInfo::getTargetNumCities() const
{
	return m_iTargetNumCities;
}
int CvWorldInfo::getBuildingClassPrereqModifier() const
{
	return m_iBuildingClassPrereqModifier;
}
int CvWorldInfo::getGridWidth() const
{
	return m_iGridWidth;
}
int CvWorldInfo::getGridHeight() const
{
	return m_iGridHeight;
}
int CvWorldInfo::getTerrainGrainChange() const
{
	return m_iTerrainGrainChange;
}
int CvWorldInfo::getFeatureGrainChange() const
{
	return m_iFeatureGrainChange;
}
int CvWorldInfo::getFatherPercent() const
{
	return m_iFatherPercent;
}
int CvWorldInfo::getAdvancedStartPointsMod() const
{
	return m_iAdvancedStartPointsMod;
}
bool CvWorldInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_iDefaultPlayers, "iDefaultPlayers");
	pXML->GetChildXmlValByName(&m_iDefaultNativePlayers, "iDefaultNativePlayers");
	pXML->GetChildXmlValByName(&m_iUnitNameModifier, "iUnitNameModifier");
	pXML->GetChildXmlValByName(&m_iTargetNumCities, "iTargetNumCities");
	pXML->GetChildXmlValByName(&m_iBuildingClassPrereqModifier, "iBuildingClassPrereqModifier");
	pXML->GetChildXmlValByName(&m_iGridWidth, "iGridWidth");
	pXML->GetChildXmlValByName(&m_iGridHeight, "iGridHeight");
	pXML->GetChildXmlValByName(&m_iTerrainGrainChange, "iTerrainGrainChange");
	pXML->GetChildXmlValByName(&m_iFeatureGrainChange, "iFeatureGrainChange");
	pXML->GetChildXmlValByName(&m_iFatherPercent, "iFatherPercent");
	pXML->GetChildXmlValByName(&m_iAdvancedStartPointsMod, "iAdvancedStartPointsMod");
	return true;
}
//======================================================================================================
//					CvClimateInfo
//======================================================================================================
CvClimateInfo::CvClimateInfo() :
m_iDesertPercentChange(0),
m_iJungleLatitude(0),
m_iHillRange(0),
m_iPeakPercent(0),
m_fSnowLatitudeChange(0.0f),
m_fTundraLatitudeChange(0.0f),
m_fGrassLatitudeChange(0.0f),
m_fDesertBottomLatitudeChange(0.0f),
m_fDesertTopLatitudeChange(0.0f),
m_fRandIceLatitude(0.0f)
{
}
CvClimateInfo::~CvClimateInfo()
{
}
int CvClimateInfo::getDesertPercentChange() const
{
	return m_iDesertPercentChange;
}
int CvClimateInfo::getJungleLatitude() const
{
	return m_iJungleLatitude;
}
int CvClimateInfo::getHillRange() const
{
	return m_iHillRange;
}
int CvClimateInfo::getPeakPercent() const
{
	return m_iPeakPercent;
}
float CvClimateInfo::getSnowLatitudeChange() const
{
	return m_fSnowLatitudeChange;
}
float CvClimateInfo::getTundraLatitudeChange() const
{
	return m_fTundraLatitudeChange;
}
float CvClimateInfo::getGrassLatitudeChange() const
{
	return m_fGrassLatitudeChange;
}
float CvClimateInfo::getDesertBottomLatitudeChange() const
{
	return m_fDesertBottomLatitudeChange;
}
float CvClimateInfo::getDesertTopLatitudeChange() const
{
	return m_fDesertTopLatitudeChange;
}
float CvClimateInfo::getRandIceLatitude() const
{
	return m_fRandIceLatitude;
}
bool CvClimateInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_iDesertPercentChange, "iDesertPercentChange");
	pXML->GetChildXmlValByName(&m_iJungleLatitude, "iJungleLatitude");
	pXML->GetChildXmlValByName(&m_iHillRange, "iHillRange");
	pXML->GetChildXmlValByName(&m_iPeakPercent, "iPeakPercent");
	pXML->GetChildXmlValByName(&m_fSnowLatitudeChange, "fSnowLatitudeChange");
	pXML->GetChildXmlValByName(&m_fTundraLatitudeChange, "fTundraLatitudeChange");
	pXML->GetChildXmlValByName(&m_fGrassLatitudeChange, "fGrassLatitudeChange");
	pXML->GetChildXmlValByName(&m_fDesertBottomLatitudeChange, "fDesertBottomLatitudeChange");
	pXML->GetChildXmlValByName(&m_fDesertTopLatitudeChange, "fDesertTopLatitudeChange");
	pXML->GetChildXmlValByName(&m_fRandIceLatitude, "fRandIceLatitude");
	return true;
}
//======================================================================================================
//					CvSeaLevelInfo
//======================================================================================================
CvSeaLevelInfo::CvSeaLevelInfo() :
m_iSeaLevelChange(0)
{
}
CvSeaLevelInfo::~CvSeaLevelInfo()
{
}
int CvSeaLevelInfo::getSeaLevelChange() const
{
	return m_iSeaLevelChange;
}
bool CvSeaLevelInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_iSeaLevelChange, "iSeaLevelChange");
	return true;
}

//======================================================================================================
//					CvEuropeInfo
//======================================================================================================
CvEuropeInfo::CvEuropeInfo() :
	m_bStart(false),
	m_iCardinalDirection(NO_CARDINALDIRECTION),
	m_iTripLength(0),
	m_iMinLandDistance(0),
	m_iWidthPercent(0)
{
}
CvEuropeInfo::~CvEuropeInfo()
{
}
bool CvEuropeInfo::isStart() const
{
	return m_bStart;
}
int CvEuropeInfo::getTripLength() const
{
	return m_iTripLength;
}
int CvEuropeInfo::getCardinalDirection() const
{
	return m_iCardinalDirection;
}
int CvEuropeInfo::getMinLandDistance() const
{
	return m_iMinLandDistance;
}
int CvEuropeInfo::getWidthPercent() const
{
	return m_iWidthPercent;
}
bool CvEuropeInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}

	CvString szVal;
	pXML->GetChildXmlValByName(szVal, "Direction");
	bool bFound = false;
	for(int iDirection=0; iDirection < NUM_CARDINALDIRECTION_TYPES; ++iDirection)
	{
		CvWString szDirectionString;
		getCardinalDirectionTypeString(szDirectionString, (CardinalDirectionTypes) iDirection);
		if (szDirectionString == CvWString(szVal))
		{
			m_iCardinalDirection = iDirection;
			bFound = true;
			break;
		}
	}
	if (!bFound)
	{
		FAssertMsg(false, "Could not match direction string.");
		m_iCardinalDirection = CARDINALDIRECTION_EAST;
	}

	pXML->GetChildXmlValByName(&m_bStart, "bStart");
	pXML->GetChildXmlValByName(&m_iTripLength, "iTripLength");
	pXML->GetChildXmlValByName(&m_iMinLandDistance, "iMinLandDistance");
	pXML->GetChildXmlValByName(&m_iWidthPercent, "iWidthPercent");

	return true;
}

//======================================================================================================
//					CvTraitInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvTraitInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvTraitInfo::CvTraitInfo() :
	m_iLevelExperienceModifier(0),
	m_iGreatGeneralRateModifier(0),
	m_iDomesticGreatGeneralRateModifier(0),
	m_iNativeAngerModifier(0),
	m_iLearnTimeModifier(0),
	m_iNativeCombatModifier(0),
	m_iMissionaryModifier(0),
	m_iRebelCombatModifier(0),
	m_iTaxRateThresholdModifier(0),
	m_iMercantileFactor(0),
	m_iTreasureModifier(0),
	m_iChiefGoldModifier(0),
	m_iNativeAttitudeChange(0),
	m_iCityDefense(0),
	m_iLandPriceDiscount(0),
	m_iRecruitPriceDiscount(0),
	m_iEuropeTravelTimeModifier(0),
	m_iImmigrationThresholdModifier(0),
	m_aiYieldModifier(NULL),
	m_aiGoodyFactor(NULL),
	m_aiBuildingProductionModifier(NULL),
	m_aiBuildingRequiredYieldModifier(NULL),
	m_aiUnitMoveChange(NULL),
	m_aiUnitStrengthModifier(NULL),
	m_aiProfessionMoveChange(NULL),
	m_aiCityExtraYields(NULL),
	m_aiExtraYieldThreshold(NULL),
	m_aiProfessionEquipmentModifier(NULL),
	m_abTaxYieldModifier(NULL),
	m_abFreePromotionUnitCombat(NULL),
	m_abFreePromotion(NULL),
	m_abFreeBuildingClass(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvTraitInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvTraitInfo::~CvTraitInfo()
{
	SAFE_DELETE_ARRAY(m_aiCityExtraYields);
	SAFE_DELETE_ARRAY(m_aiExtraYieldThreshold);
	SAFE_DELETE_ARRAY(m_aiProfessionEquipmentModifier);
	SAFE_DELETE_ARRAY(m_aiYieldModifier);
	SAFE_DELETE_ARRAY(m_aiGoodyFactor);
	SAFE_DELETE_ARRAY(m_aiBuildingProductionModifier);
	SAFE_DELETE_ARRAY(m_aiBuildingRequiredYieldModifier);
	SAFE_DELETE_ARRAY(m_aiUnitMoveChange);
	SAFE_DELETE_ARRAY(m_aiUnitStrengthModifier);
	SAFE_DELETE_ARRAY(m_aiProfessionMoveChange);
	SAFE_DELETE_ARRAY(m_abFreePromotionUnitCombat);
	SAFE_DELETE_ARRAY(m_abFreePromotion);
	SAFE_DELETE_ARRAY(m_abFreeBuildingClass);
	SAFE_DELETE_ARRAY(m_abTaxYieldModifier);

	for (uint iBuildingClass = 0; iBuildingClass < m_aaiBuildingYieldChanges.size(); ++iBuildingClass)
	{
		SAFE_DELETE_ARRAY(m_aaiBuildingYieldChanges[iBuildingClass]);
	}
}
int CvTraitInfo::getLevelExperienceModifier() const
{
	return m_iLevelExperienceModifier;
}
int CvTraitInfo::getGreatGeneralRateModifier() const
{
	return m_iGreatGeneralRateModifier;
}
int CvTraitInfo::getDomesticGreatGeneralRateModifier() const
{
	return m_iDomesticGreatGeneralRateModifier;
}
int CvTraitInfo::getNativeAngerModifier() const
{
	return m_iNativeAngerModifier;
}
int CvTraitInfo::getLearnTimeModifier() const
{
	return m_iLearnTimeModifier;
}
int CvTraitInfo::getMercantileFactor() const
{
	return m_iMercantileFactor;
}
int CvTraitInfo::getTreasureModifier() const
{
	return m_iTreasureModifier;
}
int CvTraitInfo::getChiefGoldModifier() const
{
	return m_iChiefGoldModifier;
}
int CvTraitInfo::getNativeCombatModifier() const
{
	return m_iNativeCombatModifier;
}
int CvTraitInfo::getMissionaryModifier() const
{
	return m_iMissionaryModifier;
}
int CvTraitInfo::getRebelCombatModifier() const
{
	return m_iRebelCombatModifier;
}
int CvTraitInfo::getTaxRateThresholdModifier() const
{
	return m_iTaxRateThresholdModifier;
}
int CvTraitInfo::getNativeAttitudeChange() const
{
	return m_iNativeAttitudeChange;
}

int CvTraitInfo::getCityDefense() const
{
	return m_iCityDefense;
}

int CvTraitInfo::getLandPriceDiscount() const
{
	return m_iLandPriceDiscount;
}

int CvTraitInfo::getRecruitPriceDiscount() const
{
	return m_iRecruitPriceDiscount;
}

int CvTraitInfo::getEuropeTravelTimeModifier() const
{
	return m_iEuropeTravelTimeModifier;
}

int CvTraitInfo::getImmigrationThresholdModifier() const
{
	return m_iImmigrationThresholdModifier;
}

int CvTraitInfo::getYieldModifier(int i) const
{
	FAssert(i < NUM_YIELD_TYPES);
	FAssert(i >= 0);
	return m_aiYieldModifier ? m_aiYieldModifier[i] : -1;
}

int CvTraitInfo::getGoodyFactor(int i) const
{
	FAssert((i >= 0) && (i < GC.getNumGoodyInfos()));
	return m_aiGoodyFactor ? m_aiGoodyFactor[i] : -1;
}

int CvTraitInfo::getBuildingProductionModifier(int i) const
{
	FAssert((i >= 0) && (i < GC.getNumBuildingClassInfos()));
	return m_aiBuildingProductionModifier ? m_aiBuildingProductionModifier[i] : -1;
}

int CvTraitInfo::getBuildingRequiredYieldModifier(int i) const
{
	FAssert((i >= 0) && (i < NUM_YIELD_TYPES));
	return m_aiBuildingRequiredYieldModifier ? m_aiBuildingRequiredYieldModifier[i] : -1;
}

const int* CvTraitInfo::getBuildingRequiredYieldModifierArray() const
{
	return m_aiBuildingRequiredYieldModifier;
}

int CvTraitInfo::getUnitMoveChange(int i) const
{
	FAssert(i < GC.getNumUnitClassInfos());
	FAssert(i >= 0);
	return m_aiUnitMoveChange ? m_aiUnitMoveChange[i] : -1;
}

int CvTraitInfo::getUnitStrengthModifier(int i) const
{
	FAssert(i < GC.getNumUnitClassInfos());
	FAssert(i >= 0);
	return m_aiUnitStrengthModifier ? m_aiUnitStrengthModifier[i] : -1;
}

int CvTraitInfo::getProfessionMoveChange(int i) const
{
	FAssert(i < GC.getNumProfessionInfos());
	FAssert(i >= 0);
	return m_aiProfessionMoveChange ? m_aiProfessionMoveChange[i] : -1;
}

bool CvTraitInfo::isTaxYieldModifier(int i) const
{
	FAssert(i < NUM_YIELD_TYPES);
	FAssert(i > -1);
	return m_abTaxYieldModifier ? m_abTaxYieldModifier[i] : false;
}

int CvTraitInfo::getBuildingYieldChange(int iBuildingClass, int iYieldType) const
{
	FAssert(iBuildingClass >= 0);
	FAssert(iBuildingClass < GC.getNumBuildingClassInfos());
	FAssert(iYieldType >= 0);
	FAssert(iYieldType < NUM_YIELD_TYPES);

	return m_aaiBuildingYieldChanges[iBuildingClass][iYieldType];
}

const char* CvTraitInfo::getShortDescription() const
{
	return m_szShortDescription;
}
void CvTraitInfo::setShortDescription(const char* szVal)
{
	m_szShortDescription = szVal;
}
// Arrays
int CvTraitInfo::getCityExtraYield(int i) const
{
	return m_aiCityExtraYields ? m_aiCityExtraYields[i] : -1;
}
int CvTraitInfo::getExtraYieldThreshold(int i) const
{
	return m_aiExtraYieldThreshold ? m_aiExtraYieldThreshold[i] : -1;
}
int CvTraitInfo::getProfessionEquipmentModifier(int i) const
{
	return m_aiProfessionEquipmentModifier ? m_aiProfessionEquipmentModifier[i] : -1;
}
int CvTraitInfo::isFreePromotion(int i) const
{
	return m_abFreePromotion ? m_abFreePromotion[i] : -1;
}
int CvTraitInfo::isFreePromotionUnitCombat(int i) const
{
	return m_abFreePromotionUnitCombat ? m_abFreePromotionUnitCombat[i] : -1;
}
bool CvTraitInfo::isFreeBuildingClass(int i) const
{
	return m_abFreeBuildingClass ? m_abFreeBuildingClass[i] : -1;
}
void CvTraitInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);

	uint uiFlag=0;
	stream->Read(&uiFlag);	// flags for expansion

	stream->Read(&m_iLevelExperienceModifier);
	stream->Read(&m_iGreatGeneralRateModifier);
	stream->Read(&m_iDomesticGreatGeneralRateModifier);
	stream->Read(&m_iNativeAngerModifier);
	stream->Read(&m_iLearnTimeModifier);
	stream->Read(&m_iNativeCombatModifier);
	stream->Read(&m_iMissionaryModifier);
	stream->Read(&m_iRebelCombatModifier);
	stream->Read(&m_iTaxRateThresholdModifier);
	stream->Read(&m_iMercantileFactor);
	stream->Read(&m_iTreasureModifier);
	stream->Read(&m_iChiefGoldModifier);
	stream->Read(&m_iNativeAttitudeChange);
	stream->Read(&m_iCityDefense);
	stream->Read(&m_iLandPriceDiscount);
	stream->Read(&m_iRecruitPriceDiscount);
	stream->Read(&m_iEuropeTravelTimeModifier);
	stream->Read(&m_iImmigrationThresholdModifier);
	stream->ReadString(m_szShortDescription);

	SAFE_DELETE_ARRAY(m_aiCityExtraYields);
	m_aiCityExtraYields = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiCityExtraYields);

	SAFE_DELETE_ARRAY(m_aiExtraYieldThreshold);
	m_aiExtraYieldThreshold = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiExtraYieldThreshold);

	SAFE_DELETE_ARRAY(m_aiProfessionEquipmentModifier);
	m_aiProfessionEquipmentModifier = new int[GC.getNumProfessionInfos()];
	stream->Read(GC.getNumProfessionInfos(), m_aiProfessionEquipmentModifier);

	SAFE_DELETE_ARRAY(m_aiYieldModifier);
	m_aiYieldModifier = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiYieldModifier);

	SAFE_DELETE_ARRAY(m_aiGoodyFactor);
	m_aiGoodyFactor = new int[GC.getNumGoodyInfos()];
	stream->Read(GC.getNumGoodyInfos(), m_aiGoodyFactor);

	SAFE_DELETE_ARRAY(m_aiBuildingProductionModifier);
	m_aiBuildingProductionModifier = new int[GC.getNumBuildingClassInfos()];
	stream->Read(GC.getNumBuildingClassInfos(), m_aiBuildingProductionModifier);

	SAFE_DELETE_ARRAY(m_aiBuildingRequiredYieldModifier);
	m_aiBuildingRequiredYieldModifier = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiBuildingRequiredYieldModifier);

	SAFE_DELETE_ARRAY(m_aiUnitMoveChange);
	m_aiUnitMoveChange = new int[GC.getNumUnitClassInfos()];
	stream->Read(GC.getNumUnitClassInfos(), m_aiUnitMoveChange);

	SAFE_DELETE_ARRAY(m_aiUnitStrengthModifier);
	m_aiUnitStrengthModifier = new int[GC.getNumUnitClassInfos()];
	stream->Read(GC.getNumUnitClassInfos(), m_aiUnitStrengthModifier);

	SAFE_DELETE_ARRAY(m_aiProfessionMoveChange);
	m_aiProfessionMoveChange = new int[GC.getNumProfessionInfos()];
	stream->Read(GC.getNumProfessionInfos(), m_aiProfessionMoveChange);

	SAFE_DELETE_ARRAY(m_abTaxYieldModifier);
	m_abTaxYieldModifier = new bool[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_abTaxYieldModifier);

	SAFE_DELETE_ARRAY(m_abFreePromotion);
	m_abFreePromotion = new bool[GC.getNumPromotionInfos()];
	stream->Read(GC.getNumPromotionInfos(), m_abFreePromotion);

	SAFE_DELETE_ARRAY(m_abFreePromotionUnitCombat);
	m_abFreePromotionUnitCombat = new bool[GC.getNumUnitCombatInfos()];
	stream->Read(GC.getNumUnitCombatInfos(), m_abFreePromotionUnitCombat);

	SAFE_DELETE_ARRAY(m_abFreeBuildingClass);
	m_abFreeBuildingClass = new bool[GC.getNumBuildingClassInfos()];
	stream->Read(GC.getNumBuildingClassInfos(), m_abFreeBuildingClass);

	for (uint iBuildingClass = 0; iBuildingClass < m_aaiBuildingYieldChanges.size(); ++iBuildingClass)
	{
		SAFE_DELETE_ARRAY(m_aaiBuildingYieldChanges[iBuildingClass]);
	}
	m_aaiBuildingYieldChanges.clear();

	for (int i=0; i< GC.getNumBuildingClassInfos(); i++)
	{
		m_aaiBuildingYieldChanges.push_back(new int[NUM_YIELD_TYPES]);
		stream->Read(NUM_YIELD_TYPES, m_aaiBuildingYieldChanges[i]);
	}
}

void CvTraitInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);

	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion

	stream->Write(m_iLevelExperienceModifier);
	stream->Write(m_iGreatGeneralRateModifier);
	stream->Write(m_iDomesticGreatGeneralRateModifier);
	stream->Write(m_iNativeAngerModifier);
	stream->Write(m_iLearnTimeModifier);
	stream->Write(m_iNativeCombatModifier);
	stream->Write(m_iMissionaryModifier);
	stream->Write(m_iRebelCombatModifier);
	stream->Write(m_iTaxRateThresholdModifier);
	stream->Write(m_iMercantileFactor);
	stream->Write(m_iTreasureModifier);
	stream->Write(m_iChiefGoldModifier);
	stream->Write(m_iNativeAttitudeChange);
	stream->Write(m_iCityDefense);
	stream->Write(m_iLandPriceDiscount);
	stream->Write(m_iRecruitPriceDiscount);
	stream->Write(m_iEuropeTravelTimeModifier);
	stream->Write(m_iImmigrationThresholdModifier);
	stream->WriteString(m_szShortDescription);
	stream->Write(NUM_YIELD_TYPES, m_aiCityExtraYields);
	stream->Write(NUM_YIELD_TYPES, m_aiExtraYieldThreshold);
	stream->Write(GC.getNumProfessionInfos(), m_aiProfessionEquipmentModifier);
	stream->Write(NUM_YIELD_TYPES, m_aiYieldModifier);
	stream->Write(GC.getNumGoodyInfos(), m_aiGoodyFactor);
	stream->Write(GC.getNumBuildingClassInfos(), m_aiBuildingProductionModifier);
	stream->Write(NUM_YIELD_TYPES, m_aiBuildingRequiredYieldModifier);
	stream->Write(GC.getNumUnitClassInfos(), m_aiUnitMoveChange);
	stream->Write(GC.getNumUnitClassInfos(), m_aiUnitStrengthModifier);
	stream->Write(GC.getNumProfessionInfos(), m_aiProfessionMoveChange);
	stream->Write(NUM_YIELD_TYPES, m_abTaxYieldModifier);
	stream->Write(GC.getNumPromotionInfos(), m_abFreePromotion);
	stream->Write(GC.getNumUnitCombatInfos(), m_abFreePromotionUnitCombat);
	stream->Write(GC.getNumBuildingClassInfos(), m_abFreeBuildingClass);

	for (int i=0; i < GC.getNumBuildingClassInfos(); i++)
	{
		stream->Write(NUM_YIELD_TYPES, m_aaiBuildingYieldChanges[i]);
	}
}

bool CvTraitInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "ShortDescription");
	setShortDescription(szTextVal);

	pXML->GetChildXmlValByName(&m_iLevelExperienceModifier, "iLevelExperienceModifier");
	pXML->GetChildXmlValByName(&m_iGreatGeneralRateModifier, "iGreatGeneralRateModifier");
	pXML->GetChildXmlValByName(&m_iDomesticGreatGeneralRateModifier, "iDomesticGreatGeneralRateModifier");
	pXML->GetChildXmlValByName(&m_iNativeAngerModifier, "iNativeAngerModifier");
	pXML->GetChildXmlValByName(&m_iLearnTimeModifier, "iLearnTimeModifier");
	pXML->GetChildXmlValByName(&m_iNativeCombatModifier, "iNativeCombatModifier");
	pXML->GetChildXmlValByName(&m_iMissionaryModifier, "iMissionaryModifier");
	pXML->GetChildXmlValByName(&m_iRebelCombatModifier, "iRebelCombatModifier");
	pXML->GetChildXmlValByName(&m_iTaxRateThresholdModifier, "iTaxRateThresholdModifier");
	pXML->GetChildXmlValByName(&m_iMercantileFactor, "iMercantileFactor");
	pXML->GetChildXmlValByName(&m_iTreasureModifier, "iTreasureModifier");
	pXML->GetChildXmlValByName(&m_iChiefGoldModifier, "iChiefGoldModifier");
	pXML->GetChildXmlValByName(&m_iNativeAttitudeChange, "iNativeAttitudeChange");
	pXML->GetChildXmlValByName(&m_iCityDefense, "iCityDefense");
	pXML->GetChildXmlValByName(&m_iLandPriceDiscount, "iLandPriceDiscount");
	pXML->GetChildXmlValByName(&m_iRecruitPriceDiscount, "iRecruitPriceDiscount");
	pXML->GetChildXmlValByName(&m_iEuropeTravelTimeModifier, "iEuropeTravelTimeModifier");
	pXML->GetChildXmlValByName(&m_iImmigrationThresholdModifier, "iImmigrationThresholdModifier");

	pXML->SetVariableListTagPair(&m_aiGoodyFactor, "GoodyFactors", GC.getNumGoodyInfos(), 1);
	pXML->SetVariableListTagPair(&m_aiBuildingProductionModifier, "BuildingProductionModifiers", GC.getNumBuildingClassInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiBuildingRequiredYieldModifier, "BuildingRequiredYieldModifiers", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiYieldModifier, "YieldModifiers", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiUnitMoveChange, "UnitMoveChanges", GC.getNumUnitClassInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiUnitStrengthModifier, "UnitStrengthModifiers", GC.getNumUnitClassInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiProfessionMoveChange, "ProfessionMoveChanges", GC.getNumProfessionInfos(), 0);
	pXML->SetVariableListTagPair(&m_abTaxYieldModifier, "TaxYieldModifiers", NUM_YIELD_TYPES, false);

	pXML->Init2DIntList(m_aaiBuildingYieldChanges, GC.getNumBuildingClassInfos(), NUM_YIELD_TYPES);
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"BuildingYieldChanges"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
			{
				if (0 < iNumSibs)
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						pXML->GetChildXmlValByName(szTextVal, "BuildingClassType");
						int iIndex = pXML->FindInInfoClass(szTextVal);
						if (iIndex > -1)
						{
							// delete the array since it will be reallocated
							SAFE_DELETE_ARRAY(m_aaiBuildingYieldChanges[iIndex]);
							pXML->SetVariableListTagPair(&m_aaiBuildingYieldChanges[iIndex], "BuildingYields", NUM_YIELD_TYPES, 0);
						}
						if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
						{
							break;
						}
					}
				}
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}


	pXML->SetVariableListTagPair(&m_aiCityExtraYields, "CityExtraYields", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiExtraYieldThreshold, "ExtraYieldThresholds", NUM_YIELD_TYPES, 0);
	pXML->SetVariableListTagPair(&m_aiProfessionEquipmentModifier, "ProfessionEquipmentModifiers", GC.getNumProfessionInfos(), 0);
	pXML->SetVariableListTagPair(&m_abFreePromotion, "FreePromotions", GC.getNumPromotionInfos(), false);
	pXML->SetVariableListTagPair(&m_abFreePromotionUnitCombat, "FreePromotionUnitCombats", GC.getNumUnitCombatInfos(), false);
	pXML->SetVariableListTagPair(&m_abFreeBuildingClass, "FreeBuildingClasses", GC.getNumBuildingClassInfos(), false);
	return true;
}

//======================================================================================================
//					CvCursorInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvCursorInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvCursorInfo::CvCursorInfo()
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvCursorInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvCursorInfo::~CvCursorInfo()
{
}
const char* CvCursorInfo::getPath()
{
	return m_szPath;
}
void CvCursorInfo::setPath(const char* szVal)
{
	m_szPath = szVal;
}
bool CvCursorInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "CursorPath");
	setPath(szTextVal);
	return true;
}
//======================================================================================================
//					CvSlideShowInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvSlideShowInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvSlideShowInfo::CvSlideShowInfo() :
m_fStartTime(0.0f)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvSlideShowInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvSlideShowInfo::~CvSlideShowInfo()
{
}
const char* CvSlideShowInfo::getPath()
{
	return m_szPath;
}
void CvSlideShowInfo::setPath(const char* szVal)
{
	m_szPath = szVal;
}
const char* CvSlideShowInfo::getTransitionType()
{
	return m_szTransitionType;
}
void CvSlideShowInfo::setTransitionType(const char* szVal)
{
	m_szTransitionType = szVal;
}
float CvSlideShowInfo::getStartTime()
{
	return m_fStartTime;
}
void CvSlideShowInfo::setStartTime(float fVal)
{
	m_fStartTime = fVal;
}
bool CvSlideShowInfo::read(CvXMLLoadUtility* pXML)
{
	float fVal;
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "Path");
	setPath(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "TransitionType");
	setTransitionType(szTextVal);
	pXML->GetChildXmlValByName(&fVal, "fStartTime");
	setStartTime(fVal);
	return true;
}
//======================================================================================================
//					CvSlideShowRandomInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvSlideShowRandomInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvSlideShowRandomInfo::CvSlideShowRandomInfo()
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvSlideShowRandomInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvSlideShowRandomInfo::~CvSlideShowRandomInfo()
{
}
const char* CvSlideShowRandomInfo::getPath()
{
	return m_szPath;
}
void CvSlideShowRandomInfo::setPath(const char* szVal)
{
	m_szPath = szVal;
}
bool CvSlideShowRandomInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "Path");
	setPath(szTextVal);
	return true;
}
//======================================================================================================
//					CvWorldPickerInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvWorldPickerInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvWorldPickerInfo::CvWorldPickerInfo()
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvWorldPickerInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvWorldPickerInfo::~CvWorldPickerInfo()
{
}
const char* CvWorldPickerInfo::getMapName()
{
	return m_szMapName;
}
void CvWorldPickerInfo::setMapName(const char* szVal)
{
	m_szMapName = szVal;
}
const char* CvWorldPickerInfo::getModelFile()
{
	return m_szModelFile;
}
void CvWorldPickerInfo::setModelFile(const char* szVal)
{
	m_szModelFile = szVal;
}
int CvWorldPickerInfo::getNumSizes()
{
	return m_aSizes.size();
}
float CvWorldPickerInfo::getSize(int index)
{
	return m_aSizes[index];
}
int CvWorldPickerInfo::getNumClimates()
{
	return m_aClimates.size();
}
const char* CvWorldPickerInfo::getClimatePath(int index)
{
	return m_aClimates[index];
}
int CvWorldPickerInfo::getNumWaterLevelDecals()
{
	return m_aWaterLevelDecals.size();
}
const char* CvWorldPickerInfo::getWaterLevelDecalPath(int index)
{
	return m_aWaterLevelDecals[index];
}
int CvWorldPickerInfo::getNumWaterLevelGloss()
{
	return m_aWaterLevelGloss.size();
}
const char* CvWorldPickerInfo::getWaterLevelGlossPath(int index)
{
	return m_aWaterLevelGloss[index];
}
bool CvWorldPickerInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	float fVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "MapName");
	setMapName(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "ModelFile");
	setModelFile(szTextVal);
	//sizes
	if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "Sizes"))
	{
		if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "Size"))
		{
			do
			{
				pXML->GetXmlVal(&fVal);
				m_aSizes.push_back(fVal);
			} while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "Size"));
			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	//climates
	if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "Climates"))
	{
		if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "ClimatePath"))
		{
			do
			{
				pXML->GetXmlVal(szTextVal);
				m_aClimates.push_back(szTextVal);
			} while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "ClimatePath"));
			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	//water level decals
	if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "WaterLevelDecals"))
	{
		if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "WaterLevelDecalPath"))
		{
			do
			{
				pXML->GetXmlVal(szTextVal);
				m_aWaterLevelDecals.push_back(szTextVal);
			} while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "WaterLevelDecalPath"));
			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	//water level gloss
	if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "WaterLevelGloss"))
	{
		if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "WaterLevelGlossPath"))
		{
			do
			{
				pXML->GetXmlVal(szTextVal);
				m_aWaterLevelGloss.push_back(szTextVal);
			} while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "WaterLevelGlossPath"));
			gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	return true;
}
//======================================================================================================
//					CvAnimationPathInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvAnimationPathInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvAnimationPathInfo::CvAnimationPathInfo() :
	m_bMissionPath(false)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvAnimationPathInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvAnimationPathInfo::~CvAnimationPathInfo()
{
}
int CvAnimationPathInfo::getPathCategory( int i )
{
	return (int)m_vctPathDefinition.size() > i ? m_vctPathDefinition[i].first : -1;
}
float CvAnimationPathInfo::getPathParameter( int i )
{
	return (int)m_vctPathDefinition.size() > i ? m_vctPathDefinition[i].second : -1;
}
int CvAnimationPathInfo::getNumPathDefinitions()
{
	return m_vctPathDefinition.size();
}
CvAnimationPathDefinition * CvAnimationPathInfo::getPath( )
{
	return &m_vctPathDefinition;
}
bool CvAnimationPathInfo::isMissionPath() const
{
	return m_bMissionPath;
}
//------------------------------------------------------------------------------------------------
// FUNCTION:    CvAnimationPathInfo::read
//! \brief      Reads in a CvAnimationPathInfo definition from XML
//! \param      pXML Pointer to the XML loading object
//! \retval     true if the definition was read successfully, false otherwise
//------------------------------------------------------------------------------------------------
bool CvAnimationPathInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	char	szTempString[1024];				// Extracting text
	int		iCurrentCategory;				// The current category information we are building
	float	fParameter;						// Temporary
	pXML->GetChildXmlValByName( &m_bMissionPath, "bMissionPath" );
	gDLL->getXMLIFace()->SetToChild(pXML->GetXML() );
	gDLL->getXMLIFace()->GetLastNodeText(pXML->GetXML(), szTempString);
	gDLL->getXMLIFace()->NextSibling(pXML->GetXML());
	gDLL->getXMLIFace()->NextSibling(pXML->GetXML());
	do
	{
		if ( pXML->GetChildXmlValByName( szTempString, _T("Category") ))
		{
			iCurrentCategory = pXML->FindInInfoClass( szTempString);
			fParameter = 0.0f;
		}
		else
		{
			pXML->GetChildXmlValByName( szTempString, _T("Operator"));
			iCurrentCategory = GC.getInfoTypeForString(szTempString);
			iCurrentCategory = ((int)ANIMOP_FIRST) + iCurrentCategory;
			if ( !pXML->GetChildXmlValByName( &fParameter, "Parameter" ) )
			{
				fParameter = 0.0f;
			}
		}
			m_vctPathDefinition.push_back( std::make_pair(iCurrentCategory, fParameter ));
	}
	while ( gDLL->getXMLIFace()->NextSibling(pXML->GetXML()));
	gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	return true;
}
//======================================================================================================
//					CvAnimationCategoryInfo
//======================================================================================================
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvAnimationCategoryInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvAnimationCategoryInfo::CvAnimationCategoryInfo()
{
	m_kCategory.second = -7540; // invalid.
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvAnimationCategoryInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvAnimationCategoryInfo::~CvAnimationCategoryInfo()
{
}
int CvAnimationCategoryInfo::getCategoryBaseID( )
{
	return m_kCategory.first;
}
int CvAnimationCategoryInfo::getCategoryDefaultTo( )
{
	if ( m_kCategory.second < -1 )
	{
		// CvXMLLoadUtility *pXML = new CvXMLLoadUtility();
		m_kCategory.second = CvXMLLoadUtility::FindInInfoClass( m_szDefaultTo);
	}
	return (int)m_kCategory.second;
}
bool CvAnimationCategoryInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	int		iBaseID;						// Temporary
	pXML->GetChildXmlValByName( m_szDefaultTo, "DefaultTo");
	pXML->GetChildXmlValByName( &iBaseID, "BaseID");
	m_kCategory.first = iBaseID;
	return true;
}
/////////////////////////////////////////////////////////////////////////////////////////////
// CvEntityEventInfo
/////////////////////////////////////////////////////////////////////////////////////////////
CvEntityEventInfo::CvEntityEventInfo() :
m_bUpdateFormation(true)
{
}
CvEntityEventInfo::~CvEntityEventInfo()
{
}
bool CvEntityEventInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTmp, szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	int iNumSibs, i;
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"AnimationPathTypes"))
	{
		// Skip any comments and stop at the next value we might want
		if (pXML->SkipToNextVal())
		{
			// get the total number of children the current xml node has
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (iNumSibs > 0)
			{
				// if the call to the function that sets the current xml node to it's first non-comment
				// child and sets the parameter with the new node's value succeeds
				if (pXML->GetChildXmlVal(szTmp))
				{
					AnimationPathTypes eAnimationPath = (AnimationPathTypes)CvXMLLoadUtility::FindInInfoClass( szTmp);
					if ( eAnimationPath > ANIMATIONPATH_NONE )
						m_vctAnimationPathType.push_back( eAnimationPath );
					// loop through all the siblings, we start at 1 since we already have the first value
					for (i=1;i<iNumSibs;i++)
					{
						if (!pXML->GetNextXmlVal(&szTmp))
						{
							break;
						}
						AnimationPathTypes eAnimationPath = (AnimationPathTypes)CvXMLLoadUtility::FindInInfoClass( szTmp);
						if ( eAnimationPath > ANIMATIONPATH_NONE )
							m_vctAnimationPathType.push_back( eAnimationPath );
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"EffectTypes"))
	{
		// Skip any comments and stop at the next value we might want
		if (pXML->SkipToNextVal())
		{
			// get the total number of children the current xml node has
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (iNumSibs > 0)
			{
				// if the call to the function that sets the current xml node to it's first non-comment
				// child and sets the parameter with the new node's value succeeds
				if (pXML->GetChildXmlVal(szTmp))
				{
					EffectTypes eEffectType = (EffectTypes)CvXMLLoadUtility::FindInInfoClass( szTmp);
					if ( eEffectType > NO_EFFECT )
						m_vctEffectTypes.push_back( eEffectType );
					// loop through all the siblings, we start at 1 since we already have the first value
					for (i=1;i<iNumSibs;i++)
					{
						if (!pXML->GetNextXmlVal(&szTmp))
						{
							break;
						}
						EffectTypes eEffectType = (EffectTypes)CvXMLLoadUtility::FindInInfoClass( szTmp);
						if ( eEffectType > NO_EFFECT )
							m_vctEffectTypes.push_back( eEffectType );
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	pXML->GetChildXmlValByName( &m_bUpdateFormation, "bUpdateFormation" );
	return true;
}
AnimationPathTypes CvEntityEventInfo::getAnimationPathType(int iIndex) const
{
	return iIndex >= (int)m_vctAnimationPathType.size() ? ANIMATIONPATH_NONE : m_vctAnimationPathType[iIndex];
}
EffectTypes CvEntityEventInfo::getEffectType(int iIndex) const
{
	return iIndex >= (int)m_vctEffectTypes.size() ? NO_EFFECT : m_vctEffectTypes[iIndex];
}
int CvEntityEventInfo::getAnimationPathCount() const
{
	return m_vctAnimationPathType.size();
}
int CvEntityEventInfo::getEffectTypeCount() const
{
	return m_vctEffectTypes.size();
}
bool CvEntityEventInfo::getUpdateFormation() const
{
	return m_bUpdateFormation;
}
/////////////////////////////////////////////////////////////////////////////////////////////
// CvAssetInfoBase
/////////////////////////////////////////////////////////////////////////////////////////////
const char* CvAssetInfoBase::getTag() const
{
	return getType();
}
void CvAssetInfoBase::setTag(const char* szDesc)
{
	m_szType = szDesc;
}
const char* CvAssetInfoBase::getPath() const
{
	return m_szPath;
}
void CvAssetInfoBase::setPath(const char* szDesc)
{
	m_szPath = szDesc;
}
bool CvAssetInfoBase::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))		// 'tag' is the same as 'type'
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "Path");
	setPath(szTextVal);
	return true;
}
/////////////////////////////////////////////////////////////////////////////////////////////
// CvArtInfoAsset
/////////////////////////////////////////////////////////////////////////////////////////////
const char* CvArtInfoAsset::getNIF() const
{
	return m_szNIF;
}
const char* CvArtInfoAsset::getKFM() const
{
	return m_szKFM;
}
void CvArtInfoAsset::setNIF(const char* szDesc)
{
	m_szNIF = szDesc;
}
void CvArtInfoAsset::setKFM(const char* szDesc)
{
	m_szKFM = szDesc;
}
bool CvArtInfoAsset::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvAssetInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "NIF");
	setNIF(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "KFM");
	setKFM(szTextVal);

	return true;
}
/////////////////////////////////////////////////////////////////////////////////////////////
// CvArtInfoBonus
/////////////////////////////////////////////////////////////////////////////////////////////
bool CvArtInfoBonus::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoScalableAsset::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_iFontButtonIndex, "FontButtonIndex");
	pXML->GetChildXmlValByName(&m_bShadowCastor, "bShadowCastor");
	pXML->GetChildXmlValByName(&m_bRefractionCastor, "bRefractionCastor");
	return true;
}
CvArtInfoBonus::CvArtInfoBonus()
{
	m_iFontButtonIndex = 0;
	m_bShadowCastor = false;
	m_bRefractionCastor = false;
}
int CvArtInfoBonus::getFontButtonIndex() const
{
	return m_iFontButtonIndex;
}
bool CvArtInfoBonus::isShadowCastor() const
{
	return m_bShadowCastor;
}
bool CvArtInfoBonus::isRefractionCastor() const
{
	return m_bRefractionCastor;
}
const CvArtInfoBonus* CvBonusInfo::getArtInfo() const
{
	return ARTFILEMGR.getBonusArtInfo( getArtDefineTag());
}

/////////////////////////////////////////////////////////////////////////////////////////////
// CvArtInfoUnit
/////////////////////////////////////////////////////////////////////////////////////////////
CvArtInfoUnit::CvArtInfoUnit() :
m_iDamageStates(0),
m_bActAsRanged(false),
m_bCombatExempt(false),
m_fTrailWidth(0.0f),
m_fTrailLength(0.0f),
m_fTrailTaper(0.0f),
m_fTrailFadeStartTime(0.0f),
m_fTrailFadeFalloff(0.0f),
m_fRangedDeathTime(0.0f),
m_fExchangeAngle(0.0f),
m_bSmoothMove(false),
m_fAngleInterRate(FLT_MAX),
m_fBankRate(0),
m_iRunLoopSoundTag(0),
m_iRunEndSoundTag(0),
m_iSelectionSoundScriptId(0),
m_iActionSoundScriptId(0)
{
}
CvArtInfoUnit::~CvArtInfoUnit()
{
}
bool CvArtInfoUnit::getActAsRanged() const
{
	return m_bActAsRanged;
}
const char* CvArtInfoUnit::getFullLengthIcon() const
{
	return m_szFullLengthIcon;
}
int CvArtInfoUnit::getDamageStates() const
{
	return m_iDamageStates;
}
const char* CvArtInfoUnit::getTrailTexture() const
{
	return m_szTrailTexture;
}
float CvArtInfoUnit::getTrailWidth() const
{
	return m_fTrailWidth;
}
float CvArtInfoUnit::getTrailLength() const
{
	return m_fTrailLength;
}
float CvArtInfoUnit::getTrailTaper() const
{
	return m_fTrailTaper;
}
float CvArtInfoUnit::getTrailFadeStarTime() const
{
	return m_fTrailFadeStartTime;
}
float CvArtInfoUnit::getTrailFadeFalloff() const
{
	return m_fTrailFadeFalloff;
}
float CvArtInfoUnit::getBattleDistance() const
{
	return m_fBattleDistance;
}
float CvArtInfoUnit::getRangedDeathTime() const
{
	return m_fRangedDeathTime;
}
float CvArtInfoUnit::getExchangeAngle() const
{
	return m_fExchangeAngle;
}
bool CvArtInfoUnit::getCombatExempt() const
{
	return m_bCombatExempt;
}
bool CvArtInfoUnit::getSmoothMove() const
{
	return m_bSmoothMove;
}
float CvArtInfoUnit::getAngleInterpRate() const
{
	return m_fAngleInterRate;
}
float CvArtInfoUnit::getBankRate() const
{
	return m_fBankRate;
}
bool CvArtInfoUnit::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoScalableAsset::read(pXML))
	{
		return false;
	}
	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "ActionSound");
	m_iActionSoundScriptId = (szTextVal.GetLength() > 0) ? gDLL->getAudioTagIndex( szTextVal.GetCString(), AUDIOTAG_3DSCRIPT ) : -1;
	pXML->GetChildXmlValByName(szTextVal, "SelectionSound");
	m_iSelectionSoundScriptId = (szTextVal.GetLength() > 0) ? gDLL->getAudioTagIndex( szTextVal.GetCString(), AUDIOTAG_3DSCRIPT ) : -1;
	pXML->GetChildXmlValByName(szTextVal, "TrainSound");
	setTrainSound(szTextVal);
	pXML->GetChildXmlValByName(&m_bActAsRanged, "bActAsRanged" );
	pXML->GetChildXmlValByName(&m_bCombatExempt, "bCombatExempt", false );
	pXML->GetChildXmlValByName(&m_fExchangeAngle, "fExchangeAngle", 0.0f );
	pXML->GetChildXmlValByName(&m_bSmoothMove, "bSmoothMove", false );
	pXML->GetChildXmlValByName(&m_fAngleInterRate, "fAngleInterpRate", FLT_MAX );
	pXML->GetChildXmlValByName(&m_fBankRate, "fBankRate", 0 );
	pXML->GetChildXmlValByName(m_szFullLengthIcon, "FullLengthIcon");
	pXML->GetChildXmlValByName(&m_iDamageStates, "iDamageStates", 0);
	pXML->GetChildXmlValByName(&m_fBattleDistance, "fBattleDistance", 0.0f);
	pXML->GetChildXmlValByName(&m_fRangedDeathTime, "fRangedDeathTime", 0.0f );
	m_fTrailWidth = -1.0f; // invalid.
	if ( gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "TrailDefinition"))
	{
		pXML->GetChildXmlValByName(m_szTrailTexture, "Texture" );
		pXML->GetChildXmlValByName(&m_fTrailWidth, "fWidth" );
		pXML->GetChildXmlValByName(&m_fTrailLength, "fLength" );
		pXML->GetChildXmlValByName(&m_fTrailTaper, "fTaper" );
		pXML->GetChildXmlValByName(&m_fTrailFadeStartTime, "fFadeStartTime" );
		pXML->GetChildXmlValByName(&m_fTrailFadeFalloff, "fFadeFalloff" );
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML() );
	}
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"AudioRunSounds"))
	{
		pXML->GetChildXmlValByName(szTextVal, "AudioRunTypeLoop");
		m_iRunLoopSoundTag = GC.getFootstepAudioTypeByTag(szTextVal);
		pXML->GetChildXmlValByName(szTextVal, "AudioRunTypeEnd");
		m_iRunEndSoundTag = GC.getFootstepAudioTypeByTag(szTextVal);
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	return true;
}
const char* CvArtInfoUnit::getTrainSound() const
{
	return m_szTrainSound;
}
void CvArtInfoUnit::setTrainSound(const char* szVal)
{
	m_szTrainSound = szVal;
}
int CvArtInfoUnit::getRunLoopSoundTag() const
{
	return m_iRunLoopSoundTag;
}
int CvArtInfoUnit::getRunEndSoundTag() const
{
	return m_iRunEndSoundTag;
}
int CvArtInfoUnit::getSelectionSoundScriptId() const
{
	return m_iSelectionSoundScriptId;
}
int CvArtInfoUnit::getActionSoundScriptId() const
{
	return m_iActionSoundScriptId;
}
/////////////////////////////////////////////////////////////////////////////////////////////
// CvArtInfoBuilding
/////////////////////////////////////////////////////////////////////////////////////////////
CvArtInfoBuilding::CvArtInfoBuilding() :
m_bAnimated(false)
{
}
CvArtInfoBuilding::~CvArtInfoBuilding()
{
}
bool CvArtInfoBuilding::isAnimated() const
{
	return m_bAnimated;
}
const char* CvArtInfoBuilding::getLSystemName() const
{
	return m_szLSystemName;
}
const char* CvArtInfoBuilding::getCityTexture() const
{
	return m_cityTexture;
}
const char* CvArtInfoBuilding::getCitySelectedTexture() const
{
	return m_citySelectedTexture;
}

bool CvArtInfoBuilding::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoScalableAsset::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(m_cityTexture, "CityTexture");
	pXML->GetChildXmlValByName(m_citySelectedTexture, "CitySelectedTexture");
	pXML->GetChildXmlValByName(m_szLSystemName, "LSystem");
	pXML->GetChildXmlValByName(&m_bAnimated, "bAnimated");
	return true;
}
/////////////////////////////////////////////////////////////////////////////////////////////
// CvArtInfoCivilization
/////////////////////////////////////////////////////////////////////////////////////////////
CvArtInfoCivilization::CvArtInfoCivilization() :
m_bWhiteFlag(false),
m_bInvertFlag(false),
m_iFontButtonIndex(0)
{
}
CvArtInfoCivilization::~CvArtInfoCivilization()
{
}
bool CvArtInfoCivilization::isWhiteFlag() const
{
	return m_bWhiteFlag;
}
int CvArtInfoCivilization::getFontButtonIndex() const
{
	return m_iFontButtonIndex;
}
bool CvArtInfoCivilization::isInvertFlag() const
{
	return m_bInvertFlag;
}
bool CvArtInfoCivilization::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoAsset::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bWhiteFlag, "bWhiteFlag");
	pXML->GetChildXmlValByName(&m_bInvertFlag, "bInvertFlag");
	pXML->GetChildXmlValByName(&m_iFontButtonIndex, "iFontButtonIndex");
	return true;
}
/////////////////////////////////////////////////////////////////////////////////////////////
// CvArtInfoLeaderhead
/////////////////////////////////////////////////////////////////////////////////////////////
const char* CvArtInfoLeaderhead::getBackgroundKFM() const
{
	return m_szBackgroundKFM;
}
void CvArtInfoLeaderhead::setBackgroundKFM( const char* szKFM)
{
	m_szBackgroundKFM = szKFM;
}
bool CvArtInfoLeaderhead::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvArtInfoAsset::read(pXML))
	{
		return false;
	}
	if (pXML->GetChildXmlValByName(szTextVal, "BackgroundKFM"))
		setBackgroundKFM(szTextVal);
	else
		setBackgroundKFM("");
	return true;
}
/////////////////////////////////////////////////////////////////////////////////////////////
// CvArtInfoScalableAsset
/////////////////////////////////////////////////////////////////////////////////////////////
bool CvArtInfoScalableAsset::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoAsset::read(pXML))
	{
		return false;
	}
	return CvScalableInfo::read(pXML);
}
//////////////////////////////////////////////////////////////////////////
// CvArtInfoImprovement
//////////////////////////////////////////////////////////////////////////
CvArtInfoImprovement::CvArtInfoImprovement() :
m_bExtraAnimations(false)
{
}
CvArtInfoImprovement::~CvArtInfoImprovement()
{
}
bool CvArtInfoImprovement::isExtraAnimations() const
{
	return m_bExtraAnimations;
}
bool CvArtInfoImprovement::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoScalableAsset::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bExtraAnimations, "bExtraAnimations");
	return true;
}
//////////////////////////////////////////////////////////////////////////
// CvArtInfoTerrain
//////////////////////////////////////////////////////////////////////////
CvArtInfoTerrain::CvArtInfoTerrain() :
m_iLayerOrder(0),
m_eTerrainGroup(TERRAIN_GROUP_NONE),
m_numTextureBlends(16),
m_pTextureSlots(NULL)
{
	m_pTextureSlots = new CvTextureBlendSlotList * [m_numTextureBlends];
	for ( int i = 0; i < m_numTextureBlends; i++ )
	{
		m_pTextureSlots[i] = new CvTextureBlendSlotList;
	}
}
CvArtInfoTerrain::~CvArtInfoTerrain()
{
	for ( int i = 0; i < m_numTextureBlends; i++ )
	{
		SAFE_DELETE(m_pTextureSlots[i]);
	}
	SAFE_DELETE_ARRAY( m_pTextureSlots);
}
const char* CvArtInfoTerrain::getBaseTexture()
{
	return getPath();
}
void CvArtInfoTerrain::setBaseTexture(const char* szTmp )
{
	setPath(szTmp);
}
const char* CvArtInfoTerrain::getGridTexture()
{
	return m_szGridTexture;
}
void CvArtInfoTerrain::setGridTexture(const char* szTmp )
{
	m_szGridTexture = szTmp;
}
const char* CvArtInfoTerrain::getDetailTexture()
{
	return m_szDetailTexture;
}
void CvArtInfoTerrain::setDetailTexture(const char* szTmp)
{
	m_szDetailTexture = szTmp;
}
int CvArtInfoTerrain::getLayerOrder() const
{
	return m_iLayerOrder;
}
TerrainGroupTypes CvArtInfoTerrain::getTerrainGroup() const
{
	return m_eTerrainGroup;
}
CvTextureBlendSlotList &CvArtInfoTerrain::getBlendList(int blendMask)
{
	FAssert(blendMask>0 && blendMask<16);
	return *m_pTextureSlots[blendMask];
}
void BuildSlotList( CvTextureBlendSlotList &list, CvString &numlist)
{
	//convert string to
	char seps[]   = " ,\t\n";
	char *token;
	const char *numstring = numlist;
	token = strtok( const_cast<char *>(numstring), seps);
	while( token != NULL )
	{
		int slot = atoi(token);
		token = strtok( NULL, seps);
		int rotation = atoi(token);
		list.push_back(std::make_pair( slot, rotation));
		token = strtok( NULL, seps);
	}
}
bool CvArtInfoTerrain::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvArtInfoAsset::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "Grid");
	setGridTexture(szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "Detail");
	setDetailTexture(szTextVal);
	pXML->GetChildXmlValByName(&m_iLayerOrder, "LayerOrder");

	pXML->GetChildXmlValByName(szTextVal, "TerrainGroup");
	if(szTextVal.CompareNoCase("TERRAIN_GROUP_OCEAN") == 0)
	{
		m_eTerrainGroup = TERRAIN_GROUP_OCEAN;
	}
	else if(szTextVal.CompareNoCase("TERRAIN_GROUP_COAST") == 0)
	{
		m_eTerrainGroup = TERRAIN_GROUP_COAST;
	}
	else if(szTextVal.CompareNoCase("TERRAIN_GROUP_LAND") == 0)
	{
		m_eTerrainGroup = TERRAIN_GROUP_LAND;
	}
	else
	{
		FAssertMsg(false, "[Jason] Unknown TerrainGroupType.");
	}

	// Parse texture slots for blend tile lists
	char xmlName[] = "TextureBlend00";
	for(int i =1; i<m_numTextureBlends;i++ )
	{
		sprintf(xmlName+(strlen(xmlName)-2),"%02d",i);
		pXML->GetChildXmlValByName(szTextVal, xmlName);
		BuildSlotList(*m_pTextureSlots[i], szTextVal);
	}
	return CvArtInfoAsset::read(pXML);
}
//////////////////////////////////////////////////////////////////////////
// CvArtInfoFeature
//////////////////////////////////////////////////////////////////////////
CvArtInfoFeature::CvArtInfoFeature() :
m_bAnimated(false),
m_eTileArtType(TILE_ART_TYPE_NONE)
{
}
CvArtInfoFeature::~CvArtInfoFeature()
{
}
bool CvArtInfoFeature::isAnimated() const
{
	return m_bAnimated;
}
TileArtTypes CvArtInfoFeature::getTileArtType() const
{
	return m_eTileArtType;
}
bool CvArtInfoFeature::read(CvXMLLoadUtility* pXML)
{
	if (!CvArtInfoScalableAsset::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bAnimated, "bAnimated");
	CvString szTemp;
	pXML->GetChildXmlValByName(szTemp, "TileArtType");
	if(szTemp.CompareNoCase("TILE_ART_TYPE_NONE") == 0)
		m_eTileArtType = TILE_ART_TYPE_NONE;
	else if(szTemp.CompareNoCase("TILE_ART_TYPE_TREES") == 0)
		m_eTileArtType = TILE_ART_TYPE_TREES;
	else if(szTemp.CompareNoCase("TILE_ART_TYPE_HALF_TILING") == 0)
		m_eTileArtType = TILE_ART_TYPE_HALF_TILING;
	else
	{
		FAssertMsg(false, "[Jason] Unknown TileArtType.");
	}

	//feature varieties
	if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"FeatureVariety"))
	{
		do
		{
			m_aFeatureVarieties.push_back(FeatureVariety());
			FeatureVariety &featureVariety = m_aFeatureVarieties.back();
			//feature art pieces
			if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"FeatureArtPieces"))
			{
				if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"FeatureArtPiece"))
				{
					do
					{
						//connection mask
						pXML->GetChildXmlValByName(szTemp, "Connections");
						int connectionMask = getConnectionMaskFromString(szTemp);
						//model files
						if(gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"ModelFile"))
						{
							do
							{
								pXML->GetXmlVal(szTemp);
								FeatureArtPiece &featureArtPiece = featureVariety.createFeatureArtPieceFromConnectionMask(connectionMask);
								featureArtPiece.m_aArtModels.push_back(FeatureArtModel(szTemp));
							} while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "ModelFile"));
							gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
						}
					} while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "FeatureArtPiece"));
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
			//variety button
			pXML->GetChildXmlValByName(&featureVariety.m_iModelCopies, "iModelCopies", 1);
			pXML->GetChildXmlValByName(featureVariety.m_szVarietyButton, "VarietyButton");
		} while(gDLL->getXMLIFace()->LocateNextSiblingNodeByTagName(pXML->GetXML(), "FeatureVariety"));
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	return true;
}
const CvArtInfoFeature::FeatureVariety &CvArtInfoFeature::getVariety(int index) const
{
	FAssertMsg((index >= 0) && (index < (int) m_aFeatureVarieties.size()), "[Jason] Feature Variety index out of range.");
	return m_aFeatureVarieties[index];
}
int CvArtInfoFeature::getNumVarieties() const
{
	return m_aFeatureVarieties.size();
}
int CvArtInfoFeature::getConnectionMaskFromString(const CvString &connectionString)
{
	if(connectionString.IsEmpty())
		return 0;
	else
	{
		std::vector<CvString> tokens;
		connectionString.getTokens(" \t\n", tokens);
		int connectionMask = 0;
		for(int i=0;i<(int)tokens.size();i++)
		{
			// found a token, parse it.
			CvString &token = tokens[i];
			if(token.CompareNoCase("NW") == 0)
				connectionMask |= DIRECTION_NORTHWEST_MASK;
			else if(token.CompareNoCase("N") == 0)
				connectionMask |= DIRECTION_NORTH_MASK;
			else if(token.CompareNoCase("NE") == 0)
				connectionMask |= DIRECTION_NORTHEAST_MASK;
			else if(token.CompareNoCase("E") == 0)
				connectionMask |= DIRECTION_EAST_MASK;
			else if(token.CompareNoCase("SE") == 0)
				connectionMask |= DIRECTION_SOUTHEAST_MASK;
			else if(token.CompareNoCase("S") == 0)
				connectionMask |= DIRECTION_SOUTH_MASK;
			else if(token.CompareNoCase("SW") == 0)
				connectionMask |= DIRECTION_SOUTHWEST_MASK;
			else if(token.CompareNoCase("W") == 0)
				connectionMask |= DIRECTION_WEST_MASK;
			else
			{
				FAssertMsg(false, "[Jason] Invalid connection direction.");
			}
		}
		FAssertMsg(connectionMask > 0, "[Jason] Did not find feature connection mask.");
		return connectionMask;
	}
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvEmphasizeInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvEmphasizeInfo::CvEmphasizeInfo() :
m_bAvoidGrowth(false),
m_aiYieldModifiers(NULL)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvEmphasizeInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvEmphasizeInfo::~CvEmphasizeInfo()
{
	SAFE_DELETE_ARRAY(m_aiYieldModifiers);
}
bool CvEmphasizeInfo::isAvoidGrowth() const
{
	return m_bAvoidGrowth;
}
// Arrays
int CvEmphasizeInfo::getYieldChange(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiYieldModifiers ? m_aiYieldModifiers[i] : -1;
}
//
// read from XML
//
bool CvEmphasizeInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bAvoidGrowth, "bAvoidGrowth");
	pXML->SetVariableListTagPair(&m_aiYieldModifiers, "YieldModifiers", NUM_YIELD_TYPES, 0);
	return true;
}
//------------------------------------------------------------------------------------------------------
//
//  CvCultureLevelInfo
//
CvCultureLevelInfo::CvCultureLevelInfo() :
m_iThreshold(0)
{
}
CvCultureLevelInfo::~CvCultureLevelInfo()
{
}
int CvCultureLevelInfo::getThreshold() const
{
	return m_iThreshold;
}
bool CvCultureLevelInfo::read(CvXMLLoadUtility* pXml)
{
	if (!CvInfoBase::read(pXml))
	{
		return false;
	}
	pXml->GetChildXmlValByName(&m_iThreshold, "iThreshold");
	return true;
}
//------------------------------------------------------------------------------------------------------
//
//  CvEraInfo
//
CvEraInfo::CvEraInfo() :
m_iGameTurn(0),
m_iStartingUnitMultiplier(0),
m_iStartingDefenseUnits(0),
m_iStartingWorkerUnits(0),
m_iStartingExploreUnits(0),
m_iAdvancedStartPoints(0),
m_iStartingGold(0),
m_iFreePopulation(0),
m_iStartPercent(0),
m_iGrowthPercent(0),
m_iTrainPercent(0),
m_iConstructPercent(0),
m_iFatherPercent(0),
m_iGreatGeneralPercent(0),
m_iEventChancePerTurn(0),
m_iSoundtrackSpace(0),
m_iNumSoundtracks(0),
m_bRevolution(false),
m_bNoGoodies(false),
m_bFirstSoundtrackFirst(false),
m_paiCitySoundscapeSciptIds(NULL),
m_paiSoundtracks(NULL)
{
}
CvEraInfo::~CvEraInfo()
{
	SAFE_DELETE_ARRAY(m_paiCitySoundscapeSciptIds);
	SAFE_DELETE_ARRAY(m_paiSoundtracks);
}
int CvEraInfo::getGameTurn() const
{
	return m_iGameTurn;
}
int CvEraInfo::getStartingUnitMultiplier() const
{
	return m_iStartingUnitMultiplier;
}
int CvEraInfo::getStartingDefenseUnits() const
{
	return m_iStartingDefenseUnits;
}
int CvEraInfo::getStartingWorkerUnits() const
{
	return m_iStartingWorkerUnits;
}
int CvEraInfo::getStartingExploreUnits() const
{
	return m_iStartingExploreUnits;
}
int CvEraInfo::getAdvancedStartPoints() const
{
	return m_iAdvancedStartPoints;
}
int CvEraInfo::getStartingGold() const
{
	return m_iStartingGold;
}
int CvEraInfo::getFreePopulation() const
{
	return m_iFreePopulation;
}
int CvEraInfo::getStartPercent() const
{
	return m_iStartPercent;
}
int CvEraInfo::getGrowthPercent() const
{
	return m_iGrowthPercent;
}
int CvEraInfo::getTrainPercent() const
{
	return m_iTrainPercent;
}
int CvEraInfo::getConstructPercent() const
{
	return m_iConstructPercent;
}
int CvEraInfo::getFatherPercent() const
{
	return m_iFatherPercent;
}
int CvEraInfo::getGreatGeneralPercent() const
{
	return m_iGreatGeneralPercent;
}
int CvEraInfo::getEventChancePerTurn() const
{
	return m_iEventChancePerTurn;
}
int CvEraInfo::getSoundtrackSpace() const
{
	return m_iSoundtrackSpace;
}
bool CvEraInfo::isFirstSoundtrackFirst() const
{
	return m_bFirstSoundtrackFirst;
}
int CvEraInfo::getNumSoundtracks() const
{
	return m_iNumSoundtracks;
}
const char* CvEraInfo::getAudioUnitVictoryScript() const
{
	return m_szAudioUnitVictoryScript;
}
const char* CvEraInfo::getAudioUnitDefeatScript() const
{
	return m_szAudioUnitDefeatScript;
}
bool CvEraInfo::isRevolution() const
{
	return m_bRevolution;
}
bool CvEraInfo::isNoGoodies() const
{
	return m_bNoGoodies;
}
// Arrays
int CvEraInfo::getSoundtracks(int i) const
{
	FAssertMsg(i < getNumSoundtracks(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_paiSoundtracks ? m_paiSoundtracks[i] : -1;
}
int CvEraInfo::getCitySoundscapeSciptId(int i) const
{
//	FAssertMsg(i < ?, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_paiCitySoundscapeSciptIds ? m_paiCitySoundscapeSciptIds[i] : -1;
}
bool CvEraInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bRevolution, "bRevolution");
	pXML->GetChildXmlValByName(&m_bNoGoodies, "bNoGoodies");
	pXML->GetChildXmlValByName(&m_iGameTurn, "iGameTurn");
	pXML->GetChildXmlValByName(&m_iStartingUnitMultiplier, "iStartingUnitMultiplier");
	pXML->GetChildXmlValByName(&m_iStartingDefenseUnits, "iStartingDefenseUnits");
	pXML->GetChildXmlValByName(&m_iStartingWorkerUnits, "iStartingWorkerUnits");
	pXML->GetChildXmlValByName(&m_iStartingExploreUnits, "iStartingExploreUnits");
	pXML->GetChildXmlValByName(&m_iAdvancedStartPoints, "iAdvancedStartPoints");
	pXML->GetChildXmlValByName(&m_iStartingGold, "iStartingGold");
	pXML->GetChildXmlValByName(&m_iFreePopulation, "iFreePopulation");
	pXML->GetChildXmlValByName(&m_iStartPercent, "iStartPercent");
	pXML->GetChildXmlValByName(&m_iGrowthPercent, "iGrowthPercent");
	pXML->GetChildXmlValByName(&m_iTrainPercent, "iTrainPercent");
	pXML->GetChildXmlValByName(&m_iConstructPercent, "iConstructPercent");
	pXML->GetChildXmlValByName(&m_iFatherPercent, "iFatherPercent");
	pXML->GetChildXmlValByName(&m_iGreatGeneralPercent, "iGreatGeneralPercent");
	pXML->GetChildXmlValByName(&m_iEventChancePerTurn, "iEventChancePerTurn");
	pXML->GetChildXmlValByName(&m_iSoundtrackSpace, "iSoundtrackSpace");
	pXML->GetChildXmlValByName(&m_bFirstSoundtrackFirst, "bFirstSoundtrackFirst");
	pXML->GetChildXmlValByName(m_szAudioUnitVictoryScript, "AudioUnitVictoryScript");
	pXML->GetChildXmlValByName(m_szAudioUnitDefeatScript, "AudioUnitDefeatScript");
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "EraInfoSoundtracks"))
	{
		CvString* pszSoundTrackNames = NULL;
		pXML->SetStringList(&pszSoundTrackNames, &m_iNumSoundtracks);
		if (m_iNumSoundtracks > 0)
		{
			m_paiSoundtracks = new int[m_iNumSoundtracks];
			int j;
			for (j=0;j<m_iNumSoundtracks;j++)
			{
				m_paiSoundtracks[j] = ((!gDLL->getAudioDisabled()) ? gDLL->getAudioTagIndex(pszSoundTrackNames[j], AUDIOTAG_2DSCRIPT) : -1);
			}
		}
		else
		{
			m_paiSoundtracks = NULL;
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
		SAFE_DELETE_ARRAY(pszSoundTrackNames);
	}
	pXML->SetVariableListTagPairForAudioScripts(&m_paiCitySoundscapeSciptIds, "CitySoundscapes", GC.getNumCitySizeTypes());
	return true;
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvColorInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvColorInfo::CvColorInfo()
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvColorInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvColorInfo::~CvColorInfo()
{
}
const NiColorA& CvColorInfo::getColor() const
{
	return m_Color;
}
bool CvColorInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	float afColorVals[4];	// array to hold the 4 color values, red, green, blue, and alpha

	pXML->GetChildXmlValByName(&afColorVals[0], "fRed");
	pXML->GetChildXmlValByName(&afColorVals[1], "fGreen");
	pXML->GetChildXmlValByName(&afColorVals[2], "fBlue");
	pXML->GetChildXmlValByName(&afColorVals[3], "fAlpha");
	m_Color = NiColorA(afColorVals[0], afColorVals[1], afColorVals[2], afColorVals[3]);
	return true;
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CvPlayerColorInfo()
//
//  PURPOSE :   Default constructor
//
//------------------------------------------------------------------------------------------------------
CvPlayerColorInfo::CvPlayerColorInfo() :
m_iColorTypePrimary(NO_COLOR),
m_iColorTypeSecondary(NO_COLOR),
m_iTextColorType(NO_COLOR)
{
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   ~CvPlayerColorInfo()
//
//  PURPOSE :   Default destructor
//
//------------------------------------------------------------------------------------------------------
CvPlayerColorInfo::~CvPlayerColorInfo()
{
}
int CvPlayerColorInfo::getColorTypePrimary() const
{
	return m_iColorTypePrimary;
}
int CvPlayerColorInfo::getColorTypeSecondary() const
{
	return m_iColorTypeSecondary;
}
int CvPlayerColorInfo::getTextColorType() const
{
	return m_iTextColorType;
}
bool CvPlayerColorInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(szTextVal, "ColorTypePrimary");
	m_iColorTypePrimary = pXML->FindInInfoClass( szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "ColorTypeSecondary");
	m_iColorTypeSecondary = pXML->FindInInfoClass( szTextVal);
	pXML->GetChildXmlValByName(szTextVal, "TextColorType");
	m_iTextColorType = pXML->FindInInfoClass( szTextVal);
	return true;
}
//------------------------------------------------------------------------------------------------------
//
//	CvLandscapeInfo
//
//
CvLandscapeInfo::CvLandscapeInfo() :
m_iPlotVertsWide(0),
m_iPlotVertsHigh(0),
m_iPlotsPerCellX(0),
m_iPlotsPerCellY(0),
m_iCellVertsWide(0),
m_iCellVertsHigh(0),
m_iWaterHeight(0),
m_fTextureScaleX(0.0f),
m_fTextureScaleY(0.0f),
m_fZScale(0.0f),
m_fPeakScale(0.0f),
m_fHillScale(0.0f)
{
}
int CvLandscapeInfo::getPlotVertsWide() const
{
	return m_iPlotVertsWide;
}
int CvLandscapeInfo::getPlotVertsHigh() const
{
	return m_iPlotVertsHigh;
}
int CvLandscapeInfo::getPlotsPerCellX() const
{
	return m_iPlotsPerCellX;
}
int CvLandscapeInfo::getPlotsPerCellY() const
{
	return m_iPlotsPerCellY;
}
int CvLandscapeInfo::getCellVertsWide() const
{
	return m_iCellVertsWide;
}
int CvLandscapeInfo::getCellVertsHigh() const
{
	return m_iCellVertsHigh;
}
int CvLandscapeInfo::getWaterHeight() const
{
	return m_iWaterHeight;
}
float CvLandscapeInfo::getTextureScaleX() const
{
	return m_fTextureScaleX;
}
float CvLandscapeInfo::getTextureScaleY() const
{
	return m_fTextureScaleY;
}
float CvLandscapeInfo::getZScale() const
{
	return m_fZScale;
}
float CvLandscapeInfo::getPeakScale() const
{
	return 	m_fPeakScale;
}
float CvLandscapeInfo::getHillScale() const
{
	return 	m_fHillScale;
}
const char* CvLandscapeInfo::getEnvironmentTexture()
{
	return m_szEnvironmentTexture;
}
//
// read from xml
//
bool CvLandscapeInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_iWaterHeight, "iWaterHeight");
	pXML->GetChildXmlValByName(m_szEnvironmentTexture, "EnvironmentTexture");
	pXML->GetChildXmlValByName(&m_fTextureScaleX, "fTextureScaleX");
	pXML->GetChildXmlValByName(&m_fTextureScaleY, "fTextureScaleY");
	pXML->GetChildXmlValByName(&m_iPlotVertsWide, "iPlotVertsWide");
	pXML->GetChildXmlValByName(&m_iPlotVertsHigh, "iPlotVertsHigh");
	pXML->GetChildXmlValByName(&m_iPlotsPerCellX, "iPlotsPerCellX");
	pXML->GetChildXmlValByName(&m_iPlotsPerCellY, "iPlotsPerCellY");
	m_iCellVertsWide = m_iPlotsPerCellX * (m_iPlotVertsWide - 1) + 1;
	m_iCellVertsHigh = m_iPlotsPerCellY * (m_iPlotVertsHigh - 1) + 1;
	pXML->GetChildXmlValByName(&m_fZScale, "fZScale");
	pXML->GetChildXmlValByName(&m_fPeakScale, "fPeakScale");
	pXML->GetChildXmlValByName(&m_fHillScale, "fHillScale");

	return true;
}
//////////////////////////////////////////////////////////////////////////
// CvGameText
//////////////////////////////////////////////////////////////////////////
// static
int CvGameText::NUM_LANGUAGES = 0;
int CvGameText::getNumLanguages() const
{
	return NUM_LANGUAGES;
}
void CvGameText::setNumLanguages(int iNum)
{
	NUM_LANGUAGES = iNum;
}
CvGameText::CvGameText() :
	m_szGender("N"),
	m_szPlural("false")
{
}
const wchar* CvGameText::getText() const
{
	return m_szText;
}
void CvGameText::setText(const wchar* szText)
{
	m_szText = szText;
}
bool CvGameText::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	CvWString wszTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	gDLL->getXMLIFace()->SetToChild(pXML->GetXML()); // Move down to Child level
	pXML->GetXmlVal(m_szType);		// TAG

	static const int iMaxNumLanguages = GC.getDefineINT("MAX_NUM_LANGUAGES");
	int iNumLanguages = NUM_LANGUAGES ? NUM_LANGUAGES : iMaxNumLanguages + 1;
	int j=0;
	for (j = 0; j < iNumLanguages; j++)
	{
		pXML->SkipToNextVal();	// skip comments
		if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()) || j == iMaxNumLanguages)
		{
			NUM_LANGUAGES = j;
			break;
		}
		if (j == GAMETEXT.getCurrentLanguage()) // Only add appropriate language Text
		{
			// TEXT
			if (pXML->GetChildXmlValByName(wszTextVal, "Text"))
			{
				setText(wszTextVal);
			}
			else
			{
				pXML->GetXmlVal(wszTextVal);
				setText(wszTextVal);
				if (NUM_LANGUAGES > 0)
				{
					break;
				}
			}
			// GENDER
			if (pXML->GetChildXmlValByName(wszTextVal, "Gender"))
			{
				setGender(wszTextVal);
			}
			// PLURAL
			if (pXML->GetChildXmlValByName(wszTextVal, "Plural"))
			{
				setPlural(wszTextVal);
			}
			if (NUM_LANGUAGES > 0)
			{
				break;
			}
		}
	}
	gDLL->getXMLIFace()->SetToParent(pXML->GetXML()); // Move back up to Parent
	return true;
}
//////////////////////////////////////////////////////////////////////////
//
//	CvDiplomacyTextInfo
//
//
CvDiplomacyTextInfo::CvDiplomacyTextInfo() :
m_iNumResponses(0),
m_pResponses(NULL)
{
}
// note - Response member vars allocated by CvXmlLoadUtility
void CvDiplomacyTextInfo::init(int iNum)
{
	uninit();
	m_pResponses = new Response[iNum];
	m_iNumResponses=iNum;
}
void CvDiplomacyTextInfo::uninit()
{
	SAFE_DELETE_ARRAY(m_pResponses);
}
int CvDiplomacyTextInfo::getNumResponses() const
{
	return m_iNumResponses;
}
bool CvDiplomacyTextInfo::getCivilizationTypes(int i, int j) const
{
	FAssertMsg(i < getNumResponses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < GC.getNumCivilizationInfos(), "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_pResponses[i].m_abCivilizationTypes[j];
}
bool CvDiplomacyTextInfo::getLeaderHeadTypes(int i, int j) const
{
	FAssertMsg(i < getNumResponses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < GC.getNumLeaderHeadInfos(), "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_pResponses[i].m_abLeaderHeadTypes[j];
}
bool CvDiplomacyTextInfo::getAttitudeTypes(int i, int j) const
{
	FAssertMsg(i < getNumResponses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < NUM_ATTITUDE_TYPES, "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_pResponses[i].m_abAttitudeTypes[j];
}
bool CvDiplomacyTextInfo::getDiplomacyPowerTypes(int i, int j) const
{
	FAssertMsg(i < getNumResponses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < NUM_DIPLOMACYPOWER_TYPES, "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_pResponses[i].m_abDiplomacyPowerTypes[j];
}
int CvDiplomacyTextInfo::getNumDiplomacyText(int i) const
{
	FAssertMsg(i < getNumResponses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_pResponses[i].m_iNumDiplomacyText;
}
const char* CvDiplomacyTextInfo::getDiplomacyText(int i, int j) const
{
	FAssertMsg(i < getNumResponses(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	FAssertMsg(j < getNumDiplomacyText(i), "Index out of bounds");
	FAssertMsg(j > -1, "Index out of bounds");
	return m_pResponses[i].m_paszDiplomacyText[j];
}
void CvDiplomacyTextInfo::Response::read(FDataStreamBase* stream)
{
	stream->Read(&m_iNumDiplomacyText);
	SAFE_DELETE_ARRAY(m_abCivilizationTypes);
	m_abCivilizationTypes = new bool[GC.getNumCivilizationInfos()];
	stream->Read(GC.getNumCivilizationInfos(), m_abCivilizationTypes);
	SAFE_DELETE_ARRAY(m_abLeaderHeadTypes);
	m_abLeaderHeadTypes = new bool[GC.getNumLeaderHeadInfos()];
	stream->Read(GC.getNumLeaderHeadInfos(), m_abLeaderHeadTypes);
	SAFE_DELETE_ARRAY(m_abAttitudeTypes);
	m_abAttitudeTypes = new bool[NUM_ATTITUDE_TYPES];
	stream->Read(NUM_ATTITUDE_TYPES, m_abAttitudeTypes);
	SAFE_DELETE_ARRAY(m_abDiplomacyPowerTypes);
	m_abDiplomacyPowerTypes = new bool[NUM_DIPLOMACYPOWER_TYPES];
	stream->Read(NUM_DIPLOMACYPOWER_TYPES, m_abDiplomacyPowerTypes);
	SAFE_DELETE_ARRAY(m_paszDiplomacyText);
	m_paszDiplomacyText = new CvString[m_iNumDiplomacyText];
	stream->ReadString(m_iNumDiplomacyText, m_paszDiplomacyText);
}
void CvDiplomacyTextInfo::Response::write(FDataStreamBase* stream)
{
	stream->Write(m_iNumDiplomacyText);
	stream->Write(GC.getNumCivilizationInfos(), m_abCivilizationTypes);
	stream->Write(GC.getNumLeaderHeadInfos(), m_abLeaderHeadTypes);
	stream->Write(NUM_ATTITUDE_TYPES, m_abAttitudeTypes);
	stream->Write(NUM_DIPLOMACYPOWER_TYPES, m_abDiplomacyPowerTypes);
	stream->WriteString(m_iNumDiplomacyText, m_paszDiplomacyText);
}
void CvDiplomacyTextInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);		// flag for expansion
	stream->Read(&m_iNumResponses);
	// Arrays
	init(m_iNumResponses);
	for (uint uiIndex = 0; (int) uiIndex < m_iNumResponses; uiIndex++)
	{
		m_pResponses[uiIndex].read(stream);
	}
}
void CvDiplomacyTextInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_iNumResponses);
	// Arrays
	for (uint uiIndex = 0; (int) uiIndex < m_iNumResponses; uiIndex++)
	{
		m_pResponses[uiIndex].write(stream);
	}
}
bool CvDiplomacyTextInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	int j;
	pXML->GetChildXmlValByName(szTextVal, "Type");
	if ( gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"Responses") )
	{
		int iIndexVal = gDLL->getXMLIFace()->NumOfChildrenByTagName(pXML->GetXML(), "Response");
		init(iIndexVal);
		for (j = 0; j < iIndexVal; j++)
		{
			if (j == 0)
			{
				gDLL->getXMLIFace()->SetToChild(pXML->GetXML());
			}
			// Civilizations
			pXML->SetVariableListTagPair(&m_pResponses[j].m_abCivilizationTypes, "Civilizations", GC.getNumCivilizationInfos(), false);
			// Leaders
			pXML->SetVariableListTagPair(&m_pResponses[j].m_abLeaderHeadTypes, "Leaders", GC.getNumLeaderHeadInfos(), false);
			// AttitudeTypes
			pXML->SetVariableListTagPair(&m_pResponses[j].m_abAttitudeTypes, "Attitudes", NUM_ATTITUDE_TYPES, false);
			// PowerTypes
			pXML->SetVariableListTagPair(&m_pResponses[j].m_abDiplomacyPowerTypes, "DiplomacyPowers", NUM_DIPLOMACYPOWER_TYPES, false);
			// DiplomacyText
			if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"DiplomacyText"))
			{
				pXML->SetStringList(&m_pResponses[j].m_paszDiplomacyText, &m_pResponses[j].m_iNumDiplomacyText);
				gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
			}
			if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
			{
				break;
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	return true;
}

//////////////////////////////////////////////////////////////////////////
//
//	CvEffectInfo			Misc\CIV4EffectInfos.xml
//
//
CvEffectInfo::CvEffectInfo() :
m_fUpdateRate(0.0f),
m_bProjectile(false),
m_bSticky(false),
m_fProjectileSpeed(0.0f),
m_fProjectileArc(0.0f)
{
}
CvEffectInfo::~CvEffectInfo()
{
}
bool CvEffectInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	CvScalableInfo::read(pXML);
	pXML->GetChildXmlValByName(szTextVal, "Path");
	setPath(szTextVal);
	pXML->GetChildXmlValByName(&m_fUpdateRate, "fUpdateRate" );
	int iTemporary;
	pXML->GetChildXmlValByName(&iTemporary, "bIsProjectile" );
	m_bProjectile = iTemporary != 0;
	pXML->GetChildXmlValByName(&m_fProjectileSpeed, "fSpeed" );
	pXML->GetChildXmlValByName(&m_fProjectileArc, "fArcValue" );
	pXML->GetChildXmlValByName(&m_bSticky, "bSticky", false );
	return true;
}

//////////////////////////////////////////////////////////////////////////
//
//	CvAttachableInfo			Misc\CIV4AttachableInfos.xml
//
//
CvAttachableInfo::CvAttachableInfo() :
m_fUpdateRate(0.0f)
{
}
CvAttachableInfo::~CvAttachableInfo()
{
}
bool CvAttachableInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	CvScalableInfo::read(pXML);
	pXML->GetChildXmlValByName(szTextVal, "Path");
	setPath(szTextVal);
	return true;
}

//////////////////////////////////////////////////////////////////////////
//
//	CvGameOptionInfo
//	Game options and their default values
//
//
CvGameOptionInfo::CvGameOptionInfo() :
m_bDefault(false),
m_bVisible(true)
{
}
CvGameOptionInfo::~CvGameOptionInfo()
{
}
bool CvGameOptionInfo::getDefault() const
{
	return m_bDefault;
}
bool CvGameOptionInfo::getVisible() const
{
	return m_bVisible;
}
bool CvGameOptionInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bDefault, "bDefault");
	pXML->GetChildXmlValByName(&m_bVisible, "bVisible");
	return true;
}
//////////////////////////////////////////////////////////////////////////
//
//	CvMPOptionInfo
//	Multiplayer options and their default values
//
//
CvMPOptionInfo::CvMPOptionInfo() :
m_bDefault(false)
{
}
CvMPOptionInfo::~CvMPOptionInfo()
{
}
bool CvMPOptionInfo::getDefault() const
{
	return m_bDefault;
}
bool CvMPOptionInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bDefault, "bDefault");
	return true;
}
//////////////////////////////////////////////////////////////////////////
//
//	CvForceControlInfo
//	Forced Controls and their default values
//
//
CvForceControlInfo::CvForceControlInfo() :
m_bDefault(false)
{
}
CvForceControlInfo::~CvForceControlInfo()
{
}
bool CvForceControlInfo::getDefault() const
{
	return m_bDefault;
}
bool CvForceControlInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bDefault, "bDefault");
	return true;
}
//////////////////////////////////////////////////////////////////////////
//
//	CvPlayerOptionInfo
//	Player options and their default values
//
//
CvPlayerOptionInfo::CvPlayerOptionInfo() :
m_bDefault(false)
{
}
CvPlayerOptionInfo::~CvPlayerOptionInfo()
{
}
bool CvPlayerOptionInfo::getDefault() const
{
	return m_bDefault;
}
bool CvPlayerOptionInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bDefault, "bDefault");
	return true;
}
//////////////////////////////////////////////////////////////////////////
//
//	CvGraphicOptionInfo
//	Graphic options and their default values
//
//
CvGraphicOptionInfo::CvGraphicOptionInfo() :
m_bDefault(false)
{
}
CvGraphicOptionInfo::~CvGraphicOptionInfo()
{
}
bool CvGraphicOptionInfo::getDefault() const
{
	return m_bDefault;
}
bool CvGraphicOptionInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bDefault, "bDefault");
	return true;
}
//////////////////////////////////////////////////////////////////////////
//
//	CvEventTriggerInfo
//	Event triggers
//
//
CvEventTriggerInfo::CvEventTriggerInfo() :
	m_iPercentGamesActive(0),
	m_iProbability(0),
	m_iNumUnits(0),
	m_iNumBuildings(0),
	m_iNumUnitsGlobal(0),
	m_iNumBuildingsGlobal(0),
	m_iNumPlotsRequired(0),
	m_iPlotType(0),
	m_iOtherPlayerShareBorders(0),
	m_iCivic(NO_CIVIC),
	m_iMinPopulation(0),
	m_iMaxPopulation(0),
	m_iMinMapLandmass(0),
	m_iMinOurLandmass(0),
	m_iMaxOurLandmass(0),
	m_iMinDifficulty(NO_HANDICAP),
	m_iUnitDamagedWeight(0),
	m_iUnitDistanceWeight(0),
	m_iUnitExperienceWeight(0),
	m_iMinTreasury(0),
	m_bTutorial(false),
	m_bSinglePlayer(false),
	m_bTeam(false),
	m_bRecurring(false),
	m_bGlobal(false),
	m_bPickPlayer(false),
	m_bOtherPlayerWar(false),
	m_bOtherPlayerAI(false),
	m_bOtherPlayerNative(false),
	m_bOtherPlayerPlayable(false),
	m_bPickCity(false),
	m_bPickOtherPlayerCity(false),
	m_bShowPlot(true),
	m_iCityFoodWeight(0),
	m_bUnitsOnPlot(false),
	m_bOwnPlot(false),
	m_bProbabilityUnitMultiply(false),
	m_bProbabilityBuildingMultiply(false),
	m_bPrereqEventCity(false),
	m_bFrontPopup(false)
{
}
CvEventTriggerInfo::~CvEventTriggerInfo()
{
}
int CvEventTriggerInfo::getPercentGamesActive() const
{
	return m_iPercentGamesActive;
}
int CvEventTriggerInfo::getProbability() const
{
	return m_iProbability;
}
int CvEventTriggerInfo::getUnitRequired(int i) const
{
	return m_aiUnitsRequired[i];
}
int CvEventTriggerInfo::getNumUnitsRequired() const
{
	return (int)m_aiUnitsRequired.size();
}
int CvEventTriggerInfo::getBuildingRequired(int i) const
{
	return m_aiBuildingsRequired[i];
}
int CvEventTriggerInfo::getNumBuildingsRequired() const
{
	return (int)m_aiBuildingsRequired.size();
}
int CvEventTriggerInfo::getNumUnits() const
{
	return m_iNumUnits;
}
int CvEventTriggerInfo::getNumBuildings() const
{
	return m_iNumBuildings;
}
int CvEventTriggerInfo::getNumUnitsGlobal() const
{
	return m_iNumUnitsGlobal;
}
int CvEventTriggerInfo::getNumBuildingsGlobal() const
{
	return m_iNumBuildingsGlobal;
}
int CvEventTriggerInfo::getNumPlotsRequired() const
{
	return m_iNumPlotsRequired;
}
int CvEventTriggerInfo::getPlotType() const
{
	return m_iPlotType;
}
int CvEventTriggerInfo::getOtherPlayerShareBorders() const
{
	return m_iOtherPlayerShareBorders;
}
int CvEventTriggerInfo::getCivic() const
{
	return m_iCivic;
}
int CvEventTriggerInfo::getMinPopulation() const
{
	return m_iMinPopulation;
}
int CvEventTriggerInfo::getMaxPopulation() const
{
	return m_iMaxPopulation;
}
int CvEventTriggerInfo::getMinMapLandmass() const
{
	return m_iMinMapLandmass;
}
int CvEventTriggerInfo::getMinOurLandmass() const
{
	return m_iMinOurLandmass;
}
int CvEventTriggerInfo::getMaxOurLandmass() const
{
	return m_iMaxOurLandmass;
}
int CvEventTriggerInfo::getMinDifficulty() const
{
	return m_iMinDifficulty;
}
int CvEventTriggerInfo::getUnitDamagedWeight() const
{
	return m_iUnitDamagedWeight;
}
int CvEventTriggerInfo::getUnitDistanceWeight() const
{
	return m_iUnitDistanceWeight;
}
int CvEventTriggerInfo::getUnitExperienceWeight() const
{
	return m_iUnitExperienceWeight;
}
int CvEventTriggerInfo::getMinTreasury() const
{
	return m_iMinTreasury;
}
int CvEventTriggerInfo::getEvent(int i) const
{
	return m_aiEvents[i];
}
int CvEventTriggerInfo::getNumEvents() const
{
	return (int)m_aiEvents.size();
}
int CvEventTriggerInfo::getPrereqEvent(int i) const
{
	return m_aiPrereqEvents[i];
}
int CvEventTriggerInfo::getNumPrereqEvents() const
{
	return (int)m_aiPrereqEvents.size();
}
int CvEventTriggerInfo::getFeatureRequired(int i) const
{
	return m_aiFeaturesRequired[i];
}
int CvEventTriggerInfo::getNumFeaturesRequired() const
{
	return (int)m_aiFeaturesRequired.size();
}
int CvEventTriggerInfo::getTerrainRequired(int i) const
{
	return m_aiTerrainsRequired[i];
}
int CvEventTriggerInfo::getNumTerrainsRequired() const
{
	return (int)m_aiTerrainsRequired.size();
}
int CvEventTriggerInfo::getImprovementRequired(int i) const
{
	return m_aiImprovementsRequired[i];
}
int CvEventTriggerInfo::getNumImprovementsRequired() const
{
	return (int)m_aiImprovementsRequired.size();
}
int CvEventTriggerInfo::getRouteRequired(int i) const
{
	return m_aiRoutesRequired[i];
}
int CvEventTriggerInfo::getNumRoutesRequired() const
{
	return (int)m_aiRoutesRequired.size();
}
bool CvEventTriggerInfo::isTutorial() const
{
	return m_bTutorial;
}
bool CvEventTriggerInfo::isSinglePlayer() const
{
	return m_bSinglePlayer;
}
bool CvEventTriggerInfo::isTeam() const
{
	return m_bTeam;
}
const CvWString& CvEventTriggerInfo::getText(int i) const
{
	FAssert(i >= 0 && i < (int)m_aszText.size());
	return m_aszText[i];
}
int CvEventTriggerInfo::getTextEra(int i) const
{
	FAssert(i >= 0 && i < (int)m_aiTextEra.size());
	return m_aiTextEra[i];
}
int CvEventTriggerInfo::getNumTexts() const
{
	FAssert(m_aiTextEra.size() == m_aszText.size());
	return m_aszText.size();
}
const CvWString& CvEventTriggerInfo::getWorldNews(int i) const
{
	FAssert(i >= 0 && i < (int)m_aszWorldNews.size());
	return m_aszWorldNews[i];
}
int CvEventTriggerInfo::getNumWorldNews() const
{
	return m_aszWorldNews.size();
}
bool CvEventTriggerInfo::isRecurring() const
{
	return m_bRecurring;
}
bool CvEventTriggerInfo::isGlobal() const
{
	return m_bGlobal;
}
bool CvEventTriggerInfo::isPickPlayer() const
{
	return m_bPickPlayer;
}
bool CvEventTriggerInfo::isOtherPlayerWar() const
{
	return m_bOtherPlayerWar;
}
bool CvEventTriggerInfo::isOtherPlayerAI() const
{
	return m_bOtherPlayerAI;
}
bool CvEventTriggerInfo::isOtherPlayerNative() const
{
	return m_bOtherPlayerNative;
}
bool CvEventTriggerInfo::isOtherPlayerPlayable() const
{
	return m_bOtherPlayerPlayable;
}
bool CvEventTriggerInfo::isPickCity() const
{
	return m_bPickCity;
}
bool CvEventTriggerInfo::isPickOtherPlayerCity() const
{
	return m_bPickOtherPlayerCity;
}
bool CvEventTriggerInfo::isShowPlot() const
{
	return m_bShowPlot;
}
int CvEventTriggerInfo::getCityFoodWeight() const
{
	return m_iCityFoodWeight;
}
bool CvEventTriggerInfo::isUnitsOnPlot() const
{
	return m_bUnitsOnPlot;
}
bool CvEventTriggerInfo::isOwnPlot() const
{
	return m_bOwnPlot;
}
bool CvEventTriggerInfo::isProbabilityUnitMultiply() const
{
	return m_bProbabilityUnitMultiply;
}
bool CvEventTriggerInfo::isProbabilityBuildingMultiply() const
{
	return m_bProbabilityBuildingMultiply;
}
bool CvEventTriggerInfo::isPrereqEventCity() const
{
	return m_bPrereqEventCity;
}
bool CvEventTriggerInfo::isFrontPopup() const
{
	return m_bFrontPopup;
}
const char* CvEventTriggerInfo::getPythonCallback() const
{
	return m_szPythonCallback;
}
const char* CvEventTriggerInfo::getPythonCanDo() const
{
	return m_szPythonCanDo;
}
const char* CvEventTriggerInfo::getPythonCanDoCity() const
{
	return m_szPythonCanDoCity;
}
const char* CvEventTriggerInfo::getPythonCanDoUnit() const
{
	return m_szPythonCanDoUnit;
}
void CvEventTriggerInfo::read(FDataStreamBase* stream)
{
	int iNumElements;
	int iElement;
	CvWString szElement;
	CvInfoBase::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);	// flags for expansion
	stream->Read(&m_iPercentGamesActive);
	stream->Read(&m_iProbability);
	stream->Read(&m_iNumUnits);
	stream->Read(&m_iNumBuildings);
	stream->Read(&m_iNumUnitsGlobal);
	stream->Read(&m_iNumBuildingsGlobal);
	stream->Read(&m_iNumPlotsRequired);
	stream->Read(&m_iPlotType);
	stream->Read(&m_iOtherPlayerShareBorders);
	stream->Read(&m_iCivic);
	stream->Read(&m_iMinPopulation);
	stream->Read(&m_iMaxPopulation);
	stream->Read(&m_iMinMapLandmass);
	stream->Read(&m_iMinOurLandmass);
	stream->Read(&m_iMaxOurLandmass);
	stream->Read(&m_iMinDifficulty);
	stream->Read(&m_iUnitDamagedWeight);
	stream->Read(&m_iUnitDistanceWeight);
	stream->Read(&m_iUnitExperienceWeight);
	stream->Read(&m_iMinTreasury);
	stream->Read(&iNumElements);
	m_aiUnitsRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiUnitsRequired.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiBuildingsRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiBuildingsRequired.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiEvents.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiEvents.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiPrereqEvents.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiPrereqEvents.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiFeaturesRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiFeaturesRequired.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiTerrainsRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiTerrainsRequired.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiImprovementsRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiImprovementsRequired.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aiRoutesRequired.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiRoutesRequired.push_back(iElement);
	}
	stream->Read(&m_bTutorial);
	stream->Read(&m_bSinglePlayer);
	stream->Read(&m_bTeam);
	stream->Read(&m_bRecurring);
	stream->Read(&m_bGlobal);
	stream->Read(&m_bPickPlayer);
	stream->Read(&m_bOtherPlayerWar);
	stream->Read(&m_bOtherPlayerAI);
	stream->Read(&m_bOtherPlayerNative);
	stream->Read(&m_bOtherPlayerPlayable);
	stream->Read(&m_bPickCity);
	stream->Read(&m_bPickOtherPlayerCity);
	stream->Read(&m_bShowPlot);
	stream->Read(&m_iCityFoodWeight);
	stream->Read(&m_bUnitsOnPlot);
	stream->Read(&m_bOwnPlot);
	stream->Read(&m_bProbabilityUnitMultiply);
	stream->Read(&m_bProbabilityBuildingMultiply);
	stream->Read(&m_bPrereqEventCity);
	stream->Read(&m_bFrontPopup);
	stream->Read(&iNumElements);
	m_aszText.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->ReadString(szElement);
		m_aszText.push_back(szElement);
	}
	m_aiTextEra.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->Read(&iElement);
		m_aiTextEra.push_back(iElement);
	}
	stream->Read(&iNumElements);
	m_aszWorldNews.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->ReadString(szElement);
		m_aszWorldNews.push_back(szElement);
	}
	stream->ReadString(m_szPythonCallback);
	stream->ReadString(m_szPythonCanDo);
	stream->ReadString(m_szPythonCanDoCity);
	stream->ReadString(m_szPythonCanDoUnit);
}
void CvEventTriggerInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_iPercentGamesActive);
	stream->Write(m_iProbability);
	stream->Write(m_iNumUnits);
	stream->Write(m_iNumBuildings);
	stream->Write(m_iNumUnitsGlobal);
	stream->Write(m_iNumBuildingsGlobal);
	stream->Write(m_iNumPlotsRequired);
	stream->Write(m_iPlotType);
	stream->Write(m_iOtherPlayerShareBorders);
	stream->Write(m_iCivic);
	stream->Write(m_iMinPopulation);
	stream->Write(m_iMaxPopulation);
	stream->Write(m_iMinMapLandmass);
	stream->Write(m_iMinOurLandmass);
	stream->Write(m_iMaxOurLandmass);
	stream->Write(m_iMinDifficulty);
	stream->Write(m_iUnitDamagedWeight);
	stream->Write(m_iUnitDistanceWeight);
	stream->Write(m_iUnitExperienceWeight);
	stream->Write(m_iMinTreasury);
	stream->Write(m_aiUnitsRequired.size());
	for (std::vector<int>::iterator it = m_aiUnitsRequired.begin(); it != m_aiUnitsRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiBuildingsRequired.size());
	for (std::vector<int>::iterator it = m_aiBuildingsRequired.begin(); it != m_aiBuildingsRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiEvents.size());
	for (std::vector<int>::iterator it = m_aiEvents.begin(); it != m_aiEvents.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiPrereqEvents.size());
	for (std::vector<int>::iterator it = m_aiPrereqEvents.begin(); it != m_aiPrereqEvents.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiFeaturesRequired.size());
	for (std::vector<int>::iterator it = m_aiFeaturesRequired.begin(); it != m_aiFeaturesRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiTerrainsRequired.size());
	for (std::vector<int>::iterator it = m_aiTerrainsRequired.begin(); it != m_aiTerrainsRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiImprovementsRequired.size());
	for (std::vector<int>::iterator it = m_aiImprovementsRequired.begin(); it != m_aiImprovementsRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aiRoutesRequired.size());
	for (std::vector<int>::iterator it = m_aiRoutesRequired.begin(); it != m_aiRoutesRequired.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_bTutorial);
	stream->Write(m_bSinglePlayer);
	stream->Write(m_bTeam);
	stream->Write(m_bRecurring);
	stream->Write(m_bGlobal);
	stream->Write(m_bPickPlayer);
	stream->Write(m_bOtherPlayerWar);
	stream->Write(m_bOtherPlayerAI);
	stream->Write(m_bOtherPlayerNative);
	stream->Write(m_bOtherPlayerPlayable);
	stream->Write(m_bPickCity);
	stream->Write(m_bPickOtherPlayerCity);
	stream->Write(m_bShowPlot);
	stream->Write(m_iCityFoodWeight);
	stream->Write(m_bUnitsOnPlot);
	stream->Write(m_bOwnPlot);
	stream->Write(m_bProbabilityUnitMultiply);
	stream->Write(m_bProbabilityBuildingMultiply);
	stream->Write(m_bPrereqEventCity);
	stream->Write(m_bFrontPopup);
	stream->Write(m_aszText.size());
	for (std::vector<CvWString>::iterator it = m_aszText.begin(); it != m_aszText.end(); ++it)
	{
		stream->WriteString(*it);
	}
	for (std::vector<int>::iterator it = m_aiTextEra.begin(); it != m_aiTextEra.end(); ++it)
	{
		stream->Write(*it);
	}
	stream->Write(m_aszWorldNews.size());
	for (std::vector<CvWString>::iterator it = m_aszWorldNews.begin(); it != m_aszWorldNews.end(); ++it)
	{
		stream->WriteString(*it);
	}
	stream->WriteString(m_szPythonCallback);
	stream->WriteString(m_szPythonCanDo);
	stream->WriteString(m_szPythonCanDoCity);
	stream->WriteString(m_szPythonCanDoUnit);
}
bool CvEventTriggerInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_iPercentGamesActive, "iPercentGamesActive");
	pXML->GetChildXmlValByName(&m_iProbability, "iWeight");
	pXML->GetChildXmlValByName(&m_iNumUnits, "iNumUnits");
	pXML->GetChildXmlValByName(&m_iNumBuildings, "iNumBuildings");
	pXML->GetChildXmlValByName(&m_iNumUnitsGlobal, "iNumUnitsGlobal");
	pXML->GetChildXmlValByName(&m_iNumBuildingsGlobal, "iNumBuildingsGlobal");
	pXML->GetChildXmlValByName(&m_iNumPlotsRequired, "iNumPlotsRequired");
	pXML->GetChildXmlValByName(&m_iPlotType, "iPlotType");
	pXML->GetChildXmlValByName(&m_iOtherPlayerShareBorders, "iOtherPlayerShareBorders");
	pXML->GetChildXmlValByName(&m_iMinPopulation, "iMinPopulation");
	pXML->GetChildXmlValByName(&m_iMaxPopulation, "iMaxPopulation");
	pXML->GetChildXmlValByName(&m_iMinMapLandmass, "iMinMapLandmass");
	pXML->GetChildXmlValByName(&m_iMinOurLandmass, "iMinOurLandmass");
	pXML->GetChildXmlValByName(&m_iMaxOurLandmass, "iMaxOurLandmass");
	pXML->GetChildXmlValByName(szTextVal, "MinDifficulty");
	m_iMinDifficulty = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iUnitDamagedWeight, "iUnitDamagedWeight");
	pXML->GetChildXmlValByName(&m_iUnitDistanceWeight, "iUnitDistanceWeight");
	pXML->GetChildXmlValByName(&m_iUnitExperienceWeight, "iUnitExperienceWeight");
	pXML->GetChildXmlValByName(&m_iMinTreasury, "iMinTreasury");
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"UnitsRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiUnitsRequired.clear();
			if (0 < iNumSibs)
			{
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiUnitsRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(&szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"BuildingsRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiBuildingsRequired.clear();
			if (0 < iNumSibs)
			{
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiBuildingsRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(&szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	pXML->GetChildXmlValByName(szTextVal, "Civic");
	m_iCivic = pXML->FindInInfoClass(szTextVal);
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"Events"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiEvents.clear();
			if (0 < iNumSibs)
			{
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiEvents.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(&szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"PrereqEvents"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiPrereqEvents.clear();
			if (0 < iNumSibs)
			{
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j=0;j<iNumSibs;j++)
					{
						m_aiPrereqEvents.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(&szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"FeaturesRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiFeaturesRequired.clear();
			if (0 < iNumSibs)
			{
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiFeaturesRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(&szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"TerrainsRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiTerrainsRequired.clear();
			if (0 < iNumSibs)
			{
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiTerrainsRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(&szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"ImprovementsRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiImprovementsRequired.clear();
			if (0 < iNumSibs)
			{
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiImprovementsRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(&szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"RoutesRequired"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			m_aiRoutesRequired.clear();
			if (0 < iNumSibs)
			{
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j = 0; j < iNumSibs; j++)
					{
						m_aiRoutesRequired.push_back(pXML->FindInInfoClass(szTextVal));
						if (!pXML->GetNextXmlVal(&szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	m_aszText.clear();
	m_aiTextEra.clear();
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"TriggerTexts"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (0 < iNumSibs)
			{
				if (gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
				{
					for (int j = 0; j < iNumSibs; ++j)
					{
						if (pXML->GetChildXmlVal(szTextVal))
						{
							m_aszText.push_back(szTextVal);
							pXML->GetNextXmlVal(&szTextVal);
							m_aiTextEra.push_back(pXML->FindInInfoClass(szTextVal));
							gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
						}
						if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	m_aszWorldNews.clear();
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"WorldNewsTexts"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (0 < iNumSibs)
			{
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j=0; j<iNumSibs; ++j)
					{
						m_aszWorldNews.push_back(szTextVal);
						if (!pXML->GetNextXmlVal(&szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	pXML->GetChildXmlValByName(&m_bTutorial, "bTutorial");
	pXML->GetChildXmlValByName(&m_bSinglePlayer, "bSinglePlayer");
	pXML->GetChildXmlValByName(&m_bTeam, "bTeam");
	pXML->GetChildXmlValByName(&m_bRecurring, "bRecurring");
	pXML->GetChildXmlValByName(&m_bGlobal, "bGlobal");
	pXML->GetChildXmlValByName(&m_bPickPlayer, "bPickPlayer");
	pXML->GetChildXmlValByName(&m_bOtherPlayerWar, "bOtherPlayerWar");
	pXML->GetChildXmlValByName(&m_bOtherPlayerAI, "bOtherPlayerAI");
	pXML->GetChildXmlValByName(&m_bOtherPlayerNative, "bOtherPlayerNative");
	pXML->GetChildXmlValByName(&m_bOtherPlayerPlayable, "bOtherPlayerPlayable");
	pXML->GetChildXmlValByName(&m_bPickCity, "bPickCity");
	pXML->GetChildXmlValByName(&m_bPickOtherPlayerCity, "bPickOtherPlayerCity");
	pXML->GetChildXmlValByName(&m_bShowPlot, "bShowPlot");
	pXML->GetChildXmlValByName(&m_iCityFoodWeight, "iCityFoodWeight");
	pXML->GetChildXmlValByName(&m_bUnitsOnPlot, "bUnitsOnPlot");
	pXML->GetChildXmlValByName(&m_bOwnPlot, "bOwnPlot");
	pXML->GetChildXmlValByName(&m_bProbabilityUnitMultiply, "bProbabilityUnitMultiply");
	pXML->GetChildXmlValByName(&m_bProbabilityBuildingMultiply, "bProbabilityBuildingMultiply");
	pXML->GetChildXmlValByName(&m_bPrereqEventCity, "bPrereqEventPlot");
	pXML->GetChildXmlValByName(&m_bFrontPopup, "bFrontPopup");
	pXML->GetChildXmlValByName(m_szPythonCallback, "PythonCallback");
	pXML->GetChildXmlValByName(m_szPythonCanDo, "PythonCanDo");
	pXML->GetChildXmlValByName(m_szPythonCanDoCity, "PythonCanDoCity");
	pXML->GetChildXmlValByName(m_szPythonCanDoUnit, "PythonCanDoUnit");
	return true;
}
//////////////////////////////////////////////////////////////////////////
//
//	CvEventInfo
//	Events
//
//
CvEventInfo::CvEventInfo() :
	m_bQuest(false),
	m_bGlobal(false),
	m_bTeam(false),
	m_bCityEffect(false),
	m_bOtherPlayerCityEffect(false),
	m_bGoldToPlayer(false),
	m_bDeclareWar(false),
	m_bDisbandUnit(false),
	m_iGold(0),
	m_iRandomGold(0),
	m_iCulture(0),
	m_iUnitClass(NO_UNITCLASS),
	m_iNumUnits(0),
	m_iUnitExperience(0),
	m_iUnitImmobileTurns(0),
	m_iBuildingClass(NO_BUILDINGCLASS),
	m_iBuildingChange(0),
	m_iFood(0),
	m_iFoodPercent(0),
	m_iFeature(NO_FEATURE),
	m_iFeatureChange(0),
	m_iImprovement(NO_IMPROVEMENT),
	m_iImprovementChange(0),
	m_iRoute(NO_ROUTE),
	m_iRouteChange(0),
	m_iBonusRevealed(NO_BONUS),
	m_iOurAttitudeModifier(0),
	m_iAttitudeModifier(0),
	m_iTheirEnemyAttitudeModifier(0),
	m_iPopulationChange(0),
	m_iRevoltTurns(0),
	m_iMinPillage(0),
	m_iMaxPillage(0),
	m_iUnitPromotion(NO_PROMOTION),
	m_iAIValue(0),
	m_aiPlotExtraYields(NULL),
	m_aiAdditionalEventChance(NULL),
	m_aiAdditionalEventTime(NULL),
	m_aiClearEventChance(NULL),
	m_aiUnitCombatPromotions(NULL),
	m_aiUnitClassPromotions(NULL)
{
}
CvEventInfo::~CvEventInfo()
{
	SAFE_DELETE_ARRAY(m_aiPlotExtraYields);
	SAFE_DELETE_ARRAY(m_aiAdditionalEventChance);
	SAFE_DELETE_ARRAY(m_aiAdditionalEventTime);
	SAFE_DELETE_ARRAY(m_aiClearEventChance);
	SAFE_DELETE_ARRAY(m_aiUnitCombatPromotions);
	SAFE_DELETE_ARRAY(m_aiUnitClassPromotions);
}
bool CvEventInfo::isGlobal() const
{
	return m_bGlobal;
}
bool CvEventInfo::isQuest() const
{
	return m_bQuest;
}
bool CvEventInfo::isTeam() const
{
	return m_bTeam;
}
bool CvEventInfo::isCityEffect() const
{
	return m_bCityEffect;
}
bool CvEventInfo::isOtherPlayerCityEffect() const
{
	return m_bOtherPlayerCityEffect;
}
bool CvEventInfo::isGoldToPlayer() const
{
	return m_bGoldToPlayer;
}
bool CvEventInfo::isDeclareWar() const
{
	return m_bDeclareWar;
}
bool CvEventInfo::isDisbandUnit() const
{
	return m_bDisbandUnit;
}
int CvEventInfo::getGold() const
{
	return m_iGold;
}
int CvEventInfo::getRandomGold() const
{
	return m_iRandomGold;
}
int CvEventInfo::getCulture() const
{
	return m_iCulture;
}
int CvEventInfo::getUnitClass() const
{
	return m_iUnitClass;
}
int CvEventInfo::getNumUnits() const
{
	return m_iNumUnits;
}
int CvEventInfo::getUnitExperience() const
{
	return m_iUnitExperience;
}
int CvEventInfo::getUnitImmobileTurns() const
{
	return m_iUnitImmobileTurns;
}
int CvEventInfo::getBuildingClass() const
{
	return m_iBuildingClass;
}
int CvEventInfo::getBuildingChange() const
{
	return m_iBuildingChange;
}
int CvEventInfo::getFood() const
{
	return m_iFood;
}
int CvEventInfo::getFoodPercent() const
{
	return m_iFoodPercent;
}
int CvEventInfo::getFeature() const
{
	return m_iFeature;
}
int CvEventInfo::getFeatureChange() const
{
	return m_iFeatureChange;
}
int CvEventInfo::getImprovement() const
{
	return m_iImprovement;
}
int CvEventInfo::getImprovementChange() const
{
	return m_iImprovementChange;
}
int CvEventInfo::getRoute() const
{
	return m_iRoute;
}
int CvEventInfo::getRouteChange() const
{
	return m_iRouteChange;
}
int CvEventInfo::getBonusRevealed() const
{
	return m_iBonusRevealed;
}
int CvEventInfo::getOurAttitudeModifier() const
{
	return m_iOurAttitudeModifier;
}
int CvEventInfo::getAttitudeModifier() const
{
	return m_iAttitudeModifier;
}
int CvEventInfo::getTheirEnemyAttitudeModifier() const
{
	return m_iTheirEnemyAttitudeModifier;
}
int CvEventInfo::getPopulationChange() const
{
	return m_iPopulationChange;
}
int CvEventInfo::getRevoltTurns() const
{
	return m_iRevoltTurns;
}
int CvEventInfo::getMinPillage() const
{
	return m_iMinPillage;
}
int CvEventInfo::getMaxPillage() const
{
	return m_iMaxPillage;
}
int CvEventInfo::getUnitPromotion() const
{
	return m_iUnitPromotion;
}
int CvEventInfo::getAIValue() const
{
	return m_iAIValue;
}
int CvEventInfo::getAdditionalEventChance(int i) const
{
	FAssert (i >= 0 && i < GC.getNumEventInfos());
	return m_aiAdditionalEventChance ? m_aiAdditionalEventChance[i] : 0;
}
int CvEventInfo::getAdditionalEventTime(int i) const
{
	FAssert (i >= 0 && i < GC.getNumEventInfos());
	return m_aiAdditionalEventTime ? m_aiAdditionalEventTime[i] : 0;
}
int CvEventInfo::getClearEventChance(int i) const
{
	FAssert (i >= 0 && i < GC.getNumEventInfos());
	return m_aiClearEventChance ? m_aiClearEventChance[i] : 0;
}
int CvEventInfo::getPlotExtraYield(int i) const
{
	FAssertMsg(i < NUM_YIELD_TYPES, "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiPlotExtraYields ? m_aiPlotExtraYields[i] : -1;
}
int CvEventInfo::getUnitCombatPromotion(int i) const
{
	FAssertMsg(i < GC.getNumUnitCombatInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiUnitCombatPromotions ? m_aiUnitCombatPromotions[i] : -1;
}
int CvEventInfo::getUnitClassPromotion(int i) const
{
	FAssertMsg(i < GC.getNumUnitClassInfos(), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_aiUnitClassPromotions ? m_aiUnitClassPromotions[i] : -1;
}
const CvWString& CvEventInfo::getWorldNews(int i) const
{
	FAssert(i >= 0 && i < (int)m_aszWorldNews.size());
	return m_aszWorldNews[i];
}
int CvEventInfo::getNumWorldNews() const
{
	return m_aszWorldNews.size();
}
int CvEventInfo::getBuildingYieldChange(int iBuildingClass, int iYield) const
{
	for (std::vector<BuildingYieldChange>::const_iterator it = m_aBuildingYieldChanges.begin(); it != m_aBuildingYieldChanges.end(); ++it)
	{
		if ((*it).eBuildingClass == (BuildingClassTypes)iBuildingClass && (*it).eYield == (YieldTypes)iYield)
		{
			return (*it).iChange;
		}
	}
	return 0;
}
int CvEventInfo::getNumBuildingYieldChanges() const
{
	return m_aBuildingYieldChanges.size();
}
const char* CvEventInfo::getPythonCallback() const
{
	return m_szPythonCallback;
}
const char* CvEventInfo::getPythonExpireCheck() const
{
	return m_szPythonExpireCheck;
}
const char* CvEventInfo::getPythonCanDo() const
{
	return m_szPythonCanDo;
}
const char* CvEventInfo::getPythonHelp() const
{
	return m_szPythonHelp;
}
const wchar* CvEventInfo::getUnitNameKey() const
{
	return m_szUnitName;
}
const wchar* CvEventInfo::getQuestFailTextKey() const
{
	return m_szQuestFailText;
}
const wchar* CvEventInfo::getLocalInfoTextKey() const
{
	return m_szLocalInfoText;
}
const wchar* CvEventInfo::getOtherPlayerPopup() const
{
	return m_szOtherPlayerPopup;
}
void CvEventInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);
	uint uiFlag=0;
	stream->Read(&uiFlag);	// flags for expansion
	stream->Read(&m_bQuest);
	stream->Read(&m_bGlobal);
	stream->Read(&m_bTeam);
	stream->Read(&m_bCityEffect);
	stream->Read(&m_bOtherPlayerCityEffect);
	stream->Read(&m_bGoldToPlayer);
	stream->Read(&m_bDeclareWar);
	stream->Read(&m_bDisbandUnit);
	stream->Read(&m_iGold);
	stream->Read(&m_iRandomGold);
	stream->Read(&m_iCulture);
	stream->Read(&m_iUnitClass);
	stream->Read(&m_iNumUnits);
	stream->Read(&m_iUnitExperience);
	stream->Read(&m_iUnitImmobileTurns);
	stream->Read(&m_iBuildingClass);
	stream->Read(&m_iBuildingChange);
	stream->Read(&m_iFood);
	stream->Read(&m_iFoodPercent);
	stream->Read(&m_iFeature);
	stream->Read(&m_iFeatureChange);
	stream->Read(&m_iImprovement);
	stream->Read(&m_iImprovementChange);
	stream->Read(&m_iRoute);
	stream->Read(&m_iRouteChange);
	stream->Read(&m_iBonusRevealed);
	stream->Read(&m_iOurAttitudeModifier);
	stream->Read(&m_iAttitudeModifier);
	stream->Read(&m_iTheirEnemyAttitudeModifier);
	stream->Read(&m_iPopulationChange);
	stream->Read(&m_iRevoltTurns);
	stream->Read(&m_iMinPillage);
	stream->Read(&m_iMaxPillage);
	stream->Read(&m_iUnitPromotion);
	stream->Read(&m_iAIValue);
	SAFE_DELETE_ARRAY(m_aiPlotExtraYields);
	m_aiPlotExtraYields = new int[NUM_YIELD_TYPES];
	stream->Read(NUM_YIELD_TYPES, m_aiPlotExtraYields);
	SAFE_DELETE_ARRAY(m_aiAdditionalEventChance);
	m_aiAdditionalEventChance = new int[GC.getNumEventInfos()];
	stream->Read(GC.getNumEventInfos(), m_aiAdditionalEventChance);
	SAFE_DELETE_ARRAY(m_aiAdditionalEventTime);
	m_aiAdditionalEventTime = new int[GC.getNumEventInfos()];
	stream->Read(GC.getNumEventInfos(), m_aiAdditionalEventTime);
	SAFE_DELETE_ARRAY(m_aiClearEventChance);
	m_aiClearEventChance = new int[GC.getNumEventInfos()];
	stream->Read(GC.getNumEventInfos(), m_aiClearEventChance);
	SAFE_DELETE_ARRAY(m_aiUnitCombatPromotions);
	m_aiUnitCombatPromotions = new int[GC.getNumUnitCombatInfos()];
	stream->Read(GC.getNumUnitCombatInfos(), m_aiUnitCombatPromotions);
	SAFE_DELETE_ARRAY(m_aiUnitClassPromotions);
	m_aiUnitClassPromotions = new int[GC.getNumUnitClassInfos()];
	stream->Read(GC.getNumUnitClassInfos(), m_aiUnitClassPromotions);
	int iNumElements;
	CvWString szText;
	stream->Read(&iNumElements);
	m_aszWorldNews.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		stream->ReadString(szText);
		m_aszWorldNews.push_back(szText);
	}
	stream->Read(&iNumElements);
	m_aBuildingYieldChanges.clear();
	for (int i = 0; i < iNumElements; ++i)
	{
		BuildingYieldChange kChange;
		kChange.read(stream);
		m_aBuildingYieldChanges.push_back(kChange);
	}
	stream->ReadString(m_szUnitName);
	stream->ReadString(m_szOtherPlayerPopup);
	stream->ReadString(m_szQuestFailText);
	stream->ReadString(m_szLocalInfoText);
	stream->ReadString(m_szPythonCallback);
	stream->ReadString(m_szPythonExpireCheck);
	stream->ReadString(m_szPythonCanDo);
	stream->ReadString(m_szPythonHelp);
}
void CvEventInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);
	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_bQuest);
	stream->Write(m_bGlobal);
	stream->Write(m_bTeam);
	stream->Write(m_bCityEffect);
	stream->Write(m_bOtherPlayerCityEffect);
	stream->Write(m_bGoldToPlayer);
	stream->Write(m_bDeclareWar);
	stream->Write(m_bDisbandUnit);
	stream->Write(m_iGold);
	stream->Write(m_iRandomGold);
	stream->Write(m_iCulture);
	stream->Write(m_iUnitClass);
	stream->Write(m_iNumUnits);
	stream->Write(m_iUnitExperience);
	stream->Write(m_iUnitImmobileTurns);
	stream->Write(m_iBuildingClass);
	stream->Write(m_iBuildingChange);
	stream->Write(m_iFood);
	stream->Write(m_iFoodPercent);
	stream->Write(m_iFeature);
	stream->Write(m_iFeatureChange);
	stream->Write(m_iImprovement);
	stream->Write(m_iImprovementChange);
	stream->Write(m_iRoute);
	stream->Write(m_iRouteChange);
	stream->Write(m_iBonusRevealed);
	stream->Write(m_iOurAttitudeModifier);
	stream->Write(m_iAttitudeModifier);
	stream->Write(m_iTheirEnemyAttitudeModifier);
	stream->Write(m_iPopulationChange);
	stream->Write(m_iRevoltTurns);
	stream->Write(m_iMinPillage);
	stream->Write(m_iMaxPillage);
	stream->Write(m_iUnitPromotion);
	stream->Write(m_iAIValue);
	stream->Write(NUM_YIELD_TYPES, m_aiPlotExtraYields);
	stream->Write(GC.getNumEventInfos(), m_aiAdditionalEventChance);
	stream->Write(GC.getNumEventInfos(), m_aiAdditionalEventTime);
	stream->Write(GC.getNumEventInfos(), m_aiClearEventChance);
	stream->Write(GC.getNumUnitCombatInfos(), m_aiUnitCombatPromotions);
	stream->Write(GC.getNumUnitClassInfos(), m_aiUnitClassPromotions);
	stream->Write(m_aszWorldNews.size());
	for (std::vector<CvWString>::iterator it = m_aszWorldNews.begin(); it != m_aszWorldNews.end(); ++it)
	{
		stream->WriteString(*it);
	}
	stream->Write(m_aBuildingYieldChanges.size());
	for (std::vector<BuildingYieldChange>::iterator it = m_aBuildingYieldChanges.begin(); it != m_aBuildingYieldChanges.end(); ++it)
	{
		(*it).write(stream);
	}
	stream->WriteString(m_szUnitName);
	stream->WriteString(m_szOtherPlayerPopup);
	stream->WriteString(m_szQuestFailText);
	stream->WriteString(m_szLocalInfoText);
	stream->WriteString(m_szPythonCallback);
	stream->WriteString(m_szPythonExpireCheck);
	stream->WriteString(m_szPythonCanDo);
	stream->WriteString(m_szPythonHelp);
}
bool CvEventInfo::read(CvXMLLoadUtility* pXML)
{
	CvString szTextVal;
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(&m_bQuest, "bQuest");
	pXML->GetChildXmlValByName(&m_bGlobal, "bGlobal");
	pXML->GetChildXmlValByName(&m_bTeam, "bTeam");
	pXML->GetChildXmlValByName(&m_bCityEffect, "bPickCity");
	pXML->GetChildXmlValByName(&m_bOtherPlayerCityEffect, "bPickOtherPlayerCity");
	pXML->GetChildXmlValByName(&m_bGoldToPlayer, "bGoldToPlayer");
	pXML->GetChildXmlValByName(&m_bDeclareWar, "bDeclareWar");
	pXML->GetChildXmlValByName(&m_iGold, "iGold");
	pXML->GetChildXmlValByName(&m_iRandomGold, "iRandomGold");
	pXML->GetChildXmlValByName(&m_iCulture, "iCulture");
	pXML->GetChildXmlValByName(szTextVal, "UnitClass");
	m_iUnitClass = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iNumUnits, "iNumFreeUnits");
	pXML->GetChildXmlValByName(&m_bDisbandUnit, "bDisbandUnit");
	pXML->GetChildXmlValByName(&m_iUnitExperience, "iUnitExperience");
	pXML->GetChildXmlValByName(&m_iUnitImmobileTurns, "iUnitImmobileTurns");
	pXML->GetChildXmlValByName(szTextVal, "BuildingClass");
	m_iBuildingClass = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iBuildingChange, "iBuildingChange");
	pXML->GetChildXmlValByName(&m_iFood, "iFood");
	pXML->GetChildXmlValByName(&m_iFoodPercent, "iFoodPercent");
	pXML->GetChildXmlValByName(szTextVal, "FeatureType");
	m_iFeature = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iFeatureChange, "iFeatureChange");
	pXML->GetChildXmlValByName(szTextVal, "ImprovementType");
	m_iImprovement = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iImprovementChange, "iImprovementChange");
	pXML->GetChildXmlValByName(szTextVal, "RouteType");
	m_iRoute = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iRouteChange, "iRouteChange");
	pXML->GetChildXmlValByName(szTextVal, "BonusRevealed");
	m_iBonusRevealed = pXML->FindInInfoClass(szTextVal);
	pXML->SetVariableListTagPair(&m_aiPlotExtraYields, "PlotExtraYields", NUM_YIELD_TYPES, 0);
	pXML->GetChildXmlValByName(&m_iOurAttitudeModifier, "iOurAttitudeModifier");
	pXML->GetChildXmlValByName(&m_iAttitudeModifier, "iAttitudeModifier");
	pXML->GetChildXmlValByName(&m_iTheirEnemyAttitudeModifier, "iTheirEnemyAttitudeModifier");
	pXML->GetChildXmlValByName(&m_iPopulationChange, "iPopulationChange");
	pXML->GetChildXmlValByName(&m_iRevoltTurns, "iRevoltTurns");
	pXML->GetChildXmlValByName(&m_iMinPillage, "iMinPillage");
	pXML->GetChildXmlValByName(&m_iMaxPillage, "iMaxPillage");
	pXML->GetChildXmlValByName(szTextVal, "UnitPromotion");
	m_iUnitPromotion = pXML->FindInInfoClass(szTextVal);
	pXML->GetChildXmlValByName(&m_iAIValue, "iAIValue");
	CvString* pszPromotions = NULL;
	FAssertMsg(NULL == m_aiUnitCombatPromotions, "Memory leak");
	m_aiUnitCombatPromotions = new int[GC.getNumUnitCombatInfos()];
	pXML->SetVariableListTagPair<CvString>(&pszPromotions, "UnitCombatPromotions", GC.getNumUnitCombatInfos(), "NONE");
	for (int i = 0; i < GC.getNumUnitCombatInfos(); ++i)
	{
		m_aiUnitCombatPromotions[i] = pXML->FindInInfoClass(pszPromotions[i]);
	}
	SAFE_DELETE_ARRAY(pszPromotions);
	FAssertMsg(NULL == m_aiUnitClassPromotions, "Memory leak");
	m_aiUnitClassPromotions = new int[GC.getNumUnitClassInfos()];
	pXML->SetVariableListTagPair<CvString>(&pszPromotions, "UnitClassPromotions", GC.getNumUnitClassInfos(), "NONE");
	for (int i = 0; i < GC.getNumUnitClassInfos(); ++i)
	{
		m_aiUnitClassPromotions[i] = pXML->FindInInfoClass(pszPromotions[i]);
	}
	SAFE_DELETE_ARRAY(pszPromotions);
	pXML->GetChildXmlValByName(m_szUnitName, "UnitName");
	pXML->GetChildXmlValByName(m_szOtherPlayerPopup, "OtherPlayerPopup");
	pXML->GetChildXmlValByName(m_szQuestFailText, "QuestFailText");
	pXML->GetChildXmlValByName(m_szLocalInfoText, "LocalInfoText");
	pXML->GetChildXmlValByName(m_szPythonCallback, "PythonCallback");
	pXML->GetChildXmlValByName(m_szPythonExpireCheck, "PythonExpireCheck");
	pXML->GetChildXmlValByName(m_szPythonCanDo, "PythonCanDo");
	pXML->GetChildXmlValByName(m_szPythonHelp, "PythonHelp");
	m_aszWorldNews.clear();
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"WorldNewsTexts"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (0 < iNumSibs)
			{
				if (pXML->GetChildXmlVal(szTextVal))
				{
					for (int j=0; j<iNumSibs; ++j)
					{
						m_aszWorldNews.push_back(szTextVal);
						if (!pXML->GetNextXmlVal(&szTextVal))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	m_aBuildingYieldChanges.clear();
	if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(),"BuildingExtraYields"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			if (0 < iNumSibs)
			{
				if (gDLL->getXMLIFace()->SetToChild(pXML->GetXML()))
				{
					for (int j = 0; j < iNumSibs; ++j)
					{
						if (pXML->GetChildXmlVal(szTextVal))
						{
							BuildingYieldChange kChange;
							kChange.eBuildingClass = (BuildingClassTypes)pXML->FindInInfoClass(szTextVal);
							pXML->GetNextXmlVal(&szTextVal);
							kChange.eYield = (YieldTypes)pXML->FindInInfoClass(szTextVal);
							pXML->GetNextXmlVal(&kChange.iChange);
							m_aBuildingYieldChanges.push_back(kChange);
							gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
						}
						if (!gDLL->getXMLIFace()->NextSibling(pXML->GetXML()))
						{
							break;
						}
					}
					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}
	return true;
}
bool CvEventInfo::readPass2(CvXMLLoadUtility* pXML)
{
	pXML->SetVariableListTagPair(&m_aiAdditionalEventChance, "AdditionalEvents", GC.getNumEventInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiAdditionalEventTime, "EventTimes", GC.getNumEventInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiClearEventChance, "ClearEvents", GC.getNumEventInfos(), 0);
	return true;
}
CvMainMenuInfo::CvMainMenuInfo()
{
}
CvMainMenuInfo::~CvMainMenuInfo()
{
}
std::string CvMainMenuInfo::getScene() const
{
	return m_szScene;
}
std::string CvMainMenuInfo::getSoundtrack() const
{
	return m_szSoundtrack;
}
std::string CvMainMenuInfo::getLoading() const
{
	return m_szLoading;
}
std::string CvMainMenuInfo::getLoadingSlideshow() const
{
	return m_szLoadingSlideshow;
}

bool CvMainMenuInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}
	pXML->GetChildXmlValByName(m_szScene, "Scene");
	pXML->GetChildXmlValByName(m_szSoundtrack, "Soundtrack");
	pXML->GetChildXmlValByName(m_szLoading, "Loading");
	pXML->GetChildXmlValByName(m_szLoadingSlideshow, "LoadingSlideshow");
	return true;
}

CvFatherInfo::CvFatherInfo() :
	m_iFatherCategory(NO_FATHERCATEGORY),
	m_iTrait(NO_TRAIT),
	m_aiFreeUnits(NULL),
	m_aiPointCost(NULL),
	m_abRevealImprovement(NULL)
{
}

CvFatherInfo::~CvFatherInfo()
{
	SAFE_DELETE_ARRAY(m_aiFreeUnits);
	SAFE_DELETE_ARRAY(m_aiPointCost);
	SAFE_DELETE_ARRAY(m_abRevealImprovement);
}

int CvFatherInfo::getFatherCategory() const
{
	return m_iFatherCategory;
}

int CvFatherInfo::getTrait() const
{
	return m_iTrait;
}

int CvFatherInfo::getFreeUnits(int iUnitClass) const
{
	FAssert(iUnitClass >= 0 && iUnitClass < GC.getNumUnitClassInfos());
	return m_aiFreeUnits ? m_aiFreeUnits[iUnitClass] : -1;
}

int CvFatherInfo::getPointCost(int i) const
{
	FAssert((i >= 0) && (i < GC.getNumFatherPointInfos()));
	return m_aiPointCost ? m_aiPointCost[i] : -1;
}

bool CvFatherInfo::isRevealImprovement(int iImprovement) const
{
	FAssert(iImprovement >= 0 && iImprovement < GC.getNumImprovementInfos());
	return m_abRevealImprovement[iImprovement];
}

const char* CvFatherInfo::getPortrait() const
{
	return m_szPortrait;
}

const wchar* CvFatherInfo::getQuoteKey()
{
	return m_szQuoteKey;
}

const char* CvFatherInfo::getSound() const
{
	return m_szSound;
}

const char* CvFatherInfo::getSoundMP() const
{
	return m_szSoundMP;
}

void CvFatherInfo::read(FDataStreamBase* stream)
{
	CvInfoBase::read(stream);

	uint uiFlag=0;
	stream->Read(&uiFlag);	// flags for expansion
	stream->Read(&m_iFatherCategory);
	stream->Read(&m_iTrait);

	SAFE_DELETE_ARRAY(m_aiFreeUnits);
	m_aiFreeUnits = new int [GC.getNumUnitClassInfos()];
	stream->Read(GC.getNumUnitClassInfos(), m_aiFreeUnits);

	SAFE_DELETE_ARRAY(m_aiPointCost);
	m_aiPointCost = new int [GC.getNumFatherPointInfos()];
	stream->Read(GC.getNumFatherPointInfos(), m_aiPointCost);

	SAFE_DELETE_ARRAY(m_abRevealImprovement);
	m_abRevealImprovement = new bool [GC.getNumImprovementInfos()];
	stream->Read(GC.getNumImprovementInfos(), m_abRevealImprovement);

	stream->ReadString(m_szQuoteKey);
	stream->ReadString(m_szSound);
	stream->ReadString(m_szSoundMP);
	stream->ReadString(m_szPortrait);
}

void CvFatherInfo::write(FDataStreamBase* stream)
{
	CvInfoBase::write(stream);

	uint uiFlag=0;
	stream->Write(uiFlag);		// flag for expansion
	stream->Write(m_iFatherCategory);
	stream->Write(m_iTrait);
	stream->Write(GC.getNumUnitClassInfos(), m_aiFreeUnits);
	stream->Write(GC.getNumFatherPointInfos(), m_aiPointCost);
	stream->Write(GC.getNumImprovementInfos(), m_abRevealImprovement);
	stream->WriteString(m_szQuoteKey);
	stream->WriteString(m_szSound);
	stream->WriteString(m_szSoundMP);
	stream->WriteString(m_szPortrait);
}

bool CvFatherInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}

	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "FatherCategory");
	m_iFatherCategory = GC.getInfoTypeForString(szTextVal);

	pXML->GetChildXmlValByName(m_szPortrait, "Portrait");
	pXML->GetChildXmlValByName(szTextVal, "Trait");
	m_iTrait = GC.getInfoTypeForString(szTextVal);

	pXML->SetVariableListTagPair(&m_aiFreeUnits, "FreeUnits", GC.getNumUnitClassInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiPointCost, "FatherPointCosts", GC.getNumFatherPointInfos(), 0);
	pXML->SetVariableListTagPair(&m_abRevealImprovement, "RevealImprovements", GC.getNumImprovementInfos(), false);

	pXML->GetChildXmlValByName(m_szQuoteKey, "Quote");
	pXML->GetChildXmlValByName(m_szSound, "Sound");
	pXML->GetChildXmlValByName(m_szSoundMP, "SoundMP");
	return true;
}

CvFatherPointInfo::CvFatherPointInfo() :
	m_iChar(0),
	m_iFontButtonIndex(0),
	m_iLandTilePoints(0),
	m_iWaterTilePoints(0),
	m_iMeetNativePoints(0),
	m_iScoutVillagePoints(0),
	m_iGoodyPoints(0),
	m_iExperiencePoints(0),
	m_iConquerCityPoints(0),
	m_iRazeCityPoints(0),
	m_iMissionaryPoints(0),
	m_iProductionConversionPoints(0),
	m_iEuropeTradeGoldPointPercent(0),
	m_iNativeTradeGoldPointPercent(0),
	m_aiBuildingPoints(NULL),
	m_aiYieldPoints(NULL)
{
}

CvFatherPointInfo::~CvFatherPointInfo()
{
	SAFE_DELETE_ARRAY(m_aiBuildingPoints);
	SAFE_DELETE_ARRAY(m_aiYieldPoints);
}

int CvFatherPointInfo::getChar() const
{
	return m_iChar;
}

void CvFatherPointInfo::setChar(int i)
{
	m_iChar = i;
}

int CvFatherPointInfo::getFontButtonIndex() const
{
	return m_iFontButtonIndex;
}

int CvFatherPointInfo::getLandTilePoints() const
{
	return m_iLandTilePoints;
}

int CvFatherPointInfo::getWaterTilePoints() const
{
	return m_iWaterTilePoints;
}

int CvFatherPointInfo::getMeetNativePoints() const
{
	return m_iMeetNativePoints;
}

int CvFatherPointInfo::getScoutVillagePoints() const
{
	return m_iScoutVillagePoints;
}

int CvFatherPointInfo::getGoodyPoints() const
{
	return m_iGoodyPoints;
}

int CvFatherPointInfo::getExperiencePoints() const
{
	return m_iExperiencePoints;
}

int CvFatherPointInfo::getConquerCityPoints() const
{
	return m_iConquerCityPoints;
}

int CvFatherPointInfo::getRazeCityPoints() const
{
	return m_iRazeCityPoints;
}

int CvFatherPointInfo::getMissionaryPoints() const
{
	return m_iMissionaryPoints;
}

int CvFatherPointInfo::getProductionConversionPoints() const
{
	return m_iProductionConversionPoints;
}

int CvFatherPointInfo::getEuropeTradeGoldPointPercent() const
{
	return m_iEuropeTradeGoldPointPercent;
}

int CvFatherPointInfo::getNativeTradeGoldPointPercent() const
{
	return m_iNativeTradeGoldPointPercent;
}

int CvFatherPointInfo::getBuildingPoints(int iBuildingClass) const
{
	FAssert(iBuildingClass >= 0 && iBuildingClass < GC.getNumBuildingClassInfos());
	return m_aiBuildingPoints[iBuildingClass];
}

int CvFatherPointInfo::getYieldPoints(int iYield) const
{
	FAssert(iYield >= 0 && iYield < NUM_YIELD_TYPES);
	return m_aiYieldPoints[iYield];
}

bool CvFatherPointInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}

	pXML->GetChildXmlValByName(&m_iFontButtonIndex, "iFontButtonIndex");
	pXML->GetChildXmlValByName(&m_iLandTilePoints, "iLandTilePoints");
	pXML->GetChildXmlValByName(&m_iWaterTilePoints, "iWaterTilePoints");
	pXML->GetChildXmlValByName(&m_iMeetNativePoints, "iMeetNativePoints");
	pXML->GetChildXmlValByName(&m_iScoutVillagePoints, "iScoutVillagePoints");
	pXML->GetChildXmlValByName(&m_iGoodyPoints, "iGoodyPoints");
	pXML->GetChildXmlValByName(&m_iExperiencePoints, "iExperiencePoints");
	pXML->GetChildXmlValByName(&m_iConquerCityPoints, "iConquerCityPoints");
	pXML->GetChildXmlValByName(&m_iRazeCityPoints, "iRazeCityPoints");
	pXML->GetChildXmlValByName(&m_iMissionaryPoints, "iMissionaryPoints");
	pXML->GetChildXmlValByName(&m_iProductionConversionPoints, "iProductionConversionPoints");
	pXML->GetChildXmlValByName(&m_iEuropeTradeGoldPointPercent, "iEuropeTradeGoldPointPercent");
	pXML->GetChildXmlValByName(&m_iNativeTradeGoldPointPercent, "iNativeTradeGoldPointPercent");

	pXML->SetVariableListTagPair(&m_aiBuildingPoints, "BuildingPoints", GC.getNumBuildingClassInfos(), 0);
	pXML->SetVariableListTagPair(&m_aiYieldPoints, "YieldPoints", NUM_YIELD_TYPES, 0);

	return true;
}

CvAlarmInfo::CvAlarmInfo() :
	m_iRange(0),
	m_iColony(0),
	m_iNumColonies(0),
	m_iPopulation(0),
	m_iUnit(0),
	m_iMissionary(0),
	m_iAttitudeDivisor(0)
{

}

CvAlarmInfo::~CvAlarmInfo()
{

}

int CvAlarmInfo::getRange() const
{
	return m_iRange;
}

int CvAlarmInfo::getColony() const
{
	return m_iColony;
}

int CvAlarmInfo::getNumColonies() const
{
	return m_iNumColonies;
}

int CvAlarmInfo::getPopulation() const
{
	return m_iPopulation;
}

int CvAlarmInfo::getUnit() const
{
	return m_iUnit;
}

int CvAlarmInfo::getMissionary() const
{
	return m_iMissionary;
}

int CvAlarmInfo::getAttitudeDivisor() const
{
	return m_iAttitudeDivisor;
}

bool CvAlarmInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
	{
		return false;
	}

	pXML->GetChildXmlValByName(&m_iRange, "iRange");
	pXML->GetChildXmlValByName(&m_iColony, "iColony");
	pXML->GetChildXmlValByName(&m_iNumColonies, "iNumColonies");
	pXML->GetChildXmlValByName(&m_iPopulation, "iPopulation");
	pXML->GetChildXmlValByName(&m_iUnit, "iUnit");
	pXML->GetChildXmlValByName(&m_iMissionary, "iMissionary");
	pXML->GetChildXmlValByName(&m_iAttitudeDivisor, "iAttitudeDivisor");

	return true;
}
