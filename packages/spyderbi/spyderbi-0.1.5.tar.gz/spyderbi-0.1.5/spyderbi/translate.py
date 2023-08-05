class translate:


    def dec(self,x):
        __table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        tr = {}
        for i in range(58):
            tr[__table[i]] = i
        s = [11, 10, 3, 8, 4, 6]
        xor = 177451812
        add = 8728348608
        r = 0
        for i in range(6):
            r += tr[x[s[i]]]*58**i
        return str((r-add) ^ xor)

    def enc(self,x):
        __table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        tr = {}
        for i in range(58):
            tr[__table[i]] = i
        s = [11, 10, 3, 8, 4, 6]
        xor = 177451812
        add = 8728348608
        r = 0
        x= int(x)
        x = (x ^ xor)+add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]] = __table[x//58**i % 58]
        return ''.join(r)





