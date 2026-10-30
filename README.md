# School Portal Reliability Engineering

## Project Overview

This project simulates a university student results portal that may experience performance and reliability problems when many students attempt to access their results simultaneously.

The objective is to deploy the application, investigate its behaviour under different traffic conditions, identify performance bottlenecks, implement reliability improvements, and compare system performance before and after those improvements.

The project demonstrates practical DevOps and cloud infrastructure engineering skills.

## Project Architecture

Current deployment architecture:

Student → Internet → AWS EC2 → Docker → Flask Application

### Technology Stack

* Python
* Flask
* Linux (Ubuntu 24.04)
* Docker
* Terraform
* AWS EC2
* AWS Security Groups
* Git and GitHub

## Project Status

### Completed

#### Application Development

* Initialized the Git repository and published it to GitHub.
* Created the Python virtual environment.
* Built the Flask application.
* Created the student results page.
* Implemented student ID submission and lookup.
* Tested successful student lookups.
* Tested unknown student ID responses.

#### Containerization

* Created a Dockerfile.
* Built the Docker image `school-portal:v1`.
* Tested the application locally using Docker.
* Verified local application accessibility.

#### Infrastructure and AWS Deployment

* Created AWS infrastructure using Terraform.
* Provisioned an EC2 instance in `eu-north-1` (Stockholm).
* Configured an AWS Security Group.
* Connected to the EC2 instance through SSH.
* Investigated and resolved an outbound connectivity problem caused by missing security group egress rules.
* Installed Docker on the EC2 instance.
* Exported the Docker image from the local computer.
* Transferred the image to AWS using SCP.
* Loaded the image into Docker on EC2.
* Started the Flask application in a Docker container.
* Configured port forwarding from EC2 port 80 to container port 8080.
* Verified the application using curl on the EC2 instance.
* Successfully accessed the deployed portal through the EC2 public IP.

## AWS Deployment Configuration

| Component         | Configuration     |
| ----------------- | ----------------- |
| AWS Region        | eu-north-1        |
| Instance Type     | t3.micro          |
| Operating System  | Ubuntu 24.04      |
| Container Image   | school-portal:v1  |
| Container Port    | 8080              |
| EC2 HTTP Port     | 80                |
| Deployment Method | Docker on AWS EC2 |

## Upcoming Work

### Performance Testing

* Establish baseline performance measurements.
* Simulate concurrent student requests.
* Measure response times and throughput.
* Investigate application behaviour under increasing traffic.

### Monitoring and Investigation

* Monitor CPU and memory utilization.
* Examine application and container logs.
* Identify potential performance bottlenecks.
* Investigate reliability issues.

### Reliability Improvements

* Implement appropriate application and infrastructure improvements.
* Repeat load tests after improvements.
* Compare baseline and improved performance.

### Documentation

* Document testing methodology.
* Publish performance measurements.
* Include architecture diagrams.
* Document engineering decisions and lessons learned.

## Project Objective

The final objective is to demonstrate how DevOps practices can help deploy, monitor, investigate, and improve the reliability and performance of an application.

This is a simulated university results portal, not a production university system.
