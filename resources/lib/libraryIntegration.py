# -*- coding: utf-8 -*-
from resources.lib.config import cConfig
from resources.lib.gui.guiElement import cGuiElement
from resources.lib import logger
import urllib
import os
import xbmc
import time
import re

class cLibraryIntegration:

    def __init__(self):
        self.__sFilename = 'empty.strm'
        self.__sStrmDir = cConfig().getSetting('StrmFolder')
        self.__sRelPath = ''
        self.__sContent = ''

    def __buildFilename(self, oGuiElement):
        itemValues = oGuiElement.getItemValues()
        sTitle = oGuiElement.getTitle().strip()
        sTitle = re.sub(' \(.*\)', '', sTitle)
        sTitle = sTitle.replace(":"," - ")
        sTitle = sTitle.replace("/","-")
        sTitle = ' '.join(sTitle.split())
        sMediaType = oGuiElement._mediaType
        if sMediaType == 'episode':
            logger.info("isEpisode")
            sSeason = itemValues['season']
            sEpisode = itemValues['episode']
            sTVShowTitle = itemValues['TVShowTitle']
            self.__sRelPath = 'TVShows/' + sTVShowTitle + '/Staffel ' + sSeason
            sTitle = '/S' + sSeason + 'E' + sEpisode + ' - ' + sTitle
        else:
            pattern = re.compile('[\W_]+', re.UNICODE)
            sDirTitle = pattern.sub('', sTitle.lower())
            sDirA = sDirTitle[0]
            sDirB = sDirTitle[1]
            self.__sRelPath = 'Movies/' + sDirA + '/' + sDirB + '/' 

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
        else:
            # replace old strm files once in a while
            if time.time() - os.path.getmtime(sFullFilename) > (3 * 30 * 24 * 60 * 60):
                fStrmFile = open(sFullFilename, 'w')
                fStrmFile.truncate()
                fStrmFile.write(self.__sContent + '\n')
                fStrmFile.close()

    def write(self, oGuiElement, sItemUrl):
        self.__sContent = sItemUrl
        self.__buildFilename(oGuiElement)
        self.__writeFile()

