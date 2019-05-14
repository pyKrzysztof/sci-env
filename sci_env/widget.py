import wx
import json

from lib.buttons import ButtonBase


class WidgetBaseClass(wx.Panel):


    def InitWidget(self, config_manager, name=__name__):
    
        # necessary bindings.
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)

        # <-------------------------------------------------
        # loading config, note that name must be passed by child, it is __name__
        self.widgetConf = self._ReadConfig(name)
        self.appConf = config_manager

        # <-------------------------------------------------
        # loading config font
        self.regFont = eval(self.appConf.Get('regFont'))
        self.titleFont = eval(self.appConf.Get('titleFont'))
        
        # <-------------------------------------------------
        # creating the sizers
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        upperSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # <-------------------------------------------------
        # add close button
        closeButton = CloseButton(self, self.appConf, size=(24, 24))
        upperSizer.Add(closeButton, 0)

        # <-------------------------------------------------
        # add title/mover
        title = Title(self, self.widgetConf['name'], self.appConf, size=(120, 24))
        upperSizer.Add(title, 1, flag=wx.EXPAND)

        # <-------------------------------------------------
        # add resizer
        resizer = Resizer(self, self.appConf, size=(24, 24))
        upperSizer.Add(resizer, 0, flag=wx.EXPAND) 

        # <-------------------------------------------------
        # adding the upper sizer
        self.sizer.Add(upperSizer, 0, wx.EXPAND)

        # <-------------------------------------------------
        # finishing by setting the sizer
        self.SetSizer(self.sizer)
        self.Fit()
    
    #---------------------------------------------------------------------------------  
    

    def AddPanel(self, panel, proportion=1, flags=wx.EXPAND):
        self.sizer.Add(panel, proportion=proportion, flag=flags|wx.ALL, border=1)


    def _ReadConfig(self, name):
        try:
            path = name.replace('.', '/').replace('main', 'config.json')
            with open(path, 'r') as config:
                return json.load(config)
        except:
        	pass


    def _OnEraseBackground(self, e):
        pass


    def _OnPaint(self, e):
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.appConf.Get('widgetFrameColor')))
        dc.Clear()
        self.Draw(dc)
        self._DrawBorder(dc)


    def _DrawBorder(self, dc):
        width, height = self.GetClientSize()
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen(self.appConf.Get('widgetFrameColor'), width=0.5))
        dc.DrawRectangle(0, 24, width, height-24)


    def Draw(self, dc):
        pass



class Title(wx.Control):


	def __init__(self, parent, title, conf, size):
		super().__init__(parent, id=wx.ID_ANY, style=wx.NO_BORDER, size=size)

		self.title = title
		self.parent = parent
		self.conf = conf
		self.font = conf.Get('regFont', True)

		self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
		self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
		self.Bind(wx.EVT_MOTION, self.Move)
		self.Bind(wx.EVT_PAINT, self._OnPaint)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)

		self._move = False


	def MouseDown(self, e):
		self._move = True
		sx, sy = self.parent.GetParent().ScreenToClient(self.parent.GetPosition())
		dx, dy = self.parent.GetParent().ScreenToClient(wx.GetMousePosition())
		self._x, self._y = (sx-dx, sy-dy)
		self.Refresh()
	

	def Move(self, e):
		if not self._move:
			return
		dx, dy = wx.GetMousePosition()
		newpos = (self._x + dx, self._y + dy)
		if self._y + dy <= 0:
			newpos = (newpos[0], 1)
		if self._x + dx <= 0:
			newpos = (1, newpos[1])
	
		self.parent.SetPosition(newpos)
		self.Refresh()


	def MouseUp(self, e):
		self._move = False
		self.Refresh()


	def _OnEraseBackground(self, e):
		pass


	def _OnPaint(self, e):
		dc = wx.BufferedPaintDC(self)
		self.Draw(dc)


	def Draw(self, dc):
		dc.SetBackground(wx.Brush(self.conf.Get('widgetFrameColor')))
		dc.SetTextForeground(self.conf.Get('textColor'))
		dc.SetFont(self.font)
		dc.Clear()

		
		textWidth, textHeight = dc.GetTextExtent(self.title)
		width, height = self.GetClientSize()
		textX = (width - textWidth) / 2
		textY = (height - textHeight) / 2
		
		dc.DrawText(self.title, textX, textY)



class Resizer(wx.Control):


	def __init__(self, parent, conf, size):
		super().__init__(parent, id=wx.ID_ANY, style=wx.NO_BORDER, size=size)

		self.parent = parent
		self.conf = conf

		self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
		self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
		self.Bind(wx.EVT_MOTION, self.Move)
		self.Bind(wx.EVT_PAINT, self._OnPaint)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)

		self._move = self._resize = False


	def MouseDown(self, e):
		self._resize = True
		self._sizex, self._sizey = self.parent.GetSize()
		self._x, self._y = self.parent.GetPosition()
	

	def Move(self, e):
		if not self._resize:
			return
		# current position of widget
		posx, posy = self.parent.GetPosition()
		# position of mouse
		mposx, mposy = self.parent.GetParent().ScreenToClient(wx.GetMousePosition())
		# getting the difference
		dy = posy - mposy
		dx = mposx - posx - self._sizex

		newpos = (self.parent.GetPosition()[0], mposy)
		newsize = (self._sizex + dx, self.parent.GetSize()[1] + dy)

		if newpos[1] <= 0:
			newpos = (newpos[0], 1)
			newsize = (newsize[0], self._sizey + self._y)

		if newsize[0] <= self.parent.GetBestSize()[0]:
			newsize = (self.parent.GetBestSize()[0], newsize[1])

		if newsize[1] <= self.parent.GetBestSize()[1]:
			newsize = (newsize[0], self.parent.GetBestSize()[1])
			newpos = (newpos[0], self._y + self._sizey - self.parent.GetSize()[1])
			
		# setting the position
		self.parent.SetPosition(newpos)
		# setting the size
		self.parent.SetSize(newsize)
	

	def MouseUp(self, e):
		self._resize = False


	def _OnEraseBackground(self, e):
		pass


	def _OnPaint(self, e):
		dc = wx.BufferedPaintDC(self)
		self.Draw(dc)


	def Draw(self, dc):
		dc.SetBackground(wx.Brush(self.conf.Get('widgetFrameColor')))
		dc.Clear()



class CloseButton(ButtonBase):


	def __init__(self, parent, conf, size):
		super().__init__(parent, conf, '', size=size)
		self.parent = parent
		self.conf = conf
		self.active_bmp = wx.Bitmap('assets/bitmaps/quit_16_active.png')
		self.inactive_bmp = wx.Bitmap('assets/bitmaps/quit_16_inactive.png')


	def _onMouseUp(self, event):
		self.parent.Destroy()


	def Draw(self, dc):
		dc.SetBackground(wx.Brush(self.conf.Get('widgetFrameColor')))
		dc.Clear()

		if self._mouseIn:
			bmp = self.active_bmp
		else:
			bmp = self.inactive_bmp

		X = (self.GetSize()[0] - 16) / 2
		Y = (self.GetSize()[1] - 16) / 2
		dc.DrawBitmap(bmp, X, Y)