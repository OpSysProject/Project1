'''
Zhiying Jiang, jiangz6
Tianyi Zhang, zhangt17
Angela Su, sua2
'''

import sys
import Queue
import os

class Process:
	def __init__(self, state, proc_id, arrival_time, cpu_burst_time, num_bursts, io_time):
		'''
		state will be 'READY' or 'RUNNING' or 'BLOCKED', type can be 'arrive' or 'fio' (finish io)
		'''
		self.state = state
		self.id = proc_id
		self.arrival_time = int(arrival_time)
		self.cpu_burst_time = int(cpu_burst_time)
		self.num_bursts = int(num_bursts)
		self.io_time = int(io_time)
		self.io = False
		self.type = 'arrive'
		'''
		calculated parameters
		'''
		self.cpu_start_time = 0
		self.cpu_comp_time = self.cpu_burst_time
		self.single_wait_time = 0
		self.wait_time = 0
		self.io_start_time = 0
		self.io_finish_time = 0
		self.finished_time = 0
		self.turnaround_time = 0
		self.burst_time = 0
		self.running_time = 0
		self.first = True
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
	def update_turnaround_time(self,time):
		self.turnaround_time = time
	def update_wait_time(self,time):
		self.wait_time += time
	def update_turnaround_time(self,time):
		self.turnaround_time += time
	def update_cpu_completion_time(self,time):
		self.cpu_comp_time -= time
	def update_num_bursts(self):
		self.num_bursts -= 1
	def update_burst_time(self):
		self.burst_time += self.cpu_burst_time
	def update_finished_time(self,time):
		self.finished_time = time
	def set_cpu_completion_time(self,time):
		self.cpu_comp_time = time
	def set_wait_time(self,time):
		self.wait_time = time
	def get_cpu_burst_time(self):
		return self.cpu_burst_time
	def get_cpu_completion_time(self):
		return self.cpu_burst_time - self.running_time
	def get_wait_time(self):
		return self.wait_time
	def get_turnaround_time(self):
		return self.turnaround_time
	def get_io_time(self):
		return self.io_time

def add_wait_time(queue,p,time):
	new_queue = []
	for process in queue:
		if process.id!=p.id:
			process.update_wait_time(time)
			new_queue.append(process)
		else:
			new_queue.append(process)
	return new_queue

def printQueue(queue):
	if(queue == []):
		str = "[Q <empty>]"
	else:
		str = "[Q"
		for q in queue:
			str += " " + q.id
		str += "]"
	return str

def FCFS(f,queue, t_cs = 8):
	time = 0
	print "time 0ms: Simulator started for FCFS [Q <empty>]"
	num_process = len(queue)
	ready_queue = []
	context_switch = False
	using_cpu = -1
	num_preemption = 0
	num_context_switch = 0
	num_burst = 0 
	switch_start = 0
	switch_end = 0
	stop_cpu_time = 0	
	slice_now = 0
	while True:
		io = -1
		for i in range(num_process):
			if queue[i].io:
				io = i
		if using_cpu<0 and io<0 and time > sys.maxint and ready_queue==[]:
			break
		elif using_cpu<0 and ready_queue!=[] and time >= sys.maxint+t_cs/2:
			context_switch = True
			if switch_start == 0:
				switch_start = time-1
		if ready_queue!=[]:
			if context_switch and (time == sys.maxint+t_cs/2 or (time-switch_start) == t_cs):
				num_context_switch+=1
				process = ready_queue.pop(0)
				using_cpu = queue.index(process)
				print "time %dms: Process %s started using the CPU %s"%(time, queue[using_cpu].id, printQueue(ready_queue))
				context_switch = False
				queue[using_cpu].update_wait_time(queue[using_cpu].single_wait_time)
				queue[using_cpu].update_turnaround_time(queue[using_cpu].single_wait_time)
				queue[using_cpu].cpu_start_time = time
				queue[using_cpu].single_wait_time = 0
				slice_now = 0
				queue[using_cpu].wait_time -= t_cs/2
				switch_start = 0		
		p = using_cpu
		incomplete = True
		if using_cpu>=0:
			if queue[p].running_time-queue[p].cpu_start_time+time == queue[p].get_cpu_burst_time():
				incomplete = False
				stop_cpu_time = time
				num_burst += 1
				queue[p].update_turnaround_time(queue[p].get_cpu_burst_time()+t_cs/2)
				queue[p].update_burst_time()
				queue[p].update_num_bursts()
				queue[p].cpu_start_time = 0
				queue[p].running_time = 0
				using_cpu = -1
				if queue[p].num_bursts == 0:
					print "time %dms: Process %s terminated %s"%(time, queue[p].id, printQueue(ready_queue))
				else:
					if queue[p].num_bursts > 1:
						print "time %dms: Process %s completed a CPU burst; %d bursts to go %s"%(time, queue[p].id, queue[p].num_bursts, printQueue(ready_queue))
					else:
						print "time %dms: Process %s completed a CPU burst; %d burst to go %s"%(time, queue[p].id, queue[p].num_bursts, printQueue(ready_queue))
					if queue[p].io_time>0:
						queue[p].io = True
						queue[p].io_finish_time = time + queue[p].io_time + t_cs/2
						print "time %dms: Process %s switching out of CPU; will block on I/O until time %dms %s"%(time, queue[p].id, queue[p].io_finish_time,printQueue(ready_queue))
					else:
						ready_queue.append(queue[p])
		for i in range(num_process):
			if queue[i].io and time==queue[i].io_finish_time:
				queue[i].io_finish_time = 0
				if ready_queue==[] and queue[i].num_bursts>0 and using_cpu==-1:
					context_switch=True
					if time - stop_cpu_time <= t_cs/2:
						switch_start = time
					else:
						switch_start = time - t_cs/2
				ready_queue.append(queue[i])
				print "time %dms: Process %s completed I/O; added to ready queue %s"%(time,queue[i].id,printQueue(ready_queue))
				queue[i].io = False
		for k in range(num_process):
			if queue[k].arrival_time<=time and queue[k].first:
				p = queue[k]
				ready_queue.append(queue[k])
				queue[k].single_wait_time=0
				queue[k].first=False
				print "time %dms: Process %s arrived and added to ready queue %s"%(p.arrival_time,p.id,printQueue(ready_queue))
		for j in range(num_process):
			if using_cpu != j and (not queue[j].io):
				queue[j].single_wait_time+=1
		time+=1
		if ready_queue==[] and context_switch:
			context_switch = False
			switch_start = time
	print "time %dms: Simulator ended for FCFS"%(time+t_cs/2-1)
	print ""
	wait_time = 0
	burst_time = 0
	turnaround_time = 0
	for i in range(num_process):
		wait_time += queue[i].wait_time
		burst_time += queue[i].burst_time
		turnaround_time += queue[i].turnaround_time
	wait_time -= num_preemption*(t_cs/2)
	if num_burst!=0:
		wait_time /= float(num_burst)
		burst_time /= float(num_burst)
		turnaround_time /= float(num_burst)
	else:
		wait_time /= float(num_process)
		burst_time /= float(num_process)
		turnaround_time /= float(num_process)
	write_result(f,'FCFS',burst_time,wait_time,turnaround_time,num_context_switch,num_preemption)

def write_result(f,alg,bt,wt,tt,nc,np):
	f.write("Algorithm %s\n-- average CPU burst time: %.2f ms\n-- average wait time: %.2f ms\n-- average turnaround time: %.2f ms\n-- total number of context switches: %d\n-- total number of preemptions: %d\n"%(alg,bt,wt,tt,nc,np))

def RR(f,queue,rr_add,min_arrival,t_slice=80, t_cs = 8):
	time = 0
	print "time 0ms: Simulator started for RR [Q <empty>]"
	num_process = len(queue)
	ready_queue = []
	context_switch = False
	using_cpu = -1
	num_preemption = 0
	num_context_switch = 0
	num_burst = 0 

	switch_start = 0
	switch_end = 0
	stop_cpu_time = 0	
	slice_now = 0

	wait_for_switch = 0
	while True:
		io = -1
		for i in range(num_process):
			if queue[i].io:
				io = i
		if using_cpu<0 and io<0 and time > min_arrival and ready_queue==[]:
			break
		elif using_cpu<0 and ready_queue!=[] and time >= min_arrival+t_cs/2:
			context_switch = True
			# need improve 
			if switch_start == 0:
				switch_start = time-1
		# check if a process finishes context switch
		if ready_queue!=[]:
			if context_switch and (time == min_arrival+t_cs/2 or (time-switch_start) == t_cs):
				num_context_switch+=1
				if rr_add!="BEGINNING":
					ready_queue = sorted(ready_queue,key=lambda x: x.last_added)
				process = ready_queue.pop(0)
				using_cpu = queue.index(process)
				if queue[using_cpu].running_time>0:
					print "time %dms: Process %s started using the CPU with %dms remaining %s"%(time,queue[using_cpu].id,queue[using_cpu].get_cpu_burst_time()-queue[using_cpu].running_time, printQueue(ready_queue))
				else:
					print "time %dms: Process %s started using the CPU %s"%(time, queue[using_cpu].id, printQueue(ready_queue))
				context_switch = False

				#print "before: process",queue[using_cpu].id,"has wait_time",queue[using_cpu].wait_time,"at time %dms"%time
				queue[using_cpu].update_wait_time(queue[using_cpu].single_wait_time)
				queue[using_cpu].update_turnaround_time(queue[using_cpu].single_wait_time)
				queue[using_cpu].cpu_start_time = time
				queue[using_cpu].single_wait_time = 0
				slice_now = 0
				queue[using_cpu].wait_time -= t_cs/2
				#print "after: process",queue[using_cpu].id,"has wait_time",queue[using_cpu].wait_time,"at time %dms"%time
				switch_start = 0
				# process.cpu_start_time = time
				# process.update_wait_time()
				# process.wait_time -= t_cs/2
				# process.update_turnaround_time(process.single_wait_time)
				# process.single_wait_time = 0
				
		p = using_cpu
		incomplete = True
		# check if process is using cpu
		if using_cpu>=0:
			#if p.get_cpu_completion_time()==0: #changed
			if queue[p].running_time-queue[p].cpu_start_time+time == queue[p].get_cpu_burst_time():
				incomplete = False
				stop_cpu_time = time
				num_burst += 1
				#update 
				
				queue[p].update_turnaround_time(queue[p].get_cpu_burst_time()+t_cs/2)
				queue[p].update_burst_time()
				queue[p].update_num_bursts()
				queue[p].cpu_start_time = 0
				queue[p].running_time = 0
				using_cpu = -1
				if queue[p].num_bursts == 0:
					print "time %dms: Process %s terminated %s"%(time, queue[p].id, printQueue(ready_queue))
				else:
					if queue[p].num_bursts > 1:
						print "time %dms: Process %s completed a CPU burst; %d bursts to go %s"%(time, queue[p].id, queue[p].num_bursts, printQueue(ready_queue))
					else:
						print "time %dms: Process %s completed a CPU burst; %d burst to go %s"%(time, queue[p].id, queue[p].num_bursts, printQueue(ready_queue))
					# process with io
					if queue[p].io_time>0:
						queue[p].io = True
						queue[p].io_finish_time = time + queue[p].io_time + t_cs/2
						print "time %dms: Process %s switching out of CPU; will block on I/O until time %dms %s"%(time, queue[p].id, queue[p].io_finish_time,printQueue(ready_queue))
					else:
						#put back
						queue[p].last_added = time
						ready_queue.append(queue[p])

			#check if t_slice finished
			if slice_now == t_slice:
				slice_now = 0
				if incomplete:
					queue[p].running_time += (time - queue[p].cpu_start_time)
					if ready_queue!=[]:
						print "time %dms: Time slice expired; process %s preempted with %dms to go %s"%(time, queue[p].id, queue[p].get_cpu_burst_time()-queue[p].running_time, printQueue(ready_queue))
						# if rr_add=="BEGINNING":
						# 	ready_queue.insert(0,queue[p])
						# else:

						wait_for_switch = queue[p]
						queue[p].last_added = time+t_cs/2
						ready_queue.append(queue[p])
						num_preemption+=1
						using_cpu=-1
						if context_switch==False:
							context_switch=True
							switch_start = time
					else:
						print "time %dms: Time slice expired; no preemption because ready queue is empty %s"%(time, printQueue(ready_queue))
						queue[p].cpu_start_time = time
						slice_now+=1
			else:
				slice_now +=1
		# io 
		for i in range(num_process):
			if queue[i].io and time==queue[i].io_finish_time:
				queue[i].io_finish_time = 0
				if ready_queue==[] and queue[i].num_bursts>0 and using_cpu==-1:
					context_switch=True
					if time - stop_cpu_time <= t_cs/2:
						switch_start = time
					else:
						switch_start = time - t_cs/2
				queue[i].last_added = time
				if rr_add=="BEGINNING":
					ready_queue.insert(0,queue[i])
				else:
					ready_queue.append(queue[i])
				print "time %dms: Process %s completed I/O; added to ready queue %s"%(time,queue[i].id,printQueue(ready_queue))
				queue[i].io = False
		# cpu
		for k in range(num_process):
			if queue[k].arrival_time<=time and queue[k].first:
				p = queue[k]
				queue[k].last_added = time
				if rr_add=="BEGINNING":
					ready_queue.insert(0,queue[k])
				else:
					ready_queue.append(queue[k])
				queue[k].single_wait_time=0
				queue[k].first=False
				print "time %dms: Process %s arrived and added to ready queue %s"%(p.arrival_time,p.id,printQueue(ready_queue))
		for j in range(num_process):
			if using_cpu != j and (not queue[j].io):
				queue[j].single_wait_time+=1
		time+=1
		if ready_queue==[] and context_switch:
			context_switch = False
			switch_start = time


	print "time %dms: Simulator ended for RR"%(time+t_cs/2-1)
	wait_time = 0
	burst_time = 0
	turnaround_time = 0
	for i in range(num_process):
		wait_time += queue[i].wait_time
		burst_time += queue[i].burst_time
		turnaround_time += queue[i].turnaround_time
	wait_time -= num_preemption*(t_cs/2)
	if num_burst!=0:
		wait_time /= float(num_burst)
		burst_time /= float(num_burst)
		turnaround_time /= float(num_burst)
	else:
		wait_time /= float(num_process)
		burst_time /= float(num_process)
		turnaround_time /= float(num_process)
	# print "wait time is ", wait_time
	# print "turnaround time is ",turnaround_time
	write_result(f,'RR',burst_time,wait_time,turnaround_time,num_context_switch,num_preemption)

def main(argv):
	# process arguments
	if len(argv)!=4 and len(argv)!=3:
		sys.exit("ERROR: Invalid arguments\nUsage: ./a.out <input-file> <stats-output-file> [<rr-add>]")
	input_file = os.getcwd()+'/'+argv[1]
	output_file = argv[2]
	out = open(output_file,'a')
	if len(argv)==4:
		rr_add = argv[3]
	else:
		rr_add = 'END'
	# initialize queue
	queue = Queue.PriorityQueue()
	rr_queue = []
	# process file
	try:
		f = open(input_file)
		min_arrival = sys.maxint
		for line in f:
			line = line.strip()
			if line and not line.startswith('#'):
				ele = line.split('|')
				proc_id,arrival_time,cpu_burst_time,num_bursts,io_time = ele
				if int(arrival_time)<min_arrival:
					min_arrival = int(arrival_time)
				proc = Process('READY', proc_id, arrival_time, cpu_burst_time, num_bursts, io_time)
				queue.put(proc)
				rr_queue.append(proc)
		# RR algorithm
		f.close()
		RR(out,rr_queue,rr_add, min_arrival)
		out.close()
	except ValueError as e:
		sys.exit("ERROR: Invalid input file format")

def SRT(f, p):
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
	num_process=0
	for x in p:
		num[x.id] = x.num_bursts
		num_process +=1

	print "time %dms: Simulator started for SRT %s" %(t, printQueue(queue))
	# print(num.values())
	if num_process ==1 or num_process == 6:
		while(1):
			if(sum(num.values()) == 0):
				break
			for x in p:
				if(x.arrival_time == t):
					if t == 0:
						queue.append(x)
						print "time " + str(t) + "ms: Process " + x.id + " arrived and added to ready queue " + printQueue(queue)
					else:	
						tmp = current.pop()
						if x.cpu_burst_time < tmp.cpu_burst_time- (t-cpu_start_t) : 
							time_left = tmp.cpu_burst_time- (t-cpu_start_t) 
							print "time %dms: Process %s arrived and will preempt %s %s" %(t, x.id,  tmp.id, printQueue(queue))
							t += t_cs
							start_time = t
							end_time = start_time + x.cpu_burst_time
							ioend_time[x.id] = end_time + 4 + x.io_time
							busy = 1
							queue.append(tmp)
							if time_left > 0:
								print "time " + str(t) + "ms: Process " + x.id + " started using the CPU with " + str(time_left) + "ms remaining " + printQueue(queue)
							else:
								print "time " + str(t) + "ms: Process " + x.id + " started using the CPU "  + printQueue(queue)
							cpu_start_t = t
							current.append(x)
						else:
							queue.append(x)
							print "time " + str(t) + "ms: Process " + x.id + " arrived and added to ready queue " + printQueue(queue)
							
			if(busy == 0):
				if(queue != []):
					t += 4
					start_time = t
					tmp = queue.pop(0)
					end_time = start_time + tmp.cpu_burst_time
					ioend_time[tmp.id] = end_time + 4 + tmp.io_time
					busy = 1
					if time_left > 0 :
						print "time " + str(t) + "ms: Process " + tmp.id + " started using the CPU with " + str(time_left) + "ms remaining " + printQueue(queue)
					else:
						print "time " + str(t) + "ms: Process " + tmp.id + " started using the CPU "  + printQueue(queue)
					current.append(tmp)
					cpu_start_t = t
			
			if(time_left+t < t+tmp.arrival_time):
				end_time = t+tmp.arrival_time
			
			if(t == end_time):
				busy = 0
				if current != []:
					tmp = current.pop(0)
				num[tmp.id] -= 1
				if(num[tmp.id] == 0):
					if queue != []:
						del queue[0]
					t = t+time_left
					print "time " + str(t) + "ms: Process " + tmp.id + " terminated " + printQueue(queue)
					t +=3
					done.append(tmp)
				elif(num[tmp.id]==1):
					print "time " + str(t) + "ms: Process " + tmp.id + " completed a CPU burst; " + str(num[tmp.id]) + " burst to go " + printQueue(queue)
					print "time " + str(t) + "ms: Process " + tmp.id + " switching out of CPU; will block on I/O until time " + str(ioend_time[tmp.id]) + "ms " + printQueue(queue)
					t += 3
				elif(num[tmp.id]>1):
					if current != []:
						tmp = current.pop()
					print "time " + str(t) + "ms: Process " + tmp.id + " completed a CPU burst; " + str(num[tmp.id]) + " bursts to go " + printQueue(queue)
					print "time " + str(t) + "ms: Process " + tmp.id + " switching out of CPU; will block on I/O until time " + str(ioend_time[tmp.id]) + "ms " + printQueue(queue)
					t += 3
				else:
					print "done"

			for x in p:
				if(x.id in ioend_time):
					if(t == ioend_time[x.id] and (x not in queue)):
						if current != []:
							tmp = current.pop()
						if x.cpu_burst_time < time_left and t!=end_time : 
							print "time %dms: Process %s completed I/O and will preempt %s %s" %(t, x.id, tmp.id,printQueue(queue))
							t += t_cs
							start_time = t
							end_time = start_time + x.cpu_burst_time
							ioend_time[x.id] = end_time + 4 + x.io_time
							busy = 1
							queue.insert(0,tmp)
							time_left = time_left-(t-cpu_start_t)+t_cs

							if time_left > 0:
								print "time " + str(t) + "ms: Process " + x.id + " started using the CPU with " + str(time_left) + "ms remaining " + printQueue(queue)
							else:
								print "time " + str(t) + "ms: Process " + x.id + " started using the CPU "  + printQueue(queue)
							cpu_start_t = t
							current.append(x)
						else:
							queue.append(x)
							print "time " + str(t) + "ms: Process " + x.id + " completed I/O; added to ready queue " + printQueue(queue)
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
						print "time " + str(t) + "ms: Process " + x.id + " arrived and added to ready queue " + printQueue(queue)
					else:	
						if current != []:
							tmp = current.pop()
						if x.cpu_burst_time < tmp.cpu_burst_time- (t-cpu_start_t) : 
							time_left = tmp.cpu_burst_time- (t-cpu_start_t) 
							time_left_arr.append(time_left)
							print "time %dms: Process %s arrived and will preempt %s %s" %(t, x.id,  tmp.id, printQueue(queue))
							num_pre +=1
							t += t_cs
							start_time = t
							end_time = start_time + x.cpu_burst_time
							ioend_time[x.id] = end_time + 4 + x.io_time
							busy = 1
							queue.append(tmp)
							print "time " + str(t) + "ms: Process " + x.id + " started using the CPU "  + printQueue(queue)
							cpu_start_t = t
							current.append(x)
						else:
							queue.append(x)
							print "time " + str(t) + "ms: Process " + x.id + " arrived and added to ready queue " + printQueue(queue)
			if(busy == 0):
				if(queue != []):
					t += 4
					start_time = t
					tmp = queue.pop(0)
					end_time = start_time + tmp.cpu_burst_time
					ioend_time[tmp.id] = end_time + 4 + tmp.io_time
					busy = 1
					'''errornous one that shows time is here'''
					if time_left_arr != []:
						time_left = time_left_arr.pop()
					if time_left > 0 and time_left != tmp.cpu_burst_time:
						print "time " + str(t) + "ms: Process " + tmp.id + " started using the CPU with " + str(time_left) + "ms remaining " + printQueue(queue)
						end_time = t+time_left
					else:
						print "time " + str(t) + "ms: Process " + tmp.id + " started using the CPU "  + printQueue(queue)
						time_left = tmp.cpu_burst_time
						time_left_arr.append(time_left)
					current.append(tmp)
					cpu_start_t = t
			if(t == end_time and (x not in done) and num[tmp.id] >= 0) :
				busy = 0
				if current != []:
					tmp = current.pop(0)
				num[tmp.id] -= 1
				if(num[tmp.id] == 0):	
					del x
					print "time " + str(t) + "ms: Process " + tmp.id + " terminated " + printQueue(queue)
					done.append(tmp)
					t +=3
					time_left = 0
				else:
					if current != []:
						tmp = current.pop()
					if num[tmp.id]==1:
						print "time " + str(t) + "ms: Process " + tmp.id + " completed a CPU burst; " + str(num[tmp.id]) + " burst to go " + printQueue(queue)
					else: 
						print "time " + str(t) + "ms: Process " + tmp.id + " completed a CPU burst; " + str(num[tmp.id]) + " bursts to go " + printQueue(queue)
					ioend_time[x.id] = end_time + 4 + x.io_time
					print "time " + str(t) + "ms: Process " + tmp.id + " switching out of CPU; will block on I/O until time " + str(ioend_time[tmp.id]) + "ms " + printQueue(queue)
					t += 3
					end_time = end_time + 4 + x.io_time
					
					time_left = 0

			''' At each io end time'''
			for x in p:
				if(x.id in ioend_time):
					if(t == ioend_time[x.id] and (x not in queue) and (x not in done)):
						if current != []:
							tmp = current.pop()
						if time_left_arr != []:
							time_left = time_left_arr.pop()
						if time_left+cpu_start_t < ioend_time[x.id]:
							busy = 0
							num[tmp.id] -= 1
							if(num[tmp.id] == 0):
								if time_left_arr != []:
									time_left = time_left_arr.pop()
								t = time_left+cpu_start_t
								print "time " + str(t) + "ms: Process " + tmp.id + " terminated " + printQueue(queue)
								done.append(tmp)
								t +=3
								time_left = 0
								t +=1
						elif(x.cpu_burst_time < time_left and t!=end_time):
							print "time %dms: Process %s completed I/O and will preempt %s %s" %(t, x.id, tmp.id,printQueue(queue))
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
								print "time " + str(t) + "ms: Process " + x.id + " started using the CPU "  + printQueue(queue)
							cpu_start_t = t
							current.append(x)
						else:
							queue.append(x)
							print "time " + str(t) + "ms: Process " + x.id + " completed I/O; added to ready queue " + printQueue(queue)
						end_time = x.cpu_burst_time+t
						t -= 1
			t += 1
			if num_process ==3:
				if len(done) == num_process-1:
					break
		

	print "time " + str(t) + "ms: Simulator ended for SRT\n"
	
	wait_time = 0
	burst_time = 0
	turnaround_time = 0

	# for i in range(num_process):
	# 	wait_time += queue[i].wait_time
	# 	burst_time += queue[i].burst_time
	# 	turnaround_time += queue[i].turnaround_time
	# wait_time -= num_preemption*(t_cs/2)
	# if num_burst!=0:
	# 	wait_time /= float(num_burst)
	# 	burst_time /= float(num_burst)
	# 	turnaround_time /= float(num_burst)
	# else:
	# 	wait_time /= float(num_process)
	# 	burst_time /= float(num_process)
	# 	turnaround_time /= float(num_process)

	num_context_switch = 0.00
	for x in p:
		num_context_switch += x.num_bursts
		burst_time += x.cpu_burst_time * x.num_bursts
	if num_context_switch != 0:
		burst_time /= num_context_switch
	turnaround_time = burst_time + wait_time + 8	
	num_preemption = num_pre

	write_result(f,'SRT',burst_time,wait_time,turnaround_time,num_context_switch,num_preemption)
	
if __name__ == "__main__":
	if len(sys.argv)!=4 and len(sys.argv)!=3:
		sys.exit("ERROR: Invalid arguments\nUsage: ./a.out <input-file> <stats-output-file> [<rr-add>]")
	input_file = os.getcwd()+'/'+sys.argv[1]
	output_file = sys.argv[2]
	out = open(output_file,'w')
	if len(sys.argv)==4:
		rr_add = sys.argv[3]
	else:
		rr_add = 'END'
	queue = Queue.PriorityQueue()
	rr_queue = []
	p=[]
	try:
		f = open(input_file)
		for line in f:
			line = line.strip()
			if line and not line.startswith('#'):
				ele = line.split('|')
				proc_id,arrival_time,cpu_burst_time,num_bursts,io_time = ele
				if int(arrival_time)<sys.maxint:
					sys.maxint = int(arrival_time)
				proc = Process('READY', proc_id, arrival_time, cpu_burst_time, num_bursts, io_time)
				# print(proc_id)
				queue.put(proc)
				rr_queue.append(proc)
		f.close()
		
		SRT(out, rr_queue)
		FCFS(out,rr_queue)
	
		out.close()
	except ValueError as e:
		sys.exit("ERROR: Invalid input file format")
	main(sys.argv)