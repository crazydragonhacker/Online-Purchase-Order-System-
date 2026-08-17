import os
os.system("cls")

import cx_Oracle
import sys,datetime
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtGui import QFont,QPixmap,QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QMessageBox,QCheckBox,QGroupBox,QRadioButton

class FrameSecond(QWidget):
    def makeLabel(self,caption,x,y,w,h,mode,pictfile):
        temp = QLabel(caption,self)
        temp.setGeometry(x,y,w,h)
        if mode == 1:
            font = QFont("Verdana",20,False)
            font.setBold(True)
            temp.setFont(font)
        elif mode == 2:
            font = QFont("Courier New",14,False)
            font.setBold(True)
            temp.setFont(font)
        elif mode == 3:
            font = QFont("Courier New",10,False)
            font.setBold(True)
            temp.setFont(font)
        elif mode == 4:
            temp.setStyleSheet("background:white;border:2px solid blue;")
            temp.setPixmap(QPixmap(pictfile))
            temp.setScaledContents(True)
        return temp
    def makeCheckBox(self,x,y,w,h):
        temp = QCheckBox()
        temp.setParent(self)
        temp.setGeometry(x,y,w,h)
        return temp
    def makeGroupBox(self,cap,x,y,w,h):
        font = QFont("Courier New",14,False)
        font.setBold(True)
        temp = QGroupBox(self)
        temp.setTitle(cap)
        temp.setFont(font)
        temp.setGeometry(x,y,w,h)
        temp.setAlignment(QtCore.Qt.AlignLeft)
        temp.setStyleSheet("border:2px solid black;background:white;")
        return temp
    def makeRadioButton(self,caption,x,y,w,h,grpBox):
        font = QFont("Courier New",12,False)
        font.setBold(True)
        temp = QRadioButton(caption,grpBox)
        temp.setFont(font)
        temp.setStyleSheet("border:none;")
        temp.setGeometry(x,y,w,h)
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
    def calculateTotal(self):
        self.total = 0
        self.lblTotal.setText("Rs."+str(self.total))
        for idx in range(3):
            if self.productList[idx]['chkbox'].isChecked(): self.total += self.productList[idx]['price']
        self.lblTotal.setText("Rs."+"{:.2f}".format(self.total))
        return None
    def payModeClick(self):
        source = self.sender()
        self.payMode = source.text()
        return None
    def submitData(self):
        try:
            orderid = "'"+self.orderID.text()+"'"
            for idx in range(3):
                if self.productList[idx]['chkbox'].isChecked():
                    pid = "'"+self.productList[idx]['pid']+"'"
                    sql = "INSERT INTO PRODUCTORDER VALUES("+orderid+","+pid+")"
                    self.curs.execute(sql)
            
            amount = self.total
            paymode = "'"+self.payMode+"'"
            sql = "INSERT INTO PAYMENT VALUES("+orderid+","+str(amount)+","+paymode+")"
            self.curs.execute(sql)
            self.conn.commit()
            QMessageBox.about(None,"Order Registration","Product Order Registered Successfully")
        except:
            QMessageBox.about(None,"Error",sys.exc_info()[0])
        return None
    def reset(self):
        for idx in range(3): self.productList[idx]['chkbox'].setChecked(False)
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
        self.makeLabel("",300,0,500,80,4,os.path.dirname(__file__)+os.sep+"pic5.jpg")
        self.drawLine(0,80,800,5)

        self.productList = [
        {"pict":os.path.dirname(__file__)+os.sep+"cap.png","pid":"P-01","name":"Cap","desc":"This product is made from at least 50% recycled polyester fiber","price":100.00},
        {"pict":os.path.dirname(__file__)+os.sep+"linen-shoe.jpg","pid":"P-02","name":"Linen Shoe","desc":"You will wear it again and again, This shoe is remarkable and loyal<br>just like you","price":1200.00},
        {"pict":os.path.dirname(__file__)+os.sep+"hoodie.png","pid":"P-03","name":"Hoodie","desc":"Durably stitched surfaces, clean finishes and the perfect amount<br>of shine to make you dazzle","price":800.00}
        ]
        self.makeLabel("My Products",20,100,300,20,2,"")
        self.makeLabel("Order ID",220,100,100,20,2,"")
        time = datetime.datetime.now()
        timestamp = time.timestamp()
        self.orderID = self.makeLabel((str(timestamp).split("."))[0],330,95,300,30,2,"")
        self.orderID.setAlignment(QtCore.Qt.AlignCenter)
        self.orderID.setStyleSheet("border:1px solid black;")

        self.productList[0]['chkbox'] = self.makeCheckBox(20,160,20,30)
        self.productList[0]['chkbox'].clicked.connect(self.calculateTotal)
        self.productList[0]['lblPict'] = self.makeLabel("",50,130,80,80,4,self.productList[0]['pict'])
        self.productList[0]['lblPID'] = self.makeLabel("Product ID: "+self.productList[0]['pid'],170,130,250,30,2,"")
        self.productList[0]['lblName'] = self.makeLabel(self.productList[0]['name'],370,130,150,30,2,"")
        self.productList[0]['lblDesc'] = self.makeLabel(self.productList[0]['desc'],170,160,600,30,3,"")
        self.productList[0]['lblPrice'] = self.makeLabel("Rs."+"{:.2f}".format(self.productList[0]['price']),650,130,120,30,2,"")
        self.drawLine(0,220,800,5)
        
        self.productList[1]['chkbox'] = self.makeCheckBox(20,260,20,30)
        self.productList[1]['chkbox'].clicked.connect(self.calculateTotal)
        self.productList[1]['lblPict'] = self.makeLabel("",50,230,80,80,4,self.productList[1]['pict'])
        self.productList[1]['lblPID'] = self.makeLabel("Product ID: "+self.productList[1]['pid'],170,230,250,30,2,"")
        self.productList[1]['lblName'] = self.makeLabel(self.productList[1]['name'],370,230,150,30,2,"")
        self.productList[1]['lblDesc'] = self.makeLabel(self.productList[1]['desc'],170,260,600,30,3,"")
        self.productList[1]['lblPrice'] = self.makeLabel("Rs."+"{:.2f}".format(self.productList[1]['price']),650,230,120,30,2,"")
        self.drawLine(0,320,800,5)

        self.productList[2]['chkbox'] = self.makeCheckBox(20,360,20,30)
        self.productList[2]['chkbox'].clicked.connect(self.calculateTotal)
        self.productList[2]['lblPict'] = self.makeLabel("",50,330,80,80,4,self.productList[2]['pict'])
        self.productList[2]['lblPID'] = self.makeLabel("Product ID: "+self.productList[2]['pid'],170,330,250,30,2,"")
        self.productList[2]['lblName'] = self.makeLabel(self.productList[2]['name'],370,330,150,30,2,"")
        self.productList[2]['lblDesc'] = self.makeLabel(self.productList[2]['desc'],170,360,600,30,3,"")
        self.productList[2]['lblPrice'] = self.makeLabel("Rs."+"{:.2f}".format(self.productList[2]['price']),650,330,120,30,2,"")
        self.drawLine(0,420,800,5)

        self.lblTotal = self.makeLabel("Rs.0.00",650,430,120,30,2,"")
        self.grpBoxPayment = self.makeGroupBox("Payment Mode",20,470,550,160)
        self.rdbtnCard = self.makeRadioButton("Debit/Credit Card",10,30,500,30,self.grpBoxPayment)
        self.rdbtnCard.clicked.connect(self.payModeClick)
        self.rdbtnUPI = self.makeRadioButton("Unified Payment Interface",10,60,500,30,self.grpBoxPayment)
        self.rdbtnUPI.clicked.connect(self.payModeClick)
        self.rdbtnUPI.setChecked(True)

        self.payMode = self.rdbtnUPI.text()

        self.rdbtnNetBank = self.makeRadioButton("Net Banking",10,90,500,30,self.grpBoxPayment)
        self.rdbtnNetBank.clicked.connect(self.payModeClick)

        self.rdbtnCash = self.makeRadioButton("Cash On DElivery",10,120,500,30,self.grpBoxPayment)
        self.rdbtnCash.clicked.connect(self.payModeClick)

        self.btnSubmit = self.makePushButton("Submit",600,488,150,30)
        self.btnSubmit.clicked.connect(self.submitData)

        self.btnReset = self.makePushButton("Reset",600,535,150,30)
        self.btnReset.clicked.connect(self.reset)

        self.btnExit = self.makePushButton("Exit",600,582,150,30)
        self.btnExit.clicked.connect(self.quitApplication)

        self.conn = cx_Oracle.connect('HR/HR@localhost:1521/xe')
        self.curs = self.conn.cursor()

        pass









