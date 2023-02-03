from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
import tkinter
import cv2
import PIL.Image,PIL.ImageTk
from threading import Thread
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits import mplot3d
import matplotlib
from matplotlib import style
from data import data
from tkinter import messagebox
import pandas
from functools import partial
import os
import matplotlib.animation as animation
from tkinter import filedialog
import pandas as pd

FILE_LOCATION = "./data"
INFO_FONT = ("Arial", 12, "bold")
SMALL_FONT = ("Arial", 12, "normal")

class App(object):
  def __init__(self):
    #set style of graphs
    style.use('dark_background')
    self.window = Tk()

    self.window.title('GUI LVTN')
    self.window.iconbitmap("ctu.ico")
    self.window.geometry('640x480')
    self.window.resizable(False, False)

    self.cap = cv2.VideoCapture(0)

    self.pie_group_name = StringVar()
    self.pie_value_name = StringVar()
    self.cap_success = False

    #initialize data
    self.xs = []
    self.ys = []
    self.zs = [] 

    #create tab
    self.Tab = Notebook(self.window)
    self.maintab = tk.Frame(self.Tab,bg="ivory")
    self.Tab.add(self.maintab, text ='Main')
    self.Tab.pack(expand = 1, fill ="both")

    self.fig_3 = None

    self.V_frame = tk.Frame(self.maintab) # the tich frame
    self.so_phan_chia_frame = tk.Frame(self.maintab) # so phan duoc chia
    self.the_tich_moi_phan_frame = tk.Frame(self.maintab) # the tich cua moi phan
    self.fig_frame = tk.Frame(self.maintab  ,padx=3.3, pady=3) # figure frame 
    self.img_frame = tk.Frame(self.maintab ,width = 320 ,height=202) # image frame
    
    self.menubar =  Menu(self.window, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')  
    self.menuBar()
    # header 
    self.frame_name = tk.Frame(self.maintab,bg="ivory")
    self.label = tk.Label(self.maintab, text='name',bg="ivory")
    
    self.count = 0

    self.photo = None 

    self.creat_canvas_image()

    #Figure 
    self.fig = Figure(figsize=(3.1,2),dpi = 100)
    self.fig.tight_layout()

    self.canvas_plot()
    self.plot_settings()
    
    
      # Image
    self.update_frame_image()
    
    #Layout
    self.layout()

    # live graph
    self.ani = animation.FuncAnimation(self.fig,self.animate , interval = 1000)

    self.window.config(menu = self.menubar)
    self.window.mainloop()

  
  def enable_camera(self):
    # On camera
    self.cap_success = True 

  def disable_camera(self):
    # Off camera
    self.cap_success = False


  def enable_plot(self):
    self.color_point_plot = 'white'

  def disable_plot(self):
    self.color_point_plot = 'black'

  def canvas_plot(self):
    self.fig_canvas = FigureCanvasTkAgg(self.fig,self.fig_frame )
    self.fig_canvas.draw()

  def plot_settings(self):
    self.color_point_plot = 'white'

    self.fig_canvas.get_tk_widget().pack(fill=BOTH)
    self.ax = self.fig.add_subplot(111, projection="3d")
    
  def creat_canvas_image(self):
      self.canvas = Canvas(self.img_frame,width = 320 ,height=202,bg='white')

  def update_frame_image(self):
    if self.cap.isOpened():
      ret , frame = self.cap.read()

      frame = cv2.resize(frame,dsize=None,fx = 0.5 , fy = 0.5)

      frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

      # Chuyển đổi ma trận điểm ảnh sang ảnh 
      self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
      if self.cap_success:
        self.canvas.create_image(0,0,image = self.photo , anchor =NW)

      self.count +=  1 

      # Thread cho phần sau
      if self.count % 10 == 0 :
        thread1 = Thread(target = self.printName )
        thread1.start()

      self.window.after(15,self.update_frame_image)

  def printName(self):
    pass

  def layout(self):
    
      self.label.pack(fill=BOTH)

      # Fill img_frame
      self.canvas.pack(fill=BOTH)

      #self.fig_frame.grid(column=1,row=1)
      self.fig_frame.place(x = 320, y = 50 , width = 320 ,height=202)

      #self.img_frame.grid(column=0,row=1)
      self.img_frame.place(x = 0 , y = 50 , width = 320 ,height=202)

      self.frame_name.place(x = 0 , y = 0 , width= 640 , height=40)

  def menuBar(self):
    #File
    file = Menu(self.menubar, tearoff=0, foreground='black')  
    file.add_command(label="New")  

    self.open = Menu(self.menubar, tearoff=0)
    self.open.add_command(label="Data" , command=self.openNewTab_history_data) 

    self.open_file_data = Menu(self.open, tearoff= 0)
    self.open_file_data.add_command(label="Available SpreadSheets" , command=self.file_open)
    self.open.add_cascade(label='...',menu=self.open_file_data)

    self.open.entryconfig("...", state="disabled")

    file.add_cascade(label='Open',menu=self.open)
    file.add_command(label="Save")
    file.add_command(label="Save as")  
    close_tab = Menu(self.menubar,tearoff=0)  
    
    file.add_separator()  
    file.add_command(label="Exit", command=self.window.quit)  
    self.menubar.add_cascade(label="File", menu=file)  

    #edit 
    edit = Menu(self.menubar, tearoff=0)  
    edit.add_command(label="Undo")  
    edit.add_separator()     
    edit.add_command(label="Cut")  
    edit.add_command(label="Copy")  
    edit.add_command(label="Paste")  

    self.menubar.add_cascade(label="Edit", menu=edit)  

    #view 
    view = Menu(self.menubar,tearoff=0)

    camera = Menu(self.menubar, tearoff=0)
    camera.add_command(label='ENABLE',command=self.enable_camera)
    camera.add_command(label='DISSABLE',command=self.disable_camera)
    view.add_cascade(label='Camera',menu=camera)
    
    plot = Menu(self.menubar,tearoff=0)
    plot.add_command(label ='ENABLE',command=self.enable_plot)
    plot.add_command(label ='DISSABLE',command=self.disable_plot)
    view.add_cascade(label='Plot',menu=plot)

    self.menubar.add_cascade(label="View", menu=view)  


    #help
    help = Menu(self.menubar, tearoff=0)  
    help.add_command(label="About", command=self.about)  
    self.menubar.add_cascade(label="Help", menu=help)

  def about(self):
    messagebox.showinfo('GUI LVTN', 'Designed by Nguyen Ngoc Thanh')

  def ToolBar(self):
    self.toolbar = NavigationToolbar2Tk(self.fig_canvas, self.fig_frame )
    self.toolbar.update()

  def disable_toolbar(self):
    self.toolbar.destroy()

  def openNewTab_history_data(self):
    self.data_tab = tk.Frame(self.Tab,bg="ivory" )

    self.left_frame = tk.Frame(self.data_tab,bg="ivory")
    self.left_frame.place(x=2, y=0, width=320, height=645)
     
    self.frame_to_plot_data_pie = tk.Frame(self.data_tab,bg="ivory")
    self.frame_to_plot_data_pie.place(x = 325 , y = 150 , width = 310 , height= 325)

    self.canvas_3 = Canvas(self.frame_to_plot_data_pie, width=310, height=325, bg="ivory", relief=RIDGE)
    self.canvas_3.pack(fill=BOTH)

    self.pie_info = tk.Frame(self.data_tab,bg="ivory")
    self.pie_info.place(x=325, y=40, width=365, height=70)

    self.pie_group_box = ttk.Combobox(self.pie_info, font=SMALL_FONT, justify="center", state="readonly",
                                          textvariable=self.pie_group_name)
    self.pie_group_box.grid(row=1, column=1)

    self.pie_value_box = ttk.Combobox(self.pie_info, font=SMALL_FONT, justify="center", state="readonly",
                                          textvariable=self.pie_value_name)
    self.pie_value_box.grid(row=0, column=1)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", backgroung="silver", foreground="black", rowheight=25, fieldbackground="silver")
    style.map("Treeview", background=[("selected", "medium sea green")])
    style.configure("Treeview.Heading", background="light steel blue", font=("Arial", 10, "bold"))  

    self.my_table = ttk.Treeview(self.left_frame)

    scroll_x_label = ttk.Scrollbar(self.left_frame, orient=HORIZONTAL, command=self.my_table.xview)
    scroll_y_label = ttk.Scrollbar(self.left_frame, orient=VERTICAL, command=self.my_table.yview)
    scroll_x_label.pack(side=BOTTOM, fill=X)
    scroll_y_label.pack(side=RIGHT, fill=Y)

    #disable data menu
    self.open.entryconfig("Data", state="disabled")
    #enable ...
    self.open.entryconfig("...", state="normal")

    self.Tab.add(self.data_tab, text ='Data')

    self.pie_draw_button = tk.Button(self.data_tab, text="draw", command=self.draw_pie_chart)
    self.pie_draw_button.place(x = 325 , y = 0 , width= 50 , height=40)

    self.pie_clear_button = tk.Button(self.data_tab, text="clean",  command=self.clear_pie)
    self.pie_clear_button.place(x = 375, y = 0 , width= 50 , height=40)

    button = tk.Button(self.data_tab, text ='Exit',command=self.closeDataTab)
    button.place(x = 425, y = 0 , width= 50 , height=40)

  def closeDataTab(self):
    self.open.entryconfig("Data", state="normal")
    self.open.entryconfig("...", state="disabled")
    self.data_tab.destroy()

  def folder_data(self):
    folder = os.path.realpath('./data')
    self.fileList = [fname for fname in os.listdir(folder)]

  def animate(self,i):
    pullData = open('./data/samplesData.txt','r').read()
    dataList = pullData.split('\n')
    for line in dataList:
      if len(line) > 1 :
        x,y,z = line.split(',')
        self.xs.append(int(x))
        self.ys.append(int(y))
        self.zs.append(int(z))
    self.ax.clear()
    self.ax.grid(False)

    #self.ax.set(xlim=(min(self.xs)*3,max(self.xs)*3), ylim=(min(self.ys)*3,max(self.ys)*3) , zlim = (min(self.zs)*3,max(self.zs)*3))

    self.ax.set_xticks([])
    self.ax.set_yticks([])
    self.ax.set_zticks([])
    self.ax.axis('off')
    self.ax.scatter(self.xs, self.ys, self.zs, lw=0.01,color=self.color_point_plot).set_sizes([2])

  def file_open(self):
        file_name = filedialog.askopenfilename(
            initialdir=FILE_LOCATION,
            title="Open A File",
            filetypes=(("csv files", "*.csv"), ("All Files", "*.*"))
        )
        if file_name:
            try:
                file_name = f"{file_name}"
                self.df = pd.read_csv(file_name)
            except ValueError:
                self.error_info.config(text="file can not be opened!")
            except FileNotFoundError:
                self.error_info.config(text="file can not be found!")

        # clean existing data:
        self.clear_table_data()
        # from csv into dataframe:
        self.my_table["column"] = list(self.df.columns)
        self.my_table["show"] = "headings"
        for column in self.my_table["column"]:
            self.my_table.heading(column, text=column)
        # resize columns:
        for column_name in self.my_table["column"]:
            self.my_table.column(column_name, width=60)
        # fill rows with data:
        df_rows_old = self.df.to_numpy()
        df_rows_refreshed = [list(item) for item in df_rows_old]
        for row in df_rows_refreshed:
            self.my_table.insert("", "end", values=row)
        self.my_table.place(x=5, y=5, width=310, height=630)
        try:
            self.fill_pie_box()
        except TclError:
            pass
        '''
        try:
            self.fill_scatter_box()
        except TclError:
            pass

        try:
            self.fill_bar_box()
        except TclError:
            pass

        try:
            self.fill_pie_box()
        except TclError:
            pass

        try:
            self.fill_line_box()
        except TclError:
            pass
        '''
        
  def fill_pie_box(self):
        columns = [item for item in self.df]
        x_labels = []
        y_labels = []
        for column in columns:
            if self.df[column].dtype == 'object':
                x_labels.append(column)
            elif self.df[column].dtype == 'int64' or self.df[column].dtype == 'float64':
                y_labels.append(column)
        print(x_labels, y_labels)
        self.pie_group_box["values"] = tuple(x_labels)
        self.pie_group_box.current(0)
        self.pie_value_box["values"] = tuple(y_labels)
        self.pie_value_box.current(0)

  def draw_pie_chart(self):
        # prepare values:
        display = self.df.groupby([f"{self.pie_group_name.get()}"]).sum(numeric_only=True)
        display = display[f"{self.pie_value_name.get()}"].to_numpy()
        my_labels = list(self.df[f"{self.pie_group_name.get()}"].unique())
        # visualize:
        self.fig_3 = Figure(figsize=(4, 2), dpi=100)
        axes = self.fig_3.add_subplot(111)
        axes.pie(display, labels=my_labels, shadow=True)
        self.output_3 = FigureCanvasTkAgg(self.fig_3, master=self.canvas_3)
        self.output_3.draw()
        self.output_3.get_tk_widget().pack(fill = BOTH)
  
  # xóa biểu đồ khi muốn xem 1 giá trị mớis
  def clear_pie(self):
    if self.output_3:
        for child in self.canvas_3.winfo_children():
            child.destroy()
    self.output_3 = None

  # Xoa bảng dử liệu cũ để hiển thị dữ liệu mới
  def clear_table_data(self):
      self.my_table.delete(*self.my_table.get_children())

if __name__ == '__main__':
  App()