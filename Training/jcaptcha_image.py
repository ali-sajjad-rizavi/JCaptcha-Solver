from PIL import Image


class JCaptchaCharacterImage:
	def __init__(self, pil_image):
		self.image = pil_image
		self.width, self.height = self.image.size
		self.pixels = self.image.load()

	def get_CSV(self):
		yellow = (255, 255, 0)
		black = (0, 0, 0)
		csv_list = []
		for x in range(self.width):
			for y in range(self.height):
				if self.pixels[x, y] == black:
					csv_list.append('0')
				else:
					csv_list.append('1')
		return ','.join(csv_list)


class JCaptchaImage:
	def __init__(self, filename):
		self.__filename = filename
		self.image = Image.open(filename)
		self.pixels = self.image.load()
		self.width, self.height = self.image.size

	def replace_color(self, color_A, color_B):
		for x in range(self.width):
			for y in range(self.height): 
				if self.pixels[x, y] == color_A:
					self.pixels[x, y] = color_B

	def blacken_everything_except(self, color):
		for x in range(self.width):
			for y in range(self.height):
				if self.pixels[x, y] != color:
					self.pixels[x, y] = (0, 0, 0)

	def fill_gaps(self):
		for x in range(self.width):
			for y in range(self.height):
				if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
					continue
				if (self.pixels[x-1, y] == (255, 255, 0) or self.pixels[x-1, y-1] == (255, 255, 0) or self.pixels[x-1, y+1] == (255, 255, 0)) and (self.pixels[x+1, y] == (255, 255, 0) or self.pixels[x+1, y+1] == (255, 255, 0) or self.pixels[x+1, y-1] == (255, 255, 0)):
					self.pixels[x, y] = (255, 255, 0)
				if self.pixels[x, y-1] == (255, 255, 0) and self.pixels[x, y+1] == (255, 255, 0):
					self.pixels[x, y] = (255, 255, 0)

	def treat(self):
		white = (255, 255, 255)
		yellow = (255, 255, 0)
		black = (0, 0, 0)
		self.replace_color(white, yellow)
		self.blacken_everything_except(yellow)
		self.fill_gaps()

	def __isBlankColumn(self, column_number):
		black = (0, 0, 0)
		for y in range(self.height):
			if self.pixels[column_number, y] != black:
				return False
		return True

	def collect_character_imageList(self):
		self.char_images = []
		startX = None
		c = 0
		while c < self.width - 1:
			isCharFound = False
			for current_column in range(c, self.width):
				c = current_column
				if not self.__isBlankColumn(current_column):
					startX = current_column
					isCharFound = True
					break
			if isCharFound == False:
				break
			#
			for current_column in range(startX, self.width):
				c = current_column
				if self.__isBlankColumn(current_column) or current_column == self.width - 1:
					endX = current_column
					break
			#---------------------------------------------------------
			charImage = self.image.crop((startX, 0, endX, self.height))
			pixels = charImage.load()
			w, h = charImage.size
			for y in range(h):
				if len([pixels[i,y] for i in range(w) if pixels[i,y] == (255, 255, 0)]) > 0:
					startY = y
					break
			for y in reversed(range(0, h)):
				if len([pixels[i,y] for i in range(w) if pixels[i,y] == (255, 255, 0)]) > 0:
					endY = y
					break
			charImage = charImage.crop((0, startY, w, endY))
			bg = Image.open('bg.jpg')
			bg.paste(charImage, (0, 0))
			charImage = bg
			#---------------------------------------------------------
			self.char_images.append(charImage)

	def get_JCaptchaCharacterImage_List(self):
		jcaptcha_char_images = []
		for char_image in self.char_images:
			jcaptcha_char_images.append(JCaptchaCharacterImage(char_image))
		return jcaptcha_char_images

	def showImage(self):
		self.image.show()

	def saveImage(self, filename):
		self.image.save(filename)

#####
#####

def main():
	image = JCaptchaImage(input('Enter image name: '))
	image.treat()
	image.showImage()
	image.collect_character_imageList()
	image.char_images[0].show()

if __name__ == '__main__':
	main()