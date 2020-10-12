def pop_ratio_by_region(region):
    import csv
    import numpy as np

    result = None
    with open('data-files/population.csv', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        
        for row in reader:
            if region in row[0]:    #region이 0번째에 포함되어 있다면
                result = np.array([ int(d.replace(',','')) for d in row[3:] ])  
                result = result / np.sum(result)

    return result

def top_one_similar_region(region, data):
    import csv
    import numpy as np

    total = []
    with open('data-files/population.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        lst = list(reader)
        lst = lst[1:]
        for row in lst:
            if region in row[0]:
                total.append(100)
            else:
                result = np.array([ int(d.replace(',', '')) for d in row[3:] ])
                result = result / np.sum(result)
                gap = data - result
                total.append(np.sum(np.abs(gap))) # 차이의 총량    
    
    mx, mn = np.argmax(total), np.argmin(total)
    region1 = lst[mx] # my region
    region2 = lst[mn] # other region
    
    region1 = (region1[0], [ int(x.replace(',', '')) for x in region1[3:] ])
    region2 = (region2[0], [ int(x.replace(',', '')) for x in region2[3:] ])

    return region1, region2

# def calculate_ratio_gap(data):    #위에서 뽑은 데이터를 계산 비교
#     import csv
#     import numpy as np

#     result = None
#     with open('data-files/population.csv', encoding = 'utf-8') as f:
#         reader = csv.reader(f)
#         next(reader)
#         for row in reader:


# if __name__ == '__main__':
#     import numpy as np
#     result = pop_ratio_by_region('화곡제1동')
#     # if result:
#     # print(result)
#     print(np.sum(result))
#     # print((result / np.sum(result)) * 100)   # 비율   %으로 보려면 *100
#     # else:
#     #     print('데이터를 찾을 수 없습니다.')

# print('이 코드는 항상 실행 됩니다.')
if __name__ == '__main__':      #import와 직접 실행을 구분하기 위한 조건
    
    # print('이 코드는 직접실행(python filename) 했을때만 실행 됩니다.')
    
    import numpy as np
    result = pop_ratio_by_region('화곡제1동')
    ## if result == None : result에 포함된 element 각각이 None인지 확인. 
    if result is None: # result자체가 None인지 확인 
        print('데이터를 찾을 수 없습니다.')
    else:
        print(np.sum(result))