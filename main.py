from tkinter import *
import tkinter as tk
import numpy as np
import pandas as pd
import math
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

enter_window = None
data = {'freq' : [], 'delta' : []}
poly = None
model = None
init_entry = None
last_entry = None
num_entry = None
y = None
new_data = None
table = None
delta_l = None
delta_niu = None

def TrainModel():
    global data
    global model
    global poly
    global enter_window
    for i in range(len(data['freq'])):
        data['freq'][i] = float(data['freq'][i].get())
        data['delta'][i] = float(data['delta'][i].get())
    poly = PolynomialFeatures(3)
    X_poly = poly.fit_transform(np.array(data['freq']).reshape(-1, 1))
    model = LinearRegression()
    model.fit(X_poly, data['delta'])
    enter_window.destroy()
    txt_label.config(text='Model Trained! You can use function below!')
    print(model)

def EnterData():
    global nb
    global enter_window
    enter_window = tk.Toplevel(root)
    if nb.get() == '':
        No_data = Label(enter_window, text='No data')
        No_data.grid(row=0, column=0)
    else:
        general_label = Label(enter_window, text="Enter the date from the measurements that ou have done:")
        general_label.grid(row=0, column=0, columnspan=2)
        global data
        for i in range(int(nb.get())):
            freq_label = Label(enter_window, text='Frequency nr {}'.format(i+1))
            freq_label.grid(row=i+1, column=0, sticky=W)
            freq_entry = Entry(enter_window)
            freq_entry.grid(row=i+1, column=1)
            delta_label = Label(enter_window, text='delta l nr {}'.format(i+1))
            delta_label.grid(row=i+1, column=2, sticky=W)
            delta_entry = Entry(enter_window)
            delta_entry.grid(row=i+1, column=3)
            data['freq'].append(freq_entry)
            data['delta'].append(delta_entry)
        fin_btn = Button(enter_window, text="Enter", command=TrainModel)
        fin_btn.grid(row=int(nb.get())+1, column=0, sticky=W)

def ApplyModel():
    global init_entry
    global last_entry
    global num_entry
    global poly
    global model
    global y
    global new_data
    new_data = {'freq':[], 'delta':[]}
    X = np.linspace(float(init_entry.get()), float(last_entry.get()), float(num_entry.get()), endpoint=True)
    X_poly = poly.transform(X.reshape(-1, 1))
    y = model.predict(X_poly)
    for i in range(len(y)):
        new_data['freq'].append(X[i])
        new_data['delta'].append(y[i])

sound_speed = lambda t : 331.5 + 0.607 * t

def ShowTable():
    global temp
    global new_data
    global init_entry
    global last_entry
    global num_entry
    global table
    HZ = np.linspace(float(init_entry.get()), float(last_entry.get()), float(num_entry.get()), endpoint=True)
    s_speed = sound_speed(float(temp.get()))
    l = []
    for hz in HZ:
        l.append(s_speed / hz)
    interval_de_incredere = []
    for i in range(len(l)):
        interval_de_incredere.append(l[i] - y[i])
        interval_de_incredere.append(l[i])
        interval_de_incredere.append(l[i] + y[i])
    new_Hz = [x for x in HZ for i in range(3)]
    table = pd.DataFrame({'freq': new_Hz, 'l': interval_de_incredere})
    table['v'] = table['freq'] * table['l']
    X = table.values
    table_wnd = tk.Toplevel(root)
    freq = Label(table_wnd, text="Frequency")
    Lambda = Label(table_wnd, text='l')
    Speed = Label(table_wnd, text='Sound Speed')
    freq.grid(row=0, column=0)
    Lambda.grid(row=0, column=1)
    Speed.grid(row=0, column=2)
    for i in range(len(X)):
        f = Label(table_wnd, text=str(X[i][0]))
        l = Label(table_wnd, text=str(X[i][1]))
        s = Label(table_wnd, text=str(X[i][2]))
        f.grid(row=i+1, column=0)
        l.grid(row=i+1, column=1)
        s.grid(row=i+1, column=2)

def ShowErrors():
    global delta_niu
    global delta_l
    global temp
    global table
    dl = float(delta_l.get())
    dniu = float(delta_niu.get())
    delta_v = 2 * math.sqrt((table['l'].mean() ** 2) * (dniu ** 2) + (table['freq'].mean() ** 2) * (dl ** 2))
    epsilon = delta_v / sound_speed(float(temp.get()))
    error_wnd = tk.Toplevel(root)
    dV_label = Label(error_wnd, text='The absolute error of speed of sound is {}'.format(delta_v))
    ep_label = Label(error_wnd, text='The relative error of speed of sound is {}'.format(epsilon))
    dV_label.grid(row=0, column=0)
    ep_label.grid(row=1, column=0)


root = Tk()
root.title("PBL Project")
topFrame = Frame(root)
topFrame.grid(row=0, column=0)
label1 = Label(topFrame, text='Enter the number of messurments:')
nb = Entry(topFrame)
enter_btn = Button(topFrame, text="Enter:", comman=EnterData)
label1.grid(row=0, column=0, sticky=W)
nb.grid(row=0, column=1)
enter_btn.grid(row=0, column=2)

sound_Frame = Frame(root)
sound_Frame.grid(row=1, column=0)
sound_label = Label(sound_Frame, text='Enter the temperature at wich the experience in taking place in Celsius:')
sound_label.grid(row=0, column=0)
temp = Entry(sound_Frame)
temp.grid(row=0, column=1)

second_Frame = Frame(root)
second_Frame.grid(row=2, column=0)
txt_label = Label(second_Frame, text='Model not Trained!')
txt_label.grid(row=0, column=0)

third_Frame = Frame(root)
third_Frame.grid(row=3, column=0)
HZ_label = Label(third_Frame, text='Enter the values bellow to continue')
HZ_label.grid(row=0, column=0, columnspan=2)
init_freq = Label(third_Frame, text="The first value of frequency:")
last_freq = Label(third_Frame, text = 'The last values of frequency:')
num_point = Label(third_Frame, text = 'The number of points on the interval:')
init_entry = Entry(third_Frame)
last_entry = Entry(third_Frame)
num_entry = Entry(third_Frame)
init_freq.grid(row=1, column=0, sticky=W)
last_freq.grid(row=2, column=0, sticky=W)
num_point.grid(row=3, column=0, sticky=W)
init_entry.grid(row=1, column=1)
last_entry.grid(row=2, column=1)
num_entry.grid(row=3, column=1)
apply = Button(third_Frame, text='Apply model', command=ApplyModel)
apply.grid(row=4, column=0)
show_table = Button(third_Frame, text='Show Table', command=ShowTable)
show_table.grid(row=4, column=1)

error_Frame = Frame(root)
error_Frame.grid(row=4, column=0)
delta_l_label =Label(error_Frame, text="Enter the delta L:")
delta_l = Entry(error_Frame)
delta_niu_label= Label(error_Frame, text='Enter the delta frequency:')
delta_niu = Entry(error_Frame)
delta_l_label.grid(row=0, column=0, sticky=W)
delta_l.grid(row=0, column=1)
delta_niu_label.grid(row=1, column=0, sticky=W)
delta_niu.grid(row=1, column=1)
error_btn = Button(error_Frame, text='Calculate Errors', command=ShowErrors)
error_btn.grid(row=2, column=0)

root.mainloop()