from solutions.Arrays_Hashing      import Solution as Arrays_Hashing
from solutions.Two_Pointers        import Solution as Two_Pointers
from solutions.Sliding_Window      import Solution as Sliding_Window
from solutions.Stack               import Solution as Stack
from solutions.Binary_Search       import Solution as Binary_Search
from solutions.Linked_List         import Solution as Linked_List
from solutions.Trees               import Solution as Trees
from solutions.Heap_Priority_Queue import Solution as Heap_Priority_Queue
from solutions.Backtracking        import Solution as Backtracking
from solutions.Tries               import Solution as Tries
from solutions.Graphs              import Solution as Graphs
from solutions.Advanced_Graphs     import Solution as Advanced_Graphs
from solutions.DP_1D               import Solution as DP_1D
from solutions.DP_2D               import Solution as DP_2D
from solutions.Greedy              import Solution as Greedy
from solutions.Intervals           import Solution as Intervals
from solutions.Math_Geometry       import Solution as Math_Geometry
from solutions.Bit_Manipulation    import Solution as Bit_Manipulation
from solutions.Finale              import Solution as Finale

from sys import argv
from Helper import Tester, ListHelper, TreeHelper, QuadTreeHelper, GraphHelper, IntervalHelper, shuffled, shuffled_size
t = Tester(); hl = ListHelper(); ht = TreeHelper(); hq = QuadTreeHelper(); hg = GraphHelper(); hv = IntervalHelper()

TESTS = [
    # 📋 ARRAYS & HASHING

    # 1
    lambda: t.test(Arrays_Hashing().getConcatenation, [
        (( [1,2,3,4] ), [1,2,3,4,1,2,3,4] ),
        (( [22,21,20,1] ), [22,21,20,1,22,21,20,1] ),
    ]),
    # 2
    lambda: t.test(Arrays_Hashing().hasDuplicate, [
        (( [1,2,3,3] ), True ),
        (( [1,2,3,4] ), False ),
    ]),
    # 3
    lambda: t.test(Arrays_Hashing().isAnagram, [
        (( "racecar", "carrace" ), True ),
        (( "jar", "jam" ), False ),
    ]),
    # 4
    lambda: t.test(Arrays_Hashing().twoSum, [
        (( [3,4,5,6], 7 ), [0,1] ),
        (( [4,5,6], 10 ), [0,2] ),
        (( [5,5], 10 ), [0,1] ),
    ]),
    # 5
    lambda: t.test(Arrays_Hashing().longestCommonPrefix, [
        (( ["bat","bag","bank","band"] ), "ba" ),
        (( ["dance","dag","danger","damage"] ), "da" ),
        (( ["neet","feet"] ), "" ),
    ]),
    # 6
    lambda: t.test(Arrays_Hashing().groupAnagrams, [
        (( ["act","pots","tops","cat","stop","hat"] ), [["act","cat"],["pots","tops","stop"],["hat"]] ),
        (( ["x"] ), [["x"]] ),
        (( [""] ), [[""]] ),
    ]),
    # 7
    lambda: t.test(Arrays_Hashing().removeElement, [
        (( [1,1,2,3,4], 1 ), len([2,3,4]) ),
        (( [0,1,2,2,3,0,4,2], 2 ), len([0,1,3,0,4]) ),
    ]),
    # 8
    lambda: t.test(Arrays_Hashing().majorityElement, [
        (( [5,5,1,1,1,5,5] ), 5 ),
        (( [2,2,2] ), 2 ),
    ]),
    # 9
    lambda: t.testcls(Arrays_Hashing().MyHashSet, (  ), [
        ("add", ( 1 ), None ),
        ("add", ( 2 ), None ),
        ("contains", ( 1 ), True ),
        ("contains", ( 3 ), False ),
        ("add", ( 2 ), None ),
        ("contains", ( 2 ), True ),
        ("remove", ( 2 ), None ),
        ("contains", ( 2 ), False ),
    ]),
    # 10
    lambda: t.testcls(Arrays_Hashing().MyHashMap, (  ), [
        ("put", ( 1, 1 ), None ),
        ("put", ( 2, 2 ), None ),
        ("get", ( 1 ), 1),
        ("get", ( 3 ), -1),
        ("put", ( 2, 1 ), None ),
        ("get", ( 2 ), 1),
        ("remove", ( 2 ), None ),
        ("get", ( 2 ), -1 ),
    ]),
    # 11
    lambda: t.test(Arrays_Hashing().sortArray, [
        (( [10,9,1,1,1,2,3,1] ), [1,1,1,1,2,3,9,10] ),
        (( [5,10,2,1,3] ), [1,2,3,5,10] ),
        (( shuffled ), list(range(shuffled_size)) ),
    ], time=2),
    # 12
    lambda: t.test(Arrays_Hashing().sortColors, [
        (( [1,0,1,2] ), [0,1,1,2] ),
        (( [2,1,0] ), [0,1,2] ),
    ]),
    # 13
    lambda: t.test(Arrays_Hashing().topKFrequent, [
        (( [1,2,2,3,3,3], 2 ), [3,2] ),
        (( [7,7], 1 ), [7] ),
    ]),
    # 14
    lambda: t.testcls(Arrays_Hashing().EncodeDecode, (  ), [
        ("decode", ( Arrays_Hashing().EncodeDecode().encode(["neet","code","love","you"]) ), ["neet","code","love","you"] ),
        ("decode", ( Arrays_Hashing().EncodeDecode().encode(["we","say",":","yes"]) ), ["we","say",":","yes"] ),
    ]),
    # 15
    lambda: t.testcls(Arrays_Hashing().NumMatrix, ( [
        [3,0,1,4,2],
        [5,6,3,2,1],
        [1,2,0,1,5],
        [4,1,0,1,7],
        [1,0,3,0,5]
    ] ), [
        ("sumRegion", ( 2, 1, 4, 3 ), 8 ),
        ("sumRegion", ( 1, 1, 2, 2 ), 11 ),
        ("sumRegion", ( 1, 2, 2, 4 ), 12 ),
    ]),
    # 16
    lambda: t.test(Arrays_Hashing().productExceptSelf, [
        (( [1,2,4,6] ), [48,24,12,8] ),
        (( [-1,0,1,2,3] ), [0,-6,0,0,0] ),
    ]),
    # 17
    lambda: t.test(Arrays_Hashing().isValidSudoku, [
        (( [
            ['1','2','.','.','3','.','.','.','.'],
            ['4','.','.','5','.','.','.','.','.'],
            ['.','9','8','.','.','.','.','.','3'],
            ['5','.','.','.','6','.','.','.','4'],
            ['.','.','.','8','.','3','.','.','5'],
            ['7','.','.','.','2','.','.','.','6'],
            ['.','.','.','.','.','.','2','.','.'],
            ['.','.','.','4','1','9','.','.','8'],
            ['.','.','.','.','8','.','.','7','9']
        ] ), True ),
        (( [
            ['1','2','.','.','3','.','.','.','.'],
            ['4','.','.','5','.','.','.','.','.'],
            ['.','9','1','.','.','.','.','.','3'],
            ['5','.','.','.','6','.','.','.','4'],
            ['.','.','.','8','.','3','.','.','5'],
            ['7','.','.','.','2','.','.','.','6'],
            ['.','.','.','.','.','.','2','.','.'],
            ['.','.','.','4','1','9','.','.','8'],
            ['.','.','.','.','8','.','.','7','9']
        ] ), False ),
    ]),
    # 18
    lambda: t.test(Arrays_Hashing().longestConsecutive, [
        (( [2,20,4,10,3,4,5] ), 4 ),
        (( [0,3,2,5,4,6,1,1] ), 7 ),
    ]),
    # 19
    lambda: t.test(Arrays_Hashing().maxProfit, [
        (( [7,1,5,3,6,4] ), 7 ),
        (( [1,2,3,4,5] ), 4 ),
    ]),
    # 20
    lambda: t.test(Arrays_Hashing().majorityElement2, [
        (( [5,2,3,2,2,2,2,5,5,5] ), [5,2] ),
        (( [4,4,4,4,4] ), [4] ),
        (( [1,2,3] ), [] ),
    ]),
    # 21
    lambda: t.test(Arrays_Hashing().subarraySum, [
        (( [2,-1,1,2], 2 ), 4 ),
        (( [4,4,4,4,4,4], 4 ), 6 ),
    ]),
    # 22
    lambda: t.test(Arrays_Hashing().firstMissingPositive, [
        (( [-2,-1,0] ), 1 ),
        (( [1,2,4] ), 3 ),
        (( [1,2,4,5,6,3,1] ), 7 ),
    ]),
    
    # ▶️ TWO POINTERS

    # 23
    lambda: t.test(Two_Pointers().reverseString, [
        (( ["n","e","e","t"] ), ["t","e","e","n"] ),
        (( ["r","a","c","e","c","a","r"] ), ["r","a","c","e","c","a","r"] ),
    ]),
    # 24
    lambda: t.test(Two_Pointers().isPalindrome, [
        (( "Was it a car or a cat I saw?" ), True ),
        (( "tab a cat" ), False ),
    ]),
    # 25
    lambda: t.test(Two_Pointers().validPalindrome, [
        (( "aca" ), True ),
        (( "abbadc" ), False ),
        (( "abbda" ), True ),
    ]),
    # 26
    lambda: t.test(Two_Pointers().mergeAlternately, [
        (( "abc", "xyz" ), "axbycz" ),
        (( "ab", "abbxxc" ), "aabbbxxc" ),
    ]),
    # 27
    lambda: t.test(Two_Pointers().merge, [
        (( [10,20,20,40,0,0], 4, [1,2], 2 ), [1,2,10,20,20,40] ),
        (( [0,0], 0, [1,2], 2 ), [1,2] ),
    ]),
    # 28
    lambda: t.test(Two_Pointers().removeDuplicates, [
        (( [1,1,2,3,4] ), 4 ),
        (( [2,10,10,30,30,30] ), 3 ),
    ]),
    # 29
    lambda: t.test(Two_Pointers().twoSum, [
        (( [1,2,3,4], 3 ), [1,2] ),
    ]),
    # 30
    lambda: t.test(Two_Pointers().threeSum, [
        (( [-1,0,1,2,-1,-4] ), [[-1,-1,2],[-1,0,1]] ),
        (( [0,1,1] ), [] ),
        (( [0,0,0] ), [[0,0,0]] ),
    ]),
    # 31
    lambda: t.test(Two_Pointers().fourSum, [
        (( [3,2,3,-3,1,0], 3 ), [[-3,0,3,3],[-3,1,2,3]] ),
        (( [1,-1,1,-1,1,-1], 2 ), [[-1,1,1,1]] ),
    ]),
    # 32
    lambda: t.test(Two_Pointers().rotate, [
        (( [1,2,3,4,5,6,7,8], 4 ), [5,6,7,8,1,2,3,4] ),
        (( [1000,2,4,-3], 2 ), [4,-3,1000,2] ),
        (( list(range(5*10**6)), 5000 ), [i % (5*10**6) for i in range((5*10**6)-5000, (5*10**6)*2-5000)] )
    ], space=512),
    # 33
    lambda: t.test(Two_Pointers().maxArea, [
        (( [1,7,2,5,4,7,3,6] ), 36 ),
        (( [2,2,2] ), 4 ),
    ]),
    # 34
    lambda: t.test(Two_Pointers().numRescueBoats, [
        (( [5,1,4,2], 6 ), 2 ),
        (( [1,3,2,3,2], 3 ), 4 ),
    ]),
    # 35
    lambda: t.test(Two_Pointers().trap, [
        (( [0,2,0,3,1,0,1,3,2,1] ), 9 ),
    ]),

    # 🪟 SLIDING WINDOW

    # 36
    lambda: t.test(Sliding_Window().containsNearbyDuplicate, [
        (( [1,2,3,1], 3 ), True ),
        (( [2,1,2], 1 ), False ),
    ]),
    # 37
    lambda: t.test(Sliding_Window().maxProfit, [
        (( [10,1,5,6,7,1] ), 6 ),
        (( [10,8,7,5,2] ), 0 ),
    ]),
    # 38
    lambda: t.test(Sliding_Window().lengthOfLongestSubstring, [
        (( "zxyzxyz" ), 3 ),
        (( "xxxx" ), 1 ),
    ]),
    # 39
    lambda: t.test(Sliding_Window().characterReplacement, [
        (( "XYYX", 2 ), 4 ),
        (( "AAABABB", 1 ), 5 ),
    ]),
    # 40
    lambda: t.test(Sliding_Window().checkInclusion, [
        (( "abc", "lecabee" ), True ),
        (( "abc", "lecaabee" ), False ),
    ]),
    # 41
    lambda: t.test(Sliding_Window().minSubArrayLen, [
        (( 10, [2,1,5,1,5,3] ), 3 ),
        (( 5, [1,2,1] ), 0 ),
    ]),
    # 42
    lambda: t.test(Sliding_Window().findClosestElements, [
        (( [2,4,5,8], 2, 6 ), [4,5] ),
        (( [2,3,4], 3, 1 ), [2,3,4] ),
    ]),
    # 43
    lambda: t.test(Sliding_Window().minWindow, [
        (( "OUZODYXAZV", "XYZ" ), "YXAZ" ),
        (( "xyz", "xyz" ), "xyz" ),
        (( "x", "xy" ), "" ),
    ]),
    # 44
    lambda: t.test(Sliding_Window().maxSlidingWindow, [
        (( [1,2,1,0,4,2,6], 3 ), [2,2,4,4,6] ),
    ]),

    # 📚 STACK

    # 45
    lambda: t.test(Stack().calPoints, [
        (( ["1","2","+","C","5","D"] ), 18 ),
        (( ["5","D","+","C"] ), 15 ),
    ]),
    # 46
    lambda: t.test(Stack().isValid, [
        (( "[]" ), True ),
        (( "([{}])" ), True ),
        (( "[(])" ), False ),
    ]),
    # 47
    lambda: t.testcls(Stack().MyStack, (  ), [
        ("push", ( 1 ), None ),
        ("push", ( 2 ), None ),
        ("top", (  ), 2 ),
        ("pop", (  ), 2 ),
        ("empty", (  ), False ),
    ]),
    # 48
    lambda: t.testcls(Stack().MyQueue, (  ), [
        ("push", ( 1 ), None ),
        ("push", ( 2 ), None ),
        ("peek", (  ), 1 ),
        ("pop", (  ), 1 ),
        ("empty", (  ), False ),
    ]),
    # 49
    lambda: t.testcls(Stack().MinStack, (  ), [
        ("push", ( 1 ), None ),
        ("push", ( 2 ), None ),
        ("push", ( 0 ), None ),
        ("getMin", (  ), 0 ),
        ("pop", (  ), None ),
        ("top", (  ), 2 ),
        ("getMin", (  ), 1 ),
    ]),
    # 50
    lambda: t.test(Stack().evalRPN, [
        (( ["1","2","+","3","*","4","-"] ), 5 ),
    ]),
    # 51
    lambda: t.test(Stack().asteroidCollision, [
        (( [2,4,-4,-1] ), [2] ),
        (( [5,5] ), [5,5] ),
        (( [7,-3,9] ), [7,9] ),
    ]),
    # 52
    lambda: t.test(Stack().dailyTemperatures, [
        (( [30,38,30,36,35,40,28] ), [1,4,1,2,1,0,0] ),
        (( [22,21,20] ), [0,0,0] ),
    ]),
    # 53
    lambda: t.testcls(Stack().StockSpanner, (  ), [
        ("next", ( 100 ), 1 ),
        ("next", ( 80 ), 1 ),
        ("next", ( 60 ), 1 ),
        ("next", ( 70 ), 2 ),
        ("next", ( 60 ), 1 ),
        ("next", ( 75 ), 4 ),
        ("next", ( 85 ), 6 ),
    ]),
    # 54
    lambda: t.test(Stack().carFleet, [
        (( 10, [1,4], [3,2] ), 1 ),
        (( 10, [4,1,0,7], [2,2,1,1] ), 3 ),
    ]),
    # 55
    lambda: t.test(Stack().simplifyPath, [
        (( "/neetcode/practice//...///../courses" ), "/neetcode/practice/courses" ),
        (( "/..//" ), "/" ),
        (( "/..//_home/a/b/..///" ), "/_home/a" ),
    ]),
    # 56
    lambda: t.test(Stack().decodeString, [
        (( "2[a3[b]]c" ), "abbbabbbc" ),
        (( "axb3[z]4[c]" ), "axbzzzcccc" ),
        (( "ab2[c]3[d]1[x]" ), "abccdddx" ),
    ]),
    # 57
    lambda: t.testcls(Stack().FreqStack, (  ), [
        ("push", ( 5 ), None ),
        ("push", ( 7 ), None ),
        ("push", ( 5 ), None ),
        ("push", ( 7 ), None ),
        ("push", ( 4 ), None ),
        ("push", ( 5 ), None ),
        ("pop", (  ), 5 ),
        ("pop", (  ), 7 ),
        ("pop", (  ), 5 ),
        ("pop", (  ), 4 ),
    ]),
    # 58
    lambda: t.test(Stack().largestRectangleArea, [
        (( [7,1,7,2,2,4] ), 8 ),
        (( [1,3,7] ), 7 ),
    ]),

    # 🎯 BINARY SEARCH

    # 59
    lambda: t.test(Binary_Search().search, [
        (( [-1,0,2,4,6,8], 4 ), 3 ),
        (( [-1,0,2,4,6,8], 3 ), -1 ),
    ]),
    # 60
    lambda: t.test(Binary_Search().searchInsert, [
        (( [-1,0,2,4,6,8], 5 ), 4 ),
        (( [-1,0,2,4,6,8], 10 ), 6 ),
    ]),
    # 61
    lambda: t.test(Binary_Search().guessNumber, [
        (( 5, 3 ), 3 ),
        (( 15, 10 ), 10 ),
        (( 1, 1 ), 1 ),
    ]),
    # 62
    lambda: t.test(Binary_Search().mySqrt, [
        (( 9 ), 3 ),
        (( 13 ), 3 ),
    ]),
    # 63
    lambda: t.test(Binary_Search().searchMatrix, [
        (( [
            [1,2,4,8],
            [10,11,12,13],
            [14,20,30,40]
        ], 10 ), True ),
        (( [
            [1,2,4,8],
            [10,11,12,13],
            [14,20,30,40]
        ], 15 ), False ),
    ]),
    # 64
    lambda: t.test(Binary_Search().minEatingSpeed, [
        (( [1,4,3,2], 9 ), 2 ),
        (( [25,10,23,4], 4 ), 25 ),
    ]),
    # 65
    lambda: t.test(Binary_Search().shipWithinDays, [
        (( [2,4,6,1,3,10], 4 ), 10 ),
        (( [1,2,3,4,5], 5 ), 5 ),
        (( [1,5,4,4,2,3], 3 ), 8 ),
    ]),
    # 66
    lambda: t.test(Binary_Search().findMin, [
        (( [3,4,5,6,1,2] ), 1 ),
        (( [4,5,0,1,2,3] ), 0 ),
        (( [4,5,6,7] ), 4 ),
    ]),
    # 67
    lambda: t.test(Binary_Search().searchRotated, [
        (( [3,4,5,6,1,2], 1 ), 4 ),
        (( [3,5,6,0,1,2], 4 ), -1 ),
    ]),
    # 68
    lambda: t.test(Binary_Search().searchRotated2, [
        (( [3,4,4,5,6,1,2,2], 1 ), True ),
        (( [3,5,6,0,0,1,2], 4 ), False ),
    ]),
    # 69
    lambda: t.testcls(Binary_Search().TimeMap, (  ), [
        ("set", ( "alice", "happy", 1 ), None ),
        ("get", ( "alice", 1 ), "happy" ),
        ("get", ( "alice", 2 ), "happy" ),
        ("set", ( "alice", "sad", 3 ), None ),
        ("get", ( "alice", 3 ), "sad" ),
    ]),
    # 70
    lambda: t.test(Binary_Search().splitArray, [
        (( [2,4,10,1,5], 2 ), 16 ),
        (( [1,0,2,3,5], 4 ), 5 ),
    ]),
    # 71
    lambda: t.test(Binary_Search().findMedianSortedArrays, [
        (( [1,2], [3] ), 2.0 ),
        (( [1,3], [2,4] ), 2.5 ),
    ]),
    # 72
    lambda: t.test(Binary_Search().findInMountainArray, [
        (( [2,4,5,2,1], 2 ), 0 ),
        (( [1,2,3,4,2,1], 6 ), -1 ),
    ]),

    # 🔗 LINKED LIST

    # 73
    lambda: t.test(Linked_List().reverseList, [
        (( hl.to([0,1,2,3]) ), hl.to([3,2,1,0]) ),
        (( hl.to([]) ), hl.to([]) ),
    ]),
    # 74
    lambda: t.test(Linked_List().mergeTwoLists, [
        (( hl.to([1,2,4]), hl.to([1,3,5]) ), hl.to([1,1,2,3,4,5]) ),
        (( hl.to([]), hl.to([1,2]) ), hl.to([1,2]) ),
    ]),
    # 75
    lambda: t.test(Linked_List().hasCycle, [
        (( hl.to([1,2,3,4], 1) ), True ),
        (( hl.to([1,2], -1) ), False ),
    ]),
    # 76
    lambda: t.test(Linked_List().reorderList, [
        (( hl.to([2,4,6,8]) ), hl.to([2,8,4,6]) ),
        (( hl.to([2,4,6,8,10]) ), hl.to([2,10,4,8,6]) ),
    ]),
    # 77
    lambda: t.test(Linked_List().removeNthFromEnd, [
        (( hl.to([1,2,3,4]), 2 ), hl.to([1,2,4]) ),
        (( hl.to([5]), 1 ), hl.to([]) ),
        (( hl.to([1,2]), 2 ), hl.to([2]) ),
    ]),
    # 78
    lambda: t.test(Linked_List().copyRandomList, [
        (( hl.to([[3,None],[7,3],[4,0],[5,1]]) ), hl.to([[3,None],[7,3],[4,0],[5,1]]) ),
        (( hl.to([[1,None],[2,2],[3,2]]) ), hl.to([[1,None],[2,2],[3,2]]) ),
    ]),
    # 79
    lambda: t.test(Linked_List().addTwoNumbers, [
        (( hl.to([1,2,3]), hl.to([4,5,6]) ), hl.to([5,7,9]) ),
        (( hl.to([9]), hl.to([9]) ), hl.to([8,1]) ),
    ]),
    # 80
    lambda: t.test(Linked_List().findDuplicate, [
        (( [1,2,3,2,2] ), 2 ),
        (( [1,2,3,4,4] ), 4 ),
    ]),
    # 81
    lambda: t.test(Linked_List().reverseBetween, [
        (( hl.to([1,2,3,4,5]), 1, 3 ), hl.to([3,2,1,4,5]) ),
        (( hl.to([1,1]), 1, 1 ), hl.to([1,1]) ),
    ]),
    # 82
    lambda: t.testcls(Linked_List().MyCircularQueue, ( 3 ), [
        ("enQueue", ( 1 ), True ),
        ("enQueue", ( 2 ), True ),
        ("enQueue", ( 3 ), True ),
        ("enQueue", ( 4 ), False ),
        ("Rear", (  ), 3 ),
        ("isFull", (  ), True ),
        ("deQueue", (  ), True ),
        ("enQueue", ( 4 ), True ),
        ("Rear", (  ), 4 ),
    ]),
    # 83
    lambda: t.testcls(Linked_List().LRUCache, ( 2 ), [
        ("put", ( 1, 10 ), None ),
        ("get", ( 1 ), 10 ),
        ("put", ( 2, 20 ), None ),
        ("put", ( 3, 30 ), None ),
        ("get", ( 2 ), 20 ),
        ("get", ( 1 ), -1 ),
    ]),
    # 84
    lambda: t.testcls(Linked_List().LFUCache, ( 2 ), [
        ("put", ( 1, 1 ), None ),
        ("put", ( 2, 2 ), None ),
        ("get", ( 1 ), 1 ),
        ("put", ( 3, 3 ), None ),
        ("get", ( 2 ), -1 ),
        ("get", ( 3 ), 3 ),
        ("put", ( 4, 4 ), None ),
        ("get", ( 1 ), -1 ),
        ("get", ( 3 ), 3 ),
        ("get", ( 4 ), 4 ),
    ]),
    # 85
    lambda: t.test(Linked_List().mergeKLists, [
        (( [hl.to([1,2,4]),hl.to([1,3,5]),hl.to([3,6])] ), hl.to([1,1,2,3,3,4,5,6]) ),
        (( [] ), hl.to([]) ),
        (( [hl.to([])] ), hl.to([]) ),
    ]),
    # 86
    lambda: t.test(Linked_List().reverseKGroup, [
        (( hl.to([1,2,3,4,5,6]), 3 ), hl.to([3,2,1,6,5,4]) ),
        (( hl.to([1,2,3,4,5]), 3 ), hl.to([3,2,1,4,5]) ),
    ]),

    # 🌳 TREES

    # 87
    lambda: t.test(Trees().inorderTraversal, [
        (( ht.to([1,2,3,4,5,6,7]) ), [4,2,5,1,6,3,7] ),
        (( ht.to([1,2,3,None,4,5,None]) ), [2,4,1,5,3] ),
        (( ht.to([]) ), [] ),
    ]),
    # 88
    lambda: t.test(Trees().preorderTraversal, [
        (( ht.to([1,2,3,4,5,6,7]) ), [1,2,4,5,3,6,7] ),
        (( ht.to([1,2,3,None,4,5,None]) ), [1,2,4,3,5] ),
        (( ht.to([]) ), [] ),
    ]),
    # 89
    lambda: t.test(Trees().postorderTraversal, [
        (( ht.to([1,2,3,4,5,6,7]) ), [4,5,2,6,7,3,1] ),
        (( ht.to([1,2,3,None,4,5,None]) ), [4,2,5,3,1] ),
        (( ht.to([]) ), [] ),
    ]),
    # 90
    lambda: t.test(Trees().invertTree, [
        (( ht.to([1,2,3,4,5,6,7]) ), ht.to([1,3,2,7,6,5,4]) ),
        (( ht.to([3,2,1]) ), ht.to([3,1,2]) ),
        (( ht.to([]) ), ht.to([]) ),
    ]),
    # 91
    lambda: t.test(Trees().maxDepth, [
        (( ht.to([1,2,3,None,None,4]) ), 3 ),
        (( ht.to([]) ), 0 ),
    ]),
    # 92
    lambda: t.test(Trees().diameterOfBinaryTree, [
        (( ht.to([1,None,2,3,4,5]) ), 3 ),
        (( ht.to([1,2,3]) ), 2 ),
    ]),
    # 93
    lambda: t.test(Trees().isBalanced, [
        (( ht.to([1,2,3,None,None,4]) ), True ),
        (( ht.to([1,2,3,None,None,4,None,5]) ),  ),
        (( ht.to([]) ), True ),
    ]),
    # 94
    lambda: t.test(Trees().isSameTree, [
        (( ht.to([1,2,3]), ht.to([1,2,3]) ), True ),
        (( ht.to([4,7]), ht.to([4,None,7]) ), False ),
        (( ht.to([1,2,3]), ht.to([1,3,2]) ), False ),
    ]),
    # 95
    lambda: t.test(Trees().isSubtree, [
        (( ht.to([1,2,3,4,5]), ht.to([2,4,5]) ), True ),
        (( ht.to([1,2,3,4,5,None,None,6]), ht.to([2,4,5]) ), False ),
    ]),
    # 96
    lambda: t.test(Trees().lowestCommonAncestor, [
        (( ht.to([5,3,8,1,4,7,9,None,2]), ht.to([3,1,4,None,2]), ht.to([8,7,9]) ), ht.to([5,3,8,1,4,7,9,None,2]) ),
        (( ht.to([5,3,8,1,4,7,9,None,2]), ht.to([3,1,4,None,2]), ht.to([4]) ), ht.to([3,1,4,None,2]) ),
    ]),
    # 97
    lambda: t.test(Trees().insertIntoBST, [
        (( ht.to([5,3,9,1,4]), 6 ), ht.to([5,3,9,1,4,6]) ),
        (( ht.to([5,3,6,None,4,None,10,None,None,7]), 9 ), ht.to([5,3,6,None,4,None,10,None,None,7,None,None,9]) ),
    ]),
    # 98
    lambda: t.test(Trees().deleteNode, [
        (( ht.to([5,3,9,1,4]), 3 ), ht.to([5,4,9,1]) ),
        (( ht.to([5,3,6,None,4,None,10,None,None,7]), 3 ), ht.to([5,4,6,None,None,None,10,7]) ),
    ]),
    # 99
    lambda: t.test(Trees().levelOrder, [
        (( ht.to([1,2,3,4,5,6,7]) ), [[1],[2,3],[4,5,6,7]] ),
        (( ht.to([1]) ), [[1]] ),
        (( ht.to([]) ), [] ),
    ]),
    # 100
    lambda: t.test(Trees().rightSideView, [
        (( ht.to([1,2,3]) ), [1,3] ),
        (( ht.to([1,2,3,4,5,6,7]) ), [1,3,7] ),
    ]),
    # 101
    lambda: t.test(Trees().construct, [
        (( [
            [1,1],
            [1,1]
        ] ), hq.to([[1,1]]) ),
        (( [
            [1,1,1,1],
            [0,0,0,0],
            [1,1,1,1],
            [1,1,1,1]
        ] ), hq.to([[0,0],[0,0],[0,0],[1,1],[1,1],[1,1],[1,1],[1,0],[1,0],[1,1],[1,1],[1,0],[1,0]]) ),
    ]),
    # 102
    lambda: t.test(Trees().goodNodes, [
        (( ht.to([2,1,1,3,None,1,5]) ), 3 ),
        (( ht.to([1,2,-1,3,4]) ), 4 ),
    ]),
    # 103
    lambda: t.test(Trees().isValidBST, [
        (( ht.to([2,1,3]) ), True ),
        (( ht.to([1,2,3]) ), False ),
    ]),
    # 104
    lambda: t.test(Trees().kthSmallest, [
        (( ht.to([2,1,3]), 1 ), 1 ),
        (( ht.to([4,3,5,2,None]), 4 ), 5 ),
    ]),
    # 105
    lambda: t.test(Trees().buildTree, [
        (( [1,2,3,4], [2,1,3,4] ), ht.to([1,2,3,None,None,None,4]) ),
        (( [1], [1] ), ht.to([1]) ),
    ]),
    # 106
    lambda: t.test(Trees().rob, [
        (( ht.to([1,4,None,2,3,3]) ), 7 ),
        (( ht.to([1,None,2,3,5,4,2]) ), 12 ),
    ]),
    # 107
    lambda: t.test(Trees().removeLeafNodes, [
        (( ht.to([1,2,3,5,2,2,5]), 2 ), ht.to([1,2,3,5,None,None,5]) ),
        (( ht.to([3,None,3,3]), 3 ), ht.to([]) ),
    ]),
    # 108
    lambda: t.test(Trees().maxPathSum, [
        (( ht.to([1,2,3]) ), 6 ),
        (( ht.to([-15,10,20,None,None,15,5,-5]) ), 40 ),
    ]),
    # 109
    lambda: t.testcls(Trees().Codec, (  ), [
        ("deserialize", ( Trees().Codec().serialize(ht.to([1,2,3,None,None,4,5])) ), ht.to([1,2,3,None,None,4,5]) ),
        ("deserialize", ( Trees().Codec().serialize(ht.to([])) ), ht.to([]) ),
    ]),

    # 🏔️ HEAP & PRIORITY QUEUE

    # 110
    lambda: t.testcls(Heap_Priority_Queue().KthLargest, ( 3, [1,2,3,3] ), [
        ("add", ( 3 ), 3 ),
        ("add", ( 5 ), 3 ),
        ("add", ( 6 ), 3 ),
        ("add", ( 7 ), 5 ),
        ("add", ( 8 ), 6 ),
    ]),
    # 111
    lambda: t.test(Heap_Priority_Queue().lastStoneWeight, [
        (( [2,3,6,2,4] ), 1 ),
        (( [1,2] ), 1 ),
    ]),
    # 112
    lambda: t.test(Heap_Priority_Queue().kClosest, [
        (( [[0,2],[2,2]], 1 ), [[0,2]] ),
        (( [[0,2],[2,0],[2,2]], 2 ), [[0,2],[2,0]] ),
    ]),
    # 113
    lambda: t.test(Heap_Priority_Queue().findKthLargest, [
        (( [2,3,1,5,4], 2 ), 4 ),
        (( [2,3,1,1,5,5,4], 3 ), 4 ),
    ]),
    # 114
    lambda: t.test(Heap_Priority_Queue().leastInterval, [
        (( ['X','X','Y','Y'], 2 ), 5 ),
        (( ['A','A','A','B','C'], 3 ), 9 ),
    ]),
    # 115
    lambda: t.testcls(Heap_Priority_Queue().Twitter, (  ), [
        ("postTweet", ( 1, 10 ), None ),
        ("postTweet", ( 2, 20 ), None ),
        ("getNewsFeed", ( 1 ), [10] ),
        ("getNewsFeed", ( 2 ), [20] ),
        ("follow", ( 1, 2 ), None ),
        ("getNewsFeed", ( 1 ), [20, 10] ),
        ("getNewsFeed", ( 2 ), [20] ),
        ("unfollow", ( 1, 2 ), None ),
        ("getNewsFeed", ( 1 ), [10] ),
    ]),
    # 116
    lambda: t.test(Heap_Priority_Queue().getOrder, [
        (( [[1,4],[3,3],[2,1]] ), [0,2,1] ),
        (( [[5,2],[4,4],[4,1],[2,1],[3,3]] ), [3,4,2,0,1] ),
    ]),
    # 117
    lambda: t.test(Heap_Priority_Queue().reorganizeString, [
        (( "axyy" ), "xyay" ),
        (( "abbccdd" ), "abcdbcd" ),
        (( "ccccd" ), "" ),
    ]),
    # 118
    lambda: t.test(Heap_Priority_Queue().longestDiverseString, [
        (( 3, 4, 2 ), "bababcabc" ),
        (( 0, 1, 5 ), "ccbcc" ),
    ]),
    # 119
    lambda: t.test(Heap_Priority_Queue().carPooling, [
        (( [[4,1,2],[3,2,4]], 4 ), True ),
        (( [[2,1,3],[3,2,4]], 4 ), False ),
    ]),
    # 120
    lambda: t.testcls(Heap_Priority_Queue().MedianFinder, (  ), [
        ("addNum", ( 1 ), None ),
        ("findMedian", (  ), 1.0 ),
        ("addNum", ( 3 ), None ),
        ("findMedian", (  ), 2.0 ),
        ("addNum", ( 2 ), None ),
        ("findMedian", (  ), 2.0 ),
    ]),
    # 121
    lambda: t.test(Heap_Priority_Queue().findMaximizedCapital, [
        (( 3, 0, [1,4,2,3], [0,3,1,1] ), 8 ),
        (( 4, 2, [2,3,1,5,3], [4,4,2,3,3] ), 14 ),
    ]),

    # 🌀 BACKTRACKING

    # 122
    lambda: t.test(Backtracking().subsetXORSum, [
        (( [2,4] ), 12 ),
        (( [3,1,1] ), 12 ),
    ]),
    # 123
    lambda: t.test(Backtracking().subsets, [
        (( [1,2,3] ), [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]] ),
        (( [7] ), [[],[7]] ),
    ]),
    # 124
    lambda: t.test(Backtracking().combinationSum, [
        (( [2,5,6,9], 9 ), [[2,2,5],[9]] ),
        (( [3,4,5], 16 ), [[3,3,3,3,4],[3,3,5,5],[3,4,4,5],[4,4,4,4]] ),
        (( [3], 5 ), [] ),
    ]),
    # 125
    lambda: t.test(Backtracking().combinationSum2, [
        (( [9,2,2,4,6,1,5], 8 ), [[1,2,5],[2,2,4],[2,6]] ),
        (( [1,2,3,4,5], 7 ), [[1,2,4],[2,5],[3,4]] ),
    ]),
    # 126
    lambda: t.test(Backtracking().combine, [
        (( 3, 2 ), [[1,2],[1,3],[2,3]] ),
        (( 3, 3 ), [[1,2,3]] ),
    ]),
    # 127
    lambda: t.test(Backtracking().permute, [
        (( [1,2,3] ), [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]] ),
        (( [7] ), [[7]] ),
    ]),
    # 128
    lambda: t.test(Backtracking().subsetsWithDup, [
        (( [1,2,1] ), [[],[1],[1,2],[1,1],[1,2,1],[2]] ),
        (( [7,7] ), [[],[7],[7,7]] ),
    ]),
    # 129
    lambda: t.test(Backtracking().permuteUnique, [
        (( [1,1,2] ), [[1,1,2],[1,2,1],[2,1,1]] ),
        (( [2,2] ), [[2,2]] ),
    ]),
    # 130
    lambda: t.test(Backtracking().generateParenthesis, [
        (( 1 ), ["()"] ),
        (( 3 ), ["((()))","(()())","(())()","()(())","()()()"] ),
    ]),
    # 131
    lambda: t.test(Backtracking().exist, [
        (( [
            ['A','B','C','D'],
            ['S','A','A','T'],
            ['A','C','A','E']
        ], "CAT" ), True ),
        (( [
            ['A','B','C','D'],
            ['S','A','A','T'],
            ['A','C','A','E']
        ], "BAT" ), False ),
    ]),
    # 132
    lambda: t.test(Backtracking().partition, [
        (( "aab" ), [["a","a","b"],["aa","b"]] ),
        (( "a" ), [["a"]] ),
    ]),
    # 133
    lambda: t.test(Backtracking().letterCombinations, [
        (( "34" ), ["dg","dh","di","eg","ei","fg","fh","fi"] ),
        (( "" ), [] ),
    ]),
    # 134
    lambda: t.test(Backtracking().makesquare, [
        (( [1,3,4,2,2,4] ), True ),
        (( [1,5,6,3] ), False ),
    ]),
    # 135
    lambda: t.test(Backtracking().canPartitionKSubsets, [
        (( [2,4,1,3,5], 3 ), True ),
        (( [1,2,3,4], 3 ), False ),
    ]),
    # 136
    lambda: t.test(Backtracking().solveNQueens, [
        (( 4 ), [
            [
                ".Q..",
                "...Q",
                "Q...",
                "..Q."
            ], [
                "..Q.",
                "Q...",
                "...Q",
                ".Q.."
            ]
        ] ),
        (( 1 ), [
            [
                "Q"
            ]
        ] ),
    ]),
    # 137
    lambda: t.test(Backtracking().totalNQueens, [
        (( 4 ), 2 ),
        (( 1 ), 1 ),
    ]),
    # 138
    lambda: t.test(Backtracking().wordBreak, [
        (( "neetcode", ["neet","code"] ), ["neet code"] ),
        (( "racecariscar", ["racecar","race","car","is"] ), ["racecar is car","race car is car"] ),
    ]),

    # 🔡 TRIES

    # 139
    lambda: t.testcls(Tries().PrefixTree, (  ), [
        ("insert", ( "dog" ), None ),
        ("search", ( "dog" ), True ),
        ("search", ( "do" ), False ),
        ("startsWith", ( "do" ), True ),
        ("insert", ( "do" ), None ),
        ("search", ( "do" ), True ),
    ]),
    # 140
    lambda: t.testcls(Tries().WordDictionary, (  ), [
        ("addWord", ( "day" ), None ),
        ("addWord", ( "bay" ), None ),
        ("addWord", ( "may" ), None ),
        ("search", ( "say" ), False ),
        ("search", ( "day" ), True ),
        ("search", ( ".ay" ), True ),
        ("search", ( "b.." ), True ),
    ]),
    # 141
    lambda: t.test(Tries().minExtraChar, [
        (( "neetcodes", ["neet","code","neetcode"] ), 1 ),
        (( "neetcodde", ["neet","code","neetcode"] ), 5 ),
    ]),
    # 142
    lambda: t.test(Tries().findWords, [
        (( [
            ['a','b','c','d'],
            ['s','a','a','t'],
            ['a','c','k','e'],
            ['a','c','d','n']
        ], ["bat","cat","back","backend","stack"] ), ["back","backend","cat"] ),
        (( [
            ['x','o'],
            ['x','o']
        ], ["xoxo"] ), [] ),
    ]),

    # 🗺️ GRAPHS

    # 143
    lambda: t.test(Graphs().islandPerimeter, [
        (( [
            [1,1,0,0],
            [1,0,0,0],
            [1,1,1,0],
            [0,0,1,1]
        ] ), 18 ),
        (( [
            [1,0]
        ] ), 4 ),
    ]),
    # 144
    lambda: t.test(Graphs().isAlienSorted, [
        (( ["dag","disk","dog"], "hlabcdefgijkmnopqrstuvwxyz" ), True ),
        (( ["neetcode","neet"], "worldabcefghijkmnpqstuvxyz" ), False ),
    ]),
    # 145
    lambda: t.test(Graphs().findJudge, [
        (( 4, [[1,3],[4,3],[2,3]] ), 3 ),
        (( 3, [[1,3],[2,3],[3,1],[3,2]] ), -1 ),
    ]),
    # 146
    lambda: t.test(Graphs().numIslands, [
        (( [
            ['0','1','1','1','0'],
            ['0','1','0','1','0'],
            ['1','1','0','0','0'],
            ['0','0','0','0','0']
        ] ), 1 ),
        (( [
            ['1','1','0','0','1'],
            ['1','1','0','0','1'],
            ['0','0','1','0','0'],
            ['0','0','0','1','1']
        ] ), 4 ),
    ]),
    # 147
    lambda: t.test(Graphs().maxAreaOfIsland, [
        (( [
            [0,1,1,0,1],
            [1,0,1,0,1],
            [0,1,1,0,1],
            [0,1,0,0,1]
        ] ), 6 ),
    ]),
    # 148
    lambda: t.test(Graphs().cloneGraph, [
        (( hg.to([[2],[1,3],[2]]) ), hg.to([[2],[1,3],[2]]) ),
        (( hg.to([[]]) ), hg.to([[]]) ),
        (( hg.to([]) ), hg.to([]) )
    ]),
    # 149
    lambda: t.test(Graphs().islandsAndTreasure, [
        (( [
            [2**31-1,-1,0,2**31-1],
            [2**31-1,2**31-1,2**31-1,-1],
            [2**31-1,-1,2**31-1,-1],
            [0,-1,2**31-1,2**31-1]
        ] ), [
            [3,-1,0,1],
            [2,2,1,-1],
            [1,-1,2,-1],
            [0,-1,3,4]
        ] ),
        (( [
            [0,-1],
            [2**31-1,2**31-1]
        ] ), [
            [0,-1],
            [1,2]
        ] ),
    ]),
    # 150
    lambda: t.test(Graphs().orangesRotting, [
        (( [
            [1,1,0],
            [0,1,1],
            [0,1,2]
        ] ), 4 ),
        (( [
            [1,0,1],
            [0,2,0],
            [1,0,1]
        ] ), -1 ),
    ]),
    # 151
    lambda: t.test(Graphs().pacificAtlantic, [
        (( [
            [4,2,7,3,4],
            [7,4,6,4,7],
            [6,3,5,3,6]
        ] ), [[0,2],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4],[2,0]] ),
        (( [
            [1],
            [1]
        ] ), [[0,0],[1,0]] ),
    ]),
    # 152
    lambda: t.test(Graphs().solve, [
        (( [
            ['X','X','X','X'],
            ['X','O','O','X'],
            ['X','O','O','X'],
            ['X','X','X','O']
        ] ), [
            ['X','X','X','X'],
            ['X','X','X','X'],
            ['X','X','X','X'],
            ['X','X','X','O']
        ] ),
    ]),
    # 153
    lambda: t.test(Graphs().openLock, [
        (( ["1111","0120","2020","3333"], "5555" ), 20 ),
        (( ["4443","4445","4434","4454","4344","4544","3444","5444"], "4444" ), -1 ),
    ]),
    # 154
    lambda: t.test(Graphs().canFinish, [
        (( 2, [[0,1]] ), True ),
        (( 2, [[0,1],[1,0]] ), False ),
    ]),
    # 155
    lambda: t.test(Graphs().findOrder, [
        (( 3, [[0,1]] ), [0,1,2] ),
        (( 3, [[0,1],[1,2],[2,0]] ), [] ),
    ]),
    # 156
    lambda: t.test(Graphs().validTree, [
        (( 5, [[0,1],[0,2],[0,3],[1,4]] ), True ),
        (( 5, [[0,1],[1,2],[2,3],[1,3],[1,4]] ), False ),
    ]),
    # 157
    lambda: t.test(Graphs().checkIfPrerequisite, [
        (( 4, [[1,0],[2,1],[3,2]], [[0,1],[3,1]] ), [False,True] ),
        (( 2, [[1,0]], [[0,1]] ), [False] ),
    ]),
    # 158
    lambda: t.test(Graphs().countComponents, [
        (( 3, [[0,1],[0,2]] ), 1 ),
        (( 6, [[0,1],[1,2],[2,3],[4,5]] ), 2 ),
    ]),
    # 159
    lambda: t.test(Graphs().findRedundantConnection, [
        (( [[1,2],[1,3],[3,4],[2,4]] ), [2,4] ),
        (( [[1,2],[1,3],[1,4],[3,4],[4,5]] ), [3,4] ),
    ]),
    # 160
    lambda: t.test(Graphs().accountsMerge, [
        (( [
            ["neet","neet@gmail.com","neet_dsa@gmail.com"],
            ["alice","alice@gmail.com"],
            ["neet","bob@gmail.com","neet@gmail.com"],
            ["neet","neetcode@gmail.com"]
        ] ), [
            ["neet","bob@gmail.com","neet@gmail.com","neet_dsa@gmail.com"],
            ["alice","alice@gmail.com"],
            ["neet","neetcode@gmail.com"]
        ] ),
        (( [
            ["James","james@mail.com"],
            ["James","james@mail.co"]
        ] ), [
            ["James","james@mail.com"],
            ["James","james@mail.co"]
        ] ),
    ]),
    # 161
    lambda: t.test(Graphs().calcEquation, [
        (( [["a","b"],["b","c"],["ab","bc"]], [4.0,1.0,3.25], [["a","c"],["b","a"],["c","c"],["ab","a"],["d","d"]] ), [4.0,0.25,1.0,-1.0,-1.0] ),
        (( [["a","b"]], [0.5], [["a","b"],["b","a"]] ), [0.5,2.0] ),
    ]),
    # 162
    lambda: t.test(Graphs().findMinHeightTrees, [
        (( 5, [[0,1],[3,1],[2,3],[4,1]] ), [3,1] ),
        (( 4, [[1,0],[2,0],[3,0]] ), [0] ),
    ]),
    # 163
    lambda: t.test(Graphs().ladderLength, [
        (( "cat", "sag", ["bat","bag","sag","dag","dot"] ), 4 ),
        (( "cat", "sag", ["bat","bag","sat","dag","dot"] ), 0 ),
    ]),

    # 🧠 ADVANCED GRAPHS

    # 164
    lambda: t.test(Advanced_Graphs().minimumEffortPath, [
        (( [
            [1,1,1],
            [3,2,4],
            [2,5,4]
        ] ), 2 ),
        (( [
            [1,1,1],
            [1,1,2],
            [6,5,2]
        ] ), 1 ),
    ]),
    # 165
    lambda: t.test(Advanced_Graphs().networkDelayTime, [
        (( [[1,2,1],[2,3,1],[1,4,4],[3,4,1]], 4, 1 ), 3 ),
        (( [[1,2,1],[2,3,1]], 3, 2 ), -1 ),
    ]),
    # 166
    lambda: t.test(Advanced_Graphs().findItinerary, [
        (( [["BUF","HOU"],["HOU","SEA"],["JFK","BUF"]] ), ["JFK","BUF","HOU","SEA"] ),
        (( [["HOU","JFK"],["SEA","JFK"],["JFK","SEA"],["JFK","HOU"]] ), ["JFK","HOU","JFK","SEA","JFK"] ),
    ]),
    # 167
    lambda: t.test(Advanced_Graphs().minCostConnectPoints, [
        (( [[0,0],[2,2],[3,3],[2,4],[4,2]] ), 10 ),
    ]),
    # 168
    lambda: t.test(Advanced_Graphs().swimInWater, [
        (( [
            [0,1],
            [2,3]
        ] ), 3 ),
        (( [
            [0,1,2,10],
            [9,14,4,13],
            [12,3,8,15],
            [11,5,7,6]
        ] ), 8 ),
    ]),
    # 169
    lambda: t.test(Advanced_Graphs().foreignDictionary, [
        (( ["z","o"] ), "zo" ),
        (( ["hrn","hrf","er","enn","rfnn"] ), "hernf" ),
    ]),
    # 170
    lambda: t.test(Advanced_Graphs().findCheapestPrice, [
        (( 4, [[0,1,200],[1,2,100],[1,3,300],[2,3,100]], 0, 3, 1 ), 500 ),
        (( 3, [[1,0,100],[1,2,200],[0,2,100]], 1, 2, 1 ), 200 ),
    ]),
    # 171
    lambda: t.test(Advanced_Graphs().findCriticalAndPseudoCriticalEdges, [
        (( 4, [[0,3,2],[0,2,5],[1,2,4]] ), [[0,2,1],[]] ),
        (( 5, [[0,3,2],[0,4,2],[1,3,2],[3,4,2],[2,3,1],[1,2,3],[0,1,1]] ), [[4,6],[0,1,2,3]] ),
    ]),
    # 172
    lambda: t.test(Advanced_Graphs().buildMatrix, [
        (( 3, [[2,1],[1,3]], [[3,1],[2,3]] ), [[2,0,0],[0,0,1],[0,3,0]] ),
        (( 3, [[1,2],[2,3],[3,1],[2,3]], [[2,1]] ), [] ),
    ]),
    # 173
    lambda: t.test(Advanced_Graphs().canTraverseAllPairs, [
        (( [4,3,12] ), True ),
        (( [2,3,7] ), False ),
    ]),

    # 📊 1-D DYNAMIC PROGRAMMING

    # 174
    lambda: t.test(DP_1D().climbStairs, [
        (( 2 ), 2 ),
        (( 3 ), 3 ),
    ]),
    # 175
    lambda: t.test(DP_1D().minCostClimbingStairs, [
        (( [1,2,3] ), 2 ),
        (( [1,2,1,2,1,1,1] ), 4 ),
    ]),
    # 176
    lambda: t.test(DP_1D().tribonacci, [
        (( 3 ), 2 ),
        (( 21 ), 121415 ),
    ]),
    # 177
    lambda: t.test(DP_1D().rob, [
        (( [1,1,3,3] ), 4 ),
        (( [2,9,8,3,6] ), 16 ),
    ]),
    # 178
    lambda: t.test(DP_1D().rob2, [
        (( [3,4,3] ), 4 ),
        (( [2,9,8,3,6] ), 15 ),
    ]),
    # 179
    lambda: t.test(DP_1D().longestPalindrome, [
        (( "ababd" ), "aba" ),
        (( "abbc" ), "bb" ),
    ]),
    # 180
    lambda: t.test(DP_1D().countSubstrings, [
        (( "abc" ), 3 ),
        (( "aaa" ), 6 ),
    ]),
    # 181
    lambda: t.test(DP_1D().numDecodings, [
        (( "12" ), 2 ),
        (( "01" ), 0 ),
    ]),
    # 182
    lambda: t.test(DP_1D().coinChange, [
        (( [1,5,10], 12 ), 3 ),
        (( [2], 3 ), -1 ),
        (( [1], 0 ), 0 ),
    ]),
    # 183
    lambda: t.test(DP_1D().maxProduct, [
        (( [1,2,-3,4] ), 4 ),
        (( [-2,-1] ), 2 ),
    ]),
    # 184
    lambda: t.test(DP_1D().wordBreak, [
        (( "neetcode", ["neet","code"] ), True ),
        (( "applepenapple", ["apple","pen","ape"] ), True ),
        (( "catsincars", ["cats","cat","sin","in","car"] ), False )
    ]),
    # 185
    lambda: t.test(DP_1D().lengthOfLIS, [
        (( [9,1,4,2,3,3,7] ), 4 ),
        (( [0,3,1,3,2,3] ), 4 ),
    ]),
    # 186
    lambda: t.test(DP_1D().canPartition, [
        (( [1,2,3,4] ), True ),
        (( [1,2,3,4,5] ), False ),
    ]),
    # 187
    lambda: t.test(DP_1D().combinationSum4, [
        (( [3,1,2], 4 ), 7 ),
        (( [1], 3 ), 1 ),
    ]),
    # 188
    lambda: t.test(DP_1D().numSquares, [
        (( 13 ), 2 ),
        (( 6 ), 3 ),
    ]),
    # 189
    lambda: t.test(DP_1D().integerBreak, [
        (( 4 ), 4 ),
        (( 12 ), 81 ),
    ]),
    # 190
    lambda: t.test(DP_1D().stoneGameIII, [
        (( [2,4,3,1] ), "Alice" ),
        (( [1,2,1,5] ), "Bob" ),
        (( [5,-3,3,5] ), "Tie" ),
    ]),

    # 🧩 2-D DYNAMIC PROGRAMMING

    # 191
    lambda: t.test(DP_2D().uniquePaths, [
        (( 3, 6 ), 21 ),
        (( 3, 3 ), 6 ),
    ]),
    # 192
    lambda: t.test(DP_2D().uniquePathsWithObstacles, [
        (( [
            [0,0,0],
            [0,0,0],
            [0,1,0]
        ] ), 3 ),
        (( [
            [0,0,0],
            [0,0,1],
            [0,1,0]
        ] ), 0 ),
    ]),
    # 193
    lambda: t.test(DP_2D().minPathSum, [
        (( [
            [1,2,0],
            [5,4,2],
            [1,1,3]
        ] ), 8 ),
        (( [
            [2,2],
            [1,0]
        ] ), 3 ),
    ]),
    # 194
    lambda: t.test(DP_2D().longestCommonSubsequence, [
        (( "cat", "crabt" ), 3 ),
        (( "abcd", "abcd" ), 4 ),
        (( "abcd", "efgh" ), 0 ),
    ]),
    # 195
    lambda: t.test(DP_2D().lastStoneWeightII, [
        (( [2,4,1,5,6,3] ), 1 ),
        (( [4,4,1,7,10] ), 2 ),
    ]),
    # 196
    lambda: t.test(DP_2D().maxProfit, [
        (( [1,3,4,0,4] ), 6 ),
        (( [1] ), 0 ),
    ]),
    # 197
    lambda: t.test(DP_2D().change, [
        (( 4, [1,2,3] ), 4 ),
        (( 7, [2,4] ), 0 ),
    ]),
    # 198
    lambda: t.test(DP_2D().findTargetSumWays, [
        (( [2,2,2], 2 ), 3 ),
    ]),
    # 199
    lambda: t.test(DP_2D().isInterleave, [
        (( "aaaa", "bbbb", "aabbbbaa" ), True ),
        (( "", "", "" ), True ),
        (( "abc", "xyz", "abxzcy" ), False ),
    ]),
    # 200
    lambda: t.test(DP_2D().stoneGame, [
        (( [1,2,3,1] ), True ),
        (( [2,1] ), True ),
    ]),
    # 201
    lambda: t.test(DP_2D().stoneGameII, [
        (( [3,1,2,5,7] ), 10 ),
        (( [4,3,2,5,10] ), 11 ),
    ]),
    # 202
    lambda: t.test(DP_2D().longestIncreasingPath, [
        (( [
            [5,5,3],
            [2,3,6],
            [1,1,1]
        ] ), 4 ),
        (( [
            [1,2,3],
            [2,1,4],
            [7,6,5]
        ] ), 7 ),
    ]),
    # 203
    lambda: t.test(DP_2D().numDistinct, [
        (( "caaat", "cat" ), 3 ),
        (( "xxyxy", "xy" ), 5 ),
    ]),
    # 204
    lambda: t.test(DP_2D().minDistance, [
        (( "monkeys", "money" ), 2 ),
        (( "neetcdee", "neetcode" ), 3 ),
    ]),
    # 205
    lambda: t.test(DP_2D().maxCoins, [
        (( [4,2,3,7] ), 143 ),
    ]),
    # 206
    lambda: t.test(DP_2D().isMatch, [
        (( "aa", ".b" ), False ),
        (( "nnn", "n*" ), True ),
        (( "xyz", ".*z" ), True ),
    ]),

    # 💲 GREEDY

    # 207
    lambda: t.test(Greedy().lemonadeChange, [
        (( [5,10,5,5,20] ), True ),
        (( [5,20,10,5] ), False ),
    ]),
    # 208
    lambda: t.test(Greedy().maxSubArray, [
        (( [2,-3,4,-2,2,1,-1,4] ), 8 ),
        (( [-1] ), -1 ),
    ]),
    # 209
    lambda: t.test(Greedy().maxSubarraySumCircular, [
        (( [-2,4,-5,4,-5,9,4] ), 15 ),
        (( [2,3,-4] ), 5 ),
    ]),
    # 210
    lambda: t.test(Greedy().maxTurbulenceSize, [
        (( [2,4,3,2,2,5,1,4] ), 4 ),
        (( [1,1,2] ), 2 ),
    ]),
    # 211
    lambda: t.test(Greedy().canJump, [
        (( [1,2,0,1,0] ), True ),
        (( [1,2,1,0,1] ), False ),
    ]),
    # 212
    lambda: t.test(Greedy().jump, [
        (( [2,4,1,1,1,1] ), 2 ),
        (( [2,1,2,1,0] ), 2 ),
    ]),
    # 213
    lambda: t.test(Greedy().canReach, [
        (( "00110010", 2, 4 ), True ),
        (( "0010", 1, 1 ), False ),
    ]),
    # 214
    lambda: t.test(Greedy().canCompleteCircuit, [
        (( [1,2,3,4], [2,2,4,1] ), 3 ),
        (( [1,2,3], [2,3,2] ), -1 ),
    ]),
    # 215
    lambda: t.test(Greedy().isNStraightHand, [
        (( [1,2,4,2,3,5,3,4], 4 ), True ),
        (( [1,2,3,3,4,5,6,7], 4 ), False ),
    ]),
    # 216
    lambda: t.test(Greedy().predictPartyVictory, [
        (( "RRDDD" ), "Radiant" ),
        (( "RDD" ), "Dire" ),
    ]),
    # 217
    lambda: t.test(Greedy().mergeTriplets, [
        (( [[1,2,3],[7,1,1]], [7,2,3] ), True ),
        (( [[2,5,6],[1,4,4],[5,7,5]], [5,4,6] ), False ),
    ]),
    # 218
    lambda: t.test(Greedy().partitionLabels, [
        (( "xyxxyzbzbbisl" ), [5,5,1,1,1] ),
        (( "abcabc" ), [6] ),
    ]),
    # 219
    lambda: t.test(Greedy().checkValidString, [
        (( "((**)" ), True ),
        (( "(((*)" ), False ),
    ]),
    # 220
    lambda: t.test(Greedy().candy, [
        (( [4,3,5] ), 5 ),
        (( [2,3,3] ), 4 ),
    ]),

    # 📐 INTERVALS

    # 221
    lambda: t.test(Intervals().insert, [
        (( [[1,3],[4,6]], [2,5] ), [[1,6]] ),
        (( [[1,2],[3,5],[9,10]], [6,7] ), [[1,2],[3,5],[6,7],[9,10]] ),
    ]),
    # 222
    lambda: t.test(Intervals().merge, [
        (( [[1,3],[1,5],[6,7]] ), [[1,5],[6,7]] ),
        (( [[1,2],[2,3]] ), [[1,3]] ),
    ]),
    # 223
    lambda: t.test(Intervals().eraseOverlapIntervals, [
        (( [[1,2],[2,4],[1,4]] ), 1 ),
        (( [[1,2],[2,4]] ), 0 ),
    ]),
    # 224
    lambda: t.test(Intervals().canAttendMeetings, [
        (( hv.to([(0,30),(5,10),(15,20)]) ), False ),
        (( hv.to([(5,8),(9,15)]) ), True ),
    ]),
    # 225
    lambda: t.test(Intervals().minMeetingRooms, [
        (( hv.to([(0,40),(5,10),(15,20)]) ), 2 ),
        (( hv.to([(4,9)]) ), 1 ),
    ]),
    # 226
    lambda: t.test(Intervals().mostBooked, [
        (( 2, [[1,10],[2,10],[3,10],[4,10]] ), 0 ),
        (( 3, [[1,20],[2,10],[3,5],[6,8],[4,9]] ), 1 ),
    ]),
    # 227
    lambda: t.test(Intervals().minInterval, [
        (( [[1,3],[2,3],[3,7],[6,6]], [2,3,1,7,6,8] ), [2,2,3,5,1,-1] ),
    ]),

    # 🧮 MATH & GEOMETRY

    # 228
    lambda: t.test(Math_Geometry().convertToTitle, [
        (( 32 ), "AF" ),
        (( 53 ), "BA" ),
    ]),
    # 229
    lambda: t.test(Math_Geometry().gcdOfStrings, [
        (( "ABAB", "AB" ), "AB" ),
        (( "NANANA", "NANA" ), "NA" ),
    ]),
    # 230
    lambda: t.test(Math_Geometry().insertGreatestCommonDivisors, [
        (( [12,3,4,6] ), [12,3,3,1,4,2,6] ),
        (( [2,1] ), [2,1,1] ),
    ]),
    # 231
    lambda: t.test(Math_Geometry().transpose, [
        (( [
            [2,1],
            [-1,3]
        ] ), [
            [2,-1],
            [1,3]
        ] ),
        (( [
            [1,0,5],
            [2,4,3]
        ] ), [
            [1,2],
            [0,4],
            [5,3]
        ] ),
    ]),
    # 232
    lambda: t.test(Math_Geometry().rotate, [
        (( [
            [1,2],
            [3,4]
        ] ), [
            [3,1],
            [4,2]
        ] ),
        (( [
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ] ), [
            [7,4,1],
            [8,5,2],
            [9,6,3]
        ] ),
    ]),
    # 233
    lambda: t.test(Math_Geometry().spiralOrder, [
        (( [
            [1,2],
            [3,4]
        ] ), [1,2,4,3] ),
        (( [
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ] ), [1,2,3,6,9,8,7,4,5] ),
        (( [
            [1,2,3,4],
            [5,6,7,8],
            [9,10,11,12]
        ] ), [1,2,3,4,8,12,11,10,9,5,6,7] ),
    ]),
    # 234
    lambda: t.test(Math_Geometry().setZeroes, [
        (( [
            [0,1],
            [1,0]
        ] ), [
            [0,0],
            [0,0]
        ] ),
        (( [
            [1,2,3],
            [4,0,5],
            [6,7,8]
        ] ), [
            [1,0,3],
            [0,0,0],
            [6,0,8]            
        ] ),
    ]),
    # 235
    lambda: t.test(Math_Geometry().isHappy, [
        (( 100 ), True ),
        (( 101 ), False ),
    ]),
    # 236
    lambda: t.test(Math_Geometry().plusOne, [
        (( [1,2,3,4] ), [1,2,3,5] ),
        (( [9,9,9] ), [1,0,0,0] ),
    ]),
    # 237
    lambda: t.test(Math_Geometry().romanToInt, [
        (( "III" ), 3 ),
        (( "XLIX" ), 49 ),
    ]),
    # 238
    lambda: t.test(Math_Geometry().myPow, [
        (( 2.0, 5 ), 32.0 ),
        (( 1.1, 10 ), 2.59374 ),
        (( 2.0, -3 ), 0.125 ),
    ]),
    # 239
    lambda: t.test(Math_Geometry().multiply, [
        (( "3", "4" ), "12" ),
        (( "111", "222" ), "24642" ),
    ]),
    # 240
    lambda: t.testcls(Math_Geometry().CountSquares, (  ), [
        ("add", ( [1,1] ), None ),
        ("add", ( [2,2] ), None ),
        ("add", ( [1,2] ), None ),
        ("count", ( [2,1] ), 1 ),
        ("count", ( [3,3] ), 0 ),
        ("add", ( [2,2] ), None ),
        ("count", ( [2,1] ), 2 ),
    ]),

    # ⚙️ BIT MANIPULATION

    # 241
    lambda: t.test(Bit_Manipulation().singleNumber, [
        (( [3,2,3] ), 2 ),
        (( [7,6,6,7,8] ), 8 ),
    ]),
    # 242
    lambda: t.test(Bit_Manipulation().hammingWeight, [
        (( int("00000000000000000000000000010111", 2) ), 4 ),
        (( int("01111111111111111111111111111101", 2) ), 30 ),
    ]),
    # 243
    lambda: t.test(Bit_Manipulation().countBits, [
        (( 4 ), [0,1,1,2,1] ),
    ]),
    # 244
    lambda: t.test(Bit_Manipulation().addBinary, [
        (( "101", "10" ), "111" ),
        (( "10010", "111" ), "11001" ),
    ]),
    # 245
    lambda: t.test(Bit_Manipulation().reverseBits, [
        (( int("00000000000000000000000000010101", 2) ), int("10101000000000000000000000000000", 2) ),
    ]),
    # 246
    lambda: t.test(Bit_Manipulation().missingNumber, [
        (( [1,2,3] ), 0 ),
        (( [0,2] ), 1 ),
    ]),
    # 247
    lambda: t.test(Bit_Manipulation().getSum, [
        (( 1, 1 ), 2 ),
        (( 4, 7 ), 11 ),
    ]),
    # 248
    lambda: t.test(Bit_Manipulation().reverse, [
        (( 1234 ), 4321 ),
        (( -1234 ), -4321 ),
        (( 1234236467 ), 0 ),
    ]),
    # 249
    lambda: t.test(Bit_Manipulation().rangeBitwiseAnd, [
        (( 1, 5 ), 0 ),
        (( 10, 12 ), 8 ),
    ]),
    # 250
    lambda: t.test(Bit_Manipulation().minEnd, [
        (( 3, 2 ), 6 ),
        (( 5, 3 ), 19 ),
    ]),

    # 👹 FINALE

    lambda: t.test(Finale().shortestUniquelyBalancedSubarray, [
        (( [0, 1, 0, 1], 2 ), [0, 2] ),
        (( [0, 1, 1], 2 ), [0, 2] ),
        (( [1, 0, 1], 2 ), [0, 2] ),
        (( [0, 0, 1, 1, 0], 2 ), [1, 3] ),
        (( [0, 1, 0, 0, 1, 0], 2 ), [1, 3] ),
        (( [0, 1, 2, 0, 1, 2], 3 ), [-1, -1] ),
        (( [0, 1, 2, 0, 1, 0, 2], 3 ), [0, 5] ),
        (( [2, 1, 0, 2, 2, 1, 0, 1], 3 ), [0, 5] ),
        (( [0, 1, 2], 3 ), [-1, -1] ),
        (( [0, 1], 3 ), [-1, -1] ),
        (( [0, 1, 2, 3, 0, 1, 2, 0, 3, 1], 4 ), [0, 6] ),
        (( [3, 2, 1, 0, 0, 1, 2, 3], 4 ), [0, 6] ),
        (( [0, 0, 0, 0], 1 ), [0, 0] ),
        (( [], 1 ), [-1, -1] ),
        (( [0, 1, 2, 3], 4 ), [-1, -1] ),
        (( [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0], 5 ), [-1, -1] ),
        (( [0, 1, 2, 3, 4], 5 ), [-1, -1] ),
        (( [0, 1, 0, 2, 0, 3, 0, 4], 5 ), [-1, -1] ),
        (( [0, 1, 2, 3, 4, 4, 3, 2, 1, 0], 5 ), [-1, -1] ),
        (( [1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 0], 5 ), [-1, -1] ),
        (( [0, 1, 0, 2, 1, 2, 0], 3 ), [1, 6] ),
        (( [0, 2, 2, 1, 0, 1, 2, 0, 1], 3 ), [-1, -1] ),
        (( [0, 1, 2, 3, 1, 2, 0, 3, 2, 1, 0], 4 ), [-1, -1] ),
        (( [0, 1, 2, 3, 0, 2, 1, 3], 4 ), [-1, -1] ),
        (( [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 2 ), [-1, -1] ),
        (( [0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 2 ), [0, 2] ),
        (( [0, 1, 2, 0], 3 ), [-1, -1] ),
        (( [0, 1, 2, 2, 0, 0, 1], 3 ), [1, 4] ),
        (( [1], 2 ), [-1, -1] ),
        (( [0]*100000, 1 ), [0, 0] ),
        (( [0]*100000 + [1], 2 ), [99998, 100000] ),
    ], time=2, space=256),

    lambda: t.test(Finale().bestMaskedRotation, [
        (( 'abca', 'caaa', '1111' ), [2, 3] ),
        (( 'aaaa', 'bbbb', '1111' ), [0, 0] ),
        (( 'aaaa', 'aaaa', '1010' ), [0, 2] ),
        (( 'abc', 'abc', '111' ), [0, 3] ),
        (( 'abc', 'bca', '111' ), [2, 3] ),
        (( 'abc', 'bca', '010' ), [2, 1] ),
        (( 'abcd', 'bcda', '1111' ), [3, 4] ),
        (( 'abcd', 'dabc', '1111' ), [1, 4] ),
        (( 'abab', 'baba', '1111' ), [1, 4] ),
        (( 'abab', 'baba', '0011' ), [1, 2] ),
        (( 'a', 'a', '1' ), [0, 1] ),
        (( 'a', 'b', '1' ), [0, 0] ),
        (( '', '', '' ), [0, 0] ),
        (( 'xyz', 'zzz', '111' ), [2, 2] ),
        (( 'xyz', 'zzz', '000' ), [0, 0] ),
        (( 'aaaaab', 'baaaaa', '111111' ), [1, 6] ),
        (( 'aaaaab', 'baaaaa', '000001' ), [1, 1] ),
        (( 'abcabc', 'bcabca', '111111' ), [5, 6] ),
        (( 'abcabc', 'bcabca', '111000' ), [5, 3] ),
        (( 'abcabc', 'bcabca', '000111' ), [5, 3] ),
        (( 'miss', 'sims', '1111' ), [1, 3] ),
        (( 'miss', 'sims', '1100' ), [3, 2] ),
        (( 'miss', 'sims', '0011' ), [3, 1] ),
        (( 'ab', 'ab', '10' ), [0, 1] ),
        (( 'ab', 'ab', '01' ), [0, 1] ),
        (( 'ab', 'ba', '11' ), [1, 2] ),
        (( 'ab', 'ba', '01' ), [1, 1] ),
        (( 'zzzy', 'yzzz', '1111' ), [1, 4] ),
        (( 'zzzy', 'yzzz', '0111' ), [1, 3] ),
        (( "a"*100000, "a"*100000, "1"*100000 ), [0, 100000] ),
        (( "a"*100000, "b"*100000, "1"*100000 ), [0, 0] ),
        (( "ab"*50000, "ba"*50000, "1"*100000 ), [1, 100000] ),
    ], time=2, space=256),

    lambda: t.test(Finale().quotaReverseBlocks, [
        (( None, 3 ), None ),
        (( hl.to([1], None), 1 ), hl.to([1], None) ),
        (( hl.to([2], None), 1 ), hl.to([2], None) ),
        (( hl.to([1, 2, 1], None), 3 ), hl.to([2, 1, 1], None) ),
        (( hl.to([2, 1, 1, 3, 2], None), 3 ), hl.to([1, 2, 1, 3, 2], None) ),
        (( hl.to([3, 3, 3], None), 3 ), hl.to([3, 3, 3], None) ),
        (( hl.to([1, 1, 1, 1], None), 3 ), hl.to([1, 1, 1, 1], None) ),
        (( hl.to([1, 1, 1, 1], None), 4 ), hl.to([1, 1, 1, 1], None) ),
        (( hl.to([4, 1, 2], None), 3 ), hl.to([4, 1, 2], None) ),
        (( hl.to([2, 2, 2, 2], None), 3 ), hl.to([2, 2, 2, 2], None) ),
        (( hl.to([2, 1, 2, 1, 2, 1], None), 3 ), hl.to([1, 2, 1, 2, 1, 2], None) ),
        (( hl.to([1, 2, 3, 1, 1, 1], None), 3 ), hl.to([2, 1, 3, 1, 1, 1], None) ),
        (( hl.to([1, 1, 2, 2, 1, 1], None), 3 ), hl.to([1, 1, 2, 2, 1, 1], None) ),
        (( hl.to([5, 1, 1, 1], None), 3 ), hl.to([5, 1, 1, 1], None) ),
        (( hl.to([1, 5, 1, 1], None), 3 ), hl.to([1, 5, 1, 1], None) ),
        (( hl.to([1, 2, 2, 1], None), 3 ), hl.to([2, 1, 2, 1], None) ),
        (( hl.to([2, 1, 0, 3], None), 3 ), hl.to([1, 2, 0, 3], None) ),
        (( hl.to([0, 0, 0], None), 0 ), hl.to([0, 0, 0], None) ),
        (( hl.to([0, 1, 0, 1, 0], None), 1 ), hl.to([0, 1, 0, 1, 0], None) ),
        (( hl.to([1, 0, 1, 0, 1], None), 1 ), hl.to([1, 0, 1, 0, 1], None) ),
        (( hl.to([2, 1, 2, 0, 1, 1], None), 3 ), hl.to([1, 2, 2, 0, 1, 1], None) ),
        (( hl.to([1, 2, 1, 2, 1, 2], None), 4 ), hl.to([1, 2, 1, 2, 1, 2], None) ),
        (( hl.to([1, 1, 2, 1, 1, 2, 1], None), 3 ), hl.to([1, 1, 2, 1, 1, 2, 1], None) ),
        (( hl.to([2, 1, 1, 2, 1, 1, 2], None), 4 ), hl.to([1, 1, 2, 2, 1, 1, 2], None) ),
        (( hl.to([3, 1, 1, 1, 3], None), 3 ), hl.to([3, 1, 1, 1, 3], None) ),
        (( hl.to([3, 1, 1, 1, 3], None), 4 ), hl.to([3, 1, 1, 1, 3], None) ),
        (( hl.to([1, 1, 1, 2, 2, 1, 1], None), 3 ), hl.to([1, 1, 1, 2, 2, 1, 1], None) ),
        (( hl.to([1, 2, 1, 1, 2, 1, 1, 2], None), 3 ), hl.to([2, 1, 1, 1, 2, 1, 1, 2], None) ),
        (( hl.to([2, 1, 1, 2, 1, 0, 0, 3, 0], None), 3 ), hl.to([1, 2, 2, 1, 1, 0, 0, 0, 3], None) ),
        (( hl.to([1]*100000, None), 3 ), hl.to([1]*100000, None) ),
        (( hl.to([2]*100000, None), 3 ), hl.to([2]*100000, None) ),
    ], time=2, space=256),

    lambda: t.test(Finale().nextHigherUnderCap, [
        (( [], [] ), [] ),
        (( [1], [0] ), [-1] ),
        (( [1, 2], [5, 5] ), [1, -1] ),
        (( [2, 1], [5, 5] ), [-1, -1] ),
        (( [5, 1, 4, 6], [3, 2, 1, 0] ), [3, 2, 3, -1] ),
        (( [5, 1, 4, 6], [0, 0, 0, 0] ), [3, 2, 3, -1] ),
        (( [1, 3, 2, 4], [5, 4, 3, 2] ), [1, 3, 3, -1] ),
        (( [1, 3, 2, 4], [1, 1, 1, 1] ), [1, 3, 3, -1] ),
        (( [4, 3, 2, 1], [3, 2, 1, 0] ), [-1, -1, -1, -1] ),
        (( [1, 2, 3, 4], [0, 0, 0, 0] ), [1, 2, 3, -1] ),
        (( [1, 2, 3, 4], [3, 2, 1, 0] ), [1, 2, 3, -1] ),
        (( [2, 2, 2], [1, 2, 3] ), [-1, -1, -1] ),
        (( [1, 2, 2, 3], [2, 2, 2, 2] ), [1, 3, 3, -1] ),
        (( [3, 1, 2, 4, 0], [5, 1, 4, 2, 3] ), [3, 2, 3, -1, -1] ),
        (( [3, 1, 2, 4, 0], [2, 4, 1, 3, 0] ), [3, 2, -1, -1, -1] ),
        (( [3, 1, 2, 4, 0], [0, 0, 0, 0, 0] ), [3, 2, 3, -1, -1] ),
        (( [10, 1, 9, 2, 8, 3], [5, 4, 3, 2, 1, 0] ), [-1, 2, -1, 4, -1, -1] ),
        (( [10, 1, 9, 2, 8, 3], [1, 2, 3, 4, 5, 6] ), [-1, 2, -1, 4, -1, -1] ),
        (( [1, 5, 2, 6, 3, 7], [3, 1, 3, 1, 3, 1] ), [1, 3, 3, 5, 5, -1] ),
        (( [1, 5, 2, 6, 3, 7], [0, 0, 0, 0, 0, 0] ), [1, 3, 3, 5, 5, -1] ),
        (( [7, 6, 5, 4, 3, 2, 1], [10, 9, 8, 7, 6, 5, 4] ), [-1, -1, -1, -1, -1, -1, -1] ),
        (( [1, 4, 2, 3, 5], [3, 2, 5, 1, 4] ), [1, 4, 3, 4, -1] ),
        (( [2, 5, 1, 4, 3], [3, 1, 4, 2, 5] ), [1, -1, 3, -1, -1] ),
        (( [2, 5, 1, 4, 3], [0, 0, 0, 0, 0] ), [1, -1, 3, -1, -1] ),
        (( [1, 3, 5, 2, 4, 6], [6, 5, 4, 3, 2, 1] ), [1, 2, 5, 4, 5, -1] ),
        (( [1, 3, 5, 2, 4, 6], [1, 2, 3, 4, 5, 6] ), [1, 2, 5, 4, 5, -1] ),
        (( [5, 4, 3, 2, 1, 6], [3, 3, 3, 3, 3, 0] ), [5, 5, 5, 5, 5, -1] ),
        (( [5, 4, 3, 2, 1, 6], [0, 0, 0, 0, 0, 0] ), [5, 5, 5, 5, 5, -1] ),
        (( [2, 1, 3, 1, 2, 4, 1], [4, 3, 2, 1, 0, 5, 6] ), [2, 2, 5, 4, 5, -1, -1] ),
        (( [2, 1, 3, 1, 2, 4, 1], [1, 1, 1, 1, 1, 1, 1] ), [2, 2, 5, 4, 5, -1, -1] ),
        (( [5]*100000, [1]*100000 ), [-1]*100000 ),
        (( list(range(100000)), [0]*100000 ), list(range(1,100000)) + [-1] ),
    ], time=2, space=256),

    lambda: t.test(Finale().minPaletteChange, [
        (( ['a'], (0, 0), (0, 0) ), [0, 0] ),
        (( ['ab', 'aa'], (0, 0), (1, 1) ), [0, 2] ),
        (( ['ab', 'aa'], (0, 1), (1, 0) ), [1, 2] ),
        (( ['aa', 'bb'], (0, 0), (1, 1) ), [1, 2] ),
        (( ['a#', 'aa'], (0, 0), (1, 1) ), [0, 2] ),
        (( ['a#', '##', 'aa'], (0, 0), (2, 1) ), [-1, -1] ),
        (( ['abc'], (0, 0), (0, 2) ), [2, 2] ),
        (( ['aba'], (0, 0), (0, 2) ), [0, 2] ),
        (( ['abba'], (0, 0), (0, 3) ), [1, 3] ),
        (( ['ab', 'ba'], (0, 0), (1, 1) ), [2, 2] ),
        (( ['ab', 'ba'], (0, 0), (0, 1) ), [1, 1] ),
        (( ['ab', 'ba'], (0, 0), (1, 0) ), [1, 1] ),
        (( ['aaa', 'aba', 'aaa'], (0, 0), (2, 2) ), [0, 4] ),
        (( ['aaa', 'bbb', 'aaa'], (0, 0), (2, 2) ), [1, 4] ),
        (( ['aaa', 'b#b', 'aaa'], (0, 0), (2, 2) ), [1, 4] ),
        (( ['a#a', 'aaa', 'a#a'], (1, 0), (1, 2) ), [0, 2] ),
        (( ['a#a', 'aaa', 'a#a'], (0, 0), (2, 2) ), [0, 4] ),
        (( ['a#a', 'a#a', 'aaa'], (0, 0), (2, 2) ), [0, 4] ),
        (( ['ab#c', 'a##c', 'abcc'], (0, 0), (2, 3) ), [1, 5] ),
        (( ['ab#c', 'a##c', 'abcc'], (0, 1), (2, 0) ), [1, 3] ),
        (( ['zz', 'zz'], (0, 0), (1, 1) ), [0, 2] ),
        (( ['az', 'za'], (0, 0), (1, 1) ), [2, 2] ),
        (( ['az', 'za'], (0, 0), (0, 1) ), [1, 1] ),
        (( ['abc', 'def', 'ghi'], (0, 0), (2, 2) ), [4, 4] ),
        (( ['abc', 'a#c', 'abc'], (0, 0), (2, 2) ), [2, 4] ),
        (( ['aaa', '###', 'aaa'], (0, 0), (2, 2) ), [-1, -1] ),
        (( ['ababa'], (0, 0), (0, 4) ), [0, 4] ),
        (( ['aaaaa'], (0, 0), (0, 4) ), [0, 4] ),
        (( ['ababa', 'babab'], (0, 0), (1, 4) ), [5, 5] ),
        (( ["a"*50]*50, (0, 0), (49, 49) ), [0, 98] ),
        (( ["ab"*500], (0, 0), (0, 999) ), [999, 999] ),
    ], time=3, space=256),

    lambda: t.test(Finale().countRemovalsToBalance, [
        (( None ), 0 ),
        (( ht.to([1]) ), 1 ),
        (( ht.to([1, 2, None]) ), 2 ),
        (( ht.to([1, None, 2]) ), 2 ),
        (( ht.to([1, 2, 3]) ), 3 ),
        (( ht.to([1, 2, 3, 4, None, None, None]) ), 3 ),
        (( ht.to([1, 2, 3, 4, 5, 6, 7]) ), 5 ),
        (( ht.to([1, 2, 3, 4, 5, None, 7]) ), 4 ),
        (( ht.to([1, 2, 3, None, 4, None, 5]) ), 3 ),
        (( ht.to([1, 2, None, 3, None, 4, None, 5]) ), 3 ),
        (( ht.to([1, 2, 3, None, None, 4, 5, None, None, None, None, 6, 7]) ), 4 ),
        (( ht.to([1, 2, 3, 4, 5, 6, None, 7, None, None, None, None, None, None, None]) ), 4 ),
        (( ht.to([1, 2, 3, 4, None, None, 5, None, None, 6, None]) ), 4 ),
        (( ht.to([1, 2, 3, 4, None, None, 5, None, None, None, None, None, None, 6]) ), 3 ),
        (( ht.to([10, 5, 15, 3, 7, 12, 18]) ), 5 ),
        (( ht.to([10, 5, 15, 3, 7, 12, 18, None, None, 6, 8]) ), 5 ),
        (( ht.to([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]) ), 9 ),
        (( ht.to([1, 2, 3, 4, 5, 6, 7, 8, None, None, None, None, None, None, None]) ), 5 ),
        (( ht.to([1, 2, 3, None, None, 4, 5]) ), 3 ),
        (( ht.to([1, 2, 3, None, None, None, 4]) ), 3 ),
        (( ht.to([1, 2, 3, 4, 5, None, None, 6]) ), 4 ),
        (( ht.to([1, 2, 3, 4, None, 5, None, 6, None, None, None, 7]) ), 4 ),
        (( ht.to([1, 2, 3, None, 4, 5, None, None, None, 6]) ), 3 ),
        (( ht.to([1, 2, 3, 4, 5, 6, 7, None, None, None, None, None, None, None, 8]) ), 5 ),
        (( ht.to([1, 2, 3, 4, 5, 6, 7, 8, 9]) ), 5 ),
        (( ht.to([1, 2, 3, 4, None, 6, 7, None, None, 12, 13]) ), 4 ),
        (( ht.to(list(range(1,32))) ), 17 ),
        (( ht.to(list(range(1,64))) ), 33 ),
        (( ht.to([1, 2, None, 3, None, None, None, 4, None, None, None, None, None, None, None, 5]) ), 3 ),
        (( ht.to(list(range(1,128))) ), 65 ),
    ], time=4, space=256),

    lambda: t.testcls(Finale().RollerMedian, (  ), [
        ("median", (  ), None ),
        ("add", ( 5 ), None ),
        ("median", (  ), 5 ),
        ("add", ( 2 ), None ),
        ("median", (  ), 2 ),
        ("add", ( 10 ), None ),
        ("median", (  ), 5 ),
        ("add", ( 2 ), None ),
        ("median", (  ), 2 ),
        ("discard", ( 7 ), None ),
        ("median", (  ), 2 ),
        ("discard", ( 2 ), None ),
        ("median", (  ), 5 ),
        ("discard", ( 2 ), None ),
        ("median", (  ), 5 ),
        ("discard", ( 2 ), None ),
        ("median", (  ), 5 ),
        ("add", ( -1 ), None ),
        ("add", ( -1 ), None ),
        ("median", (  ), -1 ),
        ("add", ( 100 ), None ),
        ("median", (  ), 5 ),
        ("discard", ( -1 ), None ),
        ("median", (  ), 5 ),
        ("add", ( 3 ), None ),
        ("add", ( 4 ), None ),
        ("median", (  ), 4 ),
        ("add", ( 4 ), None ),
        ("median", (  ), 4 ),
        ("discard", ( 5 ), None ),
        ("median", (  ), 4 ),
        ("discard", ( 10 ), None ),
        ("median", (  ), 4 ),
        ("discard", ( 100 ), None ),
        ("median", (  ), 4 ),
        ("discard", ( -1 ), None ),
        ("median", (  ), 4 ),
        ("discard", ( 3 ), None ),
        ("discard", ( 4 ), None ),
        ("discard", ( 4 ), None ),
        ("median", (  ), None ),
    ], time=2, space=256),

    lambda: t.testcls(Finale().PrefixOracle, ( ['app', 'apple', 'apply', 'apt', 'bat', 'batch', 'bath', 'banana'], [5, 7, 7, 6, 2, 4, 4, 10] ), [
        ("best", ( 'a' ), 'apple' ),
        ("best", ( 'app' ), 'apple' ),
        ("best", ( 'appl' ), 'apple' ),
        ("best", ( 'b' ), 'banana' ),
        ("best", ( 'ba' ), 'banana' ),
        ("add", ( 'ball', 10 ), None ),
        ("best", ( 'ba' ), 'ball' ),
        ("add", ( 'baton', 10 ), None ),
        ("best", ( 'bat' ), 'baton' ),
        ("remove", ( 'banana' ), None ),
        ("best", ( 'b' ), 'ball' ),
        ("best", ( 'ban' ), '' ),
        ("add", ( 'banana', 10 ), None ),
        ("best", ( 'ban' ), 'banana' ),
        ("add", ( 'banana', 9 ), None ),
        ("best", ( 'ban' ), 'banana' ),
        ("add", ( 'apple', 8 ), None ),
        ("best", ( 'app' ), 'apple' ),
        ("add", ( 'ap', 8 ), None ),
        ("best", ( 'a' ), 'ap' ),
        ("remove", ( 'ap' ), None ),
        ("best", ( 'a' ), 'apple' ),
        ("remove", ( 'apt' ), None ),
        ("best", ( 'a' ), 'apple' ),
        ("add", ( 'az', 100 ), None ),
        ("best", ( 'a' ), 'az' ),
        ("remove", ( 'az' ), None ),
        ("best", ( 'a' ), 'apple' ),
        ("add", ( 'apply', 7 ), None ),
        ("add", ( 'apply', 6 ), None ),
        ("best", ( 'appl' ), 'apple' ),
        ("add", ( 'ape', 8 ), None ),
        ("best", ( 'ap' ), 'ape' ),
        ("remove", ( 'apple' ), None ),
        ("best", ( 'app' ), 'apply' ),
        ("remove", ( 'app' ), None ),
        ("best", ( 'app' ), 'apply' ),
        ("best", ( '' ), 'ball' ),
    ], time=3, space=256),

    lambda: t.test(Finale().firstRainbowComponent, [
        (( 1, [0], 1, [] ), 0 ),
        (( 2, [0, 0], 1, [(0, 1)] ), 0 ),
        (( 2, [0, 1], 2, [] ), -1 ),
        (( 2, [0, 1], 2, [(0, 1)] ), 1 ),
        (( 3, [0, 1, 2], 3, [(0, 1), (1, 2)] ), 2 ),
        (( 3, [0, 1, 2], 3, [(0, 2), (0, 1)] ), 2 ),
        (( 4, [0, 0, 1, 1], 2, [(0, 1), (2, 3)] ), -1 ),
        (( 4, [0, 0, 1, 1], 2, [(0, 2)] ), 1 ),
        (( 5, [0, 1, 0, 1, 0], 2, [(0, 1), (1, 2)] ), 1 ),
        (( 5, [0, 1, 0, 1, 0], 2, [(0, 2), (2, 4)] ), -1 ),
        (( 5, [0, 1, 2, 0, 1], 3, [(0, 1), (1, 2)] ), 2 ),
        (( 5, [0, 1, 2, 0, 1], 3, [(3, 4), (0, 3), (1, 4)] ), 2 ),
        (( 6, [0, 1, 2, 0, 1, 2], 3, [(0, 3), (1, 4), (2, 5)] ), -1 ),
        (( 6, [0, 1, 2, 0, 1, 2], 3, [(0, 1), (2, 3), (4, 5)] ), -1 ),
        (( 6, [0, 1, 2, 0, 1, 2], 3, [(0, 1), (1, 2), (3, 4)] ), 2 ),
        (( 7, [0, 0, 0, 1, 1, 2, 2], 3, [(0, 3), (3, 5)] ), 2 ),
        (( 7, [0, 0, 0, 1, 1, 2, 2], 3, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)] ), 5 ),
        (( 7, [0, 0, 0, 1, 1, 2, 2], 3, [(3, 4), (5, 6)] ), -1 ),
        (( 8, [0, 1, 2, 3, 0, 1, 2, 3], 4, [(0, 1), (1, 2), (2, 3)] ), 3 ),
        (( 8, [0, 1, 2, 3, 0, 1, 2, 3], 4, [(0, 4), (4, 5), (5, 6), (6, 7), (7, 3)] ), 5 ),
        (( 8, [0, 1, 2, 3, 0, 1, 2, 3], 4, [(0, 5), (5, 2), (2, 7)] ), 3 ),
        (( 9, [0, 1, 2, 0, 1, 2, 0, 1, 2], 3, [(0, 1), (1, 2)] ), 2 ),
        (( 9, [0, 1, 2, 0, 1, 2, 0, 1, 2], 3, [(0, 3), (3, 6), (6, 7), (7, 8)] ), -1 ),
        (( 10, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 2, [(0, 2), (2, 4), (4, 6), (6, 8)] ), -1 ),
        (( 10, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 2, [(0, 1)] ), 1 ),
        (( 10, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 2, [] ), -1 ),
        (( 100000, [0,1,2]*33333 + [0], 3, [(0, 1), (1, 2)] ), 2 ),
        (( 100000, [0,1,2]*33333 + [0], 3, [(0, 99999), (1, 99998), (2, 99997)] ), -1 ),
        (( 100000, [0]*99999 + [1], 2, [(i, i+1) for i in range(99999)] ), 99999 ),
        (( 100000, [0]*100000, 2, [(0, 1)] ), -1 ),
    ], time=2, space=256),

    lambda: t.test(Finale().minOddSpectrumPartition, [
        (( '', 0 ), 0 ),
        (( '', 1 ), -1 ),
        (( 'a', 1 ), 1 ),
        (( 'a', 2 ), -1 ),
        (( 'ab', 1 ), 2 ),
        (( 'ab', 2 ), 2 ),
        (( 'ab', 3 ), -1 ),
        (( 'aba', 1 ), 1 ),
        (( 'aba', 2 ), 3 ),
        (( 'aba', 3 ), 3 ),
        (( 'abba', 2 ), 0 ),
        (( 'abba', 3 ), 2 ),
        (( 'abba', 4 ), 4 ),
        (( 'abc', 2 ), 3 ),
        (( 'abc', 3 ), 3 ),
        (( 'aaaa', 2 ), 0 ),
        (( 'aaaa', 3 ), 1 ),
        (( 'aaaa', 4 ), 4 ),
        (( 'abcd', 2 ), 4 ),
        (( 'abcd', 1 ), 4 ),
        (( 'aabb', 2 ), 0 ),
        (( 'aabb', 3 ), 2 ),
        (( 'aabb', 4 ), 4 ),
        (( 'miss', 2 ), 2 ),
        (( 'miss', 3 ), 4 ),
        (( 'miss', 4 ), 4 ),
        (( 'leetcode', 3 ), 4 ),
        (( 'leetcode', 8 ), 8 ),
        (( 'abcabcabc', 3 ), 0 ),
        (( 'abcabcabc', 5 ), 2 ),
        (( "ab"*50, 10 ), 0 ),
        (( "ab"*50, 99 ), 100 ),
        (( "a"*300, 200 ), 100 ),
        (( "a"*100000, 200 ), 0 ),
        (( "a"*99999, 200 ), 1 ),
    ], time=4, space=256)
]

if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: python3 Test.py <test-number>")
        exit(1)

    choice = int(argv[1])

    if not (1 <= choice <= len(TESTS)):
        print(f"Invalid problem number, choose between 1-{len(TESTS)}")
        exit(1)

    TESTS[choice - 1]()
