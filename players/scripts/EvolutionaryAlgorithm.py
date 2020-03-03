from players.player import Player
from players.scripts.DSL import DSL
from players.scripts.Script import Script
import random
import string
import importlib
import numpy as np
import sys
import collections
from game import Board, Game
import os, shutil
import matplotlib.pyplot as plt 

class EvolutionaryAlgorithm:
    def __init__(self):
         #Total No of  Script to generate automatically
        self.pop_n=10 # Total no of script from Population z
        self.e=5 #best 4 script
        self.t=5
        self.genL=3
        self.rules_list= []
        self.rate=0.5
        self.dsl= DSL()
        self.scripts=[] #list of script object
        #print("In Initialization.....")
        for r in range(self.pop_n): #for each script
            no_of_rules= random.randint(1, 5) #No of rules in a script
            templist=[]
            for c in range(no_of_rules): #for each rule in a script
                subrule=random.randint(1,4)
                str2=''
                for i in range(subrule):
                    str2+=random.choice(self.dsl._grammar['B1'])
                    if str2.find('SMALL_NUMBER') != -1:
                        str2=str2.replace('SMALL_NUMBER', random.choice(self.dsl._grammar['SMALL_NUMBER']))
                    if str2.find('NUMBER') != -1:
                        str2=str2.replace('NUMBER', random.choice(self.dsl._grammar['NUMBER']))
                    if i<(subrule-1):
                        str2+=' and '
                str1=str2
                templist.append(str1)
            setlist=set(templist) #Removing Duplicate rules using set
            templist=list(setlist)
            self.rules_list.append(templist)
            self.scripts.append(Script(self.rules_list[r],r))

        for i in range(self.pop_n):
            self.scripts[i].saveFile('/Users/maithrreye/Winter2020/XAI/cant-stop-assignment/players/scripts/__pycache__/')  
        self.ezs()


    def ezs(self):
        self.instance_script=[]
        self.P=[]
        for i in range(self.pop_n):
            obj=self.generate_scriptInstance(i)
            self.instance_script.append(obj)#obj of all Script class
        self.P=self.instance_script
        self.Pscript=self.scripts
        for _ in range(self.genL):
            self.evaluate()
            PDash=[]
            topEindex=[]
            pdashscripts=[]
            topEindex=self.elite()
            for i in topEindex:
                PDash.append(self.P[i])
                pdashscripts.append(self.scripts[i])
            while len(PDash) < len(self.P):
                p=[]
                p=self.tournament()
                p1=self.Pscript[p[0]].getRules()
                p2=self.Pscript[p[1]].getRules()
                c=self.crossover(p1,p2)
                c=self.mutation(c)
                self.rules_list.append(c)
                l=(len(self.rules_list)-1)
                self.scripts.append(Script(self.rules_list[l],l))
                self.scripts[l].saveFile('/Users/maithrreye/Winter2020/XAI/cant-stop-assignment/players/scripts/__pycache__/')
                pdashscripts.append(self.scripts[l])
                obj=self.generate_scriptInstance(l)
                PDash.append(obj)
            self.P=[]
            self.P=PDash
            self.Pscript=[]
            self.Pscript=pdashscripts
            print("GO TO NEXT GENERATION.....")
        self.evaluate()
        self.getLargestFitness()


    def generate_scriptInstance(self,id):
        classname='Script'+str(id)
        tempstr='players.scripts.__pycache__.'+classname
        import importlib
        module = importlib.import_module(tempstr)
        class_ = getattr(module,classname)
        obj=class_()
        return obj
        

    def evaluate(self):
        #print("In Evaluate.....")
        self.victories_list=np.zeros(len(self.P), dtype=int)
        self.loss_list=np.zeros(len(self.P), dtype=int)
        self.fitness_list=np.zeros(len(self.P), dtype=int)
        for i in range(len(self.P)):
            for j in range(len(self.P)):
                random=self.P[i]
                test=self.P[j]
                print("Random player  type..." +str(random))
                print("test player  type..." +str(test))
                victories1=0
                victories2=0
                for _ in range(100): #100
                    game = Game(n_players = 2, dice_number = 4, dice_value = 3, column_range = [2,6],
                    offset = 2, initial_height = 1)
                    is_over = False
                    who_won = None
                    number_of_moves = 0
                    current_player = game.player_turn
                    while not is_over:
                        moves = game.available_moves()
                        if game.is_player_busted(moves):
                            if current_player == 1:
                                current_player = 2
                            else:
                                current_player = 1
                            continue
                        else:
                            if game.player_turn == 1:
                                chosen_play = random.get_action(game)
                            else:
                                chosen_play = test.get_action(game)
                            if chosen_play == 'n':
                                if current_player == 1:
                                    current_player = 2
                                else:
                                    current_player = 1
                            #print('Chose: ', chosen_play)
                            #game.print_board()
                            game.play(chosen_play)
                            #game.print_board()
                            number_of_moves += 1
                
                            #print()
                        who_won, is_over = game.is_finished()
            
                        if number_of_moves >= 200:
                            is_over = True
                            who_won = -1
                            #print('No Winner!')
                            self.victories_list[i]-=1
                            self.victories_list[j]-=1
                
                if who_won == 1:
                    victories1 += 1
                    self.victories_list[i]+=1
                    self.loss_list[j]+=1

                if who_won == 2:
                    victories2 += 1
                    self.victories_list[j]+=1
                    self.loss_list[i]+=1

                print(victories1, victories2)

                #print('Player 1: ', victories1 / (victories1 + victories2))
                #print('Player 2: ', victories2 / (victories1 + victories2))

        self.fitness_list=np.subtract(self.victories_list,self.loss_list)
        print("Fitness Result " + str(self.fitness_list))
        #self.plotgraph()
        self.clearpycache()
        self.remove_unused_rules()
        for i in range(len(self.Pscript)):
            self.Pscript[i].saveFile('/Users/maithrreye/Winter2020/XAI/cant-stop-assignment/players/scripts/__pycache__/')  
        for i in range(len(self.P)):
            id=self.Pscript[i].getId()
            self.P[i]=self.generate_scriptInstance(id)


    def elite(self):
        N=self.e
        elite_list=[]
        tempFitness=self.fitness_list
        flist=tempFitness.tolist()
        elite_list = sorted(range(len(flist)), key = lambda sub: flist[sub],reverse=True)[:N]
        #return the index of Top 'e' fitness
        return elite_list
        
    def tournament(self):
        #print("Coming inside tournament")
        #t_index=np.random.randint(0,len(self.P),self.t)
        temp=self.fitness_list.tolist()
        t_index=np.random.randint(low = 0, high = len(self.P), size = self.t)
        #print("Script Index..."+str(t_index))
        flist=[]
        p=[]
        q=[]
        for i in t_index:
            flist.append(temp[i])
        p=sorted(range(len(flist)), key = lambda sub: flist[sub],reverse=True)[:2]
        for i in p:
            q.append(temp.index(flist[i]))
        return q

    def crossover(self,p1,p2):
        c1=[] 
        #p1 and p2 are rules list of 2 parents
        p1_c1,p1_c2=self.generateSplit(p1)
        #print("p1_c1")
        p2_c2,p2_c1=self.generateSplit(p2)
        #print("p2_c2")
        c1=p1_c1+p2_c1
        return c1


    def generateSplit(self,p):
        split_index = random.randint(0, len(p))
        split1 = p[0:split_index + 1]
        split2 = p[split_index + 1: len(p) + 1]
                
        return split1, split2

    def mutation(self,c):
        #print("Coming inside mutation")
        #print(str(type(c)))
        #print(str(c))
        mutated_rules = []
        has_mutated = False
        for i in range(len(c)):
            #checking if mutation will happen
            if random.randint(0, 100) < self.rate * 100:
                has_mutated = True
                rule =self.generateRandomRule()
                #verify if mutation replaces old rule
                if random.randint(0, 100) < self.rate * 100:
                    mutated_rules.append(rule)
                else:
                    mutated_rules.append(c[i])
                    mutated_rules.append(rule)
            else:
                mutated_rules.append(c[i])
                
        if has_mutated:
            c= mutated_rules
        return c

    def generateRandomRule(self):
        subrule=random.randint(1,3)
        str2=''
        for i in range(subrule):
            str2+=random.choice(self.dsl._grammar['B1'])
            if str2.find('SMALL_NUMBER') != -1:
                str2=str2.replace('SMALL_NUMBER', random.choice(self.dsl._grammar['SMALL_NUMBER']))
            if str2.find('NUMBER') != -1:
                str2=str2.replace('NUMBER', random.choice(self.dsl._grammar['NUMBER']))
            if i<(subrule-1):
                str2+=' and '
        return str2

    def getLargestFitness(self):
        flist=self.fitness_list.tolist()
        p=sorted(range(len(flist)), key = lambda sub: flist[sub],reverse=True)[:1]
        id=self.Pscript[p[0]].getId()
        print("The highest fitness script is......" + "Script" +str(id) + "with Fitness value " +str(flist[p[0]]))


    def remove_unused_rules(self):
        new_rules = []
        rules=[]
        for i in range(len(self.Pscript)):
            rules=self.Pscript[i].getRules()
            lengthofRules=len(rules)
            obj=self.P[i]
            print(str(obj))
            countercalls=self.P[i].get_counter_calls()
            lengthofCounter=len(countercalls)
            print("lengthofCounter" +str(lengthofCounter))
            if lengthofRules== lengthofCounter:
                for j in range(0,lengthofCounter):
                    r=rules[j]
                    temp=countercalls[j]
                    if temp > 0:
                        new_rules.append(r)
                if len(new_rules) > 0:
                    rules = new_rules
            setlist=set(rules) 
            rules=list(setlist)
            self.Pscript[i].setRules(rules)

    
    def clearpycache(self):
        folder = '/Users/maithrreye/Winter2020/XAI/cant-stop-assignment/players/scripts/__pycache__/'
        filelist = [ f for f in os.listdir(folder) if f.endswith(".py") ]
        for f in filelist:
            os.remove(os.path.join(folder, f))
        mydir='/Users/maithrreye/Winter2020/XAI/cant-stop-assignment/players/scripts/__pycache__/__pycache__/'
        filelist2 = [ fp for fp in os.listdir(mydir) if f.endswith(".pyc") ]
        for fp in filelist2:
            os.remove(os.path.join(mydir, fp))

    def plotgraph(self):
        tempFitness=[]
        X=[]
        Y=[]
        tempFitness=self.fitness_list
        arrsum=np.sum(tempFitness, dtype = np.uint8)
        #l=len(self.fitness_list)
        #div=l*l
        for i in range(len(self.Pscript)):
           id=self.Pscript[i].getId()
           X.append(id)
           win=int(self.fitness_list[i]/arrsum)
           Y.append(win)
        #plt.plot(X, Yavg, color='green', linestyle='dashed', linewidth = 3, 
         #marker='o', markerfacecolor='blue', markersize=12)
        plt.xticks(np.arange(0, 60, 2))
        #plt.yticks(np.arange(-10,50,5))  
        plt.plot(X,Y)
        plt.xlabel('Script IDs') 
        plt.ylabel('Average') 
        plt.title('Script ID vs Average') 
        plt.show() 
  


       






