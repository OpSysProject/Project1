import sys
import os


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

def SRT(p):
	t_cs = 8
	t = 0
	queue = []
	current = []
	busy = 0
	done = []
	num = {}
	start_time = 0
	end_time = 0
	time_left=0
	cpu_start_t = 0
	ioend_time = {}
	time_left_arr = []
	tmp = None
	io_time_beg=0
	num_pre=0
	num_processes=0
	for x in p:
		num[x.id] = x.num_bursts
		num_processes +=1

	print("time %dms: Simulator started for SRT %s" %(t, printQueue(queue)))
	if num_processes ==1:
		while(1):
			if(sum(num.values()) == 0):
				break
			for x in p:

				if(x.arrival_time == t):
					# print("arrived", x.id)
					if t == 0:
						queue.append(x)
						print("time " + str(t) + "ms: Process " + x.id + " arrived and added to ready queue " + printQueue(queue))
					else:	
						tmp = current.pop()
						if x.cpu_burst_time < tmp.cpu_burst_time- (t-cpu_start_t) : 
							time_left = tmp.cpu_burst_time- (t-cpu_start_t) 
							print("time %dms: Process %s arrived and will preempt %s %s" %(t, x.id,  tmp.id, printQueue(queue)))
							t += t_cs
							start_time = t
							end_time = start_time + x.cpu_burst_time
							ioend_time[x.id] = end_time + 4 + x.io_time
							busy = 1
							queue.append(tmp)
							if time_left > 0:
								print("time " + str(t) + "ms: Process " + x.id + " started using the CPU with " + str(time_left) + "ms remaining " + printQueue(queue))
							else:
								print("time " + str(t) + "ms: Process " + x.id + " started using the CPU "  + printQueue(queue))
							cpu_start_t = t
							current.append(x)
						else:
							queue.append(x)
							print("time " + str(t) + "ms: Process " + x.id + " arrived and added to ready queue " + printQueue(queue))
							
			if(busy == 0):
				# print("started using cpu", x.id)
				# tmp2 = current.pop()
				# print("current", tmp2)
				if(queue != []):
					t += 4
					start_time = t
					tmp = queue.pop(0)
					end_time = start_time + tmp.cpu_burst_time
					ioend_time[tmp.id] = end_time + 4 + tmp.io_time
					busy = 1
					if time_left > 0:
						print("time " + str(t) + "ms: Process " + tmp.id + " started using the CPU with " + str(time_left) + "ms remaining " + printQueue(queue))
					else:
						print("time " + str(t) + "ms: Process " + tmp.id + " started using the CPU "  + printQueue(queue))
					current.append(tmp)
					cpu_start_t = t
			
			if(time_left+t < t+tmp.arrival_time):
				# print("end time change", x.id)
				end_time = t+tmp.arrival_time
			
			if(t == end_time):
				# print("now is end time", x.id)
				busy = 0
				if current != []:
					tmp = current.pop(0)
				# else:
				# 	if q
				# 	tmp = queue.pop(0)
				num[tmp.id] -= 1
				# print(str(end_time))
				# print(str(time_left))
				# print(cpu_start_t)
				# print("end time"+str(end_time))
				if(num[tmp.id] == 0):
					# print("time " + str(t) + "ms: FIX-Process " + tmp.id + " terminated " + printQueue(queue))
					# current.remove(tmp)
					if queue != []:
						del queue[0]
					t = t+time_left
					print("time " + str(t) + "ms: Process " + tmp.id + " terminated " + printQueue(queue))
					t +=3
				# elif(num[tmp.id] == 1):
				elif(num[tmp.id]==1):
					print("time " + str(t) + "ms: Process " + tmp.id + " completed a CPU burst; " + str(num[tmp.id]) + " burst to go " + printQueue(queue))
					print("time " + str(t) + "ms: Process " + tmp.id + " switching out of CPU; will block on I/O until time " + str(ioend_time[tmp.id]) + "ms " + printQueue(queue))
					t += 3
				elif(num[tmp.id]>1):
					if current != []:
						tmp = current.pop()
					print("time " + str(t) + "ms: Process " + tmp.id + " completed a CPU burst; " + str(num[tmp.id]) + " bursts to go " + printQueue(queue))
					print("time " + str(t) + "ms: Process " + tmp.id + " switching out of CPU; will block on I/O until time " + str(ioend_time[tmp.id]) + "ms " + printQueue(queue))
					t += 3
				else:
					print("done")

			for x in p:
				if(x.id in ioend_time):
					if(t == ioend_time[x.id] and (x not in queue)):
						if current != []:
							tmp = current.pop()
						if x.cpu_burst_time < time_left and t!=end_time : 
							print("time %dms: Process %s completed I/O and will preempt %s %s" %(t, x.id, tmp.id,printQueue(queue)))
							t += t_cs
							start_time = t
							end_time = start_time + x.cpu_burst_time
							ioend_time[x.id] = end_time + 4 + x.io_time
							busy = 1
							# queue.append(tmp)
							queue.insert(0,tmp)
							time_left = time_left-(t-cpu_start_t)+t_cs

							if time_left > 0:
								print("time " + str(t) + "ms: Process " + x.id + " started using the CPU with " + str(time_left) + "ms remaining " + printQueue(queue))
							else:
								print("time " + str(t) + "ms: Process " + x.id + " started using the CPU "  + printQueue(queue))
							cpu_start_t = t
							current.append(x)
						else:
							queue.append(x)
							print("time " + str(t) + "ms: Process " + x.id + " completed I/O; added to ready queue " + printQueue(queue))
						t -= 1
			t += 1
	else:
		while(1):
			if(sum(num.values()) == 0):
				break
			for x in p:
				if(t ==x.arrival_time):
					if t == 0:
						queue.append(x)
						print("time " + str(t) + "ms: Process " + x.id + " arrived and added to ready queue " + printQueue(queue))
					else:	
						tmp = current.pop()
						if x.cpu_burst_time < tmp.cpu_burst_time- (t-cpu_start_t) : 
							time_left = tmp.cpu_burst_time- (t-cpu_start_t) 
							time_left_arr.append(time_left)
							print("time %dms: Process %s arrived and will preempt %s %s" %(t, x.id,  tmp.id, printQueue(queue)))
							num_pre +=1
							t += t_cs
							start_time = t
							end_time = start_time + x.cpu_burst_time
							ioend_time[x.id] = end_time + 4 + x.io_time
							busy = 1
							queue.append(tmp)
							print("time " + str(t) + "ms: Process " + x.id + " started using the CPU "  + printQueue(queue))
							cpu_start_t = t
							current.append(x)
						else:
							queue.append(x)
							print("time " + str(t) + "ms: Process " + x.id + " arrived and added to ready queue " + printQueue(queue))
			if(busy == 0):
				# print("not busy", str(time_left))
				if(queue != []):
					t += 4
					start_time = t
					tmp = queue.pop(0)
					end_time = start_time + tmp.cpu_burst_time
					ioend_time[tmp.id] = end_time + 4 + tmp.io_time
					busy = 1
					'''errornous one that shows time is here'''
					# print("time left", str(time_left))
					if time_left_arr != []:
						# print("here")
						time_left = time_left_arr.pop()
					# if current != []:
					# 	current_one = current.pop(0)
					# # 	print("current", current_one.id)
					# print("time elft", str(time_left))
					if time_left > 0:
						print("time " + str(t) + "ms: Process " + tmp.id + " started using the CPU with " + str(time_left) + "ms remaining " + printQueue(queue))
						end_time = t+time_left
					else:
						print("time " + str(t) + "ms: Process " + tmp.id + " started using the CPU "  + printQueue(queue))
						time_left = tmp.cpu_burst_time
						time_left_arr.append(time_left)
					current.append(tmp)
					cpu_start_t = t
					# print(time_left)

			# if(time_left+t < t+tmp.arrival_time):
			# 	# print("end time change", x.id)
			# 	end_time = t+tmp.arrival_time
			# 	# print("hi 1?")
		
			# # if(time_left+t < tmp.cpu_burst_time):
			# # 	# end_time = t+time_left
			# # 	end_time = io_time_beg+time_left
			# 	# print("hi?")

			# # if(time_left+ t < io_time_beg+)
			
			# if (time_left+t < io_time_beg):
			# 	end_time = t+time_left

			if(t == end_time and (x not in done) and num[tmp.id] >= 0) :

				# print("end time", str(time_left))
				# print("end time", str(end_time))
				# print("time left ", str(time_left))
				# print("t", str(t))
				busy = 0
				if current != []:
					tmp = current.pop(0)
				num[tmp.id] -= 1
				# print("tmp", tmp.id)

				# print("io end time", str(ioend_time))
				# if(x.id in ioend_time):
				# 	if t > ioend_time[x.id]:
				# 		print("hi")
				if(num[tmp.id] == 0):	
					del x
					print("time " + str(t) + "ms: Process " + tmp.id + " terminated " + printQueue(queue))
					done.append(tmp)
					t +=3
					time_left = 0
				else:
					if current != []:
						tmp = current.pop()
					if num[tmp.id]==1:
						print("time " + str(t) + "ms: Process " + tmp.id + " completed a CPU burst; " + str(num[tmp.id]) + " burst to go " + printQueue(queue))
					else: 
						print("time " + str(t) + "ms: Process " + tmp.id + " completed a CPU burst; " + str(num[tmp.id]) + " bursts to go " + printQueue(queue))
					ioend_time[x.id] = end_time + 4 + x.io_time
					print("time " + str(t) + "ms: Process " + tmp.id + " switching out of CPU; will block on I/O until time " + str(ioend_time[tmp.id]) + "ms " + printQueue(queue))
					t += 3
					
					# io_time_beg = t
					# end_time = t+time_left
					end_time = end_time + 4 + x.io_time
					# print("end time io", str(end_time))
					# previous.append(tmp)
					time_left = 0

			''' At each io end time'''
			for x in p:
				if(x.id in ioend_time):
					if(t == ioend_time[x.id] and (x not in queue) and (x not in done)):
			
						# print("iotime", str(time_left))
						if current != []:
							tmp = current.pop()
						if time_left_arr != []:
						# print("here")
							time_left = time_left_arr.pop()
						if time_left+cpu_start_t < ioend_time[x.id]:
							busy = 0
							num[tmp.id] -= 1
							if(num[tmp.id] == 0):
								if time_left_arr != []:
									# print("here")
									time_left = time_left_arr.pop()
								t = time_left+cpu_start_t
								print("time " + str(t) + "ms: Process " + tmp.id + " terminated " + printQueue(queue))
								done.append(tmp)
								t +=3
								time_left = 0
								t +=1
						elif(x.cpu_burst_time < time_left and t!=end_time):
							print("time %dms: Process %s completed I/O and will preempt %s %s" %(t, x.id, tmp.id,printQueue(queue)))
							num_pre +=1
							t += t_cs
							start_time = t
							end_time = start_time + x.cpu_burst_time
							ioend_time[x.id] = end_time + 4 + x.io_time
							busy = 1
							queue.insert(0,tmp)
							time_left = time_left-(t-cpu_start_t)+t_cs
							time_left_arr.append(time_left)

							if time_left >0:
								print("time " + str(t) + "ms: Process " + x.id + " started using the CPU "  + printQueue(queue))
							cpu_start_t = t
							current.append(x)
						else:
							queue.append(x)
							print("time " + str(t) + "ms: Process " + x.id + " completed I/O; added to ready queue " + printQueue(queue))
						end_time = x.cpu_burst_time+t
						t -= 1
			t += 1

	print("time " + str(t) + "ms: Simulator ended for SRT\n")
	return num_pre

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
	# FCFS(p)
	num_pre =SRT(p)
	# RR(p)

	f = open(sys.argv[2], "w+")

	cbt = 0.00
	wt = 0.00
	tt = 0.00
	cs = 0
	for x in p:
		cs += x.num_bursts
		cbt += x.cpu_burst_time * x.num_bursts
	cbt /= cs
	tt = cbt + wt + 8	
	f.write("Algorithm FCFS\n")
	f.write("-- average CPU burst time: %.2f ms\n" %cbt)
	f.write("-- average wait time: %.2f ms\n" %wt)
	f.write("-- average turnaround time: %.2f ms\n"%tt)	
	f.write("-- total number of context switches: %d\n" %(cs))
	f.write("-- total number of preemptions: 0\n")

	# placeholder
	f.write("Algorithm SRT\n")
	f.write("-- average CPU burst time: %.2f ms\n" %cbt)
	f.write("-- average wait time: %.2f ms\n" %wt)
	f.write("-- average turnaround time: %.2f ms\n"%tt)	
	f.write("-- total number of context switches: %d\n" %(cs))
	f.write("-- total number of preemptions: %d\n" %(num_pre))

	f.write("Algorithm RR\n")
	f.write("-- average CPU burst time: %.2f ms\n" %cbt)
	f.write("-- average wait time: %.2f ms\n" %wt)
	f.write("-- average turnaround time: %.2f ms\n"%tt)	
	f.write("-- total number of context switches: %d\n" %(cs))
	f.write("-- total number of preemptions: %d\n" %(num_pre))

	f.close()