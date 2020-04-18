#include "CvGameCoreDLL.h"
#include "CyTradeRoute.h"
#include "CvTradeRoute.h"
#include "CyCity.h"


CyTradeRoute::CyTradeRoute() :
m_pTradeRoute(NULL)
{
}

CyTradeRoute::CyTradeRoute(CvTradeRoute* pTradeRoute) :
	m_pTradeRoute(pTradeRoute)
{
}

int CyTradeRoute::getID() const
{
	return m_pTradeRoute ? m_pTradeRoute->getID() : -1;
}

IDInfo CyTradeRoute::getSourceCity() const
{
	return (m_pTradeRoute ? m_pTradeRoute->getSourceCity() : IDInfo());
}

IDInfo CyTradeRoute::getDestinationCity() const
{
	return (m_pTradeRoute ? m_pTradeRoute->getDestinationCity() : IDInfo());
}

std::wstring CyTradeRoute::getSourceCityNameKey() const
{
	return (m_pTradeRoute ? m_pTradeRoute->getSourceCityNameKey() : L"");
}

std::wstring CyTradeRoute::getDestinationCityNameKey() const
{
	return (m_pTradeRoute ? m_pTradeRoute->getDestinationCityNameKey() : L"");
}

std::wstring CyTradeRoute::getSourceCityName() const
{
	return gDLL->getObjectText(m_pTradeRoute ? m_pTradeRoute->getSourceCityNameKey() : L"", 0);
}

std::wstring CyTradeRoute::getDestinationCityName() const
{
	return gDLL->getObjectText(m_pTradeRoute ? m_pTradeRoute->getDestinationCityNameKey() : L"", 0);
}

int CyTradeRoute::getYield() const
{
	return m_pTradeRoute ? m_pTradeRoute->getYield() : -1;
}

// < JTradeRoutes Mod Start >
std::wstring CyTradeRoute::getName() const
{
	return m_pTradeRoute ? m_pTradeRoute->getName() : L"";
}

void CyTradeRoute::setName(std::wstring szNewValue)
{
	if (m_pTradeRoute)
		m_pTradeRoute->setName(szNewValue);
}

int /*PlayerTypes*/ CyTradeRoute::getOwner() const
{
    return m_pTradeRoute ? m_pTradeRoute->getOwner() : -1;
}


int CyTradeRoute::getEuropeCityID() const
{
    return m_pTradeRoute ? m_pTradeRoute->getEuropeCityID() : m_pTradeRoute->EUROPE_CITY_ID;
}

int CyTradeRoute::getAnywhereCityID() const
{
    return m_pTradeRoute ? m_pTradeRoute->getAnywhereCityID() : m_pTradeRoute->ANYWHERE_CITY_ID;
}

int CyTradeRoute::getNoCityID() const
{
    return m_pTradeRoute ? m_pTradeRoute->getNoCityID() : m_pTradeRoute->NO_CITY_ID;
}


bool CyTradeRoute::isSourceEurope() const
{
	return m_pTradeRoute ? m_pTradeRoute->isSourceEurope() : false;
}

bool CyTradeRoute::isDestinationEurope() const
{
	return m_pTradeRoute ? m_pTradeRoute->isDestinationEurope() : false;
}

bool CyTradeRoute::isLandRoute() const
{
	return m_pTradeRoute ? m_pTradeRoute->isLandRoute() : false;
}

bool CyTradeRoute::isSeaRoute() const
{
	return m_pTradeRoute ? m_pTradeRoute->isSeaRoute() : false;
}
// < JTradeRoutes Mod End >
