import requests

url = "http://localhost:8000//Users/HP/Documents/networking/lab2"

x=input("What Do You Want To Do-\n1.GET REQUEST\n2.POST REQUEST\n3.TO EXIT\n")

while x<'1' or x>'3':
    print("INVALID OPTION...")
    x=input("What Do You Want To Do-\n1.GET REQUEST\n2.POST REQUEST\n")

if x=='1':
    file_name=input("Enter File Name- ")
    download_url = f"{url}/{file_name}"
    response = requests.get(download_url)
    if response.status_code == 200:
        with open("c.txt", "wb") as f:
            f.write(response.content)
        print("File Successfully received.")
    else:
        print(f"Error: Could not receive file. Status code: {response.status_code}")


elif x=='2':
    file_name=input("Enter File Name- ")

    files = {'file': (file_name, open(file_name, 'rb'))}
    
    response = requests.post(url, files=files)
    if response.status_code == 201:
        print(response.text)
        print(f"File {file_name} successfully uploaded.")
    else:
        print(response.text)
        print(f"Error: Could not upload file. Status code: {response.status_code}")

else:
    pass

