import re
import ipaddress
from urllib.parse import urlparse
import requests


SHORTENER_DOMAINS = {
    "bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co", "is.gd", "buff.ly",
    "adf.ly", "bit.do", "cutt.ly", "shorturl.at", "rebrand.ly", "tiny.cc",
    "lc.chat", "soo.gd", "s2r.co", "clicky.me", "rb.gy", "bl.ink"
}


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url


def get_parsed_url(url: str):
    return urlparse(normalize_url(url))


def get_hostname(url: str) -> str:
    parsed = get_parsed_url(url)
    return parsed.hostname if parsed.hostname else ""


def having_ip_address(url: str) -> int:
    hostname = get_hostname(url)
    try:
        ipaddress.ip_address(hostname)
        return -1
    except ValueError:
        return 1


def url_length(url: str) -> int:
    length = len(normalize_url(url))

    # Common phishing dataset style thresholds
    if length < 54:
        return 1
    elif 54 <= length <= 75:
        return 0
    else:
        return -1


def shortening_service(url: str) -> int:
    hostname = get_hostname(url).lower()
    return -1 if hostname in SHORTENER_DOMAINS else 1


def having_at_symbol(url: str) -> int:
    return -1 if "@" in url else 1


def double_slash_redirecting(url: str) -> int:
    normalized = normalize_url(url)
    protocol_index = normalized.find("//")
    remaining = normalized[protocol_index + 2:] if protocol_index != -1 else normalized
    return -1 if "//" in remaining else 1


def prefix_suffix(url: str) -> int:
    hostname = get_hostname(url)
    return -1 if "-" in hostname else 1


def having_sub_domain(url: str) -> int:
    hostname = get_hostname(url)

    if not hostname:
        return -1

    parts = hostname.split(".")

    # remove common www
    if parts and parts[0] == "www":
        parts = parts[1:]

    # basic assumption: last 2 parts are main domain + tld
    subdomain_count = max(len(parts) - 2, 0)

    if subdomain_count == 0:
        return 1
    elif subdomain_count == 1:
        return 0
    else:
        return -1


def https_token(url: str) -> int:
    hostname = get_hostname(url).lower()
    return -1 if "https" in hostname else 1


def abnormal_url(url: str) -> int:
    try:
        parsed = get_parsed_url(url)
        hostname = parsed.hostname

        if not hostname:
            return -1

        # malformed patterns
        if " " in url:
            return -1

        if parsed.scheme not in ["http", "https"]:
            return -1

        return 1

    except Exception:
        return -1


def redirect(url: str, timeout: int = 5) -> int:
    try:
        response = requests.get(
            normalize_url(url),
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        redirect_count = len(response.history)

        # dataset has 0 / 1
        return 1 if redirect_count > 1 else 0

    except Exception:
        return 0


def sslfinal_state(url: str, timeout: int = 5) -> int:
    normalized = normalize_url(url)
    parsed = get_parsed_url(normalized)

    try:
        response = requests.get(
            normalized,
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        final_url = response.url
        final_scheme = urlparse(final_url).scheme

        if final_scheme == "https":
            return 1
        elif parsed.scheme == "https":
            return 0
        else:
            return -1

    except requests.exceptions.SSLError:
        return -1
    except Exception:
        return 0


def extract_url_features(url: str) -> dict:
    normalized = normalize_url(url)

    features = {
        "having_IP_Address": having_ip_address(normalized),
        "URL_Length": url_length(normalized),
        "Shortining_Service": shortening_service(normalized),
        "having_At_Symbol": having_at_symbol(normalized),
        "double_slash_redirecting": double_slash_redirecting(normalized),
        "Prefix_Suffix": prefix_suffix(normalized),
        "having_Sub_Domain": having_sub_domain(normalized),
        "SSLfinal_State": sslfinal_state(normalized),
        "HTTPS_token": https_token(normalized),
        "Abnormal_URL": abnormal_url(normalized),
        "Redirect": redirect(normalized),
    }

    return features


if __name__ == "__main__":
    user_url = input("Enter URL: ").strip()
    features = extract_url_features(user_url)

    print("\nExtracted URL Features:")
    for key, value in features.items():
        print(f"{key}: {value}")