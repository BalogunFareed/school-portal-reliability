# School Portal Performance & Reliability Report

## 1. Project Overview

The School Portal Reliability Engineering project simulates a university results portal and investigates how its application performs under different traffic conditions.

The objective of this phase was to establish a performance baseline, introduce a production-oriented application server, simulate student traffic, and compare application performance.

### Objectives

* Deploy the Flask application using Docker.
* Establish baseline response times using Flask's development server.
* Replace the development server with Gunicorn.
* Investigate how Gunicorn worker processes affect request handling.
* Simulate student traffic using Locust.
* Measure response times, throughput, failures, and container resource consumption.

### Testing Environment

| Component                         | Configuration |
| --------------------------------- | ------------- |
| Application                       | Python Flask  |
| Application server                | Gunicorn      |
| Containerisation                  | Docker        |
| Load testing                      | Locust        |
| Cloud provider                    | AWS           |
| Compute                           | EC2 t3.micro  |
| Operating system                  | Ubuntu 24.04  |
| AWS Region                        | eu-north-1    |
| Application port inside container | 8080          |
| Public application port           | 80            |

## 2. Testing Methodology

Performance testing was conducted in three stages.

### Stage 1: Flask Development Server

The application initially ran using Flask's built-in development server inside a Docker container.

Five sequential requests were sent directly from the EC2 instance to its local application endpoint.

The purpose was to establish an initial response-time reference.

**Results:**

| Request     | Response Time |
| ----------- | ------------: |
| 1           |      1.952 ms |
| 2           |      1.664 ms |
| 3           |      1.575 ms |
| 4           |      1.713 ms |
| 5           |      1.651 ms |
| **Average** |  **1.711 ms** |

All five requests returned HTTP 200.

*Note: These measurements were taken through localhost. They do not represent actual internet-facing user response times.*

### Stage 2: Gunicorn with One Worker

The Flask development server was replaced with Gunicorn, a production-oriented WSGI application server.

The application was rebuilt and redeployed using Docker.

Gunicorn initially ran with one synchronous worker.

Locust was used to simulate student activity, including homepage visits and results checks.

**Test 1: One simulated user**

| Metric                |    Result |
| --------------------- | --------: |
| Total requests        |       133 |
| Failures              |         0 |
| Average response time | 417.82 ms |
| Median response time  |    410 ms |
| 95th percentile       |    530 ms |
| 99th percentile       |    650 ms |
| Maximum response time |    689 ms |

**Test 2: Ten simulated users**

| Metric                |    Result |
| --------------------- | --------: |
| Total requests        |       535 |
| Failures              |         0 |
| Average response time | 435.61 ms |
| Median response time  |    380 ms |
| 95th percentile       |    740 ms |
| 99th percentile       |  1,100 ms |
| Maximum response time |  1,430 ms |
| Throughput (RPS)      |       4.2 |

### Stage 3: Gunicorn with Two Workers

The Dockerfile was updated to run Gunicorn with two synchronous workers instead of one.

The application was rebuilt, transferred to EC2, and redeployed.

The same Locust test configuration was used: ten simulated users, ramping up at two users per second.

**Results:**

| Metric                |    Result |
| --------------------- | --------: |
| Total requests        |       538 |
| Failures              |         0 |
| Average response time | 398.45 ms |
| Median response time  |    370 ms |
| 95th percentile       |    540 ms |
| 99th percentile       |    700 ms |
| Maximum response time |  1,487 ms |
| Throughput (RPS)      |       4.6 |

## 3. Performance Analysis

### 3.1 One Worker vs Two Workers

The results showed that the two-worker configuration performed better across most response-time measurements during the ten-user Locust test.

| Metric                | One Worker | Two Workers |
| --------------------- | ---------: | ----------: |
| Average response time |  435.61 ms |   398.45 ms |
| Median                |     380 ms |      370 ms |
| 95th percentile       |     740 ms |      540 ms |
| 99th percentile       |   1,100 ms |      700 ms |
| Maximum               |   1,430 ms |    1,487 ms |
| Throughput            |    4.2 RPS |     4.6 RPS |
| Failures              |         0% |          0% |

The two-worker configuration achieved:

* Approximately 8.5% lower average response time.
* Approximately 27% lower 95th-percentile response time.
* Approximately 36% lower 99th-percentile response time.
* Slightly higher throughput.

However, the maximum response time increased slightly.

These results suggest that additional worker capacity can improve request handling, although repeated controlled tests would be needed to establish a reliable performance difference.

### 3.2 Container Resource Consumption

Docker resource measurements were also collected.

| Configuration | Memory Usage | Memory Percentage | CPU Snapshot |
| ------------- | -----------: | ----------------: | -----------: |
| One worker    |    37.12 MiB |             4.08% |        0.01% |
| Two workers   |    53.49 MiB |             5.88% |        0.01% |

The two-worker configuration consumed approximately 16.37 MiB more memory than the one-worker configuration.

This is expected because additional worker processes require additional resources.

The measured memory consumption remained relatively small compared with the container's reported memory limit.

*Note: These were individual Docker statistics snapshots, not peak or average resource measurements throughout the load tests.*

### 3.3 Worker Timeout Investigation

During the investigation, Gunicorn logs revealed previous worker timeout events.

The logs included messages such as:

* `WORKER TIMEOUT`
* `Error handling request (no URI read)`
* Worker termination and replacement.

The configured Gunicorn timeout was 30 seconds.

Docker inspection reported `OOMKilled=false` for the running container. This did not establish that the earlier worker terminations were caused by memory exhaustion.

The exact cause of the earlier timeout events was not conclusively established.

After deploying the two-worker configuration, the latest log search found no matching timeout, error, or killed messages.

This investigation demonstrated the importance of examining application logs when investigating reliability problems.

## 4. Conclusion

The performance testing phase successfully established an initial performance baseline and demonstrated how changing the application server configuration affects application behaviour.

The Flask development server was replaced with Gunicorn, and Locust was used to simulate student traffic under different configurations.

The two-worker configuration produced better average and percentile response times than the one-worker configuration during the recorded ten-user test.

Both configurations completed their recorded tests without request failures.

Docker statistics also showed that the additional worker increased memory consumption, demonstrating the resource trade-off involved in increasing application concurrency.

### Key Engineering Lessons

This phase provided practical experience with:

* Deploying containerised applications on AWS EC2.
* Using Gunicorn to serve Flask applications.
* Understanding synchronous worker processes.
* Performing load tests with Locust.
* Interpreting response-time percentiles and requests per second.
* Monitoring Docker container resource consumption.
* Investigating application logs and worker timeout events.
* Comparing application configurations using measured results.

## 5. Limitations

The experiments had several limitations:

1. The application uses an in-memory Python dictionary rather than a production database.
2. The tests involved only one and ten simulated users.
3. The EC2 instance was a small `t3.micro` instance.
4. Network latency introduced variability into response-time measurements.
5. The one-worker and two-worker experiments were separate test runs, not perfectly controlled repeated experiments.
6. Docker resource measurements were snapshots rather than continuous monitoring.
7. The worker timeout investigation did not establish a definitive root cause.

Consequently, these results should not be interpreted as proof of production-scale capacity or guaranteed performance improvements.

## 6. Next Steps

The next phase will focus on Continuous Integration and Continuous Deployment (CI/CD).

Planned improvements include:

* Automating application testing with GitHub Actions.
* Building Docker images automatically.
* Publishing container images to Amazon Elastic Container Registry (ECR).
* Establishing an automated deployment workflow.

The longer-term objective is to develop a more reliable, observable, secure and scalable application infrastructure.
