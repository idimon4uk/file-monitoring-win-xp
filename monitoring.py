import os
import json
import time
import http.client

token = '' #telegram_bot_token
chat_id = '' #chat id
pc_name = '' #name of computer
path = '' #path for monitoring
file_name = 'tree.json'

def send_telegram_message(token, chat_id, message):
    conn = http.client.HTTPSConnection("api.telegram.org")
    url = f"/bot{token}/sendMessage"
    
    payload = json.dumps({
        'chat_id': chat_id,
        'text': message
    })

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        conn.request("POST", url, payload, headers)
        response = conn.getresponse()
        data = response.read()
        if response.status == 200:
            print("Повідомлення успішно відправлено.")
        else:
            print("Помилка при відправці повідомлення.")
    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        conn.close()

def alarm(status ,text):
    print(status, text)
    message = pc_name + ':' + status + ':' + '--' + text
    send_telegram_message(token, chat_id, message)


def compare_arrays(arr1, arr2):
    new_elements = list(set(arr2) - set(arr1)) 
    removed_elements = list(set(arr1) - set(arr2)) 
    return new_elements, removed_elements

def read_array_from_json_file(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data

def write_array_to_json_file(arr, file_name):
    with open(file_name, 'w') as file:
        json.dump(arr, file, indent=4)

def remove_duplicates(arr):
    return list(set(arr))

def list_files_and_folders(path, array):
    for root, dirs, files in os.walk(path):
        # print(f"Поточна папка: {root}")
        array.append(root)
        for dir_name in dirs:
            array.append(os.path.join(root, dir_name))
            # print(f"Папка: {os.path.join(root, dir_name)}")
        for file_name in files:
            array.append(os.path.join(root, file_name))
            # print(f"Файл: {os.path.join(root, file_name)}")


def run ():
    array = []
    list_files_and_folders(path, array)
    array = remove_duplicates(array)
    old_array = read_array_from_json_file(file_name)
    new_elements, removed_elements = compare_arrays(old_array, array)
    for el in new_elements:
        alarm(' Новий файл/нова папка', el)
    for el in removed_elements:
        alarm('Видалений файл/видалена папка', el)
    write_array_to_json_file(array, file_name)

def periodic_run(interval=30):
    while True:
        run()
        time.sleep(interval)

periodic_run(30)