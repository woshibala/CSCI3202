import math
state = None
output = None
evidence = None
original = None
i_probability = None
e_probability = None
t_probability = None
def input():
	global state,output,evidence,original
	file = open("typos20.data")
	line = file.readline()
	state = []
	output = []
	while line != "":
		state.append(line.split()[0])
		output.append(line.split()[1])
		#print line.split()[1]
		line = file.readline()
	file.close()

	e = open("typos20Test.data")
	e.readline()
	line = e.readline()
	evidence = []
	original = []
	while line != "":
		original.append(line.split()[0])
		evidence.append(line.split()[1])
		#print line.split()[1]
		line = e.readline()
	e.close()


def HMM():
	global state,output,i_probability,e_probability,t_probability
	#asc95: "_";asc96: "`";asc97: "a"
	emission = []
	for n in range(28):
		emission.append([])
		for m in range(28):
			emission[n].append(0)
	transition = []
	for n in range(28):
		transition.append([])
		for m in range(28):
			transition[n].append(0)
	initial = []
	i_probability = []
	for n in range(28):
		initial.append(0)
		i_probability.append(0)

	i = 0
	while i < len(state):
		emission[ord(state[i])-95][ord(output[i])-95] += 1
		initial[ord(state[i])-95] += 1
		if i+1 < len(state):
			transition[ord(state[i])-95][ord(state[i+1])-95] += 1
			#P(X-1|X)
		i += 1
	e_probability = []
	for n in range(28):
		e_probability.append([])
		for m in range(28):
			e_probability[n].append(0)
	t_probability = []
	for n in range(28):
		t_probability.append([])
		for m in range(28):
			t_probability[n].append(0)
	i = 0
	while i < 28:
		#get denominator
		e_deno = 0
		for x in emission[i]:
				e_deno += x
		t_deno = 0
		for x in transition[i]:
				t_deno += x

		j = 0
		normal = 0.0
		while j < 28:
			if i != 1 and j != 1:
				#emission probability
				e_probability[i][j] = (1.0+emission[i][j])/(27.0+e_deno)
		
				#transition probability
				t_probability[i][j] = (1.0+transition[i][j])/(27.0+t_deno)
	
			j += 1
		
		i += 1
	#calculate i_probability
	i_deno = 0
	for i in initial:
		i_deno += i
	i = 0
	while i < 28:
		if i != 1:
			i_probability[i]= (1.0+initial[i])/(27.0+i_deno)
		i += 1
	i = 0
	j = 0
	e = open("emissionprobability.txt","w")
	e.writelines("P( Et | Xt ): \n")
	#print "Emission probability: "
	while i < 28:
		j = 0
		while j < 28:
			if i != 1 and j != 1:
				#print "P(",str(unichr(j+95)),"|",str(unichr(i+95)),") =",e_probability[i][j]
				e.writelines("P("+str(unichr(j+95))+"|"+str(unichr(i+95))+") = "+str(e_probability[i][j])+"\n")
			j += 1
		i += 1
	i = 0
	j = 0
	e.close()
	t = open("transitionalprobability.txt","w")
	t.writelines("transitional probability: \n")
	#print "transitional probability:"
	while i < 28:
		j = 0
		while j < 28:
			if i != 1 and j != 1:
				#print "P(",str(unichr(i+95)),"|",str(unichr(j+95)),") =",t_probability[i][j]
				t.write("P("+str(unichr(i+95))+"|"+str(unichr(j+95))+") = "+str(t_probability[i][j])+"\n")
			j += 1
		i += 1
	t.close()
	ini = open("initialprobability.txt","w")
	ini.writelines("Initial probability: \n")
	i = 0
	while i < 28:
		if i != 1:
			#print "P(",str(unichr(i+95)),") =",i_probability[i]
			ini.write("Pi("+str(unichr(i+95))+") = "+str(i_probability[i])+"\n")
		i += 1
	ini.close()

def  viterbi():
	global i_probability,e_probability,t_probability,evidence,original
	statesequence = []

	#state 1:v1x1 = max{ P(E1 | x1)*Pi }
	l1 = []
	E1 = evidence[0]
	#print E1
	E1 = ord(E1)-95
	i = 0
	while i < len(i_probability):
		if i != 1:
			EgivenX = e_probability[i][E1]
			if i_probability[i] != 0 and EgivenX != 0:
				Pi = math.log(i_probability[i])
				EgivenX = math.log(EgivenX)
				l1.append(EgivenX + Pi)
		else:
			l1.append(float("-Inf"))
		i += 1
	v1x1 = unichr(l1.index(max(l1)) + 95)
	statesequence.append(v1x1)
	print v1x1

	#For other state: vtxt = max{P(Et|xt)*P(Xt|Xt-1)*v(t-1)x(t-1)}
	previousstate = []
	previousprobability = []
	r = 0
	while r < 28:
		previousstate.append(l1.index(max(l1)))
		r += 1
	previousprobability = l1

	paths = []
	i = 1
	while i < len(original):
		
		Et = ord(evidence[i])-95
	
		v_list = []
		j = 0
		while j < 28:#current state
			#P(Et|xt)*P(Xt|Xt-1)*v(t-1)x(t-1)
			v_list.append([])
			if j != 1 :
				k = 0
				while k < 28:#previous state
					if k != 1 and t_probability[k][j] != 0 and e_probability != 0:
						EgivenX = math.log(e_probability[j][Et])
						transition = math.log(t_probability[j][k])
						current = EgivenX + transition + previousprobability[j]
						v_list[j].append(current)
					else:
						v_list[j].append(float("-Inf"))
					k += 1
			j += 1
		
		#set previousstate and previousprobability
		p = 0
		while p < 28:
			
			if p != 1:
				q = 0
				l2 = []
				while q < 28:
					if q != 1:
						l2.append(v_list[q][p])
					else:
						l2.append(float("-Inf"))
					q += 1

				previousprobability[p] = (max(l2))
				previousstate[p] = l2.index(max(l2))

			else:
				previousprobability[p] = (float("-Inf"))
				previousstate[p] = -1
			p += 1
		
		a = []
		for aa in previousstate:
			a.append(aa)
		paths.append(a)
			
		i += 1
	
	
	reversesequence = []
	n = len(paths) - 2

	laststate = previousprobability.index(max(previousprobability))
	#print str(unichr(previousstate.index(max(previousstate))+95))
	print len(paths),len(original)
	while n >= 0:
		reversesequence.append(str(unichr(laststate + 95)))
		laststate = paths[n][laststate]
		n -= 1
	statesequence.append("n")
	while len(reversesequence):
		statesequence.append(reversesequence.pop())
	i = 0
	while i < len(statesequence):
		print statesequence[i],original[i]
		i += 1
	
	n = 0
	k = 0.0
	while n < len(statesequence):
		if statesequence[n] == original[n]:
			k += 1
		n += 1
	print "error rate after viterbi: ",1-k/n
	n = 0
	k = 0.0
	while n <len(original):
		if evidence[n] == original[n]:
			k += 1
		n += 1
	print "original error rate:",1-k/n

	file = open("result.txt","w")
	for i in statesequence:
		file.write(i)
	file.close()

def run():
	input()
	HMM()
	viterbi()

run()