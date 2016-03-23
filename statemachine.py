#!/usr/bin/env python


class StateMachine:

	def __init__(self):
		self.handlers = {}
		self.startState = None
		self.endStates = []
		self.detailList = []
	
	def add_state(self,name,handler,end_state = 0):
		name = name.upper()
		self.handlers[name] = handler
		if end_state:
			self.endStates.append(name)


	def set_start(self,name):
		self.startState = name.upper()

	def process(self,cargo):
		self.detailList = []
		try:
			handler = self.handlers[self.startState]
		except:
			raise InitialzationError("must call .set_start() before .run()")
		if not self.endStates:
			raise InitialzationError("at least one state must be an end_state") 

		while True:
			(newState,cargo,returnList) = handler(cargo,self.detailList)

			if newState.upper() in self.endStates:
				# print("reached ",newState,",".join([x[0] + "|" + x[1].encode("utf8") for x in returnList]))
				for x,y in returnList:
					print x,y
				
				break
			else:
				handler = self.handlers[newState.upper()]
