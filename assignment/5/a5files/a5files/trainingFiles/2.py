execfile('StrokeHmmbasic_XL.py')
a = StrokeLabeler()
# a.trainHMMDir('trainingFiles/')
result = a.confusioninput('trainingFiles/')

print '*' * 80
print 'table: ' ,result