import sys

class Process:
	def __init__(self, state, proc_id, arrival_time, cpu_burst_time, num_bursts, io_time):
		'''
		state will be 'READY' or 'RUNNING' or 'BLOCKED'
		'''
		self.state = state
		self.id = proc_id
		self.arrival_time = arrival_time
		self.cpu_burst_time = cpu_burst_time
		self.num_bursts = num_bursts
		self.io_time = io_time
		'''
		calculated parameters
		'''
		self.cpu_comp_time = self.cpu_burst_time
		self.wait_time = 0
		self.turnaround_time = self.cpu_burst_time + self.wait_time
	def __cmp__(self, other):
		if self.cpu_burst_time > other.cpu_burst_time:
			return 1
		elif self.cpu_burst_time < other.cpu_burst_time:
			return -1
		else:
			if self.io_time > other.io_time:
				return 1
			elif self.io_time < other.io_time:
				return -1
			else:
				if self.arrival_time > other.arrival_time:
					return 1
				elif self.arrival_time < other.arrival_time:
					return -1
				else:
					return cmp(self.proc_id, other.proc_id)
	def update_wait_time(self,time):
		self.wait_time += time
	def update_cpu_completion_time(self,time):
		self.cpu_comp_time -= time
	def update_num_bursts(self):
		self.num_bursts -= 1
	def get_cpu_burst_time(self):
		return self.cpu_burst_time
	def get_cpu_completion_time(self):
		return self.cpu_comp_time
	def get_wait_time(self):
		return self.wait_time
	def get_turnaround_time(self):
		return self.turnaround_time

def printQueue(queue):
	if(queue == []):
		str = "[Q <empty>]"
	else:
		str = "[Q"
		for q in queue:
			str += " " + q.id
		str += "]"
	return str

def FCFS(p):
	print("time 0ms: Simulator started for FCFS [Q <empty>]")
	t_cs = 8
	t = 0
	queue = []
	busy = 0
	num = {}
	start_time = 0
	end_time = 0
	ioend_time = {}
	tmp = None
	for x in p:
		num[x.id] = x.num_bursts
	while(1):
		if(sum(num.values()) == 0):
			break
		for x in p:
			if(x.arrival_time == t):
				queue.append(x)
				print("time " + str(t) + "ms: Process " + x.id + " arrived and added to ready queue " + printQueue(queue))
		if(busy == 0):
			t += 4
			start_time = t
			if(queue != []):
				tmp = queue.pop(0)
				end_time = start_time + tmp.cpu_burst_time
				ioend_time[tmp.id] = end_time + 4 + tmp.io_time
				busy = 1
				print("time " + str(t) + "ms: Process " + tmp.id + " started using the CPU " + printQueue(queue))
		if(t == end_time):
			busy = 0
			num[tmp.id] -= 1
			if(num[tmp.id] == 0):
				print("time " + str(t) + "ms: Process " + tmp.id + " terminated " + printQueue(queue))
				t += 3
			elif(num[tmp.id] == 1):
				print("time " + str(t) + "ms: Process " + tmp.id + " completed a CPU burst; " + str(num[tmp.id]) + " burst to go " + printQueue(queue))
				print("time " + str(t) + "ms: Process " + tmp.id + " switching out of CPU; will block on I/O until time " + str(ioend_time[tmp.id]) + "ms " + printQueue(queue))
				t += 3
			else:
				print("time " + str(t) + "ms: Process " + tmp.id + " completed a CPU burst; " + str(num[tmp.id]) + " bursts to go " + printQueue(queue))
				print("time " + str(t) + "ms: Process " + tmp.id + " switching out of CPU; will block on I/O until time " + str(ioend_time[tmp.id]) + "ms " + printQueue(queue))
				t += 3
		for x in p:
			if(x.id in ioend_time):
				if(t == ioend_time[x.id]):
					queue.append(x)
					print("time " + str(t) + "ms: Process " + x.id + " completed I/O; added to ready queue " + printQueue(queue))
		t += 1
	print("time " + str(t) + "ms: Simulator ended for FCFS")
'''
	cbt = 0.00
	wt = 0.00
	tt = 0.00
	cs = 0
	for x in p:
		cs += x.num_bursts
		cbt += x.cpu_burst_time * x.num_bursts
	cbt /= cs
	tt = cbt + wt + 8	
	print("Algorithm FCFS")
	print("-- average CPU burst time: " + str(cbt) + " ms")
	print("-- average wait time: " + str(wt) + " ms")
	print("-- average turnaround time: " + str(tt) + " ms")	
	print("-- total number of context switches: " + str(cs))
	print("-- total number of preemptions : 0")
'''

if(__name__ == "__main__"):
	if((len(sys.argv) != 3) and (len(sys.argv) != 4)):
		sys.exit("ERROR: Invalid arguments\nUSAGE: ./a.out <input-file> <stats-output-file> [<rr-add>]")
	try:
		input_file = open(sys.argv[1], 'r')
	except:
		sys.exit("ERROR: Invalid input file format")
	try:
		output_file = open(sys.argv[2], 'w')
	except:
		sys.exit("ERROR: Invalid output file")
	p = []
	for line in input_file:
		if ((line[0] != '#') and (line[0] != '\n')):
			line = line.strip().split('|')
			try:
				p.append(Process('READY', line[0], int(line[1]), int(line[2]), int(line[3]), int(line[4])))
			except:
				input_file.close()
				sys.exit("ERROR: Invalid input file format")
		else:
			continue
	input_file.close()
	FCFS(p)
