import requests

# response = requests.post("http://127.0.0.1:5000/api/v1/advertisements",
#                 json={"title": "iphone 9", "description": "very expensive very expensive", "owner": "user_1"})
#
#
# print(response.status_code)
# print(response.json())

response = requests.delete("http://127.0.0.1:5000/api/v1/advertisements/3")

#
# print(response.status_code)
# print(response.json())
#
# response = requests.get("http://127.0.0.1:5000/api/v1/advertisements/3")
# print(response.status_code)
# print(response.json())
#
#
# response = requests.patch("http://127.0.0.1:5000/api/v1/advertisements/3",
#                 json={"title": "new title"})
#
#
# print(response.status_code)
# print(response.json())