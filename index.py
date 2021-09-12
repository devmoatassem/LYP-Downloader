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


        ##Get video information in Single youtube video
        self.pushButton_7.clicked.connect(self.Video_data)
        self.pushButton_14.clicked.connect(self.Download_Video)
        self.pushButton_4.clicked.connect(self.Save_location_video)

        
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
        
        
        self.lineEdit_2.setText(str(save_location[0]))
    
    
    
    ##Downloading files
    def Download(self):
        
        
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
        

   
 
    #############################################
    ################ YOUTUBE#####################
    #############################################
    def Video_data(self):
        ##storing entered text in variaable
        video_url=self.lineEdit_4.text()
        
        if video_url=='':
            QMessageBox.information(self ,"Data Error" , "PLease provide the valid URL") 
        else:
            video=pafy.new(video_url)
            
    
            video_stream=video.videostreams
            for stream in video_stream:
                size=humanize.naturalsize(stream.get_filesize())
                data="{} {} {} {}".format(stream.mediatype,stream.extension,stream.quality ,size )
                
                ##giving data to box for quality select
                self.comboBox.addItem(data)
    ##Save Location in Line edit
    def Save_location_video(self):
        save_location=QFileDialog().getSaveFileName(self, caption="Save As", directory=".", filter="All Files(*.*)")

        self.lineEdit_3.setText(str(save_location[0]))           
    
    ##Download Single Youtube video            
    def Download_Video(self):
        video_url=self.lineEdit_4.text()
        save_location=self.lineEdit_3.text()
        
        
        if video_url=='' or save_location=='':
            QMessageBox.warning(self, "Data Error" , "Dear User Please Provide a Valid URL or Save Location")
        else:
            video=pafy.new(video_url) 
            video_stream=video.videostreams
            video_quality=self.comboBox.currentIndex()
            download=video_stream[video_quality].download(filepath=save_location , callback=self.Video_progress)
            
            ##Check if URL is valid then proceed otherwise stop
                    
          
        ##Download compelete Dialog box 
        QMessageBox.information(self ,"Download Completed" , "Video Downloaded Successfully") 
        
        
        ##St lines of URL and save location and progress bar to empty after downloading
        
        self.lineEdit_4.setText('')
        self.lineEdit_3.setText('')
        self.progressBar_2.setValue(0)
        
        
    def Video_progress(self,total,received,ratio,rate,time):
         read_data=received
         if total>0:
             download_percentage=read_data*100/total
             self.progressBar_2.setValue(download_percentage)
             remaining_time=round(time/60,2)
             
             self.label.setText(str('{} minutes remaining'.format(remaining_time)))
             QApplication.processEvents()
        

def main():
    app=QApplication(sys.argv)
    window=MainApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
    
    