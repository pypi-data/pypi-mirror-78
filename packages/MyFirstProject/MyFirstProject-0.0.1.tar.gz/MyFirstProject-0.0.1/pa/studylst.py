class StudyLst:
    '''
    学习科目数量要求要求
    '''
    def __init__(self):
        self.minNum='3'
    def num(self,age):
        if(age<=3):
            return self.minNum
        elif(age>3 and age<10):
            return '5'
        elif (age > 3 and age < 10):
            return '7'
        else:
            return '不规定数量'
if __name__=='__main__':
    print("这是一条测试：")
    ff=StudyLst()
    classNum=ff.num(8)
    print("科目数量为"+classNum)