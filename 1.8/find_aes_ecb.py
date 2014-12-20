lines = [line.strip().decode('base64') for line in open('8.txt')]

# Return the number of matched substrings between blockA & blockB with a given pattern size
def numPatterns(blockA, blockB, patternSize):
	matches = 0
	for i in range(0, 16 - patternSize):
		pattern = blockA[i:patternSize]
		matches += blockB.count(pattern)
	return matches

# Return the number of patterns between these two blocks
def scoreBlocks(blockA, blockB):
	score = 0
	for patternSize in range(1, 16):
		score += numPatterns(blockA, blockB, patternSize)
	return score

# Score a line by checking for any repetitions between blocks (of 16 bytes) in the line
def scoreLine(line):
	blocks = [line[i:i+16] for i in range(0, len(line), 16)]
	score = 0
	for i in range(1, len(blocks)):
		for j in range(0, i):
			score += scoreBlocks(blocks[i], blocks[j])
	return score


bestScore = 0
bestLine = ''
for line in lines:
	score = scoreLine(line)
	if score > bestScore:
		bestScore = score
		bestLine = line
	
print bestLine
print "Scored: " + str(bestScore)
