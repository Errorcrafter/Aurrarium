import praw
import prawcore


def start_spam(event,values,window,reddit : praw.Reddit):
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