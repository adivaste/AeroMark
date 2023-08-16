from urllib.parse import urlparse

def extract_site_name(url):
    parsed_url = urlparse(url)
    site_name = parsed_url.netloc

    if site_name.startswith('www.'):
        site_name = site_name[4:]

    return site_name

# # Example usage
# url = "https://www.youtube.com/watch?v=6xoB4ZiKKn0&list=RDMMRiZL2j5mIPw&index=23"
# site_name = extract_site_name(url)
# print(site_name)  # Output: youtube.com
