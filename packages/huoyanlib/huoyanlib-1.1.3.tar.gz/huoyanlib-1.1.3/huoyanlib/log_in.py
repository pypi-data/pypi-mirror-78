def log_in_machine():
    import tkinter as tk
    import tkinter.messagebox
    import pickle

    window = tk.Tk()
    window.title('欢迎进入登陆器')
    window.geometry('450x300')
    canvas = tk.Canvas(window, height=300, width=500)
    canvas.pack(side='top')
    tk.Label(window, text='用户名:').place(x=100, y=150)
    tk.Label(window, text='密码:').place(x=100, y=190)
    var_usr_name = tk.StringVar()
    entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
    entry_usr_name.place(x=160, y=150)
    var_usr_pwd = tk.StringVar()
    entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
    entry_usr_pwd.place(x=160, y=190)

    def usr_log_in():
        usr_name = var_usr_name.get()
        usr_pwd = var_usr_pwd.get()
        try:
            with open('usr_info.pickle', 'rb') as usr_file:
                usrs_info = pickle.load(usr_file)
        except FileNotFoundError:
            with open('usr_info.pickle', 'wb') as usr_file:
                usrs_info = {'admin': 'admin'}
                pickle.dump(usrs_info, usr_file)
        if usr_name in usrs_info:
            if usr_pwd == usrs_info[usr_name]:
                tk.messagebox.showinfo(title='欢迎',
                                       message='欢迎登陆呀：' + usr_name)
            else:
                tk.messagebox.showerror(message='密码错误!再试试吧')
        elif usr_name == '' or usr_pwd == '':
            tk.messagebox.showerror(message='用户名或密码为空')
        else:
            is_signup = tk.messagebox.askyesno('欢迎', '您还没有注册，是否现在注册')
            if is_signup:
                usr_sign_up()

    def usr_sign_up():
        def signtowcg():
            nn = new_name.get()
            np = new_pwd.get()
            npf = new_pwd_confirm.get()
            try:
                with open('usr_info.pickle', 'rb') as usr_file:
                    exist_usr_info = pickle.load(usr_file)
            except FileNotFoundError:
                exist_usr_info = {}
            if nn in exist_usr_info:
                tk.messagebox.showerror('错误', '用户名已存在')
            elif np == '' or nn == '':
                tk.messagebox.showerror('错误', '用户名或密码为空')
            elif np != npf:
                tk.messagebox.showerror('错误', '密码前后不一致')
            else:
                exist_usr_info[nn] = np
                with open('usr_info.pickle', 'wb') as usr_file:
                    pickle.dump(exist_usr_info, usr_file)
                tk.messagebox.showinfo('欢迎', '注册成功')
                window_sign_up.destroy()

        window_sign_up = tk.Toplevel(window)
        window_sign_up.geometry('350x200')
        window_sign_up.title('注册')
        new_name = tk.StringVar()
        tk.Label(window_sign_up, text='用户名：').place(x=10, y=10)
        tk.Entry(window_sign_up, textvariable=new_name).place(x=150, y=10)
        new_pwd = tk.StringVar()
        tk.Label(window_sign_up, text='请输入密码：').place(x=10, y=50)
        tk.Entry(window_sign_up, textvariable=new_pwd, show='*').place(x=150, y=50)
        new_pwd_confirm = tk.StringVar()
        tk.Label(window_sign_up, text='请再次输入密码：').place(x=10, y=90)
        tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*').place(x=150, y=90)
        bt_confirm_sign_up = tk.Button(window_sign_up, text='确认注册',
                                       command=signtowcg)
        bt_confirm_sign_up.place(x=150, y=130)

    def usr_sign_quit():
        window.destroy()

    bt_login = tk.Button(window, text='登录', command=usr_log_in)
    bt_login.place(x=140, y=230)
    bt_log_up = tk.Button(window, text='注册', command=usr_sign_up)
    bt_log_up.place(x=210, y=230)
    bt_log_quit = tk.Button(window, text='退出', command=usr_sign_quit)
    bt_log_quit.place(x=280, y=230)
    window.mainloop()
