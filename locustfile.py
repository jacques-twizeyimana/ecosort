from locust import HttpUser, task, between
import os

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def predict(self):
        # Ensure we have a test image
        img_path = "test_image.jpg"
        if not os.path.exists(img_path):
            # Create a dummy image if not exists
            from PIL import Image
            img = Image.new('RGB', (224, 224), color = 'red')
            img.save(img_path)

        with open(img_path, "rb") as f:
            self.client.post("/predict", files={"file": f})
