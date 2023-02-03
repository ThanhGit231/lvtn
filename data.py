import pandas as pd
import numpy as np
import os

class data():
    def __init__(self,file_name):
        # đọc file xlsx
        read_file = pd.read_excel(file_name)
        read_file.to_csv(r'data2.csv',index=None , header=True)
        self.data = pd.read_csv('data2.csv')

    # in  data
    def show(self):
        print(self.data)

    def du_lieu_de_ve(self):
        lst_x = self.data['x'].to_numpy()
        lst_y = self.data['y'].to_numpy()
        lst_z = self.data['z'].to_numpy()
        self.buoc = lst_x
        return lst_x,lst_y,lst_z

    def du_lieu_the_tich_tong(self):
        V  = self.data['V'].to_numpy()
        return V[-1]

    def du_lieu_de_cat(self):
        q = self.data['t'].to_numpy()
        buoc_de_cat = []
        for i in range(len(q)) :
            if q[i] == 1 :
                buoc_de_cat.append(self.buoc[i])

        return buoc_de_cat


