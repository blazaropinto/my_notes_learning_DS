import tkinter as tk

#create the window where the widgets will be
window = tk.Tk()

window.title('Convert kf to g, pounds and ounces')
window.geometry('600x120')
window.configure(background='purple')

#define fucntions to be performed by buttoms:convert and clean
def convert():
    try:
        t1.insert(tk.END, float(kgvar.get())*1000)
        t2.insert(tk.END, float(kgvar.get())*2.20)
        t3.insert(tk.END, float(kgvar.get())*35.27)
    except ValueError:
        t2.insert(tk.END, 'Please insert a float')

def clean():
    t1.delete(1.0,tk.END)
    t2.delete(1.0,tk.END)
    t3.delete(1.0,tk.END)
    e.delete(0, tk.END)

#add buttoms
b = tk.Button(window, text='Convert', command=convert, 
                background='green', foreground='yellow')
b.grid(row=0, rowspan=2, column=3)

b2 = tk.Button(window, text='Clean', command=clean, 
                background='green', foreground='white')
b2.grid(row=15, rowspan=3, column=2)

#add text entry widgets
kgvar = tk.StringVar()
e = tk.Entry(window, textvariable= kgvar)
e.grid(row=0, column=2)

#add text boxes

t1 = tk.Text(window, height=1, width=20)
t1.grid(row=3, rowspan=2, column=1)

t2 = tk.Text(window, height=1, width=30)
t2.grid(row=3, rowspan=2, column=2)

t3 = tk.Text(window, height=1, width=20)
t3.grid(row=3, column=3)

#add labels
l0 = tk.Label(window, text='Insert wt in kg', background='purple', foreground='white')
l0.grid(row=0, column=1)

l1 = tk.Label(window, text='grams')
l1.grid(row=7, column=1)

l2 = tk.Label(window, text='pounds')
l2.grid(row=7, column=2)

l3 = tk.Label(window, text='ounces')
l3.grid(row=7, column=3)

#this line has to at be the end
window.mainloop()
