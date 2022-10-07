s = "bbbbb"
t = ""
le = 0


for j in range(len(s)):
    if s[j] in t:
        le = max(le,len(t))
        i = t.index(s[j])
        t = t[i+1:]

    t+=s[j]

print(le)