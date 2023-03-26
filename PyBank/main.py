# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 17:27:12 2023

@author: roberterick
"""
import csv
import math

IMPORTPATH=r'.\resources\budget_data.csv'
EXPORTPATH=r'.\analysis\analysis.txt'

class App:
    def __init__(self):
        self.data=[]
        self.changes=[]
        self.stats={}
        
        self.get_file()
        self.compute()
        self.export()
        
        # for l in self.data:
        #     print(l)

    def get_file(self):
        with open(IMPORTPATH,newline='') as fobj:
            csvreader=csv.reader(fobj)
            for row in csvreader:
                self.data+=[row]
        self.data.pop(0) #remove the header
    
    def compute(self):
        self.stats['total number of months']=len(self.data)
        self.stats['net profit/loss']=sum([int(x[1]) for x in self.data])
        for i in range(1,len(self.data)):
            self.changes+=[(self.data[i][0],int(self.data[i][1])-int(self.data[i-1][1]))]
        self.stats['average change']=round(sum([x[1] for x in self.changes])/len(self.changes),2)
        
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
        print(self.stats)

    def export(self):
        exportlist=[]
        exportlist+=['Financial Analysis']
        exportlist+=['-'*30]
        exportlist+=['Total Months: %s'%self.stats['total number of months']]
        exportlist+=['Total: $%s'%self.stats['net profit/loss']]
        exportlist+=['Average Change: $%s'%self.stats['average change']]
        exportlist+=['Greatest Increase in Profits: %s ($%s)'%(self.stats['greatest increase'][0],self.stats['greatest increase'][1])]
        exportlist+=['Greatest Decrease in Profits: %s ($%s)'%(self.stats['greatest decrease'][0],self.stats['greatest decrease'][1])]
        exportlist=[x+'\n\n' for x in exportlist]
        with open(EXPORTPATH,'w') as fobj:
            fobj.writelines(exportlist)
        print('done.')


if __name__=='__main__':
    app=App()