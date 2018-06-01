#!/usr/bin/python

try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

try:  #first look for libraries in the same folder
    import sys
    #sys.path.insert(0, '/home/pi/Dexter/DI_Sensors/Python/di_sensors/red_line_follower/line_follower')

    import line_sensor
    import scratch_line
except ImportError:
    try:  # look in the standard Raspbian for Robots folder.
        sys.path.insert(0, '/home/pi/Dexter/DI_Sensors/Python/di_sensors/red_line_follower/line_follower')

        import line_sensor
        import scratch_line

    except ImportError:
        raise ImportError,"Line sensor libraries not found"
        sys.exit(0)

PIHOME="/home/pi"
DEXTER="Dexter"
SCRATCH="Scratch_GUI"
RFR_TOOLS="RFR_Tools"
ICON_PATH = "/".join( (PIHOME, DEXTER,"lib",DEXTER, RFR_TOOLS, "icons")  )+"/"

class MainPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(wx.WHITE)
        self.frame = parent

        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, u'Helvetica')
        self.SetFont(font)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        vSizer = wx.BoxSizer(wx.VERTICAL)

        logo_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bmp = wx.Bitmap(ICON_PATH+"dexter_industries_logo.png",type=wx.BITMAP_TYPE_PNG)
        bitmap = wx.StaticBitmap(self, bitmap=bmp)
        bmpW,bmpH = bitmap.GetSize()
        logo_sizer.Add(bitmap,0,wx.RIGHT|wx.LEFT|wx.EXPAND)
        vSizer.Add(logo_sizer,0,wx.SHAPED|wx.EXPAND)

        instructions = u'Instructions:\n\n' + \
                       u' 1.\tPlace the line sensor so that all of the black sensors are \n\tover your black line.  Then press the button "Set Black Line Values".\n\n' + \
                       u' 2.\tNext, place the line sensor so that all of the black sensors are \n\tNOT over your black line and on the white background surface.\n\tThen press "Set White Line Values".\n\n' + \
                       u' 3.\tFinally, test the sensor by pressing "Read Line Position"'
        self.label_top = wx.StaticText(self,-1,label=instructions)
        vSizer.Add(self.label_top,1,wx.EXPAND)

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Set up buttons
        self.black_line_set_button = wx.Button(self,-1,label="Set Black Line Values")
        self.Bind(wx.EVT_BUTTON, self.black_line_set_OnButtonClick, self.black_line_set_button)
        buttonSizer.AddSpacer(10)
        buttonSizer.Add(self.black_line_set_button,0)
        buttonSizer.AddSpacer(10)

        self.white_line_set_button = wx.Button(self,-1,label="Set White Line Values")
        self.Bind(wx.EVT_BUTTON, self.white_line_set_button_OnButtonClick, self.white_line_set_button)
        buttonSizer.Add(self.white_line_set_button,0)
        buttonSizer.AddSpacer(10)
        
        self.line_position_set_button = wx.Button(self,-1,label="Read Line Position")
        self.Bind(wx.EVT_BUTTON, self.line_position_set_button_OnButtonClick, self.line_position_set_button)
        buttonSizer.Add(self.line_position_set_button,0)
        buttonSizer.AddSpacer(10)

        vSizer.AddSpacer(20)
        vSizer.Add(buttonSizer)
        vSizer.AddSpacer(10)

        # Set up labels: This is where the output of sensor readings will be printed.
        self.label = wx.StaticText(self,-1,label=u'  ')	# Prints line sensor information out.
        vSizer.Add( self.label )
        
                # Exit
        self.exit_button = wx.Button(self, label="Exit")
        self.exit_button.Bind(wx.EVT_BUTTON, self.onClose)
        vSizer.AddSpacer(20)
        vSizer.Add(self.exit_button, 0, wx.ALIGN_RIGHT)
        hSizer.AddSpacer(5)
        hSizer.Add(vSizer)
        hSizer.AddSpacer(5)
        self.SetSizerAndFit(hSizer)

        self.Show(True)

    def black_line_set_OnButtonClick(self,event):
        for i in range(2):
            line_sensor.get_sensorval()
        line_sensor.set_black_line()
        line_val=line_sensor.get_black_line()
        self.label.SetLabel("Black Line : "+str(line_val))


    def white_line_set_button_OnButtonClick(self,event):
        for i in range(2):
            line_sensor.get_sensorval()
        line_sensor.set_white_line()
        line_val=line_sensor.get_white_line()
        self.label.SetLabel("White Line : "+str(line_val))

    def line_position_set_button_OnButtonClick(self, event):
        # There's an issue with the line follower being "behind"
        for i in range(3):
            line_val=scratch_line.absolute_line_pos()
        self.label.SetLabel("Line Position : "+str(line_val))

    def onClose(self, event):	# Close the entire program.
        self.frame.Close()

class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        # wx.ComboBox

        wx.Icon(ICON_PATH+'favicon.ico', wx.BITMAP_TYPE_ICO)
        wx.Log.SetVerbose(False)
        wx.Frame.__init__(self, None, title="Line Follower Calibration", size=(530,600))		# Set the fram size
        panel = MainPanel(self)
        self.Center()

class Main(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        dlg = MainFrame()
        dlg.Show()


if __name__ == "__main__":
    app = Main()
    app.MainLoop()
