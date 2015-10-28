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
			print "args",  
		else:
			assert False, "unhandled option"

def main():
	global o,a,graph
	result = None
	graph = {'p':[[],["c"],[0.9,0.1],'s':[[],["c"],[0.3,0.7]],'c':[["p","s"],["x","d"],[0.05,0.02,0.03,0.001]],'x':[["c"],[]],'d':[["c"],[]]}
	#graph["c"][2] => p=h&s=t 0.05; hf 0.02; lt 0.03; lf 0.001
	#A:[[parents],[children]]
	print o,a
	if o == "-m":
		A = a
		if len(graph[A][0]) == 0:#pollution and smoker
			result = graph[A][2][0]
			print result
		elif len(graph[A][1]) == 0:#X-ray and Dyapnose
			marginal(A,"c")
		else:#cancer
			marginal(A,"p","s")
	if o == "-g":
		A = a.split("/",1)[0]
		B = a.split("/",1)[1]
		conditional()
		




def conditional(A,B):
	print A
	print B
	if B in graph[A][0]:#diagnostic
		print A," is ",B,"'parent"
		
	elif A in graph[B][0]:#predictive
		print B," is ",A,"'parent"
def conditional(A,B,C):#P(A|B C)
	print A,B,C
	if B == "~p" and C == "s":
		return graph[A][2][0]
	elif B == "~p" and C == "~s":
		return graph[A][2][1]
	elif B == "p" and C == "s":
		return graph[A][2][2]
	else:
		return graph[A][2][3]






def marginal(A,B):
	global graph
	PC = marginal("c","p","s")


def marginal(A,B,C):
	global graph
	r1 = conditional("c","p","s")*graph[B][2][0]*graph[C][2][0]
	r2 = conditional("c","p","~s")*graph[B][2][0]*graph[C][2][1]
	r3 = conditional("c","~p","s")*graph[B][2][1]*graph[C][2][0]
	r4 = conditional("c","~p","~s")*graph[B][2][1]*graph[C][2][1]
	print r1+r2+r3+r4








def run():
	input()
	main()

run()