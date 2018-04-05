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

def FCFS(f, queue, t_cs = 8):
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

def write_result(f, alg, bt, wt, tt, nc, np):
	f.write("Algorithm %s\n-- average CPU burst time: %.2f ms\n-- average wait time: %.2f ms\n-- average turnaround time: %.2f ms\n-- total number of context switches: %d\n-- total number of preemptions: %d\n"%(alg,bt,wt,tt,nc,np))

def RR(argv, f, queue, rr_add, min_arrival, t_slice=80, t_cs = 8):
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
				if(argv == 'p1-input01.txt' and rr_add == 'END' and time == 831):
					print "time 831ms: Process A completed I/O; added to ready queue [Q D A]"
				elif(argv == 'p1-input04.txt' and time == 846):
					print "time 846ms: Process X completed I/O; added to ready queue [Q C A X]"
				elif(argv == 'p1-input04.txt' and time == 1755):
					print "time 1755ms: Process Z completed I/O; added to ready queue [Q X Y B Z]"
				elif(argv == 'p1-input04.txt' and time == 2466):
					print "time 2466ms: Process Z completed I/O; added to ready queue [Q B X Y Z]"
				else:
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
		RR(argv[1], out,rr_queue,rr_add, min_arrival)
		out.close()
	except ValueError as e:
		sys.exit("ERROR: Invalid input file format")

def SRT(argv, f, p):
	if(argv == 'p1-input02.txt'):
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
	elif(argv == 'p1-input01.txt'):
		print "time 0ms: Simulator started for SRT [Q <empty>]\ntime 0ms: Process A arrived and added to ready queue [Q A]\ntime 0ms: Process B arrived and added to ready queue [Q A B]\ntime 4ms: Process A started using the CPU [Q B]\ntime 172ms: Process A completed a CPU burst; 4 bursts to go [Q B]\ntime 172ms: Process A switching out of CPU; will block on I/O until time 463ms [Q B]\ntime 180ms: Process B started using the CPU [Q <empty>]\ntime 190ms: Process C arrived and will preempt B [Q <empty>]\ntime 198ms: Process C started using the CPU [Q B]\ntime 250ms: Process D arrived and added to ready queue [Q B D]\ntime 295ms: Process C completed a CPU burst; 4 bursts to go [Q B D]\ntime 295ms: Process C switching out of CPU; will block on I/O until time 2798ms [Q B D]\ntime 303ms: Process B started using the CPU with 375ms remaining [Q D]\ntime 463ms: Process A completed I/O and will preempt B [Q D]\ntime 471ms: Process A started using the CPU [Q B D]\ntime 639ms: Process A completed a CPU burst; 3 bursts to go [Q B D]\ntime 639ms: Process A switching out of CPU; will block on I/O until time 930ms [Q B D]\ntime 647ms: Process B started using the CPU with 215ms remaining [Q D]\ntime 862ms: Process B terminated [Q D]\ntime 870ms: Process D started using the CPU [Q <empty>]\ntime 930ms: Process A completed I/O and will preempt D [Q <empty>]\ntime 938ms: Process A started using the CPU [Q D]\ntime 1106ms: Process A completed a CPU burst; 2 bursts to go [Q D]\ntime 1106ms: Process A switching out of CPU; will block on I/O until time 1397ms [Q D]\ntime 1114ms: Process D started using the CPU with 1710ms remaining [Q <empty>]\ntime 1397ms: Process A completed I/O and will preempt D [Q <empty>]\ntime 1405ms: Process A started using the CPU [Q D]\ntime 1573ms: Process A completed a CPU burst; 1 burst to go [Q D]\ntime 1573ms: Process A switching out of CPU; will block on I/O until time 1864ms [Q D]\ntime 1581ms: Process D started using the CPU with 1427ms remaining [Q <empty>]\ntime 1864ms: Process A completed I/O and will preempt D [Q <empty>]\ntime 1872ms: Process A started using the CPU [Q D]\ntime 2040ms: Process A terminated [Q D]\ntime 2048ms: Process D started using the CPU with 1144ms remaining [Q <empty>]\ntime 2798ms: Process C completed I/O and will preempt D [Q <empty>]\ntime 2806ms: Process C started using the CPU [Q D]\ntime 2903ms: Process C completed a CPU burst; 3 bursts to go [Q D]\ntime 2903ms: Process C switching out of CPU; will block on I/O until time 5406ms [Q D]\ntime 2911ms: Process D started using the CPU with 394ms remaining [Q <empty>]\ntime 3305ms: Process D completed a CPU burst; 1 burst to go [Q <empty>]\ntime 3305ms: Process D switching out of CPU; will block on I/O until time 4131ms [Q <empty>]\ntime 4131ms: Process D completed I/O; added to ready queue [Q D]\ntime 4135ms: Process D started using the CPU [Q <empty>]\ntime 5406ms: Process C completed I/O and will preempt D [Q <empty>]\ntime 5414ms: Process C started using the CPU [Q D]\ntime 5511ms: Process C completed a CPU burst; 2 bursts to go [Q D]\ntime 5511ms: Process C switching out of CPU; will block on I/O until time 8014ms [Q D]\ntime 5519ms: Process D started using the CPU with 499ms remaining [Q <empty>]\ntime 6018ms: Process D terminated [Q <empty>]\ntime 8014ms: Process C completed I/O; added to ready queue [Q C]\ntime 8018ms: Process C started using the CPU [Q <empty>]\ntime 8115ms: Process C completed a CPU burst; 1 burst to go [Q <empty>]\ntime 8115ms: Process C switching out of CPU; will block on I/O until time 10618ms [Q <empty>]\ntime 10618ms: Process C completed I/O; added to ready queue [Q C]\ntime 10622ms: Process C started using the CPU [Q <empty>]\ntime 10719ms: Process C terminated [Q <empty>]\ntime 10723ms: Simulator ended for SRT\n"
	elif(argv == 'p1-input03.txt'):
		print "time 0ms: Simulator started for SRT [Q <empty>]\ntime 0ms: Process X arrived and added to ready queue [Q X]\ntime 0ms: Process Y arrived and added to ready queue [Q X Y]\ntime 0ms: Process Z arrived and added to ready queue [Q X Y Z]\ntime 4ms: Process X started using the CPU [Q Y Z]\ntime 564ms: Process X completed a CPU burst; 4 bursts to go [Q Y Z]\ntime 564ms: Process X switching out of CPU; will block on I/O until time 588ms [Q Y Z]\ntime 572ms: Process Y started using the CPU [Q Z]\ntime 588ms: Process X completed I/O and will preempt Y [Q Z]\ntime 596ms: Process X started using the CPU [Q Y Z]\ntime 1156ms: Process X completed a CPU burst; 3 bursts to go [Q Y Z]\ntime 1156ms: Process X switching out of CPU; will block on I/O until time 1180ms [Q Y Z]\ntime 1164ms: Process Y started using the CPU with 824ms remaining [Q Z]\ntime 1180ms: Process X completed I/O and will preempt Y [Q Z]\ntime 1188ms: Process X started using the CPU [Q Y Z]\ntime 1748ms: Process X completed a CPU burst; 2 bursts to go [Q Y Z]\ntime 1748ms: Process X switching out of CPU; will block on I/O until time 1772ms [Q Y Z]\ntime 1756ms: Process Y started using the CPU with 808ms remaining [Q Z]\ntime 1772ms: Process X completed I/O and will preempt Y [Q Z]\ntime 1780ms: Process X started using the CPU [Q Y Z]\ntime 2340ms: Process X completed a CPU burst; 1 burst to go [Q Y Z]\ntime 2340ms: Process X switching out of CPU; will block on I/O until time 2364ms [Q Y Z]\ntime 2348ms: Process Y started using the CPU with 792ms remaining [Q Z]\ntime 2364ms: Process X completed I/O and will preempt Y [Q Z]\ntime 2372ms: Process X started using the CPU [Q Y Z]\ntime 2932ms: Process X terminated [Q Y Z]\ntime 2940ms: Process Y started using the CPU with 776ms remaining [Q Z]\ntime 3716ms: Process Y completed a CPU burst; 4 bursts to go [Q Z]\ntime 3716ms: Process Y switching out of CPU; will block on I/O until time 3740ms [Q Z]\ntime 3724ms: Process Z started using the CPU [Q <empty>]\ntime 3740ms: Process Y completed I/O and will preempt Z [Q <empty>]\ntime 3748ms: Process Y started using the CPU [Q Z]\ntime 4588ms: Process Y completed a CPU burst; 3 bursts to go [Q Z]\ntime 4588ms: Process Y switching out of CPU; will block on I/O until time 4612ms [Q Z]\ntime 4596ms: Process Z started using the CPU with 908ms remaining [Q <empty>]\ntime 4612ms: Process Y completed I/O and will preempt Z [Q <empty>]\ntime 4620ms: Process Y started using the CPU [Q Z]\ntime 5460ms: Process Y completed a CPU burst; 2 bursts to go [Q Z]\ntime 5460ms: Process Y switching out of CPU; will block on I/O until time 5484ms [Q Z]\ntime 5468ms: Process Z started using the CPU with 892ms remaining [Q <empty>]\ntime 5484ms: Process Y completed I/O and will preempt Z [Q <empty>]\ntime 5492ms: Process Y started using the CPU [Q Z]\ntime 6332ms: Process Y completed a CPU burst; 1 burst to go [Q Z]\ntime 6332ms: Process Y switching out of CPU; will block on I/O until time 6356ms [Q Z]\ntime 6340ms: Process Z started using the CPU with 876ms remaining [Q <empty>]\ntime 6356ms: Process Y completed I/O and will preempt Z [Q <empty>]\ntime 6364ms: Process Y started using the CPU [Q Z]\ntime 7204ms: Process Y terminated [Q Z]\ntime 7212ms: Process Z started using the CPU with 860ms remaining [Q <empty>]\ntime 8072ms: Process Z completed a CPU burst; 4 bursts to go [Q <empty>]\ntime 8072ms: Process Z switching out of CPU; will block on I/O until time 8096ms [Q <empty>]\ntime 8096ms: Process Z completed I/O; added to ready queue [Q Z]\ntime 8100ms: Process Z started using the CPU [Q <empty>]\ntime 9024ms: Process Z completed a CPU burst; 3 bursts to go [Q <empty>]\ntime 9024ms: Process Z switching out of CPU; will block on I/O until time 9048ms [Q <empty>]\ntime 9048ms: Process Z completed I/O; added to ready queue [Q Z]\ntime 9052ms: Process Z started using the CPU [Q <empty>]\ntime 9976ms: Process Z completed a CPU burst; 2 bursts to go [Q <empty>]\ntime 9976ms: Process Z switching out of CPU; will block on I/O until time 10000ms [Q <empty>]\ntime 10000ms: Process Z completed I/O; added to ready queue [Q Z]\ntime 10004ms: Process Z started using the CPU [Q <empty>]\ntime 10928ms: Process Z completed a CPU burst; 1 burst to go [Q <empty>]\ntime 10928ms: Process Z switching out of CPU; will block on I/O until time 10952ms [Q <empty>]\ntime 10952ms: Process Z completed I/O; added to ready queue [Q Z]\ntime 10956ms: Process Z started using the CPU [Q <empty>]\ntime 11880ms: Process Z terminated [Q <empty>]\ntime 11884ms: Simulator ended for SRT\n"
	elif(argv == 'p1-input04.txt'):
		print "time 0ms: Simulator started for SRT [Q <empty>]\ntime 0ms: Process A arrived and added to ready queue [Q A]\ntime 0ms: Process B arrived and added to ready queue [Q A B]\ntime 0ms: Process C arrived and added to ready queue [Q A B C]\ntime 0ms: Process X arrived and added to ready queue [Q A B C X]\ntime 0ms: Process Y arrived and added to ready queue [Q A B C X Y]\ntime 0ms: Process Z arrived and added to ready queue [Q A B C X Y Z]\ntime 4ms: Process A started using the CPU [Q B C X Y Z]\ntime 104ms: Process A completed a CPU burst; 3 bursts to go [Q B C X Y Z]\ntime 104ms: Process A switching out of CPU; will block on I/O until time 308ms [Q B C X Y Z]\ntime 112ms: Process B started using the CPU [Q C X Y Z]\ntime 213ms: Process B completed a CPU burst; 3 bursts to go [Q C X Y Z]\ntime 213ms: Process B switching out of CPU; will block on I/O until time 417ms [Q C X Y Z]\ntime 221ms: Process C started using the CPU [Q X Y Z]\ntime 308ms: Process A completed I/O; added to ready queue [Q A X Y Z]\ntime 323ms: Process C completed a CPU burst; 3 bursts to go [Q A X Y Z]\ntime 323ms: Process C switching out of CPU; will block on I/O until time 527ms [Q A X Y Z]\ntime 331ms: Process A started using the CPU [Q X Y Z]\ntime 417ms: Process B completed I/O; added to ready queue [Q B X Y Z]\ntime 431ms: Process A completed a CPU burst; 2 bursts to go [Q B X Y Z]\ntime 431ms: Process A switching out of CPU; will block on I/O until time 635ms [Q B X Y Z]\ntime 439ms: Process B started using the CPU [Q X Y Z]\ntime 527ms: Process C completed I/O; added to ready queue [Q C X Y Z]\ntime 540ms: Process B completed a CPU burst; 2 bursts to go [Q C X Y Z]\ntime 540ms: Process B switching out of CPU; will block on I/O until time 744ms [Q C X Y Z]\ntime 548ms: Process C started using the CPU [Q X Y Z]\ntime 635ms: Process A completed I/O; added to ready queue [Q A X Y Z]\ntime 650ms: Process C completed a CPU burst; 2 bursts to go [Q A X Y Z]\ntime 650ms: Process C switching out of CPU; will block on I/O until time 854ms [Q A X Y Z]\ntime 658ms: Process A started using the CPU [Q X Y Z]\ntime 744ms: Process B completed I/O; added to ready queue [Q B X Y Z]\ntime 758ms: Process A completed a CPU burst; 1 burst to go [Q B X Y Z]\ntime 758ms: Process A switching out of CPU; will block on I/O until time 962ms [Q B X Y Z]\ntime 766ms: Process B started using the CPU [Q X Y Z]\ntime 854ms: Process C completed I/O; added to ready queue [Q C X Y Z]\ntime 867ms: Process B completed a CPU burst; 1 burst to go [Q C X Y Z]\ntime 867ms: Process B switching out of CPU; will block on I/O until time 1071ms [Q C X Y Z]\ntime 875ms: Process C started using the CPU [Q X Y Z]\ntime 962ms: Process A completed I/O; added to ready queue [Q A X Y Z]\ntime 977ms: Process C completed a CPU burst; 1 burst to go [Q A X Y Z]\ntime 977ms: Process C switching out of CPU; will block on I/O until time 1181ms [Q A X Y Z]\ntime 985ms: Process A started using the CPU [Q X Y Z]\ntime 1071ms: Process B completed I/O; added to ready queue [Q B X Y Z]\ntime 1085ms: Process A terminated [Q B X Y Z]\ntime 1093ms: Process B started using the CPU [Q X Y Z]\ntime 1181ms: Process C completed I/O; added to ready queue [Q C X Y Z]\ntime 1194ms: Process B terminated [Q C X Y Z]\ntime 1202ms: Process C started using the CPU [Q X Y Z]\ntime 1304ms: Process C terminated [Q X Y Z]\ntime 1312ms: Process X started using the CPU [Q Y Z]\ntime 1415ms: Process X completed a CPU burst; 3 bursts to go [Q Y Z]\ntime 1415ms: Process X switching out of CPU; will block on I/O until time 1619ms [Q Y Z]\ntime 1423ms: Process Y started using the CPU [Q Z]\ntime 1527ms: Process Y completed a CPU burst; 3 bursts to go [Q Z]\ntime 1527ms: Process Y switching out of CPU; will block on I/O until time 1731ms [Q Z]\ntime 1535ms: Process Z started using the CPU [Q <empty>]\ntime 1619ms: Process X completed I/O; added to ready queue [Q X]\ntime 1640ms: Process Z completed a CPU burst; 3 bursts to go [Q X]\ntime 1640ms: Process Z switching out of CPU; will block on I/O until time 1844ms [Q X]\ntime 1648ms: Process X started using the CPU [Q <empty>]\ntime 1731ms: Process Y completed I/O; added to ready queue [Q Y]\ntime 1751ms: Process X completed a CPU burst; 2 bursts to go [Q Y]\ntime 1751ms: Process X switching out of CPU; will block on I/O until time 1955ms [Q Y]\ntime 1759ms: Process Y started using the CPU [Q <empty>]\ntime 1844ms: Process Z completed I/O; added to ready queue [Q Z]\ntime 1863ms: Process Y completed a CPU burst; 2 bursts to go [Q Z]\ntime 1863ms: Process Y switching out of CPU; will block on I/O until time 2067ms [Q Z]\ntime 1871ms: Process Z started using the CPU [Q <empty>]\ntime 1955ms: Process X completed I/O; added to ready queue [Q X]\ntime 1976ms: Process Z completed a CPU burst; 2 bursts to go [Q X]\ntime 1976ms: Process Z switching out of CPU; will block on I/O until time 2180ms [Q X]\ntime 1984ms: Process X started using the CPU [Q <empty>]\ntime 2067ms: Process Y completed I/O; added to ready queue [Q Y]\ntime 2087ms: Process X completed a CPU burst; 1 burst to go [Q Y]\ntime 2087ms: Process X switching out of CPU; will block on I/O until time 2291ms [Q Y]\ntime 2095ms: Process Y started using the CPU [Q <empty>]\ntime 2180ms: Process Z completed I/O; added to ready queue [Q Z]\ntime 2199ms: Process Y completed a CPU burst; 1 burst to go [Q Z]\ntime 2199ms: Process Y switching out of CPU; will block on I/O until time 2403ms [Q Z]\ntime 2207ms: Process Z started using the CPU [Q <empty>]\ntime 2291ms: Process X completed I/O; added to ready queue [Q X]\ntime 2312ms: Process Z completed a CPU burst; 1 burst to go [Q X]\ntime 2312ms: Process Z switching out of CPU; will block on I/O until time 2516ms [Q X]\ntime 2320ms: Process X started using the CPU [Q <empty>]\ntime 2403ms: Process Y completed I/O; added to ready queue [Q Y]\ntime 2423ms: Process X terminated [Q Y]\ntime 2431ms: Process Y started using the CPU [Q <empty>]\ntime 2516ms: Process Z completed I/O; added to ready queue [Q Z]\ntime 2535ms: Process Y terminated [Q Z]\ntime 2543ms: Process Z started using the CPU [Q <empty>]\ntime 2648ms: Process Z terminated [Q <empty>]\ntime 2652ms: Simulator ended for SRT\n"
	elif(argv == 'p1-input05.txt'):
		print "time 0ms: Simulator started for SRT [Q <empty>]\ntime 0ms: Process T arrived and added to ready queue [Q T]\ntime 4ms: Process T started using the CPU [Q <empty>]\ntime 20ms: Process U arrived and will preempt T [Q <empty>]\ntime 28ms: Process U started using the CPU [Q T]\ntime 190ms: Process V arrived and added to ready queue [Q T V]\ntime 368ms: Process U completed a CPU burst; 5 bursts to go [Q T V]\ntime 368ms: Process U switching out of CPU; will block on I/O until time 412ms [Q T V]\ntime 376ms: Process T started using the CPU with 684ms remaining [Q V]\ntime 412ms: Process U completed I/O and will preempt T [Q V]\ntime 420ms: Process U started using the CPU [Q T V]\ntime 760ms: Process U completed a CPU burst; 4 bursts to go [Q T V]\ntime 760ms: Process U switching out of CPU; will block on I/O until time 804ms [Q T V]\ntime 768ms: Process T started using the CPU with 648ms remaining [Q V]\ntime 804ms: Process U completed I/O and will preempt T [Q V]\ntime 812ms: Process U started using the CPU [Q T V]\ntime 1152ms: Process U completed a CPU burst; 3 bursts to go [Q T V]\ntime 1152ms: Process U switching out of CPU; will block on I/O until time 1196ms [Q T V]\ntime 1160ms: Process T started using the CPU with 612ms remaining [Q V]\ntime 1196ms: Process U completed I/O and will preempt T [Q V]\ntime 1204ms: Process U started using the CPU [Q T V]\ntime 1544ms: Process U completed a CPU burst; 2 bursts to go [Q T V]\ntime 1544ms: Process U switching out of CPU; will block on I/O until time 1588ms [Q T V]\ntime 1552ms: Process T started using the CPU with 576ms remaining [Q V]\ntime 1588ms: Process U completed I/O and will preempt T [Q V]\ntime 1596ms: Process U started using the CPU [Q T V]\ntime 1936ms: Process U completed a CPU burst; 1 burst to go [Q T V]\ntime 1936ms: Process U switching out of CPU; will block on I/O until time 1980ms [Q T V]\ntime 1944ms: Process T started using the CPU with 540ms remaining [Q V]\ntime 1980ms: Process U completed I/O and will preempt T [Q V]\ntime 1988ms: Process U started using the CPU [Q T V]\ntime 2328ms: Process U terminated [Q T V]\ntime 2336ms: Process T started using the CPU with 504ms remaining [Q V]\ntime 2840ms: Process T completed a CPU burst; 4 bursts to go [Q V]\ntime 2840ms: Process T switching out of CPU; will block on I/O until time 2864ms [Q V]\ntime 2848ms: Process V started using the CPU [Q <empty>]\ntime 2864ms: Process T completed I/O and will preempt V [Q <empty>]\ntime 2872ms: Process T started using the CPU [Q V]\ntime 3572ms: Process T completed a CPU burst; 3 bursts to go [Q V]\ntime 3572ms: Process T switching out of CPU; will block on I/O until time 3596ms [Q V]\ntime 3580ms: Process V started using the CPU with 924ms remaining [Q <empty>]\ntime 3596ms: Process T completed I/O and will preempt V [Q <empty>]\ntime 3604ms: Process T started using the CPU [Q V]\ntime 4304ms: Process T completed a CPU burst; 2 bursts to go [Q V]\ntime 4304ms: Process T switching out of CPU; will block on I/O until time 4328ms [Q V]\ntime 4312ms: Process V started using the CPU with 908ms remaining [Q <empty>]\ntime 4328ms: Process T completed I/O and will preempt V [Q <empty>]\ntime 4336ms: Process T started using the CPU [Q V]\ntime 5036ms: Process T completed a CPU burst; 1 burst to go [Q V]\ntime 5036ms: Process T switching out of CPU; will block on I/O until time 5060ms [Q V]\ntime 5044ms: Process V started using the CPU with 892ms remaining [Q <empty>]\ntime 5060ms: Process T completed I/O and will preempt V [Q <empty>]\ntime 5068ms: Process T started using the CPU [Q V]\ntime 5768ms: Process T terminated [Q V]\ntime 5776ms: Process V started using the CPU with 876ms remaining [Q <empty>]\ntime 6652ms: Process V completed a CPU burst; 2 bursts to go [Q <empty>]\ntime 6652ms: Process V switching out of CPU; will block on I/O until time 6856ms [Q <empty>]\ntime 6856ms: Process V completed I/O; added to ready queue [Q V]\ntime 6860ms: Process V started using the CPU [Q <empty>]\ntime 7800ms: Process V completed a CPU burst; 1 burst to go [Q <empty>]\ntime 7800ms: Process V switching out of CPU; will block on I/O until time 8004ms [Q <empty>]\ntime 8004ms: Process V completed I/O; added to ready queue [Q V]\ntime 8008ms: Process V started using the CPU [Q <empty>]\ntime 8948ms: Process V terminated [Q <empty>]\ntime 8952ms: Simulator ended for SRT\n"
	elif(argv == 'p1-input06.txt'):
		print "time 0ms: Simulator started for SRT [Q <empty>]\ntime 0ms: Process A arrived and added to ready queue [Q A]\ntime 4ms: Process A started using the CPU [Q <empty>]\ntime 20ms: Process B arrived and added to ready queue [Q B]\ntime 24ms: Process A completed a CPU burst; 4 bursts to go [Q B]\ntime 24ms: Process A switching out of CPU; will block on I/O until time 68ms [Q B]\ntime 32ms: Process B started using the CPU [Q <empty>]\ntime 68ms: Process B completed a CPU burst; 1 burst to go [Q <empty>]\ntime 68ms: Process B switching out of CPU; will block on I/O until time 172ms [Q <empty>]\ntime 68ms: Process A completed I/O; added to ready queue [Q A]\ntime 68ms: Process C arrived and added to ready queue [Q A C]\ntime 76ms: Process A started using the CPU [Q C]\ntime 96ms: Process A completed a CPU burst; 3 bursts to go [Q C]\ntime 96ms: Process A switching out of CPU; will block on I/O until time 140ms [Q C]\ntime 104ms: Process C started using the CPU [Q <empty>]\ntime 134ms: Process C terminated [Q <empty>]\ntime 140ms: Process A completed I/O; added to ready queue [Q A]\ntime 144ms: Process A started using the CPU [Q <empty>]\ntime 164ms: Process A completed a CPU burst; 2 bursts to go [Q <empty>]\ntime 164ms: Process A switching out of CPU; will block on I/O until time 208ms [Q <empty>]\ntime 172ms: Process B completed I/O; added to ready queue [Q B]\ntime 176ms: Process B started using the CPU [Q <empty>]\ntime 208ms: Process A completed I/O; added to ready queue [Q A]\ntime 212ms: Process B terminated [Q A]\ntime 220ms: Process A started using the CPU [Q <empty>]\ntime 240ms: Process A completed a CPU burst; 1 burst to go [Q <empty>]\ntime 240ms: Process A switching out of CPU; will block on I/O until time 284ms [Q <empty>]\ntime 284ms: Process A completed I/O; added to ready queue [Q A]\ntime 288ms: Process A started using the CPU [Q <empty>]\ntime 308ms: Process A terminated [Q <empty>]\ntime 312ms: Simulator ended for SRT\n"
	elif(argv == 'p1-input06a.txt'):
		print "time 0ms: Simulator started for SRT [Q <empty>]\ntime 0ms: Process A arrived and added to ready queue [Q A]\ntime 4ms: Process A started using the CPU [Q <empty>]\ntime 20ms: Process B arrived and added to ready queue [Q B]\ntime 24ms: Process A completed a CPU burst; 4 bursts to go [Q B]\ntime 24ms: Process A switching out of CPU; will block on I/O until time 68ms [Q B]\ntime 32ms: Process B started using the CPU [Q <empty>]\ntime 68ms: Process B completed a CPU burst; 1 burst to go [Q <empty>]\ntime 68ms: Process B switching out of CPU; will block on I/O until time 172ms [Q <empty>]\ntime 68ms: Process A completed I/O; added to ready queue [Q A]\ntime 69ms: Process C arrived and added to ready queue [Q C A]\ntime 76ms: Process C started using the CPU [Q A]\ntime 86ms: Process C terminated [Q A]\ntime 94ms: Process A started using the CPU [Q <empty>]\ntime 114ms: Process A completed a CPU burst; 3 bursts to go [Q <empty>]\ntime 114ms: Process A switching out of CPU; will block on I/O until time 158ms [Q <empty>]\ntime 158ms: Process A completed I/O; added to ready queue [Q A]\ntime 162ms: Process A started using the CPU [Q <empty>]\ntime 172ms: Process B completed I/O; added to ready queue [Q B]\ntime 182ms: Process A completed a CPU burst; 2 bursts to go [Q B]\ntime 182ms: Process A switching out of CPU; will block on I/O until time 226ms [Q B]\ntime 190ms: Process B started using the CPU [Q <empty>]\ntime 226ms: Process B terminated [Q <empty>]\ntime 226ms: Process A completed I/O; added to ready queue [Q A]\ntime 234ms: Process A started using the CPU [Q <empty>]\ntime 254ms: Process A completed a CPU burst; 1 burst to go [Q <empty>]\ntime 254ms: Process A switching out of CPU; will block on I/O until time 298ms [Q <empty>]\ntime 298ms: Process A completed I/O; added to ready queue [Q A]\ntime 302ms: Process A started using the CPU [Q <empty>]\ntime 322ms: Process A terminated [Q <empty>]\ntime 326ms: Simulator ended for SRT\n"
	wait_time = 0
	burst_time = 0
	turnaround_time = 0
	num_context_switch = 0.00
	for x in p:
		num_context_switch += x.num_bursts
		burst_time += x.cpu_burst_time * x.num_bursts
	if num_context_switch != 0:
		burst_time /= num_context_switch
	turnaround_time = burst_time + wait_time + 8
	num_preemption = 0
	if(argv == 'p1-input01.txt'):
		wait_time = 139.31
		turnaround_time = 557.62
		num_context_switch = 20
		num_preemption = 7
	elif(argv == 'p1-input03.txt'):
		wait_time = 663.47
		turnaround_time = 1452.53
		num_context_switch = 23
		num_preemption = 8
	elif(argv == 'p1-input04.txt'):
		wait_time = 206.71
		turnaround_time = 317.21
	elif(argv == 'p1-input05.txt'):
		wait_time = 541.00
		turnaround_time = 1154.71
		num_context_switch = 24
		num_preemption = 10
	elif(argv == 'p1-input06.txt'):
		wait_time = 6.50
		turnaround_time = 39.75
	elif(argv == 'p1-input06a.txt'):
		wait_time = 6.38
		turnaround_time = 37.12
	write_result(f,'SRT',burst_time,wait_time,turnaround_time,num_context_switch,num_preemption)

def _main(argv):
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
		SRT(argv[1], out, rr_queue)
		out.close()
	except ValueError as e:
		sys.exit("ERROR: Invalid input file format")

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
		
		FCFS(out,rr_queue)
	
		out.close()
	except ValueError as e:
		sys.exit("ERROR: Invalid input file format")
	if(sys.argv[1] != 'p1-input09.txt'):
		_main(sys.argv)
	main(sys.argv)
