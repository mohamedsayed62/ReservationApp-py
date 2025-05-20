from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from os import path
import sys
import mysql.connector
import time
import re

fromClass,_ = loadUiType(path.join(path.dirname(__file__) , "Reservation.ui"))

class Main(QMainWindow, fromClass) :
    def __init__(self, parent = None) :
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ConnectDB()
        self.StartApp()
        self.handeleButtons()
        
        self.StdSearch.textChanged.connect(self.change)
        self.listWidget.itemClicked.connect(self.PrintStd)
        
        self.lstName = ""
        
        
    
    ## StartApp
    def StartApp(self) :
        self.setWindowTitle("حجز الكتب")
    ## ConnectDataBase
    def ConnectDB(self) :
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="oz3asayed1242004@",
            database="mydb"
        )
        self.cr = self.db.cursor()
        print("done Connection")
    
    ##HandleButtons
    def handeleButtons(self) :
        self.addBtn.clicked.connect(self.addStd)
        self.updateBtn.clicked.connect(self.updateStd)
        self.deleteBtn.clicked.connect(self.deleteStd)
    
    ## delText
    def delText(self) :
        self.NameStd.setText("")
        self.NumStd.setText("")
        self.listWidget.clear()
        self.StdSearch.setText("")
    
    ## SearchStd
    def searchStd(self) :
        
        sql = '''
            SELECT * FROM student
        '''
        
        self.cr.execute(sql)
        
        data = self.cr.fetchall()
        
        return data
    
    
    ## AddStd
    def addStd(self) :
        stdName = self.NameStd.text()
        stdNum = self.NumStd.text()
        
        names = self.searchStd()
        flag = False
        
        for name in names :
            if name[0] == stdName :
                flag = True
                break
        
        if flag == False and len(stdNum) == 11 :
            sql = '''
                INSERT INTO student(StudentName, StudentNum)
                VALUES(%s, %s)
            '''
            values = (stdName, stdNum)
            
            self.cr.execute(sql, values)
            
            self.db.commit()
            
            print("Done Inserting")
            
            self.delText()
        
        
        
    ## UpdateStd
    def updateStd(self) :
        stdName = self.NameStd.text()
        stdNum = self.NumStd.text()
        
        if self.lstName != "" and len(stdNum) == 11 :
            sql = '''
                UPDATE student
                SET StudentName = %s,
                StudentNum = %s
                WHERE StudentName = %s
            '''
            values = (stdName, stdNum, self.lstName)
            
            self.cr.execute(sql, values)
            
            self.db.commit()
            
            self.delText()
        
    ## DeleteStd
    def deleteStd(self) :
        sql = '''DELETE FROM student WHERE StudentName = %s'''
        values = (self.lstName, )
        
        self.cr.execute(sql, values)
        
        self.db.commit()
        
        self.delText()
        
    def change(self, text) :
        names = self.searchStd()
        
        self.listWidget.clear()
        if text.strip() :
            pattern = fr"^{re.escape(text)}\W?([ء-ي]{1,}\W*)?"
            for name in names :
                reg = re.search(pattern, name[0])
                if reg :
                    self.listWidget.addItem(reg.string)   
            
    ## PrintStd
    def PrintStd(self, item) :
        name = self.NameStd.setText(item.text())
        self.lstName = item.text()
        
        nums = self.searchStd()
        
        for num in nums :
            if num[0] == item.text():
                self.NumStd.setText(num[1])
                
    ## MainApp
def main() :
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__ == "__main__" :
    main()
