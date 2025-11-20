file = open("mbox.txt")

senders = dict()

run = True
while run:
    line = file.readline()
    if len(line) == 0:
        run = False
        continue

    if not line.startswith("From "):
        continue

    lineSplit = line.split()
    if len(lineSplit) < 2 or "@" not in lineSplit[1]:
        continue

    sender = lineSplit[1].lower()

    if sender not in senders:
        senders[sender] = 0
    senders[sender] += 1

maxCount = 0
maxCountSender = ""
for sender, count in senders.items():
    if count > maxCount:
        maxCount = count
        maxCountSender = sender

print(maxCountSender, maxCount)
