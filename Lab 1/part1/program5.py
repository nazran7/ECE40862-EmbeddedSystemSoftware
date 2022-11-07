class program5:
    def sum(self, list, target_num):
        temp = {}
        for i, num in enumerate(list):
            if target_num - num in temp:
                return (temp[target_num - num], i )
            temp[num] = i

list =  [10, 20, 10, 40, 50, 60, 70]
target_num  = int(input('What is your target number? '))
print("index1=%d, index2=%d" % program5().sum((list),target_num))           

