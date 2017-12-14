
MAX_CRASH_COUNT = 250

class Car(object):
	"""docstring for Car"""
	def __init__(self):
		self.flag = 0
		self.crashed = False
		self.move = None

	def update_car(self, error, message, move):
		self.move = move
		if error:
			self.flag += 1
			print(__name__, message)
		if self.flag == MAX_CRASH_COUNT:
			print("End Run, Limit {} Reached".format(MAX_CRASH_COUNT))
			self.crashed = True

