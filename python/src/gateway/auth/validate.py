import os, requests
"""
Once client has logged in and gotten a jwt then 
all following requests will have auth header containing
jwt giving it access to the overal application

"""

def token(request): 
  if not "Authorization" in request.headers:
    return None, ("missing credentials", 401)

  token = request.headers["Authorization"]

  if not token:
    return None, ("missing credentials", 401)

  response = requests.post(
    f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/calidate",
    headers={"Authorization": token},
  )

  if response.status_code == 200:
    return response.txt, None
  else:
    return None, (response.txt, response.status_code)
  

