f = open("data.txt", "r", encoding="utf-8")
data = f.readlines()
f.close()
print(data)
scores = list()
for d in data:
    scores.append(int(d))
print(scores)
print("Max:", max(scores))
print("Min:", min(scores))
print("Average:", round(sum(scores)/len(scores), 2))
