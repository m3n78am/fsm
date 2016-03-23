#!/usr/bin/env python
# -*- coding: utf8 -*-

from statemachine import StateMachine


def getIndex(doc,substr):
	try:
		index = doc.index(substr)
	except ValueError:
		return -1
	return index


def start_transitions(doc,detailList=[]):
	#detailList = []	
	breakIndex = -1

	newState = "error_state"

	for i,char in enumerate(doc.decode("utf8")):
		char = char.encode("utf8")
		# find it
		if char in ("省","市"):
			breakIndex = i
			if char == "省":
				newState = "province_state"
			else:
				newState = "city_state"
			break

	if breakIndex <> -1:
		restStr = doc.decode("utf8")[breakIndex+1:]
		detailList.append((newState,doc.decode("utf8")[:breakIndex+1]))

	return (newState,restStr,detailList)

def province_transitions(doc,detailList):
	breakIndex = -1
	newState = "error_state"

	for i,char in enumerate(doc):
		char = char.encode("utf8")
		if char in ("市","县","区"):
			breakIndex = i
			if char == "市":
				newState = "city_state"
			else:
				newState = "region_state"
			break

	if breakIndex <> -1:
		restStr = doc[breakIndex+1:]
		detailList.append((newState,doc[:breakIndex + 1]))

	return (newState,restStr,detailList)

def city_transitions(doc,detailList):
	breakIndex = -1
	newState = "error_state"

	for i,char in enumerate(doc):
		char = char.encode("utf8")
		if char in ("路","街","区"):
			breakIndex = i
			if char == "区":
				newState = "region_state"
			else:
				newState = "street_state"
			break

	if breakIndex <> -1:
		restStr = doc[breakIndex+1:]
		detailList.append((newState,doc[:breakIndex + 1]))

	return (newState,restStr,detailList)


def region_transitions(doc,detailList):
	breakIndex = -1
	newState = "error_state"

	for i,char in enumerate(doc):
		char = char.encode("utf8")
		if char in ("路","街","区"):
			breakIndex = i
			if char in ("路","街"):
				newState = "street_state"
			else:
				newState = "region_state"
			break

	if breakIndex <> -1:
		restStr= doc[breakIndex+1:]
		detailList.append((newState,doc[:breakIndex + 1]))

	return (newState,restStr,detailList)

def street_transitions(doc,detailList):
	breakIndex = -1
	newState = "street_state"

	for i,char in enumerate(doc):
		char = char.encode("utf8")
		if char == "号":
			breakIndex = i
			newState = "doorplate_state"
			break

	if breakIndex <> -1:
		restStr = doc[breakIndex+1:]
		detailList.append((newState,doc[:breakIndex + 1]))

	return (newState,restStr,detailList)



if __name__ == "__main__":
	m = StateMachine()
	m.add_state("start_state",start_transitions)
	m.add_state("province_state",province_transitions)
	m.add_state("city_state",city_transitions)
	m.add_state("region_state",region_transitions)
	m.add_state("street_state",street_transitions,end_state = 1)
	m.add_state("doorplate_state",None,end_state = 1)

	m.set_start("start_state")

	#m.process("浙江杭州市西湖区城区文三路黄龙国际G座18层")
	m.process("浙江省杭州市西湖区城区文三路黄龙国际G座18层")

	m.process("北京市北三环东路8号静安中心大厦")
