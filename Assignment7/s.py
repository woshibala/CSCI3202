#
import sys
randomNo = None
def input():
	global randomNo
	file = open("sample.txt")
	line = file.readline()
	randomNo = []
	while not line == "":
		randomNo.append(float(line.split()[0]))
		line = file.readline()
	
def priorSample():
	global randomNo 
	print "Prior sample: "
	p_sample = []
	n = 0
	while n < 99:
		c = randomNo[n]
		n += 1
		s = randomNo[n]
		n += 1
		r = randomNo[n]
		n += 1
		w = randomNo[n]
		#0<=c<0.5:T 0.5<=c<1.0: F
		if c >= 0 and c < 0.5:
			c = True
		elif c >= 0.5 and c < 1:
			c = False
		#if c== True 0<=s<0.1:True 0.1<=s<1:False 
		if c == True:
			if  s >= 0 and s < 0.1:
				s = True
			else:
				s = False
		else:#if c = False 0<=s<0.5:True 0.5<=s<1:False
			if s >= 0 and s < 0.5:
				s = True
			else:
				s = False
		#if r==True 0<=r<0.8:True 0.8<=r<1:False
		if c == True:
			if r >= 0 and r < 0.8:
				r = True
			else:
				r = False
		else:#if r==False 0<=r<0.2:True 0.2<=r<1:False
			if r >= 0 and r <= 0.2:
				r = True
			else:
				r = False

		if s == True and r == True:
			if w >= 0 and w < 0.99:
				w = True
			else:
				w = False
		elif s == True and r == False:
			if w >= 0 and w < 0.90:
				w = True
			else:
				w = False
		elif s == False and r == True:
			if w >= 0 and w < 0.90:
				w = True
			else:
				w = False
		else:
			 w = False

		p_sample.append([c,s,r,w])
		n += 1

	p = 0.0
	q = 0.0
	for i in p_sample:
		q += 1
		if i[0] == True:
			p += 1
	print "P(c = true) =",p/q
	p = 0.0
	q = 0.0
	for i in p_sample:
		if i[2] == True:
			q += 1
			if i[0] == True:
				p += 1
	print "P(c = true|rain = true) =",p/q
	p = 0.0
	q = 0.0
	for i in p_sample:
		if i[3] == True:
			q += 1
			if i[1] == True:
				p += 1
	print "P(s = true|w = true) =",p/q
	p = 0.0
	q = 0.0
	for i in p_sample:
		if i[0] == True and  i[3] == True:
			q += 1
			if i[1] == True:
				p += 1
	print "P(s = true|c = true, w = true) =",p/q

def rejectionSample():
	global randomNo
	print "Rejection sample:"
	#P(c = true)
	p = 0.0
	q = 0.0
	for i in randomNo:
		q += 1
		if i >= 0 and i < 0.5:
			p += 1
	print "P(c = true) =",p/q
	#p(c = true|rain = true)
	p = 0.0
	q = 0.0
	n = 0
	while n < 99:
		c = randomNo[n]
		n += 1
		r = randomNo[n]
		n += 1
		if c >= 0 and c < 0.5:
			if r >= 0 and r < 0.8:
				p += 1
				q += 1
		else:
			if r >= 0 and r < 0.2:
				q += 1
	print "p(c = true|rain = true) =",p/q
	#P(s|w)
	p = 0.0
	q = 0.0
	n = 0
	while n < 95:
		c = randomNo[n]
		n += 1
		r = randomNo[n]
		n += 1
		s = randomNo[n]
		n += 1
		w = randomNo[n]
		n += 1
		if c >= 0 and c < 0.5:
			if s >= 0 and s < 0.1:
				if r >= 0 and r < 0.8:
					if w >= 0 and w < 0.99:
						p += 1
						q += 1
				else:
					if w >= 0 and  w < 0.9:
						p += 1
						q += 1
			else:
				if r >= 0 and r < 0.8:
					if w >= 0 and w < 0.9:
						q += 1
		else: 
			if s >= 0 and s < 0.5:
				if r >= 0 and r < 0.2:
					if w >= 0 and w < 0.99:
						p += 1
						q += 1
				else:
					if w >= 0 and  w < 0.9:
						p += 1
						q += 1
			else:
				if r >= 0 and r < 0.2:
					if w >= 0 and w < 0.9:
						q += 1
	print "P(s = true|w = true) =",p/q
	#P(s = true| c = true , w = true)
	p = 0.0
	q = 0.0
	n = 0
	while n < 95:
		c = randomNo[n]
		n += 1
		r = randomNo[n]
		n += 1
		s = randomNo[n]
		n += 1
		w = randomNo[n]
		n += 1
		if c >= 0 and c < 0.5:
			if s >= 0 and s < 0.1:
				if r >= 0 and r < 0.8:
					if w >= 0 and w < 0.99:
						p += 1
						q += 1
				else:
					if w >= 0 and  w < 0.9:
						p += 1
						q += 1
			else:
				if r >= 0 and r < 0.8:
					if w >= 0 and w < 0.9:
						q += 1
	print "P(s = true|c = true, w = true) =",p/q
		
def run():
	input()
	priorSample()
	print "***********************"
	rejectionSample()
run()