import wx,sys,random
import addition
import Multiplication
import subtraction
import lcm
import FullLongDiv
import GetInput
class MA(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title)
        self.MainPanel=wx.Panel(self,-1)
        self.Flag=0
        self.butList=range(3) #List of buttons...
        self.ButtonIndex=0 #Index Points to Current Active Button..
        self.MenuTimer=wx.Timer(self)
        self.Mx1,self.My1=0,0
        self.wdt,self.ht=0,0
        self.fontsize=30
        self.speed=9000
        self.num1=0
        self.num2=0
        self.Bind(wx.EVT_TIMER,self.ChangeButCur)
        self.MainPanel.Bind(wx.EVT_PAINT,self.OnMenuPaint)
        self.font=wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self.font.SetPointSize(self.fontsize)
        self.font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.font.SetFamily(wx.FONTFAMILY_DECORATIVE)
        self.question=wx.StaticText(self.MainPanel,-1,"Choose the size of letters and digits to be \ndisplayed (Present is Largest Size)",pos=(10,200))
        self.question.SetFont(self.font)
        tmpx,tmpy=wx.GetDisplaySize()
        wx.Button(self.MainPanel,-1,'About Math Assistant',pos=(tmpx-200,5)).Bind(wx.EVT_BUTTON,self.CreditsDialog)
        for i in range(3):
            self.butList[i]=wx.Button(self.MainPanel,i,'')
            self.butList[i].Bind(wx.EVT_BUTTON,self.OnButtonClick)
            self.butList[i].SetFont(self.font)
        x,y=20,400
        self.butList[0].SetLabel("Small")
        self.butList[1].SetLabel("Medium")
        self.butList[2].SetLabel("Large")
        maxx,maxy=wx.GetDisplaySize()
        for i in range(3):
            sz=len(self.butList[i].GetLabel())
            wd=30*sz+10
            self.font.SetPointSize(20+i*5)
            self.butList[i].SetFont(self.font)
            self.butList[i].SetSize((wd,60))
            if x+wd+20>maxx:
                y+=80
                x=20
            self.butList[i].SetPosition((x,y))
            x+=wd+20
        self.Bind(wx.EVT_CLOSE,self.OnExit)
        wx.EVT_LEFT_DOWN(self.MainPanel,self.OnLeftClick) #Mouse Event
        
        self.menuRefresh()
        self.Show()
        self.ShowFullScreen(True)
    def OnExit(self,event):
        self.Destroy()

     
    def OnMenuPaint(self,event):
        paint=wx.PaintDC(self.MainPanel)
        paint.SetPen(wx.Pen('#000000'))
        paint.SetBrush(wx.Brush('#dd2222'))
        paint.DrawRoundedRectangle(self.Mx1,self.My1,self.wdt,self.ht,10)
    def OnLeftClick(self,event):
        if self.Flag!=0:
            pass
        elif self.ButtonIndex==0:
            self.fontsize=20
        elif self.ButtonIndex==1:
            self.fontsize=25
        elif self.ButtonIndex==2:
            self.fontsize=30
        self.NextDialog1()
        #print "LeftClk 1 font:"
        #print self.fontsize
    def OnLeftClick2(self,event):
        if self.Flag!=1:
            pass
        elif self.ButtonIndex==0:
            self.speed=2000
        elif self.ButtonIndex==1:
            self.speed=3000
        elif self.ButtonIndex==2:
            self.speed=6000
        else:
            self.speed=9000
        #print "LeftClk 2 speed:"
        #print self.speed
        self.NextDialog2()
    def GetInputLast(self,event):
        obj=event.GetEventObject()
        self.num2=obj.GetInputNumber()
        obj.Destroy()
        self.LaunchModule()
    def GetInput(self,event):
        obj=event.GetEventObject()
        self.num1=obj.GetInputNumber()
        obj.Destroy()
        obj=GetInput.GetInput(self,-1,"Getting Input2",self.fontsize,self.speed,2)
        obj.Bind(wx.EVT_CLOSE,self.GetInputLast)
    def OnLeftClick3(self,event):
        if self.Flag!=2:
            pass
        elif self.ButtonIndex==5:
            self.Close()
        else:
            self.SoundFlag=1
            obj=GetInput.GetInput(self,-1,"Getting Input1",self.fontsize,self.speed,1)
            obj.Bind(wx.EVT_CLOSE,self.GetInput)
            self.MenuTimer.Stop()
        
    def LaunchModule(self):
        if self.num1<self.num2: #swapping Number.. num1 must be greater than num2
            tmp=self.num1
            self.num1=self.num2
            self.num2=tmp
        if self.ButtonIndex==0:
            obj=addition.addition(self,-1,"Addition",self.num1,self.num2,self.fontsize,self.speed)
            print 'after in addition'
        elif self.ButtonIndex==1:
            print 'before'
            obj=subtraction.subtraction(self,-1,"Subtraction",self.num1,self.num2,self.fontsize,self.speed)
            print 'after'
        elif self.ButtonIndex==2:
            obj=Multiplication.multiplication(self,-1,"Multiplication",self.num1,self.num2,self.fontsize,self.speed)
        elif self.ButtonIndex==3:
            obj=FullLongDiv.LongDiv(self,-1,"Long Division",self.num1,self.num2,self.fontsize,self.speed)
        elif self.ButtonIndex==4:
            obj=lcm.lcm(self,-1,"Least Common Multiple",self.num1,self.num2,self.fontsize,self.speed)
        obj.Bind(wx.EVT_CLOSE,self.StartTimer)

    def StartTimer(self,event):
        obj=event.GetEventObject()
        obj.Destroy()
        self.menuRefresh()
    def MathClose(self,event):
        self.Destroy()
    def NextDialog1(self):
        self.Flag=1
        self.question.SetLabel("Choose the Speed of Cursor Movement \n(Present cursor movement is the slowest)")
        self.butList[0].SetLabel("Fastest")
        self.butList[1].SetLabel("Fast")
        self.butList[2].SetLabel("Slow")
        self.butList.append(wx.Button(self.MainPanel,3,'Slower',size=(190,60)))
        self.butList[3].Bind(wx.EVT_BUTTON,self.OnButtonClick)
        self.font.SetPointSize(30)
        x,y=self.butList[0].GetPosition()
        maxx,maxy=wx.GetDisplaySize()
        for i in range(4):
            sz=len(self.butList[i].GetLabel())
            wd=30*sz+10
            self.butList[i].SetFont(self.font)
            self.butList[i].SetSize((wd,60))
            if x+wd+20>maxx:
                y+=80
                x=20
            self.butList[i].SetPosition((x,y))
            x+=wd+20
        self.menuRefresh()
        wx.EVT_LEFT_DOWN(self.MainPanel,self.OnLeftClick2) #Mouse Event

    def NextDialog2(self):
        self.Flag=2
        self.question.SetLabel("Choose the Chapter:")
        self.butList[0].SetLabel("Addition")
        self.butList[1].SetLabel("Subtraction")
        self.butList[2].SetLabel("Multiplication")
        self.butList[3].SetLabel("Division")
        self.butList.append(wx.Button(self.MainPanel,4,'LCM'))
        self.butList[4].Bind(wx.EVT_BUTTON,self.OnButtonClick)
        self.butList.append(wx.Button(self.MainPanel,5,'Exit'))
        self.butList[5].Bind(wx.EVT_BUTTON,self.OnExitClick)
        x,y=self.butList[0].GetPosition()
        maxx,maxy=wx.GetDisplaySize()
        for i in range(6):
            sz=len(self.butList[i].GetLabel())
            wd=30*sz+10
            self.butList[i].SetSize((wd,60))
            self.butList[i].SetFont(self.font)
            if x+wd+20>maxx:
                y+=80
                x=20
            self.butList[i].SetPosition((x,y))
            x+=wd+20
        self.menuRefresh()
        wx.EVT_LEFT_DOWN(self.MainPanel,self.OnLeftClick3) #Mouse Event
    def OnButtonClick(self,event):  #Button Click for menus.. selecting font, speed etc..
        tmp=self.ButtonIndex
        self.ButtonIndex=event.GetId()
        if self.Flag==0:
            self.OnLeftClick(None)
        elif self.Flag==1:
            self.OnLeftClick2(None)
        else:
            self.OnLeftClick3(None)
    def OnExitClick(self,event):
        self.Close()
    def menuRefresh(self):
        self.ButtonIndex=0
        self.Mx1,self.My1=self.butList[0].GetPosition()
        self.wdt,self.ht=self.butList[0].GetSize()
        self.Mx1,self.My1=self.Mx1-10,self.My1-10
        self.wdt,self.ht=self.wdt+20,self.ht+20
        snd=wx.Sound('files/voice/'+self.butList[self.ButtonIndex].GetLabel()+'.wav')
        snd.Play()
        self.Refresh()
        self.MenuTimer.Start(9000)
    
    def ChangeButCur(self,event):
        self.ButtonIndex=(self.ButtonIndex+1)%(len(self.butList))
        self.Mx1,self.My1=self.butList[self.ButtonIndex].GetPosition()
        self.wdt,self.ht=self.butList[self.ButtonIndex].GetSize()
        self.Mx1,self.My1=self.Mx1-10,self.My1-10
        self.wdt,self.ht=self.wdt+20,self.ht+20
        #Voice..
        snd=wx.Sound('files/voice/'+self.butList[self.ButtonIndex].GetLabel()+'.wav')
        snd.Play()
        #Ends..
        self.Refresh()
        self.MenuTimer.Start(9000)
    # Menu Handlers Ends..
    
    def CreditsDialog(self,event):
        
        description="""Math Assistant is a Comprehensive tool of speacially enabled children, 
providing a Math Worksheet Environment for easy way of solving simple Math problems.
        """
        license="""     Math Assistant is a free software;
You can redistribute it and/or modify it 
under the terms of the GNU General Public License 
as published by the Free Software Foundation; 
        """
        Mentors="""Mentors:
        Ranjini Parthasarathi
            (rp@annauniv.edu)
        T.V Geetha
            (rctamil@annauniv.edu)
        Bama S
            (bama@cs.annauniv.edu)
        """
        Devs="""Developers:
        Venkatanathan Varadarajan 
            (venk1989@gmail.com)
        VenkataKrishnan G
            (venkri2004@gmail.com)
        Sanath Kumar R
            (dayanandasaraswati@gmail.com)
        """
        info=wx.AboutDialogInfo()
        info.SetIcon(wx.Icon('files/math.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Math Assistant')
        info.SetVersion('2.0')
        info.SetDescription(description)
        info.SetCopyright('GNU General Public License')
        info.SetLicence(license)
        info.AddDeveloper(Mentors)
        info.AddDeveloper(Devs)
        wx.AboutBox(info)
        

def OnExit(event):
    ma=MA(None,-1,"Math Assistant")
    event.Skip()

if __name__=='__main__':
    app=wx.App()
    aBitmap = wx.Image(name = "files/MA.png").ConvertToBitmap()
    splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
    splashDuration = 2000 
    obj=wx.SplashScreen(aBitmap, splashStyle,splashDuration, None)
    wx.Yield()
    obj.Bind(wx.EVT_CLOSE,OnExit)
    app.MainLoop()
