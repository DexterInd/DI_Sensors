#!/usr/bin/python

try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

from di_sensors import easy_line_follower

lf = easy_line_follower.EasyLineFollower()

PIHOME="/home/pi"
DEXTER="Dexter"
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
        lf.set_calibration("black")
        line_val=lf.get_calibration("black")
        self.label.SetLabel("Black Line : \n"+str(line_val).replace(",","\n").replace(" ","")[1:-1])


    def white_line_set_button_OnButtonClick(self,event):
        lf.set_calibration("white")
        line_val=lf.get_calibration("white")
        self.label.SetLabel("White Line : \n"+str(line_val).replace(",", "\n").replace(" ","")[1:-1])

    def line_position_set_button_OnButtonClick(self, event):
        # There's an issue with the line follower being "behind"
        line_val = lf.position()
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
