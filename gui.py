import PySimpleGUI as sg
import praw      # this is here so i can initiate the Reddit instance and get account stats
import prawcore  # and this is here to make sure input credentials are valid
from datetime import datetime  # used in -statsAccAge- because yes

sg.theme("Dark Amber")  # colour scheme!

### ╔══════════════════════ FIRST TAB ══════════════════════╗ ###
###  ┏━━━━━━━━━━━━━━━━━━━━━━ TOP ROW ━━━━━━━━━━━━━━━━━━━━━━┓  ###
# LOGIN FRAME: connect your account here
login_frame_col = [ [sg.Text("Logged in as:"),sg.Text("",k="-loggedInMsg-",size=(20,1))],
                       [sg.Text("Username",size=(15,1)),sg.Input("",k="-usernameInput-",size=(25,1),do_not_clear=False)],
                       [sg.Text("Password",size=(15,1)),sg.Input("",k="-passwordInput-",size=(25,1),do_not_clear=False,password_char="•")],
                       [sg.Text("User Agent",size=(15,1)),sg.Input("Aurrarium by u/Xianthu_Exists",k="-uAgentInput-",size=(25,1))],
                       [sg.Text("Client ID",size=(15,1)),sg.Input("",k="-clidInput-",size=(25,1),do_not_clear=False,password_char="•")],
                       [sg.Text("Client Secret",size=(15,1)),sg.Input("",k="-clsecretInput-",size=(25,1),do_not_clear=False,password_char="•")],
                       [sg.Text("",size=(7,0)),sg.Submit("Use This Account",k="-loginButton-",size=(25,1))] ]

login_frame_layout = [ [sg.Column(login_frame_col,size=(400,220))] ]

# STATS FRAME: shows the connected account's info
stats_frame_col = [ [sg.Text("Your Account Info")],
                       [sg.Text("Username:"),sg.Text("",k="-statsUsername-",size=(20,1))],
                       [sg.Text("Post Karma:"),sg.Text("",k="-statsPostKarma-",size=(20,1))],
                       [sg.Text("Comment Karma:"),sg.Text("",k="-statsCommentKarma-",size=(20,1))],
                       [sg.Text("Created On:"),sg.Text("",k="-statsAccAge-",size=(20,1))],
                       [sg.Text("Has Premium:"),sg.Text("",k="-statsHasPrem-",size=(20,1))],
                       [sg.Text("Suspended:"),sg.Text("",k="-statsSuspended-",size=(20,1))], ]

stats_frame_layout = [ [sg.Column(stats_frame_col,size=(400,220))] ]

###  ┏━━━━━━━━━━━━━━━━━━━━━ BOTTOM ROW ━━━━━━━━━━━━━━━━━━━━━┓  ###
# SELECTION FRAME: select what to spam here
select_phrase_col = [ [sg.Radio("Select from Preset",group_id=1,k="-sfpRadio-",enable_events=True,default=True),
                          sg.Combo(["Memey","Evangelical","Advertisment"],k="-phraseSelector-",readonly=True)],
                         [sg.Radio("Custom Message",group_id=1,k="-customMsgRadio-",enable_events=True,default=False)],
                         [sg.Multiline(default_text="sigma balls lmao ez\n\ndownload this shit instead https://github.com/XatzClient/Sigma-Deleter",k="-customPhrase-",size=(40,5))] ]

select_phrase_layout = [ [sg.Column(select_phrase_col,size=(400,214))] ]

# HOT/NEW SELECTOR: select whether to sort through hot or new
hn_sel_col = [ [sg.Text("Sort By:"),sg.Radio("Hot",group_id=2,k="-hotRadio-"),sg.Radio("New",group_id=2,k="-newRadio-")] ]

hn_sel_layout = [ [sg.Column(hn_sel_col,size=(400,50))] ]

# CREDITS: yay attribution
credits_col = [ [sg.Text("Aurrarium v0.5b1\n" +
                        "Made by G1galovaniac\n" +
                        "Discord: macpherson#1415\n" +
                        "Guilded: guilded.gg/g1ga\n" +
                        "Reddit: /u/Xianthu_Exists\n" +
                        "GitHub: Errorcrafter")] ]

credits_layout = [ [sg.Column(credits_col,size=(400,130))] ]

# combines credits and h/n selector into a column on its own because sphagetti code
misc_col = [ [sg.Frame("Sorting",hn_sel_layout)],
                [sg.Frame("Credits",credits_layout)] ]

# this compiles all of the above into one window
layout = [ [sg.Frame("Login",login_frame_layout),sg.Frame("Account Stats",stats_frame_layout)],
           [sg.Frame("Select Phrase to Spam",select_phrase_layout),sg.Column(misc_col)] ]

window = sg.Window('Aurrarium', layout, font=("Helvetica", 12))  # Draws the window

while True:  # Event Loop
    event, values = window.read()
    print(event,values)  # here for logging purposes, may delete
    if event == sg.WIN_CLOSED or event == 'Exit':
        break  # breaks out of theloop when the winow is closed

    if event == "-loginButton-":  # initiates Reddit instance
        reddit = praw.Reddit(client_id=values["-clidInput-"],
                            client_secret=values["-clsecretInput-"],
                            password=values["-passwordInput-"],
                            user_agent=values["-uAgentInput-"],
                            username=values["-usernameInput-"])
        try:
            me = reddit.user.me()
        except (prawcore.exceptions.ResponseException,AttributeError) as e:  # here if invalid or empty
            window["-loggedInMsg-"].Update("Login credentials invalid")
            print(str(e))
        except Exception as e:
            window["-loggedInMsg-"].Update("Unexpected error!")  # here if things go all sorts of wrong and some other error occurs
            print(str(e))

        try:   # try block in case no values were input or login invalidd
            window["-loggedInMsg-"].Update(me)  # two ifferent text labels to tel you who you are because WHY NOT

            # updating stats panel
            window["-statsUsername-"].Update(me)
            window["-statsPostKarma-"].Update(me.link_karma)
            window["-statsCommentKarma-"].Update(me.comment_karma)
            accAge = datetime.fromtimestamp(me.created_utc).strftime("%d %b %Y UTC")
            window["-statsAccAge-"].Update(accAge)
            window["-statsHasPrem-"].Update(me.is_gold)
            window["-statsSuspended-"].Update(me.is_suspended)
        except (prawcore.exceptions.ResponseException,AttributeError):  # here if invalid or empty
            window["-loggedInMsg-"].Update("Login credentials invalid")
        except:
            window["-loggedInMsg-"].Update("Unexpected error!")  # here if things go all sorts of wrong and some other error occurs
        
    if event == "-sfpRadio-":
        window["-phraseSelector-"].Update(disabled=False)  # very bad way to toggle
        window["-customPhrase-"].Update(disabled=True)     # between using custom
    if event == "-customMsgRadio-":                        # phrases and presets.
        window["-phraseSelector-"].Update(disabled=True)   # also this comment layout
        window["-customPhrase-"].Update(disabled=False)    # only exists to annoy you.

window.close()  # closes the window once out of event loop
