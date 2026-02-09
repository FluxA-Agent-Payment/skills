#!/bin/bash
#
# x402-api-call.sh - Automate the x402 payment + API call cycle
#
# Wraps the entire 402 flow into a single command:
#   1. Hit the API (expect HTTP 402)
#   2. Extract the 402 payload
#   3. Sign payment via fluxa-cli x402-v3
#   4. Retry the API with X-Payment header
#   5. Save response to output file
#
# Usage:
#   ./scripts/x402-api-call.sh \
#     --mandate MANDATE_ID \
#     --url API_URL \
#     --body '{"json":"payload"}' \
#     --output response.json
#
# Options:
#   --mandate   (required) The mandate ID for payment signing
#   --url       (required) The API endpoint URL
#   --method    (optional) HTTP method, default: POST
#   --body      (optional) Request body JSON (required for POST)
#   --output    (optional) Output file path, default: stdout
#   --cli-path  (optional) Path to fluxa-cli.bundle.js

set -euo pipefail

METHOD="POST"
OUTPUT=""
BODY=""
MANDATE=""
URL=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_PATH="${SCRIPT_DIR}/../fluxa-wallet/scripts/fluxa-cli.bundle.js"
s
while [[ $# -gt 0 ]]; do
    case $1 in
        --mandate)  MANDATE="$2"; shift 2 ;;
        --url)      URL="$2"; shift 2 ;;
        --method)   METHOD="$2"; shift 2 ;;
        --body)     BODY="$2"; shift 2 ;;
        --output)   OUTPUT="$2"; shift 2 ;;
        --cli-path) CLI_PATH="$2"; shift 2 ;;
        *)
            echo "{\"success\":false,\"error\":\"Unknown option: $1\"}" >&2
            exit 1
            ;;
    esac
done

if [[ -z "$MANDATE" ]]; then
    echo "{\"success\":false,\"error\":\"--mandate is required\"}" >&2
    exit 1
fi
if [[ -z "$URL" ]]; then
    echo "{\"success\":false,\"error\":\"--url is required\"}" >&2
    exit 1
fi
if [[ ! -f "$CLI_PATH" ]]; then
    echo "{\"success\":false,\"error\":\"CLI not found at $CLI_PATH\"}" >&2
    exit 1
fi

TMPFILE_402=$(mktemp)
TMPFILE_PAYMENT=$(mktemp)
TMPFILE_RESPONSE=$(mktemp)
trap 'rm -f "$TMPFILE_402" "$TMPFILE_PAYMENT" "$TMPFILE_RESPONSE"' EXIT

# Step 1: Hit the API to get 402 payload
if [[ "$METHOD" == "POST" ]]; then
    HTTP_CODE=$(curl -s -o "$TMPFILE_402" -w "%{http_code}" "$URL" \
        -X POST -H "Content-Type: application/json" -d "$BODY")
else
    HTTP_CODE=$(curl -s -o "$TMPFILE_402" -w "%{http_code}" "$URL" -X "$METHOD")
fi

if [[ "$HTTP_CODE" != "402" ]]; then
    if [[ "$HTTP_CODE" =~ ^2 ]]; then
        if [[ -n "$OUTPUT" ]]; then
            cp "$TMPFILE_402" "$OUTPUT"
            echo "{\"success\":true,\"http_code\":$HTTP_CODE,\"output\":\"$OUTPUT\",\"payment\":false}"
        else
            cat "$TMPFILE_402"
        fi
        exit 0
    else
        echo "{\"success\":false,\"error\":\"Expected HTTP 402 but got $HTTP_CODE\"}" >&2
        cat "$TMPFILE_402" >&2
        exit 1
    fi
fi

PAYLOAD_402=$(cat "$TMPFILE_402")

# Step 2: Sign payment via CLI
node "$CLI_PATH" x402-v3 \
    --mandate "$MANDATE" \
    --payload "$PAYLOAD_402" 2>/dev/null > "$TMPFILE_PAYMENT" || true

# Step 3: Extract xPaymentB64
XPAYMENT=$(jq -r '.data.xPaymentB64 // empty' "$TMPFILE_PAYMENT" 2>/dev/null || echo "")

if [[ -z "$XPAYMENT" ]]; then
    ERROR=$(jq -r '.error // .data.error // "Unknown payment error"' "$TMPFILE_PAYMENT")
    echo "{\"success\":false,\"error\":\"Payment signing failed: $ERROR\"}" >&2
    exit 1
fi

# Step 4: Retry the API with X-Payment header
if [[ "$METHOD" == "POST" ]]; then
    HTTP_CODE=$(curl -s -o "$TMPFILE_RESPONSE" -w "%{http_code}" "$URL" \
        -X POST -H "Content-Type: application/json" -H "X-Payment: $XPAYMENT" -d "$BODY")
else
    HTTP_CODE=$(curl -s -o "$TMPFILE_RESPONSE" -w "%{http_code}" "$URL" \
        -X "$METHOD" -H "X-Payment: $XPAYMENT")
fi

if [[ ! "$HTTP_CODE" =~ ^2 ]]; then
    echo "{\"success\":false,\"error\":\"API call failed with HTTP $HTTP_CODE after payment\"}" >&2
    cat "$TMPFILE_RESPONSE" >&2
    exit 1
fi

# Step 5: Output
if [[ -n "$OUTPUT" ]]; then
    cp "$TMPFILE_RESPONSE" "$OUTPUT"
    echo "{\"success\":true,\"http_code\":$HTTP_CODE,\"output\":\"$OUTPUT\",\"payment\":true}"
else
    cat "$TMPFILE_RESPONSE"
fi
