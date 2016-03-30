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
		if char in ("省","市","区"):
			breakIndex = i
			if char in ("省","区"): # 新疆维吾尔自治区昌吉回族自治州昌吉市昌吉市建国西路甜蜜家园9-1-301
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
		if char in ("市","县","区","州"):
			breakIndex = i
			if char == "市":
				newState = "city_state"
				break
			elif char == "州" and i >= 2:
			#elif char == "州" and detailList[-1][-1][-1].encode("utf8") == "区":
				newState = "state_state"
				break
			elif char in ("县","区"): # 县|区
				newState = "region_state"
				break

	if breakIndex <> -1:
		restStr = doc[breakIndex+1:]
		detailList.append((newState,doc[:breakIndex + 1]))

	return (newState,restStr,detailList)

def state_transitions(doc,detailList):
	breakIndex = -1
	newState = "error_state"

	for i,char in enumerate(doc):
		char = char.encode("utf8")
		if char in ("市"):
			breakIndex = i
			newState = "city_state"
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
		if char in ("路","街","区","县","市"):
			breakIndex = i
			if char in ("区","县"):
				newState = "region_state"
			elif char == "市":
				newState = "city_state"
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
		if char in ("路","街","区","镇","村"):
			breakIndex = i
			if char in ("路","街"):
				newState = "street_state"
			elif char in ("镇","村"):
				newState = "town_state"
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

def town_transitions(doc,detailList):
	breakIndex = -1
	newState = "error_state"

	for i,char in enumerate(doc):
		char = char.encode("utf8")
		if char in ("路","街","村"):
			breakIndex = i
			if char in ("路","街"):
				newState = "street_state"
			else:
				newState = "town_state"
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
	m.add_state("state_state",state_transitions)
	m.add_state("town_state",town_transitions,end_state=1)
	m.add_state("street_state",street_transitions,end_state = 1)
	m.add_state("doorplate_state",None,end_state = 1)

	m.set_start("start_state")

	#m.process("浙江杭州市西湖区城区文三路黄龙国际G座18层")
	#m.process("浙江省杭州市西湖区城区文三路黄龙国际G座18层")
	#m.process("北京市北三环东路8号静安中心大厦")
	#m.process("黑龙江省哈尔滨市呼兰区南京路美兰家园5栋2单元303")
	#m.process("广东省深圳市罗湖区金稻田路1228号理想新城9栋A单元301室")
	#m.process("新疆维吾尔自治区昌吉回族自治州昌吉市昌吉市建国西路甜蜜家园9-1-301")
	#m.process("北京市北京市大兴区黄村镇海子角海悦公馆41号楼4单元602")
	#m.process("陕西省宝鸡市千阳县南关路粮食小区")
	#m.process("黑龙江省鸡西市虎林市黑龙江省虎林市公安南街276号")
	#m.process("辽宁省大连市金州区站前街道生辉第一城物业")
	#m.process("安徽省芜湖市无为县高沟镇龙庵街道")
	#m.process("广东省深圳市南山区科兴科学园A3单元12楼")
	#m.process("湖北省黄冈市浠水县散花镇涂墩村七组")
	for x in open("sample_address.txt"):
		m.process(x.strip("\n"))
