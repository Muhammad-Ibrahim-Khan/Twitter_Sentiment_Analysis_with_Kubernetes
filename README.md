# Overview
By the end of this repository, you'll have accomplished the following
- Analyzed Data and created a Pipeline to extract and clean textual data from raw data
- Trained the following models:
  - Sentiment Analysis through Word Embeddings.
  - GRU implementation of Twitter Sentiment Analysis.
- Created a minimal application in Flask to serve requests using [Batch Prediction](https://www.machinelearningatscale.com/machine-learning-batch-serving/)
- Create a Docker Image of your Application.
- Created a Kubernetes cluster.
- Deployed your Docker Image to your Kuberenetes cluster for serving (With a Horizontal Pod Autoscalar to take care of your application's throughput).

## Twitter Sentiment Analysis

This project is aimed to develop a sentiment analyzer using tweets from Twitter as our input data and training two models on them to make predictions.
The pre-processing on data, word embedding model and GRU based implementation have been done seperately in the notebooks, kindly follow the format for the directory arrangement.
Details on each individual element is present in the notebooks.

For deploying and serving your project, this repository will also go through setting up a local Kubernetes cluster. See the final section of the README for more details on setting up your local cluster.

Here is the link to the used -> [Dataset](https://www.kaggle.com/kazanova/sentiment140)

### Creating A Twitter Sentiment Analysis Docker Image
#### Environment Setup

Recommended: Use Conda for your virtual environment.

*Python Version: 3.9.12*
Run the following line for installing the necessary dependencies into your virtual environment.
> pip install -r requirements.txt

#### Flask API

The basic API configuration is present and is self-sufficient to get a response(sentiment) from your POST request at
the port you create.

*By default, the Port exposed is 4000*
#### Docker
Dockerfile has the necessary configuration to build your images and run your containers. Run this command to build your Docker image from the Docker File
* ***Note: It is important to tag your image with an appropriate name and label otherwise the name is chosen at random and label will always be 'latest'*** 
> docker build . -t <Insert_Any_Unique_Name>:<Add_Label>

For the Kubernetes Demo, use the following tag (If not then replace the image name in deployment.yaml with the one used to build it)
> docker build . -t k8s-demo:v1

## Kubernetes
Kubernetes is a powerful tool for managing containerized applications in production environments. It is a portable, extensible, open-source platform for managing containerized workloads and services.
#### Important
- Before going through this section, it is recommended to familiarize yourself with APIs and Docker Images and Containers.
- It is assumed that Docker has been installed locally, if not, go to this link to install [Docker](https://docs.docker.com/desktop/install/linux-install/)
- The following section only sets you up for Linux based OS (Personally tested on Ubuntu 22.04.01)
### Installation
* **Virtualbox** - Minikube is meant to run in a virtual machine (VM) so you will need virtualization software to act as the VM driver. By default, `docker` is set as the VM driver, however, it is extremely limited and debugging the issues are a headache so it's best to use Virtualbox instead. Installation instructions can be found [here](https://www.virtualbox.org/wiki/Downloads).

* **kubectl** - the command line tool for interacting with Kubernetes clusters. Installation instructions can be found [here](https://kubernetes.io/docs/tasks/tools/)

* **Minikube** - a Kubernetes distribution geared towards new users and development work. It is not meant for production deployments however since it can only run a single node cluster on your machine. Installation instructions [here](https://minikube.sigs.k8s.io/docs/start/).

The configuration of the minikube cluster I set are as follows:
- Minikube Version: 1.26.0-beta.1
- Driver: Virtualbox
- Kubernetes Version: 1.23.6
- Docker Version: 20.10.14
- Kubectl Version: 1.25.3

### Starting Minikube

Run the following command to start your minikube cluster.
> minikube start --driver=virtualbox --cpus="max" --disk-size='80000mb'

* **Exposing Local Images to Cluster** The image created locally won't be visible to the minikube cluster. To solve this issue, run the following command after starting minikube. See [this](https://octopus.com/blog/local-images-minikube) for more details
> minikube image load <Docker_Image_Tag>

### Configuring the Cluster
The yaml files have all the necessary instructions to deploy your Docker Image in the cluster. Here is the order in which to execute each

#### Deployment
This file has all the necessary configurations to create a deployment within the cluster which uses your docker image.

*Important: In case the image tag isn't k8s-demo:v1, replace it with your own.*

Execute the following command to create a deployment type object in your cluster
> kubectl apply -f yaml/deployment.yaml

After running this, wait until the pod is ready. To see the status of the pod, run the following command:
> kubectl get all

It'll take a few minutes for the pod to get ready. If it doesn't, debug and resolve the issue (try changing the kubernetes or kubectl versions).
Don't proceed until this part is done.
#### Service
This file has all the necessary configurations to create a service (external) which uses the deployment type object created previously and exposes it to calls from outside the cluster.

Execute the following command to create a service
> kubectl apply -f yaml/service.yaml

#### Autoscale
This file has the necessary instructions to horizontally scale, up (or down), the number of replicas of your Deployment based on certain conditions.

Execute the following command to create
> kubectl apply -f yaml/autoscale.yaml


### Test your Deployment
Open the dashboard by running the following command
> minikube dashboard

On the dashboard, you'll see the current status of your cluster (number of pods, usage etc).

The request.sh script sends a request to the service type object created previously. By running this, you'll be sending a POST request to an API within the cluster through this service in a loop (Interval of 0.1s).
*Important: Check the IP of the Minikube and replace the Host in the bash script if it's different.*

Run the following command in your terminal (in a separate window)
> bash request.sh

While the bash script is running, you'll notice an increase in the usage of the pods on the dashboard.
Moreover, the time taken for a request to be completed will also be slower than the rate at which it is being sent (by you).
This part is where the Horizontal Pod Autoscalar will come into play.

After a few minutes, you'll observe that the number of pods will increase due to increase in the demand (number of requests received by the service).
As soon as more number of pods are 'available', you'll notice an increase in the speed at which the requests are being fullfilled plus a decrease in the usage (per pod).
