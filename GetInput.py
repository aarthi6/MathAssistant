import wx

class GetInput(wx.Frame):
    def __init__(self,parent,id,title,fntsz,mnuspeed,no):
        wx.Frame.__init__(self,parent,id,title)
        #Menu Initialisation Starts..
        self.fontsize=fntsz
        self.speed=mnuspeed
        self.MainPanel=wx.Panel(self,-1)#Main Panel Contains .. MenuPanel+WorksheetPanel
        
        self.butList=range(14) #List of buttons...
        self.ButtonIndex=-1 #Index Points to Current Active Button..
        self.MenuTimer=wx.Timer(self)
        self.Group=0
        self.Mx1,self.My1=0,0
        self.wdt,self.ht=0,0
        self.MenuPanel=wx.Panel(self.MainPanel,-1) #Menu Panel
        self.Bind(wx.EVT_TIMER,self.ChangeButCur)
        self.MenuPanel.Bind(wx.EVT_PAINT,self.OnMenuPaint)
        font=wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(self.fontsize)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        font.SetFamily(wx.FONTFAMILY_DECORATIVE)
        menuBox1=wx.BoxSizer(wx.HORIZONTAL)
        menuBox2=wx.BoxSizer(wx.HORIZONTAL)
        vMenuBox=wx.BoxSizer(wx.VERTICAL)
        for i in range(10):
            self.butList[i]=wx.Button(self.MenuPanel,i,str(i))
            self.butList[i].SetFont(font)
            self.butList[i].Bind(wx.EVT_BUTTON,self.OnButtonClick)
            menuBox1.Add(self.butList[i],0,wx.ALL,5)
        for i in range(10,14):
            self.butList[i]=wx.Button(self.MenuPanel,i,'')
            self.butList[i].SetFont(font)
            self.butList[i].Bind(wx.EVT_BUTTON,self.OnButtonClick)
            menuBox2.Add(self.butList[i],0,wx.ALL,5)
        self.butList[10].SetLabel("-->")
        self.butList[11].SetLabel("<--")
        self.butList[12].SetLabel("Delete")
        self.butList[13].SetLabel("Finish")
        vMenuBox.Add(menuBox1,0,wx.ALL,5)
        vMenuBox.Add(menuBox2,0,wx.ALL,5)
        self.MenuPanel.SetSizer(vMenuBox)
        
        #Menu Initialisation Ends...
        
        #Worksheet Initialisation Starts...
        
        self.WorkSheetPanel=wx.Panel(self.MainPanel,-1) # Worksheet panel
        x,y=300,150
        wx.StaticText(self.WorkSheetPanel,-1,'Enter The Number '+str(no)+" :",(x-100,y)).SetFont(font)
        self.num=wx.StaticText(self.WorkSheetPanel,-1,'0',(x,y+100))
        self.num.SetFont(font)
        
        # to get the height and width of a single digit in present fontsize
        wd,ht=self.num.GetSize()
        self.digitsize=wd
        self.y2=ht
        ht+=10
        self.num.SetLabel('0')
        self.x1,self.y1=0,0
        tmp,self.y2=self.num.GetSize()
        self.CurPos=0
        
        self.cursor=wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/HlineG.png'),pos=(0,0),size=(self.digitsize,5))
        self.cursorUp=wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/HlineG.png'),pos=(0,0),size=(self.digitsize,5))
        
        self.WorkSheetPanel.Bind(wx.EVT_PAINT,self.OnWorkSheetPaint)
        wx.EVT_LEFT_DOWN(self.MenuPanel,self.OnLeftClick) #Mouse Event
        wx.EVT_LEFT_DOWN(self.WorkSheetPanel,self.OnLeftClick) #Mouse Event
        wx.EVT_LEFT_DOWN(self.MainPanel,self.OnLeftClick) #Mouse Event
        self.WorkSheetPanel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)   #Key Event
        self.WorkSheetPanel.SetFocus()
        self.color='#33aa43'
        self.PaintLabel()
        (x,y)=wx.GetDisplaySize()
        self.WorkSheetPanel.SetSizeWH(x,y-200)
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.MenuPanel,0)
        vbox.Add(self.WorkSheetPanel,2)
        self.MainPanel.SetSizer(vbox)
        self.ShowFullScreen(True)
        self.Show(True)
        # WorkSheet Initialisation ends..
        self.ChangeButCur(None)
        self.MenuTimer.Start(self.speed) # Timer for Menu Cursor Movement,...
    # Menu Handlers Starts..
    def OnButtonClick(self,event):
        tmp=self.ButtonIndex
        self.ButtonIndex=event.GetId()
        tmpG=self.Group
        if self.ButtonIndex>9:
            self.Group=2
        else:
            self.Group=1
        self.OnLeftClick(None)
        self.ButtonIndex=tmp
        self.Group=tmpG
    def OnKeyDown(self,event):
        key=event.GetKeyCode()
        if key>=ord('0') and key<=ord('9'):
            self.OnDigitPress(str(key-ord('0')))
            self.CarryFlag=0
            self.PaintLabel()
    def OnMenuPaint(self,event):
        paint=wx.PaintDC(self.MenuPanel)
        paint.SetPen(wx.Pen('#000000'))
        paint.SetBrush(wx.Brush('#dd2222'))
        paint.DrawRoundedRectangle(self.Mx1,self.My1,self.wdt,self.ht,10)
    def OnLeftClick(self,event):
        if self.Group==0:
            self.Group=self.ButtonIndex+1
            self.ButtonIndex=self.ButtonIndex*10-1
            self.MenuTimer.Start(500)
        elif self.Group==1:
            #Digits Pressed
            self.OnDigitPress(str(self.ButtonIndex))
            self.Group=0
        elif self.Group==2:
            if self.ButtonIndex==10:  #-->
                txt=self.num.GetLabel()
                if self.CurPos<len(txt):
                    self.CurPos+=1
            elif self.ButtonIndex==11:  #<--
                if self.CurPos>0:
                    self.CurPos-=1
            elif self.ButtonIndex==12:  #Delete
                if len(self.num.GetLabel())-1>=self.CurPos:
                    txt=self.num.GetLabel()
                    txt=txt[:self.CurPos]+txt[self.CurPos+1:]
                    self.num.SetLabel(txt)
            else:                       #Exit
                #print self.GetInputNumber()
                self.Close()
            self.Group=0
        self.PaintLabel()
        self.WorkSheetPanel.SetFocus()
        self.ChangeButCur(None)
    def ChangeButCur(self,event):
        if self.Group==0:
            self.ButtonIndex=(self.ButtonIndex+1)%2
            self.Mx1,self.My1=self.butList[self.ButtonIndex*10].GetPosition()
            self.wdt,self.ht=self.butList[0].GetSize()  #for getting ht alone..
            self.Mx1,self.My1=self.Mx1-5,self.My1-5
            twd,tht=wx.GetDisplaySize()
            self.wdt,self.ht=twd-70,self.ht+10
        else:
            if self.Group==1:
                self.ButtonIndex=(self.ButtonIndex+1)%10
            else:
                self.ButtonIndex=(self.ButtonIndex+1-10)%(len(self.butList)-10)+10
            #Voice Playing...
            if self.butList[self.ButtonIndex].GetLabel()=="-->":
                snd=wx.Sound('files/voice/MoveRight.wav')
            elif self.butList[self.ButtonIndex].GetLabel()=="<--":
                snd=wx.Sound('files/voice/MoveLeft.wav')
            else:
                snd=wx.Sound('files/voice/'+self.butList[self.ButtonIndex].GetLabel()+'.wav')
            snd.Play()
            #Voice ends..
            self.Mx1,self.My1=self.butList[self.ButtonIndex].GetPosition()
            self.wdt,self.ht=self.butList[self.ButtonIndex].GetSize()
            self.Mx1,self.My1=self.Mx1-5,self.My1-5
            self.wdt,self.ht=self.wdt+10,self.ht+10
        self.Refresh()
        self.MenuTimer.Start(self.speed)
    # Menu Handlers Ends..
    
    # Worksheet Handlers starts..
    def GetInputNumber(self):
        return int(self.num.GetLabel())
    def OnWorkSheetPaint(self,event):
        dc=wx.PaintDC(self.WorkSheetPanel)
        dc.SetPen(wx.Pen('#dd0022'))
        dc.SetBrush(wx.Brush(self.color))
        #dc.DrawRectangle(self.x1,self.y1,self.fontsize,self.y2)
        self.cursor.SetPosition((self.x1,self.y1+self.y2-5))
        self.cursorUp.SetPosition((self.x1,self.y1))
    def PaintLabel(self):
        self.x1,self.y1=self.num.GetPosition()
        wd,ht=self.num.GetSize()
        if self.num.GetLabel()!='':
            wd=wd/len(self.num.GetLabel())
        self.x1+=self.CurPos*wd 
        self.Refresh()
    def OnDigitPress(self,digit):
        txt=self.num.GetLabel()
        txt=txt[:self.CurPos]+digit+txt[self.CurPos+1:]
        if len(txt)<=10:
            self.num.SetLabel(txt)
            self.CurPos+=1
if __name__=='__main__':
    app=wx.App()
    GetInput(None,-1,"Getting Input",30,2000,2)
    app.MainLoop()
