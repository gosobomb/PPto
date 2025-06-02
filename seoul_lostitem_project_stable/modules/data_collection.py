
import pandas as pd
import requests
import time

def fetch_total_count(api_key):
    TYPE = "json"
    SERVICE = "lostArticleInfo"
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/{TYPE}/{SERVICE}/1/1"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API 호출 실패: {response.status_code}")
    data = response.json()
    total_count = int(data[SERVICE]['list_total_count'])
    return total_count

def fetch_batch(api_key, start_index, end_index):
    TYPE = "json"
    SERVICE = "lostArticleInfo"
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/{TYPE}/{SERVICE}/{start_index}/{end_index}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"API 호출 실패: {response.status_code}")
        return []
    data = response.json()
    try:
        rows = data[SERVICE]['row']
    except KeyError:
        print("API 데이터 파싱 오류 발생")
        return []
    extracted_data = []
    for item in rows:
        extracted_data.append({
            'lost_id': item.get('LOST_MNG_NO', ''),
            'status': item.get('LOST_STTS', ''),
            'reg_date': item.get('REG_YMD', ''),
            'rcv_date': item.get('RCV_YMD', ''),
            'details': item.get('LGS_DTL_CN', ''),
            'storage': item.get('CSTD_PLC', ''),
            'registrant_id': item.get('LOST_RGTR_ID', ''),
            'item_name': item.get('LOST_NM', ''),
            'item_type': item.get('LOST_KND', ''),
            'receive_place': item.get('RCPL', ''),
            'view_count': item.get('INQ_CNT', '')
        })
    return extracted_data

def load_data_from_api(api_key, batch_size=1000, delay=0.05):
    total_count = fetch_total_count(api_key)
    print(f"총 데이터 건수: {total_count} 건 수집 시작")
    all_data = []
    for start in range(1, total_count+1, batch_size):
        end = min(start + batch_size - 1, total_count)
        print(f"수집 중: {start} ~ {end}")
        batch_data = fetch_batch(api_key, start, end)
        all_data.extend(batch_data)
        time.sleep(delay)
    df = pd.DataFrame(all_data)
    return df
