import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSplitter,\
    QComboBox, QLabel, QSpinBox, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QPixmap, QPainter, QPoint, QPaintEvent, QMouseEvent, QPen, QColor, QSize, QCursor
from PyQt5.QtCore import Qt
from CI import Ui_MainWindow
import datetime
import glob
import win32gui

CurFolder = os.getcwd()
DefaultImFolder = CurFolder
NowTime = datetime.datetime.now()
Month = str(NowTime.month).zfill(2)
Day = str(NowTime.day).zfill(2)
Hour = str(NowTime.hour).zfill(2)
Minute = str(NowTime.minute).zfill(2)


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.setMouseTracking(True)
        self.imglist = []
        self.ImgFolder = ''
        self.CurImg = ''

        #新建QPixmap作为画板，尺寸为__size
        self.__board = QPixmap()
        self.__board.fill(Qt.white) #用白色填充画板

        self.__IsEmpty = True  # 默认为空画板
        self.EraserMode = False  # 默认为禁用橡皮擦模式

        self.__lastPos = QPoint(0, 0)  # 上一次鼠标位置
        self.__currentPos = QPoint(0, 0)  # 当前的鼠标位置

        self.__painter = QPainter()  # 新建绘图工具

        self.__thickness = 10  # 默认画笔粗细为10px
        self.__penColor = QColor("black")  # 设置默认画笔颜色为黑色
        self.__colorList = QColor.colorNames()  # 获取颜色列表

        # 按键信号与回调函数连接
        self.OpenDir.clicked.connect(self.OpenDirBntClicked)
        self.NextImg.clicked.connect(self.NextImBntClicked)
        self.LastImg.clicked.connect(self.PreImBntClicked)
        self.SaveImg.clicked.connect(self.on_btn_Save_Clicked)
        self.PenThicknessSpinBox.valueChanged.connect(self.on_PenThicknessChange)
        # self.NextImg.clicked.connect(self.NextImBntClicked)

    #########选择图片文件夹#########
    def OpenDirBntClicked(self):
        self.ImgFolder = QtWidgets.QFileDialog.getExistingDirectory(None, "select folder", DefaultImFolder)  # 这个语句有些邪门
        if self.ImgFolder != '':
            ImNameSet = os.listdir(self.ImgFolder)
            self.imglist = glob.glob(self.ImgFolder + '/*.jpg')
            print(self.imglist)
            print(ImNameSet)
            ImNameSet.sort()
            # ImPath = os.path.join(ImFolder, ImNameSet[0])
            ImPath = os.path.join(self.ImgFolder, ImNameSet[1])
            # pix = QtGui.QPixmap(ImPath)
            # self.ImgShowLabel.setPixmap(pix)


            # 画板
            # self.__board = QtGui.QPixmap(r'C:\Users\49942\Pictures\Saved Pictures\t2.jpg')
            self.__board = QtGui.QPixmap(self.imglist[0])
            self.__board = self.__board.scaled(500,500)
            # self.__IsEmpty = True  # 默认为空画板
            # self.EraserMode = False  # 默认为禁用橡皮擦模式
            #
            # self.__lastPos = QPoint(0, 0)  # 上一次鼠标位置
            # self.__currentPos = QPoint(0, 0)  # 当前的鼠标位置
            #
            # self.__painter = QPainter()  # 新建绘图工具
            #
            # self.__thickness = 5  # 默认画笔粗细为10px
            # self.__penColor = QColor("black")  # 设置默认画笔颜色为黑色
            # self.__colorList = QColor.colorNames()  # 获取颜色列表

            # 界面标题
            self.ImNameSet = ImNameSet
            self.CurImId = 0
            _, SelectFolderName = os.path.split(self.ImgFolder)
            CopyImFolderName = 'From{}CopyIm_{}-{}-{}-{}'.format(SelectFolderName, Month, Day, Hour, Minute)
            self.CopyImFolder = os.path.join(CurFolder, CopyImFolderName)

            _translate = QtCore.QCoreApplication.translate
            CurWinTitle = "检测工具                                                " + \
                          "                                                             " + \
                          SelectFolderName + '\\' + ImNameSet[0]
            self.setWindowTitle(_translate("MainWindow", '审查工具 '+self.imglist[0]))
        else:
            print('请重新选择文件夹')

    #########显示下一张图片 #########
    def NextImBntClicked(self):
        ImFolder = self.ImgFolder
        # ImNameSet = self.ImNameSet
        CurImId = self.CurImId
        ImNum = len(self.imglist)
        if CurImId < ImNum - 1:  # 不可循环看图
            ImPath = os.path.join(ImFolder, self.imglist[CurImId + 1])
            self.__board = QtGui.QPixmap(self.imglist[CurImId + 1])
            self.__board = self.__board.scaled(500, 500)
            self.update()
            # self.ImgShowLabel.setPixmap(pix)
            self.CurImId = CurImId + 1

            _, SelectFolderName = os.path.split(ImFolder)
            _translate = QtCore.QCoreApplication.translate
            CurWinTitle = "审查图片                                                " + \
                          "                                                             " + \
                          SelectFolderName + '\\'
            self.setWindowTitle(_translate("MainWindow", self.imglist[CurImId + 1]))

    #########显示前一张图片 #########
    def PreImBntClicked(self):
        ImFolder = self.ImgFolder
        ImNameSet = self.ImNameSet
        CurImId = self.CurImId
        ImNum = len(self.imglist)
        if CurImId > 0:  # 第一张图片没有前一张
            ImPath = os.path.join(ImFolder, ImNameSet[CurImId - 1])
            self.__board = QtGui.QPixmap(self.imglist[CurImId - 1])
            self.__board = self.__board.scaled(500,500)
            self.update()
            # self.ImgShowLabel.setPixmap(pix)
            self.CurImId = CurImId - 1

            _, SelectFolderName = os.path.split(ImFolder)
            _translate = QtCore.QCoreApplication.translate
            CurWinTitle = "看图工具1.0                                                " + \
                          "                                                             " + \
                          SelectFolderName + '\\'
            self.setWindowTitle(_translate("MainWindow", self.imglist[CurImId - 1]))
        if self.CurImId < 0:
            self.CurImId = 0

    def Clear(self):
        # 清空画板
        self.__board.fill(Qt.white)
        self.update()
        self.__IsEmpty = True

    def ChangePenColor(self, color="black"):
        # 改变画笔颜色
        self.__penColor = QColor(color)

    def ChangePenThickness(self, thickness=10):
        # 改变画笔粗细
        self.__thickness = thickness

    def IsEmpty(self):
        # 返回画板是否为空
        return self.__IsEmpty

    def GetContentAsQImage(self):
        # 获取画板内容（返回QImage）
        image = self.__board.toImage()
        return image

    def paintEvent(self, paintEvent):
        # 绘图事件
        # 绘图时必须使用QPainter的实例，此处为__painter
        # 绘图在begin()函数与end()函数间进行
        # begin(param)的参数要指定绘图设备，即把图画在哪里
        # drawPixmap用于绘制QPixmap类型的对象
        self.__painter.begin(self)
        # 0,0为绘图的左上角起点的坐标，__board即要绘制的图
        self.__painter.drawPixmap(0, 0, self.__board)
        self.__painter.end()

    def mousePressEvent(self, mouseEvent):
        # 鼠标按下时，获取鼠标的当前位置保存为上一次位置
        self.__currentPos = mouseEvent.pos()
        self.__lastPos = self.__currentPos

    def mouseMoveEvent(self, mouseEvent):
        # 鼠标移动时，更新当前位置，并在上一个位置和当前位置间画线
        self.__currentPos = mouseEvent.pos()

        if mouseEvent.buttons() == QtCore.Qt.LeftButton:
            self.__painter.begin(self.__board)

            if self.EraserMode == False:
                # 非橡皮擦模式
                self.__painter.setPen(QPen(self.__penColor, self.__thickness))  # 设置画笔颜色，粗细
            else:
                # 橡皮擦模式下画笔为纯白色，粗细为10
                self.__painter.setPen(QPen(Qt.white, 10))

            # 画线
            self.__painter.drawLine(self.__lastPos, self.__currentPos)
            self.__painter.end()
            self.__lastPos = self.__currentPos
            self.update()  # 更新显示

        self.mouseEventpos = mouseEvent.pos()
        # pos = self.mapToGlobal(mouseEvent.pos()) #相對位置轉絕對
        # print(pos)
        pos = QCursor.pos()
        hwnd = win32gui.WindowFromPoint((pos.x(), pos.y()))
        print('x,y', pos.x(), pos.y())
        print(*win32gui.GetWindowRect(hwnd))
        # self.frameWidget.setRect(*win32gui.GetWindowRect(hwnd))
        # 截图
        screen = QApplication.primaryScreen()  # 获取主显示屏对象（QScreen对象）
        if screen is not None:
            image = screen.grabWindow(0, pos.x() - 60, pos.y() - 60, 120, 120)
            if not image.isNull():
                self.EnlargeImg.setPixmap(image.scaled(240, 240))
        #         self.EnlargeImg.update()

    def mouseReleaseEvent(self, mouseEvent):
        self.__IsEmpty = False  # 画板不再为空

    # def leaveEvent(self, event):
    #     # super(Label, self).leaveEvent(event)
    #     # 得到鼠标在屏幕中的位置
    #     print('鼠标离开')
    #     print(event)
    #     pos = QCursor.pos()
    #     print(pos)
    #     hwnd = win32gui.WindowFromPoint((pos.x(), pos.y()))
    #     print('x,y', pos.x(), pos.y())
    #     print(*win32gui.GetWindowRect(hwnd))
    #     # self.frameWidget.setRect(*win32gui.GetWindowRect(hwnd))
    #     # 截图
    #     screen = QApplication.primaryScreen()  # 获取主显示屏对象（QScreen对象）
    #     if screen is not None:
    #         image = screen.grabWindow(0, pos.x() - 60, pos.y() - 60, 120, 120)
    #         if not image.isNull():
    #             self.EnlargeImg.setPixmap(image.scaled(240, 240))
    #     #         self.EnlargeImg.update()

    def on_PenColorChange(self):
        color_index = self.__comboBox_penColor.currentIndex()
        color_str = self.__colorList[color_index]
        self.__paintBoard.ChangePenColor(color_str)

    def on_PenThicknessChange(self):
        penThickness = self.__spinBox_penThickness.value()
        self.__paintBoard.ChangePenThickness(penThickness)

    def on_btn_Save_Clicked(self):
        # savePath = QFileDialog.getSaveFileName(self, 'Save Your Paint', '.\\', '*.png')
        # print(savePath)
        curImg = self.imglist[self.CurImId]
        ImgName = os.path.split(curImg)[-1]
        savePath = os.path.join(r'C:\Users\49942\Pictures', ImgName)
        print('保存')
        print(savePath)
        if savePath == "":
            print("Save cancel")
            return
        image = self.__board.toImage()
        image.save(savePath)

    def on_cbtn_Eraser_clicked(self):
        if self.__cbtn_Eraser.isChecked():
            self.__paintBoard.EraserMode = True  # 进入橡皮擦模式
        else:
            self.__paintBoard.EraserMode = False  # 退出橡皮擦模式

    def Quit(self):
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
