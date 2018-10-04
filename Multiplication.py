import wx

class multiplication(wx.Frame):
    def __init__(self,parent,id,title,nm1,nm2,fntsz,mnuspeed):
        wx.Frame.__init__(self,parent,id,title)
        #Menu Initialisation Starts..
        self.fontsize=fntsz
        self.speed=mnuspeed
        self.MainPanel=wx.Panel(self,-1)#Main Panel Contains .. MenuPanel+WorksheetPanel
        
        self.butList=range(16) #List of buttons...
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
        for i in range(10,16):
            self.butList[i]=wx.Button(self.MenuPanel,i,'')
            self.butList[i].SetFont(font)
            self.butList[i].Bind(wx.EVT_BUTTON,self.OnButtonClick)
            menuBox2.Add(self.butList[i],0,wx.ALL,5)
        self.butList[10].SetLabel("Next")
        self.butList[11].SetLabel("Previous")
        self.butList[12].SetLabel("-->")
        self.butList[13].SetLabel("<--")
        self.butList[14].SetLabel("GotoCarry")
        self.butList[15].SetLabel("Exit")
        vMenuBox.Add(menuBox1,0,wx.ALL,5)
        vMenuBox.Add(menuBox2,0,wx.ALL,5)
        self.MenuPanel.SetSizer(vMenuBox)
        
        #Menu Initialisation Ends...
        # WorkSheet Initialisation Starts..
        self.WorkSheetPanel=wx.Panel(self.MainPanel,-1) # Worksheet panel
        x,y=300,75
        self.maxsz=len(str(nm1*nm2))   #maximum length of the static texts
        self.sz=len(str(nm2))
        self.stList=range(self.sz+1)
        self.pic=wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/default.png'),pos=(600,200))
        self.num1=wx.StaticText(self.WorkSheetPanel,-1,'0',(x,y))
        self.num1.SetFont(font)
        
        # to get the height and width of a single digit in present fontsize
        wd,ht=self.num1.GetSize()
        self.digitsize=wd
        self.y2=ht
        ht+=10
        self.num1.SetLabel(str(nm1))
        #finished getting ht and wd

        self.num2=wx.StaticText(self.WorkSheetPanel,-1,str(nm2),(x,y+ht))
        self.num2.SetFont(font)

        # for positioning the num1 and num2 reverse direcn..
        tx,ty=self.num1.GetPosition()
        wd,tmp=self.num1.GetSize()
        tx+=(self.digitsize*self.maxsz-wd)
        self.num1.SetPosition((tx,ty))      
        self.carry1=wx.StaticText(self.WorkSheetPanel,-1,'',(tx,ty-ht)) # carry 1
        self.carry1.SetFont(font)
        tx,ty=self.num2.GetPosition()
        wd,tmp=self.num2.GetSize()
        tx+=(self.digitsize*self.maxsz-wd)
        self.num2.SetPosition((tx,ty))      
        wx.StaticText(self.WorkSheetPanel,-1,'x',(tx-self.digitsize*2,ty)).SetFont(font)
        #positioning ends..
        wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/Hline.png'),pos=(x,y+ht*2),size=(self.digitsize*self.maxsz,5))
        self.carry2=wx.StaticText(self.WorkSheetPanel,-1,'',(x,y+ht*2+10))
        self.carry2.SetFont(font)
        self.carry=None #to be used transperently for carry1 or carry2..
        y+=(ht*3+10)
        for i in range(self.sz):
            self.stList[i]=wx.StaticText(self.WorkSheetPanel,-1,'',(x,y+ht*i))
            self.stList[i].SetFont(font)
        self.stList[0].SetLabel('0'*self.maxsz)
        self.lines=range(2)
        self.lines[0]=wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/Hline.png'),pos=(x,y+ht*(i+1)+10),size=(self.digitsize*self.maxsz,5))
        self.stList[i+1]=wx.StaticText(self.WorkSheetPanel,-1,'',(x,y+ht*(i+1)+20))    #ans label
        self.stList[i+1].SetFont(font)
        self.lines[1]=wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/Hline.png'),pos=(x,y+ht*(i+2)+60),size=(self.digitsize*self.maxsz,5))
        self.lines[0].Show(False)
        self.lines[1].Show(False)
        self.x1,self.y1=0,0
        self.CarryFlag=0
        self.CurPos=-1
        self.prevCurPos=-1
        self.stIndex=0
        self.cursor=wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/HlineG.png'),pos=(0,0),size=(self.fontsize,5))
        self.cursorUp=wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/HlineG.png'),pos=(0,0),size=(self.fontsize,5))
        self.WorkSheetPanel.Bind(wx.EVT_PAINT,self.OnWorkSheetPaint)
        wx.EVT_LEFT_DOWN(self.MenuPanel,self.OnLeftClick) #Mouse Event
        wx.EVT_LEFT_DOWN(self.WorkSheetPanel,self.OnLeftClick) #Mouse Event
        wx.EVT_LEFT_DOWN(self.MainPanel,self.OnLeftClick) #Mouse Event
        self.WorkSheetPanel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)   #Key Event
        self.WorkSheetPanel.SetFocus()
        self.color='#33aa43'
        self.PaintLabel()
        
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.MenuPanel,0)
        vbox.Add(self.WorkSheetPanel,0)
        self.MainPanel.SetSizer(vbox)
        #self.WorkSheetPanel.SetFocus()
        self.ShowFullScreen(True)
        self.Show(True)
        # WorkSheet Initialisation ends..
        self.MenuTimer.Start(self.speed) # Timer for Menu Cursor Movement,...
        self.ChangeButCur(None)
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
            if self.CarryFlag==1:
                self.CurPos=self.prevCurPos
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
            self.OnDigitPress(str(self.ButtonIndex))
            if self.CarryFlag==1:
                self.CurPos=self.prevCurPos
            self.CarryFlag=0
            self.Group=0
        elif self.Group==2:
            if self.ButtonIndex==12:  #-->
                if self.CurPos<0:
                    self.CurPos+=1
                
            elif self.ButtonIndex==13:  #<--
                if self.CarryFlag!=1:   # when its not in the carry 1
                    if self.CurPos>=(-1*self.maxsz):
                        self.CurPos-=1
                else:
                    if self.CurPos>=(-1*len(self.num1.GetLabel())):
                        self.CurPos-=1
                
            elif self.CarryFlag!=0:
                # if carry is being filled ONLY digits, <-- & --> must be processed
                pass
            elif self.ButtonIndex==10:  #Next
                self.CurPos=-1
                if self.stIndex+1==self.sz:
                    self.lines[0].Show(True)
                    self.lines[1].Show(True)
                    self.stIndex+=1
                elif self.stList[self.stIndex].GetLabel()!='':
                    self.stIndex=(self.stIndex+1)%(self.sz+1)
                    
                if self.stList[self.stIndex].GetLabel()=='':    #filling with zeros if label-empty
                    self.stList[self.stIndex].SetLabel('0'*self.maxsz)
            elif self.ButtonIndex==11:  #Prev
                self.CurPos=-1
                if self.stIndex!=0:
                    self.stIndex=(self.stIndex-1)%self.sz
                
            elif self.ButtonIndex==14:  #Goto Carry
                if self.stIndex==self.sz:
                    self.carry=self.carry2  # carry during addition to get final result..
                    if self.carry.GetLabel()=='':    #filling with zeros if label-empty
                        self.carry.SetLabel('0'*self.maxsz)
                    self.CarryFlag=2
                else:
                    self.carry=self.carry1  #for carry during multiplication
                    if self.carry.GetLabel()=='':    #filling with zeros if label-empty
                        self.carry.SetLabel('0'*len(self.num1.GetLabel()))
                    self.CarryFlag=1
                    self.prevCurPos=self.CurPos
                    self.CurPos=-1
            elif self.ButtonIndex==15:
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
    def OnWorkSheetPaint(self,event):
        dc=wx.PaintDC(self.WorkSheetPanel)
        dc.SetPen(wx.Pen('#dd0022'))
        dc.SetBrush(wx.Brush(self.color))
        #dc.DrawRectangle(self.x1,self.y1,self.digitsize,self.y2)
        self.cursor.SetPosition((self.x1,self.y1+self.y2-5))
        self.cursorUp.SetPosition((self.x1,self.y1))
    def PaintLabel(self):
        if self.CarryFlag!=0:
            LabelObj=self.carry
        else:
            LabelObj=self.stList[self.stIndex]
        self.x1,self.y1=LabelObj.GetPosition()
        wd,ht=LabelObj.GetSize()
        self.x1+=wd
        self.x1+=(self.CurPos*self.digitsize) # note: CurPos is -ve
        self.Refresh()
    def OnDigitPress(self,digit):
        if self.CarryFlag!=0:
            LabelObj=self.carry
        else:
            LabelObj=self.stList[self.stIndex]
        txt=LabelObj.GetLabel() 
        if self.CurPos==-1:
            txt=txt[:-1]+digit
        else:
            txt=txt[:self.CurPos]+digit+txt[self.CurPos+1:]
        if self.CurPos>=(-1*self.maxsz) and self.CarryFlag==0:
            self.CurPos-=1
        if self.CarryFlag!=1:
            txt='0'*(self.maxsz-len(txt))+txt
        LabelObj.SetLabel(txt)
if __name__=='__main__':
    app=wx.App()
    multiplication(None,-1,"Multiplication",63221,192,30,2000)
    app.MainLoop()
