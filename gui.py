import PySimpleGUI as sg
import praw

sg.theme("Dark Amber")

login_frame_layout = [ [sg.Text("Logged in as:"),sg.Text("",k="-loggedInMsg-",size=(20,1))],
                       [sg.Text("Username",size=(15,1)),sg.Input("",k="-usernameInput-",size=(25,1),do_not_clear=False)],
                       [sg.Text("Password",size=(15,1)),sg.Input("",k="-passwordInput-",size=(25,1),do_not_clear=False,password_char="•")],
                       [sg.Text("User Agent",size=(15,1)),sg.Input("Aurrarium by u/Xianthu_Exists",k="-uAgentInput-",size=(25,1))],
                       [sg.Text("Client ID",size=(15,1)),sg.Input("",k="-clidInput-",size=(25,1),do_not_clear=False,password_char="•")],
                       [sg.Text("Client Secret",size=(15,1)),sg.Input("",k="-clsecretInput-",size=(25,1),do_not_clear=False,password_char="•")],
                       [sg.Text("",size=(7,0)),sg.Submit("Use This Account",k="-loginButton-",size=(25,1),)] ]

select_phrase_layout = [ [sg.Radio("Select from Preset",group_id=1,k="-sfpRadio-",enable_events=True,default=True),
                          sg.Combo(["Memey","Evangelical"],k="-phraseSelector-",readonly=True)],
                         [sg.Radio("Custom Message",group_id=1,k="-customMsgRadio-",enable_events=True,default=False)],
                         [sg.Multiline(default_text="sigma balls lmao ez\n\ndownload this shit instead https://github.com/XatzClient/Sigma-Deleter",k="-customPhrase-",size=(40,5))] ]

layout = [ [sg.Frame("Login",login_frame_layout)],
           [sg.Frame("Select Phrase to Spam",select_phrase_layout)] ]

window = sg.Window('Aurrarium', layout, font=("Helvetica", 12))
while True:  # Event Loop
    event, values = window.read()
    print(event,values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == "-loginButton-":
        reddit = praw.Reddit(client_id=values["-clidInput-"],
                             client_secret=values["-clsecretInput-"],
                             password=values["-passwordInput-"],
                             user_agent=values["-uAgentInput-"],
                             username=values["-usernameInput-"])
        try:
            window["-loggedInMsg-"].Update(reddit.user.me())
        except:
            window["-loggedInMsg-"].Update("Login credentials invalid")
    if event == "-sfpRadio-":
        window["-phraseSelector-"].Update(disabled=False)
        window["-customPhrase-"].Update(disabled=True)
    if event == "-customMsgRadio-":
        window["-phraseSelector-"].Update(disabled=True)
        window["-customPhrase-"].Update(disabled=False)

window.close()