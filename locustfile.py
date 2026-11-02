from locust import HttpUser, task, between

class StudentUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def visit_portal(self):
        self.client.get("/")

    @task(1)
    def check_results(self):
        self.client.post(
            "/",
            data={"student_id": "STU001"}
        )