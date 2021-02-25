from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from pprint import pprint
import requests



def index(request):
    """
    """

    context = {'title': 'タイトルです'}

    return render(request, 'app/index.html', context)


def data_insert(listData, domain, app_id, api_token):
    """
    kintoneへのデータ挿入
    """

    url = "https://{}.cybozu.com/k/v1/records.json".format(domain)

    headers = {"X-Cybozu-API-Token": api_token,
               "Content-Type": "application/json"}

    listRecords = []
    for dictTemp in listData:
        dictData = {}
        for key, val in dictTemp.items():
            dictData[key] = {"value": val}

        listRecords.append(dictData)

    params = {
        "app": app_id,
        "records": listRecords
    }

    # pprint(params)
    resp = requests.post(url, json=params, headers=headers)
    # print(resp.text)


@csrf_exempt
def api_02(request):
    """
    postでjsonを受け取り、jsonを返すAPI
    """

    request_data = json.loads(request.body)

    # pprint(request_data)

    listData = []
    for row in request_data['rows']:
        # pprint(row)
        for cnt in range(5):
            if row[cnt+2] != "":
                sag = '{:02d}_{}'.format(row[0], row[1])
                dictTemp = { '作業NO': 1,
                            '作業': sag, '測定回': cnt+1, '時間': float(row[cnt+2])}
                listData.append(dictTemp)

    app_id = int(request_data['app_id'])
    domain = request_data['domain']
    api_token = request_data['api_token']

    data_insert(listData, domain, app_id, api_token)

    # print(request_data)

    dctData = {}
    # dctData['初期値'] = 'なし'
    # dctData['データ'] = request_data

    return HttpResponse(
        json.dumps(dctData, ensure_ascii=False),
        content_type='application/json; charset=utf-8',
    )
