# Docker Image Prometheus Exporter

This Repo hosts python code which export metrics about the number of pulls of docker images of a specific organization.

## Code Structure

There are four functions:

- hello: used to print hello world for / route (used as health check)

- set_gauge: used to set the metric values based on results from the Dockerhub JSON.

- get_images: used to curl dockerhub and get JSON data about a specific organization.

- main: used to start the Prometheus HTTP server using wsgi_app on port 2113 and route /metrics.

The python code expects environment variable DOCKERHUB_ORGANIZATION which matches the name of organization to curl