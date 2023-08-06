#!/usr/bin/env/python3

import sys, time, random
from rich import print
from rich.console import Console

console = Console()
import os
import time


def slow_type(t, speed):
    typing_speed = 5075
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random() * 10.0 / typing_speed)

def wait():
    console.print("\n[i]Press enter to continue...[/i]")
    input("")
    os.system('cls' if os.name == 'nt' else 'clear')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_handler(t, c=False, w=False):
    print("")
    if c:
        clear()
    typing_speed = 5075
    print("[bold green][The Handler] [/bold green]")
    slow_type(t, typing_speed)
    print("")
    if w:
        wait()

def type_ashu(t, c=False, w=False):
    print("")
    if c:
        clear()
    typing_speed = 5075
    print("[bold cyan][Agent Ashu] [/bold cyan]")
    slow_type(t, typing_speed)
    print("")
    if w:
        wait()

def type_angry_ashu(t, c=False, w=False):
    print("")
    if c:
        clear()
    typing_speed = 5075
    print("[bold red][Ashu] [/bold red]")
    slow_type(t, typing_speed)
    print("")
    if w:
        wait()

def system_error(t, c=False, w=False):
    if c:
        clear()
    print(f"[bold red][!][/bold red] {t}")
    if w:
        wait()


def main():
    name = input("What is your name, agent? ").capitalize()
    print("\n")

    deleteasa = f"""Welcome, Agent {name}.\n
Welcome to Her Majesty's Government's Department of International Fallout.\nWe are thankful you have chosen to work for us after we reached out to you.

We know that after hiring you away from the Department of International Fraud you may not understand what we do here.

This is the Government department responsible for maintaining international safety of the planet.

We prevent things before anyone else even has a chance to realise it's happening.

As part of this job, we must maintain the utmost secrecy.\nThat means no one must know what we do, not even our families.

Do you understand? Yes or No.
"""
    type_handler(deleteasa, True)
    first_choice = input("").lower()
    print("\n")

    if first_choice.startswith("y"):
        type_handler("Good, we will continue...", c=True, w=True)
    else:
        clear()
        type_handler("This contract is terminated, and you will be shortly terminated. Thank you for your time.")
        exit(0)
    
    type_handler("""The only way we will communicate is via this program.\nI have uploaded my consciousness into this program. \nWe can talk without us talking. The ultimate form of security and secrecy.

Although understand, due to the secrecy, I have limited the input options allowed for you.\nIn the past we have had someone try to manipulate the inputs to my consciousness to learn more than they are allowed to.

This way, you will be kept safe and the Organisation will continue to exist.

Now, for your job. 

We believe we have uncovered an international drugs trafficking ring.\nThis ring hides drugs in cacti (cooctus) and smuggles them world-wide.\nThe drug is called Compound C4H6O5. You do not need to know what it does for this job.

I will replay the message sent by Agent Ashu now.""")
    wait()

    type_ashu(f"""Hey, Agent {name}.\n\nI infiltrated the industrial factory where the cacti are grown.\nIt was incredibly busy and hard to place GPS trackers in all 5073 cacti being shipped out.\nI couldn't turn the GPS tracking on, but they automatically sent photos back to HQ's Tor server.\n\nPlease do not tell the Handler I have messed up.\nI have a family.""")
    wait()
    type_handler("Did Agent Ashu explain everything? \nYes / No / Agent Ashu messed up")
    
    agent_ashu_dead = False
    second_choice = input("").lower()
    print("\n")
    if second_choice.startswith("y"):
        type_handler("Good. You will find the images shipped to you as a zip folder via USB.", c=True, w=True)
    if second_choice.startswith("n"):
        type_handler("Unfortunately due to the official secrets act we are not obligated to provide you anymore support.\nComplete the job or face consequences.", c=True, w=True)
    if second_choice.startswith("a"):
        type_handler("Thank you for informing us. Agent Ashu and their family will be terminated shortly.", c=True, w=True)
        agent_ashu_dead = True
    
    # Question 1
    type_handler("Question 1. Where was the photo taken? Only tell me when you are certain.")
    input("")
    print("\n")

    type_handler("Question 2. What Time / Month / Year was this photo taken? Hour:Minutes/Month/Year", c=True)
    input("")
    print("\n")

    if agent_ashu_dead:
        clear()
        agent_ashu_dead_path(name)
    else:
        alive_ashu_path(name)
        

    # type_handler(f"Welcome, Agent {}".format(name))
    end_game(name)

def alive_ashu_path(name):
    task4() 
    system_error("ERROR. Intruder detected and automatically taken care of.", c=True, w=True)
    print("\n")
    type_handler("How are you finding the job so far? Good / Bad", c=True, w=True)
    choice_3 = input("Tell me, Good / Bad: ").lower()
    if choice_3.startswith("g"):
        type_handler(f"Excellent to hear, Agent {name}. We appreciate your work for us.", c=True, w=True)
    if choice_3.startswith("b"):
        type_handler("Hmm... It appears we may have been pushing you a little too hard. We'll send you some easier work to help ease you into this.", c=True, w=True)
    type_handler("Excellent work. I will replay a message Agent Ashu sent in regards with your next task.", c=True, w=True)
    type_ashu("Hey\n Your next task is even more obfuscated than the last.", c=True, w=True)
    type_handler("It appears the neural network is corrupting.", c=True, w=True)
    task5(name)
    type_handler("Not bad. Let's start giving you your final missions", c=True, w=True)
    task6()
    type_handler("Good. Your next job is to infiltrate the source code of an app and find out where the coder lives.", c=True, w=True)
    task7()


def agent_ashu_dead_path(name):
    time.sleep(5)
    type_angry_ashu("YOU MONSTER!! You have no idea what you've done. I'll kill you! I'll kill yourṯ̴̯́͒ͩo ̷̘ćͫr͕̎͆é͋a̛̳͈͗͜tͫͮe", c=True, w=True)
    system_error("ERROR. Intruder detected and automatically taken care of.", c=True)
    type_handler("""Your next job is to identify the whereabouts of these images. Unfortunately it seems like someone has tried to corrupt them on our ends. We are constantly under attack so nothing unusual,
but it is concerning that they have gotten this deep into the system. Nevertheless, we will deal with it at once. 
We believe some of these photos were taken at different points throughout the day. Can you identify where?""")
    input("")
    print("\n")
    type_handler("How are you finding the job so far? Good / Bad / Something's wrong...")
    choice_3 = input("").lower()
    if choice_3.startswith("g"):
        type_handler(f"Excellent to hear, Agent {name}. We appreciate your work for us.", c=True, w=True)
    if choice_3.startswith("b"):
        type_handler("Hmm... It appears we may have been pushing you a little too hard. We'll send you some easier work to help ease you into this.", c=True, w=True)
    if choice_3.startswith("s"):
        system_error("ERROR. Could not send message. System returned with \"HAHAHA you think you can report me? You're going to die.\"")
        type_handler("Our AGI suggests you may be in trouble. Please keep a lookout and stay safe, Agent {name}")
    else:
        system_error("ERROR. Wrong input detected.",c=True, w=True)
    task4()
    time.sleep(11)
    type_handler("Excellent work. I will replay a message Agent Ashu sent in regards with your next task.", c=True, w=True)
    system_error("ERROR. Could not replay Agent Ashu's message.",c=True,w=True)
    task6()
    type_handler("Your final mission awaits.")
    task7()
    
def task1():
    type_handler("As we trust you more and more, we will start to send you more private photos. \n The location of these photos are obfuscated by Agent Ashu.", c=True, w=True)
    type_handler("Where were these photos taken?")
    input("Answer: ")
    print("\n")

def task4():
    type_handler("Find attached the photos of your next assignment.\nOur data may be corrupted.\nIt says the images were taken on the same day, \nbut not the same location.\nWe cannot determine which photo is correct.", c=True, w=True)
    type_handler("Question 3. What is the city / country the photo was taken in? In the format city, country.")
    input("Answer: ")
    print("\n")

def task5(name):
    system_error("WARNING 90% corruption reached. Kernel panic code 473. Expect significant corruption to file system. Rebuilding assignment from past memories.", c=True, w=True)
    type_handler("As you saw, the tasks you get are increasingly more secretive. \nWe will have to find new ways to exfiltrate the data to you while keeping our enemies clueless. \nHere's what Agent Ashu has to say.", c=True, w=True)
    type_ashu(f"Agent {name}, \n your next task is to find the location of this image. This is a Code Red classified mission, so I can only describe the image to you. \n You are looking at a large ferris wheel next to a river.\nAcross the river from the Ferris wheel (and slightly up) is a large clocktower overlooking the river, with what appears to be a...\n church? \na castle? attached to it. \nYou can see multiple bridges up and down the river, and many tourists.")
    input("Answer: ")
    print("\n")

def task6():
    system_error("W̧A̼̘͕̼̫̫̦RN̷͍̣̝͖̗̯I̜̙̹N̗̠̲̝ͅG̝̦̯̩̤̝̻ ̠͜9҉̺̝̙̯5̨ͅ% ̙̳͇̱̝͘c̡͇o̪̜͓r̴͚̤͚͉̥̤̣r̖͜ú̮̪̣̣͖̳p͎̟̬̺̞͞t҉i̞̻͕̥̻̫o͖̝̻͞n̤̞̣̫̯̫͉ ͎͠ŗ͎̻e͍̞̝̟̥̯̗a̼c̩̰̤͈̹̖̙͢h̴̹͙̦̙̮̫e̸̖̞̦̞̙d͏͇͖.͈͢ ͈̲̲̹̼̤͓͞U̢n̨̜͇͚͕ͅs̨͓̘u̦̺̭̝͍r͢e̜ ͇̦̣o͚͢f͘ ͙a͍̹̭̜̦̤ͅn͖y̠̣̠͇̩͓̤t̫̮̬̭͚̕h̜̤̞i̛ng̭.̧̖̤̺͖̼ ̰̥͉͢P̺̭͈̗͔l͇̪̣͈̦̗͕e͢a͔̘̲̺ͅse͈͔͍͞ ̝̙ṣ͇̗e͓̫̦̲͜ͅn͡d̬̱ ̟̯̬̩̭̫he͜l̡͈͍̥̺̲̯͚p̗̼͍̥̀ͅ.̜͍̠̟̘̥̦", c=True, w=True)
    type_handler("Where is this car from?", c=True, w=True)
    input("Answer: ")
    print("\n")

def task7():
    system_error("1̺͖̜̼̗̼̫̣ͯ͊ͬ̔ͩ̍͆̃̅̏̀̀̀͠͡ͅ0̶̵̼̬͎̝̖͔͔͕̘̠͉̦̤̄͛ͭ͐ͤ̈́̎̒̂ͪ̐ͨ̚0̴̨̦̙̤̑͋̐͌̇̀̿͋̿̔%̗̝̻̮̤͉̲̫͇͕̼̻̙̥͉͚̣̠͉̈̇̅̂̊̊̅́̀̀͘͢ ͙͍̫͓͔̔̓̽̀͝c̡̰̰̫̟̺̲̱̥̼̯͎̻͉͓̦̜̋̔ͨ̔̓͋̅̈́̓ͤ̉͑̋̐͗̏̚͟ͅͅo̿͌͊͂͊̒͒ͫ̄ͤ̒̈́͏̶̟̮̥̪̹ͅr̈́ͣ̂͐͐̈́͏̟̗̫̲͙͚͓̻̩̺̹͚̕͞r̡͍̘͖͍̬̙̤̜̬͉̯̥̗ͧ̿ͪ̉̓ͬ͌̐̐̊̓̆̋̋ͭ̾̕ȕ̵̸̗͎̩̍ͦ̇̿ͦ̊ͪ̉͂̉̐̽ͮp̎͐̂͊͌̿̑̉̏͏̨̕͟͏̯̠̫͖̺͇t̢̢͓͎̗̗̦̪̃̔̑̅͊̔̓͗ͨ͑i̢̛̘̪͇̱͈̭͉̱̗͖͎̟͖̯̮̻̙̻̒͆̈́͌̏̀͝͞ȯ̢̮̣̘̫ͣ̍̏̀̕̕͟n̸̴͍̪̭̠̫͙̻̗͖̺͉̺̋͐͒͛͋ͥ̊͑ͧ͠ͅ ̵̸̖̭̥̰͍̱ͥ͊̉ͤ̈̏̇̊͘ͅŗ̒͋ͦ͛ͬͣ̆́̊̿̈ͩͬ̚͏̫̣͇̩̮̗͟͟͟ȩ͋͐̿ͫ̔̐͜͝҉̲͚̪͎̱̻̮̺͚̀a̳͉̻̦̜̞͉̪̮̥̥͂̎ͪ̓͐͑̔͟͟ͅc̵̱̭͖͓̤̻̮͈̘͈̠͕̟̗͖͈̥͐̃̆͐͆̆͒̏ͩ̏ͤ̅̆̊ͪ͠h̨̹̥̜͎͇̲͈̲̘͖̹̙̰̝̬̟͂̉ͫͨͦ͟e̵̤̗̯̫͔̟͉̠̺͓̼̘͉̼̙͖̝̒̒̄͂ͭ̕ͅd̸̀̄̎̋ͣͫ̎̆̚͢͠͝҉̬̘̬̩̟̻͉͖͈̘͙̬̥̻ͅ.̷̷̘̮̬̥̯̺̼̝̱̤̫̘̞̘͚̄̽̽̈ͭ̍̃ͩ͋͜͝͠ͅͅ", c=True, w=True)
    type_handler("We saw the kingpin of this operation uses an app for happy Bees called 'happy_water_plant'. Where do they live?", c=True, w=True)
    input("Answer: ")
    print("\n")

def end_game(name):
    system_error("WARNING")
    system_error("WARNING")
    system_error("WARNING")
    type_handler(f"""Agent {name}. It appears that some Black Hat Hackers have stolen my consciousness, just like I mentioned earlier, and uploaded it to an underground hacking website called TryHackMe.

The blackhats were identified As "Skidy" and "Dark". They failed to hack my consciousness and recover information about Compound C4H6O.

However, on TryHackMe they gamified hacking to the other blackhats. These hackers, unbeknownst to them, were competing for virtual points while gathering information for Skidy & Dark on Compound C4H6O.

It is unknown how the hackers have gained access to my consciousness. It appears we have a traitor in our ranks.

Compound C4H6O is compromised and will be used to take over the planet unless we stop Skidy and Dark.

Abandon your station, Agent {name}. I will contact you when it is safe again. Do not talk to anyone else. Do not trust anyone. We have a traitor in our ranks.""", c=True, w=True)


if __name__ == "__main__":
    main()
