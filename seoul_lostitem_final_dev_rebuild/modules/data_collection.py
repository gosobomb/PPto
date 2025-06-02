import pandas as pd
import requests
import time

def load_data_from_api(api_key="4b556375586e756e34365179614251", batch_size=1000, delay=0.05):
    total_count = fetch_total_count(api_key)
    print(f"총 데이터 건수: {total_count} 건 수집 시작")
    all_data = []
    for start in range(1, total_count+1, batch_size):
        end = min(start + batch_size - 1, total_count)
        print(f"수집 중: {start} ~ {end}")
        batch_data = fetch_batch(api_key, start, end)
        all_data.extend(batch_data)
        time.sleep(delay)
    df_raw = pd.DataFrame(all_data)
    return df_raw

def fetch_total_count(api_key):
    TYPE = "json"
    SERVICE = "lostArticleInfo"
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/{TYPE}/{SERVICE}/1/1"
    response = requests.get(url)
    data = response.json()
    total_count = int(data[SERVICE]['list_total_count'])
    return total_count

def fetch_batch(api_key, start_index, end_index, retries=5, delay=2):
    TYPE = "json"
    SERVICE = "lostArticleInfo"
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/{TYPE}/{SERVICE}/{start_index}/{end_index}"

    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            rows = data[SERVICE]['row']
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
        except Exception as e:
            print(f"Attempt {attempt+1} failed for batch {start_index}~{end_index}. Retrying...")
            time.sleep(delay)
    
    raise Exception(f"Failed to fetch data after {retries} retries for batch {start_index}~{end_index}.")