
import pymysql
import matplotlib.pyplot as plt
mmm=pymysql.connect("123.56.23.174",'wang','wang1997','zb_dict')
cursor=mmm.cursor()
sql=("select qg from weibo ")
cursor.execute(sql)
y=cursor.fetchall()
mmm.close()
qg1 = 0
qg2 = 0
qg3 = 0
qg4 = 0
qg5 = 0
for num in range(0,len(y)):

    if 0 <= y[num][0]< 0.2 :
        qg1+=1
    elif 0.2<=y[num][0]<0.4 :
        qg2+=1
    elif 0.4<=y[num][0]<0.6 :
        qg3+=1
    elif 0.6<=y[num][0]<0.8 :
        qg4+=1
    else:
        qg5+=1

print(qg1,qg2,qg3,qg4,qg5)

plt.rcParams['font.sans-serif']='SimHei'
plt.figure(figsize=(8,8))
labels = ["消极","一般消极","较为客观","一般积极","积极"]
data = [qg1,qg2,qg3,qg4,qg5]
explode = [0.1,0.1,0.1,0.1,0.1]
patches,l_text,p_text=plt.pie(data,labels=labels,labeldistance=1.1,autopct="%1.1f%%",pctdistance=0.8,explode=explode,shadow=False)
for t in l_text:
    t.set_size(20)
for p in p_text:
    p.set_size(15)
title = plt.title("%d 条微博文本分析结果"%(qg1+qg2+qg3+qg4+qg5))
title.set_size(30)
plt.savefig('./华为注册鸿蒙.png')#保存图片
plt.show()



