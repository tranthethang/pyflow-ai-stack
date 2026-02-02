import asyncio
import os

import requests
from dotenv import load_dotenv

from app.core.config import Config
from app.services.gemini_service import gemini_service
from app.services.redis_service import redis_service
from app.services.s3_service import s3_service

load_dotenv()

APP_PORT = os.getenv("APP_PORT", "80")
BASE_URL = f"http://127.0.0.1:{APP_PORT}"


def test_health():
    print("\n[*] Testing Health Check (HTTP)...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"[+] Health check response: {response.json()}")
    except Exception as e:
        print(f"[-] Health check failed: {e}")


def test_api_gemini():
    print("\n[*] Testing Gemini API Endpoint (HTTP)...")
    payload = {
        "project_id": "verify-test",
        "tasks": [{"task_id": "1", "prompt": "Say 'Gemini is working'"}],
    }
    try:
        response = requests.post(f"{BASE_URL}/api/v1/run", json=payload)
        print(f"[+] API response: {response.json()}")
    except Exception as e:
        print(f"[-] API test failed: {e}")


async def verify_redis():
    print("\n[*] Verifying Redis Connection (Direct)...")
    try:
        status = await redis_service.ping()
        if status:
            print("[+] Redis is CONNECTED")
        else:
            print("[-] Redis is DISCONNECTED")
    except Exception as e:
        print(f"[-] Redis verification failed: {e}")


async def verify_gemini():
    print("\n[*] Verifying Gemini Service (Direct)...")
    try:
        result = await gemini_service.generate_content("Hello, are you active?")
        if result:
            print(f"[+] Gemini is ACTIVE. Response length: {len(result)}")
        else:
            print("[-] Gemini returned empty response")
    except Exception as e:
        print(f"[-] Gemini verification failed: {e}")


async def verify_s3():
    print("\n[*] Verifying S3 Storage (Direct)...")
    test_key = "verify_test.txt"
    test_content = "Connection test"
    try:
        # Test Upload
        await s3_service.upload_file(test_content, test_key)
        print("[+] S3 Upload: SUCCESS")

        # Test Download
        downloaded = await s3_service.get_file(test_key)
        if downloaded == test_content:
            print("[+] S3 Download: SUCCESS")
        else:
            print("[-] S3 Download: DATA MISMATCH")

        print("[+] S3 is CONNECTED and FUNCTIONAL")
    except Exception as e:
        print(f"[-] S3 verification failed: {str(e)}")


async def main():
    print(f"=== Starting Verification for {Config.APP_NAME} ===")

    # 1. Direct Service Checks
    await verify_redis()
    await verify_gemini()
    await verify_s3()

    # 2. HTTP API Checks (Requires the app to be running)
    print("\n--- HTTP API Checks ---")
    print("(Make sure the app is running via 'sh start.sh' first)")
    test_health()
    test_api_gemini()

    print("\n=== Verification Finished ===")


if __name__ == "__main__":
    asyncio.run(main())
