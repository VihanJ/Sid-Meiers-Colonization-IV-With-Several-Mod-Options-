#include "CvGameCoreDLL.h"
#include "CvTradeRoute.h"
#include "CvDLLInterfaceIFaceBase.h"

CvTradeRoute::CvTradeRoute() :
	m_iId(ANYWHERE_CITY_ID),
	// < JTradeRoutes Mod Start >
	m_szName(L""),
	m_eOwner(NO_PLAYER),
	// < JTradeRoutes Mod End >
	m_eYield(NO_YIELD)
{

}

CvTradeRoute::~CvTradeRoute()
{

}

void CvTradeRoute::init(const IDInfo& kSourceCity, const IDInfo& kDestinationCity, YieldTypes eYield)
{
	m_kSourceCity = kSourceCity;
	m_kDestinationCity = kDestinationCity;
	m_eYield = eYield;
}

int CvTradeRoute::getID() const
{
	return m_iId;
}

void CvTradeRoute::setID(int iId)
{
	m_iId = iId;
}

const IDInfo& CvTradeRoute::getSourceCity() const
{
	return m_kSourceCity;
}

void CvTradeRoute::setSourceCity(const IDInfo& kCity)
{
	if (getSourceCity() != kCity)
	{
		setActiveDirty();
		const IDInfo& kOldCity = getSourceCity();

		m_kSourceCity = kCity;

		CvCity* pCity = ::getCity(getSourceCity());
		FAssert(pCity != NULL);
		if (pCity != NULL)
		{
			pCity->updateExport(getYield());
		}

		pCity = ::getCity(kOldCity);
		FAssert(pCity != NULL);
		if (pCity != NULL)
		{
			pCity->updateExport(getYield());
		}

		setActiveDirty();
	}
}

const wchar* CvTradeRoute::getSourceCityNameKey() const
{
	if (getSourceCity().iID == EUROPE_CITY_ID)
	{
		return L"TXT_KEY_CONCEPT_EUROPE";
	}

	CvCity* pCity = ::getCity(getSourceCity());
	FAssert(pCity != NULL);
	if (pCity != NULL)
	{
		return pCity->getNameKey();
	}

	return L"";
}

const IDInfo& CvTradeRoute::getDestinationCity() const
{
	return m_kDestinationCity;
}

void CvTradeRoute::setDestinationCity(const IDInfo& kCity)
{
	if (getDestinationCity() != kCity)
	{
		setActiveDirty();
		const IDInfo& kOldCity = getDestinationCity();

		m_kDestinationCity = kCity;

		CvCity* pCity = ::getCity(getDestinationCity());
		FAssert(pCity != NULL || getDestinationCity().iID == EUROPE_CITY_ID);
		if (pCity != NULL)
		{
			pCity->updateImport(getYield());
		}

		pCity = ::getCity(kOldCity);
		FAssert(pCity != NULL || getDestinationCity().iID == EUROPE_CITY_ID);
		if (pCity != NULL)
		{
			pCity->updateImport(getYield());
		}

		setActiveDirty();
	}
}

const wchar* CvTradeRoute::getDestinationCityNameKey() const
{
	if (getDestinationCity().iID == EUROPE_CITY_ID)
	{
		return L"TXT_KEY_CONCEPT_EUROPE";
	}

	CvCity* pCity = ::getCity(getDestinationCity());
	FAssert(pCity != NULL);
	if (pCity != NULL)
	{
		return pCity->getNameKey();
	}

	return L"";
}


YieldTypes CvTradeRoute::getYield() const
{
	return m_eYield;
}

void CvTradeRoute::setYield(YieldTypes eYield)
{
	if (getYield() != eYield)
	{
		YieldTypes  eOldYield = getYield();

		m_eYield = eYield;

		CvCity* pCity = ::getCity(getDestinationCity());
		FAssert(pCity != NULL);
		if (pCity != NULL)
		{
			pCity->updateImport(getYield());
			pCity->updateImport(eOldYield);
		}

		pCity = ::getCity(getSourceCity());
		FAssert(pCity != NULL);
		if (pCity != NULL)
		{
			pCity->updateExport(getYield());
			pCity->updateExport(eOldYield);
		}

		setActiveDirty();
	}
}

bool CvTradeRoute::checkValid(PlayerTypes ePlayer) const
{
	CvPlayer& kPlayer = GET_PLAYER(ePlayer);

	if (!kPlayer.canLoadYield(getSourceCity().eOwner))
	{
		return false;
	}

	if (!kPlayer.canLoadYield(getDestinationCity().eOwner))
	{
		return false;
	}

	if (getDestinationCity().iID == EUROPE_CITY_ID)
	{
		if (!kPlayer.isYieldEuropeTradable(getYield()))
		{
			return false;
		}
	}

	return true;
}


void CvTradeRoute::read(FDataStreamBase* pStream)
{
	uint uiFlag = 0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iId);
	// < JTradeRoutes Mod Start >
	pStream->ReadString(m_szName);
	pStream->Read((int*) &m_eOwner);
	// < JTradeRoutes Mod End >
	m_kSourceCity.read(pStream);
	m_kDestinationCity.read(pStream);
	pStream->Read((int*) &m_eYield);
}

void CvTradeRoute::write(FDataStreamBase* pStream)
{
	uint uiFlag = 0;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iId);
	// < JTradeRoutes Mod Start >
	pStream->WriteString(m_szName);
	pStream->Write(m_eOwner);
	// < JTradeRoutes Mod End >
	m_kSourceCity.write(pStream);
	m_kDestinationCity.write(pStream);
	pStream->Write(m_eYield);
}

void CvTradeRoute::setActiveDirty()
{
	if (getDestinationCity().eOwner == GC.getGameINLINE().getActivePlayer())
	{
		gDLL->getInterfaceIFace()->setDirty(Domestic_Advisor_DIRTY_BIT, true);
	}

	if (getSourceCity().eOwner == GC.getGameINLINE().getActivePlayer())
	{
		gDLL->getInterfaceIFace()->setDirty(Domestic_Advisor_DIRTY_BIT, true);
	}
}

// < JTradeRoutes Mod Start >
const CvWString& CvTradeRoute::getName() const
{
    return m_szName;
}

void CvTradeRoute::setName(CvWString szNewValue)
{
	gDLL->stripSpecialCharacters(szNewValue);
	m_szName = szNewValue;
}


PlayerTypes CvTradeRoute::getOwner() const
{
    return m_eOwner;
}

void CvTradeRoute::setOwner(PlayerTypes ePlayer)
{
    if (getOwner() != ePlayer)
    {
        m_eOwner = ePlayer;
    }
}


int CvTradeRoute::getEuropeCityID() const
{
    return EUROPE_CITY_ID;
}

int CvTradeRoute::getAnywhereCityID() const
{
    return ANYWHERE_CITY_ID;
}

int CvTradeRoute::getNoCityID() const
{
    return NO_CITY_ID;
}


bool CvTradeRoute::isSourceEurope() const
{
    if (getSourceCity().iID == EUROPE_CITY_ID)
	{
		return true;
	}
	return false;
}

bool CvTradeRoute::isDestinationEurope() const
{
    if (getDestinationCity().iID == EUROPE_CITY_ID)
	{
		return true;
	}
	return false;
}


bool CvTradeRoute::isLandRoute() const
{
    if (!isSourceEurope() && !isDestinationEurope())
    {
        CvCity* pSourceCity = ::getCity(getSourceCity());
        CvCity* pDestinationCity = ::getCity(getDestinationCity());
        if (pSourceCity->area()->getID() == pDestinationCity->area()->getID())
        {
            return true;
        }
    }
    return false;
}

bool CvTradeRoute::isSeaRoute() const
{
    if (isSourceEurope() || isDestinationEurope())
    {
        return true;
    }
    CvCity* pSourceCity = ::getCity(getSourceCity());
    CvCity* pDestinationCity = ::getCity(getDestinationCity());
    if (pSourceCity->area()->getID() != pDestinationCity->area()->getID())
    {
        return true;
    }
    CvPlot* pLoopPlot;
	int iI, iJ;
	int aiDestinationAreaIDs[NUM_CARDINALDIRECTION_TYPES];

	for (iI = 0; iI < NUM_CARDINALDIRECTION_TYPES; ++iI)
	{
		pLoopPlot = plotCardinalDirection(pDestinationCity->getX_INLINE(), pDestinationCity->getY_INLINE(), ((CardinalDirectionTypes)iI));

		if (pLoopPlot != NULL)
		{
			if (pLoopPlot->isWater())
			{
			    aiDestinationAreaIDs[iI] = pLoopPlot->area()->getID();
			}
			else
			{
                aiDestinationAreaIDs[iI] = -1;
			}
		}
	}

	bool bWaterConnected = false;
	for (iI = 0; iI < NUM_CARDINALDIRECTION_TYPES; ++iI)
	{
		pLoopPlot = plotCardinalDirection(pSourceCity->getX_INLINE(), pSourceCity->getY_INLINE(), ((CardinalDirectionTypes)iI));

		if (pLoopPlot != NULL)
		{
			if (!pLoopPlot->isWater())
			{
			    continue;
			}
			for (iJ = 0; iJ < NUM_CARDINALDIRECTION_TYPES; ++iJ)
            {
                if (aiDestinationAreaIDs[iJ] < 0)
                {
                    continue;
                }
                else if (aiDestinationAreaIDs[iJ] == pLoopPlot->area()->getID())
                {
                    bWaterConnected = true;
                    break;
                }
            }
		}
        if (bWaterConnected)
        {
            break;
        }
	}
    return bWaterConnected;
}
// < JTradeRoutes Mod End >
