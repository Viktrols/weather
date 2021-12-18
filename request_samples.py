import requests
#cities
print(requests.get('http://127.0.0.1:5000/cities').json())
#mean
print(requests.get('http://127.0.0.1:5000/mean/?city=Kyiv&value_type=temp').json())
print(requests.get('http://127.0.0.1:5000/mean/?city=Sumi&value_type=pcp').json())
#records
print(requests.get('http://127.0.0.1:5000/records/?city=Sumi&end_dt=2021-12-20&start_dt=2021-12-18').json())
print(requests.get('http://127.0.0.1:5000/records/?city=Kharkiv&end_dt=2021-12-22&start_dt=2021-12-16').json())
#moving_mean
print(requests.get('http://127.0.0.1:5000/moving_mean/?city=Kharkiv&value_type=clouds').json())
print(requests.get('http://127.0.0.1:5000/moving_mean/?city=Odessa&value_type=clouds').json())
