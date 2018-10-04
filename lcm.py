import wx

class lcm(wx.Frame):
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
        self.butList[14].SetLabel("Delete")
        self.butList[15].SetLabel("Exit")
        vMenuBox.Add(menuBox1,0,wx.ALL,5)
        vMenuBox.Add(menuBox2,0,wx.ALL,5)
        self.MenuPanel.SetSizer(vMenuBox)
        
        #Menu Initialisation Ends...
        
        #Worksheet Initialisation Starts...
        
        self.WorkSheetPanel=wx.Panel(self.MainPanel,-1) # Worksheet panel
        x,y=200,150
        self.pic=wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/default.png'),pos=(700,200))
        self.num1=wx.StaticText(self.WorkSheetPanel,-1,'0',(x,y))
        self.num1.SetFont(font)
        
        # to get the height and width of a single digit in present fontsize
        wd,ht=self.num1.GetSize()
        self.digitsize=wd
        self.y2=ht
        ht+=10
        self.num1.SetLabel(str(nm1))
        
        self.num2=wx.StaticText(self.WorkSheetPanel,-1,str(nm2),(x+300,y))
        self.num2.SetFont(font)
        self.x1,self.y1=0,0
        wd,ht=self.num1.GetSize()
        self.y2=ht
        ht+=10
        self.Factors=range(2)
        self.Factors[0]=self.FindFactors(nm1)
        self.Factors[1]=self.FindFactors(nm2)
        self.maxsz=len(str(max(nm1,nm2)));
        self.fac=range(2)
        self.vals=range(2)
        self.vals[0]=range(len(self.Factors[0])-1)
        self.fac[0]=range(len(self.Factors[0])-1)
        self.vals[1]=range(len(self.Factors[1])-1)
        self.fac[1]=range(len(self.Factors[1])-1)
        factsz=range(2) # for setting the size between factor static texts and vals static txts
        factsz[0]=len(str(max(self.Factors[0])))+1
        factsz[1]=len(str(max(self.Factors[1])))+1
        for j in (0,1):
            #j used for seperation of two numbers...
            for i in range(len(self.Factors[j])-1):
                self.fac[j][i]=wx.StaticText(self.WorkSheetPanel,-1,'',((x-self.fontsize*factsz[j]-15)+j*300,y+i*ht))
                self.fac[j][i].SetFont(font)
                self.vals[j][i]=wx.StaticText(self.WorkSheetPanel,-1,'',((x)+j*300,y+(i+1)*ht))
                self.vals[j][i].SetFont(font)
        self.DrawLCMLines(x,y,len(str(nm1)))
        x+=300
        self.DrawLCMLines(x,y,len(str(nm2)))
        
        self.stIndex=0  #Index used for Static Text lists... self.fac and self.vals..
        
        self.CurPos=0   # Cursor from starting... CurPos is maintained positive
        
        #Flags used.. NmFlag for num 0 or num 1
        self.NmFlag=0
        #FactorFlag==1 when the cursor is in factor area... else 0
        self.FactorFlag=1
        
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
        
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.MenuPanel,0)
        vbox.Add(self.WorkSheetPanel,0)
        self.MainPanel.SetSizer(vbox)
        #self.WorkSheetPanel.SetFocus()
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
            if self.ButtonIndex==10:  #Next
                if self.FactorFlag==1:
                    if self.fac[self.NmFlag][self.stIndex].GetLabel()!='':
                        self.FactorFlag=0
                        self.CurPos=len(self.vals[self.NmFlag][self.stIndex].GetLabel())
                else:
                    if self.NmFlag==0 and self.stIndex==len(self.fac[0])-1: # to move to number 2
                        self.stIndex=0
                        self.NmFlag=1
                        self.FactorFlag=1
                    elif self.vals[self.NmFlag][self.stIndex].GetLabel()!='':
                        self.FactorFlag=1
                        # Drawing LCM Lines..
                        if self.stIndex<len(self.fac[self.NmFlag])-1:
                            x,y=self.vals[self.NmFlag][self.stIndex].GetPosition()
                            prevLen=len(self.vals[self.NmFlag][self.stIndex].GetLabel())
                            self.DrawLCMLines(x,y,prevLen)
                        # Incrementing index..
                        self.stIndex=(self.stIndex+1)%len(self.fac[self.NmFlag])
                    self.CurPos=self.CurPos=len(self.fac[self.NmFlag][self.stIndex].GetLabel())
            elif self.ButtonIndex==11:  #Prev
                if self.FactorFlag==1:
                    self.FactorFlag=0
                    if self.stIndex!=0:
                        self.stIndex-=1
                    elif self.NmFlag==1:    # to move to number 1
                        self.NmFlag=0
                        self.stIndex=len(self.fac[self.NmFlag])-1
                    self.CurPos=self.CurPos=len(self.vals[self.NmFlag][self.stIndex].GetLabel())
                else:
                    self.FactorFlag=1
                    self.CurPos=len(self.fac[self.NmFlag][self.stIndex].GetLabel())
            elif self.ButtonIndex==12:  #-->
                if self.FactorFlag==1:
                    txt=self.fac[self.NmFlag][self.stIndex].GetLabel()
                else:
                    txt=self.vals[self.NmFlag][self.stIndex].GetLabel()
                if self.CurPos<len(txt):
                    self.CurPos+=1
                    #print "as"
                #print self.CurPos
                #print "#"
                #print len(txt)
            elif self.ButtonIndex==13:  #<--
                if self.CurPos>0:
                    self.CurPos-=1
            elif self.ButtonIndex==14:  #Delete
                if self.FactorFlag==1:
                    LabelObj=self.fac[self.NmFlag][self.stIndex]
                else:
                    LabelObj=self.vals[self.NmFlag][self.stIndex]
                if len(LabelObj.GetLabel())-1>=self.CurPos:
                    txt=LabelObj.GetLabel()
                    txt=txt[:self.CurPos]+txt[self.CurPos+1:]
                    LabelObj.SetLabel(txt)
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
    def DrawLCMLines(self,x,y,prevNumLen):
        wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/Vline.png'),pos=(x-10,y),size=(5,self.fontsize+20))
        wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/Hline.png'),pos=(x-10,y+self.fontsize+20),size=((prevNumLen)*self.fontsize+20,5))
    
    def FindFactors(self,nm):
        tmp=nm
        count=0
        Fact_list=[]
        i=2
        while tmp!=0 and tmp>i:
            if tmp%i==0:
                Fact_list.append(i)
                count+=1
                tmp=tmp/i
            else:
                i+=1
        if tmp!=0:
            Fact_list.append(tmp)
            count+=1
        return (Fact_list)

    def OnWorkSheetPaint(self,event):
        dc=wx.PaintDC(self.WorkSheetPanel)
        dc.SetPen(wx.Pen('#dd0022'))
        dc.SetBrush(wx.Brush(self.color))
        #dc.DrawRectangle(self.x1,self.y1,self.fontsize,self.y2)
        self.cursor.SetPosition((self.x1,self.y1+self.y2-5))
        self.cursorUp.SetPosition((self.x1,self.y1+3))
    def PaintLabel(self):
        if self.FactorFlag==1:
            LabelObj=self.fac[self.NmFlag][self.stIndex]
        else:
            LabelObj=self.vals[self.NmFlag][self.stIndex]
        self.x1,self.y1=LabelObj.GetPosition()
        wd,ht=LabelObj.GetSize()
        if LabelObj.GetLabel()!='':
            wd=wd/len(LabelObj.GetLabel())
        self.x1+=self.CurPos*wd 
        self.Refresh()
    
    def OnDigitPress(self,digit):
        if self.FactorFlag==1:
            LabelObj=self.fac[self.NmFlag][self.stIndex]
        else:
            LabelObj=self.vals[self.NmFlag][self.stIndex]
        txt=LabelObj.GetLabel()
        if len(txt)<(self.maxsz-self.FactorFlag):
            txt=txt[:self.CurPos]+digit+txt[self.CurPos+1:]
            LabelObj.SetLabel(txt)
            self.CurPos+=1
        
if __name__=='__main__':
    app=wx.App()
    lcm(None,-1,"Least Common Multiple",320,126,30,2000)
    app.MainLoop()
