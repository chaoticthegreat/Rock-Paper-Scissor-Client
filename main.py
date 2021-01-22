import requests
from threading import Thread
import time, os, sys
totalwins = 0
quit = False
red = "\u001b[31m"
green = "\u001b[32m"
yellow = "\033[0;93m"
reset = "\u001b[0m"
logic = {"rock":"scissor","scissor":"paper","paper":"rock"}
def type(string:str):
  for char in string:
    sys.stdout.write(char)
    sys.stdout.flush()
    time.sleep(0.025)
  print()
def alive(username):
  while not quit:
    requests.post("https://Server-for-Online-Rock-Paper-Scissors.proryan.repl.co/check", json = {"username":username})
    time.sleep(4)
username = input("What's your username:\n")
Thread(target = alive, daemon = True, args = (username,)).start()
type("Please wait while we match you up with someone!\nFor a quicker match up, call a partner to play on a different computer!")
r = requests.get(f"https://Server-for-Online-Rock-Paper-Scissors.proryan.repl.co/{username}/false").json()
while r["match"] == "nothing":
  time.sleep(2)
  r = requests.get(f"https://Server-for-Online-Rock-Paper-Scissors.proryan.repl.co/{username}/true", json = {"server":r["server"]}).json()
while True:
  server = int(r["server"])
  type("Your server id is "+str(server))
  type("You are playing against "+r["match"])
  for i in range(1,4):
    time.sleep(3)
    os.system("clear")
    while True:
      choice = input("Pick an option:\n1. Rock\n2. Paper\n3. Scissor\n").lower()
      if choice in ["rock","1"]:
        choice = "rock"
        break
      elif choice in ["paper","2"]:
        choice = "paper"
        break
      elif choice in ["scissor","3"]:
        choice = "scissor"
        break
      else:
        type("Please pick a valid option!")
        continue
    requests.post("https://Server-for-Online-Rock-Paper-Scissors.proryan.repl.co/server", json = {"round":i,"username":username,"choice":choice,"server":server})
    type("Waiting for the other player to answer...")
    kicked = False
    while True:
      done = requests.get("https://Server-for-Online-Rock-Paper-Scissors.proryan.repl.co/server", json = {"round":i, "username":username,"server":server})
      if done.text == "Nothing":
          time.sleep(2)
      elif done.text == "kicked":
        if not kicked:
          os.system("clear")
          type("The other player left!")
          type("Finding you a new match...")
          kicked = True
      elif done.json()["1"] == "true":
        r = done.json()["0"]
        type("Found you a new match!")
        totalwins = 0
        break
      else:
        otherchoice = done.json()["0"]
        type(r["match"]+" picked "+otherchoice)
        if otherchoice == choice:
          type(f"{yellow}Tie!{reset}")
        elif logic[choice] == otherchoice:
          type(f"{green}You win!{reset}")
          totalwins+=1
        elif logic[otherchoice] == choice:
          type(f"{red}You lose!{reset}")
        break
    if done.json()["1"] == "true" or i == 3:
      breaktrue = True
      break
  if done.json()["1"] == "true":
      continue
  elif breaktrue:
    break
type(f"You won: {totalwins}/3")
quit = True