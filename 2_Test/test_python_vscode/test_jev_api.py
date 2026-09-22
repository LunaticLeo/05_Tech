#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch-test OpenJEV on CAD Part-Pair mate classification.

Input:
  jev_part_pairs.jsonl
Ground truth (optional):
  jev_part_pairs_ground_truth.jsonl

Each input line is one OpenJEV request with:
  - state.partA
  - state.partB
  - questions.concentric
  - questions.coincident

Usage (PowerShell):
  $env:OPENJEV_API_KEY="your_key_here"
  python test_jev_api.py --input jev_part_pairs.jsonl --gt jev_part_pairs_ground_truth.jsonl --limit 1

Then run all:
  python test_jev_api.py --input jev_part_pairs.jsonl --gt jev_part_pairs_ground_truth.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests


DEFAULT_ENDPOINT = "https://api.openjev.sh/v1/systemone"
DEFAULT_THRESHOLD = 0.5


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"{path}:{lineno}: invalid JSON: {e}") from e
    return rows


def load_ground_truth(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    return {row["sample_id"]: row for row in load_jsonl(path)}


def call_jev(
    session: requests.Session,
    endpoint: str,
    api_key: str,
    request_obj: dict[str, Any],
    timeout: float,
    retries: int,
) -> dict[str, Any]:
    """
    Send one OpenJEV request.

    sample_id is our local bookkeeping field and is NOT part of OpenJEV's API schema,
    so it is removed before sending.
    """
    payload = {
        "model": request_obj.get("model", "openjev"),
        "state": request_obj["state"],
        "questions": request_obj["questions"],
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    last_error: Exception | None = None

    for attempt in range(retries + 1):
        try:
            response = session.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=timeout,
            )

            # Retry transient errors.
            if response.status_code in (429, 500, 502, 503, 504):
                if attempt < retries:
                    wait_s = min(2 ** attempt, 8)
                    print(
                        f"  transient HTTP {response.status_code}; retry in {wait_s}s...",
                        file=sys.stderr,
                    )
                    time.sleep(wait_s)
                    continue

            if response.status_code == 401:
                raise RuntimeError(
                    "HTTP 401: invalid/missing OpenJEV API key."
                )

            if response.status_code == 422:
                raise RuntimeError(
                    "HTTP 422: OpenJEV rejected the request body.\n"
                    f"Response: {response.text[:4000]}"
                )

            response.raise_for_status()

            result = response.json()
            if "answers" not in result:
                raise RuntimeError(
                    f"OpenJEV response has no 'answers': {json.dumps(result, ensure_ascii=False)[:4000]}"
                )
            return result

        except (requests.RequestException, ValueError, RuntimeError) as e:
            last_error = e
            if attempt < retries and not (
                isinstance(e, RuntimeError)
                and ("HTTP 401" in str(e) or "HTTP 422" in str(e))
            ):
                wait_s = min(2 ** attempt, 8)
                print(f"  request failed: {e}; retry in {wait_s}s...", file=sys.stderr)
                time.sleep(wait_s)
                continue
            raise

    assert last_error is not None
    raise last_error


def get_noul(result: dict[str, Any], question_id: str) -> float | None:
    answer = result.get("answers", {}).get(question_id)
    if not isinstance(answer, dict):
        return None
    value = answer.get("noul")
    if isinstance(value, (int, float)):
        return float(value)
    return None


def update_binary_stats(
    stats: dict[str, dict[str, int]],
    label: str,
    truth: bool,
    prob: float,
    threshold: float,
) -> None:
    pred = prob >= threshold
    s = stats[label]

    if pred and truth:
        s["tp"] += 1
    elif pred and not truth:
        s["fp"] += 1
    elif not pred and truth:
        s["fn"] += 1
    else:
        s["tn"] += 1


def metrics(s: dict[str, int]) -> dict[str, float]:
    tp, fp, fn, tn = s["tp"], s["fp"], s["fn"], s["tn"]
    n = tp + fp + fn + tn
    accuracy = (tp + tn) / n if n else 0.0
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Batch-test OpenJEV on CAD part-pair mate classification."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("jev_part_pairs.jsonl"),
        help="Input JSONL generated for OpenJEV.",
    )
    parser.add_argument(
        "--gt",
        type=Path,
        default=None,
        help="Optional ground-truth JSONL.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("jev_results.jsonl"),
        help="Where to save raw + parsed results.",
    )
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help=f"OpenJEV endpoint (default: {DEFAULT_ENDPOINT})",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help="Noul probability threshold for true/false (default: 0.5).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only run the first N samples. Use --limit 1 for the first API smoke test.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=90.0,
        help="HTTP timeout in seconds (default: 90).",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="Retries for transient failures (default: 2).",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.0,
        help="Sleep between samples in seconds (default: 0).",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="API key. Prefer OPENJEV_API_KEY environment variable instead.",
    )
    args = parser.parse_args()

    api_key = args.api_key or os.getenv("OPENJEV_API_KEY")
    if not api_key:
        print(
            "Missing API key.\n"
            "PowerShell:\n"
            '  $env:OPENJEV_API_KEY="your_key_here"\n'
            "CMD:\n"
            '  set OPENJEV_API_KEY=your_key_here\n'
            "Linux/macOS:\n"
            '  export OPENJEV_API_KEY="your_key_here"',
            file=sys.stderr,
        )
        return 2

    if not args.input.exists():
        print(f"Input file not found: {args.input}", file=sys.stderr)
        return 2

    if args.gt is not None and not args.gt.exists():
        print(f"Ground-truth file not found: {args.gt}", file=sys.stderr)
        return 2

    requests_data = load_jsonl(args.input)
    ground_truth = load_ground_truth(args.gt)

    if args.limit is not None:
        requests_data = requests_data[: args.limit]

    print(f"Endpoint : {args.endpoint}")
    print(f"Samples  : {len(requests_data)}")
    print(f"Threshold: {args.threshold:.2f}")
    print(f"Output   : {args.output}")
    print()

    stats = {
        "concentric": {"tp": 0, "fp": 0, "fn": 0, "tn": 0},
        "coincident": {"tp": 0, "fp": 0, "fn": 0, "tn": 0},
    }

    session = requests.Session()

    with args.output.open("w", encoding="utf-8") as fout:
        for i, request_obj in enumerate(requests_data, 1):
            sample_id = request_obj.get("sample_id", f"sample_{i}")

            state = request_obj.get("state", {})
            part_a = state.get("partA", {}).get("part_id", "?")
            part_b = state.get("partB", {}).get("part_id", "?")

            # Useful when diagnosing oversized CAD states.
            payload_bytes = len(
                json.dumps(
                    {
                        "model": request_obj.get("model", "openjev"),
                        "state": request_obj.get("state"),
                        "questions": request_obj.get("questions"),
                    },
                    ensure_ascii=False,
                    separators=(",", ":"),
                ).encode("utf-8")
            )

            print(
                f"[{i}/{len(requests_data)}] {sample_id} "
                f"(Part {part_a} <-> Part {part_b}, {payload_bytes / 1024:.1f} KiB)"
            )

            started = time.perf_counter()

            try:
                result = call_jev(
                    session=session,
                    endpoint=args.endpoint,
                    api_key=api_key,
                    request_obj=request_obj,
                    timeout=args.timeout,
                    retries=args.retries,
                )
                elapsed = time.perf_counter() - started

                concentric = get_noul(result, "concentric")
                coincident = get_noul(result, "coincident")

                print(
                    "  Jev:"
                    f" concentric={concentric if concentric is not None else 'N/A'}"
                    f"  coincident={coincident if coincident is not None else 'N/A'}"
                    f"  time={elapsed:.3f}s"
                )

                gt = ground_truth.get(sample_id)
                gt_labels = gt.get("labels", {}) if gt else None

                if gt_labels:
                    gt_c = bool(gt_labels.get("concentric"))
                    gt_o = bool(gt_labels.get("coincident"))

                    if concentric is not None:
                        update_binary_stats(
                            stats, "concentric", gt_c, concentric, args.threshold
                        )
                    if coincident is not None:
                        update_binary_stats(
                            stats, "coincident", gt_o, coincident, args.threshold
                        )

                    print(
                        "  GT :"
                        f" concentric={int(gt_c)}"
                        f"  coincident={int(gt_o)}"
                    )

                row = {
                    "sample_id": sample_id,
                    "partA": part_a,
                    "partB": part_b,
                    "request_bytes": payload_bytes,
                    "elapsed_seconds": elapsed,
                    "prediction": {
                        "concentric": concentric,
                        "coincident": coincident,
                    },
                    "ground_truth": gt_labels,
                    "response": result,
                }

            except Exception as e:
                elapsed = time.perf_counter() - started
                print(f"  ERROR: {e}", file=sys.stderr)
                row = {
                    "sample_id": sample_id,
                    "partA": part_a,
                    "partB": part_b,
                    "request_bytes": payload_bytes,
                    "elapsed_seconds": elapsed,
                    "error": str(e),
                }

            fout.write(
                json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
            )
            fout.flush()

            if args.sleep > 0 and i < len(requests_data):
                time.sleep(args.sleep)

    if ground_truth:
        print("\n=== Evaluation ===")
        for label in ("concentric", "coincident"):
            s = stats[label]
            m = metrics(s)
            n = sum(s.values())
            print(
                f"{label:10s}"
                f"  n={n:2d}"
                f"  TP={s['tp']:2d}"
                f" FP={s['fp']:2d}"
                f" FN={s['fn']:2d}"
                f" TN={s['tn']:2d}"
                f"  Acc={m['accuracy']:.3f}"
                f" Prec={m['precision']:.3f}"
                f" Recall={m['recall']:.3f}"
                f" F1={m['f1']:.3f}"
            )

    print(f"\nSaved: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
