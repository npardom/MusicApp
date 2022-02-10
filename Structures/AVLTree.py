class AVLTree:
	def __init__(self):
		self.size = 0

	class Node:
		def __init__(self, id,data = None):
			self.left = None
			self.right = None
			self.id = id
			self.data = data
			self.height = 1

	def insert(self, root, id, data):
		#Inserta en forma de BST y retorna la raiz del arbol, usando recursion
		if root is None:
			self.size += 1
			return AVLTree.Node(id, data)
		elif id < root.id:
			root.left = self.insert(root.left, id, data)
		else:
			root.right = self.insert(root.right, id, data)
		
		#Actualiza la altura del nodo
		root.height = 1 + max(self.getHeight(root.left),self.getHeight(root.right))

		# Actualiza el balance del arbol
		balance = self.getBalance(root)

		#Si el balance es mayor a 1 (height(left) > 1 + height(right)), balanceamos
		if balance > 1:
			if id < root.left.id:
				#Se realiza rotacion R
				return self.rightRotate(root)
			else:
				#Realiza doble rotacion LR
				root.left = self.leftRotate(root.left)
				return self.rightRotate(root)
		
		#Si el balance es menor a -1 (height(right) > 1 + height(left)), balanceamos
		if balance < -1:
			if id > root.right.id:
				#Realiza rotacion L
				return self.leftRotate(root)
			else:
				#Realiza doble rotacion RL
				root.right = self.rightRotate(root.right)
				return self.leftRotate(root)
		
		#Retorna el nodo raiz
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
			root.right = self.delete(root.right,temp.id)
		if root is None:
			return root
			
		# Actualiza el balance y la altura del nodo
		root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
		balanceFactor = self.getBalance(root)

		# Balancea el arbol
		if balanceFactor > 1:
			if self.getBalance(root.left) >= 0:
				return self.rightRotate(root)
			else:
				root.left = self.leftRotate(root.left)
				return self.rightRotate(root)
		if balanceFactor < -1:
			if self.getBalance(root.right) <= 0:
				return self.leftRotate(root)
			else:
				root.right = self.rightRotate(root.right)
				return self.leftRotate(root)
		return root

	# Rotacion izquierda
	def leftRotate(self, X):
		#Toma un nodo X con un hijo derecho Y y convierte a X en el hijo izquierdo de Y)
		Y = X.right
		temp = Y.left
		Y.left = X
		X.right = temp
		#Actualiza las alturas de los nodos 
		X.height = 1 + max(self.getHeight(X.left),self.getHeight(X.right))
		Y.height = 1 + max(self.getHeight(Y.left),self.getHeight(Y.right))
		#Retorna el nuevo nodo raiz
		return Y

	# Rotacion Derecha
	def rightRotate(self, X):
		#Toma un nodo X con un hijo izquierdo Y y convierte a X en el hijo derechio de Y)
		Y = X.left
		temp = Y.right
		Y.right = X
		X.left = temp
		#Actualiza las alturas de los nodos 
		X.height = 1 + max(self.getHeight(X.left),self.getHeight(X.right))
		Y.height = 1 + max(self.getHeight(Y.left),self.getHeight(Y.right))
		#Retorna el nuevo nodo raiz
		return Y

	#Obtiene la altura de un arbol, dado un nodo raiz
	def getHeight(self, root):
		#Si el arbol es vacio, la altura es 0
		if root is None:
			return 0
		#Si no, retorna la altura del arbol
		return root.height

	#Obtiene el balance actual del arbol, dado un nodo raiz
	def getBalance(self, root):
		#Si el arbol es vacio, el balance es 0
		if root is None:
			return 0
		#Si el nodo no es vacio, retorna la diferencia de altura entre los nodos hijos
		return self.getHeight(root.left) - self.getHeight(root.right)

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