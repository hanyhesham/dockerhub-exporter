import time
import threading
import os
import requests
from prometheus_client import Gauge, make_wsgi_app
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# Create the Gauge metric
x = Gauge('docker_image_pulls', 'The total number of Docker image pulls',
    ['image', 'organization'])
# Access DockerHUB_ORG ENV Variable
dockerhub_org = os.environ["DOCKERHUB_ORGANIZATION"]
# Export Port
HTTP_PORT = 2113
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

def set_gauge():
    while True:
        results = get_images(dockerhub_org)
        # Iterate on the docker images
        for item in results:
            # Set the metric value
            x.labels(image=item["name"], organization=dockerhub_org).set(item["pull_count"])
        # Sleep for 5 sec
        time.sleep(5)

def get_images(org):
    try:
        # Retrieve List of images and their counts
        docker_image_url = f"https://hub.docker.com/v2/repositories/{org}/?page_size=25&page=1"
        response = requests.get(docker_image_url, timeout=3, verify=True)
        response.raise_for_status()
        # Access JSON content
        json_response = response.json()
    # Handle different exceptions
    except requests.exceptions.HTTPError as http_error:
        print("HTTP Error")
        print(http_error.args[0])
    except requests.exceptions.ReadTimeout:
        print("Timeout")
    except requests.exceptions.ConnectionError:
        print("Connection error")
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
    return json_response["results"]


if __name__ == '__main__':

    # Start a new thread
    k = threading.Thread(target=set_gauge)
    k.start()
    dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
    run_simple(hostname="0.0.0.0", port=2113, application=dispatcher)
