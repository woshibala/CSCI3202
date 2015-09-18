import sys,math
world = None
start = None
end = None
method = None
def input():
	global world,method
	for i in range(0,len(sys.argv)):
		print i,": ",sys.argv[i]
	if sys.argv[2] == "Manhatten":
		method = "M"
	elif sys.argv[2] == "Euclid":
		method = "E"
	file_object = open(sys.argv[1])
	try:
	     all_the_text = file_object.read( )
	finally:
	     file_object.close( )
	print all_the_text
	l = [[]]
	j = 0
	for i in all_the_text:
		if i != "\n":
			if not i.isspace():
				l[j].append(int(i))
		else:
			j += 1
			l.append([])
	while j>0:
		if l[j] == []:
			l.pop()
		j-=1 		
	for i in l:
		print i
	return l

def Astar(st,en):
	global world,end,method
	world = input()
	start = st
	end = en
	length = len(world)-1
	width = len(world[0])-1
	flag = True
	if start[0] < 0 or start[0] > length or start[1] < 0 or start[1] > width:
		print("start node error!")
		flag = False
	if end[0] < 0 or end[0] > length or end[1] < 0 or end[1] > width:
		print("end node error!")
		flag = False
	if not flag:
		return 
	begin = Node(end,start,0,None)
	#print world[0][1]
	openList = []
	closeList = []
	openList.append(begin)
	path = []
	total = 0
	while len(openList)>0:# is not empty
		current = miniCost(openList)
		openList = removeNode(current,openList)
		if current.location != end:
			closeList.append(current)
			adjacent = searchAdjacent(current)
			total += len(adjacent)
			for i in adjacent:
				i.calculate_F(method)
				if inList(i,openList):
					if i.f < current.f:
						i.parent = current.location
						#openList = update(i,current,openList)
				elif inList(i,closeList):
					continue
				else:
					openList.append(i)
		else:
			print "Done!"
			print "Path:"
			now = current
			while True:
				print now.parent.location 
				now = now.parent
				if now.parent == None:
					break
			print "cost = ",current.distanceTostart
			print "location evaluated = ",total
			break

'''def update(i,current,openList):
	for n in openList:
		move = (n.location[0]-i.location[0],n.location[1]-i.location[1])
		move = (i.location[0]-current.location[0],i.location[1]-current.location[1])
		if move == (-1,0):
			if world[n.location[0]][n.location[1]] == 0:
				n.distanceTostart += 10
				n.calculate_F()
			else:
				n.distanceTostart += 20
				n.calculate_F()
		elif move == (1,0):
			if world[n.location[0]][n.location[1]] == 0:
				n.distanceTostart += 10
				n.calculate_F()
			else:
				n.distanceTostart += 20
				n.calculate_F()
		elif move == (0,-1):
			if world[n.location[0]][n.location[1]] == 0:
				n.distanceTostart += 10
				n.calculate_F()
			else:
				n.distanceTostart += 20
				n.calculate_F()
		elif move == (0,1):
			if world[n.location[0]][n.location[1]] == 0:
				n.distanceTostart += 10
				n.calculate_F()
			else:
				n.distanceTostart += 20
				n.calculate_F()
		elif move == (1,1):
			if world[n.location[0]][n.location[1]] == 0:
				n.distanceTostart += 14
				n.calculate_F()
			else:
				n.distanceTostart += 24
				n.calculate_F()
		elif move == (1,-1):
			if world[n.location[0]][n.location[1]] == 0:
				n.distanceTostart += 14
				n.calculate_F()
			else:
				n.distanceTostart += 24
				n.calculate_F()
		elif move == (-1,1):
			if world[n.location[0]][n.location[1]] == 0:
				n.distanceTostart += 14
				n.calculate_F()
			else:
				n.distanceTostart += 24
				n.calculate_F()
		elif move == (-1,-1):
			if world[n.location[0]][n.location[1]] == 0:
				n.distanceTostart += 14
				n.calculate_F()
			else:
				n.distanceTostart += 24
				n.calculate_F()
		elif move == (0,0):
			displace = (n.location[0]-current.location[0],n.location[1]-current.location[1])
			if displace == (-1,0):
				if world[n.location[0]][n.location[1]] == 0:
					n.distanceTostart += 10
					n.calculate_F()
				else:
					n.distanceTostart += 20
					n.calculate_F()
			elif displace == (1,0):
				if world[n.location[0]][n.location[1]] == 0:
					n.distanceTostart += 10
					n.calculate_F()
				else:
					n.distanceTostart += 20
					n.calculate_F()
			elif displace == (0,-1):
				if world[n.location[0]][n.location[1]] == 0:
					n.distanceTostart += 10
					n.calculate_F()
				else:
					n.distanceTostart += 20
					n.calculate_F()
			elif displace == (0,1):
				if world[n.location[0]][n.location[1]] == 0:
					n.distanceTostart += 10
					n.calculate_F()
				else:
					n.distanceTostart += 20
					n.calculate_F()
			elif displace == (1,1):
				if world[n.location[0]][n.location[1]] == 0:
					n.distanceTostart += 14
					n.calculate_F()
				else:
					n.distanceTostart += 24
					n.calculate_F()
			elif displace == (1,-1):
				if world[n.location[0]][n.location[1]] == 0:
					n.distanceTostart += 14
					n.calculate_F()
				else:
					n.distanceTostart += 24
					n.calculate_F()
			elif displace == (-1,1):
				if world[n.location[0]][n.location[1]] == 0:
					n.distanceTostart += 14
					n.calculate_F()
				else:
					n.distanceTostart += 24
					n.calculate_F()
			elif displace == (-1,-1):
				if world[n.location[0]][n.location[1]] == 0:
					n.distanceTostart += 14
					n.calculate_F()
				else:
					n.distanceTostart += 24
					n.calculate_F()
	return openList'''

def find(node,list):
	for i in list:
		if i.location == node.location:
			return list.index(i)
def miniCost(list):
	l = []
	for i in list:
		l.append(i.f)
	return list[l.index(min(l))]

def removeNode(node,list):
	j = 0
	for i in list:
		if i.location == node.location:
			#print j
			list.pop(list.index(i))
			return list
		j += 1

def searchAdjacent(node):
	global world,start,end
	length = len(world)-1
	width = len(world[0])-1
	#print length,width
	adjacent_list = []
	#adjacent node should in the world and is not wal
	if (node.location[1]-1)>=0 and world[node.location[0]][node.location[1]-1] != 2:
		if world[node.location[0]][node.location[1]-1] == 0:
			adjacent_list.append(Node(end,(node.location[0],node.location[1]-1),node.distanceTostart+10,node))
		elif world[node.location[0]][node.location[1]-1] == 1:
			adjacent_list.append(Node(end,(node.location[0],node.location[1]-1),node.distanceTostart+20,node))
	if (node.location[1]+1) <= width and world[node.location[0]][node.location[1]+1] != 2:
		if world[node.location[0]][node.location[1]+1] == 0:
			adjacent_list.append(Node(end,(node.location[0],node.location[1]+1),node.distanceTostart+10,node))
		else:
			adjacent_list.append(Node(end,(node.location[0],node.location[1]+1),node.distanceTostart+20,node))
	if (node.location[0]-1)>=0 and world[node.location[0]-1][node.location[1]] != 2:
		if world[node.location[0]-1][node.location[1]] == 0:
			adjacent_list.append(Node(end,(node.location[0]-1,node.location[1]),node.distanceTostart+10,node))
		else:
			adjacent_list.append(Node(end,(node.location[0]-1,node.location[1]),node.distanceTostart+20,node))
	if (node.location[0]+1) <= length and world[node.location[0]+1][node.location[1]] != 2:
		if world[node.location[0]+1][node.location[1]] == 0:
			adjacent_list.append(Node(end,(node.location[0]+1,node.location[1]),node.distanceTostart+10,node))
		else:
			adjacent_list.append(Node(end,(node.location[0]+1,node.location[1]),node.distanceTostart+20,node))
	if (node.location[0]-1)>=0 and (node.location[1]-1)>=0 and world[node.location[0]-1][node.location[1]-1] != 2:
		if world[node.location[0]-1][node.location[1]-1] == 0:
			adjacent_list.append(Node(end,(node.location[0]-1,node.location[1]-1),node.distanceTostart+14,node))
		else:
			adjacent_list.append(Node(end,(node.location[0]-1,node.location[1]-1),node.distanceTostart+24,node))
	if (node.location[0]-1)>=0 and (node.location[1]+1) <= width and world[node.location[0]-1][node.location[1]+1] != 2:
		if world[node.location[0]-1][node.location[1]+1] == 0:
			adjacent_list.append(Node(end,(node.location[0]-1,node.location[1]+1),node.distanceTostart+14,node))
		else:
			adjacent_list.append(Node(end,(node.location[0]-1,node.location[1]+1),node.distanceTostart+24,node))
	if (node.location[0]+1) <= length and (node.location[1]+1) <= width and world[node.location[0]+1][node.location[1]+1] != 2:
		if world[node.location[0]+1][node.location[1]+1] == 0:
			adjacent_list.append(Node(end,(node.location[0]+1,node.location[1]+1),node.distanceTostart+14,node))
		else:
			adjacent_list.append(Node(end,(node.location[0]+1,node.location[1]+1),node.distanceTostart+24,node))
	if (node.location[0]+1) <= length and (node.location[1]-1)>=0 and world[node.location[0]+1][node.location[1]-1] != 2:
		if world[node.location[0]+1][node.location[1]-1] == 0:
			adjacent_list.append(Node(end,(node.location[0]+1,node.location[1]-1),node.distanceTostart+14,node))
		else:
			adjacent_list.append(Node(end,(node.location[0]+1,node.location[1]-1),node.distanceTostart+24,node))
	return adjacent_list

def inList(node,list):
	for i in list:
		if i.location == node.location:
			return True
	return False



class Node():

	def __init__(self,end,location,distanceTostart,parent):
		
		self.location = location
		self.end = end
		self.distanceTostart = distanceTostart
		self.heuristic = None
		self.f = None
		self.parent = parent


	def Heuristic_Manhatten(self,end):
		self.heuristic = (abs(self.location[0]-end[0])+abs(self.location[1]-end[1]))*10
		return (abs(self.location[0]-end[0])+abs(self.location[1]-end[1]))*10
	def Heuristic_euclid(self,end):
		self.heuristic = math.sqrt(((self.location[0]-end[0])*10)**2+((self.location[1]-end[1])*10)**2)
		return math.sqrt(((self.location[0]-end[0])*10)**2+((self.location[1]-end[1])*10)**2)
	def calculate_F(self,method):
		if method == "M":
			self.Heuristic_Manhatten(self.end)
		elif method == "E":
			self.Heuristic_euclid(self.end)
		else:
			print "no such method!"
			return
		self.f = self.heuristic+self.distanceTostart
		return self.f
'''
class Node():

	def __init__(self,end,location,distanceTostart,parent):
		
		self.location = location
		self.end = end
		self.distanceTostart = distanceTostart
		self.heuristic = self.euclid(end)
		self.f = None
		self.parent = parent

	def euclid(self,end):
		return math.sqrt(((self.location[0]-end[0])*10)**2+((self.location[1]-end[1])*10)**2)
	def calculate_F(self):
		self.f = self.heuristic+self.distanceTostart
		return self.f
'''
Astar((7,0),(0,9))


#Python bbb.py World1.txt