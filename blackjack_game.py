'''
Project: Twenty One Game:
Course: CS 1410 X01
Name: Jordan Paxman
Due Date: January 20th 2023

Description:
A game of Black Jack. You, the user, play as the player against the dealer, or the program.
There is no betting involved, but you can play the game by running the program in the command line.
press the up arrow key until it reads 'python3 twentyone.py'. Press enter. Then follow the instructions
to play the game!
The only issue with the cards printing side to side is that when it runs out of space on the screen, it begins to print weird.
usually more than 4 cards in a hand will throw things off. But hand_values are still acurate. 

'''

import os
import random
import time


class Card:
   '''needs a method that returns the card as a string in ASCII art.
    Also a boolean flag that indicates whether the card is face 
    up or down.'''
   def __init__(self, suit, value, numeric_value, is_ace, flipped):
      self.suit = suit
      self.value = value
      self.numeric_value = numeric_value
      self.is_ace = False
      self.flipped = False

   def is_ace(self):
      '''To see if a card has an ace value'''
      if self.value == 'A':
         self.is_ace = True
         

   def __repr__(self):
      '''returning the representation of the cards in each situation'''
      if self.value == '10':
         return f"""
 ---------------- 
|                |
|  {self.value}            |
|                |
|                |
|                |
|                |
|       {self.suit}        |
|                |
|                |
|                |
|                |
|             {self.value} |
|                |
 ---------------- 
 \n
"""
      if self.flipped == True:
         return f"""
 ---------------- 
|                |
|  ?             |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|             ?  |
|                |
 ---------------- 
 \n
"""

      else:
         return f"""
 ---------------- 
|                |
|  {self.value}             |
|                |
|                |
|                |
|                |
|       {self.suit}        |
|                |
|                |
|                |
|                |
|             {self.value}  |
|                |
 ---------------- 
 \n
"""


#Boolean flag that needs to show if card is face up or face down

class Deck:
   def __init__(self):
      self.suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
      self.suits_values = {"Spades":"\u2664", "Hearts":"\u2661", "Clubs": "\u2667", "Diamonds": "\u2662"}
      self.cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
      self.numeric_values = {"A": 11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}
      self.deck = []

   def build(self):
      '''builds the deck'''
      for s in self.suits:
         for v in self.cards:
            is_ace = False
            if self.numeric_values[v] == 11:
               is_ace = True
            card = Card(self.suits_values[s], v, self.numeric_values[v], is_ace, False)
            self.deck.append(card)

   def show_deck(self):
      '''function that helps you print each card in the deck'''
      for card in self.deck:
         print(card)

   def shuffle(self):
      '''shuffles the deck'''
      for i in range(len(self.deck) - 1, 0, -1):
         r = random.randint(0, i)
         self.deck[i], self.deck[r] = self.deck[r], self.deck[i]
      return self.deck

   def draw_card(self):
      '''draws card and prints the string repr of card'''
      card = self.deck.pop()
      return card


class Hand:
   def __init__(self):
      self.cards = []

   def add_card(self, card):
      '''adds card to hand'''
      self.cards.append(card)
   
   def sum(self):
      '''finds the sum of the hands value'''
      hand_value = 0
      has_ace = False
      for card in self.cards:
         #filter out cards that are face down
         hand_value += card.numeric_value
         if card.value == 'A':
            card.is_ace = True
            if card.is_ace == True:
               has_ace = True
         if hand_value > 21 and has_ace == True:
            for card in self.cards:
               if hand_value > 21:
                  if card.is_ace == True:
                     hand_value -= 10
      return hand_value
   
   def dealer_sum(self):
      '''finds the sum for the dealer before he reveals his flipped card'''
      hand_value = 0
      has_ace = False
      first_card = self.cards[0]
      hand_value += first_card.numeric_value
      return hand_value


   def zip_cards(self, card1, card2): 
      '''takes the repr of each string of the card, splits them, and returns them
      as single card, so then it can be passed to the next method'''

      '''Must return a string with new line characters at the end!!!
      '''
      lines1 = card1.split('\n')
      lines2 = card2.split('\n')
      tuples = zip(lines1, lines2)
      single_unit = '' #array of strings representing the results
      for tple in tuples:
         # combine all parts of tuple into single string
         tmp_string = ""
         for i in tple:
            tmp_string += i + "      "
         single_unit += tmp_string + '\n'
         # append the result of ^^^^ to single_unit
      return single_unit 
   
   def side_by_side(self):
      '''prints each repr string side by side'''
      tmp_cards = self.cards.copy()
      c1 = tmp_cards.pop(0)
      c2 = tmp_cards.pop(0)
      retval = self.zip_cards(str(c1), str(c2))
      while len(tmp_cards) > 0:
         retval = self.zip_cards(retval, str(tmp_cards.pop(0)))
      
      print(retval)

class Dealer:
   def __init__(self, deck, player):
      self.hand = Hand()
      self.deck = deck
      self.player = player

   def to_dealer(self):
      '''deals to dealer hand'''
      self.hand.add_card(self.deck.draw_card())

   def to_player(self):
      '''deals to player hand'''
      self.player.hand.add_card(self.deck.draw_card())

class Player:
   def __init__(self):
      '''the collection of cards dealt to the player'''
      self.hand = Hand()

class Game:
   def __init__(self, deck, player, dealer):
      self.deck = deck
      self.player = player
      self.dealer = dealer

   def run(self):
      '''implements the pseudocode algorithm 
      given in the module docstring.'''
      self.deck.build()
      self.deck.shuffle()
      #initial deal
      self.dealer.to_player()
      self.dealer.to_dealer()
      self.dealer.to_player()
      self.dealer.to_dealer()
      self.dealer.hand.cards[1].flipped = True

      #zip cards to go side by side
      #show cards
      print('PLAYER CARDS:')
      self.player.hand.side_by_side() 
      print('DEALER CARDS:')
      self.dealer.hand.side_by_side()
      print('PLAYER SCORE: ', self.player.hand.sum())
      print('DEALER SCORE: ', self.dealer.hand.dealer_sum())
      self.player_turn()


   def player_turn(self):
      '''implement code for the player’s turn.'''
      player_cards = self.player.hand.cards
      if self.player.hand.sum() == 21:
         input('YOU GOT BLACKJACK! \nRUN PROGRAM AGAIN FOR NEW HAND>')

      while self.player.hand.sum() < 21:
         user_input = input('Type Y to hit or N to not hit: ') 
         if user_input.lower() == 'y':
            #add card
            self.dealer.to_player()
            print('PLAYER CARDS:')
            self.player.hand.side_by_side()
            print('PLAYER SCORE: ', self.player.hand.sum(), '\n')
            if self.player.hand.sum() > 21:
               print('YOU BUSTED! :( \nRUN PROGRAM AGAIN FOR NEW HAND.')
            if self.player.hand.sum() == 21:
               self.dealer_turn()
         if user_input == 'n':
            self.dealer_turn()
            break
            
           
   def dealer_turn(self):
      '''implement code for the dealer’s turn.'''
      dealer_cards = self.dealer.hand.cards
      print('DEALERS TURN')
      self.dealer.hand.cards[1].flipped = False
      self.dealer.hand.side_by_side()
      print('DEALER SCORE:', self.dealer.hand.sum())
      time.sleep(1)
      while self.dealer.hand.sum() < 17:
         self.dealer.to_dealer()
         self.dealer.hand.side_by_side()
      print('PLAYER SCORE:', self.player.hand.sum())
      print('DEALER SCORE:', self.dealer.hand.sum())
      if self.dealer.hand.sum() <= 21:
         if self.dealer.hand.sum() > self.player.hand.sum():
            print('DEALER WINS! SORRY! :( \nRUN PROGRAM AGAIN FOR NEW HAND.')
         if self.dealer.hand.sum() < self.player.hand.sum():
            print('YOU WIN! :) \nRUN PROGRAM AGAIN FOR NEW HAND.')
      if self.dealer.hand.sum() == self.player.hand.sum():
         print('YOU PUSHED! \nRUN PROGRAM AGAIN FOR NEW HAND.')
      if self.dealer.hand.sum() > 21:
         print('DEALER BUSTS! YOU WIN! :) \nRUN PROGRAM AGAIN FOR NEW HAND.')


def clear():
   """Clear the console."""
   # for windows
   if os.name == 'nt':
      _ = os.system('cls')
   # for mac and linux, where os.name is 'posix'
   else:
      _ = os.system('clear')

def main():
   #creating deck -  will move to the Game class once its all working.
   deck = Deck()
   player = Player()
   dealer = Dealer(deck, player)
   my_game = Game(deck, player, dealer)
   my_game.run()
   
   
   #deck.show_deck() # prints the whole shuffled deck


if __name__ == '__main__':
   main()

