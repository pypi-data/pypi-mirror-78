import pandas as pd
# pip install pandas==1.0.1
import numpy as np
forest = pd.DataFrame(columns=('id','name','parent_id','flag'))
item = [{'id':'0','name':'root','parent_id':'-1','flag':0}]
forest = forest.append(item,ignore_index=True)

# print(forest)
#设置初始化的标准，第一次生效
kc_initial = True