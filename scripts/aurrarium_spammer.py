import praw
import prawcore
import re
import random

def split_file(category):  # splits contents of txt files in phrases folder into a list.
    f = open(f"phrases/{category.lower()}.txt","r").read()
    return f.split(" §\n")  # end of each phrase is marked by a space + section sign + line break

def gen_random_string(chars:list,len:int):
    return ''.join(random.choice(chars) for _ in range(len))

def parse_text(txt:str):  # applies & and % notation
    happy_emjs = "😁😀😂🤣😄🤩".split()       # used in &em_spam&
    sad_emjs = "😥😖😫☹😔😞😟😭😩".split()  # used in &sad_spam&
    anger_emjs = "😠😡🤬👿".split()            # used in &anger_spam&
    zero_width = ['​', '‍', '‌']                    # used in % notation

    sp_txt = txt.split(" ")
    for word in sp_txt:
        re.sub("&sd&","https://github.com/XatzClient/Sigma-Deleter",word)

def start_spam(event,values,window,reddit:praw.Reddit):
    print = lambda *args, **kwargs: window['-spammerOutput-'].print(*args, **kwargs)
    print("Starting Aurrarium now!")

    # checks to see if reddit instance is valid
    try:
        me = reddit.user.me()
    except:
        print("Hmm, there seems to be a problem with your login credentials. Please try again.")
        return
    
    print(f"Logged in as u/{me}")
    if (me.link_karma + me.comment_karma) < 100:
        print("Warning: Your karma level is below 100. As such, you account may not pass r/sigmaclient's karma threshold.",text_color='red')

    # looping thru all posts:
    target = reddit.subreddit("test")  # for testing purposes, will change to sigmaclient later
    for s in target.stream.submissions():
        pass  # WILL ADD SPAMBOT REPLY HERE

if __name__ == "__main__":
    start_spam(None,None,None,None)