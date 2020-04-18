#
# JCvAlertManager Mod
# Code writen by Jeckel
# v0.1
#

"""This module has a single class that allows the quick sending of messages
and popups to players.

To use this module you import it and then instance the class CvAlertManager.
The constructor takes no arguments.
    import CvAlertManager
    alert = CvAlertManager.CvAlertManager()
You can then call instance methods like normal.

Message Methods:
    logCombat(iPlayer, sText)
        "Return None"
        Adds the message 'sText' to iPlayer's Combat Log.

    alert(iPlayer, sText, iColor = 7)
        "Return None"
        Adds the message 'sText' to iPlayer's screen.

    debug(iPlayer, sText, xValue, iColor = 7)
        "Return None"
        Adds the message 'sText = xValue' to iPlayer's screen.
        xValue can be anything and it will be turned into a string
        before output.

    icon(iPlayer, pObject, sText, szIcon = None, iColor = 7)
        "Return None"
        Adds the message 'sText' to iPlayer's screen.
        szIcon should be the Art path to a valid button starting from the
        Art directory and including the file extension.
        For example:
            "Art/Interface/Buttons/Units/Warrior.dds"

Popup Methods:
    popup(self, iPlayer, sText)
        "Return None"
        Shows a popup with sText and a close button to iPlayer.

    popup(self, iPlayer, sText, sButtonText)
        "Return None"
        Shows a popup to iPlayer with sText and a button with sButtonText.

    popup(self, iPlayer, sText, sButtonText = "Close",
          sHandler = None, iData1 = -1, iData2 = -1, iData3 = -1, iFlags = -1,
          bOption1 = False, bOption2 = False):
        "Return None"
        This method opens most of the basic power of popups allowing you to set
        the button handler, iDatas, iFlags, and the bOptions.

    popupList(self, lPlayers, sText, sButtonText = "Close",
              sHandler = None, iData1 = -1, iData2 = -1, iData3 = -1, iFlags = -1,
              bOption1 = False, bOption2 = False):
        "Return None"
        Shows a popup to a list of players.
        lPlayers is a list of PlayerID numbers.

    popupAll(self, sText, sButtonText = "Close",
             sHandler = None, iData1 = -1, iData2 = -1, iData3 = -1, iFlags = -1,
             bOption1 = False, bOption2 = False):
        "Return None"
        Shows a popup to all human players.
"""

from CvPythonExtensions import *

#import Popup as PyPopup

###################################################
# globals

gc = CyGlobalContext()
gi = CyInterface()

############################################################################

class CvAlertManager:
        def __init__(self):
                self.dColors = {"white": [-1, 0, -1], "grey": [4, 5, 6],
                                "red": [298, 7, -1], "green": [46, 8, -1], "blue": [59, 9, -1],
                                "cyan": [44, 10, -1], "yellow": [97, 11, -1], "magenta": [69, 12, -1],
                                "brown": [41, 18, 13]}

        ###################################################################
        # These methods produce messages in the log and/or on the screen. #
        ###################################################################
        
        def logCombat(self, iPlayer, sText):
                """Return None"""
                sText = str(sText)
                gi.addCombatMessage(iPlayer, sText)

        def test(self, iColor = None, lColor = None):
                """Return None"""
                if (iColor == None) and (lColor == None):
                        for sColor in self.dColors:
                                sText = "A test of " + sColor
                                lColors = self.dColors[sColor]
                                s = sText + " dark"
                                i = lColors[0]
                                self.debug(0, s, i, i)
                                s = sText
                                i = lColors[1]
                                self.debug(0, s, i, i)
                                s = sText + " light"
                                i = lColors[2]
                                self.debug(0, s, i, i)
                        return None
                if (lColor == None):
                        iColor = int(iColor)
                        sText = "a color test"
                        self.debug(0, sText, iColor, iColor)
                        return None
                for iColor in lColors:
                        iColor = int(iColor)
                        sText = "a color test"
                        self.debug(0, sText, iColor, iColor)
                        return None

        def debug(self, iPlayer, sText, xValue, iColor = 7):
                """Return None"""
                pPlayer = gc.getPlayer(iPlayer)
                # Return immediately if the player passed in is invalid
	        if (pPlayer == None) or (pPlayer.isNone()) or (not pPlayer.isHuman()):
		        return None

                eventMessageTimeLong = gc.getDefineINT("EVENT_MESSAGE_TIME_LONG")
                szIcon = None
                iFlashX = 0
                iFlashY = 0
                szString = str(sText) + " = " + str(xValue)

                gi.addMessage(iPlayer, True, eventMessageTimeLong,
                                         szString, None, 0, szIcon, ColorTypes(iColor),
                                         iFlashX, iFlashY, False, False)

        def alert(self, iPlayer, sText, iColor = 7):
                """Return None"""
                pPlayer = gc.getPlayer(iPlayer)
                # Return immediately if the player passed in is invalid
	        if (pPlayer == None) or (pPlayer.isNone()) or (not pPlayer.isHuman()):
		        return None

                eventMessageTimeLong = gc.getDefineINT("EVENT_MESSAGE_TIME_LONG")
                szIcon = None
                iFlashX = 0
                iFlashY = 0
                szString = str(sText)

                gi.addMessage(iPlayer, True, eventMessageTimeLong,
                                         szString, None, 0, szIcon, ColorTypes(iColor),
                                         iFlashX, iFlashY, False, False)

        def icon(self, iPlayer, pObject, sText, szIcon = None, iColor = 7):
                """Return None"""
                pPlayer = gc.getPlayer(iPlayer)
                # Return immediately if the player passed in is invalid
	        if (pPlayer == None) or (pPlayer.isNone()) or (not pPlayer.isHuman()):
        	        return None
                # Return immediately if the object passed in is invalid
	        if (pObject == None) or (pObject.isNone()):
		        return None

                eventMessageTimeLong = gc.getDefineINT("EVENT_MESSAGE_TIME_LONG")
                szString = str(sText)

                gi.addMessage(iPlayer, True, eventMessageTimeLong,
                                         szString, None, 0, szIcon, ColorTypes(iColor),
                                         pObject.getX(), pObject.getY(), True, True)

        ############################################################################

        ###################################################################
        # These methods produce messages in the log and/or on the screen. #
        ###################################################################

        def popup(self, iPlayer,
                  sText, sButtonText = "Close",
                  sHandler = None,
                  iData1 = -1, iData2 = -1, iData3 = -1, iFlags = -1,
                  bOption1 = False, bOption2 = False
                  ):
                """Return None"""
                pPlayer = gc.getPlayer(iPlayer)
                # No need to ever show the Computer Popups
	        if (pPlayer == None) or (pPlayer.isNone()) or (not pPlayer.isHuman()):
                        return None
                popupInfo = CyPopupInfo()
                popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
                popupInfo.setText(sText)
                if (sHandler != None):
                        popupInfo.setOnClickedPythonCallback(sHandler)
                        popupInfo.setData1(iData1)
                        popupInfo.setData2(iData2)
                        popupInfo.setData3(iData3)
                        popupInfo.setFlags(iFlags)
                        popupInfo.setOption1(bOption1)
                        popupInfo.setOption2(bOption2)
                popupInfo.addPythonButton(sButtonText, "")
                popupInfo.addPopup(iPlayer)

        def popupList(self, lPlayers,
                      sText, sButtonText = "Close",
                      sHandler = None,
                      iData1 = -1, iData2 = -1, iData3 = -1, iFlags = -1,
                      bOption1 = False, bOption2 = False
                      ):
                """Return None"""
                for iPlayer in lPlayers:
                        self.popup(iPlayer, sText, sButtonText, sHandler,
                                   iData1, iData2, iData3, iFlags, bOption1, bOption2)

        def popupAll(self, sText, sButtonText = "Close",
                     sHandler = None,
                     iData1 = -1, iData2 = -1, iData3 = -1, iFlags = -1,
                     bOption1 = False, bOption2 = False
                     ):
                """Return None"""
                iPlayers = gc.getMAX_CIV_PLAYERS()
                for iPlayer in iPlayers:
                        self.popup(iPlayer, sText, sButtonText, sHandler,
                                   iData1, iData2, iData3, iFlags, bOption1, bOption2)

        ############################################################################
