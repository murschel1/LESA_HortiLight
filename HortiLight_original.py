from Tkinter import *
from PIL import ImageTk, Image
import time
import numpy as np
import socket
import sys
import datetime
import RPi.GPIO as GPIO

#TCP/IP related
TCP_IP = '192.168.0.249'
TCP_PORT = 50000
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


FanStatus = 0
EnaStatus = 0
AllStatus = 0
StaStatus = 0
data = ['']
LineNumber = 0


def EN_CallBack():
  global EnaStatus
  global s
  if EnaStatus == 0:
    EnaStatus = 1
    s.send('DIS')
    EN_Button.configure(text = "Enable LED")
  else:
    EnaStatus = 0 
    s.send('ENA')
    EN_Button.configure(text = 'Disabled LED')

def Al_CallBack():
  global AllStatus
  global EnaStatus
  global s
  if AllStatus == 0:
    AllStatus = 1
    EnaStatus = 0 
    s.send('ENA')
    EN_Button.configure(text = 'Disable LED')
    time.sleep(0.5)
    s.send('UVX 100')
    W_UV.set(100)
    time.sleep(0.5)
    s.send('DBL 99')
    W_DB.set(100)
    time.sleep(0.5)
    s.send('BLU 99')
    W_BL.set(100)
    time.sleep(0.5)
    s.send('GRE 99')
    W_GR.set(100)
    time.sleep(0.5)
    s.send('RED 99')
    W_RE.set(100)
    time.sleep(0.5)
    s.send('IRX 99')
    W_IR.set(100)
    DI_Button.configure(text = 'All off')
  else:
    s.send('UVX 0')
    W_UV.set(0)
    time.sleep(0.5)
    s.send('DBL 0')
    W_DB.set(0)
    time.sleep(0.5)
    s.send('BLU 0')
    W_BL.set(0)
    time.sleep(0.5)
    s.send('GRE 0')
    W_GR.set(0)
    time.sleep(0.5)
    s.send('RED 0')
    W_RE.set(0)
    time.sleep(0.5)
    s.send('IRX 0')
    W_IR.set(0)
    time.sleep(0.5)
    s.send('DIS')
    AllStatus = 0
    EnaStatus = 1
    
    EN_Button.configure(text = "Enable LED")
    DI_Button.configure(text = 'All on')

def FA_CallBack():
  global FanStatus
  global s
  if FanStatus == 0:
    FanStatus = 1
  else:
    FanStatus = 0
  s.send('FAN %d'%FanStatus)

def ST_CallBack():
  global StaStatus
  global s
  global data
  global LineNumber
  if StaStatus == 0:
    StaStatus = 1
    s.send('ENA')
    ST_Button.configure(text = "Stop", bg = 'red')
    EN_Button.configure(state = DISABLED)
    DI_Button.configure(state = DISABLED)
    FA_Button.configure(state = DISABLED)
    try:
      file = open("Data.txt", "r")
      data = file.readlines()
      LineNumber = len(data)
      close(file)
    except:
      print 'No such file' 
  else:
    StaStatus = 0 
    ST_Button.configure(text = "Start", bg = 'green')
    EN_Button.configure(state = ACTIVE)
    DI_Button.configure(state = ACTIVE)
    FA_Button.configure(state = ACTIVE)
    W_UV.configure(state = ACTIVE)
    W_DB.configure(state = ACTIVE)
    W_BL.configure(state = ACTIVE)
    W_GR.configure(state = ACTIVE)
    W_RE.configure(state = ACTIVE)
    W_IR.configure(state = ACTIVE)
    W_UV.set(0)
    W_DB.set(0)
    W_BL.set(0)
    W_GR.set(0)
    W_RE.set(0)
    W_IR.set(0)
    s.send('DIS')

def UV_CallBack(event):
  global s
  s.send('UVX %f'%W_UV.get())

def DB_CallBack(event):
  global s
  s.send('DBL %f'%W_DB.get())

def BL_CallBack(event):
  global s
  s.send('BLU %f'%W_BL.get())


def GR_CallBack(event):
  global s
  s.send('GRE %f'%W_GR.get())


def RE_CallBack(event):
  global s
  s.send('RED %f'%W_RE.get())

def IR_CallBack(event):
  global s
  s.send('IRX %f'%W_IR.get())



#Implementation of GUI
root = Tk()
root.attributes('-fullscreen', True)
root.configure(background = "White")

#LESA banner
Banner_Frame = Frame(root)
Banner_Frame.pack(side = TOP)
LESA_b = ImageTk.PhotoImage(Image.open("LESA.png"))
Banner = Label(Banner_Frame, image = LESA_b, bg = 'white', highlightbackground = 'white')
Banner.pack()

#Frame with sliders and buttons
Second_Frame = Frame(root, bg = 'white')
Second_Frame.pack(side = TOP)

#Frame for temperature
Temperature_Frame = Frame(root, bg = 'white')
Temperature_Frame.pack(side = TOP)

#Sliders frame
Sliders_Frame = Frame(Second_Frame, bg = 'white')
Sliders_Frame.pack(fill = None, expand = False, side = LEFT, anchor = NW, padx = 0, pady = 20)

#Buttons Frame
Buttons_Frame = Frame(Second_Frame, bg = 'white')
Buttons_Frame.pack(fill = None, expand = False, side = LEFT, anchor = NW, padx = 50, pady = 20)

#Sliders

UV_var = 0
DB_var = 0
BL_var = 0
GR_var = 0
RE_var = 0
IR_var = 0



W_UV = Scale(Sliders_Frame, command = UV_CallBack, resolution = 0.1, bg = 'white', highlightbackground = 'white', troughcolor = 'Cornflower Blue', length = 300,width = 50, from_=100.0, to=0.0)
W_DB = Scale(Sliders_Frame, command = DB_CallBack, resolution = 0.1, bg = 'white', highlightbackground = 'white', troughcolor = 'Medium Blue',     length = 300,width = 50, from_=100.0, to=0.0)
W_BL = Scale(Sliders_Frame, command = BL_CallBack, resolution = 0.1, bg = 'white', highlightbackground = 'white', troughcolor = 'Blue',            length = 300,width = 50, from_=100.0, to=0.0)
W_GR = Scale(Sliders_Frame, command = GR_CallBack, resolution = 0.1, bg = 'white', highlightbackground = 'white', troughcolor = 'Green',           length = 300,width = 50, from_=100.0, to=0.0)
W_RE = Scale(Sliders_Frame, command = RE_CallBack, resolution = 0.1, bg = 'white', highlightbackground = 'white', troughcolor = 'Red',             length = 300,width = 50, from_=100.0, to=0.0)
W_IR = Scale(Sliders_Frame, command = IR_CallBack, resolution = 0.1, bg = 'white', highlightbackground = 'white', troughcolor = 'Firebrick',       length = 300,width = 50, from_=100.0, to=0.0)

W_UV.pack(side = LEFT)
W_DB.pack(side = LEFT)
W_BL.pack(side = LEFT)
W_GR.pack(side = LEFT)
W_RE.pack(side = LEFT)
W_IR.pack(side = LEFT)

#Buttons
EN_Button = Button(Buttons_Frame, command = EN_CallBack, width = 20, height = 3, padx = 3, pady = 14, text = "LED En/Dis")
DI_Button = Button(Buttons_Frame, command = Al_CallBack, width = 20, height = 3, padx = 3, pady = 14, text = "All on/off")
FA_Button = Button(Buttons_Frame, command = FA_CallBack, width = 20, height = 3, padx = 3, pady = 14, text = "Fan on/off")
ST_Button = Button(Buttons_Frame, command = ST_CallBack, width = 20, height = 2, padx = 2, pady = 14, text = "Start", font = ("Helvetica", 14))

EN_Button.pack()
DI_Button.pack()
FA_Button.pack()
ST_Button.pack()

#Temperature sensors

Temp1 = StringVar()
Temp2 = StringVar()
Temp3 = StringVar()
Temp4 = StringVar()
Temp5 = StringVar()

Temp1.set('T1: 20C')
Temp2.set('T2: 20C')
Temp3.set('T3: 20C')
Temp4.set('T4: 20C')
Temp5.set('T5: 20C')

Label_T1 = Label(Temperature_Frame, bg = 'white', padx = 20, font = ("Helvetica", 14), textvariable = Temp1) 
Label_T2 = Label(Temperature_Frame, bg = 'white', padx = 20, font = ("Helvetica", 14), textvariable = Temp2) 
Label_T3 = Label(Temperature_Frame, bg = 'white', padx = 20, font = ("Helvetica", 14), textvariable = Temp3) 
Label_T4 = Label(Temperature_Frame, bg = 'white', padx = 20, font = ("Helvetica", 14), textvariable = Temp4) 
Label_T5 = Label(Temperature_Frame, bg = 'white', padx = 20, font = ("Helvetica", 14), textvariable = Temp5) 

Label_T1.pack(side = LEFT)
Label_T2.pack(side = LEFT)
Label_T3.pack(side = LEFT)
Label_T4.pack(side = LEFT)
Label_T5.pack(side = LEFT)


def main():
  global s
  global StaStatus
  s.connect((TCP_IP, TCP_PORT))
  n = 0
  k = 0
  while 1:
    if n == 10000:
      n = 0
      try:
        s.send('TEM 0')
        Temp1.set('T1: %sC'%s.recv(BUFFER_SIZE)[0:2])
        s.send('TEM 1')
        Temp2.set('T2: %sC'%s.recv(BUFFER_SIZE)[0:2])
        s.send('TEM 2')
        Temp3.set('T3: %sC'%s.recv(BUFFER_SIZE)[0:2])
        s.send('TEM 3')
        Temp4.set('T4: %sC'%s.recv(BUFFER_SIZE)[0:2])
        s.send('TEM 7')
        Temp5.set('T5: %sC'%s.recv(BUFFER_SIZE)[0:2])
      except:
        Temp1.set('T1: -1C')
        Temp2.set('T2: -1C')
        Temp3.set('T3: -1C')
        Temp4.set('T4: -1C')
        Temp5.set('T5: -1C')
      print StaStatus
    n = n + 1
    root.update()
    if StaStatus == 1:
      for i in range (0, LineNumber):
        Elements = data[i].split(' ')
        Elements_Y = Elements[0].split('-')
        Elements_H = Elements[1].split(':')
        Time = datetime.datetime(int(Elements_Y[0]), int(Elements_Y[1]), int(Elements_Y[2]), int(Elements_H[0]), int(Elements_H[1]), int(Elements_H[2]))
        if Time > datetime.datetime.now():
          if float(Elements[2]) >= 0:
          	if (i-1) >= 0:

			UV_value = float(0)
          		DB_value = float(0)
          		BL_value = float(0)
          		GR_value = float(0)
          		RE_value = float(0)
          		IR_value = float(0)
		
         		W_UV.set(UV_value)
          		W_DB.set(DB_value)
          		W_BL.set(BL_value)
          		W_GR.set(GR_value)
          		W_RE.set(RE_value)
          		W_IR.set(IR_value)

			GPIO.setmode(GPIO.BCM)
			GPIO.setwarnings(False)

			GPIO.setup(9, GPIO.OUT)
			GPIO.setup(26, GPIO.OUT)
			GPIO.setup(12, GPIO.OUT)
			GPIO.setup(13, GPIO.OUT)
			GPIO.setup(14, GPIO.OUT)
			GPIO.setup(15, GPIO.OUT)

			GPIO.output(9, 1) #UV
			GPIO.output(26, 1) #Deep blue
			GPIO.output(12, 1) #Blue
			GPIO.output(13, 1) #Green
			GPIO.output(14, 1) #Red
			GPIO.output(15, 1) #IR

			#time.sleep(0.5)
			 
          		Elements = data[i-1].split(' ')

          		UV_value = float(Elements[2])
          		DB_value = float(Elements[3])
          		BL_value = float(Elements[4])
          		GR_value = float(Elements[5])
          		RE_value = float(Elements[6])
          		IR_value = float(Elements[7])
		

			if UV_value > 0:
         			W_UV.set(UV_value)
			else:
				GPIO.output(9, 0) #UV

			if UV_value > 0:
          			W_DB.set(DB_value)
			else:
				GPIO.output(26, 0) #Deep blue

			if BL_value > 0:
          			W_BL.set(BL_value)
			else:
				GPIO.output(12, 0) #Blue

			if GR_value > 0:
          			W_GR.set(GR_value)
			else:
				GPIO.output(13, 0) #Green

			if RE_value > 0:
          			W_RE.set(RE_value)
			else:
				GPIO.output(14, 0) #Red

			if IR_value > 0:
          			W_IR.set(IR_value)
			else:
				GPIO.output(15, 0) #IR

          		print UV_value, DB_value, BL_value, GR_value, RE_value, IR_value
        		break
	  else:

		UV_value = float(0)
          	DB_value = float(0)
          	BL_value = float(0)
          	GR_value = float(0)
          	RE_value = float(0)
          	IR_value = float(0)
		
         	W_UV.set(UV_value)
          	W_DB.set(DB_value)
          	W_BL.set(BL_value)
          	W_GR.set(GR_value)
          	W_RE.set(RE_value)
          	W_IR.set(IR_value)

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		GPIO.setup(9, GPIO.OUT)
		GPIO.setup(26, GPIO.OUT)
		GPIO.setup(12, GPIO.OUT)
		GPIO.setup(13, GPIO.OUT)
		GPIO.setup(14, GPIO.OUT)
		GPIO.setup(15, GPIO.OUT)

		GPIO.output(9, 0) #UV
		GPIO.output(26, 0) #Deep blue
		GPIO.output(12, 0) #Blue
		GPIO.output(13, 0) #Green
		GPIO.output(14, 0) #Red
		GPIO.output(15, 0) #IR

	
     # k = 0
     # date = str(datetime.datetime.now()).split(' ')
     # date_a = date[0].split('-')
     # date_b = date[1].split(':')
     # print int(date_a[0] + date_a[1] + date_a[2] +date_b[0] + date_b[1] + str(int(float(date_b[2]))))
      #print datetime.datetime(2017, 5, 1, 15, 34, 4)
     # print datetime.datetime.now()
      #print (datetime.datetime(2017, 5, 1, 15, 34, 4) > datetime.datetime.now())
    #k = k + 1

    #time.sleep(0.2)

if __name__ == '__main__':
  main()