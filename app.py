import requests
import wx
from wx import adv
from wx import html
from wx import html2


class APP(wx.App):
    def __init__(self):
        super().__init__()
        frame = MainFrame(parent=None, title="lyp123 - Eccentric Tensor Labs")
        frame.SetIcon(wx.Icon("icon.jpg"))
        TaskBarIcon(frame)
        frame.Hide()


class HomePage(wx.Panel):
    def __init__(self, parent, browser):
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

    def onEnter(self, event):
        self._urlbar.SetValue("")
        self._urlbar.AppendText(self._urlbar.Value)

    def updateUrl(self, event):
        current_url = str(self._browser.GetCurrentURL())
        print("Current URL: ", current_url)
        data_index = current_url.find("wlanuserip")
        if data_index != -1:
            result = current_url[data_index:]
            file = open("./cache/data.txt", "w")
            file.write(result)
            file.close()
            print(result)


class TabPage(wx.Panel):
    def __init__(self, parent, browser):
        super().__init__(parent)
        self._browser = browser


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
        file = open('./cache/data.txt', 'r')
        data = {
            "userId": "1170800716",
            "password": "6757421081",
            "service": "",
            "queryString": file.read(),
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

    def onAbout(self, event):
        wx.MessageBox('程序作者：李奕鹏\n最后更新日期：2019-11-18', "关于")

    def onClose(self, event):
        self.Hide()


class HelpDlg(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title="Help", size=(500, 400))
        html = wxHTML(self)
        html.SetPage(
            "<h2>lyp123<br>Help</h2>"
        )


class wxHTML(wx.html.HtmlWindow):
    def OnLinkClicked(self, link):
        pass


class TaskBarIcon(wx.adv.TaskBarIcon):
    ICON = "icon.jpg"
    TITLE = "哈工大校园网辅助登录"

    def __init__(self, frame):
        self.frame = frame
        wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(wx.Icon(self.ICON), self.TITLE)  # 设置图标和标题
        self.Bind(wx.EVT_MENU, self.onAbout, id=wx.ID_ABOUT)  # 绑定“关于”选项的点击事件
        self.Bind(wx.EVT_MENU, self.onExit, id=wx.ID_EXIT)  # 绑定“退出”选项的点击事件
        self.Bind(wx.EVT_MENU, self.onShowWeb, id=wx.ID_APPLY)  # 绑定“显示页面”选项的点击事件
        self.Bind(wx.EVT_MENU, self.onLogin, id=wx.ID_EXECUTE)  # 绑定“显示页面”选项的点击事件

    # “关于”选项的事件处理器
    def onAbout(self, event):
        wx.MessageBox('程序作者：李奕鹏\n最后更新日期：2019-11-18', "关于")

    # “退出”选项的事件处理器
    def onExit(self, event):
        wx.Exit()

    # “显示页面”选项的事件处理器
    def onShowWeb(self, event):
        self.frame.Show()

    def onLogin(self, event):
        if self.frame.onLogin(event) == 'success':
            self.ShowBalloon("Success", "登陆成功")

    # 创建菜单选项
    def CreatePopupMenu(self):
        menu = wx.Menu()
        for mentAttr in self.getMenuAttrs():
            menu.Append(mentAttr[1], mentAttr[0])
        return menu

    # 获取菜单的属性元组
    def getMenuAttrs(self):
        return [('登录', wx.ID_EXECUTE),
                ('关于', wx.ID_ABOUT),
                ('退出', wx.ID_EXIT)]


def main():
    app = APP()
    app.MainLoop()


if __name__ == "__main__":
    main()
