#!/usr/bin/python
from random import *
from voronoi import *
import wx

class Canvas(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, name = "Canvas"):
        wx.Panel.__init__(self, parent, id, pos, size, wx.NO_BORDER, name)
        
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self._OnClick)
        self.Bind(wx.EVT_KEY_UP, self._OnChar)
        self.delaunay = None
        self.voronoi = None
        self.initPoints(10, size)
        self.initTriangulation()
        
    def initPoints(self, count, limits = (200, 200)):
        self.points = []
##        for i in range(count):
##            x = random()*limits[0]
##            y = random()*limits[1]
##            self.points.append(Point(x,y))
        self.points += [Point(100, 120), Point(100,180), Point(50, 150)]
        
    def initTriangulation(self):
        self.triangulation = Triangulation(self.points)
        self.delaunay = Delaunay(self.triangulation)
        self.voronoi = Voronoi(self.triangulation, (0,0, self.GetSize()[0], self.GetSize()[1]))

    def _OnChar(self, evt):
        if evt.GetKeyCode() == wx.WXK_RETURN:
            saveFileDialog = wx.FileDialog(self, "Save SVG file", "", "",
                                   "SVG files (*.svg)|*.svg", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return

        self.voronoi.saveSVG(saveFileDialog.GetPath(), self.points)
        
    def _OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        
        dc.Clear()
        
        if self.delaunay is None or self.voronoi is None:
            return
        
        dc.SetPen(wx.Pen(wx.LIGHT_GREY, 1))
        for e in self.triangulation.edges:
            a = self.points[e.a]
            b = self.points[e.b]
            dc.DrawLine(a.x, a.y, b.x, b.y)
    
        #dc.SetPen(wx.Pen(wx.GREEN, 3))
        #for e in self.voronoi.edges:
        #    a = self.voronoi.points[e.a]
        #    b = self.voronoi.points[e.b]
        #    dc.DrawLine(a.x, a.y, b.x, b.y)
        
        dc.SetPen(wx.Pen(wx.RED, 1))
        dc.SetBrush(wx.Brush(wx.RED))
        for p in self.points:
            dc.DrawCircle(p.x, p.y, 2)
        
    def _OnClick(self, evt):
        pos = evt.GetPosition()
        self.points.append(Point(pos.x, pos.y))
	self.initTriangulation()
        self.Refresh(False, wx.RectS(self.GetSize()))
    
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Voronoi/Delaunay Test", size = (400, 400))
        whatever = Canvas(self, wx.ID_ANY, pos = (5,5), size = self.GetSize())
        whatever.SetFocus()
        
app = wx.PySimpleApp()
frame = MyFrame()
frame.Show(True)
app.MainLoop()
