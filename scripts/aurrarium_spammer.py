import praw
import prawcore

# def test():
#     print("this is a test")

# if __name__ == "__main__":
#     test()

def start_spam(event,values,window,reddit):
    try:
        print("Starting Aurrarium now!")

        # checks to see if reddit instance is valid
        try:
            me = reddit.user.me()
        except:
            print("Hmm, there seems to be a problem with your login credentials. Please try again.")
            return
        
        print(f"Logged in as u/{me}")
        if (me.link_karma + me.comment_karma) < 100:
            print("Warning: Your karma level is below 100. As such, you account may not pass r/sigmaclient's karma threshold.")
    
    except Exception as e:
        print(repr(e))

if __name__ == "__main__":
    start_spam(None,None,None,None)