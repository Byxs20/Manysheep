import re
import sys
import time
import ujson
import aiohttp
import asyncio
from src import GUI
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

# PyInstaller 项目的 Issue #1113 有讨论到两种方法来避免出现 LookupError: unknown encoding: idna
import encodings.idna
u''.encode('idna')

class Main(QMainWindow, GUI.Ui_MainWindow):
    str_pattern = re.compile("^[0-9]*$")

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("./images/Logo.ico")) # 设置软件图标
        self.setFixedSize(self.width(), self.height()) # 禁止窗口最大化

        # 信号
        self.pushButton.clicked.connect(self.start)

    def get_token(self):
        if (text := self.plainTextEdit.toPlainText()) != "":
            return text.replace("\n", "")
        QMessageBox.information(self, "温馨提示", "您输入的内容为空!", QMessageBox.Yes)

    def get_number(self):
        if (text := self.lineEdit.text()) == "":
            QMessageBox.information(self, "温馨提示", "您输入的通关次数内容不能为空!", QMessageBox.Yes)
        elif self.str_pattern.match(text):
            return int(text)
        else:
            QMessageBox.information(self, "温馨提示", "您输入的通关次数内容不规范!", QMessageBox.Yes)

    def get_time(self):
        if (text := self.lineEdit_2.text()) == "":
            QMessageBox.information(self, "温馨提示", "您输入的通关时间内容不能为空!", QMessageBox.Yes)
        elif self.str_pattern.match(text):
            return text
        else:
            QMessageBox.information(self, "温馨提示", "您输入的通关时间内容不规范!", QMessageBox.Yes)

    def show_info(self, number, ret, timed):
        QMessageBox.information(self, "温馨提示", f"期待发送：{number}次，成功发送：{sum(1 for i in ret if i)}，花费时间：{timed}", QMessageBox.Yes)

    def start(self):
        # 判断是否输入框是否为空
        if (token := self.get_token()) is not None and (game_time := self.get_time()) is not None and (number := self.get_number()) is not None:
            global url, headers
            url = f"http://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=1&rank_time={game_time}&rank_role=1&skin=1"

            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; HD1900 Build/QKQ1.190716.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3263 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/146 MicroMessenger/8.0.16.2040(0x28001037) Process/appbrand2 WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android",
                "t": token,
                "referer": "https://servicewechat.com/wx141bfb9b73c970a9/20/page-frame.html",
            }
            
            self.workThread = WorkThread(number)
            self.workThread.end.connect(self.show_info)
            self.workThread.start()

class WorkThread(QtCore.QThread):
    end = QtCore.pyqtSignal(int, list, float) # 计数完成后发送一个信号

    def __init__(self, number) -> None:
        super().__init__()
        self.number = number
        
    def run(self):
        t0 = time.time()
        ret = asyncio.run(main(self.number))
        timed = round(time.time() - t0)
        self.end.emit(self.number, ret, timed)

async def get(url):
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(url, headers=headers, timeout=3) as response:
                response = await response.text()
                return ujson.loads(response)["err_code"] == 0
        except asyncio.exceptions.TimeoutError:
                return False

async def main(number):
    return await asyncio.gather(*[get(url=url) for _ in range(number)])

if __name__ == "__main__":
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) # DPI自适应
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    sys.exit(app.exec_())