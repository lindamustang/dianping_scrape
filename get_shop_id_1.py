import requests
from settings import SERVICE_ENDPOINT, SERVICE_SECRET


def get_start_page(saved_reviews):
    start_page = saved_reviews // 15 + 1
    if start_page == 1:
        return start_page - 1
    return start_page


def distribute_id(num):
    start_id = 22725
    print(num + start_id)
    while True:
        get_shop_url = SERVICE_ENDPOINT + 'shopMains?secret=' + \
                       SERVICE_SECRET + '&id=' + str(num + start_id)
        shop_data = requests.get(get_shop_url).json()['data'][0]
        if shop_data['reviews'] > shop_data['saved_reviews']:
            break
        num += 1
    start_page = get_start_page(shop_data['saved_reviews'])
    num += 1
    return shop_data['new_shop_id'], start_page, num


with open('random_shop_id.txt', 'r', encoding='utf-8') as f:
    s = f.readlines()

# with open('end_pages.txt', 'w', encoding='utf-8') as fw:
#     for i in s:
#         fw.write(i)

for n, i in enumerate(s):
    if 'k85bc0omqdN7QAxO' in i:
        print(n)



