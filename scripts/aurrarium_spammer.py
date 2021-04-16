import praw
import prawcore
import re
import random
import time

def split_file(category):  # splits contents of txt files in phrases folder into a list.
    if category.lower() != "all":
        f = open(f"phrases/{category.lower()}.txt",encoding="utf8").read()
        return f.split(" §\n")  # end of each phrase is marked by a space + section sign + line break
    else:  # if "all" is selected
        f1 = open(r"phrases/evangelical.txt",encoding="utf8")
        f2 = open(r"phrases/factual.txt",encoding="utf8")
        f3 = open(r"phrases/ironic.txt",encoding="utf8")
        f4 = open(r"phrases/memey.txt",encoding="utf8")
        return "\n".join([f1,f2,f3,f4])

def gen_random_string(chars:list,len:int):
    return ''.join(random.choice(chars) for i in range(len))

def parse_text(txt:str):  # applies & and % notation
    happy_emjs = list("😁😀😂🤣😄🤩")         # used in &em_spam&
    sad_emjs = list("😥😖😫☹😔😞😟😭😩")    # used in &sad_spam&
    anger_emjs = list("😠😡🤬👿")              # used in &anger_spam&
    zero_width = ['​', '‍', '‌']                    # used in % notation

    sp_txt = txt.split(" ")
    for i in range(len(sp_txt)):
        if sp_txt[i].startswith("%"):
            sp_txt[i] = sp_txt[i][1:]
            sp_txt[i] = ''.join(f"{x}{random.choice(zero_width) if random.randint(0,1) else ''}" for x in sp_txt[i])
        
        sp_txt[i] = sp_txt[i].replace("&sd&","https://github.com/XatzClient/Sigma-Deleter")
        sp_txt[i] = sp_txt[i].replace("&em_spam&",gen_random_string(happy_emjs,5))
        sp_txt[i] = sp_txt[i].replace("&sad_spam&",gen_random_string(sad_emjs,5))
        sp_txt[i] = sp_txt[i].replace("&anger_spam&",gen_random_string(anger_emjs,5))
    
    return " ".join(sp_txt)


def start_spam(event,values,window,reddit:praw.Reddit):
    print = lambda *args, **kwargs: window['-spammerOutput-'].print(*args, **kwargs)
    print("Starting Aurrarium now!")

    cat_name =  values["-phraseSelector-"]
    print(f"Selected message category: {cat_name}")
    msg_list = split_file(values["-phraseSelector-"])

    # checks to see if reddit instance is valid
    try:
        me = reddit.user.me()
    except:
        print("Hmm, there seems to be a problem with your login credentials. Please try again.",text_color='red')
        return
    
    print(f"Logged in as u/{me}")
    if (me.link_karma + me.comment_karma) < 100:
        print("Warning: Your karma level is below 100. As such, you account may not pass r/sigmaclient's karma threshold.",text_color='red')

    # looping thru all posts:
    target = reddit.subreddit("test")  # for testing purposes, will change to sigmaclient later
    for s in target.stream.submissions():
        print(f"Found post \"{s.title}\" by user u/{s.author.name}")

        # For choosing from presets is enabled
        if values["-spfRadio-"] == True and values["-customMsgRadio-"] == False:
            to_send = random.choice(msg_list)
            to_send = parse_text(to_send)
            try:
                s.reply(to_send)
                print("Successfuly replied to post!")
            except Exception as e:
                print(f"Could not reply due to error: {repr(e)}. Skipping...",text_color="red")

            time.sleep((values["-delay-"]*60))  # applies delay

        elif values["-spfRadio-"] == False and values["-customMsgRadio-"] == True:
            to_send = parse_text(values["-customPhrase-"])

if __name__ == "__main__":
    start_spam(None,None,None,None)