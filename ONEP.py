import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import time
import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
import tkinter.ttk as ttk
import sqlite3
from scipy.optimize import linprog

class Fenetre():
    def __init__(self,root):
        #Menu
        self.fenetre=root #l'identificateur de la fenetre principal est stocké dans l'attribut fenetre
        #création du menu
        self.menubar=Menu(self.fenetre)
        self.fenetre.config(menu=self.menubar)
        
        self.subMenu=Menu(self.menubar,tearoff=0)
        self.subMenu1=Menu(self.menubar,tearoff=0)
        self.subsubMenu=Menu(self.subMenu,tearoff=0)
        self.subsubMenu1=Menu(self.subMenu,tearoff=0)
        self.subsubMenu2=Menu(self.subMenu,tearoff=0)
        self.subsubMenu3=Menu(self.subMenu,tearoff=0)
        
        self.menubar.add_cascade(label='Données',menu=self.subMenu)
        self.menubar.add_cascade(label='Calcul',menu=self.subMenu1)
        
        self.subMenu.add_command(label='Saisir les données',command= self.saisie)
        
        
        self.subMenu.add_cascade(label='Modifier les données',menu=self.subsubMenu)
        self.subsubMenu.add_command(label='Régions',command= self.Modif_region)
        self.subsubMenu.add_command(label='Entrepôts',command= self.Modif_entrepot)
        
        self.subMenu.add_cascade(label='Supprimer les données',menu=self.subsubMenu1)
        self.subsubMenu1.add_command(label='Régions',command= self.supprimeRegion)
        self.subsubMenu1.add_command(label='Entrepôts',command= self.supprimeEntrepot)
        
        self.subMenu.add_cascade(label='Afficher les données',menu=self.subsubMenu2)
        self.subsubMenu2.add_command(label='Régions',command= self.afficherRegion)
        self.subsubMenu2.add_command(label='Entrepôts',command= self.afficherEntrepot)
        
        self.subMenu1.add_command(label='Afficher les calculs',command= self.afficherCalcul)
        self.subMenu1.add_command(label='Optimisation des entrepôts',command= self.optimisation)
        
        self.subMenu.add_separator()
        self.subMenu.add_command(label='Exit',command=self.quitter)
    def optimisation(self):
        self.quitter()
        master=Tk()
        master.title('Optimisation des entrepôts ')
        h=master.winfo_screenheight()//100*100-10
        w=master.winfo_screenwidth()//100*100+50
        master.geometry(str(w)+'x'+str(h)+'+0+0')
        app=Optimisation_entrepot(master)
        master.mainloop()
    def afficherCalcul(self):
        self.quitter()
        master=Tk()
        master.title('Afficher les calculs  ')
        h=master.winfo_screenheight()//100*100-10
        w=master.winfo_screenwidth()//100*100+50
        master.geometry(str(w)+'x'+str(h)+'+0+0')
        app=Calculs(master)
        master.mainloop()
    def afficherEntrepot(self):
        self.quitter()
        master=Tk()
        master.title('Afficher les entrepôts')
        h=master.winfo_screenheight()//100*100-10
        w=master.winfo_screenwidth()//100*100+50
        master.geometry(str(w)+'x'+str(h)+'+0+0')
        app=AfficherEntrepot(master)
        master.mainloop()
    
    def afficherRegion(self):
        self.quitter()
        master=Tk()
        master.title('Afficher les régions')
        h=master.winfo_screenheight()//100*100-10
        w=master.winfo_screenwidth()//100*100+50
        master.geometry(str(w)+'x'+str(h)+'+0+0')
        app=AfficherRegion(master)
        master.mainloop()
        
    def supprimeEntrepot(self):
        self.quitter()
        master=Tk()
        master.title('Suppression des entrepôts et/ou des dessertes')
        h=master.winfo_screenheight()//100*100-10
        w=master.winfo_screenwidth()//100*100+50
        master.geometry(str(w)+'x'+str(h)+'+0+0')
        app=SupprimerEntrepot(master)
        master.mainloop()
        
    def supprimeRegion(self):
        self.quitter()
        master=Tk()
        master.title('Suppression des régions')
        h=master.winfo_screenheight()//100*100-10
        w=master.winfo_screenwidth()//100*100+50
        master.geometry(str(w)+'x'+str(h)+'+0+0')
        app=SupprimerRegion(master)
        master.mainloop()
        
        
    def Modif_entrepot(self):
        self.quitter()
        master=Tk()
        master.title('Modifications des données concernant les entrepôts enregistrés')
        h=master.winfo_screenheight()//100*100-10
        w=master.winfo_screenwidth()//100*100+50
        master.geometry(str(w)+'x'+str(h)+'+0+0')
        app=ModifierEntrepot(master)
        master.mainloop()
    def Modif_region(self):
        self.quitter()
        master=Tk()
        master.title('Modifications des données concernant les régions enregistrées')
        h=master.winfo_screenheight()//100*100-10
        w=master.winfo_screenwidth()//100*100+50
        master.geometry(str(w)+'x'+str(h)+'+0+0')
        app=ModifierRegion(master)
        master.mainloop()
    def quitter(self):
        self.fenetre.destroy()
    def saisie(self):
        self.quitter()
        master=Tk()
        master.title('Saisie des données')
        h=master.winfo_screenheight()
        w=master.winfo_screenwidth()
        master.geometry(str(w//3)+'x'+str(h//3)+'+'+str(w//3)+'+'+str(h//3))
        app=SaisieDonnee(master)
        master.mainloop()
        
        
class SaisieDonnee():
    def __init__(self,root):
        self.fenetre=root
        try:
            self.db=sqlite3.connect('Base_ONEP')
            self.c=self.db.cursor()
            self.c.execute('create table IF NOT EXISTS Entrepot(Id_e integer primary key AUTOINCREMENT, Nom_e varchar UNIQUE, Csi float, ouvert integer);')
            self.c.execute('create table IF NOT EXISTS Region(Id_r integer primary key AUTOINCREMENT, Nom_r varchar UNIQUE,Dj float);')
            self.c.execute('create table IF NOT EXISTS Desservir(Id_e integer references Entrepot(Id_e),Id_r integer references Region(Id_r),Cij float,Yij integer Default 0,primary key(Id_e,Id_r));')
            self.c.execute("select * from Entrepot;")
            L=self.c.fetchall()
            self.c.execute("select * from Region;")
            L1=self.c.fetchall()
        except Exception as e:
            showwarning('Attention',e)
        else:
            
            #interface graphique
            self.cadre=LabelFrame(root,text='',width=100,height=100,borderwidth=2)
            self.cadre.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            
            self.label1=Label(self.cadre,text='Nombre d\'entrepôts déjà enregistrés : '+str(len(L)),justify='left')
            self.label1.grid(column=0, row=0, sticky='w', in_=self.cadre)
            
            self.label2=Label(self.cadre,text='Nombre de régions déjà enregistrées : '+str(len(L1)),justify='left')
            self.label2.grid(column=0, row=1, sticky='w', in_=self.cadre)
            
            self.label3=Label(self.cadre,text='Nombre d\'entrepôts à enregistrer : ',justify='left')
            self.label3.grid(column=0, row=2, sticky='w', in_=self.cadre)
            self.saisie1=Entry(self.cadre,justify='left')
            self.saisie1.grid(column=1, row=2, sticky='w', in_=self.cadre)
            
            self.label4=Label(self.cadre,text='Nombre de régions à enregistrer : ',justify='left')
            self.label4.grid(column=0, row=3, sticky='w', in_=self.cadre)
            self.saisie2=Entry(self.cadre,justify='left')
            self.saisie2.grid(column=1, row=3, sticky='w', in_=self.cadre)
            
            self.Valider=Button(self.cadre,text='Valider',command=self.valider,width=15,bg='orange',fg='white')
            self.Valider.grid(column=0, row=4, sticky='w', in_=self.cadre)
            self.Valider=Button(self.cadre,text='Quitter',command=self.quitter,width=15,bg='orange',fg='white')
            self.Valider.grid(column=1, row=4, sticky='w', in_=self.cadre)
        
        nbR=0
        nbE=0
    def quitter(self):
        self.fenetre.destroy()
    def valider(self):
        try:
            try:
                SaisieDonnee.nbE=int(self.saisie1.get())
            except Exception as e:
                showwarning('Attention','Entrée: Nombre entrepôts, invalide')
                raise
            try:
                SaisieDonnee.nbR=int(self.saisie2.get())
            except Exception as e:
                showwarning('Attention','Entrée: Nombre régions, invalide')
                raise
        except Exception as e:
            pass
        else:
            self.quitter()
            master=Tk()
            master.title('Saisie des régions')
            h=master.winfo_screenheight()//100*100-10
            w=master.winfo_screenwidth()//100*100+50
            master.geometry(str(w)+'x'+str(h)+'+0+0')
            app=SaisieRegion(master)
            master.mainloop()
        
        
class SaisieRegion(SaisieDonnee):
    def __init__(self,root):
        SaisieDonnee.__init__(self,root)
        self.cadre.pack_forget()
        
        #classe fille
        self.compteur=1
        self.compteurMod=0
        self.cadre1=LabelFrame(root,text='',width=100,height=100,borderwidth=2)
        self.cadre1.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        
        self.label11=Label(self.cadre1,text='Nombre de régions enregistrées : 0/'+str(SaisieDonnee.nbR),justify='left')
        self.label11.grid(column=0, row=0, sticky='w', in_=self.cadre1)
        self.label12=Label(self.cadre1,text='Nombre de régions restantes : '+str(SaisieDonnee.nbR),justify='left')
        self.label12.grid(column=0, row=1, sticky='w', in_=self.cadre1)
        self.label13=Label(self.cadre1,text='Nombre de régions ajoutées : 0',justify='left')
        self.label13.grid(column=0, row=2, sticky='w', in_=self.cadre1)
        self.label14=Label(self.cadre1,text='Nombre de régions modifiées : 0',justify='left')
        self.label14.grid(column=0, row=3, sticky='w', in_=self.cadre1)
        
        
        self.cadre2=LabelFrame(root,text='',width=100,height=100,borderwidth=2)
        self.cadre2.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        
        self.label21=Label(self.cadre2,text='Région '+str(self.compteur),justify='left')
        self.label21.grid(column=0, row=0, sticky='w', in_=self.cadre2)
        self.saisie21=Entry(self.cadre2,justify='left')
        self.saisie21.grid(column=1, row=0, sticky='w', in_=self.cadre2)
        self.label22=Label(self.cadre2,text='Demande de la région ',justify='left')
        self.label22.grid(column=0, row=1, sticky='w', in_=self.cadre2)
        self.saisie22=Entry(self.cadre2,justify='left')
        self.saisie22.grid(column=1, row=1, sticky='w', in_=self.cadre2)
        self.Valider2=Button(self.cadre2,text='Valider',command=self.valider,width=15,bg='orange',fg='white')
        self.Valider2.grid(column=2, row=2, sticky='w', in_=self.cadre2)
        
        self.cadre3=LabelFrame(root,text='',width=100,height=20,borderwidth=2)
        self.cadre3.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        self.tree1 = ttk.Treeview(self.cadre3,columns=['A','B','C'], show="headings",height=20)
        self.tree1.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
        self.tree1.column("B", width=100,anchor="center",minwidth= 100)
        self.tree1.column("C", width=100,anchor="center",minwidth= 100 )
        self.tree1.heading("A", text="N°")
        self.tree1.heading("B", text="Région")
        self.tree1.heading("C", text="Demande de la région")
        
        vsb1 = ttk.Scrollbar(orient="vertical",command=self.tree1.yview)
        hsb1 = ttk.Scrollbar(orient="horizontal",command=self.tree1.xview)
        self.tree1.configure(yscrollcommand=vsb1.set,xscrollcommand=hsb1.set)
        self.tree1.grid(column=0, row=0, sticky='nsew', in_=self.cadre3)
        vsb1.grid(column=1, row=0, sticky='ns', in_=self.cadre3)
        hsb1.grid(column=0, row=1, sticky='ew', in_=self.cadre3)
        self.cadre3.grid_columnconfigure(0, weight=1)
        self.cadre3.grid_rowconfigure(0, weight=1)
        self.tree1.bind('<Double-Button-1>', self.update_tree)
        self.dictionnaire={}
        self.MODIFIER=0
        self.k=0 #pour la tree
        self.iid=0
        self.Fermer=Button(self.cadre3,text='Quitter la saisie',command=self.quitterF,width=20,bg='orange',fg='white')
        self.Fermer.grid(column=2, row=2, sticky='e',in_=self.cadre3)
        self.Continuer=Button(self.cadre3,text='Continuer >> Entrepôts',command=self.entrepots,width=20,bg='orange',fg='white')
        self.Continuer.grid(column=2, row=3, sticky='e',in_=self.cadre3)
    def quitterF(self):
        self.fenetre.destroy()
        main()
        
    def entrepots(self):
        self.quitter()
        master=Tk()
        master.title('Saisie des entrepôts')
        h=master.winfo_screenheight()//100*100-10
        w=master.winfo_screenwidth()//100*100+50
        master.geometry(str(w)+'x'+str(h)+'+0+0')
        app=Entrepots(master)
        master.mainloop()
           
    def valider(self):
        if self.MODIFIER==0:
            #enregistrement dans la base
            try:
                self.c.execute('insert into Region(Nom_r,Dj) values(?,?)',(self.saisie21.get(),float(self.saisie22.get())))
            except Exception as e:
                showwarning('Attention',e)
            else:
                self.db.commit()
                #insertion dans la liste
                self.iid=self.tree1.insert("",self.k,text=str(self.k),values=(str(self.k),self.saisie21.get(),self.saisie22.get()));self.k+=1
                self.dictionnaire[self.iid]=(self.saisie21.get(),self.saisie22.get())
                #mise à jour de la fenetre
                if SaisieDonnee.nbR-self.compteur>=0:
                    #mise à jour des labels
                    self.label11.config(text='Nombre de régions enregistrées : '+str(self.compteur)+'/'+str(SaisieDonnee.nbR))
                    self.label12.config(text='Nombre de régions restantes :'+str(SaisieDonnee.nbR-self.compteur))
                else:
                    #mise à jour du bouton
                    self.Valider2.config(text='Ajouter')
                    self.label13.config(text='Nombre de régions ajoutées : '+str(-(SaisieDonnee.nbR-self.compteur)))
                self.label21.config(text='Région :'+str(self.compteur))
                self.compteur+=1
            finally:
                #raz des zones de saisie
                self.saisie21.delete(0, END)
                self.saisie22.delete(0, END)
                self.tree1.selection_set(self.iid)
        else:
            
            try:
                self.c.execute('update Region set Nom_r=?,Dj=? where Id_r in (select Id_r from Region where Nom_r==?);',(self.saisie21.get(),float(self.saisie22.get()),self.dictionnaire[self.iid[0]][0]))
            except Exception as e:
                showwarning('Attention',e)
            else:
                self.db.commit()
                #mise à jour dans la liste
                self.tree1.set(self.iid,'B',self.saisie21.get())
                self.tree1.set(self.iid,'C',self.saisie22.get())
                self.dictionnaire[self.iid[0]]=tuple([self.saisie21.get(),self.saisie22.get()])
                self.compteurMod+=1
                self.label14.config(text='Nombre de régions modifiées : '+str(self.compteurMod))
                self.MODIFIER=0
                if SaisieDonnee.nbR-self.compteur>=0:
                    self.Valider2.config(text='Valider')
                else:
                    self.Valider2.config(text='Ajouter')
            finally:
                #raz des zones de saisie
                self.saisie21.delete(0, END)
                self.saisie22.delete(0, END)
                self.tree1.selection_set(self.iid)

    def update_tree(self,event):
        #raz des zones de saisie
        self.saisie21.delete(0, END)
        self.saisie22.delete(0, END)
        #mise à jour du bouton
        self.MODIFIER=1
        self.Valider2.config(text='Modifier')
        self.iid=self.tree1.selection()
        self.saisie21.insert(0, self.dictionnaire[self.iid[0]][0])
        self.saisie22.insert(0, self.dictionnaire[self.iid[0]][1])

class Entrepots(SaisieDonnee):
    def __init__(self,root):
        SaisieDonnee.__init__(self,root)
        self.cadre.pack_forget()
        #classe fille
        
        self.compteur=1
        self.compteurMod=0
        
        self.cadre1=LabelFrame(root,text='',width=100,height=100,borderwidth=2)
        self.cadre1.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        
        self.label11=Label(self.cadre1,text='Nombre d\'entrepôts enregistrés : 0/'+str(SaisieDonnee.nbE),justify='left')
        self.label11.grid(column=0, row=0, sticky='w', in_=self.cadre1)
        self.label12=Label(self.cadre1,text='Nombre d\'entrepôts restants : '+str(SaisieDonnee.nbE),justify='left')
        self.label12.grid(column=0, row=1, sticky='w', in_=self.cadre1)
        self.label13=Label(self.cadre1,text='Nombre d\'entrepôts ajoutés : 0',justify='left')
        self.label13.grid(column=0, row=2, sticky='w', in_=self.cadre1)
        self.label14=Label(self.cadre1,text='Nombre d\'entrepôts modifiés : 0',justify='left')
        self.label14.grid(column=0, row=3, sticky='w', in_=self.cadre1)
        
        
        self.cadre2=LabelFrame(root,text='',width=100,height=100,borderwidth=2)
        self.cadre2.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        
        self.label21=Label(self.cadre2,text='Entrepôt '+str(self.compteur),justify='left')
        self.label21.grid(column=0, row=0, sticky='w', in_=self.cadre2)
        self.saisie21=Entry(self.cadre2,justify='left')
        self.saisie21.grid(column=1, row=0, sticky='w', in_=self.cadre2)
        self.label22=Label(self.cadre2,text='Coût de transport entre la SNEP et l\'entrepôt ',justify='left')
        self.label22.grid(column=0, row=1, sticky='w', in_=self.cadre2)
        self.saisie22=Entry(self.cadre2,justify='left')
        self.saisie22.grid(column=1, row=1, sticky='w', in_=self.cadre2)
        self.label23=Label(self.cadre2,text='Ouvert ',justify='left')
        self.label23.grid(column=0, row=2, sticky='w', in_=self.cadre2)
        self.valueOuvert=StringVar()
        self.valueOuvert.set('1')
        self.bouton1=Radiobutton(self.cadre2,text='Oui',variable=self.valueOuvert,value='1')
        self.bouton1.grid(column=1, row=2, sticky='w', in_=self.cadre2)
        self.bouton2=Radiobutton(self.cadre2,text='Non',variable=self.valueOuvert,value='2')
        self.bouton2.grid(column=1, row=3, sticky='w', in_=self.cadre2)
        
        self.Valider2=Button(self.cadre2,text='Valider',command=self.valider,width=15,bg='orange',fg='white')
        self.Valider2.grid(column=4, row=5, sticky='w', in_=self.cadre2)
        
        self.cadre3=LabelFrame(root,text='',width=100,height=20,borderwidth=2)
        self.cadre3.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        self.tree1 = ttk.Treeview(self.cadre3,columns=['A','B','C','G'], show="headings",height=20)
        self.tree1.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
        self.tree1.column("B", width=100,anchor="center",minwidth= 100)
        self.tree1.column("C", width=100,anchor="center",minwidth= 100 )
        self.tree1.column("G", width=100,anchor="center",minwidth= 100 )
        
        self.tree1.heading("A", text="N°")
        self.tree1.heading("B", text="Entrepôt")
        self.tree1.heading("C", text="Coût snep entrepôt")
        self.tree1.heading("G", text="Ouvert(1)/Fermé(0)")
        
        vsb1 = ttk.Scrollbar(orient="vertical",command=self.tree1.yview)
        hsb1 = ttk.Scrollbar(orient="horizontal",command=self.tree1.xview)
        self.tree1.configure(yscrollcommand=vsb1.set,xscrollcommand=hsb1.set)
        self.tree1.grid(column=0, row=0, sticky='nsew', in_=self.cadre3)
        vsb1.grid(column=1, row=0, sticky='ns', in_=self.cadre3)
        hsb1.grid(column=0, row=1, sticky='ew', in_=self.cadre3)
        self.cadre3.grid_columnconfigure(0, weight=1)
        self.cadre3.grid_rowconfigure(0, weight=1)
        self.tree1.bind('<Double-Button-1>', self.update_tree)
        self.dictionnaire={}
        self.MODIFIER=0
        self.k=0 #pour la tree
        self.iid=0
        self.Fermer=Button(self.cadre3,text='Quitter la saisie',command=self.quitter,width=20,bg='orange',fg='white')
        self.Fermer.grid(column=2, row=2, sticky='e',in_=self.cadre3)
        self.Continuer=Button(self.cadre3,text='Continuer >> Dessertes',command=self.dessertes,width=20,bg='orange',fg='white')
        self.Continuer.grid(column=2, row=3, sticky='e',in_=self.cadre3)
        
    def dessertes(self):
        self.fenetre.destroy()
        master=Tk()
        master.title('Saisie des dessertes')
        h=master.winfo_screenheight()//100*100-10
        w=master.winfo_screenwidth()//100*100+50
        master.geometry(str(w)+'x'+str(h)+'+0+0')
        app=SaisieDessertes(master)
        master.mainloop()
    def quitter(self):
        self.fenetre.destroy()
        main()
    def valider(self):
        if self.MODIFIER==0:
            #enregistrement dans la base
            try:
                self.c.execute('insert into entrepot(Nom_e,Csi,ouvert) values(?,?,?)',(self.saisie21.get(),float(self.saisie22.get()),int(self.valueOuvert.get())%2))
            except Exception as e:
                showwarning('Attention',e)
            else:
                self.db.commit()
                #insertion dans la liste
                self.iid=self.tree1.insert("",self.k,text=str(self.k),values=(str(self.k),self.saisie21.get(),self.saisie22.get(),int(self.valueOuvert.get())%2));self.k+=1
                self.dictionnaire[self.iid]=(self.saisie21.get(),self.saisie22.get(),int(self.valueOuvert.get())%2)
                #mise à jour de la fenetre
                if SaisieDonnee.nbE-self.compteur>=0:
                    #mise à jour des labels
                    self.label11.config(text='Nombre d\'entrepôts enregistrés : '+str(self.compteur)+'/'+str(SaisieDonnee.nbE))
                    self.label12.config(text='Nombre d\'entrepôts restants :'+str(SaisieDonnee.nbE-self.compteur))
                else:
                    #mise à jour du bouton
                    self.Valider2.config(text='Ajouter')
                    self.label13.config(text='Nombre d\'entrepôts ajoutés : '+str(-(SaisieDonnee.nbE-self.compteur)))
                self.label21.config(text='Entrepôt :'+str(self.compteur))
                self.compteur+=1
            finally:
                #raz des zones de saisie
                self.saisie21.delete(0, END)
                self.saisie22.delete(0, END)
                self.tree1.selection_set(self.iid)
        else:
            try:
                self.c.execute('update entrepot set Nom_e=?,Csi=?,ouvert=? where Id_e in (select Id_e from entrepot where Nom_e==?);',(self.saisie21.get(),float(self.saisie22.get()),int(self.valueOuvert.get())%2,self.dictionnaire[self.iid[0]][0]))
                
            except Exception as e:
                showwarning('Attention',e)
            else:
                self.db.commit()
                #mise à jour dans la liste
                self.tree1.set(self.iid,'B',self.saisie21.get())
                self.tree1.set(self.iid,'C',self.saisie22.get())
                self.tree1.set(self.iid,'G',int(self.valueOuvert.get())%2)
                self.dictionnaire[self.iid[0]]=tuple([self.saisie21.get(),self.saisie22.get(),int(self.valueOuvert.get())%2])
                self.compteurMod+=1
                self.label14.config(text='Nombre d\'entrepôts modifiés : '+str(self.compteurMod))
                self.MODIFIER=0
                if SaisieDonnee.nbE-self.compteur>=0:
                    self.Valider2.config(text='Valider')
                else:
                    self.Valider2.config(text='Ajouter')
            finally:
                #raz des zones de saisie
                self.saisie21.delete(0, END)
                self.saisie22.delete(0, END)
                self.tree1.selection_set(self.iid)

    def update_tree(self,event):
        #raz des zones de saisie
        self.saisie21.delete(0, END)
        self.saisie22.delete(0, END)
        #mise à jour du bouton
        self.MODIFIER=1
        self.Valider2.config(text='Modifier')
        self.iid=self.tree1.selection()
        self.saisie21.insert(0, self.dictionnaire[self.iid[0]][0])
        self.saisie22.insert(0, self.dictionnaire[self.iid[0]][1])
        if self.dictionnaire[self.iid[0]][2]==0:
            self.valueOuvert.set('2')
        else:
            self.valueOuvert.set('1')
class ModifierRegion():
    def __init__(self,root):
        self.fenetre=root
        self.cadre=LabelFrame(root,text='',width=100,height=20,borderwidth=2)
        self.cadre.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        self.tree1 = ttk.Treeview(self.cadre,columns=['A','AA','B','C'], show="headings",height=20)
        self.tree1.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
        self.tree1.column("AA", width=100,anchor="center", minwidth= 100)
        self.tree1.column("B", width=100,anchor="center",minwidth= 100)
        self.tree1.column("C", width=100,anchor="center",minwidth= 100 )
        self.tree1.heading("A", text="N°")
        self.tree1.heading("AA", text="Id_r")
        self.tree1.heading("B", text="Région")
        self.tree1.heading("C", text="Demande de la région")
        
        vsb1 = ttk.Scrollbar(orient="vertical",command=self.tree1.yview)
        hsb1 = ttk.Scrollbar(orient="horizontal",command=self.tree1.xview)
        self.tree1.configure(yscrollcommand=vsb1.set,xscrollcommand=hsb1.set)
        self.tree1.grid(column=0, row=0, sticky='nsew', in_=self.cadre)
        vsb1.grid(column=1, row=0, sticky='ns', in_=self.cadre)
        hsb1.grid(column=0, row=1, sticky='ew', in_=self.cadre)
        self.cadre.grid_columnconfigure(0, weight=1)
        self.cadre.grid_rowconfigure(0, weight=1)
        self.tree1.bind('<Double-Button-1>', self.update_tree)
        #les zones de saisie
        self.cadre1=LabelFrame(root,text='',width=100,height=100,borderwidth=2)
        self.cadre1.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        self.label21=Label(self.cadre1,text='Région ',justify='left')
        self.label21.grid(column=0, row=0, sticky='w', in_=self.cadre1)
        self.saisie21=Entry(self.cadre1,justify='left')
        self.saisie21.grid(column=1, row=0, sticky='w', in_=self.cadre1)
        self.label22=Label(self.cadre1,text='Demande de la région ',justify='left')
        self.label22.grid(column=0, row=1, sticky='w', in_=self.cadre1)
        self.saisie22=Entry(self.cadre1,justify='left')
        self.saisie22.grid(column=1, row=1, sticky='w', in_=self.cadre1)
        #boutons
        self.Fermer=Button(self.cadre1,text='Terminer',command=self.quitter,width=15,bg='orange',fg='white')
        self.Fermer.grid(column=4, row=2, sticky='e',in_=self.cadre1)
        
        self.Valider=Button(self.cadre1,text='Valider',command=self.valider,width=15,bg='orange',fg='white')
        self.Valider.grid(column=2, row=2, sticky='e',in_=self.cadre1)
        
        self.Annuler=Button(self.cadre1,text='Annuler',command=self.annuler,width=15,bg='orange',fg='white')
        self.Annuler.grid(column=1, row=2, sticky='e',in_=self.cadre1)
        #remplissage de la tree
        self.dictionnaire={}
        try:
            self.db=sqlite3.connect('Base_ONEP')
            self.c=self.db.cursor()
            self.c.execute("select * from Region;")
            self.L=self.c.fetchall()
        except Exception as e:
            showwarning('Attention',e)
        else:
            for i in range(len(self.L)):
                self.iid=self.tree1.insert("",i,text=str(i),values=(str(i),self.L[i][0],self.L[i][1],self.L[i][2]))
                self.dictionnaire[self.iid]=[self.L[i][0],self.L[i][1],self.L[i][2]]
            self.tree1.selection_set(self.iid)
        
    def quitter(self):
        self.fenetre.destroy()
        main()
    def valider(self):
        try:
            self.c.execute('update Region set Nom_r=?,Dj=? where Id_r in (select Id_r from Region where Nom_r==?);',(self.saisie21.get(),float(self.saisie22.get()),self.dictionnaire[self.iid[0]][1]))
        except Exception as e:
            showwarning('Attention',e)
        else:
            self.db.commit()
            #mise à jour dans la liste
            self.tree1.set(self.iid,'B',self.saisie21.get())
            self.tree1.set(self.iid,'C',self.saisie22.get())
            self.dictionnaire[self.iid[0]][1]=self.saisie21.get()
            self.dictionnaire[self.iid[0]][2]=self.saisie22.get()
        finally:
            #raz des zones de saisie
            self.saisie21.delete(0, END)
            self.saisie22.delete(0, END)
            self.tree1.selection_set(self.iid)
            self.saisie21.focus_set()
    def update_tree(self,event):
        #raz des zones de saisie
        self.saisie21.delete(0, END)
        self.saisie22.delete(0, END)
        self.iid=self.tree1.selection()
        self.saisie21.insert(0, self.dictionnaire[self.iid[0]][1])
        self.saisie22.insert(0, self.dictionnaire[self.iid[0]][2])
        self.saisie21.focus_set()
    def annuler(self):
        self.saisie21.delete(0, END)
        self.saisie22.delete(0, END)
        self.saisie21.focus_set() 
class ModifierEntrepot():
    def __init__(self,root):
        self.fenetre=root
        try:
            self.db=sqlite3.connect('Base_ONEP')
            self.c=self.db.cursor()
            self.c.execute("select Nom_r from Region;")
            self.L=[e[0] for e in self.c.fetchall()]
            self.c.execute('''  select * 
                                from entrepot;''') 
            self.L1=self.c.fetchall()
        except Exception as e:
            showwarning('Attention',e)
        else:
            self.cadre3=LabelFrame(root,text='',width=50,height=10,borderwidth=2)
            self.cadre3.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            self.tree1 = ttk.Treeview(self.cadre3,columns=['A','B','C','D','E'], show="headings",height=10)
            
            self.tree1.column("A", width=10,anchor="w", stretch = True, minwidth= 50)
            self.tree1.column("B", width=10,anchor="center",minwidth= 10)
            self.tree1.column("C", width=10,anchor="center",minwidth= 10 )
            self.tree1.column("D", width=10,anchor="center",minwidth= 10 )
            self.tree1.column("E", width=10,anchor="center",minwidth= 10 )
                       
            self.tree1.heading("A", text="N°")
            self.tree1.heading("B", text="Id_e")
            self.tree1.heading("C", text="Entrepôt")
            self.tree1.heading("D", text="Coût snep entrepôt")
            self.tree1.heading("E", text="Ouvert(1)/Fermé(0)")
            
            vsb1 = ttk.Scrollbar(orient="vertical",command=self.tree1.yview)
            hsb1 = ttk.Scrollbar(orient="horizontal",command=self.tree1.xview)
            self.tree1.configure(yscrollcommand=vsb1.set,xscrollcommand=hsb1.set)
            self.tree1.grid(column=0, row=0, sticky='nsew', in_=self.cadre3)
            vsb1.grid(column=1, row=0, sticky='ns', in_=self.cadre3)
            hsb1.grid(column=0, row=1, sticky='ew', in_=self.cadre3)
            self.cadre3.grid_columnconfigure(0, weight=1)
            self.cadre3.grid_rowconfigure(0, weight=1)
            self.tree1.bind('<Double-Button-1>', self.update_tree)
            
            self.cadre4=LabelFrame(root,text='',width=100,height=20,borderwidth=2)
            self.cadre4.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            self.label21=Label(self.cadre4,text='Entrepôt ',justify='left')
            self.label21.grid(column=0, row=0, sticky='w', in_=self.cadre4)
            self.saisie21=Entry(self.cadre4,justify='left')
            self.saisie21.grid(column=1, row=0, sticky='w', in_=self.cadre4)
            
            self.label22=Label(self.cadre4,text='Coût de transport \nentre la SNEP et l\'entrepôt ',justify='left')
            self.label22.grid(column=0, row=1, sticky='w', in_=self.cadre4)
            self.saisie22=Entry(self.cadre4,justify='left')
            self.saisie22.grid(column=1, row=1, sticky='w', in_=self.cadre4)
            
            self.label23=Label(self.cadre4,text='Ouvert ',justify='left')
            self.label23.grid(column=0, row=2, sticky='w', in_=self.cadre4)
            self.valueOuvert=StringVar()
            self.valueOuvert.set('1')
            self.bouton1=Radiobutton(self.cadre4,text='Oui',variable=self.valueOuvert,value='1')
            self.bouton1.grid(column=1, row=2, sticky='w', in_=self.cadre4)
            self.bouton2=Radiobutton(self.cadre4,text='Non',variable=self.valueOuvert,value='2')
            self.bouton2.grid(column=1, row=3, sticky='w', in_=self.cadre4)
            
            self.ValiderE=Button(self.cadre4,text='Modifier Entrepôt',command=self.validerE,width=15,bg='orange',fg='white')
            self.ValiderE.grid(column=2, row=4, sticky='w', in_=self.cadre4)
            self.AnnulerE=Button(self.cadre4,text='Annuler',command=self.annulerE,width=15,bg='orange',fg='white')
            self.AnnulerE.grid(column=3, row=4, sticky='e',in_=self.cadre4)

            ###########-----------------------------------------------------------------------------------------------------

            self.cadre2=LabelFrame(root,text='',width=50,height=10,borderwidth=2)
            self.cadre2.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            self.cadre21=LabelFrame(self.cadre2,text='',width=50,height=10,borderwidth=2)
            self.cadre21.pack(side=LEFT,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            self.label21=Label(self.cadre21,text='Les régions desservies par l\'entrepôt sélectionné sont : ',justify='left')
            self.label21.grid(column=0, row=0,sticky='w', in_=self.cadre21)

            self.tree2 = ttk.Treeview(self.cadre21,columns=['A','B','C','D','E','F'], show="headings",height=10)
            self.tree2.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
            self.tree2.column("B", width=100,anchor="center",minwidth= 100)
            self.tree2.column("C", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("D", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("E", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("F", width=100,anchor="center",minwidth= 100 )
            
            self.tree2.heading("A", text="N°")
            self.tree2.heading("B", text="Id_r")
            self.tree2.heading("C", text="Région")
            self.tree2.heading("D", text="Demande de la région")
            self.tree2.heading("E", text="Coût Entrepôt-région")
            self.tree2.heading("F", text="Desservie")
            
            vsb2 = ttk.Scrollbar(orient="vertical",command=self.tree2.yview)
            hsb2 = ttk.Scrollbar(orient="horizontal",command=self.tree2.xview)
            self.tree2.configure(yscrollcommand=vsb2.set,xscrollcommand=hsb2.set)
            self.tree2.grid(column=0, row=1, sticky='nsew', in_=self.cadre21)
            vsb2.grid(column=1, row=1, sticky='ns', in_=self.cadre21)
            hsb2.grid(column=0, row=2, sticky='ew', in_=self.cadre21)
            self.cadre21.grid_columnconfigure(0, weight=1)
            self.cadre21.grid_rowconfigure(0, weight=1)
            self.tree2.bind('<Double-Button-1>', self.update_tree2)
            
            self.cadre22=LabelFrame(self.cadre2,text='',width=50,height=10,borderwidth=2)
            self.cadre22.pack(side=LEFT,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            
            self.label24=Label(self.cadre22,text='Coût de transport \nentre l\'entrepôt \n et la région',justify='left')
            self.label24.grid(column=2, row=3, sticky='w', in_=self.cadre22)
            self.comboregion=ttk.Combobox(self.cadre22,width=15,state='readonly')
            self.comboregion['values']=tuple([self.L[i] for i in range(len(self.L))])
            self.comboregion.grid(column=3, row=3, sticky='w', in_=self.cadre22)
            self.label25=Label(self.cadre22,text='Coût ',justify='left')
            self.label25.grid(column=4, row=3, sticky='w', in_=self.cadre22)
            self.saisie23=Entry(self.cadre22,justify='left')
            self.saisie23.grid(column=5, row=3, sticky='w', in_=self.cadre22)
            
            self.label26=Label(self.cadre22,text='desservie ',justify='left')
            self.label26.forget()
            self.valuedesservie=StringVar()
            self.valuedesservie.set('2')
            self.bouton3=Radiobutton(self.cadre22,text='Oui',variable=self.valuedesservie,value='1')
            self.bouton3.forget()
            self.bouton4=Radiobutton(self.cadre22,text='Non',variable=self.valuedesservie,value='2')
            self.bouton4.forget()
            
            self.ValiderD=Button(self.cadre22,text='Modifier \nla desserte',command=self.validerD,width=15,bg='orange',fg='white')
            self.ValiderD.grid(column=6, row=6, sticky='w', in_=self.cadre22)
            self.ValiderD['state']='disabled'
            self.AnnulerD=Button(self.cadre22,text='Annuler   ',command=self.annulerD,width=15,bg='orange',fg='white')
            self.AnnulerD.grid(column=5, row=7, sticky='e',in_=self.cadre22)
            self.Fermer=Button(self.cadre22,text='Terminer',command=self.quitter,width=15,bg='orange',fg='white')
            self.Fermer.grid(column=6, row=7, sticky='e',in_=self.cadre22)
            #remplissage de la tree1
            self.dictionnaire={}
            for i in range(len(self.L1)):
                self.iid=self.tree1.insert("",i,text=str(i),values=(str(i),self.L1[i][0],self.L1[i][1],self.L1[i][2],int(self.L1[i][3])%2))
                self.dictionnaire[self.iid]=[self.L1[i][0],self.L1[i][1],self.L1[i][2],int(self.L1[i][3])%2]
            self.tree1.selection_set(self.iid)
            
            
    
            
    def annulerE(self):
        self.saisie21.delete(0, END)
        self.saisie22.delete(0, END)
        

    def quitter(self):
        self.fenetre.destroy()
        main()
        
    def validerE(self):
        try:
            self.c.execute('update entrepot set Nom_e=?,Csi=?,ouvert=? where Id_e ==?;',(self.saisie21.get(),float(self.saisie22.get()),int(self.valueOuvert.get())%2,self.dictionnaire[self.iid[0]][0]))
            
        except Exception as e:
            showwarning('Attention',e)
        else:
            self.db.commit()
            #mise à jour dans la liste
            self.tree1.set(self.iid,'C',self.saisie21.get())
            self.tree1.set(self.iid,'D',self.saisie22.get())
            self.tree1.set(self.iid,'E',int(self.valueOuvert.get())%2)
            
            self.dictionnaire[self.iid[0]][1]=self.saisie21.get()
            self.dictionnaire[self.iid[0]][2]=self.saisie22.get()
            self.dictionnaire[self.iid[0]][3]=int(self.valueOuvert.get())%2
                            
        finally:
            #raz des zones de saisie
            self.tree1.selection_set(self.iid)
            self.update_tree(None)
    
            
    
    def update_tree(self,event):
        #raz des zones de saisie
        self.saisie21.delete(0, END)
        self.saisie22.delete(0, END)
        x = self.tree2.get_children()
        for item in x:
            self.tree2.delete(item)
        
        #mise à jour des zones de saisie
        self.iid=self.tree1.selection()
        self.saisie21.insert(0, self.dictionnaire[self.iid[0]][1])
        self.saisie22.insert(0, self.dictionnaire[self.iid[0]][2])
        if self.dictionnaire[self.iid[0]][3]==0:
            self.valueOuvert.set('2')
        else:
            self.valueOuvert.set('1')
        
        #remplissage de la tree2
        self.dictionnaire1={}
        try:
            self.c.execute("select d.Id_r,r.Nom_r,r.Dj,d.Cij,d.Yij from desservir d join region r on d.Id_r==r.Id_r where d.Id_e==?",(self.dictionnaire[self.iid[0]][0],))
            self.L2=self.c.fetchall()
        except Exception as e:
            showwarning('Attention',e)
        else:
            for i in range(len(self.L2)):
                self.iid1=self.tree2.insert("",i,text=str(i),values=(str(i),self.L2[i][0],self.L2[i][1],self.L2[i][2],self.L2[i][3],self.L2[i][4]))
                self.dictionnaire1[self.iid1]=[self.L2[i][0],self.L2[i][1],self.L2[i][2],self.L2[i][3],self.L2[i][4]]
            if len(self.L2)!=0:
                self.ValiderD['state']='normal'
                self.tree2.selection_set(self.iid1)
                self.update_tree2(None)
            else:
                self.label26.grid_forget()
                self.bouton3.grid_forget()
                self.bouton4.grid_forget()
                self.ValiderD['state']='disabled'
                
    def update_tree2(self,event):
        #vider la zone Cij
        self.saisie23.delete(0, END)
        #mise à jour des zones de saisie
        self.iid1=self.tree2.selection()
        self.comboregion.current(self.L.index(self.dictionnaire1[self.iid1[0]][1]))
        self.saisie23.insert(0,self.dictionnaire1[self.iid1[0]][3])
        if (self.dictionnaire[self.iid[0]][3])%2!=0:
            
            self.label26.grid(column=2, row=4, sticky='w', in_=self.cadre22)
            self.bouton3.grid(column=3, row=4, sticky='w', in_=self.cadre22)
            self.bouton4.grid(column=3, row=5, sticky='w', in_=self.cadre22)
            if self.dictionnaire1[self.iid1[0]][4]==0 or self.dictionnaire1[self.iid1[0]][4]==None:
                self.valuedesservie.set('2')
            else:
                self.valuedesservie.set('1')
        else:
            self.label26.grid_forget()
            self.bouton3.grid_forget()
            self.bouton4.grid_forget()
            


    def annulerD(self):
        self.saisie23.delete(0, END)
        self.comboregion.current(0)
        if (self.dictionnaire[self.iid[0]][3])%2!=0:
            self.label26.grid(column=2, row=4, sticky='w', in_=self.cadre22)
            self.bouton3.grid(column=3, row=4, sticky='w', in_=self.cadre22)
            self.bouton4.grid(column=3, row=5, sticky='w', in_=self.cadre22)
            self.valuedesservie.set('2')
        else:
            self.label26.grid_forget()
            self.bouton3.grid_forget()
            self.bouton4.grid_forget()
            
    def validerD(self):
        if self.saisie23.get()!='':
            self.indicereg=self.comboregion.current()
            try:
                self.c.execute("select Id_r from region where Nom_r==?;",(self.L[self.indicereg],))
                self.idr=self.c.fetchone()[0]
                self.c.execute("delete from desservir where Id_e==? and Id_r==?;",(self.dictionnaire[self.iid[0]][0],self.dictionnaire1[self.iid1[0]][0]))
                if self.dictionnaire[self.iid[0]][3]==1:
                    self.c.execute('insert into desservir (Id_r,Id_e,Cij,Yij) values(?,?,?,?);',(self.idr,self.dictionnaire[self.iid[0]][0],self.saisie23.get(),int(self.valuedesservie.get())%2))
                else:
                    self.c.execute('insert into desservir (Id_r,Id_e,Cij) values(?,?,?);',(self.idr,self.dictionnaire[self.iid[0]][0],self.saisie23.get()))
                    
            except Exception as e:
                showwarning('Attention',e)
            else:
                self.db.commit()
                self.dictionnaire1[self.iid1[0]][0]=self.idr
                self.dictionnaire1[self.iid1[0]][1]=self.L[self.indicereg]
                self.dictionnaire1[self.iid1[0]][3]=self.saisie23.get()
                self.dictionnaire1[self.iid1[0]][4]=int(self.valuedesservie.get())%2
                self.update_tree(None)
        else:
            showwarning("Attention","Information manquante")
            

            
class SupprimerRegion():
    def __init__(self,root):
        self.fenetre=root
        try:
            self.db=sqlite3.connect('Base_ONEP')
            self.c=self.db.cursor()
            self.c.execute("select * from Region;")
            self.L=self.c.fetchall()
            
        except Exception as e:
            showwarning('Attention',e)
        else:
            self.cadre3=LabelFrame(root,text='',width=100,height=15,borderwidth=2)
            self.cadre3.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            self.tree1 = ttk.Treeview(self.cadre3,columns=['A','B','C','D'], show="headings",height=15)
            
            self.tree1.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
            self.tree1.column("B", width=100,anchor="center",minwidth= 100)
            self.tree1.column("C", width=100,anchor="center",minwidth= 100 )
            self.tree1.column("D", width=100,anchor="center",minwidth= 100 )
            
            self.tree1.heading("A", text="N°")
            self.tree1.heading("B", text="Id_r")
            self.tree1.heading("C", text="Région")
            self.tree1.heading("D", text="Demande de la région")

            vsb1 = ttk.Scrollbar(orient="vertical",command=self.tree1.yview)
            hsb1 = ttk.Scrollbar(orient="horizontal",command=self.tree1.xview)
            self.tree1.configure(yscrollcommand=vsb1.set,xscrollcommand=hsb1.set)
            self.tree1.grid(column=0, row=0, sticky='nsew', in_=self.cadre3)
            vsb1.grid(column=1, row=0, sticky='ns', in_=self.cadre3)
            hsb1.grid(column=0, row=1, sticky='ew', in_=self.cadre3)
            self.cadre3.grid_columnconfigure(0, weight=1)
            self.cadre3.grid_rowconfigure(0, weight=1)
            self.tree1.bind('<Double-Button-1>', self.update_tree)
            #remplissage de la tree1
            self.dictionnaire={}
            for i in range(len(self.L)):
                self.iid=self.tree1.insert("",i,text=str(i),values=(str(i),self.L[i][0],self.L[i][1],self.L[i][2]))
                self.dictionnaire[self.iid]=[self.L[i][0],self.L[i][1],self.L[i][2]]
            self.tree1.selection_set(self.iid)
            self.label21=Label(self.cadre3,text='Les entrepôts desservant la région sélectionnée sont : ',justify='left')
            self.label21.grid(column=0, row=2,sticky='w', in_=self.cadre3)
            #la tree2
            self.cadre2=LabelFrame(root,text='',width=100,height=15,borderwidth=2)
            self.cadre2.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            
            self.tree2 = ttk.Treeview(self.cadre2,columns=['A','B','C','D','E','F','G'], show="headings",height=15)
            self.tree2.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
            self.tree2.column("B", width=100,anchor="center",minwidth= 100)
            self.tree2.column("C", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("D", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("E", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("F", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("G", width=200,anchor="center",minwidth= 200 )
            
            self.tree2.heading("A", text="N°")
            self.tree2.heading("B", text="Id_e")
            self.tree2.heading("C", text="Entrepôt")
            self.tree2.heading("D", text="Coût snep entrepôt")
            self.tree2.heading("E", text="Ouvert(1)/Fermé(0)")
            self.tree2.heading("F", text="Coût entrepôt-région")
            self.tree2.heading("G", text="desservant(1)/non desservant(0)")

            vsb2 = ttk.Scrollbar(orient="vertical",command=self.tree2.yview)
            hsb2 = ttk.Scrollbar(orient="horizontal",command=self.tree2.xview)
            self.tree2.configure(yscrollcommand=vsb2.set,xscrollcommand=hsb2.set)
            self.tree2.grid(column=0, row=0, sticky='nsew', in_=self.cadre2)
            vsb2.grid(column=1, row=0, sticky='ns', in_=self.cadre2)
            hsb2.grid(column=0, row=1, sticky='ew', in_=self.cadre2)
            self.cadre2.grid_columnconfigure(0, weight=1)
            self.cadre2.grid_rowconfigure(0, weight=1)

            self.Valider=Button(self.cadre2,text='Supprimer',command=self.supprimer,width=15,bg='orange',fg='white')
            self.Valider.grid(column=2, row=2, sticky='w', in_=self.cadre2)
            self.Fermer=Button(self.cadre2,text='Terminer',command=self.quitter,width=15,bg='orange',fg='white')
            self.Fermer.grid(column=3, row=2, sticky='e',in_=self.cadre2)
    def quitter(self):
        self.fenetre.destroy()
        main()
    def supprimer(self):
        self.iid=self.tree1.selection()
        if len(self.iid)!=0:
            reponse=messagebox.askquestion('Supprimer région','Êtes vous sûr de vouloir supprimer la région '+self.dictionnaire[self.iid[0]][1]+' ?')
            if reponse=='yes':
                try:
                    self.c.execute('delete from desservir where  Id_r==?;',(self.dictionnaire[self.iid[0]][0],))
                    self.c.execute('delete from region where  Id_r==?;',(self.dictionnaire[self.iid[0]][0],))
                except Exception as e:
                    showwarning('Attention',e)
                else:
                    self.db.commit()
                    self.tree1.delete(self.iid)
                    x = self.tree2.get_children()
                    for item in x:
                        self.tree2.delete(item)
                    del self.dictionnaire[self.iid[0]]
                    if len(self.dictionnaire)!=0:
                        x = self.tree1.get_children()
                        self.tree1.selection_set(x[0])
        else:
            showwarning('Attention','Aucune région n\'est sélectionnée')
                
    def update_tree(self,event):
        #vider la tree 2
        x = self.tree2.get_children()
        for item in x:
            self.tree2.delete(item)
        #remplissage de la tree2
        self.iid=self.tree1.selection()
        try:
            self.c.execute('''  select * 
                                from entrepot e,desservir d
                                where e.Id_e==d.Id_e and d.Id_r==?;''',(self.dictionnaire[self.iid[0]][0],)) 
            self.L1=self.c.fetchall()
        except Exception as e:
            showwarning('Attention',e)
        else:
            for i in range(len(self.L1)):
                iid1=self.tree2.insert("",i,text=str(i),values=(str(i),self.L1[i][0],self.L1[i][1],self.L1[i][2],int(self.L1[i][3])%2,self.L1[i][6],self.L1[i][7]))
            if len(self.L1)!=0:
                self.tree2.selection_set(iid1)
class SupprimerEntrepot():
    def __init__(self,root):
        self.fenetre=root
        try:
            self.db=sqlite3.connect('Base_ONEP')
            self.c=self.db.cursor()
            self.c.execute("select * from entrepot;")
            self.L=self.c.fetchall()
            
        except Exception as e:
            showwarning('Attention',e)
        else:
            
            self.cadre3=LabelFrame(root,text='',width=100,height=15,borderwidth=2)
            self.cadre3.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            self.tree1 = ttk.Treeview(self.cadre3,columns=['A','B','C','D','E'], show="headings",height=15)
            
            self.tree1.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
            self.tree1.column("B", width=100,anchor="center",minwidth= 100)
            self.tree1.column("C", width=100,anchor="center",minwidth= 100 )
            self.tree1.column("D", width=100,anchor="center",minwidth= 100 )
            self.tree1.column("E", width=100,anchor="center",minwidth= 100 )
            
            self.tree1.heading("A", text="N°")
            self.tree1.heading("B", text="Id_e")
            self.tree1.heading("C", text="Entrepôt")
            self.tree1.heading("D", text="Coût Snep-Entrepôt")
            self.tree1.heading("E", text="Ouvert(1)/Fermé(0)")
            
            vsb1 = ttk.Scrollbar(orient="vertical",command=self.tree1.yview)
            hsb1 = ttk.Scrollbar(orient="horizontal",command=self.tree1.xview)
            self.tree1.configure(yscrollcommand=vsb1.set,xscrollcommand=hsb1.set)
            self.tree1.grid(column=0, row=0, sticky='nsew', in_=self.cadre3)
            vsb1.grid(column=1, row=0, sticky='ns', in_=self.cadre3)
            hsb1.grid(column=0, row=1, sticky='ew', in_=self.cadre3)
            self.cadre3.grid_columnconfigure(0, weight=1)
            self.cadre3.grid_rowconfigure(0, weight=1)
            self.tree1.bind('<Double-Button-1>', self.update_tree)
            #remplissage de la tree1
            self.dictionnaire={}
            for i in range(len(self.L)):
                self.iid=self.tree1.insert("",i,text=str(i),values=(str(i),self.L[i][0],self.L[i][1],self.L[i][2],int(self.L[i][3])%2))
                self.dictionnaire[self.iid]=[self.L[i][0],self.L[i][1],self.L[i][2],int(self.L[i][3])%2]
            self.tree1.selection_set(self.iid)
            self.label21=Label(self.cadre3,text='Les régions desservies par l\'entrepôt sélectionné sont : ',justify='left')
            self.label21.grid(column=0, row=2,sticky='w', in_=self.cadre3)
            #la tree2
            self.cadre2=LabelFrame(root,text='',width=100,height=15,borderwidth=2)
            self.cadre2.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            
            self.tree2 = ttk.Treeview(self.cadre2,columns=['A','B','C','D','E','F'], show="headings",height=15)
            self.tree2.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
            self.tree2.column("B", width=100,anchor="center",minwidth= 100)
            self.tree2.column("C", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("D", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("E", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("F", width=100,anchor="center",minwidth= 100 )
            
            
            self.tree2.heading("A", text="N°")
            self.tree2.heading("B", text="Id_r")
            self.tree2.heading("C", text="Région")
            self.tree2.heading("D", text="Demande de la région")
            self.tree2.heading("E", text="Coût Entrepôt-région")
            self.tree2.heading("E", text="desservie(1)/non desservie(0)")
            
            vsb2 = ttk.Scrollbar(orient="vertical",command=self.tree2.yview)
            hsb2 = ttk.Scrollbar(orient="horizontal",command=self.tree2.xview)
            self.tree2.configure(yscrollcommand=vsb2.set,xscrollcommand=hsb2.set)
            self.tree2.grid(column=0, row=0, sticky='nsew', in_=self.cadre2)
            vsb2.grid(column=1, row=0, sticky='ns', in_=self.cadre2)
            hsb2.grid(column=0, row=1, sticky='ew', in_=self.cadre2)
            self.cadre2.grid_columnconfigure(0, weight=1)
            self.cadre2.grid_rowconfigure(0, weight=1)

            self.Valider=Button(self.cadre2,text='Supprimer Entrepôt',command=self.supprimerE,width=15,bg='orange',fg='white')
            self.Valider.grid(column=0, row=2, sticky='n', in_=self.cadre2)
            self.Valider1=Button(self.cadre2,text='Supprimer Desserte',command=self.supprimerD,width=15,bg='orange',fg='white')
            self.Valider1.grid(column=0, row=3, sticky='n', in_=self.cadre2)
            self.Fermer=Button(self.cadre2,text='Terminer',command=self.quitter,width=15,bg='orange',fg='white')
            self.Fermer.grid(column=0, row=4, sticky='e',in_=self.cadre2)
            self.dictionnaire1={}
    def quitter(self):
        self.fenetre.destroy()
        main()
    def supprimerE(self):
        self.iid=self.tree1.selection()
        if len(self.iid)!=0:
            reponse=messagebox.askquestion('Supprimer Entrepôt','Êtes vous sûr de vouloir supprimer l\'entrepôt '+self.dictionnaire[self.iid[0]][1]+' ?')
            if reponse=='yes':
                try:
                    self.c.execute('delete from desservir where  Id_e==?;',(self.dictionnaire[self.iid[0]][0],))
                    self.c.execute('delete from entrepot where  Id_e==?;',(self.dictionnaire[self.iid[0]][0],))
                except Exception as e:
                    showwarning('Attention',e)
                else:
                    self.db.commit()
                    self.tree1.delete(self.iid)
                    x = self.tree2.get_children()
                    for item in x:
                        self.tree2.delete(item)
                    del self.dictionnaire[self.iid[0]]
                    if len(self.dictionnaire)!=0:
                        x = self.tree1.get_children()
                        self.tree1.selection_set(x[0])
        else:
            showwarning('Attention','Aucun Entrepôt n\'est sélectionné')
                
    def update_tree(self,event):
        #vider la tree 2
        x = self.tree2.get_children()
        for item in x:
            self.tree2.delete(item)
        #remplissage de la tree2
        self.iid=self.tree1.selection()
        try:
            self.c.execute('''  select * 
                                from desservir d,region r
                                where d.Id_r==r.Id_r and d.Id_e==?;''',(self.dictionnaire[self.iid[0]][0],)) 
            self.L1=self.c.fetchall()
        except Exception as e:
            showwarning('Attention',e)
        else:
            for i in range(len(self.L1)):
                iid1=self.tree2.insert("",i,text=str(i),values=(str(i),self.L1[i][1],self.L1[i][5],self.L1[i][6],self.L1[i][2],self.L1[i][3]))
                self.dictionnaire1[iid1]=[self.L1[i][1],self.L1[i][5],self.L1[i][6],self.L1[i][2],self.L1[i][3]]
            if len(self.L1)!=0:
                self.tree2.selection_set(iid1)
    def supprimerD(self):
        self.iid1=self.tree2.selection()
        self.iid=self.tree1.selection()
        if len(self.iid1)!=0:
            try:
                self.c.execute('delete from desservir where Id_e==? and Id_r==?;',(self.dictionnaire[self.iid[0]][0],self.dictionnaire1[self.iid1[0]][0])) 
            except Exception as e:
                showwarning('Attention',e)
            else:
                self.db.commit()
                self.tree2.delete(self.iid1)
                x=self.tree2.get_children()
                if len(x)!=0:
                    self.tree2.selection_set(x[0])
        else:
            showwarning('Attention','Aucune région n\'est sélectionnée')
class AfficherRegion():
    def __init__(self,root):
        self.fenetre=root
        try:
            self.db=sqlite3.connect('Base_ONEP')
            self.c=self.db.cursor()
            self.c.execute("select * from Region;")
            self.L=self.c.fetchall()
            
        except Exception as e:
            showwarning('Attention',e)
        else:
            self.cadre3=LabelFrame(root,text='',width=100,height=10,borderwidth=2)
            self.cadre3.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            self.tree1 = ttk.Treeview(self.cadre3,columns=['A','B','C','D'], show="headings",height=10)
            
            self.tree1.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
            self.tree1.column("B", width=100,anchor="center",minwidth= 100)
            self.tree1.column("C", width=100,anchor="center",minwidth= 100 )
            self.tree1.column("D", width=100,anchor="center",minwidth= 100 )
            
            self.tree1.heading("A", text="N°")
            self.tree1.heading("B", text="Id_r")
            self.tree1.heading("C", text="Région")
            self.tree1.heading("D", text="Demande de la région")

            vsb1 = ttk.Scrollbar(orient="vertical",command=self.tree1.yview)
            hsb1 = ttk.Scrollbar(orient="horizontal",command=self.tree1.xview)
            self.tree1.configure(yscrollcommand=vsb1.set,xscrollcommand=hsb1.set)
            self.tree1.grid(column=0, row=0, sticky='nsew', in_=self.cadre3)
            vsb1.grid(column=1, row=0, sticky='ns', in_=self.cadre3)
            hsb1.grid(column=0, row=1, sticky='ew', in_=self.cadre3)
            self.cadre3.grid_columnconfigure(0, weight=1)
            self.cadre3.grid_rowconfigure(0, weight=1)
            self.tree1.bind('<Double-Button-1>', self.update_tree)
            #remplissage de la tree1
            self.dictionnaire={}
            for i in range(len(self.L)):
                self.iid=self.tree1.insert("",i,text=str(i),values=(str(i),self.L[i][0],self.L[i][1],self.L[i][2]))
                self.dictionnaire[self.iid]=[self.L[i][0],self.L[i][1],self.L[i][2]]
            self.tree1.selection_set(self.iid)
            
            self.label21=Label(self.cadre3,text='Les entrepôts desservant la région sélectionnée sont : ',justify='left')
            self.label21.grid(column=0, row=2,sticky='w', in_=self.cadre3)
            #la tree2
            self.cadre2=LabelFrame(root,text='',width=100,height=15,borderwidth=2)
            self.cadre2.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            
            self.tree2 = ttk.Treeview(self.cadre2,columns=['A','B','C','D','E','F','G'], show="headings",height=15)
            self.tree2.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
            self.tree2.column("B", width=100,anchor="center",minwidth= 100)
            self.tree2.column("C", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("D", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("E", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("F", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("G", width=200,anchor="center",minwidth= 200 )
            
            self.tree2.heading("A", text="N°")
            self.tree2.heading("B", text="Id_e")
            self.tree2.heading("C", text="Entrepôt")
            self.tree2.heading("D", text="Coût snep entrepôt")
            self.tree2.heading("E", text="Ouvert(1)/Fermé(0)")
            self.tree2.heading("F", text="Coût entrepôt-région")
            self.tree2.heading("G", text="desservant(1)/non desservant(0)")

            vsb2 = ttk.Scrollbar(orient="vertical",command=self.tree2.yview)
            hsb2 = ttk.Scrollbar(orient="horizontal",command=self.tree2.xview)
            self.tree2.configure(yscrollcommand=vsb2.set,xscrollcommand=hsb2.set)
            self.tree2.grid(column=0, row=0, sticky='nsew', in_=self.cadre2)
            vsb2.grid(column=1, row=0, sticky='ns', in_=self.cadre2)
            hsb2.grid(column=0, row=1, sticky='ew', in_=self.cadre2)
            self.cadre2.grid_columnconfigure(0, weight=1)
            self.cadre2.grid_rowconfigure(0, weight=1)

            self.Fermer=Button(self.cadre2,text='Terminer',command=self.quitter,width=15,bg='orange',fg='white')
            self.Fermer.grid(column=0, row=2, sticky='e',in_=self.cadre2)
            self.update_tree(None)
    def quitter(self):
        self.fenetre.destroy()
        main()

    def update_tree(self,event):
        #vider la tree 2
        x = self.tree2.get_children()
        for item in x:
            self.tree2.delete(item)
        #remplissage de la tree2
        self.iid=self.tree1.selection()
        try:
            self.c.execute('''  select * 
                                from entrepot e,desservir d
                                where e.Id_e==d.Id_e and d.Id_r==?;''',(self.dictionnaire[self.iid[0]][0],)) 
            self.L1=self.c.fetchall()
        except Exception as e:
            showwarning('Attention',e)
        else:
            for i in range(len(self.L1)):
                iid1=self.tree2.insert("",i,text=str(i),values=(str(i),self.L1[i][0],self.L1[i][1],self.L1[i][2],int(self.L1[i][3])%2,self.L1[i][6],self.L1[i][7]))
            if len(self.L1)!=0:
                self.tree2.selection_set(iid1)
                
class AfficherEntrepot():
    def __init__(self,root):
        self.fenetre=root
        try:
            self.db=sqlite3.connect('Base_ONEP')
            self.c=self.db.cursor()
            self.c.execute("select * from entrepot;")
            self.L=self.c.fetchall()
            
        except Exception as e:
            showwarning('Attention',e)
        else:
            
            self.cadre3=LabelFrame(root,text='',width=100,height=15,borderwidth=2)
            self.cadre3.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            self.tree1 = ttk.Treeview(self.cadre3,columns=['A','B','C','D','E'], show="headings",height=15)
            
            self.tree1.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
            self.tree1.column("B", width=100,anchor="center",minwidth= 100)
            self.tree1.column("C", width=100,anchor="center",minwidth= 100 )
            self.tree1.column("D", width=100,anchor="center",minwidth= 100 )
            self.tree1.column("E", width=100,anchor="center",minwidth= 100 )
            
            self.tree1.heading("A", text="N°")
            self.tree1.heading("B", text="Id_e")
            self.tree1.heading("C", text="Entrepôt")
            self.tree1.heading("D", text="Coût Snep-Entrepôt")
            self.tree1.heading("E", text="Ouvert(1)/Fermé(0)")
            
            vsb1 = ttk.Scrollbar(orient="vertical",command=self.tree1.yview)
            hsb1 = ttk.Scrollbar(orient="horizontal",command=self.tree1.xview)
            self.tree1.configure(yscrollcommand=vsb1.set,xscrollcommand=hsb1.set)
            self.tree1.grid(column=0, row=0, sticky='nsew', in_=self.cadre3)
            vsb1.grid(column=1, row=0, sticky='ns', in_=self.cadre3)
            hsb1.grid(column=0, row=1, sticky='ew', in_=self.cadre3)
            self.cadre3.grid_columnconfigure(0, weight=1)
            self.cadre3.grid_rowconfigure(0, weight=1)
            self.tree1.bind('<Double-Button-1>', self.update_tree)
            #remplissage de la tree1
            self.dictionnaire={}
            for i in range(len(self.L)):
                self.iid=self.tree1.insert("",i,text=str(i),values=(str(i),self.L[i][0],self.L[i][1],self.L[i][2],int(self.L[i][3])%2))
                self.dictionnaire[self.iid]=[self.L[i][0],self.L[i][1],self.L[i][2],int(self.L[i][3])%2]
            self.tree1.selection_set(self.iid)
            self.label21=Label(self.cadre3,text='Les régions desservies par l\'entrepôt sélectionné sont : ',justify='left')
            self.label21.grid(column=0, row=2,sticky='w', in_=self.cadre3)
            #la tree2
            self.cadre2=LabelFrame(root,text='',width=100,height=15,borderwidth=2)
            self.cadre2.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            
            self.tree2 = ttk.Treeview(self.cadre2,columns=['A','B','C','D','E','F'], show="headings",height=15)
            self.tree2.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
            self.tree2.column("B", width=100,anchor="center",minwidth= 100)
            self.tree2.column("C", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("D", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("E", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("F", width=200,anchor="center",minwidth= 200 )
            
            self.tree2.heading("A", text="N°")
            self.tree2.heading("B", text="Id_r")
            self.tree2.heading("C", text="Région")
            self.tree2.heading("D", text="Demande de la région")
            self.tree2.heading("E", text="Coût Entrepôt-région")
            self.tree2.heading("F", text="desservie(1)/non desservie(0)")
            
            vsb2 = ttk.Scrollbar(orient="vertical",command=self.tree2.yview)
            hsb2 = ttk.Scrollbar(orient="horizontal",command=self.tree2.xview)
            self.tree2.configure(yscrollcommand=vsb2.set,xscrollcommand=hsb2.set)
            self.tree2.grid(column=0, row=0, sticky='nsew', in_=self.cadre2)
            vsb2.grid(column=1, row=0, sticky='ns', in_=self.cadre2)
            hsb2.grid(column=0, row=1, sticky='ew', in_=self.cadre2)
            self.cadre2.grid_columnconfigure(0, weight=1)
            self.cadre2.grid_rowconfigure(0, weight=1)

            self.Fermer=Button(self.cadre2,text='Terminer',command=self.quitter,width=15,bg='orange',fg='white')
            self.Fermer.grid(column=0, row=2, sticky='e',in_=self.cadre2)
            self.update_tree(None)
    def quitter(self):
        self.fenetre.destroy()
        main()

    def update_tree(self,event):
        #vider la tree 2
        x = self.tree2.get_children()
        for item in x:
            self.tree2.delete(item)
        #remplissage de la tree2
        self.iid=self.tree1.selection()
        try:
            self.c.execute('''  select * 
                                from desservir d,region r
                                where d.Id_r==r.Id_r and d.Id_e==?;''',(self.dictionnaire[self.iid[0]][0],)) 
            self.L1=self.c.fetchall()
        except Exception as e:
            showwarning('Attention',e)
        else:
            for i in range(len(self.L1)):
                iid1=self.tree2.insert("",i,text=str(i),values=(str(i),self.L1[i][1],self.L1[i][5],self.L1[i][6],self.L1[i][2],self.L1[i][3]))
            if len(self.L1)!=0:
                self.tree2.selection_set(iid1)


class SaisieDessertes():
    def __init__(self,root):
        self.fenetre=root
        try:
            self.db=sqlite3.connect('Base_ONEP')
            self.c=self.db.cursor()
            self.c.execute("select * from entrepot where ouvert=1;")
            self.L=self.c.fetchall()
            self.c.execute("select * from region ;")
            self.L1=self.c.fetchall()
            
        except Exception as e:
            showwarning('Attention',e)
        else:
            
            self.cadre3=LabelFrame(root,text='',width=100,height=10,borderwidth=2)
            self.cadre3.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            self.label31=Label(self.cadre3,text='Les entrepôts ouverts : ',justify='left')
            self.label31.grid(column=0, row=0, sticky='w', in_=self.cadre3)
            self.tree1 = ttk.Treeview(self.cadre3,columns=['A','B','C','D','E'], show="headings",height=10)
            
            self.tree1.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
            self.tree1.column("B", width=100,anchor="center",minwidth= 100)
            self.tree1.column("C", width=100,anchor="center",minwidth= 100 )
            self.tree1.column("D", width=100,anchor="center",minwidth= 100 )
            self.tree1.column("E", width=100,anchor="center",minwidth= 100 )
            
            self.tree1.heading("A", text="N°")
            self.tree1.heading("B", text="Id_e")
            self.tree1.heading("C", text="Entrepôt")
            self.tree1.heading("D", text="Coût Snep-Entrepôt")
            self.tree1.heading("E", text="Ouvert(1)/Fermé(0)")
            
            vsb1 = ttk.Scrollbar(orient="vertical",command=self.tree1.yview)
            hsb1 = ttk.Scrollbar(orient="horizontal",command=self.tree1.xview)
            self.tree1.configure(yscrollcommand=vsb1.set,xscrollcommand=hsb1.set)
            self.tree1.grid(column=0, row=1, sticky='nsew', in_=self.cadre3)
            vsb1.grid(column=1, row=1, sticky='ns', in_=self.cadre3)
            hsb1.grid(column=0, row=2, sticky='ew', in_=self.cadre3)
            self.cadre3.grid_columnconfigure(0, weight=1)
            self.cadre3.grid_rowconfigure(0, weight=1)
            self.tree1.bind('<Double-Button-1>', self.update_tree)
            #remplissage de la tree1
            self.dictionnaire={}
            for i in range(len(self.L)):
                self.iid=self.tree1.insert("",i,text=str(i),values=(str(i),self.L[i][0],self.L[i][1],self.L[i][2],int(self.L[i][3])%2))
                self.dictionnaire[self.iid]=[self.L[i][0],self.L[i][1],self.L[i][2],int(self.L[i][3])%2]
            self.tree1.selection_set(self.iid)
            
            #la tree2
            self.cadre2=LabelFrame(root,text='',width=100,height=10,borderwidth=2)
            self.cadre2.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            self.cadre21=LabelFrame(self.cadre2,text='',width=100,height=10,borderwidth=2)
            self.cadre21.pack(side=LEFT,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            
            self.label211=Label(self.cadre21,text='Les régions enregistrées sont : ',justify='left')
            self.label211.grid(column=0, row=0,sticky='w', in_=self.cadre21)
            self.tree2 = ttk.Treeview(self.cadre21,columns=['A','B','C','D'], show="headings",height=10)
            self.tree2.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
            self.tree2.column("B", width=100,anchor="center",minwidth= 100)
            self.tree2.column("C", width=100,anchor="center",minwidth= 100 )
            self.tree2.column("D", width=200,anchor="center",minwidth= 200 )
            
            self.tree2.heading("A", text="N°")
            self.tree2.heading("B", text="Id_r")
            self.tree2.heading("C", text="Région")
            self.tree2.heading("D", text="Demande de la région")
            
            vsb2 = ttk.Scrollbar(orient="vertical",command=self.tree2.yview)
            hsb2 = ttk.Scrollbar(orient="horizontal",command=self.tree2.xview)
            self.tree2.configure(yscrollcommand=vsb2.set,xscrollcommand=hsb2.set)
            self.tree2.grid(column=0, row=1, sticky='nsew', in_=self.cadre21)
            vsb2.grid(column=1, row=1, sticky='ns', in_=self.cadre21)
            hsb2.grid(column=0, row=2, sticky='ew', in_=self.cadre21)
            self.cadre21.grid_columnconfigure(0, weight=1)
            self.cadre21.grid_rowconfigure(0, weight=1)
            self.tree2.bind('<Double-Button-1>', self.update_tree1)
            #remplissage de la tree2
            self.dictionnaire1={}
            for i in range(len(self.L1)):
                self.iid1=self.tree2.insert("",i,text=str(i),values=(str(i),self.L1[i][0],self.L1[i][1],self.L1[i][2]))
                self.dictionnaire1[self.iid1]=[self.L1[i][0],self.L1[i][1],self.L1[i][2]]
            self.tree2.selection_set(self.iid1)
            #la tree4 les dessertes déjà enregistrées
            self.label212=Label(self.cadre21,text='Les dessertes déjà enregistrées sont : ',justify='left')
            self.label212.grid(column=0, row=3,sticky='w', in_=self.cadre21)
            self.tree4 = ttk.Treeview(self.cadre21,columns=['A','B','C','D'], show="headings",height=5)
            self.tree4.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
            self.tree4.column("B", width=100,anchor="center",minwidth= 100)
            self.tree4.column("C", width=100,anchor="center",minwidth= 100 )
            self.tree4.column("D", width=200,anchor="center",minwidth= 200 )
            
            self.tree4.heading("A", text="Entrepôt")
            self.tree4.heading("B", text="Région")
            self.tree4.heading("C", text="C e_r")
            self.tree4.heading("D", text="Y e_r")
            
            vsb4 = ttk.Scrollbar(orient="vertical",command=self.tree4.yview)
            hsb4 = ttk.Scrollbar(orient="horizontal",command=self.tree4.xview)
            self.tree4.configure(yscrollcommand=vsb4.set,xscrollcommand=hsb4.set)
            self.tree4.grid(column=0, row=4, sticky='nsew', in_=self.cadre21)
            vsb4.grid(column=1, row=4, sticky='ns', in_=self.cadre21)
            hsb4.grid(column=0, row=5, sticky='ew', in_=self.cadre21)
            self.cadre21.grid_columnconfigure(0, weight=1)
            self.cadre21.grid_rowconfigure(0, weight=1)
            self.tree4.bind('<Double-Button-1>', self.update_tree4)

            #saisie de C e_r, Y e_r
            self.cadre22=LabelFrame(self.cadre2,text='',width=100,height=10,borderwidth=2)
            self.cadre22.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            
            self.label22=Label(self.cadre22,text='Coût Entrepôt - région ',justify='left')
            self.label22.grid(column=0, row=3, sticky='w', in_=self.cadre22)
            self.saisie21=Entry(self.cadre22,justify='left')
            self.saisie21.grid(column=1, row=3, sticky='w', in_=self.cadre22)
            
            self.label23=Label(self.cadre22,text='L\'entrepôt dessert la région : ',justify='left')
            self.label23.grid(column=0, row=4, sticky='w', in_=self.cadre22)
            self.valueDesserte=StringVar()
            self.valueDesserte.set('1')
            self.bouton1=Radiobutton(self.cadre22,text='Oui',variable=self.valueDesserte,value='1')
            self.bouton1.grid(column=1, row=4, sticky='w', in_=self.cadre22)
            self.bouton2=Radiobutton(self.cadre22,text='Non',variable=self.valueDesserte,value='2')
            self.bouton2.grid(column=1, row=5, sticky='w', in_=self.cadre22)

            self.Valider=Button(self.cadre22,text='Valider',command=self.valider,width=20,bg='orange',fg='white')
            self.Valider.grid(column=2, row=6, sticky='e',in_=self.cadre22)

            self.Annuler=Button(self.cadre22,text='Annuler',command=self.annuler,width=15,bg='orange',fg='white')
            self.Annuler.grid(column=3, row=6, sticky='e',in_=self.cadre22)
            
            #la tree3
            self.cadre23=LabelFrame(self.cadre2,text='',width=100,height=10,borderwidth=2)
            self.cadre23.pack(side=BOTTOM,anchor='nw',expand=1,padx=10,pady=5,fill=X)
            
            self.label21=Label(self.cadre23,text='Les dessertes enregistrées récemment sont : ',justify='left')
            self.label21.grid(column=0, row=0,sticky='w', in_=self.cadre23)
            self.tree3 = ttk.Treeview(self.cadre23,columns=['A','B','C','D','E','F','G','H','I','J'], show="headings",height=10)
            self.tree3.column("A", width=100,anchor="w", stretch = True, minwidth= 100)
            self.tree3.column("B", width=100,anchor="center",minwidth= 100)
            self.tree3.column("C", width=100,anchor="center",minwidth= 100 )
            self.tree3.column("D", width=100,anchor="center",minwidth= 100 )
            self.tree3.column("E", width=100,anchor="center",minwidth= 100 )
            self.tree3.column("F", width=100,anchor="center",minwidth= 100 )
            self.tree3.column("G", width=100,anchor="center",minwidth= 100 )
            self.tree3.column("H", width=100,anchor="center",minwidth= 100 )
            self.tree3.column("I", width=100,anchor="center",minwidth= 100 )
            self.tree3.column("J", width=200,anchor="center",minwidth= 200 )
            
            self.tree3.heading("A", text="N°")
            self.tree3.heading("B", text="Id_e")
            self.tree3.heading("C", text="Entrepôt")
            self.tree3.heading("D", text="Cs_e")
            self.tree3.heading("E", text="Etat")
            self.tree3.heading("F", text="Id_r")
            self.tree3.heading("G", text="Région")
            self.tree3.heading("H", text="Demande région")
            self.tree3.heading("I", text="C e_r")
            self.tree3.heading("J", text="Desservie O(1)/N(0)")
            
            
            vsb3 = ttk.Scrollbar(orient="vertical",command=self.tree3.yview)
            hsb3 = ttk.Scrollbar(orient="horizontal",command=self.tree3.xview)
            self.tree3.configure(yscrollcommand=vsb3.set,xscrollcommand=hsb3.set)
            self.tree3.grid(column=0, row=1, sticky='nsew', in_=self.cadre23)
            vsb3.grid(column=1, row=1, sticky='ns', in_=self.cadre23)
            hsb3.grid(column=0, row=2, sticky='ew', in_=self.cadre23)
            
            self.cadre23.grid_columnconfigure(0, weight=1)
            self.cadre23.grid_rowconfigure(0, weight=1)
            self.tree3.bind('<Double-Button-1>', self.update_tree3)
            self.Fermer=Button(self.cadre23,text='Terminer',command=self.fermer,width=15,bg='orange',fg='white')
            self.Fermer.grid(column=0, row=3, sticky='e',in_=self.cadre23)
            
            self.update_tree(None)
            self.k=0
            self.modifier=0
            self.dictionnaire2={}

    def fermer(self):
        self.fenetre.destroy()
        main()        
    def annuler(self):
        self.saisie21.delete(0, END)
        self.valueDesserte.set('1')
    def valider(self):
        self.iid=self.tree1.selection()
        self.iid1=self.tree2.selection()
        if self.modifier==0:
            if self.saisie21.get()!='':
                reponse=askquestion('Confirmer la desserte','Voulez vous enregistrer la desserte entre l\'entrepôt '+self.dictionnaire[self.iid[0]][1]+' et la région '+self.dictionnaire1[self.iid1[0]][1]+' ?')
                if reponse=='yes':
                    #enregistrement dans la base
                    try:
                        self.c.execute("insert into desservir values(?,?,?,?);",(self.dictionnaire[self.iid[0]][0],self.dictionnaire1[self.iid1[0]][0],self.saisie21.get(),int(self.valueDesserte.get())%2))
                    except Exception as e:
                        showwarning('Attention',e)
                    else:
                        self.db.commit()
                        #mise à jour de la tree3
                        self.iid2=self.tree3.insert("",self.k,text=str(self.k),values=(str(self.k),self.dictionnaire[self.iid[0]][0],self.dictionnaire[self.iid[0]][1],self.dictionnaire[self.iid[0]][2],self.dictionnaire[self.iid[0]][3],self.dictionnaire1[self.iid1[0]][0],self.dictionnaire1[self.iid1[0]][1],self.dictionnaire1[self.iid1[0]][2],self.saisie21.get(),int(self.valueDesserte.get())%2))
                        self.k+=1
                        self.dictionnaire2[self.iid2]=[self.iid,self.iid1,self.dictionnaire[self.iid[0]][0],self.dictionnaire[self.iid[0]][1],self.dictionnaire[self.iid[0]][2],self.dictionnaire[self.iid[0]][3],self.dictionnaire1[self.iid1[0]][0],self.dictionnaire1[self.iid1[0]][1],self.dictionnaire1[self.iid1[0]][2],self.saisie21.get(),int(self.valueDesserte.get())%2]
                self.annuler()
            else:
                showwarning('Attention','information manquante')
        else:
            if self.saisie21.get()!='':
                reponse=askquestion('Confirmer la desserte','Voulez vous enregistrer les modifications de la desserte entre l\'entrepôt '+self.dictionnaire[self.iid[0]][1]+' et la région '+self.dictionnaire1[self.iid1[0]][1]+' ?')
                if reponse=='yes':
                    #enregistrement dans la base
                    try:
                        self.c.execute("update desservir set Cij=?,Yij=? where Id_e==? and Id_r==?;",(self.saisie21.get(),int(self.valueDesserte.get())%2),self.dictionnaire[self.iid[0]][0],self.dictionnaire1[self.iid1[0]][0])
                    except Exception as e:
                        showwarning('Attention',e)
                    else:
                        self.db.commit()
                        #mise à jour de la tree3
                        self.tree3.delete(self.iid2)
                        self.iid2=self.tree3.insert("",self.k,text=str(self.k),values=(str(self.k),self.dictionnaire[self.iid[0]][0],self.dictionnaire[self.iid[0]][1],self.dictionnaire[self.iid[0]][2],self.dictionnaire[self.iid[0]][3],self.dictionnaire1[self.iid1[0]][0],self.dictionnaire1[self.iid1[0]][1],self.dictionnaire1[self.iid1[0]][2],self.saisie21.get(),int(self.valueDesserte.get())%2))
                        self.k+=1
                        self.dictionnaire2[self.iid2]=[self.iid,self.iid1,self.dictionnaire[self.iid[0]][0],self.dictionnaire[self.iid[0]][1],self.dictionnaire[self.iid[0]][2],self.dictionnaire[self.iid[0]][3],self.dictionnaire1[self.iid1[0]][0],self.dictionnaire1[self.iid1[0]][1],self.dictionnaire1[self.iid1[0]][2],self.saisie21.get(),int(self.valueDesserte.get())%2]
                    
                self.annuler()
                self.modifier=0
                self.Valider['text']='Valider'
            else:
                showwarning('Attention','information manquante')
        self.update_tree(None)
            
        
    def update_tree(self,event):
        #vider la tree4
        x=self.tree4.get_children()
        for e in x:
            self.tree4.delete(e)
        #remplissage de la tree4
        try:
            self.iid=self.tree1.selection()
            self.c.execute("select * from desservir d join region r on d.Id_r=r.Id_r where d.Id_e==?",(self.dictionnaire[self.iid[0]][0],))
            self.L2=self.c.fetchall()
        except Exception as e:
            showwarning('Attention',e)
        else:
            for i in range(len(self.L2)):
                iid2=self.tree4.insert("",i,text=str(i),values=(self.dictionnaire[self.iid[0]][1],self.L2[i][5],self.L2[i][2],self.L2[i][3]))
            if len(self.L2)!=0:self.tree4.selection_set(iid2)
    def update_tree1(self,event):
        pass
    def update_tree3(self,event):
        self.iid2=self.tree3.selection()
        if len(self.iid2)!=0:
            self.tree1.selection_set(self.dictionnaire2[self.iid2[0]][0])
            self.tree2.selection_set(self.dictionnaire2[self.iid2[0]][1])
            self.saisie21.delete(0, END)
            self.saisie21.insert(0,self.dictionnaire2[self.iid2[0]][-2])
            if self.dictionnaire2[self.iid2[0]][-1]==0:
                self.valueDesserte.set('2')
            else:
                self.valueDesserte.set('1')
            self.Valider['text']='Modifier la desserte'
            self.modifier=1
    def update_tree4(self,event):
        pass
class Calculs():
    def __init__(self,root):
        self.fenetre=root
        self.cadre3=LabelFrame(root,text='',width=100,height=10,borderwidth=2)
        self.cadre3.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        self.label31=Label(self.cadre3,text='Les entrepôts ouverts : ',justify='left')
        self.label31.grid(column=0, row=0, sticky='w', in_=self.cadre3)
        self.tree1 = ttk.Treeview(self.cadre3,columns=['B','C','D','E'], show="headings",height=10)
        
        self.tree1.column("B", width=100,anchor="w", stretch = True, minwidth= 100)
        self.tree1.column("C", width=100,anchor="center",minwidth= 100)
        self.tree1.column("D", width=100,anchor="center",minwidth= 100 )
        self.tree1.column("E", width=100,anchor="center",minwidth= 100 )

        

        self.tree1.heading("B", text="Id_e")
        self.tree1.heading("C", text="Entrepôt")
        self.tree1.heading("D", text="Coût Snep-Entrepôt")
        self.tree1.heading("E", text="Ouvert(1)/Fermé(0)")
        
        vsb1 = ttk.Scrollbar(orient="vertical",command=self.tree1.yview)
        hsb1 = ttk.Scrollbar(orient="horizontal",command=self.tree1.xview)
        self.tree1.configure(yscrollcommand=vsb1.set,xscrollcommand=hsb1.set)
        self.tree1.grid(column=0, row=1, sticky='nsew', in_=self.cadre3)
        vsb1.grid(column=1, row=1, sticky='ns', in_=self.cadre3)
        hsb1.grid(column=0, row=2, sticky='ew', in_=self.cadre3)
        self.cadre3.grid_columnconfigure(0, weight=1)
        self.cadre3.grid_rowconfigure(0, weight=1)
        
        self.label32=Label(self.cadre3,text='Valeur de la fonction objective : ',justify='left')
        self.label32.grid(column=0, row=3,sticky='w', in_=self.cadre3)

        #la tree2
        self.cadre2=LabelFrame(root,text='',width=100,height=10,borderwidth=2)
        self.cadre2.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        self.cadre21=LabelFrame(self.cadre2,text='',width=100,height=10,borderwidth=2)
        self.cadre21.pack(side=LEFT,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        
        self.label211=Label(self.cadre21,text='Les dessertes minimisant la fonction objective : ',justify='left')
        self.label211.grid(column=0, row=0,sticky='w', in_=self.cadre21)
        self.tree2 = ttk.Treeview(self.cadre21,columns=['B','C','D','E','F','G','H'], show="headings",height=10)
        self.tree2.column("B", width=100,anchor="w", stretch = True, minwidth= 100)
        self.tree2.column("C", width=100,anchor="center",minwidth= 100)
        self.tree2.column("D", width=100,anchor="center",minwidth= 100 )
        self.tree2.column("E", width=100,anchor="center",minwidth= 100 )
        self.tree2.column("F", width=100,anchor="center",minwidth= 100 )
        self.tree2.column("G", width=100,anchor="center",minwidth= 100 )
        self.tree2.column("H", width=100,anchor="center",minwidth= 100 )

        self.tree2.heading("B", text="Id_r")
        self.tree2.heading("C", text="Région")
        self.tree2.heading("D", text="Demande de la région")
        self.tree2.heading("E", text="Entrepôt")
        self.tree2.heading("F", text="C s_e")
        self.tree2.heading("G", text="Etat")
        self.tree2.heading("H", text="C e_r")
        
        
        vsb2 = ttk.Scrollbar(orient="vertical",command=self.tree2.yview)
        hsb2 = ttk.Scrollbar(orient="horizontal",command=self.tree2.xview)
        self.tree2.configure(yscrollcommand=vsb2.set,xscrollcommand=hsb2.set)
        self.tree2.grid(column=0, row=1, sticky='nsew', in_=self.cadre21)
        vsb2.grid(column=1, row=1, sticky='ns', in_=self.cadre21)
        hsb2.grid(column=0, row=2, sticky='ew', in_=self.cadre21)
        self.cadre21.grid_columnconfigure(0, weight=1)
        self.cadre21.grid_rowconfigure(0, weight=1)
        self.Valider=Button(self.cadre21,text='Enregistrer les dessertes',command=self.enregistrer,width=25,bg='orange',fg='white')
        self.Valider.grid(column=0, row=3, sticky='e',in_=self.cadre21)
        self.progressBar = ttk.Progressbar(self.cadre21, orient="horizontal", length=300,mode="determinate")
        self.progressBar.grid_forget()
        
        #la tree3
        self.cadre23=LabelFrame(self.cadre2,text='',width=100,height=10,borderwidth=2)
        self.cadre23.pack(side=BOTTOM,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        
        self.label21=Label(self.cadre23,text='Modifier les états des entrepôts : ',justify='left')
        self.label21.grid(column=0, row=0,sticky='w', in_=self.cadre23)
        self.tree3 = ttk.Treeview(self.cadre23,columns=['B','C','D','E'], show="headings",height=10)
        self.tree3.column("B", width=100,anchor="w", stretch = True, minwidth= 100)
        self.tree3.column("C", width=100,anchor="center",minwidth= 100)
        self.tree3.column("D", width=100,anchor="center",minwidth= 100 )
        self.tree3.column("E", width=100,anchor="center",minwidth= 100 )
        
        self.tree3.heading("B", text="Id_e")
        self.tree3.heading("C", text="Entrepôt")
        self.tree3.heading("D", text="Cs_e")
        self.tree3.heading("E", text="Etat")
        
        vsb3 = ttk.Scrollbar(orient="vertical",command=self.tree3.yview)
        hsb3 = ttk.Scrollbar(orient="horizontal",command=self.tree3.xview)
        self.tree3.configure(yscrollcommand=vsb3.set,xscrollcommand=hsb3.set)
        self.tree3.grid(column=0, row=1, sticky='nsew', in_=self.cadre23)
        vsb3.grid(column=1, row=1, sticky='ns', in_=self.cadre23)
        hsb3.grid(column=0, row=2, sticky='ew', in_=self.cadre23)
        
        self.cadre23.grid_columnconfigure(0, weight=1)
        self.cadre23.grid_rowconfigure(0, weight=1)
        self.tree3.bind('<Double-Button-1>', self.update_tree3)
        self.rel=Button(self.cadre23,text='Relancer les calculs',command=self.relancer_calcul,width=20,bg='orange',fg='white')
        self.rel.grid(column=0, row=3, sticky='e',in_=self.cadre23)
        self.Fermer=Button(self.cadre23,text='Terminer',command=self.fermer,width=15,bg='orange',fg='white')
        self.Fermer.grid(column=0, row=4, sticky='e',in_=self.cadre23)
        self.relancer_calcul()

    def enregistrer(self):
        self.progressBar.grid(column = 0, row = 4,in_=self.cadre21)
        self.progressBar['maximum'] = len(self.res['x'])
    
        for i in range(len(self.res['x'])):
            e=i//self.nbR
            r=i%self.nbR
            try:
                self.c.execute('update desservir set Yij=? where Id_e==? and Id_r==?',(self.res['x'][i],self.L[e][0],self.L1[r][0]))
            except Exception as e:
                showwarning('Attention',e)
            else:
                self.db.commit()
                time.sleep(0.05)
                self.progressBar["value"] = i
                self.progressBar.update()
                self.progressBar["value"] = 0
        self.progressBar.grid_forget()
                    
            
    def update_tree3(self,event):
        self.iid2=self.tree3.selection()
        self.etat='ouvert'
        if self.dictionnaire2[self.iid2[0]][3]==0:
            self.etat='fermé'
        reponse=askquestion('Changement d\'état :','L\'entrepôt '+self.dictionnaire2[self.iid2[0]][1]+' est '+self.etat+' voulez vous  changer son état?')
        if reponse=='yes':
            if self.etat=='ouvert':
                try:
                    self.c.execute('update entrepot set ouvert=0 where Id_e==?',(self.dictionnaire2[self.iid2[0]][0],))
                except Exception as e:
                    showwarning('Attention',e)
                else:
                    self.db.commit()
                    
            else:
                try:
                    self.c.execute('update entrepot set ouvert=1 where Id_e==?',(self.dictionnaire2[self.iid2[0]][0],))
                except Exception as e:
                    showwarning('Attention',e)
                else:
                    self.db.commit()
            self.c.execute("select * from entrepot;")
            self.L=self.c.fetchall()
            x=self.tree3.get_children()
            for e in x:
                self.tree3.delete(e)
            self.dictionnaire2={}
            for i in range(len(self.L)):
                self.iid2=self.tree3.insert("",i,text=str(i),values=(self.L[i][0],self.L[i][1],self.L[i][2],int(self.L[i][3])%2))
                self.dictionnaire2[self.iid2]=[self.L[i][0],self.L[i][1],self.L[i][2],int(self.L[i][3])%2]
                self.tree3.selection_set(self.iid2)
                    

    def fermer(self):
        self.fenetre.destroy()
        main()
    def relancer_calcul(self):
        #vider les trees
        x=self.tree1.get_children()
        for e in x:
            self.tree1.delete(e)
        x=self.tree2.get_children()
        for e in x:
            self.tree2.delete(e)
        x=self.tree3.get_children()
        for e in x:
            self.tree3.delete(e)
        self.calcul()
        #remplissage de la tree1
        #remplissage de la tree1
        for i in range(len(self.L)):
            if int(self.L[i][3])%2==1:
                self.iid=self.tree1.insert("",i,text=str(i),values=(self.L[i][0],self.L[i][1],self.L[i][2],int(self.L[i][3])%2))
                self.tree1.selection_set(self.iid)
        self.label32['text']='Valeur de la fonction objective : '+str(self.Z)
        #remplissage de la tree2
        #remplissage de la tree2
        for i in range(self.k):
            self.iid1=self.tree2.insert("",i,text=str(i),values=(self.dictionnaire1[i][0],self.dictionnaire1[i][1],self.dictionnaire1[i][2],self.dictionnaire1[i][3],self.dictionnaire1[i][4],self.dictionnaire1[i][5],self.dictionnaire1[i][6]))
            self.tree2.selection_set(self.iid1)
        #remplissage de la tree3
        self.dictionnaire2={}
        for i in range(len(self.L)):
            self.iid2=self.tree3.insert("",i,text=str(i),values=(self.L[i][0],self.L[i][1],self.L[i][2],int(self.L[i][3])%2))
            self.dictionnaire2[self.iid2]=[self.L[i][0],self.L[i][1],self.L[i][2],int(self.L[i][3])%2]
            self.tree3.selection_set(self.iid2)
        
        
    def calcul(self):
        try:
            self.db=sqlite3.connect('Base_ONEP')
            self.c=self.db.cursor()
            self.c.execute("select * from entrepot;")
            self.L=self.c.fetchall()
            self.c.execute("select * from region ;")
            self.L1=self.c.fetchall()
            self.c.execute("select * from desservir ;")
            self.L2=self.c.fetchall()
            
        except Exception as e:
            showwarning('Attention',e)
        else:
            self.nbE=len(self.L)
            self.nbR=len(self.L1)
            self.Csi={self.L[i][0]:self.L[i][2] for i in range(len(self.L))}
            self.Dj={self.L1[i][0]:self.L1[i][2] for i in range(len(self.L1))}
            self.Cij={self.L[i][0]:{} for i in range(len(self.L))}
            for key in self.Cij.keys():
                for i in range(len(self.L2)):
                    if key==self.L2[i][0]:
                        self.Cij[key][self.L2[i][1]]=self.L2[i][2]
            self.Xi=[self.L[i][3] for i in range(len(self.L))]
            print(self.Xi)
            self.C=[0]*(self.nbE*self.nbR)
            for i in range(self.nbE):
                for j in range(self.nbR):
                    self.C[i*self.nbR+j]=self.Csi[self.L[i][0]]*self.Dj[self.L1[j][0]]+self.Cij[self.L[i][0]][self.L1[j][0]]*self.Dj[self.L1[j][0]]
            self.A_ub=np.eye(self.nbE*self.nbR)
            self.B_ub=[0]*(self.nbE*self.nbR)
            for k in range(self.nbE*self.nbR):
                i=k//self.nbR
                self.B_ub[k]=self.Xi[i]
            self.A_eq=np.zeros((self.nbR,self.nbE*self.nbR))
            for j in range(self.nbR):
                for i in range(self.nbE):
                    self.A_eq[j][i*self.nbR+j]=1
            self.B_eq=[1]*self.nbR
            self.bound=[(0,1) for i in range(self.nbE*self.nbR)]
            self.res=linprog(self.C, A_ub=self.A_ub, b_ub=self.B_ub, A_eq=self.A_eq, b_eq=self.B_eq, bounds=self.bound, method='simplex', options=None)
            self.dictionnaire1={}
            self.Z=0
            self.k=0
            for i in range(len(self.res['x'])):
                if self.res['x'][i]==1:
                    e=i//self.nbR
                    r=i%self.nbR
                    self.dictionnaire1[self.k]=[self.L1[r][0],self.L1[r][1],self.L1[r][2],self.L[e][1],self.L[e][2],self.L[e][3],self.Cij[self.L[e][0]][self.L1[r][0]]]
                    self.Z+=self.C[i]
                    self.k+=1
class Optimisation_entrepot():
    def __init__(self,root):
        self.fenetre=root
        self.cadre3=LabelFrame(root,text='',width=100,height=10,borderwidth=2)
        self.cadre3.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        self.label31=Label(self.cadre3,text='Minimisation de la fonction objective en fonction du nombre d\'entrepôts ouverts ',justify='left')
        self.label31.grid(column=0, row=0, sticky='w', in_=self.cadre3)
        
        self.cadre32=LabelFrame(self.cadre3,text='',height=7,width=300,borderwidth=0,bg='gray92',padx=5)
        self.cadre32.grid(column=0, row=1,  in_=self.cadre3)
        
        self.cadre31=LabelFrame(self.cadre3,text='',height=7,width=300,borderwidth=0,bg='gray92',padx=5)
        self.cadre31.grid(column=1, row=1,  in_=self.cadre3)
        self.label32=Label(self.cadre31,text=' ',justify='left',bg='gray92')
        self.label32.grid(column=0, row=0, sticky='ew', in_=self.cadre31)
        self.tree1 = ttk.Treeview(self.cadre31,columns=['B','C'], show="headings",height=10)
        self.tree1.column("B", width=200,anchor="w", stretch = True, minwidth= 100)
        self.tree1.column("C", width=200,anchor="center",minwidth= 100)
        self.tree1.heading("B", text="Nombre d'entrepôts ouverts")
        self.tree1.heading("C", text="Valeur de la fonction objective")
        vsb1 = ttk.Scrollbar(orient="vertical",command=self.tree1.yview)
        hsb1 = ttk.Scrollbar(orient="horizontal",command=self.tree1.xview)
        self.tree1.configure(yscrollcommand=vsb1.set,xscrollcommand=hsb1.set)
        self.tree1.grid(column=0, row=1, sticky='nsew', in_=self.cadre31)
        vsb1.grid(column=1, row=1, sticky='ns', in_=self.cadre31)
        hsb1.grid(column=0, row=2, sticky='ew', in_=self.cadre31)
        self.cadre3.grid_columnconfigure(0, weight=1)
        self.cadre3.grid_rowconfigure(0, weight=1)
        self.tree1.bind('<Double-Button-1>', self.update_tree)
        
        #la tree2
        self.cadre2=LabelFrame(root,text='',width=100,height=10,borderwidth=2)
        self.cadre2.pack(side=TOP,anchor='nw',expand=1,padx=10,pady=5,fill=X)
        self.cadre21=LabelFrame(self.cadre2,text='',width=300,height=10,borderwidth=2)
        self.cadre21.grid(column=0, row=0,  in_=self.cadre2)
        
        self.label211=Label(self.cadre21,text='Les dessertes minimisant la fonction objective : ',justify='left')
        self.label211.grid(column=0, row=0,sticky='w', in_=self.cadre21)
        self.tree2 = ttk.Treeview(self.cadre21,columns=['B','C','D','E','F','G','H'], show="headings",height=10)
        self.tree2.column("B", width=100,anchor="w", stretch = True, minwidth= 100)
        self.tree2.column("C", width=200,anchor="center",minwidth= 100)
        self.tree2.column("D", width=200,anchor="center",minwidth= 100 )
        self.tree2.column("E", width=200,anchor="center",minwidth= 100 )
        self.tree2.column("F", width=100,anchor="center",minwidth= 100 )
        self.tree2.column("G", width=100,anchor="center",minwidth= 100 )
        self.tree2.column("H", width=100,anchor="center",minwidth= 100 )

        self.tree2.heading("B", text="Id_r")
        self.tree2.heading("C", text="Région")
        self.tree2.heading("D", text="Demande de la région")
        self.tree2.heading("E", text="Entrepôt")
        self.tree2.heading("F", text="C s_e")
        self.tree2.heading("G", text="Etat")
        self.tree2.heading("H", text="C e_r")

        vsb2 = ttk.Scrollbar(orient="vertical",command=self.tree2.yview)
        hsb2 = ttk.Scrollbar(orient="horizontal",command=self.tree2.xview)
        self.tree2.configure(yscrollcommand=vsb2.set,xscrollcommand=hsb2.set)
        self.tree2.grid(column=0, row=1, sticky='nsew', in_=self.cadre21)
        vsb2.grid(column=1, row=1, sticky='ns', in_=self.cadre21)
        hsb2.grid(column=0, row=2, sticky='ew', in_=self.cadre21)
        self.cadre2.grid_columnconfigure(0, weight=1)
        self.cadre2.grid_rowconfigure(0, weight=1)
        
        self.Fermer=Button(self.cadre2,text='Terminer',command=self.fermer,width=15,bg='orange',fg='white')
        self.Fermer.grid(column=0, row=1, sticky='e',in_=self.cadre2)
        self.calcul1()
    def fermer(self):
        self.fenetre.destroy()
        main()
    def update_tree(self,event):
        #vider la tree2
        x=self.tree2.get_children()
        for e in x:
            self.tree2.delete(e)
        #remplissage de la tree2
        self.iid=self.tree1.selection()
        for e in self.list_iid_tree1:
            if e[0]==self.iid[0]:
                indice=e[1]
        dictionnaire1=self.tableau_sol[indice][1]
        k=len(dictionnaire1.keys())
        for i in range(k):
            self.iid1=self.tree2.insert("",i,text=str(i),values=(dictionnaire1[i][0],dictionnaire1[i][1],dictionnaire1[i][2],dictionnaire1[i][3],dictionnaire1[i][4],dictionnaire1[i][5],dictionnaire1[i][6]))
            
        
    def binaire(self,i):
        rep=[]
        while i!=0:
            rep.insert(0,i%2)
            i=i//2
        return([0]*(self.nbE-len(rep))+rep)
    def calcul1(self):
        try:
            self.db=sqlite3.connect('Base_ONEP')
            self.c=self.db.cursor()
            self.c.execute("select * from entrepot;")
            self.L=self.c.fetchall()
            self.c.execute("select * from region ;")
            self.L1=self.c.fetchall()
            self.c.execute("select * from desservir ;")
            self.L2=self.c.fetchall()
            
        except Exception as e:
            showwarning('Attention',e)
        else:
            self.nbE=len(self.L)
            self.tableau_f_o=[np.inf]*self.nbE
            self.tableau_sol=[0]*self.nbE
            self.nbR=len(self.L1)
            self.Csi={self.L[i][0]:self.L[i][2] for i in range(len(self.L))}
            self.Dj={self.L1[i][0]:self.L1[i][2] for i in range(len(self.L1))}
            self.Cij={self.L[i][0]:{} for i in range(len(self.L))}
            for key in self.Cij.keys():
                for i in range(len(self.L2)):
                    if key==self.L2[i][0]:
                        self.Cij[key][self.L2[i][1]]=self.L2[i][2]
            self.C=[0]*(self.nbE*self.nbR)
            for i in range(self.nbE):
                for j in range(self.nbR):
                    self.C[i*self.nbR+j]=self.Csi[self.L[i][0]]*self.Dj[self.L1[j][0]]+self.Cij[self.L[i][0]][self.L1[j][0]]*self.Dj[self.L1[j][0]]
            self.A_ub=np.eye(self.nbE*self.nbR)
            self.A_eq=np.zeros((self.nbR,self.nbE*self.nbR))
            for j in range(self.nbR):
                for i in range(self.nbE):
                    self.A_eq[j][i*self.nbR+j]=1
            self.B_eq=[1]*self.nbR
            self.bound=[(0,1) for i in range(self.nbE*self.nbR)]
            for jj in range(2**self.nbE):
                self.Xi=self.binaire(jj)
                self.B_ub=[0]*(self.nbE*self.nbR)
                for k in range(self.nbE*self.nbR):
                    i=k//self.nbR
                    self.B_ub[k]=self.Xi[i]
                self.res=linprog(self.C, A_ub=self.A_ub, b_ub=self.B_ub, A_eq=self.A_eq, b_eq=self.B_eq, bounds=self.bound, method='simplex', options=None)
                self.dictionnaire1={}
                self.Z=0
                self.k=0
                try:
                    len(self.res['x'])
                except:
                    continue
                else:
                    for i in range(len(self.res['x'])):
                        if self.res['x'][i]==1:
                            e=i//self.nbR
                            r=i%self.nbR
                            self.dictionnaire1[self.k]=[self.L1[r][0],self.L1[r][1],self.L1[r][2],self.L[e][1],self.L[e][2],self.L[e][3],self.Cij[self.L[e][0]][self.L1[r][0]]]
                            self.Z+=self.C[i]
                            self.k+=1
                    indice=self.Xi.count(1)
                    if self.Z<self.tableau_f_o[indice-1]:
                        self.tableau_f_o[indice-1]=self.Z
                        self.tableau_sol[indice-1]=(self.Xi[:],self.dictionnaire1.copy())
        
            fig1 = Figure(figsize=(8,3), dpi=96)
            bx = fig1.add_subplot(111)
            bx.plot([i+1 for i in range(self.nbE)],self.tableau_f_o,'ko',label='minimum de la fonction objective')
            bx.xaxis.set_tick_params(color = 'black', labelsize = 8, pad = 1,
                            labelcolor = 'black')
            bx.yaxis.set_tick_params(direction = 'in', length = 10, width = 1,
                            color = 'black', labelsize = 8, pad = 1,
                            labelcolor = 'black', left = True,right=False)
            bx.legend(fontsize=6,loc='best')
            graph = FigureCanvasTkAgg(fig1, master=self.cadre32)
            canvas = graph.get_tk_widget()
            canvas.grid(row=0, column=0)
            indice_min=0
            for i in range(len(self.tableau_f_o)):
                if self.tableau_f_o[i]<self.tableau_f_o[indice_min]:
                    indice_min=i
            self.label32.config(text="Nombre d'entrepôt minimal à ouvrir :"+str(indice_min+1))
            #vider les trees
            x=self.tree1.get_children()
            for e in x:
                self.tree1.delete(e)
            #remplissage de la tree1
            self.list_iid_tree1=[]
            for i in range(len(self.tableau_f_o)):
                self.iid=self.tree1.insert("",i,values=(i+1,self.tableau_f_o[i]))
                self.list_iid_tree1.append((self.iid,i))
            
            self.tree1.selection_set(self.iid)
            self.update_tree(None)
            
                
            
                
            

        
        
        
        
            

        
            

        
        
                
        
        
        
        
        



import os

def main():
    master=Tk()
    master.title('Optimisation du coût de transport du chlore ------------ ONEP Errachidia')
    h=master.winfo_screenheight()
    w=master.winfo_screenwidth()
    master.geometry(str(w//2)+'x'+str(h//3)+'+'+str(w//4)+'+'+str(h//3))

    app=Fenetre(master)
    master.mainloop()
main()