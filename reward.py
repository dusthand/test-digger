import random
def run(list,val,tigger):
	
	r = [100]*10+[1000]*10+[300]*18+[5000]*4
	result = [0]*42
	
	while(len(r)>0):
		ri = random.random()*len(r)
		ri = int(ri)
		re = r[int(ri)]
		while(True):
			index = random.random()*sum(list)
			index = int(index)

			i = 0
			# print 1
			while(True):
				# print(list,len(list),i,index)
				if list[i]>index:
					break
				index -= list[i]
				i+=1
			# print(list,len(list))
			# print(i)
			if i >0 or tigger == 0:
				if re >= val:
					list[i] = 0
					result[i] = re
					break
				else:
					if list[i]==1:
						result[i] = re
						list[i] = 0
						break
					else:
						list[i] -=1
			elif tigger==1:
				val2 = sum(r)/len(r)
				if re >= val2:
					list[i] = 0
					result[i] = re
					break
				else:
					if list[i]==1:
						result[i] = re
						list[i] = 0
						break
					else:
						list[i] -=1
			elif tigger==2:
				val2 = r[int(len(r)/2)]
				if re >= val2:
					list[i] = 0
					result[i] = re
					break
				else:
					if list[i]==1:
						result[i] = re
						list[i] = 0
						break
					else:
						list[i] -=1
			elif tigger==3:
				# val2 = r[int(len(r)/2)]
				if re >= 1200:
					list[i] = 0
					result[i] = re
					break
				else:
					if list[i]==1:
						result[i] = re
						list[i] = 0
						break
					else:
						list[i] -=1



		del r[ri]
	return result

TEST_TIME = 10000
def main():
	for my in range(3,4):

		for val in [300,1000]:
			list = [my]*1+[2,3,3,3,3,1,3,3,3,3,3,3,3,3,3,2,3,3,2,3,1,3,3,3,1,3,3,3,3,3,3,1,1,3,1,1,3,2,1,2,2]
			summ = {}
			for i in range(TEST_TIME):
				list = [my]*1+[2,3,3,3,3,1,3,3,3,3,3,3,3,3,3,2,3,3,2,3,1,3,3,3,1,3,3,3,3,3,3,1,1,3,1,1,3,2,1,2,2]
				result = run(list,val,0)
				summ[result[0]] = summ.get(result[0],0)+1
			value = 0
			for i in summ:
				value+=i*summ[i]
			print(my,val,summ,value/TEST_TIME,TEST_TIME-summ[100]-summ[300])
		print "-"*40
		for val in [300,1000]:
			list = [my]*1+[3]*29
			summ = {}
			for i in range(TEST_TIME):
				list = [my]*1+[2,3,3,3,3,1,3,3,3,3,3,3,3,3,3,2,3,3,2,3,1,3,3,3,1,3,3,3,3,3,3,1,1,3,1,1,3,2,1,2,2]
				result = run(list,val,1)
				summ[result[0]] = summ.get(result[0],0)+1
			value = 0
			for i in summ:
				value+=i*summ[i]
			print(my,val,summ,value/TEST_TIME,TEST_TIME-summ[100]-summ[300])
		print "-"*40
		for val in [300,1000]:
			
			summ = {}
			for i in range(TEST_TIME):
				list = [my]*1+[2,3,3,3,3,1,3,3,3,3,3,3,3,3,3,2,3,3,2,3,1,3,3,3,1,3,3,3,3,3,3,1,1,3,1,1,3,2,1,2,2]
				result = run(list,val,2)
				summ[result[0]] = summ.get(result[0],0)+1
			value = 0
			for i in summ:
				value+=i*summ[i]
			print(my,val,summ,value/TEST_TIME,TEST_TIME-summ[100]-summ[300])
		print "-"*40
		for val in [300,1000]:
			
			summ = {}
			for i in range(TEST_TIME):
				list = [my]*1+[2,3,3,3,3,1,3,3,3,3,3,3,3,3,3,2,3,3,2,3,1,3,3,3,1,3,3,3,3,3,3,1,1,3,1,1,3,2,1,2,2]
				result = run(list,val,3)
				summ[result[0]] = summ.get(result[0],0)+1
			value = 0
			for i in summ:
				value+=i*summ[i]
			print(my,val,summ,value/TEST_TIME,TEST_TIME-summ[100]-summ[300])
		print "-"*40

main()
# print [1]*3+[2]*3