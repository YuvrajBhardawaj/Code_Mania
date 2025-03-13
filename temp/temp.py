i = input()
i = i[1:len(i)-1].split(',')
j=set()
if(i[0]==""):
	print(0)
else:
	for nums in i:
		j.add(int(nums))
	print(len(j))
