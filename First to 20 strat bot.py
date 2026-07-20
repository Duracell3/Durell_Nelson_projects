from random import randint
wins=0
losses=0
moves=[20,14,2,7,13,3,6,9,15,10,19,18]#Strat_bot will only ever choose these numbers

def choose_order():#Choosing a different order every time
  picker=randint(0,len(player_val)-1)
  val=player_val[picker]
  player_val.pop(picker)
  return val

def next_player(current_player):#Taking turns
  if current_player==3:
    return 1
  else:
    return current_player+1

for games in range(10000):#Let the games begin!!!
  player_turn=1
  total=0
  player_val=[1,2,3]
  strat_bot=choose_order()
  bot_1=choose_order()
  bot_2=choose_order()

  while total<20:#The game can't end until someone gets 20
    if player_turn==strat_bot:
      for num in range(12):
        if moves[num]==total+1 or moves[num]==total+2 or moves  [num]==total+3:
          total=moves[num]
          if total<20:
            player_turn=next_player(player_turn)
          break

    elif player_turn==bot_1:
      add=0
      while add==0:
        add=randint(1,3)
        if add+total>20 or (3+total>=20 and add+total!=20):
          add=0
        else:
          total+=add
          if total<20:
            player_turn=next_player(player_turn)

    else:#Bot_2's turn
      add=0
      while add==0:
        add=randint(1,3)
        if add+total>20 or (3+total>=20 and add+total!=20):
          add=0
        else:
          total+=add
          if total<20:
            player_turn=next_player(player_turn)


  if player_turn==strat_bot:#How well is strat_bot playing
    wins+=1
  else:
    losses+=1

#The results are in
print("Wins: "+str(wins))
print("Losses: "+str(losses))
if ((wins/(wins+losses))*100)%2==0 or ((wins/(wins+losses))*100)%2==1:
  print("Win percentage: "+str(int((wins/(wins+losses))*100))+"%")
else:
  print("Win percentage: "+str((wins/(wins+losses))*100)+"%")