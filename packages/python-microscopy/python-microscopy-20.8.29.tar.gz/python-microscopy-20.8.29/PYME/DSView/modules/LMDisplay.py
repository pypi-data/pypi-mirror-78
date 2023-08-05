# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 17:43:10 2015

@author: david
"""

import wx

import os

#from pylab import *


import numpy
# import pylab
import matplotlib.cm

#import PYME.ui.autoFoldPanel as afp

from PYME.DSView import fitInfo
from PYME.DSView.OverlaysPanel import OverlayPanel
import wx.lib.agw.aui as aui

from PYME.misc import extraCMaps


from PYME.LMVis import pipeline



import numpy as np

debug = True

def debugPrint(msg):
    if debug:
        print(msg)
        

from PYME.LMVis import visCore
from ._base import Plugin

class LMDisplay(visCore.VisGUICore, Plugin):
    def __init__(self, dsviewer):
        Plugin.__init__(self, dsviewer)

        if 'fitResults' in dir(self.image):
            self.fitResults = self.image.fitResults
        else:
            self.fitResults = []
        
        if 'resultsMdh' in dir(self.image):
            self.resultsMdh = self.image.resultsMdh


        dsviewer.paneHooks.append(self.GenPanels)
        dsviewer.updateHooks.append(self.update)


        
        if (len(self.fitResults) > 0) and not 'PYME_BUGGYOPENGL' in os.environ.keys():
            self.GenResultsView()   
            
        if not 'pipeline' in dir(dsviewer):
            dsviewer.pipeline = pipeline.Pipeline(visFr=self)
        
        self.pipeline = dsviewer.pipeline
        self.pipeline.visFr = self
        self.view.filter = self.pipeline
        
        #self.Quads = None
        #dsviewer.menubar.Insert(dsviewer.menubar.GetMenuCount()-1, self.CreateMenuBar(subMenu=True), 'Points')

        # initialize the common parts
        visCore.VisGUICore.__init__(self)

        self.CreateMenuBar(subMenu=True)



        #self.Bind(wx.EVT_IDLE, self.OnIdle)

        self._sf = False

        #statusLog.SetStatusDispFcn(self.SetStatus)
    

        



        
            
    def CreateFoldPanel(self):
        self.dsviewer.CreateFoldPanel()

    
        
    def Bind(self, *args, **kwargs):
        self.dsviewer.Bind(*args, **kwargs)

    def AddExtrasMenuItem(self,label, callback):
        """Add an item to the VisGUI extras menu.
        
        parameters:
            label       textual label to use for the menu item.
            callback    function to call when user selects the menu item. This 
                        function should accept one argument, which will be the
                        wxPython event generated by the menu selection.
        """
        
        ID_NEWITEM = wx.NewId()
        self.extras_menu.Append(ID_NEWITEM, label)
        self.dsviewer.Bind(wx.EVT_MENU, callback, id=ID_NEWITEM)

    

            
      
            
    

   

    def GenResultsView(self):
        voxx, voxy = self.image.voxelsize_nm
        
        self.SetFitInfo()

        from PYME.LMVis import gl_render
        self.glCanvas = gl_render.LMGLCanvas(self.dsviewer, False, vp = self.do, vpVoxSize = voxx)
        self.glCanvas.cmap = matplotlib.cm.gist_rainbow
        self.glCanvas.pointSelectionCallbacks.append(self.OnPointSelect)

        self.dsviewer.AddPage(page=self.glCanvas, select=True, caption='VisLite')

        xsc = self.image.data.shape[0]*voxx/self.glCanvas.Size[0]
        ysc = self.image.data.shape[1]*voxy/ self.glCanvas.Size[1]

        if xsc > ysc:
            self.glCanvas.setView(0, xsc*self.glCanvas.Size[0], 0, xsc*self.glCanvas.Size[1])
        else:
            self.glCanvas.setView(0, ysc*self.glCanvas.Size[0], 0, ysc*self.glCanvas.Size[1])

        #we have to wait for the gui to be there before we start changing stuff in the GL view
        #self.timer.WantNotification.append(self.AddPointsToVis)

        self.glCanvas.Bind(wx.EVT_IDLE, self.OnIdle)
        self.pointsAdded = False
        
    def SetFitInfo(self):
        self.view.pointMode = 'lm'
        voxx, voxy = self.image.voxelsize_nm
        
        self.view.points = numpy.vstack((self.fitResults['fitResults']['x0']/voxx, self.fitResults['fitResults']['y0']/voxy, self.fitResults['tIndex'])).T

        if 'Splitter' in self.image.mdh.getEntry('Analysis.FitModule'):
            self.view.pointMode = 'splitter'
            if 'BNR' in self.image.mdh['Analysis.FitModule']:
                self.view.pointColours = self.fitResults['ratio'] > 0.5
            else:
                self.view.pointColours = self.fitResults['fitResults']['Ag'] > self.fitResults['fitResults']['Ar']
            
        if not 'fitInf' in dir(self):
            self.fitInf = fitInfo.FitInfoPanel(self.dsviewer, self.fitResults, self.resultsMdh, self.do.ds)
            self.dsviewer.AddPage(page=self.fitInf, select=False, caption='Fit Info')
        else:
            self.fitInf.SetResults(self.fitResults, self.resultsMdh)
            
        
    def OnPointSelect(self, xp, yp):
        dist = np.sqrt((xp - self.fitResults['fitResults']['x0'])**2 + (yp - self.fitResults['fitResults']['y0'])**2)
        
        cand = dist.argmin()
        
        vx, vy, _ = self.image.voxelsize_nm
        self.dsviewer.do.xp = xp/vx
        self.dsviewer.do.yp = yp/vy
        self.dsviewer.do.zp = self.fitResults['tIndex'][cand]
        

#    def OnIdle(self,event):
#        if not self.pointsAdded:
#            self.pointsAdded = True
#
#            self.glCanvas.setPoints(self.fitResults['fitResults']['x0'],self.fitResults['fitResults']['y0'],self.fitResults['tIndex'].astype('f'))
#            self.glCanvas.setCLim((0, self.fitResults['tIndex'].max()))


    def AddPointsToVis(self):
        self.glCanvas.setPoints(self.fitResults['fitResults']['x0'],self.fitResults['fitResults']['y0'],self.fitResults['tIndex'].astype('f'))
        self.glCanvas.setCLim((0, self.fitResults['tIndex'].max()))

        self.timer.WantNotification.remove(self.AddPointsToVis)

    def GetStatusText(self):
        return 'Frames Analysed: %d    Events detected: %d' % (self.numAnalysed, self.numEvents)
        


#    def GenFitStatusPanel(self, _pnl):
#        item = afp.foldingPane(_pnl, -1, caption="Fit Status", pinned = True)
#
#        pan = wx.Panel(item, -1, size = (160, 300))
#
#        vsizer = wx.BoxSizer(wx.VERTICAL)
#
#        hsizer = wx.BoxSizer(wx.HORIZONTAL)
#        hsizer.Add(wx.StaticText(pan, -1, 'Colour:'), 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
#
#        self.chProgDispColour = wx.Choice(pan, -1, choices = ['z', 'gFrac', 't'], size=(60, -1))
#        self.chProgDispColour.Bind(wx.EVT_CHOICE, self.OnProgDispColourChange)
#        hsizer.Add(self.chProgDispColour, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
#
#        vsizer.Add(hsizer, 0,wx.BOTTOM|wx.EXPAND, 2)
#
#        hsizer = wx.BoxSizer(wx.HORIZONTAL)
#        hsizer.Add(wx.StaticText(pan, -1, 'CMap:'), 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
#
#        self.chProgDispCMap = wx.Choice(pan, -1, choices = ['gist_rainbow', 'RdYlGn'], size=(60, -1))
#        self.chProgDispCMap.Bind(wx.EVT_CHOICE, self.OnProgDispCMapChange)
#        hsizer.Add(self.chProgDispCMap, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
#
#        vsizer.Add(hsizer, 0,wx.BOTTOM|wx.EXPAND, 7)
#
#        self.progPan = progGraph.progPanel(pan, self.fitResults, size=(220, 250))
#        self.progPan.draw()
#
#        vsizer.Add(self.progPan, 1,wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 0)
#
#        pan.SetSizer(vsizer)
#        vsizer.Fit(pan)
#
#        #_pnl.AddFoldPanelWindow(item, pan, fpb.FPB_ALIGN_WIDTH, fpb.FPB_DEFAULT_SPACING, 0)
#        item.AddNewElement(pan)
#        _pnl.AddPane(item)

#    def OnProgDispColourChange(self, event):
#        #print 'foo'
#        self.analDispMode = self.chProgDispColour.GetStringSelection()
#        self.refresh_analysis()
#
#    def OnProgDispCMapChange(self, event):
#        #print 'foo'
#        self.glCanvas.setCMap(pylab.cm.__getattribute__(self.chProgDispCMap.GetStringSelection()))

   

#    def refresh_analysis(self):
#        newNumAnalysed = self.tq.getNumberTasksCompleted(self.image.seriesName)
#        if newNumAnalysed > self.numAnalysed:
#            self.numAnalysed = newNumAnalysed
#            newResults = self.tq.getQueueData(self.image.seriesName, 'FitResults', len(self.fitResults))
#            if len(newResults) > 0:
#                if len(self.fitResults) == 0:
#                    self.fitResults = newResults
#                else:
#                    self.fitResults = numpy.concatenate((self.fitResults, newResults))
#                self.progPan.fitResults = self.fitResults
#
#                self.view.points = numpy.vstack((self.fitResults['fitResults']['x0'], self.fitResults['fitResults']['y0'], self.fitResults['tIndex'])).T
#
#                self.numEvents = len(self.fitResults)
#
#                if self.analDispMode == 'z' and (('zm' in dir(self)) or ('z0' in self.fitResults['fitResults'].dtype.fields)):
#                    #display z as colour
#                    if 'zm' in dir(self): #we have z info
#                        if 'z0' in self.fitResults['fitResults'].dtype.fields:
#                            z = 1e3*self.zm(self.fitResults['tIndex'].astype('f')).astype('f')
#                            z_min = z.min() - 500
#                            z_max = z.max() + 500
#                            z = z + self.fitResults['fitResults']['z0']
#                            self.glCanvas.setPoints(self.fitResults['fitResults']['x0'],self.fitResults['fitResults']['y0'],z)
#                            self.glCanvas.setCLim((z_min, z_max))
#                        else:
#                            z = self.zm(self.fitResults['tIndex'].astype('f')).astype('f')
#                            self.glCanvas.setPoints(self.fitResults['fitResults']['x0'],self.fitResults['fitResults']['y0'],z)
#                            self.glCanvas.setCLim((z.min(), z.max()))
#                    elif 'z0' in self.fitResults['fitResults'].dtype.fields:
#                        z = self.fitResults['fitResults']['z0']
#                        self.glCanvas.setPoints(self.fitResults['fitResults']['x0'],self.fitResults['fitResults']['y0'],z)
#                        self.glCanvas.setCLim((-1e3, 1e3))
#
#                elif self.analDispMode == 'gFrac' and 'Ag' in self.fitResults['fitResults'].dtype.fields:
#                    #display ratio of colour channels as point colour
#                    c = self.fitResults['fitResults']['Ag']/(self.fitResults['fitResults']['Ag'] + self.fitResults['fitResults']['Ar'])
#                    self.glCanvas.setPoints(self.fitResults['fitResults']['x0'],self.fitResults['fitResults']['y0'],c)
#                    self.glCanvas.setCLim((0, 1))
#                elif self.analDispMode == 'gFrac' and 'ratio' in self.fitResults['fitResults'].dtype.fields:
#                    #display ratio of colour channels as point colour
#                    c = self.fitResults['fitResults']['ratio']
#                    self.glCanvas.setPoints(self.fitResults['fitResults']['x0'],self.fitResults['fitResults']['y0'],c)
#                    self.glCanvas.setCLim((0, 1))
#                else:
#                    #default to time
#                    self.glCanvas.setPoints(self.fitResults['fitResults']['x0'],self.fitResults['fitResults']['y0'],self.fitResults['tIndex'].astype('f'))
#                    self.glCanvas.setCLim((0, self.numAnalysed))
#
#        if (self.tq.getNumberOpenTasks(self.image.seriesName) + self.tq.getNumberTasksInProgress(self.image.seriesName)) == 0 and 'SpoolingFinished' in self.image.mdh.getEntryNames():
#            self.dsviewer.statusbar.SetBackgroundColour(wx.GREEN)
#            self.dsviewer.statusbar.Refresh()
#
#        self.progPan.draw()
#        self.progPan.Refresh()
#        self.dsviewer.Refresh()
#        self.dsviewer.update()

    def update(self, dsviewer):
        #self.RefreshView()
        if 'fitInf' in dir(self) and not self.dsviewer.playbackpanel.tPlay.IsRunning():
            try:
                self.fitInf.UpdateDisp(self.view.PointsHitTest())
            except:
                import traceback
                print((traceback.format_exc()))


    

def Plug(dsviewer):
    dsviewer.create_overlay_panel()
    
    return LMDisplay(dsviewer)
