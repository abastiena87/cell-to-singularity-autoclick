start = 115_870_000
step = 70
total = 0

for i in range(step):
    start *= 1.15
    total += start

print(total)

# 61801728004830
# 15754402083559