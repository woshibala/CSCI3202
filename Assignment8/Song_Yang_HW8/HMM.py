state = None
output = None
def input():
	global state,output
	file = open("typos20.data")
	line = file.readline()
	state = []
	output = []
	while line != "":
		state.append(line.split()[0])
		output.append(line.split()[1])
		line = file.readline()

def HMM():
	global state,output
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
				#normal += (1.0+emission[i][j])/(26.0+e_deno)
				#transition probability
				t_probability[i][j] = (1.0+transition[i][j])/(27.0+t_deno)
				normal += (1.0+transition[i][j])/(27.0+t_deno)
			j += 1
		#print i,normal
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
	print "Emission probability: "
	while i < 28:
		j = 0
		while j < 28:
			if i != 1 and j != 1:
				print "P(",str(unichr(j+95)),"|",str(unichr(i+95)),") =",e_probability[i][j]
				e.writelines("P("+str(unichr(j+95))+"|"+str(unichr(i+95))+") = "+str(e_probability[i][j])+"\n")
			j += 1
		i += 1
	i = 0
	j = 0
	e.close()
	t = open("transitionalprobability.txt","w")
	t.writelines("transitional probability: \n")
	print "transitional probability:"
	while i < 28:
		j = 0
		while j < 28:
			if i != 1 and j != 1:
				print "P(",str(unichr(i+95)),"|",str(unichr(j+95)),") =",t_probability[i][j]
				t.write("P("+str(unichr(i+95))+"|"+str(unichr(j+95))+") = "+str(t_probability[i][j])+"\n")
			j += 1
		i += 1
	t.close()
	ini = open("initialprobability.txt","w")
	ini.writelines("Initial probability: \n")
	i = 0
	while i < 28:
		if i != 1:
			print "P(",str(unichr(i+95)),") =",i_probability[i]
			ini.write("Pi("+str(unichr(i+95))+") = "+str(i_probability[i])+"\n")
		i += 1
	ini.close()
	
	






 

def run():
	input()
	HMM()
run()