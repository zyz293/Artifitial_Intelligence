execfile('StrokeHmm1.py')
a = StrokeLabeler()
# a.trainHMMDir('trainingFiles/')
result = a.confusioninput('trainingFiles/')

print '*' * 80
print 'table: ' ,result
print '*' * 80