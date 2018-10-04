import wx

class addition(wx.Frame):
    def __init__(self,parent,id,title,nm1,nm2,fntsz,mnuspeed):
        wx.Frame.__init__(self,parent,id,title)
        #Menu Initialisation Starts..
        self.fontsize=fntsz
        self.speed=mnuspeed
        self.MainPanel=wx.Panel(self,-1)#Main Panel Contains .. MenuPanel+WorksheetPanel
        
        self.butList=range(15) #List of buttons...
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
        for i in range(10,15):
            self.butList[i]=wx.Button(self.MenuPanel,i,'')
            self.butList[i].SetFont(font)
            self.butList[i].Bind(wx.EVT_BUTTON,self.OnButtonClick)
            menuBox2.Add(self.butList[i],0,wx.ALL,5)
        self.butList[10].SetLabel("-->")
        self.butList[11].SetLabel("<--")
        self.butList[12].SetLabel("GotoCarry")
        self.butList[13].SetLabel("Evaluate")
        self.butList[14].SetLabel("Exit")
        vMenuBox.Add(menuBox1,0,wx.ALL,5)
        vMenuBox.Add(menuBox2,0,wx.ALL,5)
        self.MenuPanel.SetSizer(vMenuBox)
        
        #Menu Initialisation Ends...
        
        #Worksheet Initialisation Starts...
        
        self.WorkSheetPanel=wx.Panel(self.MainPanel,-1) # Worksheet panel
        x,y=300,150
        self.maxsz=-1*len(str(nm1)) #Used for CurPos
        num1=str(nm1)
        num2='0'*(len(str(nm1))-len(str(nm2)))+str(nm2)
        self.pic=wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/default.png'),pos=(600,200))
        self.carry=wx.StaticText(self.WorkSheetPanel,-1,'0'*abs(self.maxsz),(x,y))
        self.num1=wx.StaticText(self.WorkSheetPanel,-1,'0',(x,y+50))
        self.num1.SetFont(font)
        
        # to get the height and width of a single digit in present fontsize
        wd,ht=self.num1.GetSize()
        self.digitsize=wd
        self.y2=ht
        ht+=10
        self.num1.SetLabel(num1)
        self.num2=wx.StaticText(self.WorkSheetPanel,-1,num2,(x,y+50*2))
        wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/Hline.png'),pos=(x,y+50*3+10),size=(self.digitsize*5,5))
        self.ans=wx.StaticText(self.WorkSheetPanel,-1,'0'*abs(self.maxsz),(x,y+50*4+10*2))
        x,y=self.num2.GetPosition()
        wx.StaticText(self.WorkSheetPanel,-1,'+',(x-self.fontsize,y)).SetFont(font)
        self.carry.SetFont(font)
        self.num1.SetFont(font)
        self.num2.SetFont(font)
        self.ans.SetFont(font)
        self.cursor=wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/HlineG.png'),pos=(0,0),size=(self.digitsize,5))
        self.cursorUp=wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/HlineG.png'),pos=(0,0),size=(self.digitsize,5))
        self.x1,self.y1=0,0
        tmp,self.y2=self.num1.GetSize()
        self.CarryFlag=0
        self.CurPos=-1
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
        self.ShowFullScreen(True)
        self.Show(True)
        self.ChangeButCur(None)
        # WorkSheet Initialisation ends..
        
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
            self.CarryFlag=0
            self.Group=0
        elif self.Group==2:
            if self.ButtonIndex==10:  #-->
                if self.CurPos<-1:
                    self.CurPos+=1
            elif self.ButtonIndex==11:  #<--
                if self.CurPos>self.maxsz-1:
                    self.CurPos-=1
            elif self.ButtonIndex==12:  #Goto Carry
                if self.CurPos==self.maxsz-1:
                    self.CurPos=self.maxsz
                self.CarryFlag=1
            elif self.ButtonIndex==13:  #Evaluate
                self.Evaluate()
            else:                       #Exit
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
        #dc.DrawRectangle(self.x1,self.y1,self.fontsize,self.y2)
        self.cursor.SetPosition((self.x1,self.y1+self.y2-5))
        self.cursorUp.SetPosition((self.x1,self.y1))
    def PaintLabel(self):
        if self.CarryFlag==1:
            LabelObj=self.carry
        else:
            LabelObj=self.ans
        self.x1,self.y1=LabelObj.GetPosition()
        wd,ht=LabelObj.GetSize()
        self.x1+=wd
        
        if self.CurPos!=0:
            self.x1+=self.CurPos*self.digitsize  # note CurPos is -ve
        else:
            txt=str(int(LabelObj.GetLabel()))
            self.x1-=len(txt)*self.digitsize
        self.Refresh()
    def Evaluate(self):
        i=-1
        carry=self.carry.GetLabel()
        num1=self.num1.GetLabel()
        num2=self.num2.GetLabel()
        ans=self.ans.GetLabel()
        tmp_ans=0
        calc_ans=''
        tmp_carry='0'
        while True:
            tmp_ans=int(num1[i])+int(num2[i])+int(tmp_carry[i])
            if tmp_ans>9:
                tmp_carry=str(tmp_ans)[0]+tmp_carry
                tmp_ans=str(tmp_ans)[1]
            else:
                tmp_carry='0'+tmp_carry
                tmp_ans=str(tmp_ans)[0]
            calc_ans=str(tmp_ans)+calc_ans
            if ans[i]!=tmp_ans or carry[i]!=tmp_carry[i]:
                break
            elif i==self.maxsz:
                if tmp_carry[0]!='0':
                    i-=1
                    tmp_ans=tmp_carry[0]
                    tmp_carry=tmp_carry[1:]
                    calc_ans=str(tmp_ans)+calc_ans
                else:
                    tmp_carry=tmp_carry[1:]
                break
            i-=1
        if i<=self.maxsz and ans==calc_ans and tmp_carry==carry:
            self.pic.SetBitmap(wx.Bitmap('files/correct.png'))
        else:
            if tmp_carry!=carry:
                self.x1,self.y1=self.carry.GetPosition()
                self.y2*=4
            else:
                self.x1,self.y1=self.num1.GetPosition()
                self.y2*=3
            if i==self.maxsz-1:
                self.x1,self.y1=self.ans.GetPosition()
            x,y=self.num1.GetSize()
            self.x1+=x
            self.x1+=i*self.fontsize
            self.color='#aa1109'
            self.Refresh()
            self.pic.SetBitmap(wx.Bitmap('files/wrong.png'))
        print tmp_carry
       	print carry
        print tmp_ans
        print ans[i]
        print calc_ans
        print ans
        
    def OnDigitPress(self,digit):
        
        if self.CarryFlag==1:
            LabelObj=self.carry
        else:
            LabelObj=self.ans
        txt=LabelObj.GetLabel() #to remove leading zeros
        if self.CurPos==-1:
            txt=txt[:-1]+digit
        else:
            txt=txt[:self.CurPos]+digit+txt[self.CurPos+1:]
        if self.CurPos>self.maxsz-1 and self.CarryFlag==0:
            self.CurPos-=1
        tmp='0'*(abs(self.maxsz)-len(txt))+txt
        LabelObj.SetLabel(tmp)
if __name__=='__main__':
    app=wx.App()
    addition(None,-1,"Addition",3221,792,30,2000)
    app.MainLoop()
