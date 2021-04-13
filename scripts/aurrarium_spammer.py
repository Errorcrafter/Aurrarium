import praw
import prawcore

# def test():
#     print("this is a test")

# if __name__ == "__main__":
#     test()

def start_spam(event,values,window,reddit):
    print("Starting spam now!")

    try:
        reddit.user.me()
    except:
        print("Hmm, there seems to be a problem with your login credentials. Please try again.")
        return

if __name__ == "__main__":
    start_spam(None,None,None,None)