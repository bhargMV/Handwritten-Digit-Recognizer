import sys
import math

#count is used to compute p[y]. Here y is a label.
count = {}

#condProb is used to compute conditional probability p(x|y). Here x is pixel and y is the label.
condProb = {}

total_labels = 0

hits = {}

testCount = {}

def initializeGlobals():
    global count
    for i in range(0, 10):
        count[i] = 0

    global hits
    for i in range(0, 10):
        hits[i] = 0

    global testCount
    for i in range(0, 10):
        testCount[i] = 0

    global condProb
    for i in range(0, 10):
        condProb[i] = []

    for i in range(0, 10):
        for j in range(0, 28):
            condProb[i].append([])

    for i in range(0,10):
        for j in range(0, 28):
            for k in range(0, 28):
                condProb[i][j].append([0, 0, 0])


def parseFileTrainingData(images, labels):

    fimg = open(images)
    flab = open(labels)

    global count, total_labels
    for entry in flab:
        Y = (entry.split('\n'))[0]
        y = int(Y)

        count[y] = count[y] + 1
        total_labels = total_labels + 1
        #print y

        line = ''
        tempLabel = []
        minLeft = 27

        for z in range(0, 28):
            line = fimg.readline()
            line = (line.split('\n'))[0]

            if not line.strip():
                line = 28 * ' '
            tempLabel.append(line)

        #print(len(tempLabel))

        for i in range(0, len(tempLabel)):
            tempLine = tempLabel[i]

            for j in range(0, 28):
                if(tempLine[j] != ' '):
                    break

            if minLeft > j:
                minLeft = j

        #print("MinLeft :", minLeft)

        global condProb
        mat =  condProb[y]

        for i in range(0, len(tempLabel)):
            tempLine = (tempLabel[i])

            #for j in range(0, len(tempLine)):
            for j in range(0, 28):
                if tempLine[j] == ' ':
                    mat[i][j][0] = mat[i][j][0] + 1

                elif tempLine[j] == '+':
                    mat[i][j][1] = mat[i][j][1] + 1

                elif tempLine[j] == '#':
                    mat[i][j][2] = mat[i][j][2] + 1

            #for j in range(len(tempLine), 28):
               # mat[i][j][0] = mat[i][j][0] + 1


        #print(condProb[y][0])

        condProb[y] = mat

    #print count
    #print(condProb[1][0])

def computeAccuracy(images, labels):

    fimg = open(images)
    flab = open(labels)
    fout = open("out.txt", 'w')
    success = 0
    fail = 0

    global count, total_labels, hits, testCount
    for entry in flab:
        Y = (entry.split('\n'))[0]
        y = int(Y)
        testCount[y] = testCount[y] + 1
        #print y

        line = ''
        tempLabel = []
        minLeft = 27
        exp_val = y
        max_prob = 0

        for z in range(0, 28):
            line = fimg.readline()
            line = (line.split('\n'))[0]

            if not line.strip():
                line = 28 * ' '
            tempLabel.append(line)

        #print(len(tempLabel))

        for i in range(0, len(tempLabel)):
            tempLine = tempLabel[i]

            for j in range(0, 28):
                if(tempLine[j] != ' '):
                    break

            if minLeft > j:
                minLeft = j

        #print("MinLeft :", minLeft)
        #for i in range(0, len(tempLabel)):
            #fout.write(str(tempLabel[i]) + "\n")
        #fout.write("\n\n")

        global condProb

        for k in range(0, 10):

            mat =  condProb[k]
            temp_prob = count[k]/float(total_labels)

            for i in range(0, len(tempLabel)):
                tempLine = (tempLabel[i])

                #for j in range(0, len(tempLine)):
                for j in range(0, 28):
                    if tempLine[j] == ' ':
                        #if mat[i][j][0] != 0:
                            #print mat[i][j][0]/float(mat[i][j][0] + mat[i][j][1] + mat[i][j][2])
                        temp_prob = temp_prob * (mat[i][j][0]+1)/float(mat[i][j][0] + mat[i][j][1] + mat[i][j][2] + 3)


                    elif tempLine[j] == '+':
                        #if mat[i][j][1] != 0:
                         temp_prob = temp_prob * ((mat[i][j][1]+1)/float(mat[i][j][0] + mat[i][j][1] + mat[i][j][2] + 3))

                    elif tempLine[j] == '#':
                        #if mat[i][j][2] != 0:
                        temp_prob = temp_prob * ((mat[i][j][2] + 1)/float(mat[i][j][0] + mat[i][j][1] + mat[i][j][2] + 3))

                #for j in range(len(tempLine), 28):
                    #temp_prob = temp_prob * (mat[i][j][0]/float(mat[i][j][0] + mat[i][j][1] + mat[i][j][2]))

            if temp_prob > max_prob:
                max_prob = temp_prob
                exp_val = k


        if exp_val == y:
            success = success + 1
            hits[y] = hits[y] + 1
            #print exp_val

        else:
            fail = fail + 1

        #print y, exp_val
        fout.write(str(y) + " " + str(exp_val) + " \n")

    for i in range(0,10):
        print "Hits ", i,"  ", hits[i], " ", " out of ", testCount[i], "Accuracy: ", hits[i]/float(testCount[i])

    print "\nOverall Hits: ",success , " Mismatch: ", fail, " Test Data Size: ", success + fail

    print "\nAccuracy : ", success/float(success + fail), "\n"

if __name__ == '__main__':

    if len(sys.argv) < 5:
        print 'Input training images file, training labels file, test images file, test labels in order'
        exit(-1)

    trainingImages = sys.argv[1]
    trainingLabels = sys.argv[2]
    testImages = sys.argv[3]
    testLabels = sys.argv[4]

    initializeGlobals()
    #print condProb[0]

    parseFileTrainingData(trainingImages, trainingLabels)

    computeAccuracy(testImages, testLabels)