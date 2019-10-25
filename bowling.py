# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 11:00:44 2019

@author: Stian
@email: stian.teien@gmail.com
"""

import random
import matplotlib.pyplot as plt
import copy


class Bowlingsimulation:
    """
    In this bowlingsimulation frames and lines can be simulated
    A scoreboeard can bring up the result in the end
    
    input: arrays of player
    """
    
    def __init__(self, players):
        self.players = players
    
    def one_frame(self, roundnumber):
        # Plays one frame for all players
        for player in self.players:
            player.frame_score = [0, 0]
            throws = 1
            pins_left = 10 - player.first_throw()
            player.frame_score[0] = 10 - pins_left
            if(pins_left > 0):
                throws = 2
                player.frame_score[1] = player.second_throw(pins_left)
                
            
            # Calculate a strike!
            if("X" in player.score[roundnumber-1]):
                if("X" in player.score[roundnumber-2]):
                    player.totalscore[roundnumber-2] += player.frame_score[0]
                    player.totalscore[roundnumber-1] += player.frame_score[0]
                    
                player.totalscore[roundnumber-1] += player.frame_score[0] + player.frame_score[1]
                player.totalscore[roundnumber] += player.totalscore[roundnumber-1] + 10
                
                
            # Calculate a spare!
            elif ("/" in player.score[roundnumber-1]):
                player.totalscore[roundnumber-1] += player.frame_score[0]
                player.totalscore[roundnumber] += player.totalscore[roundnumber-1] + 10
               
            # Normal calcualtion
            else:
                player.totalscore[roundnumber] += player.totalscore[roundnumber-1] + sum(player.frame_score)
                
            
            player.score[roundnumber] = self.spare_and_strike(player.frame_score, throws)            
            
            
            
            # Extra throw in the end!
            if(roundnumber == 9 and not sum(player.frame_score) == 10):
                player.score[10] = ["",""]
                
            if roundnumber == 9 and sum(player.frame_score) == 10:
                player.frame_score = [0, 0]
                if('X' in player.score[roundnumber]):
                    # To ekstra kast
                    player.frame_score[0] = player.third_throw()
                    if(10 - player.frame_score[0] > 0):
                        player.frame_score[1] = player.second_throw(10 - player.frame_score[0])
                    if(10 - player.frame_score[0] == 0):
                        player.frame_score[1] =  player.third_throw()                       
                    
                else:
                    player.frame_score[0] = player.third_throw()
                  
                # Calculate a strike!
                if("X" in player.score[roundnumber]):
                    if("X" in player.score[roundnumber-1]):
                        player.totalscore[roundnumber-1] += player.frame_score[0]
                        player.totalscore[roundnumber] += player.frame_score[0]
                    
                    player.totalscore[roundnumber] += player.frame_score[0] + player.frame_score[1]

                    
                # Calculate a spare!
                elif ("/" in player.score[roundnumber]):
                    player.totalscore[roundnumber] += player.frame_score[0]
                
                if(player.frame_score[0] == 10): player.frame_score[0] = "X"
                if(player.frame_score[1] == 10): player.frame_score[1] = "X" 
                if(player.frame_score[0] == 0): player.frame_score[1] = ""
                if(player.frame_score[1] == 0): player.frame_score[1] = ""
                player.score[10] = player.frame_score

            
            
     
    def one_line(self):
        # Plays one line for all players
        for i in range(10):
            self.one_frame(i)

            
    def spare_and_strike(self, points, throws):
        """
        if throw = 1 & score = 10 --> X
        if throw = 2 & score = 10 --> /
        if point = 0 --> "-"
        
        """
        temp_points = copy.deepcopy(points)
        if(throws == 1 and temp_points[0] == 10):
            return ["X"]
        elif(throws == 2 and sum(temp_points) == 10):
            return [temp_points[0], "/"]
        
        
        if(temp_points[0] == 0):
            temp_points[0] = "-"
        if(temp_points[1] == 0):
            temp_points[1] = "-"
        return temp_points
            
        
    
    
    def scoreboard(self):
        #Shows scoreboeard
        self.fig = plt.figure(figsize=(10,5))
        axis_headline = plt.axes([0.3, 0.93, 0.3, 0.0001])
        axis_headline.set_title("BOWLINGSCORE!")
        axis_headline.axis('off')
        
        axis_round = plt.axes([0.43, 0.84, 0.1, 0.1])
        axis_round.text(0,0, "Frame", style='italic')
        axis_round.axis('off')
        
        axis_totalscore = plt.axes([0.78, 0.8, 0.3, 0.3])
        axis_totalscore.text(0,0, "Totalscore")
        axis_totalscore.axis('off')
        
        users_axis = [None]*len(self.players)
        total_axis = [None]*len(self.players)
        y = 0.7
        
        throw_axis = [None]*11
        for i in range(11):
            throw_axis[i] = plt.axes([0.22+(i/20), 0.80, 1,1])
            throw_axis[i].axis('off')
            throw_axis[i].text(0,0, i+1)
            
        
        for i, player in enumerate(self.players):
            users_axis[i] = plt.axes([0.05, y, 0.1, 0.001]) 
            users_axis[i].set_title(player.name)
            users_axis[i].axis('off')
            #axis[i].axes.get_xaxis().set_visible(False)
            #axis[i].axes.get_yaxis().set_visible(False)
            
            total_axis[i] = plt.axes([0.80, y+0.017, 1, 1])
            total_axis[i].text(0,0, player.totalscore[-1], fontweight='bold')
            total_axis[i].axis('off')
            
            axis = [None]*11
            for j, value in enumerate(player.score):
                # Puts out first tabel with round score
                axis[j] = plt.axes([0.2+(j/20), y+0.01, 0.05, 0.04])
                temp = str(value[0])
                if(len(value)>1): temp += " | "+str(value[1])
                axis[j].text(0.25, 0.2, temp)
                axis[j].axes.get_xaxis().set_visible(False)
                axis[j].axes.get_yaxis().set_visible(False)
            
            axis = [None]*11
            for j, value in enumerate(player.totalscore):
                # Puts out totalscore tabel
                axis[j] = plt.axes([0.2+(j/20), y-0.03, 0.1, 0.1])
                axis[j].text(0.17, 0.05, value)
                axis[j].axis('off')
            
            y = y - 0.15
            #axis_name = plt.axes([0.05])
            #axis[i] = [][]
            #self.ax1 = plt.axes([[0.07, 0.65, 0.41, 0.32]])
            
            
    
    
    
class Bowlingplayer:
    """
    In this bowlingplayer object a bowlingplayer is made based on experiencelevel
    Used to make the player throw bowlingsballs and controll score of each player
    
    input: experience of player 
    """
    def __init__(self, level, name):
        self.level = level
        self.score = [[0,0]]*11
        self.level_distrubtior()
        self.frame_score = [0, 0]
        self.totalscore = [0]*10
        self.max_point_frame = 10
        self.name = name
        
        
    def level_distrubtior(self):
        # Makes a random-konstant based on level
        levels = {"New":0, "Great":1, "Advance":2, "Expert":3}
        if self.level not in levels:
            raise KeyError("Not legal level")
            
        self.random_constant = levels[self.level]
        
        
    def first_throw(self):
        return random.randint(self.random_constant, self.max_point_frame)
        
    def second_throw(self, pins_left):
        if self.random_constant >= pins_left:
            return pins_left
        
        return random.randint(self.random_constant, pins_left)
    
    def third_throw(self):
        return self.first_throw()
    

if __name__ == "__main__":
    
    """
    Levels: New, Great, Advance, Expert
    """
    
    # Players
    stian = Bowlingplayer("New", "Stian")
    julie = Bowlingplayer("Advance", "Julie")
    lars = Bowlingplayer("Expert", "Lars")
    marte = Bowlingplayer("Expert", "Marte")
    
    
    # Simualtion
    sparebankens_bowlinghall = Bowlingsimulation([stian, julie, lars, marte])
    sparebankens_bowlinghall.one_line()
    sparebankens_bowlinghall.scoreboard()
    