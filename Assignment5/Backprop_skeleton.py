import math
import random
import copy

#The transfer function of neurons, g(x)
def logFunc(x):
    return (1.0/(1.0+math.exp(-x)))

#The derivative of the transfer function, g'(x)
def logFuncDerivative(x):
    return math.exp(-x)/(pow(math.exp(-x)+1,2))

def randomFloat(low,high):
    return random.random()*(high-low) + low

#Initializes a matrix of all zeros
def makeMatrix(I, J):
    m = []
    for i in range(I):
        m.append([0]*J)
    return m

class NN: #Neural Network
    def __init__(self, numInputs, numHidden, learningRate=0.001):
        #Inputs: number of input and hidden nodes. Assuming a single output node.
        # +1 for bias node: A node with a constant input of 1. Used to shift the transfer function.
        self.numInputs = numInputs + 1
        self.numHidden = numHidden

        # Current activation levels for nodes (in other words, the nodes' output value)
        self.inputActivation = [1.0]*self.numInputs
        self.hiddenActivations = [1.0]*self.numHidden
        self.outputActivation = 1.0 #Assuming a single output.
        self.learningRate = learningRate

        # create weights
        #A matrix with all weights from input layer to hidden layer
        self.weightsInput = makeMatrix(self.numInputs,self.numHidden)
        #A list with all weights from hidden layer to the single output neuron.
        self.weightsOutput = [0 for i in range(self.numHidden)]# Assuming single output
        # set them to random vaules
        for i in range(self.numInputs):
            for j in range(self.numHidden):
                self.weightsInput[i][j] = randomFloat(-0.5, 0.5)
        for j in range(self.numHidden):
            self.weightsOutput[j] = randomFloat(-0.5, 0.5)

        #Data for the backpropagation step in RankNets.
        #For storing the previous activation levels (output levels) of all neurons
        self.prevInputActivations = []
        self.prevHiddenActivations = []
        self.prevOutputActivation = 0
        #For storing the previous delta in the output and hidden layer
        self.prevDeltaOutput = 0
        self.prevDeltaHidden = [0 for i in range(self.numHidden)]
        #For storing the current delta in the same layers
        self.deltaOutput = 0
        self.deltaHidden = [0 for i in range(self.numHidden)]

    def propagate(self, inputs):
        if len(inputs) != self.numInputs-1:
            raise ValueError('wrong number of inputs')

        # input activations
        self.prevInputActivations=copy.deepcopy(self.inputActivation)
        for i in range(self.numInputs-1):
            self.inputActivation[i] = inputs[i]
        self.inputActivation[-1] = 1 #Set bias node to -1.

        # hidden activations
        self.prevHiddenActivations=copy.deepcopy(self.hiddenActivations)
        for j in range(self.numHidden):
            sum = 0.0
            for i in range(self.numInputs):
                #print self.ai[i] ," * " , self.wi[i][j]
                sum = sum + self.inputActivation[i] * self.weightsInput[i][j]
            self.hiddenActivations[j] = logFunc(sum)

        # output activations
        self.prevOutputActivation=self.outputActivation
        sum = 0.0
        for j in range(self.numHidden):
            sum = sum + self.hiddenActivations[j] * self.weightsOutput[j]
        self.outputActivation = logFunc(sum)
        return self.outputActivation

    def computeOutputDelta(self):
        #TODO: Implement the delta function for the output layer (see exercise text)
        deltaCalculation = (self.prevOutputActivation - self.outputActivation)
        probability = logFunc(deltaCalculation)
        self.prevDeltaOutput = logFuncDerivative(self.prevOutputActivation) * (1 - probability)
        self.deltaOutput = logFuncDerivative(self.outputActivation) * (1 - probability)
        pass


    def computeHiddenDelta(self):
        #TODO: Implement the delta function for the hidden layer (see exercise text)
        for h in range(self.numHidden):
            self.prevDeltaHidden[h] = logFuncDerivative(self.prevHiddenActivations[h])*self.weightsOutput[h]*(self.prevDeltaOutput - self.deltaOutput)
            self.deltaHidden[h] = logFuncDerivative(self.hiddenActivations[h])*self.weightsOutput[h]*(self.prevDeltaOutput - self.deltaOutput)
        pass


    def updateWeights(self):
        #TODO: Update the weights of the network using the deltas (see exercise text)
        for i in range(0,self.numInputs):
            for j in range(0,self.numHidden):
                self.weightsInput[i][j] = self.weightsInput[i][j] + self.learningRate*(self.prevDeltaHidden[j] * self.prevHiddenActivations[j] - self.deltaHidden[j] * self.hiddenActivations[j])

        for i in range(len(self.weightsOutput)):
            self.weightsOutput[i] += self.learningRate*(self.prevDeltaOutput*self.prevHiddenActivations[i] - self.deltaOutput*self.hiddenActivations[i])
        pass

    def backpropagate(self):
        self.computeOutputDelta()
        self.computeHiddenDelta()
        self.updateWeights()

    #Prints the network weights
    def weights(self):
        print('Input weights:')
        for i in range(self.numInputs):
            print(self.weightsInput[i])
        print()
        print('Output weights:')
        print(self.weightsOutput)

    def train(self, patterns, iterations=1):
        #TODO: Train the network on all patterns for a number of iterations.
        #TODO: Training is done  like this (details in exercise text):
        for pair in patterns:
            #-Propagate A
            self.propagate(pair[0].features)
            #-Propagate B
            self.propagate(pair[1].features)
            #-Backpropagate
            self.backpropagate()

    def countMisorderedPairs(self, patterns):
        #TODO: Let the network classify all pairs of patterns. The highest output determines the winner.
        #for each pair, do
        #Propagate A
        #Propagate B
        #if A>B: A wins. If B>A: B wins
        #if rating(winner) > rating(loser): numRight++
        #else: numMisses++
        #end of for
        #TODO: Calculate the ratio of correct answers:
        #errorRate = numMisses/(numRight+numMisses)
        self.numRight = 0
        self.numMisses = 0
        for pair in patterns:
            A = self.propagate(pair[0].features)
            B = self.propagate(pair[1].features)
            if(A > B):
                won = pair[0]
                lost = pair[1]
            elif(B > A):
                won = pair[1]
                lost = pair[0]
            if(won.rating > lost.rating):
                self.numRight+=1
            else:
                self.numMisses+=1
        self.errorRate = (float(self.numMisses) / float(self.numRight + self.numMisses))
        print(self.errorRate)
        return self.errorRate