import math
import random

def main():
	test = read_from_file("data/test.txt")
	training = read_from_file("data/training.txt")
	tree = decision_tree_learning(training, range(len(training[0])-1), [], False)
	print ("==================================")
	print "Expected information gain: "
	run_tests(tree,test)
	print tree.print_Tree()
	print ("==================================")
	print "Random number: "
	tree = decision_tree_learning(training, range(len(training[0])-1), [], True)
	run_tests(tree,test)
	print tree.print_Tree()
	print ("==================================")
	

class node():
	def __init__(self,data):
		self.data = data
		self.children = {}

	def print_Tree(self):
		if len(self.children)==0:
			return "["+str(self.data) + "]"
		else:
			temp = "["+str(self.data)+" "

		for key, test in self.children.items():
			temp +=self.children[key].print_Tree()

		return temp + "]"

def Plurality(examples):
	ones = 0
	twos = 0

	for n in xrange(0, len(examples)):
		if examples[-1]=='1':
			ones+=1
		else:
			twos+=1

	if ones>twos:
		return 1
	elif twos>ones:
		return 2
	else:
		return r.randint(1,2)

def same_classification(examples):
	classification = examples[0][-1]
	for n in xrange(1, len(examples)):
		if examples[n][-1] != classification:
			return False
	return True

#page 704
def B(q):
	if q ==0:
		return q
	else:
		return -( ( q*math.log(q, 2) ) + ( (1.0-q)*math.log((1.0-q), 2) ) )

#section 18.3.4
def importance(data, attributes):
	attribute_entropy = {}
	for attribute in attributes:
		count =0
		for read in data:
			if read[attribute]==data[0][attribute]:
				count+=1
		attribute_entropy[attribute]=B(count/len(data))

	minimum = 1.1
	index = None
	for n in attribute_entropy:
		if attribute_entropy[n] < minimum:
			minimum=attribute_entropy[n]
			index=n
	return index


#page 702
def decision_tree_learning(examples, attributes, parent_examples, random_importance):
	if not examples:
		return node(Plurality(parent_examples))
	elif same_classification(examples):
		return node(examples[0][-1])
	elif not attributes:
		return node(Plurality(examples))
	else:
		if random_importance:
			A = attributes[random.randint(0, len(attributes)-1)]
		else:
			A = importance(examples, attributes)

		tree = node(A)
		attributes.remove(A)

		for n in xrange(1,3):
			read = []
			for e in examples:
				if int(e[A])==n:
					read.append(e)
			sub_tree = decision_tree_learning(read, list(attributes), examples, random_importance)
			tree.children[n] = sub_tree
	return tree

def classify(root, line):
	current = root
	while current.children:
		current=current.children[int(line[current.data])]
	return current.data

def run_tests(tree, data):
	correct_tests = 0
	for line in data:
		if line[-1] == classify(tree, line):
			correct_tests+=1
	print "Correct tests: \t", correct_tests
	print "Total number of tests:\t", len(data)
	
def read_from_file(name):
	read = []
	fil = open(name, 'r')
	for line in fil.readlines():
		read.append(line.rstrip("\n").split("\t"))
	return read

def print_list(l):
	for line in l:
		print line

main()