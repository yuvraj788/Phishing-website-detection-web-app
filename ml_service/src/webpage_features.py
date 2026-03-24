import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


USER_AGENT = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url


def get_domain(url: str) -> str:
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except Exception:
        return ""


def is_internal_link(link: str, base_domain: str) -> bool:
    if not link:
        return True

    link = link.strip().lower()

    if link.startswith(("#", "/", "javascript:void(0)", "javascript:;", "mailto:")):
        return True

    parsed = urlparse(link)

    if not parsed.netloc:
        return True

    return base_domain in parsed.netloc.lower()


def fetch_webpage(url: str, timeout: int = 8):
    normalized = normalize_url(url)

    try:
        response = requests.get(
            normalized,
            headers=USER_AGENT,
            timeout=timeout,
            allow_redirects=True,
            verify=True
        )
        final_url = response.url
        soup = BeautifulSoup(response.text, "html.parser")

        return {
            "success": True,
            "normalized_url": normalized,
            "final_url": final_url,
            "html": response.text,
            "soup": soup,
            "status_code": response.status_code
        }

    except Exception:
        return {
            "success": False,
            "normalized_url": normalized,
            "final_url": normalized,
            "html": "",
            "soup": None,
            "status_code": None
        }


def favicon_feature(soup, final_url: str) -> int:
    if soup is None:
        return 1

    base_domain = get_domain(final_url)

    icon_links = soup.find_all("link", rel=True)

    for tag in icon_links:
        rel_value = " ".join(tag.get("rel", [])).lower()
        if "icon" in rel_value:
            href = tag.get("href", "").strip()
            if not href:
                continue

            full_href = urljoin(final_url, href)
            return 1 if is_internal_link(full_href, base_domain) else -1

    return 1


def request_url_feature(soup, final_url: str) -> int:
    if soup is None:
        return 1

    base_domain = get_domain(final_url)
    resource_links = []

    for tag in soup.find_all(["img", "audio", "embed", "iframe", "script", "source"]):
        src = tag.get("src")
        if src:
            resource_links.append(urljoin(final_url, src))

    for tag in soup.find_all("link"):
        href = tag.get("href")
        if href:
            resource_links.append(urljoin(final_url, href))

    if not resource_links:
        return 1

    external_count = sum(
        1 for link in resource_links if not is_internal_link(link, base_domain)
    )
    ratio = external_count / len(resource_links)

    if ratio < 0.22:
        return 1
    elif ratio <= 0.61:
        return 0
    else:
        return -1


def url_of_anchor_feature(soup, final_url: str) -> int:
    if soup is None:
        return 1

    base_domain = get_domain(final_url)
    anchors = soup.find_all("a")

    if not anchors:
        return 1

    unsafe_count = 0

    for tag in anchors:
        href = (tag.get("href") or "").strip().lower()

        if href in ("", "#", "#content", "#skip", "javascript:void(0)", "javascript:;"):
            unsafe_count += 1
            continue

        full_href = urljoin(final_url, href)

        if not is_internal_link(full_href, base_domain):
            unsafe_count += 1

    ratio = unsafe_count / len(anchors)

    if ratio < 0.31:
        return 1
    elif ratio <= 0.67:
        return 0
    else:
        return -1


def links_in_tags_feature(soup, final_url: str) -> int:
    if soup is None:
        return 1

    base_domain = get_domain(final_url)
    links = []

    for tag in soup.find_all("link"):
        href = tag.get("href")
        if href:
            links.append(urljoin(final_url, href))

    for tag in soup.find_all("script"):
        src = tag.get("src")
        if src:
            links.append(urljoin(final_url, src))

    for tag in soup.find_all("meta"):
        content = tag.get("content", "")
        if "http" in content.lower():
            links.append(content.strip())

    if not links:
        return 1

    external_count = sum(
        1 for link in links if not is_internal_link(link, base_domain)
    )
    ratio = external_count / len(links)

    if ratio < 0.17:
        return 1
    elif ratio <= 0.81:
        return 0
    else:
        return -1


def sfh_feature(soup, final_url: str) -> int:
    if soup is None:
        return 1

    base_domain = get_domain(final_url)
    forms = soup.find_all("form")

    if not forms:
        return 1

    for form in forms:
        action = (form.get("action") or "").strip().lower()

        if action == "" or action == "about:blank":
            return -1

        full_action = urljoin(final_url, action)

        if not is_internal_link(full_action, base_domain):
            return 0

    return 1


def submitting_to_email_feature(soup) -> int:
    if soup is None:
        return 1

    html_text = str(soup).lower()

    if "mailto:" in html_text:
        return -1

    return 1


def on_mouseover_feature(soup) -> int:
    if soup is None:
        return 1

    html_text = str(soup).lower()

    suspicious_patterns = [
        "onmouseover",
        "window.status",
        "status="
    ]

    return -1 if any(pattern in html_text for pattern in suspicious_patterns) else 1


def rightclick_feature(soup) -> int:
    if soup is None:
        return 1

    html_text = str(soup).lower()

    suspicious_patterns = [
        "event.button==2",
        "event.button == 2",
        "contextmenu",
        "return false"
    ]

    return -1 if any(pattern in html_text for pattern in suspicious_patterns) else 1


def popupwindow_feature(soup) -> int:
    if soup is None:
        return 1

    html_text = str(soup).lower()

    suspicious_patterns = [
        "window.open(",
        "alert(",
        "prompt("
    ]

    return -1 if any(pattern in html_text for pattern in suspicious_patterns) else 1


def iframe_feature(soup) -> int:
    if soup is None:
        return 1

    iframes = soup.find_all("iframe")
    return -1 if len(iframes) > 0 else 1


def extract_webpage_features(url: str) -> dict:
    page_data = fetch_webpage(url)
    soup = page_data["soup"]
    final_url = page_data["final_url"]

    features = {
        "Favicon": favicon_feature(soup, final_url),
        "Request_URL": request_url_feature(soup, final_url),
        "URL_of_Anchor": url_of_anchor_feature(soup, final_url),
        "Links_in_tags": links_in_tags_feature(soup, final_url),
        "SFH": sfh_feature(soup, final_url),
        "Submitting_to_email": submitting_to_email_feature(soup),
        "on_mouseover": on_mouseover_feature(soup),
        "RightClick": rightclick_feature(soup),
        "popUpWidnow": popupwindow_feature(soup),
        "Iframe": iframe_feature(soup),
    }

    return features


if __name__ == "__main__":
    user_url = input("Enter URL: ").strip()
    features = extract_webpage_features(user_url)

    print("\nExtracted Webpage Features:")
    for key, value in features.items():
        print(f"{key}: {value}")