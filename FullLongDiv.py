
import wx,sys,random
    
class LongDiv(wx.Frame):
    def __init__(self,parent,id,title,nm1,nm2,fntsz,mnuspeed):
        #Menu Initialisation Starts..
        wx.Frame.__init__(self,parent,id,title)
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
        self.butList[14].SetLabel("Evaluate")
        self.butList[15].SetLabel("Exit")
        
        vMenuBox.Add(menuBox1,0,wx.ALL,5)
        vMenuBox.Add(menuBox2,0,wx.ALL,5)
        self.MenuPanel.SetSizer(vMenuBox)
        
        #Menu Initialisation Ends...
        
        # Worksheet Initialisation starts..
        """
        nm1 -- Dividend
        nm2 -- Divisor
        """
        num=(nm1/nm2)
        num=len(str(num))*2

        self.WorkSheetPanel=wx.Panel(self.MainPanel,-1) # Worksheet panel
        (x,y)=(250,50)
        self.LabelIndex=0
        self.LineIndex=0
        self.QuotientFlag=1
        self.ReverseFlag=0
        self.Line2Flag=0
        self.TxtCursor=0
        self.quo=wx.StaticText(self.WorkSheetPanel,-1,"0",(x+40,y+15))
        self.quo.SetFont(font)
        
        # to get the height and width of a single digit in present fontsize
        wd,ht=self.quo.GetSize()
        self.digitsize=wd
        self.y2=ht
        ht+=10
        self.quo.SetLabel("")
        wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/Hline.png'),pos=(x,y+60),size=(280,5))
        wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/Vline.png'),pos=(x,y+60),size=(5,100))
        self.divisor=wx.StaticText(self.WorkSheetPanel,-1,str(nm2),(x-45*2,y+65))
        self.divisor.SetFont(font)
        (x2,y2)=(x+40,y+65)
        (xdiff,ydiff)=(25,40)
        self.stList=[]
        self.lines=[]
        self.dividend=wx.StaticText(self.WorkSheetPanel,-1,str(nm1),(x2,y2))
        self.dividend.SetFont(font)
        j=0
        for i in range(num):
            if i%2==0 :
                self.stList.append(wx.StaticText(self.WorkSheetPanel,-1,pos=(x2,y2+ydiff)))
                self.stList[i].SetFont(font)
                self.lines.append(wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/Hline.png'),pos=(x2,y2+ydiff*2+5),size=(280,5)))
                self.lines[j].Show(False)
                y2+=ydiff+self.fontsize
                j+=1
            else:
                self.stList.append(wx.StaticText(self.WorkSheetPanel,-1,pos=(x2,y2+ydiff)))
                self.stList[i].SetFont(font)
                #x2+=xdiff
                y2+=ydiff
        self.x1,self.y1=0,0#self.quo.GetPosition()
        #self.x2,self.y2=self.quo.GetSize()
        
        self.cursor=wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/HlineG.png'),pos=(0,0),size=(self.digitsize,5))
        self.cursorUp=wx.StaticBitmap(self.WorkSheetPanel,-1,wx.Bitmap('files/HlineG.png'),pos=(0,0),size=(self.digitsize,5))
        self.WorkSheetPanel.Bind(wx.EVT_PAINT,self.OnWorkSheetPaint)
        wx.EVT_LEFT_DOWN(self.MenuPanel,self.OnLeftClick) #Mouse Event
        wx.EVT_LEFT_DOWN(self.WorkSheetPanel,self.OnLeftClick) #Mouse Event
        wx.EVT_LEFT_DOWN(self.MainPanel,self.OnLeftClick) #Mouse Event
        self.WorkSheetPanel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)   #Key Event
        self.WorkSheetPanel.SetFocus()
        self.PaintLabel()
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.MenuPanel,0)
        vbox.Add(self.WorkSheetPanel,0)
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
            self.OnDigitPress(key)
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
            #0-9 DIGITS
            self.OnDigitPress(ord(str(self.ButtonIndex)))
            self.Group=0
        elif self.Group==2:
            if self.ButtonIndex==10: #neXt
                self.OnNext()
            elif self.ButtonIndex==11: #preV
                self.OnPrev()
            elif  self.ButtonIndex==12: #-->
                self.OnKeyPress("+")
            elif  self.ButtonIndex==13: #<--
                self.OnKeyPress("-")
            elif self.ButtonIndex==14: #Done
                self.AnswerChecker()
            elif self.ButtonIndex==15:  #EXIT
                self.Close()
            self.Group=0
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
    
    #Worksheet Handlers Starts...

    def OnWorkSheetPaint(self,event):
        dc=wx.PaintDC(self.WorkSheetPanel)
        dc.SetPen(wx.Pen('#dd0022'))
        dc.SetBrush(wx.Brush('#33aa43'))
        #dc.DrawRectangle(self.x1,self.y1,self.x2,self.y2)
        self.cursor.SetPosition((self.x1,self.y1+self.y2-5))
        self.cursorUp.SetPosition((self.x1,self.y1))
    def PaintLabel(self):
        """
        To Highlight quotient or Static Labels
        """
        if self.QuotientFlag==1:
            objHandle=self.quo
        else:
            objHandle=self.stList[self.LabelIndex]
        if self.TxtCursor!=0:
            self.x1,self.y1=objHandle.GetPosition()
            self.x1+=(len(objHandle.GetLabel())+self.TxtCursor)*self.digitsize
            self.x2=self.fontsize#*5/4
        elif self.ReverseFlag==1:
            # for moving pointer in reverse
            self.x1,self.y1=self.stList[self.LabelIndex].GetPosition()
            prev=self.stList[self.LabelIndex-1].GetLabel()
            tmp=self.stList[self.LabelIndex].GetLabel()
            tmpLen=0
            if tmp!="":
                tmpLen=len(str(int(tmp)))
            self.x1+=(len(prev)-tmpLen-1)*self.digitsize
            self.x2=self.fontsize#*5/4
        elif self.Line2Flag==1 and self.stList[self.LabelIndex].GetLabel()==None:
            #pointer in the second line
            self.x1,self.y1=self.stList[self.LabelIndex].GetPosition()
            prev=self.stList[self.LabelIndex-1].GetLabel()
            prev1=""
            if prev!="":
                prev1=str(int(prev)) #removing zeros at the start..
            self.x1+=abs(len(prev)-len(prev1))*self.digitsize
            self.x2=self.fontsize#*5/4
        else:
            #general case...
            self.x1,self.y1=objHandle.GetPosition()
            self.x1+=len(objHandle.GetLabel())*self.digitsize
            self.x2=self.fontsize#*5/4
        self.y2=self.fontsize*3/2
        
        self.Refresh()
    
    def OnNext(self):
        #Enter Pressed -- update to next position
        self.TxtCursor=0
        if self.QuotientFlag==0:
            value=self.stList[self.LabelIndex].GetLabel()
        else:
            value=self.quo.GetLabel()
        if len(value.strip())==0:
            pass
        elif self.LabelIndex==(len(self.stList)-1):
            QuotientFlag=1
            self.PaintLabel()
            self.LabelIndex=0
        elif self.ReverseFlag==1: 
            #Subtraction finished now... bring down digit
            self.ReverseFlag=0
            self.PaintLabel()
        elif self.QuotientFlag==1:
            self.QuotientFlag=0
            self.PaintLabel()
        else :
            #updated line 1 or 2
                if self.LabelIndex%2==1:
                    self.LabelIndex+=1
                    self.Line2Flag=1
                    self.PaintLabel()
                else:
                    # to show line and next is subtraction (reverse) part
                    self.lines[self.LabelIndex/2].Show(True)
                    self.LabelIndex+=1
                    if len(self.stList[self.LabelIndex].GetLabel())==0:
                        self.ReverseFlag=1
                    self.PaintLabel()
                    #if self.LineIndex==(len(self.lines)-1):
                    #    self.LineIndex+=1  #line index increment....
    
    def OnPrev(self):
        self.TxtCursor=0
        self.ReverseFlag=0
        self.Line2Flag=0
        if self.LabelIndex==0:
            self.QuotientFlag=1
            self.PaintLabel()
        elif self.QuotientFlag==1:
            pass #search for last static line with value and place cursor there
        else:
            self.LabelIndex-=1
            self.PaintLabel()
        
        
    def OnDigitPress(self,ch):
        #Number Pressed
            if self.QuotientFlag==1:
                LabelHandle=self.quo
            else:
                LabelHandle=self.stList[self.LabelIndex]
            if self.TxtCursor==0 and self.ReverseFlag==0 and len(LabelHandle.GetLabel())>=len(self.dividend.GetLabel()):
                pass    # Avoiding overflow
            elif self.TxtCursor!=0:
                txt=LabelHandle.GetLabel()
                if self.TxtCursor==-1:
                    tmp=txt[:self.TxtCursor]+chr(ch)
                else:
                    tmp=txt[:self.TxtCursor]+chr(ch)+txt[self.TxtCursor+1:]
                LabelHandle.SetLabel(tmp)
            elif self.Line2Flag==1 and self.LabelIndex%2==0:
                # writing divisor quotient...
                prev=self.stList[self.LabelIndex-1].GetLabel()
                txt=LabelHandle.GetLabel()
                prev1=""
                if txt!='':
                    txt=str(int(txt))
                if prev!='':
                    prev1=str(int(prev))
                tmp='0'*(len(prev)-len(prev1))
                txt=tmp+txt+chr(ch)
                LabelHandle.SetLabel(txt)
                self.Line2Flag=0
            elif self.QuotientFlag==1 or self.ReverseFlag==0:
                #wrtining quo or general concat at end
                txt=LabelHandle.GetLabel()
                txt=txt+chr(ch)
                LabelHandle.SetLabel(txt)
            elif self.ReverseFlag==1:
                #reverse typing during subtraction
                prev=self.stList[self.LabelIndex-1].GetLabel()
                txt=LabelHandle.GetLabel()
                if txt!='':
                    txt=str(int(LabelHandle.GetLabel()))
                if len(prev)==len(txt): # Avoiding overflow
                    pass
                else:
                    txt=chr(ch)+txt
                    tmp='0'*(len(prev)-len(txt))
                    txt=tmp+txt
                    #print "Reverse:"+txt
                    LabelHandle.SetLabel(txt)
            # To Refresh Highlights..
            if self.QuotientFlag==1:
                self.PaintLabel()
            else:
                self.PaintLabel()
    def AnswerChecker(self):
        num1=int(self.dividend.GetLabel())
        num2=int(self.divisor.GetLabel())
        quo=int(self.quo.GetLabel())
        quostr=str(quo)
        if quo!=num1/num2:
            str2=str(num1/num2)
            for i in range(len(quostr)-1):
                if quostr[i]!=str2[i]:
                    break
            self.TxtCursor=i-(len(quostr)-1)
            #print self.TxtCursor
            self.QuotientFlag=1
            self.PaintLabel()
        else:
            for i in range(len(self.stList)):
                if self.stList[i].GetLabel()=="":
                    pass # NO Value
                else:
                    pass
    def OnKeyPress(self,ch):
        if ch=="+":
            if self.QuotientFlag==1:
                objHandle=self.quo
            else:
                objHandle=self.stList[self.LabelIndex]
            if self.TxtCursor==0:
                pass
            else:
                self.TxtCursor+=1
                self.PaintLabel()
        elif ch=="-":
            if self.QuotientFlag==1:
                objHandle=self.quo
            else:
                objHandle=self.stList[self.LabelIndex]
            if self.TxtCursor==-1*len(objHandle.GetLabel()):
                pass
            else:
                self.TxtCursor-=1
                self.PaintLabel()
            
        #self.dividend.SetLabel(str(ch))
        #print chr(ch)
        
        #Worksheet Handlers Ends...

#if len(sys.argv)!=3 or sys.argv[1]<sys.argv[2]:
#    print """
#   Usage: LongDiv.py Dividend Divisor
#    """
#numbers=map(int,sys.argv[1:3])
#frame=LongDiv(None,-1,"MathAssistant",numbers[0],numbers[1])
if __name__=='__main__':
    fileobj=open("files/input") #Input File
    if fileobj==None:
        #print "Error Opening Input File"
        exit()
    lst=fileobj.readlines()
    nm=lst[random.randint(0,len(lst)-1)].split(' ')
    while nm[0].strip()=="":
        nm=lst[random.randint(0,len(lst)-1)].split(' ')
        #print nm
    app=wx.App()
    frame=LongDiv(None,-1,"MathAssistant",int(nm[1]),int(nm[2]),20,2000)
    app.MainLoop()

	
