# Video to MP3 Converter
This is a video to mp3 convert built with a Microservice Architecture using Python, Docker, Kubernetes, AWS SQS, MongoDB and MySQL.

## Description
This application has a distributed system design make use of microservice architecture and is written with Python. It makes use of Docker, Kubernetes, AWS SQS, Mongo DB and mySQL. There 3 main services that are run on kubernetes and that is the auth service, the video to mp3 converter service and notification service. The system works as follows:

* Users interact with website via API Gateway which routes requests to authentication service. 
* Authenticated User credentials are stored in MySQLDB and has an attached JWT Token to gain access to the overall service. 
* AWS SQS is used to handle communication between the distributed microservice components. 
* When user uploads video it is stored in Mongo DB then a message is sent through SQS notifying converter servcice a video is ready for converation. 
* Once convertion is completed the conveter service sends a message through SQS which the notification service recieves then proceeds to alert the user via email that their mp3 is read for download.

![image](https://user-images.githubusercontent.com/21098368/216708933-25cee95d-572d-419e-b09c-621b32fec08f.png)

## Getting Started
Please note Mac OS was used thus installation methods may differ from windows and linux

### Prerequisite

* Docker Desktop
* Kubectl
* Minikube
* Python 3.7 or later
* You must have an AWS account, and have your default credentials and AWS Region configured as described in the [AWS Tools and SDKs Shared Configuration and Credentials Reference Guide](https://docs.aws.amazon.com/credref/latest/refdocs/creds-config-files.html). (NOTE! Costs are minimal for a small project but your account will still incure charges so set AWS Budgets)


#### Installing packages
Please note each service will have its own python virtualenv. So it's encourage to keep the base python install clean and install required packages in each venv.

Create a virtual env as follows:
```
python -m venv venv
```
Start a virtual env with:
```
source venv/bin/activate
```
Deactivate:
```
deactivate
```

Use python pip3 python package manager to install the following packages as required by service:
```
python -m pip install [package]
```
* Boto3 1.11.10 or later (converter & gateway service)
* MySQL (auth service)
* MongoDB (converter & gateway service)
* Flask (all)
* GridFS (converter & gateway service)

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

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [selikapro](https://github.com/selikapro)
* [awsdocs-sdk-examples](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/sqs#code-examples)
