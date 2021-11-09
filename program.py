from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from playsound import playsound
import sys
import random

def nd(s):              #중요하지 않음
    if s[-1]=='\n':
        s=s[:-1]
    return s
class program(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(70, 70, 1680, 910)  # ----그냥 gui
        image = QImage("./polka-dot-pattern.jpg")
        image = image.scaled(QSize(1980, 1250))
        palette = QPalette()
        palette.setBrush(10, QBrush(image))
        self.setPalette(palette)
        self.groups = []
        self.group = []

        self.initUI()
    def initUI(self):
        f= open('자리.txt','r',encoding='utf-8')    #이전에 저장한 자리 불러옴
        self.lines = list(map(nd,f.readlines()))
        f.close()
        row=int(self.lines.pop(0))
        self.front=self.lines[:row*3+1]    #앞 뒤줄을 따로 나눠서 섞기
        self.back=self.lines[row*3+1:]

        

        self.btnlist=[]
        
        self.row =QLabel('줄 수:', self)
        row_font=self.row.font()
        row_font.setPointSize(20)
        self.row.setFont(row_font)
        self.row.move(1670,56)
        
        self.t =QLabel('      교탁      ', self)
        t_font=self.t.font()
        t_font.setPointSize(40)
        t_font.setBold(True)
        self.t.setFont(t_font)
        self.t.move(518,900)
        self.t.setStyleSheet("color: white;"
                       "background-color: #87CEFA;"
                       "border-style: dashed;"
                       "border-width: 3px;"
                       "border-color: #1E90FF")
        
        self.txt1 = QLineEdit("",self)
        self.txt1.move(1670,88)
        
        
        self.btn= QPushButton('자리 생성',self)
        self.btn.move(1670,245)
        self.btn.resize(QSize(126,70))
        self.btn.clicked.connect(self.create)

        self.btn1= QPushButton('저장',self)
        self.btn1.move(1670,525)
        self.btn1.resize(QSize(126,70))
        self.btn1.clicked.connect(self.save)


        self.btn3 = QPushButton('현재 자리', self)
        self.btn3.move(1870, 245)
        self.btn3.resize(QSize(126, 70))
        self.btn3.clicked.connect(self.place)

        self.row.show()
        self.t.show()
        self.txt1.show()
        self.btn.show()
        self.btn1.show()
        self.btn3.show()
        self.show()

    def create(self):                   #자리 배치

        if self.txt1.text() == '자':
            self.initDis()
            return
        random.shuffle(self.front)          #섞기
        random.shuffle(self.back)
        self.lines = self.back+self.front
        self.r = int(self.txt1.text())

        y=0
        for i in self.groups:
            random.shuffle(i)

            if y>len(self.lines)//self.r:
                y=0
            ny = [1] * self.r
            for j in i:
                self.lines.remove(j)
                
                sy = []
                
                for k in range(len(ny)):
                    if ny[k]:
                        sy.append(k)

                if not sy:
                    y+=1
                    ny = [1] * self.r
                    continue
                x=sy[random.randint(0,len(sy)-1)]
                self.lines.insert(self.r*y+x,j)
                ny = [1] * self.r
                ny[x] = ny[max(0,x-1)] = ny[min(len(ny)-1,x+1)] = 0
                y+=1
                print(ny)




        self.place()





    def place(self):
        for i in self.btnlist:              #새로 뽑으면 이미 만들어진거 삭제
            i.deleteLater()
        self.btnlist=[]



        o=0
        s=0
        for i in range(len(self.lines)//self.r+1):   #섞은 자리대로 배치합니다
            p=0
            if len(self.lines)-o > self.r:
                loop=self.r
            else:
                loop=len(self.lines)-o
            for j in range(loop):
                l=QLabel(self.lines[o],self)
                l.setAlignment(Qt.AlignCenter)
                l.setStyleSheet("color: blue;"
                       "background-color: #87CEFA;"
                       "border-style: dashed;"
                       "border-width: 3px;"
                       "border-color: #1E90FF")
                l_font=l.font()
                l_font.setBold(True)
                l_font.setPointSize(25)
                l.setFont(l_font)
                self.btnlist.append(l)
                self.btnlist[o].resize(QSize(210,105))
                if p%2==0:
                    k=48
                else:
                    k=36
                self.btnlist[o].move(j*224+k,835-(i*119+105))
                self.btnlist[o].show()
                p+=1
                o+=1
        playsound("pop.mp3")
    def save(self):
        if self.r and self.lines:
            f= open('자리.txt','w',encoding='utf-8')
            f.write(str(self.r)+'\n')
            for line in self.lines:
                f.write(line+'\n')
            f.close()

    def initDis(self):
        self.t.deleteLater()
        self.btn.deleteLater()
        self.btn1.deleteLater()
        self.btn3.deleteLater()
        self.txt1.deleteLater()
        self.row.deleteLater()
        self.distance()

    def deldis(self):
        self.btn3.deleteLater()
        self.btn4.deleteLater()
        self.btn5.deleteLater()
        for i in self.btnlist:
            i.deleteLater()
        self.initUI()

    def reload(self):
        self.btn3.deleteLater()
        self.btn4.deleteLater()
        self.btn5.deleteLater()
        self.distance()

    def distance(self):
        self.groups=[]
        self.group=[]
        o=0
        for i in self.btnlist:
            i.deleteLater()

        self.btn3 = QPushButton('그룹추가', self)
        self.btn3.move(1670, 245)
        self.btn3.resize(QSize(126, 70))
        self.btn3.clicked.connect(self.newgroup)

        self.btn4 = QPushButton('초기화', self)
        self.btn4.move(1670, 445)
        self.btn4.resize(QSize(126, 70))
        self.btn4.clicked.connect(self.reload)

        self.btn5 = QPushButton('뒤로가기', self)
        self.btn5.move(1670, 845)
        self.btn5.resize(QSize(126, 70))
        self.btn5.clicked.connect(self.deldis)

        self.btn3.show()
        self.btn4.show()
        self.btn5.show()

        self.btnlist = []
        self.lines = []
        f = open('반.txt', 'r', encoding='utf-8')
        self.lines = list(map(nd, f.readlines()))[1:]
        f.close()

        for i in range(len(self.lines)//6+1):
            if len(self.lines)-o > 6:
                loop=6
            else:
                loop=len(self.lines)-o
            for j in range(loop):
                l=QPushButton(self.lines[o],self)
                l_font=l.font()
                l_font.setBold(True)
                l_font.setPointSize(25)
                l.setFont(l_font)
                self.btnlist.append(l)
                self.btnlist[o].resize(QSize(210,105))
                self.btnlist[o].move(j*224,835-(i*119+105))
                self.btnlist[o].show()
                self.btnlist[o].clicked.connect(self.color)
                o+=1

    def color(self):
        sender= self.sender()
        sender.setStyleSheet("color: blue;"
                       "background-color: #87CEFA;"
                       "border-style: dashed;"
                       "border-width: 3px;"
                       "border-color: #1E90FF")
        self.group.append(sender)

    def newgroup(self):
        for ele in self.group:
            ele.setStyleSheet("color: yellow;"
                       "background-color: #87CEFA;"
                       "border-style: dashed;"
                       "border-width: 3px;"
                       "border-color: #1E90FF")
        self.groups.append(list(map(lambda x: x.text(), self.group)))
        self.group = []


app=QApplication([])
ex = program()
sys.exit(app.exec_())
