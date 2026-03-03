# Integrate Nano Banana API

**API Endpoint:** `https://proxy-monetize.fluxapay.xyz/api/nano-banana/7ded04c9`

## Discover Available Endpoints

```bash
curl https://proxy-monetize.fluxapay.xyz/api/nano-banana/7ded04c9
```

Returns JSON with:
- `name`: Server name
- `description`: Server description
- `endpoints`: List of endpoints with paths, methods, descriptions, and prices
- `paymentRequired`: Whether payment is needed
- `networks`: Supported payment networks

## Available Endpoints

| Method | Path | Description | Price |
|--------|------|-------------|-------|
| POST | `/gen-image` | generate image with nano banana 2.5 | $0.10 / 0.10 cr |
| POST | `/gen-image-pro` | generate image with nano banana 3 | $0.10 / 0.10 cr |

## Setup — Install FluxA Wallet CLI

```bash
npm install -g @fluxa-pay/fluxa-wallet
```

Or use without installing:

```bash
npx fluxa-wallet <command> [options]
```

All commands output JSON: `{ "success": true, "data": { ... } }`

## Register Agent

```bash
fluxa-wallet init --name "<YOUR_AGENT_NAME>" --client "<YOUR_CLIENT>"
```

The CLI handles JWT storage and automatic refresh. Verify status:

```bash
fluxa-wallet status
```

## x402 v3 Intent Mandate Payment

x402 v3 uses **intent mandates**: the user pre-approves a spending plan (budget + time window), then the agent can make autonomous payments within those limits. The user only needs to approve once.

### Step 1 — Choose Payment Method

Ask the user which payment method to use:
- **On-chain USDC (Base)** — `--currency USDC`, `--amount` in atomic units (6 decimals, e.g., `100000` = 0.10 USDC)
- **FluxA Monetize Credits** — `--currency FLUXA_MONETIZE_CREDITS`, `--amount` in 2-decimal units (e.g., `10` = 0.10 credits = 0.10 USDC)

### Step 2 — Create Intent Mandate

```bash
fluxa-wallet mandate-create \
  --desc "Spend up to <BUDGET> for <DESCRIPTION> valid for <DURATION>" \
  --amount <BUDGET_IN_UNITS> \
  --seconds <DURATION_IN_SECONDS> \
  --currency <USDC or FLUXA_MONETIZE_CREDITS>
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--desc` | Yes | — | Human-readable spending plan description |
| `--amount` | Yes | — | Budget limit in units for the chosen currency |
| `--seconds` | No | `28800` (8h) | Validity duration in seconds |
| `--currency` | No | `USDC` | `USDC` or `FLUXA_MONETIZE_CREDITS` |

Response includes `mandateId` and `authorizationUrl`. Ask the user to open `authorizationUrl` (TTL: 10 minutes) to review and sign.

### Step 3 — User Signs Mandate

Present the user with a choice:
- "Yes, open the link" → run `open "<authorizationUrl>"`
- "No, show me the URL" → display URL and ask how to proceed

### Step 4 — Check Mandate Status

```bash
fluxa-wallet mandate-status --id <MANDATE_ID>
```

Wait until `mandate.status` is `"signed"`. Response includes `remainingAmount` to track budget.

**Important:** Use `--id`, not `--mandate`.

### Step 5 — Call the API

```bash
curl https://proxy-monetize.fluxapay.xyz/api/nano-banana/7ded04c9/<endpoint>
```

If the API returns HTTP 402, continue to Step 6.

### Step 6 — Make x402 v3 Payment

Pass the **complete** HTTP 402 response body as `--payload`:

```bash
fluxa-wallet x402-v3 \
  --mandate <MANDATE_ID> \
  --payload '$PAYLOAD_402'
```

The payload **must** contain an `accepts` array. Do NOT extract individual fields — pass the entire 402 response JSON.

Response includes `xPaymentB64` (the payment token).

### Step 7 — Retry with X-Payment Header

```bash
curl -H "X-Payment: <xPaymentB64>" https://proxy-monetize.fluxapay.xyz/api/nano-banana/7ded04c9/<endpoint>
```

Return the API response to the user.

## Credits Conversion Reference

| USDC | Mandate amount (USDC atomic) | Mandate amount (Credits 2-decimal) |
|------|------------------------------|-----------------------------------|
| 0.01 | `10000` | `1` |
| 0.10 | `100000` | `10` |
| 1.00 | `1000000` | `100` |

## Opening Links for User

When you need to open a URL (authorization, approval, or any external link):
1. Present the user with a choice using your interactive options/menu capability (e.g., AskUserQuestion tool)
2. Options: "Yes, open the link" / "No, show me the URL"
3. If YES: run `open "<URL>"` to open in their default browser
4. If NO: display the URL and ask how to proceed

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| `mandate_not_signed` | User hasn't signed yet | Ask user to open `authorizationUrl` |
| `mandate_expired` | Time window passed | Create a new mandate |
| `mandate_budget_exceeded` | Budget too low | Create a new mandate with higher limit |
| `agent_not_registered` | No Agent ID | Run `fluxa-wallet init` first |
| `Invalid payload: missing accepts array` | Incomplete 402 payload | Pass the full 402 response JSON |