import getopt,sys

def input():
	args = sys.argv
	del args[0]
	optlist,args = getopt.getopt(args,'g:j:m:p:')
	print optlist
	option = optlist[0][0]
	arguments = optlist[0][1]
	if option == "-g":
		conditional(arguments)
	elif option == "-j":
		joint(arguments)
	elif option == "-m":
		marginal(marginal)
	else:
		setprior(arguments)


def conditional(a):
	print a
	print a.split(0,"|")

def joint(a):
	print a

def marginal(a):
	print a

def setprior(a):
	print a

input()