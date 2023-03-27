# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 17:27:12 2023

@author: roberterick
"""
import csv

#this always worked before
# IMPORTPATH=r'.\resources\election_data.csv'
# EXPORTPATH=r'.\analysis\analysis.txt'

#i adjusted things.  hopefully this works.  i think the 
#directory structure is to spec
IMPORTPATH=r'resources\election_data.csv'
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
        '''this function performs all computations and saves those to self.stats'''
        self.stats['total votes']=len(self.data)
        self.stats['by candidate']={}
        #
        self.count_votes_by_candidate()
        self.compute_vote_percentages()
        self.find_the_winner()
    
    def count_votes_by_candidate(self):
        for i in range(0,len(self.data)): 
            ballot,county,candidate=self.data[i]
            if not candidate in self.stats['by candidate']:#setup a new key if needed
                self.stats['by candidate'][candidate]=[0,0] #this means [percentage,votes]
            self.stats['by candidate'][candidate][1]+=1  
        
    def compute_vote_percentages(self):
        #compute vote percentages
        for k in self.stats['by candidate']: #
            self.stats['by candidate'][k][0]=self.stats['by candidate'][k][1]/self.stats['total votes']
        
    def find_the_winner(self):
        #find the winner
        summary=[(self.stats['by candidate'][x][1],x) for x in self.stats['by candidate']]
        summary.sort(reverse=True)
        self.stats['winner']=summary[0][1]

    def export(self):
        '''this function creates a list and exports it to the text file as an analysis'''
        exportlist=[]
        exportlist+=['Election Results']
        exportlist+=['-'*30]
        exportlist+=['Total Votes: %s'%self.stats['total votes']]
        exportlist+=['-'*30]
        for k in self.stats['by candidate']:#print each candidate
            exportlist+=['%s: %s (%s)'%(k,'{:.3%}'.format(self.stats['by candidate'][k][0])
                                       ,self.stats['by candidate'][k][1])]
        exportlist+=['-'*30]
        exportlist+=['Winner: %s'%self.stats['winner']]
        exportlist+=['-'*30]
        exportlist=[x+'\n\n' for x in exportlist]
        with open(EXPORTPATH,'w') as fobj:
            fobj.writelines(exportlist)


if __name__=='__main__':
    app=App()