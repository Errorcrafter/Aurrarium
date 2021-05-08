import PySimpleGUI as sg
import praw      # this is here so i can initiate the Reddit instance and get account stats
import prawcore  # and this is here to make sure input credentials are valid
from datetime import datetime  # used in -statsAccAge- because yes
from aurrarium_spammer import start_spam  # To run the spammer
import threading  # Threading to prevent the gui from freezing up
import sys
import os

def get_phrases():
    files = []
    path = os.path.dirname(__file__) + '/../phrases'

    for file in os.listdir(path):
        if file.endswith(".txt"):
            filename = file[:-4]
            files.append(filename.capitalize())
    
    files.append("All")
    return files

def call_spammer(event,values,window,reddit):  # starts the spammer in another thread
    try:
        start_spam(event,values,window,reddit)
    except NameError:  # in case some dumb fuck forgets to enter their login
        pass
    except Exception as e:  # if shit goes horribly wrong
        sg.Print(repr(e))
    window.write_event_value('-THREAD-', '** DONE **')

def draw_gui():
    sg.theme("Dark Amber")  # colour scheme!

    ###   ═══════════════════════ IMPORTANT ══════════════════════   ###
    current_full_release = "0"     # change THIS every time there is a major update (overhaul, new feature, etc)
    current_minor_release = "6"    # change THIS every time there is a smaller update (bugfixes, etc)
    current_build = "14"            # change THIS every time there is a new commit or smth idfc

    ### ╔══════════════════════ SETTINGS TAB ══════════════════════╗ ###
    ###    ┏━━━━━━━━━━━━━━━━━━━━━━ TOP ROW ━━━━━━━━━━━━━━━━━━━━━━┓   ###
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

    stats_frame_layout = [ [sg.Column(stats_frame_col,size=(400,225))] ]

    ###    ┏━━━━━━━━━━━━━━━━━━━━━ BOTTOM ROW ━━━━━━━━━━━━━━━━━━━━━┓   ###
    # SELECTION FRAME: select what to spam here
    select_phrase_col = [ [sg.Radio("Select from Preset",group_id=1,k="-sfpRadio-",enable_events=True,default=True),
                        sg.Combo(get_phrases(),k="-phraseSelector-",readonly=True,default_value="Memey",disabled=False)],
                        [sg.Radio("Custom Message",group_id=1,k="-customMsgRadio-",enable_events=True,default=False)],
                        [sg.Multiline(default_text="%sigma %balls lmao ez\n\ndownload this shit instead &sd&",k="-customPhrase-",disabled=True,size=(40,7))] ]

    select_phrase_layout = [ [sg.Column(select_phrase_col,size=(400,220))] ]

    # HOT/NEW SELECTOR: select whether to sort through hot or new
    hn_sel_col = [ [sg.Text("Sort By:"),sg.Radio("Hot",group_id=2,k="-hotRadio-"),sg.Radio("New",group_id=2,k="-newRadio-",default=True),
                    sg.Text("Delay:"),sg.Spin([x / 10 for x in range(0, 200)],initial_value=6.0,k="-delay-"),sg.Text("mins")] ]

    hn_sel_layout = [ [sg.Column(hn_sel_col,size=(400,50))] ]

    # CREDITS: yay attribution
    version_col = [ [sg.Text(f"Aurrarium {current_full_release}.{current_minor_release}b{current_build}\n" +
                            "Made by G1galovaniac\n" +
                            "Note: If you paid for this software, you have been\n" +
                            "scammed. This is available on my GitHub profile\n" +
                            "at www.github.com/Errorcrafter")] ]

    version_col = [ [sg.Column(version_col,size=(400,130))] ]

    # combines stuff into MORE columns because alignment
    tab1_col_l = [ [sg.Frame("Login",login_frame_layout)],
                [sg.Frame("Select Phrase to Spam",select_phrase_layout)] ]
    tab1_col_r = [ [sg.Frame("Account Stats",stats_frame_layout)],
                [sg.Frame("Sorting",hn_sel_layout)],
                [sg.Frame("Version",version_col)] ]

    # this compiles all of the above into one tab
    tab1= [[sg.Column(tab1_col_l),sg.Column(tab1_col_r)]]

    ### ╔══════════════════════ SPAMMER TAB ══════════════════════╗ ###
    tab2 = [ [sg.Multiline(k="-spammerOutput-",size=(95,25),disabled=True)],
            [sg.Text("",size=(30,0)),sg.Button("Start Spam",k="-startSpam-",size=(30,None))] ]

    # Draws the window
    layout = [ [sg.TabGroup([[sg.Tab("Settings",tab1),sg.Tab("Spammer",tab2)]])] ]
    window = sg.Window(f'Aurrarium {current_full_release}.{current_minor_release}b{current_build}',  # version number in window heading
                    layout, font=("Tahoma", 12))  # font and layout

    while True:  # Event Loop
        event, values = window.read()
        sg.Print(event,values)  # here for logging purposes, may delete
        if event == sg.WIN_CLOSED or event == 'Exit':
            break  # breaks out of the loop when the winow is closed

        if event == "-loginButton-":  # initiates Reddit instance
            reddit = praw.Reddit(client_id=values["-clidInput-"],
                                client_secret=values["-clsecretInput-"],
                                password=values["-passwordInput-"],
                                user_agent=values["-uAgentInput-"],
                                username=values["-usernameInput-"],
                                praw8_raise_exception_on_me=True)
            try:
                me = reddit.user.me()
            except (prawcore.exceptions.ResponseException,AttributeError) as e:  # here if invalid or empty
                window["-loggedInMsg-"].Update("Login credentials invalid")
                sg.Print(repr(e))
            except praw.exceptions.ReadOnlyException as e:
                window["-loggedInMsg-"].Update("Login credentials invalid")
                sg.Print(repr(e))
            except Exception as e:
                window["-loggedInMsg-"].Update("Unexpected error!")  # here if things go all sorts of wrong and some other error occurs
                sg.Print(repr(e))

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
            except (prawcore.exceptions.ResponseException,AttributeError,praw.exceptions.ReadOnlyException):  # here if invalid or empty
                window["-loggedInMsg-"].Update("Login credentials invalid")
            except:
                window["-loggedInMsg-"].Update("Unexpected error!")  # here if things go all sorts of wrong and some other error occurs
            
        if event == "-sfpRadio-":
            window["-phraseSelector-"].Update(disabled=False)  # very bad way to toggle
            window["-customPhrase-"].Update(disabled=True)     # between using custom
        if event == "-customMsgRadio-":                        # phrases and presets.
            window["-phraseSelector-"].Update(disabled=True)   # also this comment layout
            window["-customPhrase-"].Update(disabled=False)    # only exists to annoy you.

        if event == "-startSpam-":  # executes code in aurrarium_spammer.py when this button is pressed
            # try:
            #     start_spam(event,values,window,reddit)
            # except NameError:  # in case some dumb fuck forgets to enter their login
            #     pass
            # except Exception as e:  # if shit goes horribly wrong
            #     sg.Print(repr(e))
            threading.Thread(target=call_spammer, args=(event,values,window,reddit), daemon=True).start()

    window.close()  # closes the window once out of event loop

if __name__ == "__main__":
    draw_gui()
    print("exiting...")
