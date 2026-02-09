#!/bin/bash
#
# poll-kling-videos.sh - Poll Kling video tasks and auto-download completed videos
#
# Accepts a JSON file with task IDs and output paths, polls every 15 seconds,
# downloads completed videos, and exits when all done or timeout.
#
# Usage:
#   ./scripts/poll-kling-videos.sh \
#     --tasks tasks.json \
#     --output-dir output/ppt_TIMESTAMP/videos
#
# tasks.json format:
#   [
#     {"task_id": "849707946472374335", "output": "preview.mp4"},
#     {"task_id": "849708171970756643", "output": "transition_01_to_02.mp4"}
#   ]
#
# Options:
#   --tasks       (required) Path to JSON file with task definitions
#   --output-dir  (required) Directory to save downloaded videos
#   --interval    (optional) Poll interval in seconds, default: 15
#   --timeout     (optional) Max wait time in seconds, default: 600

set -euo pipefail

TASKS_FILE=""
OUTPUT_DIR=""
INTERVAL=15
TIMEOUT=600
BASE_URL="https://proxy-monetize.fluxapay.xyz/api/kling-i2v/v1/videos/image2video"

while [[ $# -gt 0 ]]; do
    case $1 in
        --tasks)      TASKS_FILE="$2"; shift 2 ;;
        --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
        --interval)   INTERVAL="$2"; shift 2 ;;
        --timeout)    TIMEOUT="$2"; shift 2 ;;
        *)
            echo "{\"success\":false,\"error\":\"Unknown option: $1\"}" >&2
            exit 1
            ;;
    esac
done

if [[ -z "$TASKS_FILE" ]]; then
    echo "{\"success\":false,\"error\":\"--tasks is required\"}" >&2
    exit 1
fi
if [[ -z "$OUTPUT_DIR" ]]; then
    echo "{\"success\":false,\"error\":\"--output-dir is required\"}" >&2
    exit 1
fi
if [[ ! -f "$TASKS_FILE" ]]; then
    echo "{\"success\":false,\"error\":\"Tasks file not found: $TASKS_FILE\"}" >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

TOTAL=$(jq 'length' "$TASKS_FILE")
COMPLETED=0
FAILED=0
START_TIME=$(date +%s)

# Track done tasks via temp file (compatible with macOS bash 3)
DONE_FILE=$(mktemp)
trap 'rm -f "$DONE_FILE"' EXIT

echo "[Videos] Polling $TOTAL video tasks every ${INTERVAL}s (timeout: ${TIMEOUT}s)" >&2

while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))

    if [[ $ELAPSED -ge $TIMEOUT ]]; then
        echo "[Videos] Timeout after ${TIMEOUT}s. $COMPLETED/$TOTAL completed, $FAILED failed." >&2
        break
    fi

    ALL_DONE=true

    for i in $(seq 0 $((TOTAL - 1))); do
        TASK_ID=$(jq -r ".[$i].task_id" "$TASKS_FILE")
        OUTPUT_NAME=$(jq -r ".[$i].output" "$TASKS_FILE")

        # Skip already processed tasks
        if grep -q "^${TASK_ID}$" "$DONE_FILE" 2>/dev/null; then
            continue
        fi

        ALL_DONE=false

        # Poll status
        RESPONSE=$(curl -s "${BASE_URL}/${TASK_ID}" 2>/dev/null || echo '{"data":{"task_status":"error"}}')
        STATUS=$(echo "$RESPONSE" | jq -r '.data.task_status // "unknown"' 2>/dev/null || echo "error")

        case "$STATUS" in
            succeed)
                VIDEO_URL=$(echo "$RESPONSE" | jq -r '.data.task_result.videos[0].url // empty' 2>/dev/null || echo "")
                if [[ -n "$VIDEO_URL" ]]; then
                    curl -s -o "${OUTPUT_DIR}/${OUTPUT_NAME}" "$VIDEO_URL"
                    SIZE=$(wc -c < "${OUTPUT_DIR}/${OUTPUT_NAME}" 2>/dev/null || echo "0")
                    COMPLETED=$((COMPLETED + 1))
                    echo "$TASK_ID" >> "$DONE_FILE"
                    echo "[Videos] ($COMPLETED/$TOTAL) Downloaded $OUTPUT_NAME ($((SIZE / 1024))KB)" >&2
                else
                    FAILED=$((FAILED + 1))
                    echo "$TASK_ID" >> "$DONE_FILE"
                    echo "[Videos] ($((COMPLETED + FAILED))/$TOTAL) FAILED $OUTPUT_NAME - no video URL" >&2
                fi
                ;;
            failed)
                FAILED=$((FAILED + 1))
                echo "$TASK_ID" >> "$DONE_FILE"
                MSG=$(echo "$RESPONSE" | jq -r '.data.task_status_msg // "unknown error"' 2>/dev/null || echo "unknown")
                echo "[Videos] ($((COMPLETED + FAILED))/$TOTAL) FAILED $OUTPUT_NAME - $MSG" >&2
                ;;
            processing|submitted)
                # Still working
                ;;
            *)
                echo "[Videos] Warning: Unknown status '$STATUS' for task $TASK_ID" >&2
                ;;
        esac
    done

    if [[ "$ALL_DONE" == true ]]; then
        break
    fi

    REMAINING=$((TOTAL - COMPLETED - FAILED))
    echo "[Videos] $COMPLETED/$TOTAL complete, $REMAINING remaining. Waiting ${INTERVAL}s..." >&2
    sleep "$INTERVAL"
done

# Output summary as JSON
echo "{\"success\":true,\"total\":$TOTAL,\"completed\":$COMPLETED,\"failed\":$FAILED,\"elapsed\":$ELAPSED,\"output_dir\":\"$OUTPUT_DIR\"}"
