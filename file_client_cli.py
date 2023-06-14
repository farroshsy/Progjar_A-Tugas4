import os
import socket
import json
import base64
import logging
import datetime

server_address = ('172.22.0.3', 6789)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received = ""  # empty string
        while True:
            # socket does not receive all data at once, data comes in parts, need to be concatenated at the end of the process
            data = sock.recv(4096)
            if data:
                # data is not empty, concatenate with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by breaking the loop
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dictionary, need to load it using json.loads()
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False


def remote_list():
    command_str = f"LIST"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print("Daftar file:")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False


def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    print("Response received:")
    if hasil['status'] == 'OK':
        # Process file from base64 to bytes
        namafile = hasil['data']['data_namafile']  # Access 'data_namafile' key correctly
        isifile = base64.b64decode(hasil['data']['data_file'])  # Access 'data_file' key correctly
        with open(namafile, 'wb+') as fp:
            fp.write(isifile)
        return True
    else:
        print("Gagal")
        return False


def remote_post(filename=""):
    with open(filename, 'rb') as fp:
        isifile = base64.b64encode(fp.read()).decode('utf-8')
        
    command_str = f"POST {filename} {isifile}\n"
    logging.warning(f"Sending command: POST")
    hasil = send_command(command_str)
    if hasil:
        logging.warning("Response received:")
        logging.warning(hasil)
        if hasil['status'] == 'OK':
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"\nFile '{filename}' berhasil diupload pada {current_time}\n")
            return True
    print("Gagal")
    return False


def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\nFile '{filename}' berhasil dihapus pada {current_time}\n")
        return True
    else:
        print("Gagal")
        return False


if __name__ == '__main__':
    server_address = ('172.22.0.2', 6789)

    print("Mencoba Fungsi List")
    remote_list()
    print("\n")
    print("Mencoba Fungsi Get")
    remote_get('donalbebek.jpg')
    remote_get('pokijan.jpg')
    remote_get('rfc2616.pdf')

    print("\n")
    print("Mencoba Fungsi Post")
    remote_post('filebaru.txt')
    remote_post('filelama.txt')
    remote_post('donalbebek2.jpg')
    print("\n")
    remote_list()
    print("\n")


    print("Mencoba Fungsi Delete")
    remote_delete('filelama.txt')
