import numpy, json

class NaiveBayesClassifier:
	def __init__(self):
		pass

	def start_training(self):
		print('Started training...')
		training_X = numpy.array([csv_line.split(',') for csv_line in open('Collected Training Data/training_X.csv').read().strip().split('\n')]).astype(numpy.int)
		training_Y = open('Collected Training Data/training_Y.csv').read().strip().split('\n')
		#---
		classes = 'abcdefghijklmnopqrstuvwxyz0123456789'
		probabilities_dict = {}
		probabilities_dict['class_probs'] = []
		probabilities_dict['0'] = {}
		probabilities_dict['1'] = {}
		#---
		progress_count = 0
		#---
		for _class in classes:
			current_class_matrix = numpy.array([list(training_X[i]) for i in range(len(training_X)) if training_Y[i] == _class])
			probabilities_dict['1'][_class] = (current_class_matrix.sum(axis=0) + 1) / (len(current_class_matrix) + 36)
			probabilities_dict['0'][_class] = 1 - probabilities_dict['1'][_class]
			#---jsonify---
			probabilities_dict['0'][_class] = probabilities_dict['0'][_class].tolist()
			probabilities_dict['1'][_class] = probabilities_dict['1'][_class].tolist()
			probabilities_dict['class_probs'].append(open('Collected Training Data/training_Y.csv').read().count(_class) / float(len(training_Y)))
			#-------------
			progress_count += 1
			print('- Training progress:', str(progress_count * 100 / 36), '%')
		print('====================')
		print(' Training Complete!')
		open('Trained Model/brain.json', 'w').write(json.dumps(probabilities_dict, indent=4, sort_keys=True))
		print('- Saved Trained Model/brain.json')

	def getClassification(self, jchar_csv):
		probabilities_dict = json.loads(open('brain.json', 'r').read())
		#
		probs_class_given_features = {}
		#
		class_index = 0
		for _class in self.classes:
			feature_index = 0
			probs_class_given_features[_class] = probabilities_dict['class_probs'][class_index]
			for feature in jchar_csv.split(','):
				probs_class_given_features[_class] *= probabilities_dict[feature][_class][feature_index]
				feature_index += 1
			class_index += 1
		#
		maximum_prob = max(probs_class_given_features.values())
		max_keys = []
		for key in probs_class_given_features.keys():
			if probs_class_given_features[key] == maximum_prob:
				max_keys.append(key)
		return max_keys[0]


######
######
######

def main():
	classifier = NaiveBayesClassifier()
	testList = open('sample.csv', 'r').read().strip().split('\n')
	for t in testList:
		print('solution:', classifier.getClassification(t))

if __name__ == '__main__':
	main()