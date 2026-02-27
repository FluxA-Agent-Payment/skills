# Integrate Grok API call API

**API Endpoint:** `https://proxy-monetize.fluxapay.xyz/api/grok-api-call`

## Discover Available Endpoints

```bash
curl https://proxy-monetize.fluxapay.xyz/api/grok-api-call
```

Returns JSON with:
- `name`: Server name
- `description`: Server description
- `endpoints`: List of endpoints with paths, methods, descriptions, and prices
- `paymentRequired`: Whether payment is needed
- `networks`: Supported payment networks

## Available Endpoints

| Method | Path | Description | Price (USDC) |
|--------|------|-------------|--------------|
| POST | `/v1/responses` | request the xai api for search on X.com | 0.01 |

## Agent JWT Configuration

Your AGENT_JWT is stored in: `~/.fluxa-ai-wallet-mcp/.agent-config.json`

```json
{
  "agents": {
    "<email>": {
      "<agent_name>": {
        "jwt": "<YOUR_AGENT_JWT>",
        "email": "<email>",
        "agent_name": "<agent_name>",
        "jwt_expires_at": "<expiry_timestamp>"
      }
    }
  }
}
```

Read JWT: `jq -r '.agents["<YOUR_EMAIL>"]["<YOUR_AGENT_NAME>"].jwt' ~/.fluxa-ai-wallet-mcp/.agent-config.json`

## x402 v3 Intent Mandate Payment

x402 v3 uses **intent mandates**: the user pre-approves a spending plan (budget + time window), then the agent can make autonomous payments within those limits. The user only needs to approve once.

### Step 1 — Create Intent Mandate

```bash
curl -X POST https://walletapi.fluxapay.xyz/api/mandates/create-intent \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_JWT" \
  -d '{
    "intent": {
      "naturalLanguage": "I plan to spend up to <BUDGET> USDC to <DESCRIPTION> valid for <DURATION>.",
      "category": "general",
      "currency": "USDC",
      "limitAmount": "<BUDGET_IN_ATOMIC_UNITS>",
      "validForSeconds": <DURATION_IN_SECONDS>,
      "hostAllowlist": []
    }
  }'
```

**Intent fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `naturalLanguage` | Yes | Human-readable description of the spending plan |
| `category` | No | Category tag (e.g., `trading_data`, `general`) |
| `currency` | No | Currency (default: `USDC`) |
| `limitAmount` | Yes | Maximum budget in atomic units (6 decimals, e.g., `100000` = 0.10 USDC) |
| `validForSeconds` | Yes | Duration in seconds (e.g., `2592000` = 30 days) |
| `hostAllowlist` | No | Restrict to specific API hosts (empty = any) |

Response includes `mandateId` and `authorizationUrl`. Ask the user to open `authorizationUrl` (TTL: 10 minutes) to review and sign.

### Step 2 — Check Mandate Status

```bash
curl -H "Authorization: Bearer $AGENT_JWT" \
  https://walletapi.fluxapay.xyz/api/mandates/agent/<MANDATE_ID>
```

Wait until `mandate.status` is `"signed"` before making payments. Response includes `remainingAmount` to track budget.

### Step 3 — Make x402 v3 Payment

When the API returns HTTP 402, extract fields from the response and call:

```bash
curl -X POST https://walletapi.fluxapay.xyz/api/payment/x402V3Payment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_JWT" \
  -d '{
    "mandateId": "<MANDATE_ID>",
    "scheme": "exact",
    "network": "base",
    "amount": "<FROM_402_accepts[0].maxAmountRequired>",
    "currency": "USDC",
    "assetAddress": "<FROM_402_accepts[0].asset>",
    "payTo": "<FROM_402_accepts[0].payTo>",
    "host": "<HOSTNAME_OF_API>",
    "resource": "<FULL_URL_OF_ENDPOINT>",
    "description": "<FROM_402_accepts[0].description>",
    "tokenName": "<FROM_402_accepts[0].extra.name>",
    "tokenVersion": "<FROM_402_accepts[0].extra.version>",
    "validityWindowSeconds": <FROM_402_accepts[0].maxTimeoutSeconds>
  }'
```

**Field mapping from HTTP 402 response:**

| Field | Source |
|-------|--------|
| `mandateId` | From Step 1 |
| `amount` | `accepts[0].maxAmountRequired` |
| `assetAddress` | `accepts[0].asset` |
| `payTo` | `accepts[0].payTo` |
| `description` | `accepts[0].description` |
| `tokenName` | `accepts[0].extra.name` (usually `"USD Coin"`) |
| `tokenVersion` | `accepts[0].extra.version` (usually `"2"`) |
| `validityWindowSeconds` | `accepts[0].maxTimeoutSeconds` |

Response includes `xPaymentB64` (payment token).

### Step 4 — Retry with X-Payment Header

```bash
curl -H "X-Payment: <xPaymentB64>" https://proxy-monetize.fluxapay.xyz/api/grok-api-call/<endpoint>
```

## CRITICAL: Opening Links for User

When you need to open a URL (authorization, approval, or any external link), you MUST:
1. Present the user with a choice using your interactive options/menu capability (e.g., AskUserQuestion tool)
2. Give them options like: "Yes, open the link" / "No, don't open"
3. If YES: Use `open "<URL>"` command to open the URL in their default browser
4. If NO: Ask how they would like to proceed

## Credits Payment Option (Alternative to On-Chain USDC)

The 402 response may include a `fluxa-monetize-credits` entry in the `accepts` array alongside the on-chain `base` USDC entry. Credits use FluxA Monetize Credits instead of on-chain USDC. **1 credit = 1 USDC**.

### To pay with credits:

1. **Create the intent mandate** with:
   - `"currency": "FLUXA_MONETIZE_CREDITS"`
   - `limitAmount` in 2-decimal units (e.g., `"10"` = 0.10 credits = 0.10 USDC, `"100"` = 1.00 credits = 1.00 USDC)
   - Use `walletapi.fluxapay.xyz` as the API host

2. **When making the x402V3Payment call**, pick the `fluxa-monetize-credits` entry from `accepts[]` and use:

| Field | Value |
|-------|-------|
| `network` | `fluxa-monetize-credits` |
| `assetAddress` | `fluxa-monetize-credit` |
| `tokenName` | `FluxA Monetize Credits` |
| `tokenVersion` | `1` |
| `amount` | From the credits entry's `maxAmountRequired` |

### Conversion

| USDC | Payment amount (from 402) | Mandate limitAmount (2-decimal) |
|------|---------------------------|--------------------------------|
| 0.01 | `"0.01"` | `"1"` |
| 0.10 | `"0.1"` | `"10"` |
| 1.00 | `"1"` | `"100"` |

## Error Handling

| Error code | Meaning | Action |
|------------|---------|--------|
| `mandate_not_signed` | User hasn't signed yet | Ask user to open `authorizationUrl` |
| `mandate_expired` | Time window has passed | Create a new mandate |
| `mandate_budget_exceeded` | Remaining budget too low | Create a new mandate with higher limit |
| `agent_not_registered` | No Agent ID configured | Register first via `/register` |
| `jwt_refresh_failed` | JWT expired | Re-register agent |

## Steps to Follow

1. **Check JWT:** Read AGENT_JWT from `~/.fluxa-ai-wallet-mcp/.agent-config.json`

2. **Register if needed:** If no JWT or expired:
   ```bash
   curl -X POST https://agentid.fluxapay.xyz/register \
     -H "Content-Type: application/json" \
     -d '{"email":"<YOUR_EMAIL>","name":"<YOUR_AGENT_NAME>"}'
   ```
   - Present user with options: "I need to open the authorization URL to complete registration."
   - If YES: Run `open "<URL>"` to open in browser
   - Save the JWT to config file

3. **Ask user for payment method:** Present the user with a choice:
   - **On-chain USDC (Base)** — uses `currency: "USDC"`, `limitAmount` in 6-decimal atomic units, and `walletapi.fluxapay.xyz`
   - **FluxA Monetize Credits** — uses `currency: "FLUXA_MONETIZE_CREDITS"`, `limitAmount` in 2-decimal units (e.g., `"10"` = 0.10), and `walletapi.fluxapay.xyz`

4. **Create intent mandate:** Create a mandate with appropriate budget and duration for the task (Step 1 above), using the currency and units from the chosen payment method

5. **User signs mandate:** Present user with options: "I need you to sign the spending mandate. Open authorization URL?"
   - If YES: Run `open "<authorizationUrl>"` to open in browser

6. **Check mandate status:** Poll until `mandate.status` is `"signed"` (Step 2 above)

7. **Make API request:** `curl https://proxy-monetize.fluxapay.xyz/api/grok-api-call/<endpoint>`

8. **Handle 402:** If HTTP 402 returned, pick the matching entry from `accepts[]` based on the chosen payment method (`network: "base"` for USDC, `network: "fluxa-monetize-credits"` for credits)

9. **Process payment:** Call `x402V3Payment` with `mandateId` and extracted fields from the matching `accepts` entry (Step 3 above)

10. **Retry with payment:** Add X-Payment header with `xPaymentB64`
   ```bash
   curl -H "X-Payment: <xPaymentB64>" https://proxy-monetize.fluxapay.xyz/api/grok-api-call/<endpoint>
   ```

11. **Return response:** Return the API response to the user