import getopt, sys
args = None
flag = None
def input():
	global args,flag
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
	global args,flag
	graph = {P:[[],["C"]],S:[[],["C"]],C:[["P","S"],["X","D"]],X:[["C"],[]],D:[["C"],[]]};
	if flag == "-g":
		Q = args.split("|",0)
		E = args.split("|",1)
		print Q,E






def run():
	input()
	main()
