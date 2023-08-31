import os
import requests
from dataclasses import dataclass


@dataclass
class Status:
    status: str
    filename: str
    timestamp: str
    explanation: str

    def is_done(self):
        return self.status == 'done'


class PythonClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        url = f"{self.base_url}/upload"
        files = {'file': open(file_path, 'rb')}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            response_json = response.json()
            uid = response_json.get('uid')
            if uid:
                return uid
            else:
                raise Exception("Invalid response from server: missing UID")
        else:
            raise Exception(f"Error uploading file: {response.text}")

    def status(self, uid):
        url = f"{self.base_url}/status"
        params = {'uid': uid}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            response_json = response.json()
            status = response_json.get('status')
            filename = response_json.get('filename')
            timestamp = response_json.get('timestamp')
            explanation = response_json.get('explanation')
            return Status(status, filename, timestamp, explanation)
        elif response.status_code == 404:
            raise Exception("Upload not found")
        else:
            raise Exception(f"Error retrieving status: {response.text}")


def main():
    client = PythonClient("http://localhost:5000")  # Replace with the actual base URL of your web app

    # Upload a file
    file_path = r"C:\Users\omer\Excellenteam\pptxPro\WebAPI\Example1.pptx"
    try:
        uid = client.upload(file_path)
        print(f"Upload successful! UID: {uid}")
    except Exception as e:
        print(f"Upload failed: {str(e)}")

    # Check the status of an upload
    uid = "123456"  # Replace with the UID of the upload you want to check
    try:
        status = client.status(uid)
        print(f"Status: {status.status}")
        print(f"Filename: {status.filename}")
        print(f"Timestamp: {status.timestamp}")
        print(f"Explanation: {status.explanation}")
        if status.is_done():
            print("Upload is done")
        else:
            print("Upload is still pending")
    except Exception as e:
        print(f"Error retrieving status: {str(e)}")


if __name__ == '__main__':
    main()
