# -*- coding: utf-8 -*-
from resources.lib.config import cConfig
from resources.lib.gui.guiElement import cGuiElement
from resources.lib import logger
import urllib
import os
import xbmc

class cLibraryIntegration:

    def __init__(self):
        self.__sFilename = 'empty.strm'
        self.__sStrmDir = cConfig().getSetting('StrmFolder')
        self.__sRelPath = ''
        self.__sContent = ''

    def __mangleFilename(self):
        self.__sFilename = self.__sFilename.replace(":"," - ")

    def __buildFilename(self, oGuiElement, itemValues):
        sTitle = oGuiElement.getTitle()
        sMediaType = oGuiElement._mediaType
        if sMediaType == 'movie':
            logger.info("isMovie")
            self.__sRelPath = 'Movies/'
        elif sMediaType == 'episode':
            logger.info("isEpisode")
            sSeason = itemValues['season']
            sEpisode = itemValues['episode']
            sTVShowTitle = itemValues['TVShowTitle']
            self.__sRelPath = 'TVShows/' + sTVShowTitle + '/Staffel ' + sSeason
            sTitle = '/S' + sSeason + 'E' + sTitle

        self.__sFilename = sTitle + '.strm'

    def __writeFile(self):
        sAbsPath = self.__sStrmDir + self.__sRelPath
        sAbsPath = xbmc.translatePath(sAbsPath)
        if not os.path.isdir(sAbsPath):
            os.makedirs(os.path.join(sAbsPath))
        sFullFilename = sAbsPath + self.__sFilename
        if not os.path.isfile(sFullFilename):
            fStrmFile = open(sFullFilename, 'w')
            fStrmFile.write(self.__sContent + '\n') 
            fStrmFile.close() 

    def write(self, oGuiElement, sItemUrl):
        itemValues = oGuiElement.getItemValues()
        self.__sContent = sItemUrl
        self.__buildFilename(oGuiElement, itemValues)
        self.__mangleFilename()
        self.__writeFile()

