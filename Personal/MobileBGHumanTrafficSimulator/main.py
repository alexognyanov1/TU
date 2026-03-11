from locust import HttpUser, task, between
import random


class WebsiteUser(HttpUser):
    wait_time = between(3, 15)

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0"
    ]

    @task
    def visit_page(self):
        headers = {
            "User-Agent": random.choice(self.user_agents)
        }

        self.client.get(
            "/obiava-11772914613643374-mercedes-benz-e-500-w211",
            headers=headers
        )
