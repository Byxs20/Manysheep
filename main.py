import re
import sys
import time
import ujson
import aiohttp
import asyncio
from src import GUI
from src import Sheep
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
        self.pushButton_2.clicked.connect(self.get_token)

    def is_Conform(self, text):
        return self.str_pattern.match(text)

    def get_id(self):
        if (text := self.lineEdit_3.text()) == "":
            QMessageBox.information(self, "温馨提示", "您输入的ID内容不能为空!", QMessageBox.Yes)
        elif self.is_Conform(text):
            return text
        else:
            QMessageBox.information(self, "温馨提示", "您输入的ID内容不规范!", QMessageBox.Yes)

    def get_token(self):
        if (text := self.plainTextEdit.toPlainText()) != "":
            return text
        elif (id := self.get_id()) is not None:
            try:
                token = Sheep.get_token(id)
            except Exception as e:
                QMessageBox.critical(self, "错误提示", f"{e}", QMessageBox.Yes)
                return None
            self.plainTextEdit.setPlainText(token)
            return token

    def get_number(self):
        if (text := self.lineEdit.text()) == "":
            QMessageBox.information(self, "温馨提示", "您输入的通关次数内容不能为空!", QMessageBox.Yes)
        elif self.is_Conform(text):
            return int(text)
        else:
            QMessageBox.information(self, "温馨提示", "您输入的通关次数内容不规范!", QMessageBox.Yes)

    def get_time(self):
        if (text := self.lineEdit_2.text()) == "":
            QMessageBox.information(self, "温馨提示", "您输入的通关时间内容不能为空!", QMessageBox.Yes)
        elif self.is_Conform(text):
            return text
        else:
            QMessageBox.information(self, "温馨提示", "您输入的通关时间内容不规范!", QMessageBox.Yes)

    def show_info(self, number, ret, timed):
        self.plainTextEdit_2.appendPlainText(f"[{time.strftime('%X', time.localtime())}] 发送 {number} 次, 成功 {sum(1 for i in ret if i)} 次, 花费时间：{timed}")
        self.pushButton.setEnabled(True)

    def start(self):
        # 判断是否输入框是否为空
        if (token := self.get_token()) is not None and (game_time := self.get_time()) is not None and (number := self.get_number()) is not None:
            global url, headers
            url, headers = Sheep.struct_params(game_time, token)

            # 开启多线程
            self.workThread = WorkThread(number)
            self.pushButton.setEnabled(False)
            self.workThread.end.connect(self.show_info)
            self.workThread.start()

class WorkThread(QtCore.QThread):
    end = QtCore.pyqtSignal(int, list, float)

    def __init__(self, number) -> None:
        super().__init__()
        self.number = number
        
    def run(self):
        t0 = time.time()
        ret = asyncio.run(main(self.number))
        timed = round(time.time() - t0, 4)
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