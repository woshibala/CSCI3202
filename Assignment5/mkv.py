import sys,math
world = None
accuracy = None
policy = None
utility_current = None
total = 0

def input():
	global world,method,accuracy,total
	for i in range(0,len(sys.argv)):
		print i,": ",sys.argv[i]
	accuracy = 0.5#sys.argv[2]
	file = open("World1MDP.txt")#sys.argv[1]
	world = []
	line = file.readline()
	while line != "\n":
		line = line[:-1]
		#line = line[:-1]
		line = line.split(" ")
		for i in range(0,len(line)):
			line[i] = int(line[i])
		world.append(line)
		line = file.readline()
	for i in world:
		print i
def MDP():
	global world,accuracy,policy,utility_current
	input()
	length = len(world)
	width = len(world[0])
	#print length
	#print width
	utility = []
	policy = []
	for i in range(0,length):
		utility.append([])
		policy.append([])
		for j in range(0,width):
			policy[i].append("#")
			if world[i][j] == 0:
				utility[i].append(0)
			elif world[i][j] == 2:
				utility[i].append(-999)
			elif world[i][j] == 3:
				utility[i].append(-2)
			elif world[i][j] == 1:
				utility[i].append(-1)
			elif world[i][j] == 4:
				utility[i].append(1)
			else:
				utility[i].append(50)
	utility_current = []
	utility_previous = []
	utility_original = []
	for i in range(0,length):
		utility_original.append([])
		for j in range(0,width):
			utility_original[i].append(0)
			utility_original[i][j] = utility[i][j]
	for i in range(0,length):
		utility_current.append([])
		for j in range(0,width):
			utility_current[i].append(0)
			utility_current[i][j] = utility[i][j]
	for i in range(0,length):
		utility_previous.append([])
		for j in range(0,width):
			utility_previous[i].append(0)
			utility_previous[i][j] = utility[i][j]
	max_change = 1
	l = 0 
	while max_change >= (accuracy * (1-0.9)/0.9):
		l += 1
		for i in range(0,length):
			for j in range(0,width):
				utility_previous[i][j] = utility_current[i][j]
		for i in range(0,length):
			for j in range(0,width):
				if utility_original[i][j] == -999:#if the position is a wall
					utility_current[i][j] == -999
					continue
				else:
					policy_utility = []# up down left right
					#up
					if (i-1) >= 0 and world[i-1][j] != 2:#when up is in the world
						if (j-1) >= 0 and world[i][j-1] != 2:#if left is in the world
							if (j+1) < width and world[i][j+1] != 2:#if right is in the world
								up = 0.8*utility_previous[i-1][j] + 0.1*utility_previous[i][j-1] + 0.1*utility_previous[i][j+1]
							else:#if right is not in the world
								up = 0.8*utility_previous[i-1][j] + 0.1*utility_previous[i][j-1]
						else:#left is not in the world
							if (j+1) < width and world[i][j+1] != 2: #right is in the world
								up = 0.8*utility_previous[i-1][j] + 0.1*utility_previous[i][j+1]
							else:#both are not in the world
								up = 0.8*utility_previous[i-1][j]
					else:#when up is not in the world
						if (j-1) >= 0 and world[i][j-1] != 2:#if left is in the world
							if (j+1) < width and world[i][j+1] != 2:#if right is in the world
								up = 0.1*utility_previous[i][j-1] + 0.1*utility_previous[i][j+1]
							else:#if right is not in the world
								up = 0.1*utility_previous[i][j-1]
						else:#left is not in the world
							if (j+1) < width and world[i][j+1] != 2: #right is in the world
								up = 0.1*utility_previous[i][j+1]
							else:#both are not in the world
								up = 0
					policy_utility.append(up)
					#down
					if (i+1) < length and world[i+1][j] != 2:#when down is in the world
						if (j-1) >= 0 and world[i][j-1] != 2:#if left is in the world
							if (j+1) < width and world[i][j+1] != 2:#if right is in the world
								down = 0.8*utility_previous[i+1][j] + 0.1*utility_previous[i][j-1] + 0.1*utility_previous[i][j+1]
							else:#if right is not in the world
								down = 0.8*utility_previous[i+1][j] + 0.1*utility_previous[i][j-1]
						else:#left is not in the world
							if (j+1) < width and world[i][j+1] != 2: #right is in the world
								down = 0.8*utility_previous[i+1][j] + 0.1*utility_previous[i][j+1]
							else:#both are not in the world
								down = 0.8*utility_previous[i+1][j]
					else:#when down is not in the world
						if (j-1) >= 0 and world[i][j-1] != 2:#if left is in the world
							if (j+1) < width and world[i][j+1] != 2:#if right is in the world
								down = 0.1*utility_previous[i][j-1] + 0.1*utility_previous[i][j+1]
							else:#if right is not in the world
								down = 0.1*utility_previous[i][j-1]
						else:#left is not in the world
							if (j+1) < width and world[i][j+1] != 2: #right is in the world
								down = 0.1*utility_previous[i][j+1]
							else:#both are not in the world
								down = 0
					policy_utility.append(down)
					#left
					if (j-1) >= 0 and world[i][j-1] != 2:#when left is in the world
						if (i-1) >= 0 and world[i-1][j] != 2:#if up is in the world
							if (i+1) < length and world[i+1][j] != 2:#if down is in the world
								left = 0.8*utility_previous[i][j-1] + 0.1*utility_previous[i+1][j] + 0.1*utility_previous[i-1][j]
							else:#if down is not in the world
								left = 0.8*utility_previous[i][j-1] + 0.1*utility_previous[i-1][j]
						else:#if up is not in the world
							if (i+1) < length and world[i+1][j] != 2: #down is in the world
								left = 0.8*utility_previous[i][j-1] + 0.1*utility_previous[i+1][j]
							else:#both are not in the world
								left = 0.8*utility_previous[i][j-1]
					else:#when left is not in the world
						if (i-1) >= 0 and world[i-1][j] != 2:#if up is in the world
							if (i+1) < length and world[i+1][j] != 2:#if down is in the world
								left = 0.1*utility_previous[i+1][j]+0.1*utility_previous[i-1][j]
							else:#if down is not in the world
								left = 0.1*utility_previous[i-1][j]
						else:#up is not in the world
							if (i+1) < width and world[i+1][j] != 2: #down is in the world
								left = 0.1*utility_previous[i+1][j]
							else:#both are not in the world
								left = 0
					policy_utility.append(left)
					#rigth
					if (j+1) < width and world[i][j+1] != 2:#when right is in the world
						if (i-1) >= 0 and world[i-1][j] != 2:#if up is in the world
							if (i+1) < length and world[i+1][j] != 2:#if down is in the world
								right = 0.8*utility_previous[i][j+1] + 0.1*utility_previous[i+1][j] + 0.1*utility_previous[i-1][j]
							else:#if down is not in the world
								right = 0.8*utility_previous[i][j+1] + 0.1*utility_previous[i-1][j]
						else:#if up is not in the world
							if (i+1) < length and world[i+1][j] != 2: #down is in the world
								right = 0.8*utility_previous[i][j+1] + 0.1*utility_previous[i+1][j]
							else:#both are not in the world
								right = 0.8*utility_previous[i][j+1]
					else:#when right is not in the world
						if (i-1) >= 0 and world[i-1][j] != 2:#if up is in the world
							if (i+1) < length and world[i+1][j] != 2:#if down is in the world
								right = 0.1*utility_previous[i+1][j]+0.1*utility_previous[i-1][j]
							else:#if down is not in the world
								right = 0.1*utility_previous[i-1][j]
						else:#up is not in the world
							if (i+1) < length and world[i+1][j] != 2: #down is in the world
								right = 0.1*utility_previous[i+1][j]
							else:#both are not in the world
								right = 0
					policy_utility.append(right)
				n = policy_utility.index(max(policy_utility)) 
				if n == 0:
					policy[i][j] = "u"
				elif n == 1:
					policy[i][j] = "d"
				elif n == 2:
					policy[i][j] = "l"
				else:
					policy[i][j] = "r"
				temper = (utility_original[i][j]+0.9*max(policy_utility))
				utility_current[i][j] = temper
		max_change = 0
		for a in range(0,length):
			for b in range(0,width):
				change = abs(utility_current[a][b] - utility_previous[a][b])
				if  change > max_change:
					max_change = change
	print l
	for i in range(0,len(utility)):
		print policy[i]
		#print utility_current[i]
	findPath(7,0)
	print total

def findPath(x,y):
	global policy,utility_current,total
	if x == 0 and y == 9:
		print "Done"
	else:
		total += utility_current[x][y]
		print (x,y),policy[x][y],utility_current[x][y]
		if policy[x][y] == "u":
			findPath(x-1,y)
		elif policy[x][y] == "d":
			findPath(x+1,y)
		elif policy[x][y] == "r":
			findPath(x,y+1)
		else:
			findPath(x,y-1)


MDP()