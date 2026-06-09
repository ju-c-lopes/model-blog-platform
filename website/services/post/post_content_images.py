import re
import shutil
from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.utils.text import get_valid_filename

POST_CONTENT_DIR = "post_content"
TEMP_DIR = "_tmp"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024


def _media_root() -> Path:
    return Path(settings.MEDIA_ROOT)


def _validate_session_id(session_id: str) -> str:
    if not session_id or not re.fullmatch(r"[a-f0-9-]{36}", session_id, re.IGNORECASE):
        raise ValueError("Identificador de sessão de upload inválido.")
    return session_id


def _validate_slug(slug: str) -> str:
    if not slug or not re.fullmatch(r"[a-z0-9-]+", slug):
        raise ValueError("Slug inválido para armazenamento de imagem.")
    return slug


def _safe_filename(original_name: str) -> str:
    sanitized = get_valid_filename(original_name or "image.jpg")
    path = Path(sanitized)
    extension = path.suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        extension = ".jpg"
    stem = path.stem or "image"
    max_stem_len = 200 - len(extension)
    if len(stem) > max_stem_len:
        stem = stem[:max_stem_len]
    return f"{stem}{extension}"


def _available_filename(directory: Path, filename: str) -> str:
    if not (directory / filename).exists():
        return filename

    path = Path(filename)
    stem, extension = path.stem, path.suffix
    counter = 2
    while (directory / f"{stem}-{counter}{extension}").exists():
        counter += 1
    return f"{stem}-{counter}{extension}"


def build_media_url(relative_path: str) -> str:
    relative = relative_path.replace("\\", "/").lstrip("/")
    return f"{settings.MEDIA_URL.rstrip('/')}/{relative}"


def temp_relative_dir(session_id: str) -> str:
    session_id = _validate_session_id(session_id)
    return f"{POST_CONTENT_DIR}/{TEMP_DIR}/{session_id}"


def post_relative_dir(slug: str) -> str:
    slug = _validate_slug(slug)
    return f"{POST_CONTENT_DIR}/{slug}"


def save_content_image(
    uploaded_file: UploadedFile,
    *,
    session_id: str | None = None,
    slug: str | None = None,
) -> str:
    if uploaded_file.size > MAX_IMAGE_SIZE_BYTES:
        raise ValueError("A imagem deve ter no máximo 5 MB.")

    extension = Path(uploaded_file.name or "").suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError("Formato de imagem não suportado. Use JPG, PNG, GIF ou WebP.")

    filename = _safe_filename(uploaded_file.name or "image.jpg")
    if slug:
        relative_dir = post_relative_dir(slug)
    elif session_id:
        relative_dir = temp_relative_dir(session_id)
    else:
        raise ValueError("Informe session_id (criação) ou slug (edição).")

    target_dir = _media_root() / relative_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = _available_filename(target_dir, filename)

    relative_path = f"{relative_dir}/{filename}"
    saved_path = default_storage.save(relative_path, uploaded_file)
    return build_media_url(saved_path)


def consolidate_temp_images(html: str, session_id: str, slug: str) -> str:
    if not html:
        return html

    session_id = _validate_session_id(session_id)
    slug = _validate_slug(slug)

    temp_relative = temp_relative_dir(session_id)
    dest_relative = post_relative_dir(slug)
    temp_dir = _media_root() / temp_relative
    dest_dir = _media_root() / dest_relative

    if not temp_dir.exists():
        return html

    dest_dir.mkdir(parents=True, exist_ok=True)
    updated_html = html

    for file_path in sorted(temp_dir.iterdir()):
        if not file_path.is_file():
            continue

        destination_name = _available_filename(dest_dir, file_path.name)
        destination = dest_dir / destination_name

        shutil.move(str(file_path), str(destination))

        old_url = build_media_url(f"{temp_relative}/{file_path.name}")
        new_url = build_media_url(f"{dest_relative}/{destination.name}")
        updated_html = updated_html.replace(old_url, new_url)

    shutil.rmtree(temp_dir, ignore_errors=True)
    return updated_html
