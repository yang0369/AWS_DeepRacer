above_three_five = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,115,116,117,118]
above_three = [16,42,62,92,93,94,95,96,97,113,114]
above_two_five = [17,18,41,63,70,71,72,73,89,90,91,98,99,110,111,112]
above_two = [19,20,39,40,64,65,66,67,68,69,74,75,87,88,100,101,108,109]
strong_left = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]
below_two = [i for i in range(0, 119) if i not in above_three_five + above_three + above_two_five + above_two]

print(below_two)