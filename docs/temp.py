test_cases = int(raw_input())
while test_cases != 0:
    test_cases -= 1
    ip = raw_input().strip().split(' ')
    l = int(ip[0])
    r = int(ip[1])
    unique_count = 0
    for x in xrange(l, r+1):
        
        non_sum = 0
        divisor_list = []
        while x != 0:
            temp = x%10
            if temp!=0:
                non_sum += temp ** temp
                divisor_list.append(temp)
            x = x//10
        # print non_sum
        # print '-divisor_list'
        # print divisor_list
        flag = 0
        for item in divisor_list:
            if non_sum % item != 0:
                flag = 1
                break
        if flag != 1:
            unique_count += 1
            
    print unique_count            