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
		num_processes+=1
	print "time %dms: Simulator started for SRT %s" %(t, printQueue(queue))
	
	if num_processes==1:
		while(1):
			# if(sum(num.values() == 0)):
			# 	break
			for x in p:

				if(x.arrival_time == t):
					# print "arrived", x.id)
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
				# print "started using cpu", x.id)
				# tmp2 = current.pop()
				# print "current", tmp2)
				if(queue != []):
					t += 4
					start_time = t
					tmp = queue.pop(0)
					end_time = start_time + tmp.cpu_burst_time
					ioend_time[tmp.id] = end_time + 4 + tmp.io_time
					busy = 1
					if time_left > 0:
						print "time " + str(t) + "ms: Process " + tmp.id + " started using the CPU with " + str(time_left) + "ms remaining " + printQueue(queue)
					else:
						print "time " + str(t) + "ms: Process " + tmp.id + " started using the CPU "  + printQueue(queue)
					current.append(tmp)
					cpu_start_t = t
			
			if(time_left+t < t+tmp.arrival_time):
				# print "end time change", x.id)
				end_time = t+tmp.arrival_time
			
			if(t == end_time):
				# print "now is end time", x.id)
				busy = 0
				if current != []:
					tmp = current.pop(0)
				# else:
				# 	if q
				# 	tmp = queue.pop(0)
				num[tmp.id] -= 1
				# print str(end_time)
				# print str(time_left)
				# print cpu_start_t)
				# print "end time"+str(end_time)
				if(num[tmp.id] == 0):
					# print "time " + str(t) + "ms: FIX-Process " + tmp.id + " terminated " + printQueue(queue)
					# current.remove(tmp)
					if queue != []:
						del queue[0]
					t = t+time_left
					print "time " + str(t) + "ms: Process " + tmp.id + " terminated " + printQueue(queue)
					t +=3
				# elif(num[tmp.id] == 1):
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
							# queue.append(tmp)
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
		print "time " + str(t) + "ms: Simulator ended for SRT\n"
	else:	
	
		while(1):
			# if(sum(num.values() == 0)):
			# 	break
			''' When processes first arrive'''
			for x in p:
				if(t ==x.arrival_time):
					if t == 0:
						queue.append(x)
						print "time " + str(t) + "ms: Process " + x.id + " arrived and added to ready queue " + printQueue(queue)
					else:	
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
			
			''' If CPU is not busy, start using CPU'''
			if(busy == 0):
				if(queue != []):
					t += 4
					start_time = t
					tmp = queue.pop(0)
					end_time = start_time + tmp.cpu_burst_time
					ioend_time[tmp.id] = end_time + 4 + tmp.io_time
					busy = 1

					if time_left_arr != []:	
						time_left = time_left_arr.pop()
					if time_left > 0:
						print "time " + str(t) + "ms: Process " + tmp.id + " started using the CPU with " + str(time_left) + "ms remaining " + printQueue(queue)
						end_time = t+time_left
					else:
						print "time " + str(t) + "ms: Process " + tmp.id + " started using the CPU "  + printQueue(queue)
						time_left = tmp.cpu_burst_time
						time_left_arr.append(time_left)
					current.append(tmp)
					cpu_start_t = t

			if(t == end_time and (x not in done) and num[tmp.id] >= 0):
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

		print "time " + str(t) + "ms: Simulator ended for SRT\n"
