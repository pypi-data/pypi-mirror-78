import pandas as pd
import os

def test_read_csv(file_name = "ipartment_cast_data.csv"):
    tips = """
tips:
    execute code:
    pd_data = pd.read_csv(file_name ,sep = ',',encoding = 'gbk')
    for i in range(len(pd_data)):
        print(i,list(pd_data.iloc[i]))
    """
    print(tips)
    file_path = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(file_path,file_name)

    print("最新的file_name",file_name)
    if not os.path.exists(file_name):
        test_to_csv(file_name)
        
    pd_data = pd.read_csv(file_name ,sep = ',',encoding = 'gbk')
    print("list(pd_data.columns):\n",list(pd_data.columns))
    print("\nlist(pd_data.iloc[i]):\n")
    for i in range(len(pd_data)):
        print(i,list(pd_data.iloc[i]))

def test_to_csv(file_name = None):
    tips = """
tips:
    execute code:
    pd_data.to_csv(file_name, sep = ',',index = False,encoding = 'gbk')
    the following parameters must be given:
    file_name,sep,index,encoding
    """
    if file_name is None:
        print(tips)
        file_name = "ipartment_cast_data.csv"
    
    columns = ["name","sex","birth year","howntown","occupation"]
    cast_data = [["陆展博","男",1986,"上海市","程序员"],
                 ["林宛瑜","女",1987,"淄博市","服装设计师"],
                 ["胡一菲","女",1988,"大连市","大学教授"],
                 ["曾小贤","男",1985,"福州市","电台主持人"],
                 ["吕子乔","男",1982,"成都市","自由职业者"],
                 ["陈美嘉","女",1985,"济南市","经纪人"],
                 ["关谷神奇","男",1985,"上海市","漫画家"],
                 ["张伟","男",1987,"鞍山市","律师"]
                ]
    pd_data = pd.DataFrame(cast_data,columns = columns)
    pd_data.to_csv(file_name, sep = ',',index = False,encoding = 'gbk')

if __name__ == "__main__":
    #test_df__to_csv()
    test_read_csv()
