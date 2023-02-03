# Video to MP3 Converter
This is a video to mp3 convert built with a Microservice Architecture using Python, Docker, Kubernetes, AWS SQS, MongoDB and MySQL.

## Description

An in-depth paragraph about your project and overview of use.

## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

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
