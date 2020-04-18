#pragma once

#ifndef CyTradeRoute_h
#define CyTradeRoute_h

#include "CvTradeRoute.h"

class CyCity;

class CyTradeRoute
{
public:
	CyTradeRoute();
	CyTradeRoute(CvTradeRoute* pTradeRoute);

	int getID() const;
	IDInfo getSourceCity() const;
	IDInfo getDestinationCity() const;
	std::wstring getSourceCityNameKey() const;
	std::wstring getDestinationCityNameKey() const;
	std::wstring getSourceCityName() const;
	std::wstring getDestinationCityName() const;
	int getYield() const;

	// < JTradeRoutes Mod Start >
	std::wstring getName() const;
    void setName(std::wstring szNewValue);
    int /*PlayerTypes*/ getOwner() const;

	int getEuropeCityID() const;
	int getAnywhereCityID() const;
	int getNoCityID() const;

	bool isSourceEurope() const;
	bool isDestinationEurope() const;
	bool isLandRoute() const;
	bool isSeaRoute() const;
	// < JTradeRoutes Mod End >

protected:
	CvTradeRoute* m_pTradeRoute;
};

#endif	// #ifndef CyTradeRoute_h
