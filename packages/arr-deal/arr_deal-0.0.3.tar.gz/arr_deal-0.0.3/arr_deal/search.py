class searching:
    def lin_search(self, arr, num):
        for i in range(len(arr)):
            if arr[i] == num:
                return i

        return -1
