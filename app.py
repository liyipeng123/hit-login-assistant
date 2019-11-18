import json
import os
import time

import requests
import wx
from wx import adv
from wx import html
from wx import html2


def isNotLogin():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/78.0.3904.97 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        res = requests.get('https://v1.hitokoto.cn/?encode=json ', headers=headers)
        return False
    except Exception as e:
        return True


class APP(wx.App):
    def __init__(self):
        super().__init__()
        self.STATUS = False
        frame = MainFrame(parent=None, title="lyp123 - Labs")
        frame.SetIcon(wx.Icon("icon.jpg"))
        TaskBarIcon(frame)
        frame.Hide()


class HomePage(wx.Panel):
    def __init__(self, parent, browser):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/78.0.3904.97 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        if not os.path.exists('./cache/data.txt'):
            url = "http://202.118.253.94:8080/eportal/InterFace.do?method=logout"
            data = {
                "userIndex": "",
            }
            requests.post(url, data=data, headers=headers)

        super().__init__(parent)
        self.browser = browser
        self._browser = html2.WebView.New(self)
        self._browser.LoadURL(self.browser)
        sizer_hor = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ver = wx.BoxSizer(wx.VERTICAL)
        sizer_ver.Add(self._browser, 1, wx.EXPAND)

        self.SetSizer(sizer_hor)
        self.SetSizer(sizer_ver)

        self.Bind(html2.EVT_WEBVIEW_LOADED, self.updateUrl)

    def updateUrl(self, event):
        current_url = str(self._browser.GetCurrentURL())
        print("Current URL: ", current_url)
        data_index = current_url.find("wlanuserip")
        if data_index != -1:
            result = current_url[data_index:]
            file = open("./cache/data.txt", "w")
            dic = {
                'username': '',
                'password': '',
                'data': result
            }
            file.write(json.dumps(dic))
            file.close()
            print(result)


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(1100, 660))
        # # Panel and Tab
        self.panel = wx.Panel(self)
        self.tab = wx.Notebook(self.panel)
        # StatusBar
        status_bar = self.CreateStatusBar()
        self.SetStatusText("lyp123 - Labs")
        # Menu Toolbar
        self.menubar = wx.MenuBar()

        file_menu = wx.Menu()
        self.exit = file_menu.Append(wx.ID_EXIT, "Exit")
        self.Bind(wx.EVT_MENU, self.onClose, self.exit)

        edit_menu = wx.Menu()
        self.login = edit_menu.Append(wx.ID_SETUP, "Login")
        self.Bind(wx.EVT_MENU, self.onLogin, self.login)

        help_menu = wx.Menu()
        self.help = help_menu.Append(wx.ID_HELP, "Help")
        self.about = help_menu.Append(wx.ID_ABOUT, "About")
        self.Bind(wx.EVT_MENU, self.onHelp, self.help)
        self.Bind(wx.EVT_MENU, self.onAbout, self.about)
        self.menuElements([file_menu, edit_menu, help_menu], ["&File", "&Tools", "&Help"])

        # Sizing up Stuff
        sizer = wx.BoxSizer()
        sizer.Add(window=self.tab, proportion=1, flag=wx.EXPAND)
        self.panel.SetSizer(sizer)
        self.onHomeTab()
        self.SetMenuBar(self.menubar)
        self.Bind(html2.EVT_WEBVIEW_TITLE_CHANGED, self.onTitle)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Centre()
        self.Hide()

    def onTitle(self, event):
        self.Title = "lyp123 - " + event.GetString()

    def menuElements(self, menu_elements, menu_names):
        for i in range(len(menu_elements)):
            self.menubar.Append(menu_elements[i], menu_names[i])

    def onHomeTab(self):
        page = HomePage(self.tab, browser="http://202.118.253.94:8080/eportal/success.jsp")
        self.tab.AddPage(page, "HOME")

    def onHelp(self, event):
        helpDlg = HelpDlg(None)
        helpDlg.Show()

    def onLogin(self, event):
        pass

    def onAbout(self, event):
        wx.MessageBox('程序作者：李奕鹏\n最后更新日期：2019-11-18', "关于")

    def onClose(self, event):
        self.Hide()


class HelpDlg(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title="Help", size=(500, 400))
        html = wxHTML(self)
        html.SetPage(
            "<h2>使用帮助</h2>"
            "<p>请设置用户名密码，点击登录测试效果</P>"
            "<p>建议设置开机自启动</P>"
            "<p>V0.0.1 BY LYP123</P>"
        )


class wxHTML(wx.html.HtmlWindow):
    def OnLinkClicked(self, link):
        pass


class TaskBarIcon(wx.adv.TaskBarIcon):
    ICON = "icon.jpg"
    TITLE = "哈工大校园网辅助登录"

    def __init__(self, frame):
        self.frame = frame
        event = ''
        wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(wx.Icon(self.ICON), self.TITLE)  # 设置图标和标题
        self.Bind(wx.EVT_MENU, self.onAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.onExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onShowWeb, id=wx.ID_APPLY)
        self.Bind(wx.EVT_MENU, self.onLogin, id=wx.ID_EXECUTE)
        self.Bind(wx.EVT_MENU, self.onSetting, id=wx.ID_SETUP)
        self.Bind(wx.EVT_MENU, self.onHelp, id=wx.ID_HELP)
        self.run(event)

    def onAbout(self, event):
        wx.MessageBox('程序作者：李奕鹏\n最后更新日期：2019-11-18', "关于")

    def run(self,event):
        while True:
            if isNotLogin():
                if self.login(event) is False:
                    return
            else:
                break
            time.sleep(3)

    def onExit(self, event):
        wx.Exit()

    def onShowWeb(self, event):
        self.frame.Show()

    def onLogin(self, event):
        status = self.login(event)
        if status == 'success':
            self.ShowBalloon("Success", "登陆成功")

    def onSetting(self, event):
        TextFrame(self).Show(True)
        pass

    def onHelp(self, event):
        self.frame.onHelp(event)

    def login(self, event):
        file = open('./cache/data.txt', 'r')
        user_info = json.loads(file.read())
        if user_info['username'] == '' or user_info['password'] == '':
            self.ShowBalloon("Error", "未设置用户名密码")
            self.onSetting(event)
            return False
        data = {
            "userId": user_info['username'],
            "password": user_info['password'],
            "service": "",
            "queryString": user_info['data'],
            "operatorUserId": "",
            "passwordEncrypt": "false",
        }
        file.close()
        url = "http://202.118.253.94:8080/eportal/InterFace.do?method=login"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/78.0.3904.97 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(url, data=data, headers=headers)
        return response.json()['result']

    def CreatePopupMenu(self):
        menu = wx.Menu()
        for mentAttr in self.getMenuAttrs():
            menu.Append(mentAttr[1], mentAttr[0])
        return menu

    def getMenuAttrs(self):
        return [('登录', wx.ID_EXECUTE),
                ('设置', wx.ID_SETUP),
                ('帮助', wx.ID_HELP),
                ('关于', wx.ID_ABOUT),
                ('退出', wx.ID_EXIT)]


class TextFrame(wx.Frame):
    def __init__(self, frame):
        wx.Frame.__init__(self, None, -1, "用户名密码设置", size=(300, 150))
        panel = wx.Panel(self, -1)
        self.frame = frame

        self.SetMaxSize((300, 150))
        self.SetMinSize((300, 150))
        # 添加用户名 文本输入框
        userLabel = wx.StaticText(panel, -1, "用户名:")
        self.SetIcon(wx.Icon("icon.jpg"))
        self.userText = wx.TextCtrl(panel, -1, "", size=(200, -1))
        # 设置默认的插入点，整数索引，开始位置为0
        self.userText.SetInsertionPoint(0)

        button = wx.Button(panel, -1, "登录")
        self.Bind(wx.EVT_BUTTON, self.OnSave, button)
        button.SetDefault()

        # 添加密码 输入框
        passwordLabel = wx.StaticText(panel, -1, "密码:   ")
        self.passwordText = wx.TextCtrl(panel, -1, '', size=(200, -1), style=wx.TE_PASSWORD)
        # 用sizer控制界面布局
        sizer = wx.BoxSizer(wx.VERTICAL)
        h_box1 = wx.BoxSizer()
        h_box1.Add(userLabel, 0, wx.ALIGN_CENTER)
        h_box1.Add(self.userText, 0, wx.ALIGN_CENTER)
        h_box2 = wx.BoxSizer()
        h_box2.Add(passwordLabel, 0, wx.ALIGN_CENTER)
        h_box2.Add(self.passwordText, 0, wx.ALIGN_CENTER)
        sizer.Add(h_box1, 1, wx.ALIGN_CENTER)
        sizer.Add(h_box2, 1, wx.ALIGN_CENTER)
        sizer.Add(button, 1, wx.ALIGN_CENTER)
        panel.SetSizer(sizer)
        self.Center()

    def OnSave(self, event):
        file = open('./cache/data.txt', 'r')
        user_info = json.loads(file.read())
        file.close()
        user_info['username'] = self.userText.GetValue()
        user_info['password'] = self.passwordText.GetValue()
        file = open('./cache/data.txt', 'w')
        file.write(json.dumps(user_info))
        file.close()
        self.frame.onLogin(event)
        self.frame.run(event)
        self.Destroy()


def main():
    app = APP()
    app.MainLoop()


if __name__ == "__main__":
    main()
