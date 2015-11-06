
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
	file = open("ps.txt")
	ps = float(file.readline().split()[0])
	graph = {'p':[[],["c"],[0.1,0.9],["x","d"]],'s':[[],["c"],[ps,1-ps],["x","d"]],'c':[["p","s"],["x","d"],[0.05,0.02,0.03,0.001]],'x':[["c"],[],[0.9,0.2]],'d':[["c"],[],[0.65,0.3]]};
	#graph["c"][2] => p=h&s=t 0.05; hf 0.02; lt 0.03; lf 0.001                                                         p(x|c)=0.9 p(x|~c)=0.2     p(d|c)=0.65 p(d|~c)=0.3
	#A:[[parents],[children]]
	file.close()
	#print o,a
	if o == "-m":
		A = a
		if len(graph[A][0]) == 0:#A is pollution and smoker
			result = marginal1(A)
			print result
		elif len(graph[A][1]) == 0:#X-ray and Dyapnose
			print marginal2(A,"c")
		else:#cancer
			print marginal3(A,"p","s")
	elif o == "-g":
		A = a.split("/")[0]
		B = a.split("/")[1]
		print A,B
		if A == B:
			#print 1
			return 
		if len(graph[A][0]) == 0:#A is pollution and smoker
			if A == "p" and B == "ds":
				#print "dsdsdsdsdsdsds"
				print cdt12(A,B)
			if B in graph[A][1]:#B is cancer ?intercausal
				print conditional4(A,B) #s|c p|s
			elif B in graph[A][3]:#B is x-ray or dyapmose combined 
			#s|d p|d
				if A == "s" and B == "d":
					print conditional8(A,B)
				elif A == "p" and B == "d":
					#print  "hjghjgjhg"
					print cdt(A,B)
			elif B == "s":
				print marginal1(A)*marginal1(B)/marginal1(B)
			elif B == "cs":
				#print "cssccscscscssscssc"
				print cdt12(A,B)

		elif len(graph[A][1]) == 0:#A is X-ray and Dyapnose
			#print "h"
			if A == "x" and B == "ds":
				print cdt12(A,B)
				return
			if A == "x" and B == "cs":
				print cdt12(A,B)
				return 
			if A == "d" and B == "cs":
				print conditional2(A,"c")
				return 
			if A == "x" and B == "d":
				print cdt12(A,B)
				return
			if len(graph[B]) == 4 and A in graph[B][3]:#d|s d|p x|s x|p
				#print A,B,"jgkhjgjgk"
				print conditional6(A,B)
			elif A == "d" and B == "c":
				#print "sadadsfafa"#d|c
				print conditional2(A,B)	
		else:#A is cancer 
			if A == "c" and B == "ds":
				#print "dsdsdsdccccc"
				print cdt12(A,B)
				return 
			if B in graph[A][0]:#B is cancer's parent
				print conditional5(A,B)
			else:
				#print "dhakjdhakchlakjs"
				print conditional5(A,B)
	else:
		print "set s as",a
		graph["s"][2][0] = float(a)
		graph["s"][2][1] = 1 - float(a)
		file = open("ps.txt","w")
		file.write(a)
		file.close()



def conditional4(A,B):
	result = conditional5(B,A)*marginal1(A)/marginal3("c","p","s")
	return result

def conditional8(A,B):
	#print "c8",A,B
	#print conditional6(B,A),marginal1(A),marginal1(B)
	#P(d|s)P(s)/P(d|s)P(s)+P(d|~s)P(~s)
	#P(d|p)P(p)/P(d|p)P(p)+P(d|~p)p(~p)
	result = conditional6(B,A)*marginal1(A)/(conditional6(B,A)*marginal1(A)+conditional6(B,"~"+A)*(1-marginal1(A)))
	return result
def conditional6(A,B):#d|s d|p x|s x|p
	#print "c6",A,B
	if A == "d" and B == "s":
		r1 = joint4(A,B,"c","p")
		r2 = joint3(B,"c","p")
		return r1/r2
	elif A == "x" and B =="s":
		r1 = joint4(A,B,"c","p")
		r2 = joint3(B,"c","p")
		return r1/r2
	elif A == "d" and B == "~s":
		r1 = joint4n(A,B[1:],"c","p")
		r2 = joint3n(B[1:],"c","p")
		return r1/r2
	elif A == "d" and B == "p":
		r1 = joint4(A,B,"c","s")
		r2 = joint3(B,"c","s")
		return r1/r2

def cdt(A,B):
	#print "cdt",A,B
	r1 = joint2(A,B)
	r2 = marginal2(B,"c")
	return r1/r2

def cdt12(A,B):
	if A == "p" and B == "cs":
		r1 = jnt3(A,B)
		r2  = joint2("c","s")
		return r1/r2
	elif A == "x" and B == "cs":
		r1 = jnt3(A,B)
		r2 = joint2("c","s")
		return r1/r2
	elif A == "p" and B == "ds":
		r1 = jnt3(A,B)
		r2 = joint2("s","d")
		return r1/r2
	elif A == "c" and B == "ds":
		r1 = jnt3(A,B)
		r2 = joint2("s","d")
		return r1/r2
	elif A == "x" and B == "ds":
		r1 = jnt3(A,B)
		r2 = joint2("s","d")
		return r1/r2
	elif A == "x" and B == "d":
		r1 = graph["x"][2][0]*graph["d"][2][0]*marginal3("c","p","s")+graph["x"][2][1]*graph["d"][2][1]*(1-marginal3("c","p","s"))
		r2 = marginal2(B,"c")
		return r1/r2
def jnt3(A,B):
	if A == "p" and B == "cs":
		return cgivenps("c","p","s")*marginal1("p")*marginal1("s")
	elif A == "p" and B == "ds":
		r1 = conditional2("d","c")*cgivenps("c","p","s")*marginal1("p")*marginal1("s")
		r2 = conditional2("d","~c")*(1-cgivenps("c","p","s"))*marginal1("p")*marginal1("s")
		#print "rrrrrrrrrrrrrrrrrrrrrr",r1+r2
		return r1+r2
	elif A == "c" and B == "ds":
		r1 = conditional2("d","c")*cgivenps("c","p","s")*marginal1("p")*marginal1("s")
		r2 = conditional2("d","c")*cgivenps("c","~p","s")*(1-marginal1("p"))*marginal1("s")
		return r1+r2
	elif A == "x" and B == "ds":
		r1 = graph["x"][2][0]*graph["d"][2][0]*cgivenps("c","p","s")*marginal1("s")*marginal1("p")
		r2 = graph["x"][2][0]*graph["d"][2][0]*cgivenps("c","~p","s")*marginal1("s")*(1-marginal1("p"))
		r3 = graph["x"][2][1]*graph["d"][2][1]*(1-cgivenps("c","p","s"))*marginal1("s")*marginal1("p")
		r4 = graph["x"][2][1]*graph["d"][2][1]*(1-cgivenps("c","~p","s"))*marginal1("s")*(1-marginal1("p"))
		return r1+r2+r3+r4
	elif A == "x" and B == "cs":
		return graph[A][2][0]*cgivenps("c","p","s")*marginal1("s")*marginal1("p")+graph[A][2][0]*cgivenps("c","~p","s")*marginal1("s")*(1-marginal1("p"))
def cgivenps(A,B,C):
	if A == "c":
		if B == "p" and C == "s":
			return 0.05
		if B == "p" and C == "~s":
			return 0.02
		if  B == "~p" and C == "s":
			return 0.03
		if B == "~p" and C == "~s":
			return 0.001
def joint2(A,B):
	if A == "p" and B == "d":
		a = conditional2("d","c")
		b = conditional2("d","~c")
		print a,b
		r1 = cgivenps("c","p","s")
		r2 = cgivenps("c","p","~s")
		r3 = cgivenps("c","~p","s")
		r4 = cgivenps("c","~p","~s")
		e1 = a*r1*marginal1("p")*marginal1("s")
		e2 = a*r2*marginal1("p")*(1-marginal1("s"))
		e3 = b*(1-r1)*marginal1("p")*marginal1("s")
		e4 = b*(1-r2)*marginal1("p")*(1-marginal1("s"))
		return e1+e2+e3+e4
	elif A == "s" and B == "d":
		a = conditional2("d","c")
		b = conditional2("d","~c")
		print a,b
		r1 = cgivenps("c","p","s")
		r2 = cgivenps("c","~p","s")
		e1 = a*r1*marginal1("s")*marginal1("p")
		e2 = a*r2*marginal1("s")*(1-marginal1("p"))
		e3 = b*(1-r1)*marginal1("s")*marginal1("p")
		e4 = b*(1-r2)*marginal1("s")*(1-marginal1("p"))
		return e1+e2+e3+e4
	elif A == "c" and B == "s":
		a = cgivenps("c","p","s")
		b = cgivenps("c","~p","s")
		e1 = a*marginal1("s")*marginal1("p")
		e2 = b*marginal1("s")*(1-marginal1("p"))
		return e1 + e2  


def joint3n(B,C,D):
	#print "j3",B,C,D
	r1 = conditional3(C,D,"~"+B)*marginal1(D)*(1-marginal1(B))
	r2 = conditional3(C,"~"+D,"~"+B)*(1-marginal1(D))*(1-marginal1(B))
	r3 = (1-conditional3(C,D,"`"+B))*marginal1(D)*(1-marginal1(B))
	r4 = (1-conditional3(C,"~"+D,"~"+B))*(1-marginal1(D))*(1-marginal1(B))
	#print "j3",r1+r2+r3+r4
	return r1+r2+r3+r4
def joint4n(A,B,C,D):#P(d,s,C,P)
	#P(d|c) P(x|c)
	#print "j4",A,B,C,D
	r1 = conditional2(A,C)*conditional3(C,D,"~"+B)*marginal1(D)*(1-marginal1(B))
	#print r1
	r2 = conditional2(A,C)*conditional3(C,"~"+D,"~"+B)*(1-marginal1(D))*(1-marginal1(B))
	#print r2
	r3 = conditional2(A,"~"+C)*(1-conditional3(C,D,"~"+B))*marginal1(D)*(1-marginal1(B))
	#print r3
	r4 = conditional2(A,"~"+C)*(1-conditional3(C,"~"+D,"~"+B))*(1-marginal1(D))*(1-marginal1(B))
	#print r4
	#print "j4",r1+r2+r3+r4
	return r1+r2+r3+r4
def joint3(B,C,D):
	#print "j3",B,C,D
	r1 = conditional3(C,D,B)*marginal1(D)*marginal1(B)
	r2 = conditional3(C,"~"+D,B)*(1-marginal1(D))*marginal1(B)
	r3 = (1-conditional3(C,D,B))*marginal1(D)*marginal1(B)
	r4 = (1-conditional3(C,"~"+D,B))*(1-marginal1(D))*marginal1(B)
	#print "j3",r1+r2+r3+r4
	return r1+r2+r3+r4
def joint4(A,B,C,D):#P(d,s,C,P)
	#P(d|c) P(x|c)
	#print "j4",A,B,C,D
	r1 = conditional2(A,C)*conditional3(C,D,B)*marginal1(D)*marginal1(B) 
	#print r1
	r2 = conditional2(A,C)*conditional3(C,"~"+D,B)*(1-marginal1(D))*marginal1(B)
	#print r2
	r3 = conditional2(A,"~"+C)*(1-conditional3(C,D,B))*marginal1(D)*marginal1(B)
	#print r3
	r4 = conditional2(A,"~"+C)*(1-conditional3(C,"~"+D,B))*(1-marginal1(D))*marginal1(B)
	#print r4
	#print "j4",r1+r2+r3+r4
	return r1+r2+r3+r4
def conditional2(A,B):
	#print "c2",A
	#print "c2",B
	if B[1:] in graph[A][0] or B in graph[A][0]:#diagnostic c x|c
		#print A," is ",B,"'parent"
		if B == "c":
			return graph[A][2][0]
		else: #B == "~c"
			return graph[A][2][1]
	elif A in graph[B][1]:#predictive c|s
		print "here"
	elif A == "d" and  B == "c":
		return graph[A][2][0]
	elif A == "d" and B == "~c":
		return graph[A][2][1]

def conditional5(A,B):
	#print "c5",A
	#print "c5",B
	if B[1:] in graph[A][0] or B in graph[A][0]:#diagnostic c P(c|s) = P(c|p,s)P(p)+P(c|~p,s)P(~p)
		#print A," is ",B,"'parent"
		if  B == "s":
			return conditional3(A,"p",B)*marginal1("p")+conditional3(A,"~p",B)*(1-marginal1("p"))
		elif B == "p":#P(c|p) = P(c|p,s)P(s)+P(c|p,~s)P(~s)
		 	#print conditional3(A,B,"s"),marginal1("s"),conditional3(A,"~s",B),(1-marginal1("s"))
			return conditional3(A,B,"s")*marginal1("s")+conditional3(A,"~s",B)*(1-marginal1("s"))
	elif A == "c" and B == "d":
		r1 = conditional2(B,A)
		r2 = marginal3("c","p","s")
		r3 = marginal2("d","c")
		return r1*r2/r3


def conditional3(A,B,C):#P(A|B C)
	#print A,B,C
	if A =="c":
		if B == "~p" and C == "s":
			return graph[A][2][2]
		elif B == "~p" and C == "~s":
			return graph[A][2][3]
		elif B == "p" and C == "s":
			return graph[A][2][0]
		else:
			return graph[A][2][1]

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
