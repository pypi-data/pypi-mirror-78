from . import gl
#import gl


class kt:
    def insert(id,name,parent_id,flag=0):
        res=[]
        item = {}
        item['id'] = id
        item['name'] = name
        item['parent_id'] = parent_id
        item['flag'] = flag
        res.append(item)
        gl.forest = gl.forest.append(res,ignore_index=True)

    def attach(item):
        gl.forest = gl.forest.append(item, ignore_index=True)
    def update(id):
        idx =[]
        idx.append(id)
        #print(idx)
        gl.forest.loc[gl.forest['id'].isin(idx), 'flag'] = 1
    def nrow(self='tree'):
        return(gl.forest.shape[0])
    def ncol(self='tree'):
        return(gl.forest.shape[1])
    def rest(self='tree'):
        return (gl.forest[gl.forest.flag == 0])

    def rest_id(self='tree'):
        res = gl.forest[gl.forest.flag == 0]['id']
        res = list(res)
        return res
    def getId(name):
        var_name =[]
        var_name.append(name)
        #print(idx)

        res = gl.forest.loc[gl.forest['name'].isin(var_name), 'id']
        res = list(res)
        res = res[0]
        return res
    def delRow(id):
        gl.forest = gl.forest.drop(index=(gl.forest.loc[(gl.forest['id'] == id)].index))
        gl.forest = gl.forest.reset_index(drop=True)
    def formatter(obj=gl.forest,format ='list'):
        nrow = obj.shape[0]
        # ncol = obj.shape[1]
        #不计算最后一列
        # ncol =ncol -1
        #不计算第一行
        #nrow =nrow +1
        res =[]

        if format =='list':
            for i in range(nrow):
                row = []
                row.append(obj.iloc[i, 1])
                row.append(obj.iloc[i, 0])
                row.append(obj.iloc[i, 2])
                res.append(row)
        else:
            for i in range(nrow):
                row = {}
                row['name'] = obj.iloc[i, 1]
                row['id'] = obj.iloc[i, 0]
                row['parent_id'] = obj.iloc[i, 2]
                res.append(row)

        return res


    def print(self='tree'):
        print(gl.forest)