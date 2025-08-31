"""
YouTube URL validation and sanitization utilities
Provides secure handling of YouTube video URLs for embedding
"""

import re


def extract_youtube_video_id(url):
    """
    Extract YouTube video ID from various YouTube URL formats

    Args:
        url (str): YouTube URL

    Returns:
        str: Video ID if valid, None otherwise
    """
    if not url or not isinstance(url, str):
        return None

    url = url.strip()

    # Common YouTube URL patterns
    patterns = [
        r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
        r"(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})",
        r"(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})",
        r"(?:https?://)?(?:www\.)?youtube-nocookie\.com/embed/([a-zA-Z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            # Validate video ID format (exactly 11 characters, alphanumeric + _ -)
            if re.match(r"^[a-zA-Z0-9_-]{11}$", video_id):
                return video_id

    return None


def validate_youtube_url(url):
    """
    Validate if a URL is a valid YouTube URL

    Args:
        url (str): URL to validate

    Returns:
        bool: True if valid YouTube URL, False otherwise
    """
    video_id = extract_youtube_video_id(url)
    return video_id is not None


def create_secure_embed_url(video_id):
    """
    Create a secure YouTube embed URL using youtube-nocookie.com

    Args:
        video_id (str): YouTube video ID

    Returns:
        str: Secure embed URL
    """
    if not video_id or not re.match(r"^[a-zA-Z0-9_-]{11}$", video_id):
        raise ValueError("Invalid YouTube video ID")

    return f"https://www.youtube-nocookie.com/embed/{video_id}"


def sanitize_youtube_content(content):
    """
    Sanitize HTML content to ensure only secure YouTube embeds are allowed

    Args:
        content (str): HTML content

    Returns:
        str: Sanitized content with secure YouTube embeds
    """
    # This is a basic implementation - in production, consider using
    # a more robust HTML sanitization library like bleach

    # Pattern to match YouTube iframe elements
    youtube_pattern = (
        r'<iframe[^>]*src=["\']https://(?:www\.)?youtube(?:-nocookie)?\.com/'
        r'embed/([a-zA-Z0-9_-]{11})[^"\']*["\'][^>]*></iframe>'
    )

    def replace_youtube_iframe(match):
        video_id = match.group(1)
        if re.match(r"^[a-zA-Z0-9_-]{11}$", video_id):
            # Create secure iframe
            secure_url = create_secure_embed_url(video_id)
            return (
                f'<iframe src="{secure_url}" frameborder="0" '
                f'allow="accelerometer; autoplay; clipboard-write; '
                f'encrypted-media; gyroscope; picture-in-picture" '
                f'allowfullscreen loading="lazy"></iframe>'
            )
        return ""  # Remove invalid iframes

    return re.sub(youtube_pattern, replace_youtube_iframe, content)


# Example usage:
if __name__ == "__main__":
    # Test URLs
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "invalid-url",
        "https://not-youtube.com/watch?v=dQw4w9WgXcQ",
    ]

    for test_url in test_urls:
        test_video_id = extract_youtube_video_id(test_url)
        is_valid = validate_youtube_url(test_url)
        print(f"URL: {test_url}")
        print(f"Video ID: {test_video_id}")
        print(f"Valid: {is_valid}")
        if test_video_id:
            print(f"Secure Embed: {create_secure_embed_url(test_video_id)}")
        print("-" * 50)
