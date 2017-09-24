output = open("tts_list.txt", "w")

with open("weiner2015_tts.tsv", "r") as f:
    lines = f.readlines()
i = 0

for line in lines:
    data = line.split("\t")
    if data[3] != "NaN":
        # output.write(data[4])
        i += 1

print(i, len(lines))
output.close()
f.close()