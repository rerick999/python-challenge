# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 17:27:12 2023

@author: roberterick
"""
import csv

#this always worked before
# IMPORTPATH=r'.\resources\budget_data.csv'
# EXPORTPATH=r'.\analysis\analysis.txt'

#i adjusted things.  hopefully this works.  i think the 
#directory structure is to spec
IMPORTPATH=r'resources\budget_data.csv'
EXPORTPATH=r'analysis\analysis.txt'
import os
pth=os.getcwd()
import os.path
IMPORTPATH=os.path.join(pth,IMPORTPATH)
EXPORTPATH=os.path.join(pth,EXPORTPATH)

class App:
    def __init__(self):
        self.header=None
        self.data=[]
        self.changes=[]
        self.stats={}
        #
        self.get_file()
        self.compute()
        self.export()
        print('done.')

    def get_file(self):
        '''this function populates the data list and saves the header'''
        with open(IMPORTPATH,newline='') as fobj:
            csvreader=csv.reader(fobj)
            for row in csvreader:
                self.data+=[row]
        self.header=self.data.pop(0) #store the header as requested, but not used
    
    def compute(self):
        '''this function performs all computations and saves those to self.stats
           also creates a list of changes
        '''
        self.stats['total number of months']=len(self.data)
        self.stats['net profit/loss']=sum([int(x[1]) for x in self.data])
        for i in range(1,len(self.data)):#populate a list of changes for use below
            self.changes+=[(self.data[i][0],int(self.data[i][1])-int(self.data[i-1][1]))]
        self.stats['sum of changes']=sum([x[1] for x in self.changes])
        self.stats['average change']=round(self.stats['sum of changes']/len(self.changes),2)
        
        #search through the list of changes for greatest increase/decrease
        self.stats['greatest increase']=self.stats['greatest decrease']=None
        for tup in self.changes:
            mo,ch=tup
            #
            if self.stats['greatest increase']==None:
                self.stats['greatest increase']=tup
            elif ch>self.stats['greatest increase'][1]:
                self.stats['greatest increase']=tup
            #
            if self.stats['greatest decrease']==None:
                self.stats['greatest decrease']=tup
            elif ch<self.stats['greatest decrease'][1]:
                self.stats['greatest decrease']=tup

    def export(self):
        '''this function creates a list and exports it to the text file as an analysis'''
        exportlist=[]
        exportlist+=['Financial Analysis']
        exportlist+=['-'*30]
        exportlist+=['Total Months: %s'%self.stats['total number of months']]
        exportlist+=['Total: $%s'%self.stats['net profit/loss']]
        exportlist+=['Average Change: $%s'%self.stats['average change']]
        exportlist+=['Greatest Increase in Profits: %s ($%s)'%(self.stats['greatest increase'][0],
                                                               self.stats['greatest increase'][1])]
        exportlist+=['Greatest Decrease in Profits: %s ($%s)'%(self.stats['greatest decrease'][0],
                                                               self.stats['greatest decrease'][1])]
        exportlist=[x+'\n\n' for x in exportlist]
        with open(EXPORTPATH,'w') as fobj:
            fobj.writelines(exportlist)


if __name__=='__main__':
    app=App()