import json
from jcaptcha_image import JCaptchaImage
from naive_bayes_classifier import NaiveBayesClassifier


class CaptchaSolver:
	def __init__(self, jcaptcha_image):
		self.jcaptcha_image = jcaptcha_image
		self.jcaptcha_image.treat()
		self.jcaptcha_image.collect_character_imageList()
		self.jchar_CSV_list = [jchar_img.get_CSV() for jchar_img in self.jcaptcha_image.get_JCaptchaCharacterImage_List()]

	def getSolution(self):
		classifier = NaiveBayesClassifier()
		solution = ''.join([classifier.getClassification(jchar_CSV) for jchar_CSV in self.jchar_CSV_list])
		return solution


######
######
######

def main():
	jcaptcha_image = JCaptchaImage(input('- Enter image filename: '))
	solver = CaptchaSolver(jcaptcha_image)
	print('\t- Solution:', solver.getSolution())

if __name__ == '__main__':
	main()