import allure
import requests

http_logs = []


def attach_http_log(response: requests.Response):
    request = response.request
    body = request.body
    if body is None:
        request_body = "-"
    elif isinstance(body, bytes):
        request_body = body.decode("utf-8", errors="replace")
    else:
        request_body = str(body)
    text = (
        f"{request.method} {request.url}\n"
        f"request body: {request_body}\n\n"
        f"status: {response.status_code}\n"
        f"response body: {response.text}\n"
        f"time: {response.elapsed.total_seconds()}s"
    )
    allure.attach(text, name="http log", attachment_type=allure.attachment_type.TEXT)
    http_logs.append(text)
