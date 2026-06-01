"""Generate one visual aid image from an image-prompts.json manifest.

This script calls the OpenAI Images API through the official ``openai`` package,
reads a prompt entry by id, and saves the returned base64 image to the
manifest's filename/path.
"""

from __future__ import annotations

import argparse
import base64
from contextlib import ExitStack
import json
import os
import sys
from pathlib import Path
from typing import Any

from openai import OpenAI


DEFAULT_MODEL = "gpt-image-1.5"
DEFAULT_OUTPUT_ROOT = Path("media") / "img" / "visual_aids"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate visual aid images from an image-prompts.json manifest."
    )
    parser.add_argument(
        "manifest",
        type=Path,
        help="Path to image-prompts.json.",
    )

    selection = parser.add_argument_group("selection")
    selection.add_argument("--id", help="Prompt id to generate.")
    selection.add_argument(
        "--index",
        type=int,
        help="Zero-based prompt index to generate. Useful if ids are inconvenient.",
    )
    selection.add_argument(
        "--first-missing",
        action="store_true",
        help="Generate the first prompt whose output file does not exist.",
    )

    listing = parser.add_argument_group("listing")
    listing.add_argument(
        "--list-ids",
        action="store_true",
        help="Print all ids in the manifest.",
    )
    listing.add_argument(
        "--list-generated",
        action="store_true",
        help="Print ids whose output files already exist.",
    )
    listing.add_argument(
        "--list-missing",
        action="store_true",
        help="Print ids whose output files do not exist yet.",
    )
    listing.add_argument(
        "--status",
        action="store_true",
        help="Print each id with generated/missing status and output path.",
    )

    output = parser.add_argument_group("output")
    output.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help=(
            "Root directory for manifest visual_aid_path values. "
            f"Default: {DEFAULT_OUTPUT_ROOT}"
        ),
    )
    output.add_argument(
        "--output-dir",
        type=Path,
        help=(
            "Fallback directory when an entry has no visual_aid_path. "
            "Defaults to the manifest directory."
        ),
    )
    output.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite an existing output file.",
    )
    output.add_argument(
        "--save-prompt",
        action="store_true",
        help="Save the final prompt beside the image as .prompt.txt.",
    )
    output.add_argument(
        "--save-response",
        action="store_true",
        help="Save a redacted API response beside the image as .response.json.",
    )
    output.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be generated without calling the API.",
    )

    api = parser.add_argument_group("api")
    api.add_argument(
        "--model",
        default=os.environ.get("OPENAI_IMAGE_MODEL", DEFAULT_MODEL),
        help=f"OpenAI image model. Default: {DEFAULT_MODEL}",
    )
    api.add_argument(
        "--quality",
        default="medium",
        choices=("auto", "low", "medium", "high"),
        help="Image quality. Default: medium.",
    )
    api.add_argument(
        "--size",
        choices=("auto", "1024x1024", "1536x1024", "1024x1536"),
        help="Output size. Defaults from aspect_ratio when possible.",
    )
    api.add_argument(
        "--background",
        choices=("auto", "opaque", "transparent"),
        default=None,
        help="Background mode, if supported by the selected model.",
    )
    api.add_argument(
        "--output-format",
        choices=("png", "jpeg", "webp"),
        default="png",
        help="Saved file format request. Default: png.",
    )
    api.add_argument(
        "--prompt-prefix",
        default="",
        help="Text to prepend to the manifest prompt.",
    )
    api.add_argument(
        "--prompt-suffix",
        default="",
        help="Text to append to the manifest prompt.",
    )
    api.add_argument(
        "--reference-image",
        action="append",
        type=Path,
        default=[],
        help=(
            "Reference image to pass to the image edits endpoint. "
            "Can be supplied multiple times. Without this option, the script "
            "uses normal text-only image generation."
        ),
    )
    api.add_argument(
        "--input-fidelity",
        choices=("low", "high"),
        default=None,
        help="Reference image fidelity for image edits, if supported by the model.",
    )
    api.add_argument(
        "--timeout",
        type=float,
        default=180.0,
        help="API request timeout in seconds. Default: 180.",
    )
    api.add_argument(
        "--retries",
        type=int,
        default=2,
        help="SDK retry count for transient API failures. Default: 2.",
    )
    api.add_argument(
        "--api-key-env",
        default="OPENAI_API_KEY",
        help="Environment variable containing the OpenAI API key.",
    )

    return parser.parse_args()


def load_manifest(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Manifest must be a JSON list of prompt entries.")

    seen: set[str] = set()
    entries: list[dict[str, Any]] = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Manifest entry {index} is not an object.")
        prompt_id = item.get("id")
        prompt = item.get("prompt")
        if not isinstance(prompt_id, str) or not prompt_id.strip():
            raise ValueError(f"Manifest entry {index} is missing a string id.")
        if prompt_id in seen:
            raise ValueError(f"Duplicate prompt id: {prompt_id}")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError(f"Manifest entry {prompt_id!r} is missing a prompt.")
        seen.add(prompt_id)
        entries.append(item)
    return entries


def output_path_for(
    entry: dict[str, Any],
    output_root: Path,
    output_dir: Path | None,
    manifest_path: Path,
) -> Path:
    visual_aid_path = entry.get("visual_aid_path")
    if isinstance(visual_aid_path, str) and visual_aid_path.strip():
        return output_root / Path(visual_aid_path)

    filename = entry.get("filename")
    if not isinstance(filename, str) or not filename.strip():
        filename = f"{entry['id']}.png"
    return (output_dir or manifest_path.parent) / filename


def status_for_entries(
    entries: list[dict[str, Any]],
    output_root: Path,
    output_dir: Path | None,
    manifest_path: Path,
) -> list[tuple[str, bool, Path]]:
    rows = []
    for entry in entries:
        path = output_path_for(entry, output_root, output_dir, manifest_path)
        rows.append((entry["id"], path.exists(), path))
    return rows


def print_listing(args: argparse.Namespace, entries: list[dict[str, Any]]) -> bool:
    rows = status_for_entries(
        entries,
        args.output_root,
        args.output_dir,
        args.manifest,
    )
    did_list = False

    if args.list_ids:
        for entry in entries:
            print(entry["id"])
        did_list = True

    if args.list_generated:
        for prompt_id, exists, _path in rows:
            if exists:
                print(prompt_id)
        did_list = True

    if args.list_missing:
        for prompt_id, exists, _path in rows:
            if not exists:
                print(prompt_id)
        did_list = True

    if args.status:
        for prompt_id, exists, path in rows:
            label = "generated" if exists else "missing"
            print(f"{label:9} {prompt_id:32} {path}")
        did_list = True

    return did_list


def choose_entry(args: argparse.Namespace, entries: list[dict[str, Any]]) -> dict[str, Any]:
    selectors = [args.id is not None, args.index is not None, args.first_missing]
    if sum(selectors) != 1:
        raise ValueError("Choose exactly one of --id, --index, or --first-missing.")

    if args.id is not None:
        for entry in entries:
            if entry["id"] == args.id:
                return entry
        raise ValueError(f"No prompt id found: {args.id}")

    if args.index is not None:
        if args.index < 0 or args.index >= len(entries):
            raise ValueError(f"--index must be between 0 and {len(entries) - 1}.")
        return entries[args.index]

    for entry in entries:
        out = output_path_for(entry, args.output_root, args.output_dir, args.manifest)
        if not out.exists():
            return entry
    raise ValueError("No missing output files found.")


def size_for_entry(entry: dict[str, Any], size_override: str | None) -> str:
    if size_override:
        return size_override
    aspect_ratio = str(entry.get("aspect_ratio", "")).strip()
    if aspect_ratio in {"16:9", "3:2", "landscape"}:
        return "1536x1024"
    if aspect_ratio in {"9:16", "2:3", "3:4", "portrait"}:
        return "1024x1536"
    if aspect_ratio in {"1:1", "square"}:
        return "1024x1024"
    return "auto"


def final_prompt(entry: dict[str, Any], prefix: str, suffix: str) -> str:
    parts = [prefix.strip(), entry["prompt"].strip(), suffix.strip()]
    return "\n\n".join(part for part in parts if part)


def validate_reference_images(paths: list[Path]) -> list[Path]:
    validated = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Reference image not found: {path}")
        if not path.is_file():
            raise ValueError(f"Reference image is not a file: {path}")
        validated.append(path)
    return validated


def response_to_dict(response: Any) -> dict[str, Any]:
    if hasattr(response, "model_dump"):
        return response.model_dump(mode="json")
    if hasattr(response, "to_dict"):
        return response.to_dict()
    if hasattr(response, "to_dict_recursive"):
        return response.to_dict_recursive()
    if hasattr(response, "json"):
        return json.loads(response.json())
    raise TypeError("Could not convert OpenAI response to a dictionary.")


def request_image(
    *,
    api_key: str,
    model: str,
    prompt: str,
    reference_images: list[Path],
    input_fidelity: str | None,
    size: str,
    quality: str,
    background: str | None,
    output_format: str,
    timeout: int,
    retries: int,
) -> dict[str, Any]:
    client = OpenAI(api_key=api_key, timeout=timeout, max_retries=retries)
    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality,
        "output_format": output_format,
    }
    if background is not None:
        payload["background"] = background

    if reference_images:
        with ExitStack() as stack:
            files = [stack.enter_context(path.open("rb")) for path in reference_images]
            payload["image"] = files[0] if len(files) == 1 else files
            if input_fidelity is not None:
                payload["input_fidelity"] = input_fidelity
            response = client.images.edit(**payload)
    else:
        response = client.images.generate(**payload)
    return response_to_dict(response)


def extract_b64_image(response: dict[str, Any]) -> str:
    data = response.get("data")
    if not isinstance(data, list) or not data:
        raise ValueError("API response did not include a data array.")

    first = data[0]
    if not isinstance(first, dict):
        raise ValueError("API response data[0] was not an object.")

    b64_json = first.get("b64_json")
    if not isinstance(b64_json, str) or not b64_json:
        raise ValueError("API response did not include data[0].b64_json.")
    return b64_json


def redacted_response(response: dict[str, Any]) -> dict[str, Any]:
    copy = json.loads(json.dumps(response))
    for item in copy.get("data", []):
        if isinstance(item, dict) and "b64_json" in item:
            item["b64_json"] = f"<redacted {len(item['b64_json'])} chars>"
    return copy


def main() -> int:
    args = parse_args()
    try:
        entries = load_manifest(args.manifest)

        did_list = print_listing(args, entries)
        if did_list and not (args.id or args.index is not None or args.first_missing):
            return 0

        entry = choose_entry(args, entries)
        out_path = output_path_for(entry, args.output_root, args.output_dir, args.manifest)
        prompt = final_prompt(entry, args.prompt_prefix, args.prompt_suffix)
        size = size_for_entry(entry, args.size)
        reference_images = validate_reference_images(args.reference_image)

        if out_path.exists() and not args.overwrite:
            raise FileExistsError(f"Output already exists. Use --overwrite: {out_path}")

        print(f"id:      {entry['id']}")
        print(f"mode:    {'edit' if reference_images else 'generate'}")
        print(f"model:   {args.model}")
        print(f"size:    {size}")
        print(f"quality: {args.quality}")
        print(f"output:  {out_path}")
        for reference_image in reference_images:
            print(f"ref:     {reference_image}")
        if args.dry_run:
            print("\nPrompt:\n")
            print(prompt)
            return 0

        api_key = os.environ.get(args.api_key_env)
        if not api_key:
            raise EnvironmentError(f"Set {args.api_key_env} before generating images.")
        api_key = api_key.strip()

        response = request_image(
            api_key=api_key,
            model=args.model,
            prompt=prompt,
            reference_images=reference_images,
            input_fidelity=args.input_fidelity,
            size=size,
            quality=args.quality,
            background=args.background,
            output_format=args.output_format,
            timeout=args.timeout,
            retries=args.retries,
        )

        image_bytes = base64.b64decode(extract_b64_image(response))
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(image_bytes)
        print(f"saved:   {out_path}")

        if args.save_prompt:
            prompt_path = out_path.with_suffix(out_path.suffix + ".prompt.txt")
            prompt_path.write_text(prompt, encoding="utf-8")
            print(f"prompt:  {prompt_path}")

        if args.save_response:
            response_path = out_path.with_suffix(out_path.suffix + ".response.json")
            response_path.write_text(
                json.dumps(redacted_response(response), indent=2),
                encoding="utf-8",
            )
            print(f"response:{response_path}")

        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
