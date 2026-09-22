import os
import urllib.parse
import webbrowser
import logging
import requests
from actions.screenshot import capture_screen

def send_to_telegram(image_path: str, bot_token: str, chat_id: str, caption: str = ""):
    """
    Directly uploads and sends a photo via Telegram Bot API to a user, group, or channel.
    Returns (success, message).
    """
    if not bot_token or not chat_id:
        return (False, "Telegram Bot Token or Chat ID not configured. Please configure in Settings.")

    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    try:
        with open(image_path, "rb") as photo_file:
            files = {"photo": photo_file}
            data = {"chat_id": chat_id}
            if caption:
                data["caption"] = caption
            response = requests.post(url, data=data, files=files, timeout=12)
            res_data = response.json()
            if res_data.get("ok"):
                return (True, f"Sent to Telegram ({chat_id}) successfully!")
            else:
                err_desc = res_data.get("description", "Unknown Telegram error")
                return (False, f"Telegram API Error: {err_desc}")
    except Exception as e:
        logging.error(f"Telegram dispatch failed: {e}")
        return (False, f"Connection error: {str(e)}")

def send_to_whatsapp(phone_number: str, caption: str = "Snapshot from Senior Officer Dashboard"):
    """
    Opens WhatsApp Web/App with the designated phone number and caption.
    Image is already copied to the clipboard, so recipient chat is opened ready for Ctrl+V.
    """
    # Clean phone number (strip spaces, dashes, parentheses)
    clean_phone = "".join(c for c in phone_number if c.isdigit() or c == "+")
    if clean_phone.startswith("+"):
        clean_phone = clean_phone[1:]

    encoded_caption = urllib.parse.quote(caption)
    if clean_phone:
        wa_url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={encoded_caption}"
    else:
        wa_url = f"https://web.whatsapp.com/"

    try:
        webbrowser.open(wa_url)
        return (True, f"WhatsApp opened for {clean_phone or 'Chat'}. Press Ctrl+V to attach snapshot.")
    except Exception as e:
        logging.error(f"WhatsApp launch failed: {e}")
        return (False, f"Failed to launch WhatsApp: {e}")

def execute_snap_and_dispatch(config: dict, hide_cb=None, restore_cb=None, target_mode="auto"):
    """
    Captures screen, then dispatches to configured destination.
    target_mode: 'auto', 'telegram', 'whatsapp'
    """
    # 1. Take Snapshot
    snap_res = capture_screen(hide_window_callback=hide_cb, restore_window_callback=restore_cb)
    if not snap_res.get("success"):
        return {"success": False, "message": "Failed to capture snapshot"}

    filepath = snap_res["filepath"]
    tg_cfg = config.get("telegram", {})
    wa_cfg = config.get("whatsapp", {})

    has_tg = bool(tg_cfg.get("bot_token") and tg_cfg.get("chat_id"))
    has_wa = bool(wa_cfg.get("default_phone"))

    results = []

    if target_mode in ("auto", "telegram"):
        if has_tg:
            tg_ok, tg_msg = send_to_telegram(
                filepath,
                tg_cfg["bot_token"],
                tg_cfg["chat_id"],
                caption="Executive Snapshot • Senior Officer Deck"
            )
            results.append(("Telegram", tg_ok, tg_msg))

    if target_mode in ("auto", "whatsapp") or (target_mode == "auto" and not has_tg):
        wa_ok, wa_msg = send_to_whatsapp(
            wa_cfg.get("default_phone", ""),
            wa_cfg.get("default_message", "Executive Snapshot")
        )
        results.append(("WhatsApp", wa_ok, wa_msg))

    if not results:
        return {
            "success": True,
            "filepath": filepath,
            "message": f"Snapshot saved & copied to clipboard! (Configure WhatsApp/Telegram in Settings)"
        }

    # Summarize result
    success_all = all(r[1] for r in results)
    summary = " • ".join(r[2] for r in results)
    return {
        "success": success_all,
        "filepath": filepath,
        "results": results,
        "message": summary
    }
