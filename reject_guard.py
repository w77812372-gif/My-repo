#!/usr/bin/env python3
"""
BlockerHero Guard - GitHub Actions script (no pip packages needed).

Kaam:
  1. Partner Gmail ko IMAP se check karta hai (App Password se).
  2. BlockerHero ki unread request emails dhoondta hai.
  3. Agar request "allowed window" ke BAHAR aayi ho, ya high-risk ho
     (partner remove / turn off / disable), to Reject link khud hit karta hai.
  4. Allowed window ke andar normal request ko haath nahi lagata (manual review).

Ye script KABHI Accept link ko touch nahi karti.

Env variables:
  GMAIL_ADDRESS          partner Gmail address            (secret, zaroori)
  GMAIL_APP_PASSWORD     Gmail App Password               (secret, zaroori)
  GUARD_TZ               timezone, default Asia/Karachi
  GUARD_ALLOW_WINDOWS    manual-review windows, e.g. "11:00-13:40,19:00-20:00"
                         khali = hamesha reject
  GUARD_DRY_RUN          "1" = sirf log karo, link hit mat karo
  GUARD_SENDER           sender hint, default "blockerhero"
"""

import imaplib
import email
import os
import re
import sys
import urllib.error
import urllib.request
        if tag == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._text).strip()))
            self._href = None
            self._text = []


def get_parts(msg):
    html_parts, text_parts = [], []
    for part in msg.walk():
        ctype = part.get_content_type()
        if ctype not in ("text/html", "text/plain"):
            continue
        payload = part.get_payload(decode=True)
        if payload is None:
            continue
        charset = part.get_content_charset() or "utf-8"
        try:
            decoded = payload.decode(charset, errors="replace")
        except LookupError:
            decoded = payload.decode("utf-8", errors="replace")
        (html_parts if ctype == "text/html" else text_parts).append(decoded)
    return "\n".join(html_parts), "\n".join(text_parts)


def find_reject_link(html, text):
    candidates = []
    if html:
        parser = LinkParser()
        parser.feed(html)
        candidates.extend(parser.links)
    for url in re.findall(r"https?://[^\s<>\"']+", text or ""):
