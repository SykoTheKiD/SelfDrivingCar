
MAX_CRASH_COUNT = 250

class Car(object):
	"""docstring for Car"""
	def __init__(self):
		self.flag = 0
		self.crashed = False

	def update_car(self, error, message):
		if error:
			self.flag += 1
			print(message)
		if self.flag == MAX_CRASH_COUNT:
			print("End Run, Limit {} Reached".format(MAX_CRASH_COUNT))
			self.crashed = True

