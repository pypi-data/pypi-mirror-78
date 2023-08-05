#write by Reshape Data
#设置数组的长度

def arrayLen(arrayData):
	res = 0
	res = len(arrayData)
	return res

#定义数据按列选择
def arrayColSel(arrayData,selector=[0,1]):
	res = []
	for i in range(len(arrayData)):
		row = []
		for j in range(len(selector)):
			index = selector[j]
			row.append(arrayData[i][index])
		res.append(row)    
	return res
#使用表达式重新设计实现方式
def arrayColSel2(arrayData,ColIndex=0):
	#使用列表表达式，代码更简洁
	res = [row[ColIndex] for row in arrayData]
	return res

#定义数据按行进行选择
def arrayRowSel(arrayData,selector=[0,1]):
	res = []
	for i in range(len(selector)):
		res.append(arrayData[selector[i]])
	return res

#按数据列进行转换为小数
def arrayColNumeric(arrayData,colIndex,digit=2):
	res = []
	for i in range(len(arrayData)):
		row = []
		for j in range(len(arrayData[i])):
			if j == colIndex:
				row.append(round(float(arrayData[i][j]),digit))
			else:
				row.append(arrayData[i][j])
		res.append(row)
	return res

#按数据列进行转换为整数
def arrayColInt(arrayData,colIndex,digit=2):
	res = []
	for i in range(len(arrayData)):
		row = []
		for j in range(len(arrayData[i])):
			if j == colIndex:
				row.append(int(arrayData[i][j]))
			else:
				row.append(arrayData[i][j])
		res.append(row)
	return res

#向数据指定列复制值
def arrayInsertRepValue(arrayData,value,colIndex =0):
	res = []
	for i in range(len(arrayData)):
		row = arrayData[i]
		row.insert(colIndex,value)
		res.append(row)
	return res
	
#向二维数据插入序号
def arrayInsertIndex(arrayData,index=-1):
	res = []
	if index == -1:
		idx =len(arrayData[0])
	else:
		idx = index
	for i in range(len(arrayData)):
		row = arrayData[i]
		row.insert(idx,i+1)
		res.append(row)
	return res
#向量处理
def vectRange(vect, selector=[1, 3]):
	res = []
	for i in range(len(selector)):
		res.append(vect[selector[i]])
	return(res)

#在数据指定列填写前缀
def arrayAddPrefix(arrayData,colIndex=0,prefix="问题",suffix=":",NumIndex=True):
	res = arrayData
	for i in range(len(arrayData)):
		if NumIndex :
			prefix_num = str(i + 1)
		else :
			prefix_num = ""
		res[i][colIndex] = prefix + prefix_num + suffix + arrayData[i][colIndex]
	return(res)

#设置数据的链接函数
def arrayPaste(arrayData, sep=",", collapse="\n"):
	res = []
	for i in range(len(arrayData)):
		res.append(sep.join(arrayData[i]))
	res2 = collapse.join(res)
	return (res2)
#检查文件中是否包含dict中的多个单词
def textSearch(key,dict):
    for x in range(len(dict)):
        item = key in dict[x]
        #print(item)
        if item :
            return True
            break
        else:
            continue
    return False

def testPrint():
	print('hello world')

# 定义dict_keys_list
def dict_keys_list(dict):
    res =  [i for i in dict.keys()]
    return res
# 定义dict_values_list
def dict_values_list(dict):
    res = [i for i in dict.values()]
    return res
#定义两个列表转dict
def list_as_dict(list_keys,list_values):
    res = dict(zip(list_keys,list_values))
    return res
#定义数据查找函数
def arrayLookup(arrayData,txt_search,look_idx,ret_idx):
	for i in range(len(arrayData)):
		look_value = arrayData[i][look_idx]
		if txt_search == look_value:
			return arrayData[i][ret_idx]
			break
		else:
			continue
	return False






if __name__ == "__main__":
	mydata = [1,2,3,4,5]
	print(vectRange(mydata,[1,2]))
	myarr = [['A1'],['B1']]
	myres = arrayAddPrefix(myarr,0)
	print(myres)
	text = "|".join(['a',"b","c"])
	print(text)
	myarr2 = arrayPaste(myarr)
	print(myarr2)
	a = ["我是胡立磊"]
	b = "我是e"
	print(textSearch(b, a))
	mydata2 =[['1','tom'],['2','jack']]
	print(arrayLookup(mydata2,'jack',1,0))
	print(arrayColSel2(mydata2,0))
