import getopt, sys
graph = None
a = None
o = None
def input():
	global o,a
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)
	for o, a in opts:
		if o in ("-p"):
			print "flag", o
			print "args", a
			print a[0]
			print float(a[1:])
			#setting the prior here works if the Bayes net is already built
			#setPrior(a[0], float(a[1:])
		elif o in ("-m"):
			print "flag", o
			print "args", a
			print type(a)
			#calcMarginal(a)
		elif o in ("-g"):
			print "flag", o
			print "args", a
			print type(a)
			'''you may want to parse a here and pass the left of |
			and right of | as arguments to calcConditional
			'''
			p = a.find("|")
			print a[:p]
			print a[p+1:]
			#calcConditional(a[:p], a[p+1:])
		elif o in ("-j"):
			print "flag", o
			print "args", a
		else:
			assert False, "unhandled option"

def main():
	global o,a,graph
	result = None
	graph = {'p':[[],["c"],[0.9,0.1]],'s':[[],["c"],[0.3,0.7]],'c':[["p","s"],["x","d"],[0.05,0.02,0.03,0.001]],'x':[["c"],[],[0.9,0.2]],'d':[["c"],[],[0.65,0.3]]};
	#graph["c"][2] => p=h&s=t 0.05; hf 0.02; lt 0.03; lf 0.001                                                         p(x|c)=0.9 p(x|~c)=0.2     p(d|c)=0.65 p(d|~c)=0.3
 	given = {"p":0.9}
	#A:[[parents],[children]]
	print o,a
	if o == "-m":
		A = a
		if len(graph[A][0]) == 0:#pollution and smoker
			result = marginal1(A)
			print result
		elif len(graph[A][1]) == 0:#X-ray and Dyapnose
			print marginal2(A,"c")
		else:#cancer
			print marginal3(A,"p","s")
	if o == "-g":
		A = a.split("/",1)[0]
		B = a.split("/",1)[1]
		conditional()
		




def conditional2(A,B):
	print A
	print B
	if B[1:] in graph[A][0] or B in graph[A][0]:#diagnostic c
		print A," is ",B,"'parent"
		if B == "c":
			return graph[A][2][0]
		else:
			return graph[A][2][1]
	elif A in graph[B][1]:#predictive
		return 
def conditional3(A,B,C):#P(A|B C)
	#print A,B,C
	if B == "~p" and C == "s":
		return graph[A][2][0]
	elif B == "~p" and C == "~s":
		return graph[A][2][1]
	elif B == "p" and C == "s":
		return graph[A][2][2]
	else:
		return graph[A][2][3]




def marginal1(A):
	global graph
	return graph[A][2][0]

def marginal2(A,B):
	global graph
	PC = marginal3("c","p","s")
	r1 = conditional2(A,B)*marginal3(B,"p","s")  #p(x|c)p(c)
	r2 = conditional2(A,"~"+B)*(1-marginal3(B,"p","s"))#p(x|~c)p(~c)
	return r1+r2


def marginal3(A,B,C):
	global graph
	r1 = conditional3("c","p","s")*graph[B][2][0]*graph[C][2][0]
	r2 = conditional3("c","p","~s")*graph[B][2][0]*graph[C][2][1]
	r3 = conditional3("c","~p","s")*graph[B][2][1]*graph[C][2][0]
	r4 = conditional3("c","~p","~s")*graph[B][2][1]*graph[C][2][1]
	return r1+r2+r3+r4








def run():
	input()
	main()

run()