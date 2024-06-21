from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time

subscription_key = "YOUR_API_KEY"
endpoint = "YOUR_ENDPOINT"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def extract_text_from_image(image_path):
    with open(image_path, "rb") as image_stream:
        read_response = computervision_client.read_in_stream(image_stream, raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower() not in ['notstarted', 'running']:
            break
        time.sleep(1)

    # Return the results if they exist
    if read_result.status == OperationStatusCodes.succeeded:
        return read_result.analyze_result.read_results
    else:
        return None

def display_text_from_results(read_results):
    for page in read_results:
        for line in page.lines:
            print(line.text)
            for word in line.words:
                print(f"Word: '{word.text}', Bounding box: {word.bounding_box}")

# Example usage
image_path = "/home/ajay/OCR/sampleIMG.png"
results = extract_text_from_image(image_path)
if results:
    display_text_from_results(results)
else:
    print("No text found in the image.")
