import os
import time

from flask import json
from pptx import Presentation
import openai


REQ = 'Please provide a summary in English ' \
      '(if the text I give you is in other language I want the summary in English)' \
      ' of the text on this slide, ' \
      'and brief explanation about the topic' \
      'along with a recommended website to learn more about the topic.' \
      'If the slide not contain eny text dont answer.' \
      'Give the answer like educational paragraph.\n'
KEY = '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'

messages = []
messages.append({"role": "system", "content": f"you are a helpful AI that is explaining a PowerPoint presentation."})
openai.api_key = KEY


def import_to_file(text_list):
    """
    Importing list of strings of GPT answers into txt file
    :param text_list: list of strings
    """
    try:
        with open('res.txt', 'w') as file:
            [file.write(f'{line}\n') for line in text_list]
        print('\nfile is ready')
    except Exception as ex:
        print(ex)


def extract_text_from_slides(presentation_path):
    """
    Extract text from each slide from pptx file.
    :param presentation_path: The path of tje pptx file.
    :return: list of strings, each string contains slide's text.
    """
    ppt = Presentation(presentation_path)
    text_list = []
    for slide in ppt.slides:
        slide_text = [shape.text_frame.text for shape in slide.shapes if shape.has_text_frame]
        text_list.append(''.join(slide_text))
    return text_list


def craete_request(text):
    """
    Create request for GPT from the "text" parameter and return GPT's answer.
    :param text: The text from the slide.
    :return: The answer of GPT about the text parameter.
    """
    request = REQ + text
    return get_ans_from_AI(request)


def get_ans_from_AI(msg):
    """
    Send a message to GPT and return its reply.
    :param msg: msg to GPT.
    :return: The answer of GPT.
    """
    messages.append({"role": "user", "content": msg})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    assistant_reply = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply


def process_files():
    uploads_folder = os.path.join(os.getcwd(), 'uploads')
    outputs_folder = os.path.join(os.getcwd(), 'outputs')

    while True:
        time.sleep(10)  # Sleep for 10 seconds between iterations

        # Scan the uploads folder and identify files that haven't been processed
        for filename in os.listdir(uploads_folder):
            file_path = os.path.join(uploads_folder, filename)
            if os.path.isfile(file_path) and filename not in os.listdir(outputs_folder):
                print(f"Processing file: {filename}")

                # Process the file using existing code
                data_list = extract_text_from_slides(file_path)
                result = []
                for text in data_list:
                    request = create_request(text)
                    answer = get_ans_from_AI(request)
                    print(text)
                    print(answer)
                    result.append({'text': text, 'answer': answer})

                # Save the explanation JSON in the outputs folder
                output_filename = os.path.splitext(filename)[0] + '.json'
                output_path = os.path.join(outputs_folder, output_filename)
                with open(output_path, 'w') as output_file:
                    json.dump(result, output_file)

                print(f"Explanation JSON saved: {output_filename}")
                os.remove(file_path)  # Remove the processed file from the uploads folder

            else:
                print(f"Skipping file: {filename} (already processed)")


if __name__ == "__main__":
    process_files()

# def main():
#     res = []
#     data_list = extract_text_from_slides(r'C:\Users\omer\Excellenteam\pptxPro\Honeypot.pptx')
#     for text in data_list:
#         request = craete_request(text)
#         answer = get_ans_from_AI(request)
#         print(text)
#         print(answer)
#         time.sleep(20)
#         res.append(text)
#     import_to_file(res)
#
#
# if __name__ == "__main__":
#     main()
