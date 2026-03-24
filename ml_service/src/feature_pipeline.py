from src.url_features import extract_url_features
from src.webpage_features import extract_webpage_features

FINAL_FEATURE_ORDER = [
    "having_IP_Address",
    "URL_Length",
    "Shortining_Service",
    "having_At_Symbol",
    "double_slash_redirecting",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "SSLfinal_State",
    "Favicon",
    "HTTPS_token",
    "Request_URL",
    "URL_of_Anchor",
    "Links_in_tags",
    "SFH",
    "Submitting_to_email",
    "Abnormal_URL",
    "Redirect",
    "on_mouseover",
    "RightClick",
    "popUpWidnow",
    "Iframe",
]


DEFAULT_FEATURE_VALUES = {
    "having_IP_Address": 1,
    "URL_Length": 1,
    "Shortining_Service": 1,
    "having_At_Symbol": 1,
    "double_slash_redirecting": 1,
    "Prefix_Suffix": 1,
    "having_Sub_Domain": 1,
    "SSLfinal_State": 0,
    "Favicon": 1,
    "HTTPS_token": 1,
    "Request_URL": 1,
    "URL_of_Anchor": 1,
    "Links_in_tags": 1,
    "SFH": 1,
    "Submitting_to_email": 1,
    "Abnormal_URL": 1,
    "Redirect": 0,
    "on_mouseover": 1,
    "RightClick": 1,
    "popUpWidnow": 1,
    "Iframe": 1,
}


def build_feature_dict(url: str) -> dict:
    final_features = DEFAULT_FEATURE_VALUES.copy()

    try:
        url_features = extract_url_features(url)
        final_features.update(url_features)
    except Exception as e:
        print(f"URL feature extraction error: {e}")

    try:
        webpage_features = extract_webpage_features(url)
        final_features.update(webpage_features)
    except Exception as e:
        print(f"Webpage feature extraction error: {e}")

    ordered_features = {
        feature: final_features.get(feature, DEFAULT_FEATURE_VALUES[feature])
        for feature in FINAL_FEATURE_ORDER
    }

    return ordered_features


def build_feature_list(url: str) -> list:
    feature_dict = build_feature_dict(url)
    return [feature_dict[feature] for feature in FINAL_FEATURE_ORDER]


if __name__ == "__main__":
    user_url = input("Enter URL: ").strip()

    feature_dict = build_feature_dict(user_url)

    print("\nFinal 21 Features:")
    for key, value in feature_dict.items():
        print(f"{key}: {value}")

    print("\nFeature List:")
    print(build_feature_list(user_url))