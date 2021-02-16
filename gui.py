import PySimpleGUI as sg

sg.theme("Dark Amber")

login_frame_layout = [ [sg.Text("Logged in as:"),sg.Text("",k="-loggedInMsg-",size=(20,1))],
                       [sg.Text("Username",size=(10,1)),sg.Input("",k="-usernameInput-",size=(20,1),do_not_clear=False)],
                       [sg.Text("Password",size=(10,1)),sg.Input("",k="-passwordInput-",size=(20,1),do_not_clear=False)],
                       [sg.Text("User Agent",size=(10,1)),sg.Input("SigmaSpammer by u/Xianthu_Exists",k="-uAgentInput-",size=(20,1))],
                       [sg.Text("Client ID",size=(10,1)),sg.Input("",k="-clidInput-",size=(20,1),do_not_clear=False)],
                       [sg.Text("Client Secret",size=(10,1)),sg.Input("",k="-clsecretInput-",size=(20,1),do_not_clear=False)],
                       [sg.Submit("Use This Account",k="-loginButton-",size=(21,1),)] ]

select_phrase_layout = [ [] ]

layout = [ [sg.Frame("Login",login_frame_layout)] ]

window = sg.Window('SigmaSpammer', layout, font=("Helvetica", 12))
while True:  # Event Loop
    event, values = window.read()
    print(values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == "-loginButton-":
        window["-loggedInMsg-"].Update(values["-usernameInput-"])

window.close()