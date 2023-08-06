class sorting:
    def bubble_sort_ascend(self, arr):
        temp = 0
        for i in range(len(arr)-1):

            for j in range(len(arr)-i-1):
                if arr[j] > arr[j + 1]:
                    temp = arr[j]
                    arr[j] = arr[j + 1]
                    arr[j + 1] = temp
        return arr
    def bubble_sort_descend(self, arr):
        temp = 0
        for i in range(len(arr)-1):
            for j in range(len(arr)-i-1):
                if arr[j] < arr[j + 1]:
                    temp = arr[j]
                    arr[j] = arr[j + 1]
                    arr[j + 1] = temp
        return arr
