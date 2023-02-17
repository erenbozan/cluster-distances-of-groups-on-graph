import matplotlib
import math
import pandas as pd
import numpy as np
import random
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from matplotlib import pyplot as plt
import sklearn.cluster as KMeans
from sklearn.cluster import KMeans

from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("Final-data.txt")
satirSayisi = len(open("Final-data.txt").readlines(  ))

root = Tk()
root.geometry("200x500")

label = ttk.Label(text="K:")
label.pack(pady=5)
cluster_box=Entry(root)
cluster_box.pack(pady=5)

labe2 = ttk.Label(text="ilk kategori:")
labe2.pack( padx=10, pady=11)
secilenKategori1 = tk.StringVar()
secilen2 = ttk.Combobox(root, textvariable=secilenKategori1)
secilen2["values"]=["Sports","Religious","Nature","Theatre","Shopping","Picnic"]
secilen2["state"]="readonly"
secilen2.pack(fill=tk.X,padx=20,pady=10)

labe3 = ttk.Label(text="ikinci kategori:")
labe3.pack( padx=10, pady=12)
secilenKategori2 = tk.StringVar()
secilen3 = ttk.Combobox(root, textvariable=secilenKategori2)
secilen3["values"]=["Sports","Religious","Nature","Theatre","Shopping","Picnic"]
secilen3["state"]="readonly"
secilen3.pack(fill=tk.X,padx=20,pady=10)


def graph():
    plt.clf()
    clusterAdet=int(cluster_box.get())
    km= KMeans(n_clusters=clusterAdet)
    y_predicted = km.fit_predict(df[[secilenKategori1.get(),secilenKategori2.get()]])
    df["cluster"]=y_predicted

    for n in range (0,clusterAdet):
        df1=(df[df.cluster==n])
        randomRenk = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
        plt.scatter(df1[secilenKategori1.get()],df1[secilenKategori2.get()],color=randomRenk)
    plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color="purple",marker="*")

    f = open("myfile.txt", "w")
    for satir in range (0,satirSayisi-1):
            f.write("kayit-"+str(satir+1)+":      kume:"+str(df.cluster[satir]+1)+"\n" )  
    f.write("---------------------------------------\n")

    kumeler=[]
    kacAdet=0
    for i in range(0,clusterAdet):
        for satir in range (0,satirSayisi-1):
            if(df.cluster[satir]==i):
                kacAdet=kacAdet+1 
        kumeler.append(kacAdet)
        kacAdet=0
    for i in range (0,clusterAdet):
        f.write("kume-"+str(i+1)+":   "+ str(kumeler[i])+" kayit\n") 
    f.write("---------------------------------------\n")
   
    wcss=0
    maxbulma=0
    maxbulmaSon=0
    for i in range(0,clusterAdet): 
        for j in range(0,satirSayisi-1):
            if(df.cluster[j]==i):
                clusterBoylamFark=abs(df[secilenKategori1.get()][j]-km.cluster_centers_[:,0][i])
                clusterEnlemFark=abs(df[secilenKategori2.get()][j]-km.cluster_centers_[:,1][i])
                merkezeUzaklik=math.sqrt(pow(clusterBoylamFark,2)+pow(clusterEnlemFark,2))
                wcss=wcss+merkezeUzaklik
                maxbulma=maxbulma+merkezeUzaklik

        if(maxbulmaSon-maxbulma<0):
            maxbulmaSon=maxbulma                                                                                #max intra cluster distance
        maxbulma=0         
    f.write("WCSS: "+str(wcss)+"\n")

    bcss=0
    toplamMeansOfClustersX=0
    toplamMeansOfClustersY=0
    for i in range(0,clusterAdet):                                                                              #great mean findd 
        toplamMeansOfClustersX+=km.cluster_centers_[:,0][i]
        toplamMeansOfClustersY+=km.cluster_centers_[:,1][i]
    toplamMeansOfClustersX=toplamMeansOfClustersX/clusterAdet
    toplamMeansOfClustersY=toplamMeansOfClustersY/clusterAdet
    plt.scatter(toplamMeansOfClustersX ,toplamMeansOfClustersY,color="green",marker="*")

    for i in range(0,clusterAdet):
        clusterBoylamFark = abs(km.cluster_centers_[:,0][i]-toplamMeansOfClustersX)
        clusterEnlemFark  = abs(km.cluster_centers_[:,1][i]-toplamMeansOfClustersY)
        greatMeanDistance = math.sqrt(pow(clusterBoylamFark,2)+pow(clusterEnlemFark,2))
        bcss=bcss+greatMeanDistance
    f.write("BCSS: "+str(bcss)+"\n")

    enUzakClusterlar=0
    for i in range(0,clusterAdet):        
        for j in range(0,clusterAdet):                                                                           #min inter cluster distances
            clusterBoylamFark=abs(km.cluster_centers_[:,0][i]-km.cluster_centers_[:,0][j]) 
            clusterEnlemFark =abs(km.cluster_centers_[:,1][i]-km.cluster_centers_[:,1][j])
            clusterlarArasiMesafe = math.sqrt(pow(clusterBoylamFark,2)+pow(clusterEnlemFark,2))
            if(enUzakClusterlar<clusterlarArasiMesafe):
                enUzakClusterlar=clusterlarArasiMesafe
    

    dunnIndex=maxbulmaSon/enUzakClusterlar
    f.write("DUNN INDEX: "+str(dunnIndex))
    f.close()
    plt.show()

 

buton_1=Button(root,text="grafiği getir",command=graph)
buton_1.pack(fill=tk.X, padx=50, pady=100)
root.mainloop()


 



   


