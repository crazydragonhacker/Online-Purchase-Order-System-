import datetime

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QMessageBox, QCheckBox,
    QGroupBox, QRadioButton,
)

from . import db
from .config import asset_path
from .products import PRODUCTS


class FrameSecond(QWidget):
    # ---- widget-building helpers (unchanged from the original app) ----
    def makeLabel(self, caption, x, y, w, h, mode, pictfile):
        temp = QLabel(caption, self)
        temp.setGeometry(x, y, w, h)
        if mode == 1:
            font = QFont("Verdana", 20, False)
            font.setBold(True)
            temp.setFont(font)
        elif mode == 2:
            font = QFont("Courier New", 14, False)
            font.setBold(True)
            temp.setFont(font)
        elif mode == 3:
            font = QFont("Courier New", 10, False)
            font.setBold(True)
            temp.setFont(font)
        elif mode == 4:
            temp.setStyleSheet("background:white;border:2px solid blue;")
            temp.setPixmap(QPixmap(pictfile))
            temp.setScaledContents(True)
        return temp

    def makeCheckBox(self, x, y, w, h):
        temp = QCheckBox()
        temp.setParent(self)
        temp.setGeometry(x, y, w, h)
        return temp

    def makeGroupBox(self, cap, x, y, w, h):
        font = QFont("Courier New", 14, False)
        font.setBold(True)
        temp = QGroupBox(self)
        temp.setTitle(cap)
        temp.setFont(font)
        temp.setGeometry(x, y, w, h)
        temp.setAlignment(QtCore.Qt.AlignLeft)
        temp.setStyleSheet("border:2px solid black;background:white;")
        return temp

    def makeRadioButton(self, caption, x, y, w, h, grpBox):
        font = QFont("Courier New", 12, False)
        font.setBold(True)
        temp = QRadioButton(caption, grpBox)
        temp.setFont(font)
        temp.setStyleSheet("border:none;")
        temp.setGeometry(x, y, w, h)
        return temp

    def makePushButton(self, caption, x, y, w, h):
        font = QFont("Courier New", 16, False)
        font.setBold(True)
        temp = QPushButton(caption, self)
        temp.setFont(font)
        temp.setGeometry(x, y, w, h)
        temp.setStyleSheet("background:silver;")
        return temp

    def drawLine(self, x, y, w, h):
        line = QtWidgets.QFrame(self)
        line.setGeometry(QtCore.QRect(x, y, w, h))
        line.setFrameShape(QtWidgets.QFrame.HLine)
        return None

    # ---- actions ----
    def calculateTotal(self):
        self.total = 0
        for idx in range(3):
            if self.productList[idx]['chkbox'].isChecked():
                self.total += self.productList[idx]['price']
        self.lblTotal.setText("Rs." + "{:.2f}".format(self.total))
        return None

    def payModeClick(self):
        source = self.sender()
        self.payMode = source.text()
        return None

    def submitData(self):
        selected = [p for p in self.productList if p['chkbox'].isChecked()]
        if not selected:
            QMessageBox.warning(self, "No products selected",
                                 "Please select at least one product before submitting.")
            return None
        try:
            order_id = self.orderID.text()
            for product in selected:
                db.insert_product_order(self.conn, order_id, product['pid'])
            db.insert_payment(self.conn, order_id, self.total, self.payMode)
            QMessageBox.about(self, "Order Registration", "Product Order Registered Successfully")
        except Exception as exc:
            self.conn.rollback()
            QMessageBox.critical(self, "Error", f"Could not register order:\n{exc}")
        return None

    def reset(self):
        for idx in range(3):
            self.productList[idx]['chkbox'].setChecked(False)
        self.calculateTotal()
        return None

    def quitApplication(self):
        if getattr(self, "conn", None) is not None:
            self.conn.close()
        QApplication.quit()
        return None

    def __init__(self):
        super().__init__()

        self.makeLabel("Purchase Order", 20, 20, 280, 40, 1, "")
        self.makeLabel("What would you like to purchase?", 20, 60, 280, 20, 3, "")
        self.makeLabel("", 300, 0, 500, 80, 4, asset_path("pic5.jpg"))
        self.drawLine(0, 80, 800, 5)

        # Product catalog is now shared via app/products.py (also seeded
        # into the PRODUCT table by db/schema.sql) instead of being
        # duplicated inline.
        self.productList = [dict(p) for p in PRODUCTS]

        self.makeLabel("My Products", 20, 100, 300, 20, 2, "")
        self.makeLabel("Order ID", 220, 100, 100, 20, 2, "")
        timestamp = str(datetime.datetime.now().timestamp()).split(".")[0]
        self.orderID = self.makeLabel(timestamp, 330, 95, 300, 30, 2, "")
        self.orderID.setAlignment(QtCore.Qt.AlignCenter)
        self.orderID.setStyleSheet("border:1px solid black;")

        self.productList[0]['chkbox'] = self.makeCheckBox(20, 160, 20, 30)
        self.productList[0]['chkbox'].clicked.connect(self.calculateTotal)
        self.productList[0]['lblPict'] = self.makeLabel("", 50, 130, 80, 80, 4, self.productList[0]['image'])
        self.productList[0]['lblPID'] = self.makeLabel("Product ID: " + self.productList[0]['pid'], 170, 130, 250, 30, 2, "")
        self.productList[0]['lblName'] = self.makeLabel(self.productList[0]['name'], 370, 130, 150, 30, 2, "")
        self.productList[0]['lblDesc'] = self.makeLabel(self.productList[0]['desc'], 170, 160, 600, 30, 3, "")
        self.productList[0]['lblPrice'] = self.makeLabel("Rs." + "{:.2f}".format(self.productList[0]['price']), 650, 130, 120, 30, 2, "")
        self.drawLine(0, 220, 800, 5)

        self.productList[1]['chkbox'] = self.makeCheckBox(20, 260, 20, 30)
        self.productList[1]['chkbox'].clicked.connect(self.calculateTotal)
        self.productList[1]['lblPict'] = self.makeLabel("", 50, 230, 80, 80, 4, self.productList[1]['image'])
        self.productList[1]['lblPID'] = self.makeLabel("Product ID: " + self.productList[1]['pid'], 170, 230, 250, 30, 2, "")
        self.productList[1]['lblName'] = self.makeLabel(self.productList[1]['name'], 370, 230, 150, 30, 2, "")
        self.productList[1]['lblDesc'] = self.makeLabel(self.productList[1]['desc'], 170, 260, 600, 30, 3, "")
        self.productList[1]['lblPrice'] = self.makeLabel("Rs." + "{:.2f}".format(self.productList[1]['price']), 650, 230, 120, 30, 2, "")
        self.drawLine(0, 320, 800, 5)

        self.productList[2]['chkbox'] = self.makeCheckBox(20, 360, 20, 30)
        self.productList[2]['chkbox'].clicked.connect(self.calculateTotal)
        self.productList[2]['lblPict'] = self.makeLabel("", 50, 330, 80, 80, 4, self.productList[2]['image'])
        self.productList[2]['lblPID'] = self.makeLabel("Product ID: " + self.productList[2]['pid'], 170, 330, 250, 30, 2, "")
        self.productList[2]['lblName'] = self.makeLabel(self.productList[2]['name'], 370, 330, 150, 30, 2, "")
        self.productList[2]['lblDesc'] = self.makeLabel(self.productList[2]['desc'], 170, 360, 600, 30, 3, "")
        self.productList[2]['lblPrice'] = self.makeLabel("Rs." + "{:.2f}".format(self.productList[2]['price']), 650, 330, 120, 30, 2, "")
        self.drawLine(0, 420, 800, 5)

        self.total = 0
        self.lblTotal = self.makeLabel("Rs.0.00", 650, 430, 120, 30, 2, "")
        self.grpBoxPayment = self.makeGroupBox("Payment Mode", 20, 470, 550, 160)
        self.rdbtnCard = self.makeRadioButton("Debit/Credit Card", 10, 30, 500, 30, self.grpBoxPayment)
        self.rdbtnCard.clicked.connect(self.payModeClick)
        self.rdbtnUPI = self.makeRadioButton("Unified Payment Interface", 10, 60, 500, 30, self.grpBoxPayment)
        self.rdbtnUPI.clicked.connect(self.payModeClick)
        self.rdbtnUPI.setChecked(True)

        self.payMode = self.rdbtnUPI.text()

        self.rdbtnNetBank = self.makeRadioButton("Net Banking", 10, 90, 500, 30, self.grpBoxPayment)
        self.rdbtnNetBank.clicked.connect(self.payModeClick)

        self.rdbtnCash = self.makeRadioButton("Cash On Delivery", 10, 120, 500, 30, self.grpBoxPayment)
        self.rdbtnCash.clicked.connect(self.payModeClick)

        self.btnSubmit = self.makePushButton("Submit", 600, 488, 150, 30)
        self.btnSubmit.clicked.connect(self.submitData)

        self.btnReset = self.makePushButton("Reset", 600, 535, 150, 30)
        self.btnReset.clicked.connect(self.reset)

        self.btnExit = self.makePushButton("Exit", 600, 582, 150, 30)
        self.btnExit.clicked.connect(self.quitApplication)

        self.conn = None
        try:
            self.conn = db.get_connection()
        except ConnectionError as exc:
            QMessageBox.critical(self, "Database Connection Error", str(exc))

        return None
