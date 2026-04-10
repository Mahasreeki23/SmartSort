#!/usr/bin/env python3

import socket
import ssl
import json
import base64
import os

# ---------------- CONFIG ----------------
HOST = "bitproduction.bitone.in"
PORT = 443
FUNCTION_NAME = "SmartSort"

# 👉 Change this to your test image path
IMAGE_PATH = "2026.jpg"


# ---------------- BIN MAPPING ----------------
def map_category_to_bin(category):
    category = category.lower().strip()

    if "metal" in category or "tweezer" in category:
        return 1
    elif "paper" in category:
        return 2
    elif "body" in category or "organic" in category or "gauze" in category:
        return 3
    elif "plastic" in category or "glove" in category or "mask" in category:
        return 4
    elif "needle" in category or "syringe" in category:
        return 5

    print("⚠️ Unknown category → default Bin 3")
    return 3


# ---------------- FAAS CALL ----------------
def send_to_faas(image_bytes):
    payload = {
        "image_b64": base64.b64encode(image_bytes).decode("utf-8")
    }

    body = json.dumps(payload)

    request = (
        f"POST /function/{FUNCTION_NAME} HTTP/1.1\r\n"
        f"Host: {HOST}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n\r\n"
        f"{body}"
    )

    print("📡 Connecting to SmartSort FAAS...\n")

    sock = socket.create_connection((HOST, PORT))
    context = ssl._create_unverified_context()
    ssock = context.wrap_socket(sock, server_hostname=HOST)

    ssock.sendall(request.encode())

    response = b""
    while True:
        data = ssock.recv(4096)
        if not data:
            break
        response += data

    ssock.close()

    response_text = response.decode(errors="ignore")

    try:
        _, body = response_text.split("\r\n\r\n", 1)
    except:
        print("❌ Invalid HTTP response")
        print(response_text)
        return

    print("📥 Raw Response:")
    print(body)

    try:
        result = json.loads(body)

        category = result.get("classification", "")
        confidence = result.get("confidence_percent", 0)

        print("\n🧠 Parsed Result:")
        print(f"Category   : {category}")
        print(f"Confidence : {confidence:.2f}%")

        bin_number = map_category_to_bin(category)

        print(f"\n🗑️ Final Bin → Bin {bin_number}")

    except Exception as e:
        print("❌ JSON parse error:", e)
        print(body)


# ---------------- MAIN ----------------
def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Image not found: {IMAGE_PATH}")
        return

    print("\n===== Local FAAS Test =====\n")

    with open(IMAGE_PATH, "rb") as f:
        image_bytes = f.read()

    send_to_faas(image_bytes)


if __name__ == "__main__":
    main()
