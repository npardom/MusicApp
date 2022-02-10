class BinaryTree:
	def __init__(self):
		self.size = 0

	class Node:
		def __init__(self, id,data = None):
			self.left = None
			self.right = None
			self.id = id
			self.data = data

	#Inserta en forma de BST y retorna la raiz del arbol, en forma iterativa
	def insert(self, root, id, data):
		curr = root
		parent = None
		#Si el arbol es vacio, inserta un nodo
		if root is None:
			return BinaryTree.Node(id, data)	
		#Recorre el arbol en busca del padre del nodo a insertar
		while curr:
			parent = curr
			if id < curr.id:
				curr = curr.left
			else:
				curr = curr.right
		#Lo asigna como hijo izquierdo o derecho del padre 
		if id < parent.id:
			parent.left = BinaryTree.Node(id, data)
		else:
			parent.right = BinaryTree.Node(id, data)
		return root

	#Elimina un nodo
	def delete(self, root, id):
		if not root:
			return root
		elif id < root.id:
			root.left = self.delete(root.left, id)
		elif id > root.id:
			root.right = self.delete(root.right, id)
		else:
			if root.left is None:
				self.size -= 1
				temp = root.right
				root = None
				return temp
			elif root.right is None:
				self.size -= 1
				temp = root.left
				root = None
				return temp
			temp = self.getMinValueNode(root.right)
			root.id = temp.id
			root.right = self.delete(root.right, temp.id)
		if root is None:
			return root	
		return root

	#Va al nodo más a la izquierda del arbol
	def getMinValueNode(self, root):
		#Si el nodo es nulo o no tiene mas hojas izquierdas, retorna el nodo
		if root is None or root.left is None:
			return root
		#Mientras no llegue al ultimo nodo, sigue la función recursiva
		return self.getMinValueNode(root.left)

	#Mientras no llega al nodo, va bajando en el arbol	
	def find(self,root,id):
		if root.id != id:
			while id != root.id:
				if id < root.id:
					root = root.left
				else:
					root = root.right
		return root

	#Inorder iterativo usando un stack
	def inOrder(self, node):
		current = node
		array = []
		stack = []
		while True:
			if current is not None:
				stack.append(current)
				current = current.left
			elif(stack):
				current = stack.pop()
				array.append(current)
				current = current.right
			else:
				break
		return array

	#Retorna el tamaño del arbol
	def getSize(self):
		return self.size