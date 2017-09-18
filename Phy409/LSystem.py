#Gabriel Martinez
#PHY 409 final project. Jun 2016
#NEEDS A REVISION FORSURE. First project written in Python.
#Fixes: Alot of parsing methods im sure can be rewritten using regex.
# I was working in 2D space only. Need to project 2d corrdinates to 3d.
# This project will simulate a biological system using a mathematical framework called D0LSystem.
#A recursive mathematical model that is given a Axiom and productions that will produce derivations until 'n' generations. 
#More info on L-Systems see: https://en.wikipedia.org/wiki/L-system
import turtle as turtle
from tkinter import *
from math import *
from numpy import *
from queue import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from builtins import int, str
########################################Mathematical Framework to model biological system##########################################################
class LSystem:
    ##Input is in form of: (arg,arg2)
    #method extracts both arguments 1 and 2
    def toNumber(self,paran,i,chlist):#"("
            string=""
            for x in range(i,len(chlist)):
                    if chlist[x]==')':
                            i = x+1
                            a=string.split(',')
                            return float()
                    else:
                            string+=chlist[x]
            return float(string)
    def rotate(self,axis,theta):#3D functions dont work
            if axis=="Y":
                    m=self.currentPos
                    mr = m.dot(array([[cos(theta),0,sin(theta)],[0,1,0],[-sin(theta),0,cos(theta)]]))
                    self.currentPos=mr
            elif axis=="Z":
                    m=self.currentPos
                    mr = m.dot(array([[cos(theta),-sin(theta),0],[sin(theta),cos(theta),0],[0,0,1]]))
                    self.currentPos=mr
            return
        ######Meat of the class. This method draws from parsing the string or axioms. Uses Turtle language to draw to the screen.
    def drawLsystem(self,instructions):#, angle, distance):
            cmd=list(instructions)
            stack = []
            #for cmd in instructions:
            for i in range(len(cmd)):
                    if cmd[i] == 'F':#move forawrd Arg times
                            turtle.forward(self.getArg(i,cmd))
                    elif cmd[i]=="!":#change line width Arg size
                            turtle.width(self.getArg(i,cmd))
                    elif cmd[i]=="+":#turn right about v-axis
                            theta=self.getArg(i,cmd)
                            turtle.right(theta)
                    elif cmd[i]=='-':# turn left about v-axis
                            theta=self.getArg(i,cmd)
                            turtle.left(theta)
                    #elif cmd[i]=="/":# Roll left by Arg about L axis
                           # theta=self.getArg(i,cmd)
                            #self.rotate("Z", theta)
                            #covert 2D coordinated to 3d vector 
                            #xpos=
                            #ypos=
                    #elif cmd[i]=="\\":# Roll left by Arg about L axis
                            #theta=self.getArg(i,cmd)
                            #xpos=
                            #ypos=
                    elif cmd[i]=='[':
                            stack.append((turtle.position(), turtle.heading()))
                    elif cmd[i]==']':
                            position, heading = stack.pop()
                            turtle.penup()
                            turtle.setposition(position)
                            turtle.setheading(heading)
                            turtle.pendown()
                    #else:
                    #	print("Exceptions:: ",cmd[i])#raise ValueError('Unknown Cmd: {}'.format(ord(cmd[i])))
                    turtle.update()

# creates a new string. Or Derives a new string until base case for 'n' generations.
    def createLSystem(self,numIters,axiom,var,meso=True):
            self.meso = meso
            startString = axiom
            endString = ""
            for i in range(numIters):
                    endString = self.processString(startString,var)
                    startString = endString

            return endString
    def getParan(self,ch,i,chlist):
            for x in range(i,len(chlist)):
                    if chlist[x]==')':
                            return x

    def processString(self,oldStr,var):
            newstr = ""
            #for ch in oldStr:
            ch=list(oldStr)
            for i in range(len(ch)):
                    newstr = newstr + self.applyRules(ch[i],i,ch,var)
                    
            return newstr
    def getList(self,ch,i,chlist,var):#ch is A and i is the index of ch in chlist
            string=""
            for x in range(i+1,len(chlist)):
                    if chlist[x]==')':
                            list_a= string.split(',')
                            list_a.append(x)
                            return list_a
                    elif not chlist[x] == "(":
                            string+=chlist[x]
            return string.split(',')
    def getArg(self,i,chlist):#get x from A(x) or B(x) etc...	
            arg=""
            x=i+1
            while x <= len(chlist)-1:
                    if chlist[x]==')':
                            return float(arg)
                    if not chlist[x] =='(' and not chlist[x]==')':
                            arg+=chlist[x]
                    x+=1
            return float(arg)
        ##Derives a new string.
    def applyRules(self,ch,i,chlist,var):
            newstr = ""
            if self.meso:
                    if ch=='A':
                            arg = self.getArg(i,chlist)
                            newstr= '[-(80)F(10)B('+str(arg)+')][+(80)F(10)B('+str(arg)+')]F(10)A('+str(float(arg+1))+')'
                    elif ch=='B':
                            arg = self.getArg(i,chlist)
                            if arg>0:
                                    newstr='F(10)B('+str(float(arg-1))+')' 
                    else:
                            newstr=ch
                    return newstr
            if ch=='A':
                    a=self.getList(ch,i,chlist,var)
                    
                    if float(a[0])>=self.min_constant:#a[1]=w0 and a[0]=s
                            w=float(a[1])
                            s=float(a[0])
                            a1=self.alpha1
                            a2=self.alpha2
                            A1=s*self.r1
                            A2=s*self.r2
                            A12=w*(self.qq**self.e)
                            A22=w*((1-self.qq)**self.e)
                            y1=self.phi1
                            y2=self.phi2
                            newstr="!("+str(w)+")F("+str(s)+")[+("+str(a1)+")/("+str(y1)+")A("+str(A1)+","+str(A12)+")][+("+str(a2)+")/("+str(y2)+")A("+str(A2)+","+str(A22)+")]" #'!('+str(a[1])+')F('+str(a[0])+')'+'[+('+str(self.alpha1)+')/('+str(self.phi1)+')A('+str(float(a[0])*self.r1)+','+str(float(a[1])*(self.qq**self.e))+')]'+'[+('+str(self.alpha2)+')/('+str(self.phi2)+')A('+str(float(a[0])*self.r2)+','+str(float(a[1])*((1-self.qq)**self.e))+')]'
                   
                    
                    return newstr
            else:
                    newstr = ch    # no rules apply so keep the character
            return newstr
        ##Main method used to start the program from gui inputs.
    def main(self,r1=.75,r2=.77,alpha1=35,alpha2=-35,phi1=0,phi2=0,w0=30,qq=.50,e=.40,min_const=0.0, n=10  ):
        turtle.title("Final Project: Computational Biology: D0L-System")
        turtle.setup(1000,600,0,0)
        turtle.pendown()
        #turtle.left(90)#point straight up
        self.min_constant=min_const
        self.alpha1= alpha1
        self.phi1= phi1
        self.alpha2= alpha2
        self.phi2=phi2;

        self.r1=r1
        self.r2=r2

        self.e=e
        self.qq=qq
        self.w0=w0
        turtle.speed(0)

        turtle.mode("logo")

        self.currentPos= array([0,0,0])
        self.Location=list()
        self.Location.append(self.currentPos)

        string = "A(100,"+str(w0)+")"
        instructions=self.createLSystem(int(n),string,[1,1,1,1,1],False)#takes in a meso value
        print (instructions)
        self.drawLsystem(instructions)
        print("done")
        print ("Now trying to create a new window for mesotonic")
        opt = input("PRESS any button to continue. Note the screen will be overwritten")

        m = Mesotonic()
        m.main(r1,r2,alpha1,alpha2,phi1,phi2,w0,qq,e,min_const,int(n))

        #print("Coord: ",self.Location[:])
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(self.Location[:],self.Location[:])
        plt.show()
class Mesotonic:#Class not implemented
    def main(self,r1=.75,r2=.77,alpha1=35,alpha2=-35,phi1=0,phi2=0,w0=30,qq=.50,e=.40,min_const=0.0, n=10  ):
        turtle.title("Final Project: Computational Biology: Mesotonic")
        turtle.setup(1000,600,0,0)
        turtle.pendown()
        #turtle.left(90)#point straight up
        self.min_constant=min_const
        self.alpha1= alpha1
        self.phi1= phi1
        self.alpha2= alpha2
        self.phi2=phi2;

        self.r1=r1
        self.r2=r2

        self.e=e
        self.qq=qq
        self.w0=w0
        turtle.speed(0)

        turtle.mode("logo")
        string = "A(100,"+str(self.w0)+")" #"F(10)A(0)"	
        l = LSystem()
        instructions=l.createLSystem(10,string,[1,1,1,1,1], meso=True)
        print (instructions)
        l.drawLsystem(instructions)
        return
###################Display Window############################################
class Gui:
    # Begin to display a Frame with the options to vary the graphs
    def prob1(self):
        self.window_prob1=Toplevel()#the new GUI window for prob#1 HW 3
        self.window_prob1.protocol("WM_DELETE_WINDOW",self.close)
        Frame(self.window_prob1,width=600, height=0,takefocus=True).pack()	
        #end default Values

        Label(self.window_prob1,text="r1").pack()
        self.r1=Spinbox(self.window_prob1, from_=.0001,to=1)
        self.r1.pack()

        Label(self.window_prob1,text="r2").pack()
        self.r2=Spinbox(self.window_prob1, from_=.0001,to=1)
        self.r2.pack()

        Label(self.window_prob1,text="alpha1").pack()
        self.alpha1=Spinbox(self.window_prob1, from_=-100,to=1000)
        self.alpha1.pack()

        Label(self.window_prob1,text="alpha2").pack()
        self.alpha2=Spinbox(self.window_prob1, from_=-100,to=1000)
        self.alpha2.pack()

        Label(self.window_prob1,text="phi1").pack()
        self.phi1=Spinbox(self.window_prob1, from_=-100,to=1000)
        self.phi1.pack()
        Label(self.window_prob1,text="phi2").pack()
        self.phi2=Spinbox(self.window_prob1, from_=-100,to=1000)
        self.phi2.pack()
        Label(self.window_prob1,text="w0").pack()
        self.w0=Spinbox(self.window_prob1, from_=-100,to=1000)
        self.w0.pack()
        Label(self.window_prob1,text="q").pack()
        self.q=Spinbox(self.window_prob1, from_=.0001,to=1000)
        self.q.pack()
        Label(self.window_prob1,text="e").pack()
        self.e=Spinbox(self.window_prob1, from_=.0001,to=1000)
        self.e.pack()
        Label(self.window_prob1,text="min").pack()
        self.min_constant=Spinbox(self.window_prob1, from_=.001,to=1000)
        self.min_constant.pack()
        Label(self.window_prob1,text="n").pack()
        self.n =Spinbox(self.window_prob1, from_=0,to=100)
        self.n.pack()
        self.graph=Button(self.window_prob1,text="Simulate plant growth",command=self.plot)
        self.graph.pack()
        self.window_prob1.focus_set()#need this to make modal window
        self.window_prob1.grab_set()
        self.window_prob1.transient(self.window)
        self.window_prob1.wait_window(self.window_prob1)#end modal
        return	
	##########END OF PROB PYTHON FRAMES
	###########BEGIN OF FUNCTIONS TO GRAPH each PROBLEMS
    def plot(self):	
        lsys = LSystem()
        #lsys.main()
        lsys.main(float(self.r1.get()),float(self.r2.get()),float(self.alpha1.get()),float(self.alpha2.get()),float(self.phi1.get()),float(self.phi2.get()),int(self.w0.get()),float(self.q.get()),float(self.e.get()),float(self.min_constant.get()),int(self.n.get()))
        return

############################CONSTRUCTOR##############################
    def __init__(self,window):#MAIN WINDOW
        self.window = window
        window.title("Final Project: D0L-System")
        window.geometry("500x200")
        window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
        label = Label( window, text="Press one of the following options.", relief=RAISED ).pack()
        Button(window,text="Final Project: D0L-System",command=self.prob1).pack()
        return
    def on_closing(self):
        print("Program terminated.")
        root.destroy()	
        return
    def close(self):
        self.window_prob1.grab_release()
        self.window_prob1.withdraw()
        return
    ##############################################################################
    ######Program runs here#######################################################
root = Tk()
window = Gui(root)
root.protocol("WM_DELETE_WINDOW",window.on_closing)#close all graphs
root.mainloop()
