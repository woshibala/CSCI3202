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
	emission = []
	for n in range(26):
		emission.append([])
		for m in range(26):
			emission[n].append(0)
	transition = []
	for n in range(26):
		transition.append([])
		for m in range(26):
			transition[n].append(0)

	i = 0
	while i < len(state):
		if not state[i] == "_":
			emission[ord(state[i])-97][ord(output[i])-97] += 1
			if i+1 < len(state):
				transition[ord(state[i])-97][ord(state[i+1])-97] += 1
		i += 1
	e_probability = []
	for n in range(26):
		e_probability.append([])
		for m in range(26):
			e_probability[n].append(0)
	t_probability = []
	for n in range(26):
		t_probability.append([])
		for m in range(26):
			t_probability[n].append(0)
	i = 0
	while i < 26:
		e_deno = 0
		for x in emission[i]:
			e_deno += x
		t_deno = 0
		for x in transition[i]:
			t_deno += x

		j = 0
		normal = 0.0
		while j < 26:
			#emission probability
			e_probability[i][j] = (1.0+emission[i][j])/(26.0+e_deno)
			#normal += (1.0+emission[i][j])/(26.0+e_deno)
			#transition probability
			t_probability[i][j] = (1.0+transition[i][j])/(26.0+t_deno)
			normal += (1.0+transition[i][j])/(26.0+t_deno)
			j += 1
		print i,normal
		i += 1

	








def run():
	input()
	HMM()
run()