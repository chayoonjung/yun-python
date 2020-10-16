from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
import json
import joblib

cyj = Blueprint('cyj', __name__, template_folder="demo_templates")

predict_model=joblib.load('models/cyj-model.pkl')


@cyj.route('/cyj/sg-pop', methods=['GET'])
def cyj1():
    import pandas as pd
    import numpy as np
    test_data = pd.read_csv('data-files/people_data_en.csv', encoding='utf-8')
    gu_data=test_data.to_dict('records')
    return json.dumps(gu_data, ensure_ascii=False)

@cyj.route('/cyj/sg-hl-pop', methods=['GET'])
def cyj3():
    import pandas as pd
    import numpy as np
    test_data = pd.read_csv('data-files/hl_people_data_en.csv', encoding='utf-8')
    hl_pop_data=test_data.to_dict('records')
    return json.dumps(hl_pop_data, ensure_ascii=False)


@cyj.route('/cyj/sg-sales', methods=['GET'])
def cyj2():
    import pandas as pd
    import numpy as np
    
    df1 = pd.read_csv('data-files/store_sale_df_en.csv', encoding='utf-8')
    # df2=df1.groupby(['yesrSe','sgSeCdName','guName']).sum().reset_index()
    df2 = df1.groupby(['guName','yesrSe'])['monthSales'].sum().reset_index()
    # df2_1=df2[df2['yesrSe']=='2019_1']

    sales_data1=df2.to_dict('records')
    return json.dumps(sales_data1, ensure_ascii=False)




@cyj.route('/cyj/sales-sex-chart', methods=['GET'])
def cyj4():
    import pandas as pd
    import numpy as np
    test_data = pd.read_csv('data-files/store_sale_df_en.csv', encoding='utf-8')
    test2=test_data[['yesrSe','guName','monthSales','menSales','womenSales']]
    test2=test2.groupby(['guName','yesrSe']).sum().reset_index()
    test2['menSalesRatio'] = test2['menSales']/(test2['womenSales']+test2['menSales'])*100
    test2['womenSalesRatio'] = test2['womenSales']/(test2['womenSales']+test2['menSales'])*100
    test2=test2.round(2)
    test3=test2[['guName','yesrSe','menSalesRatio','womenSalesRatio']]

    test3=test3.sort_values(by=['guName','yesrSe'], axis=0)
    sales_data2=test3.to_dict('records')
    return json.dumps(sales_data2, ensure_ascii=False)

@cyj.route('/cyj/choice', methods=['GET'])  
def cyj5():

    gu = request.args.get('gu')
    category = request.args.get('category')
    storecnt = int( request.args.get('storecnt') )

    import pandas as pd

    choice=pd.read_csv('data-files/choice_en.csv')
    choice=choice.replace('상권확장',1).replace('다이나믹' ,4).replace('정체',2).replace('상권축소',3)


    choice2 = choice[(choice['guName'] == gu) & 
                      (choice['serviceKind'] == category) & 
                      (choice['storeCnt'] <= storecnt)]


    test = choice2.to_dict('records')  # json으로 처리할때 dict과 유사함  

    return json.dumps(test, ensure_ascii=False)  

@cyj.route('/cyj/choice2', methods=['GET'])  
def cyj6():

    gu = request.args.get('gu')
    category = request.args.get('category')
    storecnt = int( request.args.get('storecnt') )

    import pandas as pd

    choice=pd.read_csv('data-files/choice_en.csv')
    choice=choice.replace('상권확장',1).replace('다이나믹' ,4).replace('정체',2).replace('상권축소',3)


    choice2 = choice[(choice['guName'] == gu) & 
                      (choice['serviceKind'] == category) & 
                      (choice['storeCnt'] <= storecnt)]

    # choice2 = choice[(choice['guName']=='강서구') & (choice['serviceKind']=='인테리어') & (choice['storeCnt'] <=3)]
    choice2 = (choice2['sgChangePoint'].sum() / len(choice2)).round(0)

    if choice2== 1 : 
        result='추천'
    elif choice2 == 2 :
        result='주의'
    elif choice2 == 3:
        result='위험'
    else:
        result='고위험'

    # result = result.to_dict('records')  # json으로 처리할때 dict과 유사함  
    return result

@cyj.route('/cyj/predict', methods=['GET'])  
def predict_gu():

    gu = request.args.get('gu')
    menFlowRatio = request.args.get('menFlowRatio')
    womenFlowRatio = request.args.get('womenFlowRatio')

    # gu='강서구'
    # menFlowRatio = 40
    # womenFlowRatio = 60
    
    params=[[gu, float(menFlowRatio), float(womenFlowRatio)]]
    
    result = predict_model.predict(params)


    if result[0]== 1 : 
        result='상권확장'
    elif result[0] == 2 :
        result='정체'
    elif result[0] == 3:
        result='상권축소'
    else:
        result='다이나믹'
                      
    return result 

