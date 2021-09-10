import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import os
import os.path
from PyQt5.uic import loadUiType
import urllib.request
ui,_ =loadUiType ('LYP.ui')

class MainApp(QMainWindow , ui):
    def __init__(self, parent=None):
        super(MainApp , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUi()
        self.BUtton_Hnadler()
        


    ##UI changes
    def InitUi(self):
        pass
    ##Buttons in App
    def BUtton_Hnadler(self):
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Browse_Location)
        
    ##Calculate the progress
    def Progress_Handler(self,blocknum,blocksize,totalsize):
        read_data=blocknum*blocksize
        
        if totalsize >0:
            download_percentage=read_data*100/totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()
            
           
    ##Browsing to file explorer
    def Browse_Location(self):
        save_location=QFileDialog().getSaveFileName(self, caption="Save As", directory=".", filter="All Files(*.*)")
        print(save_location)
        
        self.lineEdit_2.setText(str(save_location[0]))
    
    
    
    ##Downloading files
    def Download(self):
        print('Starting Download')
        
        download_url=self.lineEdit.text()
        Save_location=self.lineEdit_2.text()
        
        
        ##Erorr box in case of Invalid File name or URL
        if download_url=='' or Save_location=='':
            QMessageBox.warning(self, "Data Error" , "Dear User Please Provide a Valid URL or Save Location")
        else:
            try:
                urllib.request.urlretrieve(download_url,Save_location,self.Progress_Handler)
                
            except Exception:
                QMessageBox.warning(self, "Data Error" , "Dear User Please Provide a Valid URL or Save Location")
                return
                
         
                
         
        QMessageBox.information(self ,"Download Completed" , "The Download Compeleted Successfully") 
        
        
        
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)
         
            
         
                
    ##Save Location in Line edit
    def Save_location(self):
        pass


def main():
    app=QApplication(sys.argv)
    window=MainApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
    
    