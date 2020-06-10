from PyQt5 import QtCore, QtGui, QtWidgets
from trainer_gui import Ui_MainWindow
from jcaptcha_image import JCaptchaImage, JCaptchaCharacterImage
import os, sys


class MessageBox:
	def showMessage_trainingComplete(form):
		msg = QtWidgets.QMessageBox(form)
		msg.setText('All training data collected and Model trained successfully!')
		msg.setWindowTitle('Training complete!')
		msg.setWindowIcon(QtGui.QIcon('icon/robot.ico'))
		msg.exec_()

	def showMessage_emptyTextBox(form):
		msg = QtWidgets.QMessageBox(form)
		msg.setText('Invalid input data!')
		msg.setWindowTitle('Try again!')
		msg.setWindowIcon(QtGui.QIcon('icon/robot.ico'))
		msg.exec_()

#-------------------------


class TrainerApp:
	def __init__(self):
		self.images_filenames = os.listdir('Training Images')
		self.imageName_index = 0
		self.training_X_outputFile = open('Collected Training Data/training_X.csv', 'w')
		self.training_Y_outputFile = open('Collected Training Data/training_Y.csv', 'w')
		#------------------------------
		app = QtWidgets.QApplication(sys.argv)
		self.MainWindow = QtWidgets.QMainWindow()
		self.UI = Ui_MainWindow()
		self.UI.setupUi(self.MainWindow, self)
		#
		self.__remainingCount = len(self.images_filenames)
		self.__failedCount = 0
		self.UI.remaining_label.setText('Remaining: ' + str(self.__remainingCount))
		self.UI.failed_label.setText('Failed: 0')
		#
		self.MainWindow.show()
		sys.exit(app.exec_())

	def storeTrainingData(self):
		if self.UI.answer_lineEdit.text() == '':
			MessageBox.showMessage_emptyTextBox(self.MainWindow)
			return
		if self.imageName_index + 1 >= len(self.images_filenames):
			MessageBox.showMessage_trainingComplete(self.MainWindow)
			self.training_X_outputFile.close()
			self.training_Y_outputFile.close()
			return
		#------------------------------
		img = JCaptchaImage('Training Images/' + self.images_filenames[self.imageName_index])
		img.treat()
		img.collect_character_imageList()
		jcaptcha_char_images = img.get_JCaptchaCharacterImage_List()
		answer_text = self.UI.answer_lineEdit.text()
		#------------------------------
		training_X = ''
		training_Y = ''
		#---
		if len(jcaptcha_char_images) != len(answer_text):
			open('log.txt', 'a').write('Issue with ' + self.images_filenames[self.imageName_index] + '\n')
			self.__failedCount += 1
			self.__remainingCount -= 1
			self.UI.failed_label.setText('Failed: ' + str(self.__failedCount))
			self.UI.remaining_label.setText('Remaining: ' + str(self.__remainingCount))
		else:
			for i in range(len(jcaptcha_char_images)):
				training_X += jcaptcha_char_images[i].get_CSV() + '\n'
				training_Y += answer_text[i] + '\n'
			self.training_X_outputFile.write(training_X)
			self.training_Y_outputFile.write(training_Y)
		#------------------------------
		self.imageName_index += 1
		self.UI.captchaBox.setPixmap(QtGui.QPixmap("Training Images/" + self.images_filenames[self.imageName_index]))
		self.UI.answer_lineEdit.setText('')
		#
		self.__remainingCount -= 1
		self.UI.remaining_label.setText('Remaining: ' + str(self.__remainingCount))


#####
#####
#####

def main():
	if os.path.isfile('log.txt'):
		os.remove('log.txt')
	trainer = TrainerApp()

if __name__ == '__main__':
	main()