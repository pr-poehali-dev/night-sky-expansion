import json
import os
import urllib.request

CHAT_ID = "@kvadronovo"


def handler(event: dict, context) -> dict:
    """Отправляет уведомление о бронировании в Telegram канал @kvadronovo"""

    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Max-Age": "86400",
            },
            "body": "",
        }

    body = json.loads(event.get("body") or "{}")
    name = body.get("name", "—")
    phone = body.get("phone", "—")
    date = body.get("date", "—")
    time = body.get("time", "—")
    message = body.get("message", "")

    text = (
        f"📅 Новая заявка на бронирование!\n\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📆 Дата: {date}\n"
        f"🕐 Время: {time}\n"
    )
    if message:
        text += f"💬 Пожелания: {message}\n"

    token = os.environ["TELEGRAM_BOT_TOKEN"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": CHAT_ID, "text": text}).encode()

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"ok": result.get("ok", False)}),
    }
