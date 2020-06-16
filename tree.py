class Node:
    def __init__(self, key, value = None):
        self.__key = key
        self.__value = value
        self.__leftChild = None
        self.__rightChild = None

    def getRightChild(self):
        return self.__rightChild

    def getLeftChild(self):
        return self.__leftChild

    def setRightChild(self, theNode):
        self.__rightChild = theNode

    def setLeftChild(self, theNode):
        self.__leftChild = theNode

    def getValue(self):
        return self.__value

    def setValue(self, value):
        self.__value = value

    def getKey(self):
        return self.__key

    def isLeaf(self):
        return self.getLeftChild() == None and self.getRightChild == None

class BinarySearchTree():
    def __init__(self):
        self.__root = None
        self.__size = 0

    def getSize(self):
        return self.__size

    def isEmpty(self):
        return self.__size == 0

    def get(self, key):
        currentNode = self.__root
        while currentNode != None:
            if currentNode.getKey() == key:
                return currentNode.getValue()
            elif currentNode.getKey() > key:
                currentNode = currentNode.getLeftChild()
            else:
                currentNode = currentNode.getRightChild()
        return None

    def __getitem__(self,key):
        return self.get(key)

    def put(self, key, value):
        if self.isEmpty():
            self.__root = Node(key,value)
            self.__size = 1
            return
        currentNode = self.__root
        while currentNode != None:
            if currentNode.getKey() == key:
                currentNode.setValue(value)
                return
            elif currentNode.getKey() > key:
                if currentNode.getLeftChild() == None:
                    newNode = Node(key,value)
                    currentNode.setLeftChild(newNode)
                    break
                else:
                    currentNode = currentNode.getLeftChild()
            else:
                if currentNode.getRightChild() == None:
                    newNode = Node(key, value)
                    currentNode.setRightChild(newNode)
                    break
                else:
                    currentNode = currentNode.getRightChild()
        self.__size += 1

    def __setitem__(self, key, data):
        self.put(key, data)

    #InOrder (Sorted if BST)
    def inOrderTraversal(self,func):
        self.__inOrderTraversalRec(self.__root, func)

    def __inOrderTraversalRec(self, theNode, func):
        if theNode != None:
            self.__inOrderTraversalRec(theNode.getLeftChild(), func)
            func(theNode.getKey(), theNode.getValue())
            self.__inOrderTraversalRec(theNode.getRightChild(), func)

    def printTree(self):
        self.inOrderTraversal(self.printNode)
        
    def printNode(self, key, value):
        print(key, value)
        print("")

    def getAndRemoveRightSmall(self, foundNode):
        return
    #remove function has yet to be compelted
    def remove(self, key):
        if self.__root == None:
            return None
        if self.__root.getKey() == key:
            self.__size -= 1
            if self.__root.getLeftChild() == None:
                self.__root = self.__root.getRightChild()
            elif self.__root.getRightChild() == None:
                self.root = self.__root.getLeftChild()
            else:
                replaceNode = self.__getAndRemoveRightSmall(self.__root)
                self.__root.setkey(replaceNode.getKey())
                self.__root.setValue(replaceNode.getValue())
        else:
            currentNode = self.__root
            while currentNode != None:
                if currentNode.getLeftChild() and currentNode.getLeftChild().getKey() == key:
                    foundNode = currentNode.getLeftChild()
                    if foundNode.isLeaf():
                        currentNode.setLeftChild(None)
                    elif foundNode.getLeftChild() == None:
                        currentNode.setLeftChild(foundNode.getRightChild())
                    elif foundNode.getRightChild() == None:
                        currentNode.setLeftChild(foundNode.getLeftChild())
                    else:
                        replaceNode = self.getAndRemoveRightSmall(foundNode)
                        foundNode.setKey(replaceNode.getKey())
                        foundNode.setValue(replaceNode.getValue())
                    break
                ####elif currentNode.getRightChild() and currentNode.getRightChild().getKey() == key:
                      #  foundNode = currentNode.getRightChild()
                     #   if foundNode.isLeaf():
                    #        currentNode.setRightChild(None)
                   #     elif foundNode.getLeftChild() == None:
                  #          currentNode.setRightChild(foundNode,getRightChild())
                 #       elif foundNode.getRightChild == None:
                #            currentNode.setRightChild(foundNode.getLeftChild())
               #         else:
              #              replaceNode = self.__getAndRemoveRightSmall(foundNode)
             #               foundNode.setKey(replaceNode.getKey())
            #                foundNode.setValue(replaceNode.getValue())
           #                 break
          #              elif currentNode.getKey() > key:
         #                   currentNode = currentNode.getLeftChild()
        #                else:
       #                     currentNode = currentNode.getRightChild()
      #              if currentNode != None:
     #                   self.__size -= 1

