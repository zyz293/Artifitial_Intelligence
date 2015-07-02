execfile('bayes.py')
a = Bayes_Classifier()
# a.__init__()
result = a.classify('I love my AI class!')
print result

# import os
# positive = 0
# negative = 0
# neutral = 0
# File = []
# for obj in os.walk('movies_reviews/'):
# 	File = obj[2]
# 	break
# for txt in File:
# 	file = 'movies_reviews/%s' % str(txt)
	
# file = 'movies_reviews\movies-5-24826.txt'
# 	text = a.loadFile(file)
# print text
# 	result = a.classify(text)
	# print result


	
# 	if result == 'positive':
# 		positive += 1
# 	elif result == 'negative':
# 		negative += 1
# 	elif result == 'neutral':
# 		neutral += 1
# print 'positive: ' ,positive 
# print 'negative: ' ,negative 
# print 'neutral: ' ,neutral 

# text = a.loadFile(file)
# print text
# print a.tokenize(text)



# for word in a.tokenize(text):
	# print word
# a.save('you',file)
# print a.load(file)
