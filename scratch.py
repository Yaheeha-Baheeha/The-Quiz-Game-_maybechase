import random
for i in range(0,400):
    score = random.gauss(19.5, 5)
    score = max(3, min(25, score))
    score = int(score)
    print(score)