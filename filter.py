def filter(func,iterable):
	"""This function takes a function as an argument and an iterable like a list,dict..
		as second argument and returns list of elements which return true when applied on the func."""
	answer = []
	for i in iterable:
		if(func(i)):
			answer.append(i)

	return answer

#a check function to test the filter function
def check(a):
	return a%2

print(filter(check,[1,2,3,4,5,6,7,8,9]))