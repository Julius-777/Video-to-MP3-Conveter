# Video to MP3 Converter
A Microservice architecture enables the rapid, frequent and reliable delivery of large, complex applications. It also enables an organization to evolve its technology stack more easily without breaking systems and has being come a popular framework intergrating well with modern software engineering principles such as Agile. This project was built in order to implement these principles on a small scale project.

## Description
This video to mp3 converter application has a distributed system design and was built using Python, Docker, Kubernetes, AWS SQS, MongoDB and MySQL. This microservice architecture has 3 main services running on kubernetes. They include the auth service, the video to mp3 converter service and the notification service. The system works as follows:

* Users interact with website via API Gateway which routes requests to authentication service. 
* Authenticated User credentials are stored in MySQLDB and has an attached JWT Token to gain access to the overall service. 
* AWS SQS is used to handle communication between the distributed microservice components. 
* When user uploads video it is stored in Mongo DB then a message is sent through SQS notifying converter servcice a video is ready for converation. 
* Once convertion is completed the conveter service sends a message through SQS which the notification service recieves then proceeds to alert the user via email that their mp3 is read for download.

![image](https://user-images.githubusercontent.com/21098368/216708933-25cee95d-572d-419e-b09c-621b32fec08f.png)

## Getting Started
PLEASE NOTE: Mac OS was used thus installation methods may differ from windows and linux

### Prerequisite

* Docker Desktop
* Kubectl
* Minikube
* Python 3.7 or later
* You must have an AWS account, and have your default credentials and AWS Region configured as described in the [AWS Tools and SDKs Shared Configuration and Credentials Reference Guide](https://docs.aws.amazon.com/credref/latest/refdocs/creds-config-files.html). (NOTE! Costs are minimal for a small project but your account will still incure charges so set AWS Budgets)
* AWS CLI Credentials need to be setup with your AWS account with permissions granted send and recieve messages from your Queues
* Need to configure an MP3 Message Queue and Video Message Queue on AWS SQS


### Installing packages
Kubernetes will run the docker images hosted on my [docker registry](https://hub.docker.com/repositories/jmc777)
If wanting to recreate the evnironemnt locally please note each service will have its own python virtualenv. So it's encourage to keep the base python install clean and install required packages for each service in its own venv.

#### Setup the virtual ENV for each service as follows:
```
mkdir gateway
cd gateway
python3 -m venv venv
source ./ven/bin/activate
env | grep ENV  
```
Deactivate ENV 
```
deactivate
```

#### Use python pip3 python package manager to install the following packages as required by service:
```
python -m pip install [package]
```
* Boto3 1.11.10 or later (converter & gateway service)
* MySQL (auth service)
* MongoDB (converter & gateway service)
* Flask (all)
* GridFS (converter & gateway service)
* awscli

## Help

Kubernetes pods may fail for one or multiple reasons. A common problem is incorrect indentation or spelling errors in the kubernetes yaml files.
The following commands are useful for debugging when getting Crashloopback errors.

```
kubectl describe pods
```
```
kubectl logs -f [pod name]
```
For further guidances read the following resource. [Debuging K8s](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)


## License

This project is licensed under the MIT License 

## Acknowledgments

Inspiration, code snippets and guidance.
* [selikapro](https://github.com/selikapro)
* [awsdocs-sdk-examples](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/sqs#code-examples)
