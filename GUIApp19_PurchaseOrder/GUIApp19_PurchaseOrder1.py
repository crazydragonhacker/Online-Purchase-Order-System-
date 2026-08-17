import os,sys
os.system("cls")
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QPixmap,QIcon
from PyQt5.QtWidgets import QApplication,QWidget,QLineEdit,QLabel,QComboBox,QPushButton,QMessageBox
import cx_Oracle
class MainWindow(QWidget):
    def makeLabel(self,caption,x,y,w,h,mode,pictfile):
        temp = QLabel(caption,self)
        temp.setGeometry(x,y,w,h)
        if mode == 1:
            font = QFont("Verdana",20,False)
            font.setBold(True)
            temp.setFont(font)
            temp.setAlignment(Qt.AlignCenter)
        elif mode == 2:
            font = QFont("Courier New",14,False)
            font.setBold(True)
            temp.setFont(font)
        elif mode == 3:
            font = QFont("Courier New",10,False)
            font.setBold(True)
            temp.setFont(font)
        elif mode ==4:
             temp.setStyleSheet("background:white;border:2px solid blue;")
             temp.setPixmap(QPixmap(pictfile))
             temp.setScaledContents(True)
    
        return temp
    def makeLineEdit(self,x,y,w,h):
        font = QFont("Courier New",16,False)
        font.setBold(True)
        temp = QLineEdit(self)
        temp.setFont(font)
        temp.setAlignment(QtCore.Qt.AlignCenter)
        temp.setGeometry(x,y,w,h)
        temp.setFixedSize(w,h)
        temp.setStyleSheet("border:2px solid black;background:white;")
        return temp  
    def makePushButton(self,caption,x,y,w,h):
        font = QFont("Courier New",16,False)
        font.setBold(True)
        temp = QPushButton(caption,self)
        temp.setFont(font)
        temp.setGeometry(x,y,w,h)
        temp.setStyleSheet("background:silver;")
        return temp
    def drawLine(self,x,y,w,h):
        line = QtWidgets.QFrame(self)
        line.setGeometry(QtCore.QRect(x,y,w,h))
        line.setFrameShape(QtWidgets.QFrame.HLine)
        return None
    

    def registation(self):
        fname = "'"+self.txtFName.text()+"'"
        lname = "'"+self.txtLName.text()+"'"
        email = "'"+self.txtEmail.text()+"'"
        street1 ="'"+self.txtStreet1.text()+"'"
        street2 ="'"+self.txtStreet2.text()+"'"
        city    ="'"+self.txtCity.text()+"'"
        state   ="'"+self.txtState.text()+"'"
        sql = "INSERT INTO CUSTOMER VALUES(" + fname + "," + lname + "," + email + "," + street1 + "," + street2 + "," + city + "," + state + ")"
        self.curs.execute(sql)
        self.conn.commit()
        QMessageBox.about(None,"Customer Registration","Customer Registered Successfully")
        

        from PurchaseOrder2 import FrameSecond
        self.Winsecond = FrameSecond()
        self.Winsecond.setWindowTitle("Purchase Order Form")
        self.Winsecond.setWindowIcon(QIcon(os.path.dirname(__file__)+os.sep+'icon.jpg'))
        self.Winsecond.setFixedSize(800,650)
        self.Winsecond.setStyleSheet("background:white;")
        self.Winsecond.show()
        self.hide()

        return None
    

    def reset(self):
        self.txtFName.setText("")
        self.txtLName.setText("")
        self.txtEmail.setText("")
        self.txtStreet1.setText("")
        self.txtStreet2.setText("")
        self.txtCity.setText("")
        self.txtState.setText("")
        return None
    
    def quitApplication(self):
        self.curs.close()
        self.conn.close()

        exit(0)
        return None
    

    def __init__(self):
            super().__init__()

            self.makeLabel("Purchase Order",20,20,280,40,1,"")
            self.makeLabel("What would you like to purchase?",20,60,280,20,3,"")
            self.makeLabel("",300,0,500,80,4,os.path.dirname(__file__)+os.sep+'pic5.jpg')
            self.drawLine(0,80,800,5)

            self.makeLabel("Your Name",20,100,300,20,2,"")
            self.txtFName = self.makeLineEdit(250,100,250,30)
            self.txtLName = self.makeLineEdit(510,100,250,30)

            self.makeLabel("First Name",250,130,300,20,3,"")
            self.makeLabel("Last Name",510,130,300,20,3,"")


            self.makeLabel("Your Email",20,170,300,20,2,"")
            self.txtEmail = self.makeLineEdit(250,170,510,30) 


            self.makeLabel("Shipping Address",20,220,300,20,2,"")
            self.txtStreet1 = self.makeLineEdit(250,220,510,30)

            self.makeLabel("Address Line1",250,250,300,20,3,"")
            self.txtStreet2 = self.makeLineEdit(250,280,510,30)
            self.makeLabel("Address Line2",250,310,300,20,3,"")

            self.txtCity = self.makeLineEdit(250,340,250,30)
            self.txtState = self.makeLineEdit(510,340,250,30)
            #self.makeLabel("Address Line2",250,310,300,20,3,"")
            self.makeLabel("City",250,370,300,20,3,"")
            self.makeLabel("State", 510,370,300,20,3,"")
            self.drawLine(0,390,800,5)

            self.btnRegister= self.makePushButton("Register",110,410,120,30)
            self.btnRegister.clicked.connect(self.registation)

            self.btnReset= self.makePushButton("Reset",340,410,120,30)
            self.btnReset.clicked.connect(self.reset)

            self.btnExit= self.makePushButton("Exit",570,410,120,30)
            self.btnExit.clicked.connect(self.quitApplication)

            self.drawLine(0,450,800,5)

            
            self.conn = cx_Oracle.connect("hr/hr@localhost:1521/xe")
            self.curs = self.conn.cursor()
            #QMessageBox.about(None,"connection confirmed","Connection established succesfully")
            return None
    pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("New Customer Registation")
    window.setWindowIcon(QIcon(os.path.dirname(__file__)+os.sep+'icon.jpg'))
    window.setFixedSize(805,500)
    window.setStyleSheet("background:bisque;")
    window.move(900,520)
    window.show()
    sys.exit(app.exec_())