execfile('StrokeHmmbasic.py')
a = HMM(1,1,1,1)
data = [{'length': 0}, {'length': 1}]
result = a.label(data)
print result 