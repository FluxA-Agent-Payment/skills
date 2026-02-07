# x402 Payment Workflow

Complete step-by-step guide for making paid Reddit/X API calls.

## Prerequisites

- User has consented to payment (~$0.03)
- Determine SKILL_DIR: the directory containing this SKILL.md file

## Step 1: Create Budget Mandate

```bash
node $SKILL_DIR/fluxa-wallet/scripts/fluxa-cli.bundle.js mandate-create \
  --desc "Research: $TOPIC" \
  --amount 50000
```

From response, save `mandateId`. Tell user to approve at the provided URL.

Wait for confirmation, then check status:
```bash
node $SKILL_DIR/fluxa-wallet/scripts/fluxa-cli.bundle.js mandate-status --id <mandate-id>
```

## Step 2: Get Reddit 402 Payload

```bash
curl -s -X POST https://proxy-monetize.fluxapay.xyz/api/openai-api-endpoints/web_search \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","tools":[{"type":"web_search","filters":{"allowed_domains":["reddit.com"]}}],"input":"Search Reddit for: $TOPIC"}'
```

Save full 402 JSON response.

## Step 3: Get Reddit Payment Header

```bash
node $SKILL_DIR/fluxa-wallet/scripts/fluxa-cli.bundle.js x402-v3 \
  --mandate <MANDATE_ID> \
  --payload '<402_RESPONSE_JSON>'
```

Save `data["X-PAYMENT"]` as `REDDIT_PAYMENT_HEADER`.

## Step 4: Get X 402 Payload

```bash
curl -s -X POST https://proxy-monetize.fluxapay.xyz/api/grok-api-call/v1/responses \
  -H "Content-Type: application/json" \
  -d '{"model":"grok-3","tools":[{"type":"x_search"}],"input":"Search X/Twitter for: $TOPIC"}'
```

Save full 402 JSON response.

## Step 5: Get X Payment Header

```bash
node $SKILL_DIR/fluxa-wallet/scripts/fluxa-cli.bundle.js x402-v3 \
  --mandate <MANDATE_ID> \
  --payload '<402_RESPONSE_JSON>'
```

Save `data["X-PAYMENT"]` as `X_PAYMENT_HEADER`.

## Step 6: Run Research Script

```bash
python3 $SKILL_DIR/scripts/last30days.py "$TOPIC" --emit=compact \
  --x-payment-reddit="$REDDIT_PAYMENT_HEADER" \
  --x-payment-x="$X_PAYMENT_HEADER" 2>&1
```

Returns structured results with engagement metrics (upvotes, likes).

## Error Handling

See `fluxa-wallet/error-handle.md` for common errors.

If FluxA Agent ID not initialized, see `fluxa-wallet/initialize-agent-id.md`.
