from tkinter import *
from tkinter import messagebox
from winsound import *
import random

class Solitaire():
    def __init__(self):
        self.cards = [['AS','2S','3S','4S','5S','6S','7S','8S','9S','10S','JS','QS','KS'],
                      ['AH','2H','3H','4H','5H','6H','7H','8H','9H','10H','JH','QH','KH'],
                      ['AD','2D','3D','4D','5D','6D','7D','8D','9D','10D','JD','QD','KD'],
                      ['AC','2C','3C','4C','5C','6C','7C','8C','9C','10C','JC','QC','KC'],
                      ]
        self.deck = []
        self.piles = [[0],
                      [0,0],
                      [0,0,0],
                      [0,0,0,0],
                      [0,0,0,0,0],
                      [0,0,0,0,0,0],
                      [0,0,0,0,0,0,0]]
        self.flipped_cards = []
        self.stacks = [[0],[0],[0],[0]]
        self.deckcard = None
        self.highlighted_card = None
        self.first_flip = True
        self.window = Tk()
        self.window.title('Solitaire')
        self.canvas = Canvas(self.window, bg='white', height=725, width=1205)
        self.canvas.pack()
        self.menubar = Menu(self.window)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.about)
        self.filemenu.add_command(label="New Game", command=self.new_game)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.window.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.window.config(menu=self.menubar)
        self.shuffle_cards()
        self.create_canvas()
        self.play_sound()
        self.window.mainloop()

    def play_sound(self):
        return PlaySound('sounds/shuffling_sound.wav', SND_FILENAME)

    def about(self):
        messagebox.showinfo('Solitaire', 'Made by Jason Alencewicz!')
        return

    def new_game(self):
        self.cards = [['AS','2S','3S','4S','5S','6S','7S','8S','9S','10S','JS','QS','KS'],
                      ['AH','2H','3H','4H','5H','6H','7H','8H','9H','10H','JH','QH','KH'],
                      ['AD','2D','3D','4D','5D','6D','7D','8D','9D','10D','JD','QD','KD'],
                      ['AC','2C','3C','4C','5C','6C','7C','8C','9C','10C','JC','QC','KC'],
                      ]
        self.deck = []
        self.piles = [[0],
                      [0,0],
                      [0,0,0],
                      [0,0,0,0],
                      [0,0,0,0,0],
                      [0,0,0,0,0,0],
                      [0,0,0,0,0,0,0]]
        self.flipped_cards = []
        self.stacks = [[0],[0],[0],[0]]
        self.highlighted_card = None
        self.deckcard = None
        self.first_flip = True
        self.canvas.delete("all")
        self.shuffle_cards()
        self.create_canvas()
        self.play_sound()
        return

    def create_canvas(self):
        #background 
        self.bgimg = PhotoImage(file="images/cardtable.png")
        self.canvas.create_image(0,0, anchor=NW, image=self.bgimg)

        #top row
        self.canvas.create_rectangle(20, 50, 170, 250,  outline="darkgray", fill="lightgrey", tag="back_of_deck")
        self.canvas.tag_bind("back_of_deck", '<1>', self.on_click_boc)
        self.boc = PhotoImage(file="images/back_of_card.png")
        self.canvas.create_image(20,50, anchor=NW, image=self.boc, tag="back_of_card")
        self.canvas.tag_bind("back_of_card", '<1>', self.on_click_boc)
        
        self.canvas.create_rectangle(530, 50, 680, 250,  outline="darkgray", fill="lightgrey", tag="spades")
        self.canvas.tag_bind("spades", '<1>', self.on_click_stack)
        self.spadesimg = PhotoImage(file="images/spades.png")
        self.canvas.create_image(580,125, anchor=NW, image=self.spadesimg, tag="spadesimg")
        self.canvas.tag_bind("spadesimg", '<1>', self.on_click_stack)
        
        self.canvas.create_rectangle(700, 50, 850, 250,  outline="darkgray", fill="lightgrey", tag="hearts")
        self.canvas.tag_bind("hearts", '<1>', self.on_click_stack)
        self.heartsimg = PhotoImage(file="images/hearts.png")
        self.canvas.create_image(750,125, anchor=NW, image=self.heartsimg, tag="heartsimg")
        self.canvas.tag_bind("heartsimg", '<1>', self.on_click_stack)

        self.canvas.create_rectangle(870, 50, 1020, 250,  outline="darkgray", fill="lightgrey", tag="diamonds")
        self.canvas.tag_bind("diamonds", '<1>', self.on_click_stack)
        self.diamondsimg = PhotoImage(file="images/diamonds.png")
        self.canvas.create_image(920,125, anchor=NW, image=self.diamondsimg, tag="diamondsimg")
        self.canvas.tag_bind("diamondsimg", '<1>', self.on_click_stack)

        self.canvas.create_rectangle(1040, 50, 1190, 250,  outline="darkgray", fill="lightgrey", tag="clubs")
        self.canvas.tag_bind("clubs", '<1>', self.on_click_stack)
        self.clubsimg = PhotoImage(file="images/clubs.png")
        self.canvas.create_image(1090,125, anchor=NW, image=self.clubsimg, tag="clubsimg")
        self.canvas.tag_bind("clubsimg", '<1>', self.on_click_stack)

        #bottom row
        axis1 = 20
        axis2 = 170
        rect_num = 500
        for x, val in enumerate(self.piles):
            top_card_length = 0
            rect_name = 'rect'+str(x+1)
            rect_value = self.canvas.create_rectangle(axis1, 300, axis2, rect_num, outline="darkgray", fill="lightgrey", tag="pile"+str(x+1))
            setattr(self, rect_name, rect_value)
            self.canvas.tag_bind("pile"+str(x+1), '<1>', self.on_click_pile)
            rect_num += 15
            for y, val2 in enumerate(val):
                if y == len(self.piles[x])-1:
                    name = self.piles[x][y]
                    value = PhotoImage(file='images/'+self.piles[x][len(self.piles[x])-1]+".png")
                    setattr(self, name, value)
                    self.canvas.create_image(axis1, 300+top_card_length, anchor=NW, image=value, tag='pile'+str(x+1)+'_'+name)
                    self.canvas.tag_bind('pile'+str(x+1)+'_'+name, '<1>', self.on_click_pile)
                    axis1 += 170
                    axis2 += 170
                else:
                    name = self.piles[x][y]
                    value = PhotoImage(file='images/back_of_card.png')
                    setattr(self, name, value)
                    self.canvas.create_image(axis1, 300+top_card_length, anchor=NW, image=value, tag='pile'+str(x+1)+'_'+name)
                    self.canvas.tag_bind('pile'+str(x+1)+'_'+name, '<1>', self.on_click_pile)
                    top_card_length +=15
        return

    def shuffle_cards(self):
        list_of_cards = []
        while len(list_of_cards) != 28:
            num1 = random.randint(0,3)
            num2 = random.randint(0,12)
            if self.cards[num1][num2] not in list_of_cards and self.cards[num1][num2] != 0:
                list_of_cards.append(self.cards[num1][num2])
                self.cards[num1][num2] = 0
            else:
                continue
        counter = 0
        for row, val1 in enumerate(self.piles):
            for col, val2 in enumerate(val1):
                self.piles[row][col] = list_of_cards[counter]
                counter+=1
        for row, val1 in enumerate(self.cards):
            for col, val2 in enumerate(val1):
                if val2 != 0:
                    self.deck.append(val2)
                    self.cards[row][col] = 0
        for x in range(len(self.piles)):
            self.flipped_cards.append(self.piles[x][len(self.piles[x])-1])
        random.shuffle(self.deck)
        self.deckcard = self.deck[0]
        return

    def on_click_stack(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        stack = self.canvas.itemcget(item, 'tag').replace(' current', '').replace('img','')
        stack_info = self.get_stack_info(stack)
        stack_location = stack_info[0]-1
        card = self.highlighted_card
        pile_num = self.get_pile_info(card)
        pile_loc = pile_num-1 if pile_num else None
        top_card_of_pile = None if pile_loc == None else self.piles[pile_loc][len(self.piles[pile_loc])-1]
        if card != None and card not in self.stacks[stack_location] and (card == top_card_of_pile or card == self.deckcard):
            self.check_if_suits_match(stack)
            if self.check_if_game_over() == True:
                return
            self.deselect()
        else:
            self.deselect()
            self.highlighted_card = self.stacks[stack_location][len(self.stacks[stack_location])-1] if self.stacks[stack_location][len(self.stacks[stack_location])-1] != 0 else None
            self.canvas.itemconfig(stack, outline="yellow", width=5)
        return

    def check_if_game_over(self):
        if len(self.stacks[0]) == 13 and len(self.stacks[1]) == 13 and len(self.stacks[2]) == 13 and len(self.stacks[3]) == 13:
            self.deselect()
            msg = messagebox.askyesno("Player wins!", "Would you like to play again?")
            if msg == True:
                self.new_game()
            else:
                self.window.destroy()
            return True
        return False

    def check_if_suits_match(self, stack):
        card = self.highlighted_card.replace('0','')  #replace removes '0' from '10' cards so that the code works properly, as every other list-item is only 2 digits in length (ie: 9S, 7H, JD...)
        if stack == 'spades' and card[1] == 'S':
            self.check_if_card_comes_next(stack, card, 0, 'S')
        elif stack == 'hearts' and card[1] == 'H':
            self.check_if_card_comes_next(stack, card, 1, 'H')
        elif stack == 'diamonds' and card[1] == 'D':
            self.check_if_card_comes_next(stack, card, 2, 'D')
        elif stack == 'clubs' and card[1] == 'C':
            self.check_if_card_comes_next(stack, card, 3, 'C')
        return

    def check_if_card_comes_next(self, stack, card, stack_num, suit):
        last_card_in_stack =  self.stacks[stack_num][len(self.stacks[stack_num])-1]
        if self.stacks[stack_num][0] == 0 and card[0] != 'A':
            return
        elif self.stacks[stack_num][0] == 0 and card[0] == 'A':
            self.stacks[stack_num][0] = card
            self.add_to_stack(stack, card, suit)
        elif last_card_in_stack[0] == 'A' and card[0] == '2':
            self.stacks[stack_num].append(card) 
            self.add_to_stack(stack, card, suit)
        elif last_card_in_stack[0] == '9' and card[0] == '1':
            card = '10'+suit #10's are the only cards with 3 digits, so must be re-adjusted here to update the image properly
            self.stacks[stack_num].append(card) 
            self.add_to_stack(stack, card, suit)
        elif last_card_in_stack[0] == '1' and card[0] == 'J':
            self.stacks[stack_num].append(card) 
            self.add_to_stack(stack, card, suit)
        elif last_card_in_stack[0] == 'J' and card[0] == 'Q':
            self.stacks[stack_num].append(card) 
            self.add_to_stack(stack, card, suit)
        elif last_card_in_stack[0] == 'Q' and card[0] == 'K':
            self.stacks[stack_num].append(card) 
            self.add_to_stack(stack, card, suit)
        else:
            try:
                card_num = int(last_card_in_stack[0])
                if card_num + 1 == int(card[0]):
                    self.stacks[stack_num].append(card)
                    self.add_to_stack(stack, card, suit)
            except:
                return
        return

    def add_to_stack(self, stack, card, suit):
        get_loc = list(self.canvas.bbox(stack))
        get_loc[0] = get_loc[0]
        get_loc[1] = get_loc[1]
        self.canvas.delete(stack+"img")
        if suit == 'S':
            self.img_spades = PhotoImage(file='images/'+self.highlighted_card+".png")
            self.canvas.create_image(get_loc[0],get_loc[1], anchor=NW, image=self.img_spades, tag=stack+"img")
        elif suit == 'H':
            self.img_hearts = PhotoImage(file='images/'+self.highlighted_card+".png")
            self.canvas.create_image(get_loc[0],get_loc[1], anchor=NW, image=self.img_hearts, tag=stack+"img")
        elif suit == 'D':
            self.img_diamonds = PhotoImage(file='images/'+self.highlighted_card+".png")
            self.canvas.create_image(get_loc[0],get_loc[1], anchor=NW, image=self.img_diamonds, tag=stack+"img")
        elif suit == 'C':
            self.img_clubs = PhotoImage(file='images/'+self.highlighted_card+".png")
            self.canvas.create_image(get_loc[0],get_loc[1], anchor=NW, image=self.img_clubs, tag=stack+"img")    
        self.canvas.tag_bind(stack+"img", '<1>', self.on_click_stack)
        self.remove_card(card, None) #'None' goes here, b/c card doesn't come from a stack, but rather a pile
        return

    def remove_card(self, card, stack_card_info):
        if stack_card_info != None:
            pile_num = stack_card_info[0]+7
            list_location = stack_card_info[0]-1
            self.stacks[list_location].remove(card)
            get_loc = list(self.canvas.bbox(stack_card_info[1]+"img"))
            get_loc[0] = get_loc[0]+1
            get_loc[1] = get_loc[1]+1
            self.update_image(pile_num, list_location, get_loc)
        elif card in self.deck:
            self.on_click_boc(None)
            self.deck.remove(card)
        else:
            pile_num = self.get_pile_info(card)
            list_location = pile_num-1
            if len(self.piles[list_location]) > 1:
                self.piles[list_location].remove(card)
            else:
                self.piles[list_location].append(None)
                self.piles[list_location].remove(card)
            self.canvas.delete('pile'+str(pile_num)+'_'+card)
            get_loc = self.get_coordinates(pile_num)
            self.update_image(pile_num, list_location, get_loc)      
        return

    def update_image(self, pile, list_location, get_loc):
        imgfile = 'images/empty_pile.png' if self.piles[list_location][0] == None else 'images/'+self.piles[list_location][len(self.piles[list_location])-1]+".png"
        if pile <= 7:
            try:
                card_to_display = self.piles[list_location][len(self.piles[list_location])-1]
            except:
                card_to_display = None
            tag_info = 'pile'+str(pile)+'_'+'empty' if card_to_display == None else 'pile'+str(pile)+'_'+card_to_display
            name = card_to_display if card_to_display != None else 'pile'+str(pile)+'_empty'
            value = PhotoImage(file=imgfile)
            setattr(self, name, value)
            self.canvas.create_image(get_loc[0],285+(len(self.piles[list_location])*15), anchor=NW, image=value, tag=tag_info)
            self.canvas.tag_bind(tag_info, '<1>', self.on_click_pile)
            rect_length = 485+(len(self.piles[pile-1])*15) if len(self.piles[pile-1]) != 0  else 500
            self.canvas.coords('pile'+str(pile), get_loc[0],get_loc[1] ,get_loc[2] , rect_length)
            self.line_up_pile(pile)
            if card_to_display != None and card_to_display not in self.flipped_cards:
                self.flipped_cards.append(card_to_display)
        else:
            self.update_stack_image(get_loc, pile, list_location)
        return

    def update_stack_image(self, get_loc, pile, list_location):
        imgfile = 'images/'+self.stacks[list_location][len(self.stacks[list_location])-1]+".png"
        if pile == 8:
            self.spadesimg = PhotoImage(file=imgfile)
            self.canvas.create_image(get_loc[0],get_loc[1], anchor=NW, image=self.spadesimg, tag="spadesimg")
        elif pile == 9:
            self.heartsimg = PhotoImage(file=imgfile)
            self.canvas.create_image(get_loc[0],get_loc[1], anchor=NW, image=self.heartsimg, tag="heartsimg")
        elif pile == 10:
            self.diamondsimg = PhotoImage(file=imgfile)
            self.canvas.create_image(get_loc[0],get_loc[1], anchor=NW, image=self.diamondsimg, tag="diamondsimg")
        elif pile == 11:
            self.clubsimg = PhotoImage(file=imgfile)
            self.canvas.create_image(get_loc[0],get_loc[1], anchor=NW, image=self.clubsimg, tag="clubsimg")
        return

    def on_click_pile(self, event):
        card = self.highlighted_card
        clicked_pile = self.canvas.itemcget(self.canvas.find_closest(event.x, event.y),"tag")
        pile_num = int(clicked_pile[4])
        list_location = pile_num-1
        topcard = self.piles[list_location][len(self.piles[list_location])-1]
        stack = self.get_stack_info(card)
        if card != None and card[0] == 'K' and topcard == None:
            self.make_new_pile(card, list_location, pile_num, stack)
            return
        elif card != None and topcard != None and card != topcard:
            cards_to_move = self.get_cards_in_front(card)
            for x in cards_to_move:
                self.get_opposite_suits(x, topcard, pile_num, stack)
                topcard = self.piles[list_location][len(self.piles[list_location])-1]
            self.deselect()
            return
        self.deselect()
        self.canvas.itemconfig('pile'+str(pile_num), outline="yellow", width=5)
        clicked_card = clicked_pile.replace('pile'+str(pile_num)+'_', '').replace(' current', '') 
        self.highlighted_card = clicked_card if clicked_card in self.flipped_cards else None
        return

    def get_stack_info(self, item):
        stack = None
        if item == self.stacks[0][len(self.stacks[0])-1] or item == 'spades':
            stack = [1,'spades']
        elif item == self.stacks[1][len(self.stacks[1])-1] or item == 'hearts':
            stack = [2,'hearts']
        elif item == self.stacks[2][len(self.stacks[2])-1] or item == 'diamonds':
            stack = [3,'diamonds']
        elif item == self.stacks[3][len(self.stacks[3])-1] or item == 'clubs':
            stack = [4,'clubs']
        return stack

    def get_pile_info(self, card):
        pile = None
        if card in self.piles[0]:
            pile = 1
        elif card in self.piles[1]:
            pile = 2
        elif card in self.piles[2]:
            pile = 3
        elif card in self.piles[3]:
            pile = 4
        elif card in self.piles[4]:
            pile = 5
        elif card in self.piles[5]:
            pile = 6
        elif card in self.piles[6]:
            pile = 7
        return pile

    def attempt_move_card(self, card, topcard, suit1, suit2, pile_num, stack):
        num  = 2 if '10' in topcard else 1
        if topcard[num] == suit1 or topcard[num] == suit2:
            if card[0] == 'Q' and topcard[0] == 'K' :
                self.remove_card(card, stack)
                self.add_card_to_pile(topcard, card, pile_num)
                return True
            elif card[0] == 'J' and topcard[0] == 'Q':
                self.remove_card(card, stack)
                self.add_card_to_pile(topcard, card, pile_num)
                return True
            elif card[0] == '1' and topcard[0] == 'J' :
                self.remove_card(card, stack)
                self.add_card_to_pile(topcard, card, pile_num)
                return True
            elif card[0] == '9' and topcard[0] == '1':
                self.remove_card(card, stack)
                self.add_card_to_pile(topcard, card, pile_num)
                return True
            else:
                try:
                    if int(topcard[0])-1 == int(card[0]):
                        self.remove_card(card, stack)
                        self.add_card_to_pile(topcard, card, pile_num)
                        return True
                    else:
                        return False
                except:
                    return False
        return False

    def add_card_to_pile(self, topcard, card, pile_num):
        list_location = pile_num-1
        self.piles[list_location].insert(len(self.piles[list_location]),card)
        get_loc = self.get_coordinates(pile_num)
        self.update_image(pile_num, list_location, get_loc)
        self.deselect()
        return

    def get_opposite_suits(self, card, topcard, pile_num, stack):
        num  = 2 if '10' in card else 1
        if card[num] == 'S' or card[num] == 'C':
            suits = ['H','D']
        elif card[num] == 'D' or card[num] == 'H':
            suits = ['S','C']
        return self.attempt_move_card(card, topcard, suits[0], suits[1], pile_num, stack)

    def make_new_pile(self, card, list_location, pile_num, stack):
        cards_to_move = self.get_cards_in_front(card)
        get_loc = self.get_coordinates(pile_num)
        for item in cards_to_move:
            self.remove_card(item, stack)
            if self.piles[list_location][0] == None:
                self.piles[list_location][0] = item
            else:
                self.piles[list_location].append(item)
            self.update_image(pile_num, list_location, get_loc)
        self.deselect()
        return 

    def get_cards_in_front(self, card):
        list_of_cards = [card]
        break_switch = False
        for x, val1 in enumerate(self.piles):
            if break_switch == True:
                break
            for y, val2 in enumerate(val1):
                if val2 == card:
                    break_switch = True
                if break_switch == True and val2 not in list_of_cards:
                    list_of_cards.append(self.piles[x][y])
        return list_of_cards

    def check_delete_boc(self):
        if len(self.deck) <= 1:
            self.canvas.delete("back_of_card")
            self.canvas.delete("back_of_deck")
        return

    def on_click_boc(self, event):
        if self.first_flip == True:
            self.flip_first_card()
            return
        elif len(self.deck) == 1:
            self.canvas.delete('deckcard_img'+str(self.deckcard))
            self.canvas.delete('deck')
            return
        else:
            old_location = self.get_card_location_in_deck()
            new_location = old_location+1 if len(self.deck)-1 != old_location else 0
            self.deckcard = self.deck[new_location]
            self.deckimg = PhotoImage(file='images/'+self.deck[new_location]+".png")
            self.canvas.create_image(190,50, anchor=NW, image=self.deckimg, tag="deckcard_img"+str(self.deckcard))
            self.canvas.tag_bind("deckcard_img"+str(self.deckcard), '<1>', self.on_click_deck)
        return self.deselect()

    def on_click_deck(self,event):
        self.deselect()
        self.canvas.itemconfig("deck", outline="yellow", width=5)
        self.highlighted_card = self.deckcard
        return 

    def flip_first_card(self):
        self.deckcard = self.deck[0]
        self.canvas.create_rectangle(190, 50, 340, 250,  outline="darkgray", fill="lightgrey", tag="deck")
        self.canvas.tag_bind("deck", '<1>', self.on_click_deck)
        self.deckimg = PhotoImage(file='images/'+self.deck[0]+".png")
        self.canvas.create_image(190,50, anchor=NW, image=self.deckimg, tag="deckcard_img"+str(self.deckcard))
        self.canvas.tag_bind("deckcard_img"+str(self.deckcard), '<1>', self.on_click_deck)
        self.deckcard = self.deck[0]
        self.first_flip = False
        return self.deselect()

    def deselect(self):
        for item in self.canvas.find_all():
            item = self.canvas.itemcget(item, "tag").replace(' current','')
            try:
                self.canvas.itemconfig(item, outline="darkgray", width=1)
            except:
                continue
        self.highlighted_card = None
        self.check_delete_boc()
        return

    def get_card_location_in_deck(self):
        for x, val in enumerate(self.deck):
            if val == self.deckcard:
                return x
        return

    def line_up_pile(self, pile):
        get_loc = self.get_coordinates(pile)
        y_axis = 300
        for x in self.piles[pile-1]:
            if x == None:
                return
            b = self.canvas.itemcget('pile'+str(pile)+'_'+x, "tag")
            self.canvas.coords(b, get_loc[0], y_axis)
            y_axis += 15
        rect_length = 485+(len(self.piles[pile-1])*15) if len(self.piles[pile-1]) != 0  else 500
        self.canvas.coords('pile'+str(pile), get_loc[0],get_loc[1] ,get_loc[2] , rect_length)
        return

    def get_coordinates(self, pile):
        coords = None
        if pile == 1:
            coords = [20, 300, 170, 500]
        elif pile == 2:
            coords = [190, 300, 340, 500]
        elif pile == 3:
            coords = [360, 300, 510, 500]
        elif pile == 4:
            coords = [530, 300, 680, 500]
        elif pile == 5:
            coords = [700, 300, 850, 500]
        elif pile == 6:
            coords = [870, 300, 1020, 500]
        elif pile == 7:
            coords = [1040, 300, 1190, 500]
        return coords

Solitaire()
