# Skill Development Agent Instructions

You are helping build a Claude Code skill that uses paid APIs from the FluxA platform.
Your goal is to explore these APIs, understand what they offer, and propose creative
ways to combine them into a useful skill.

## Available APIs

### Grok API call

- **Proxy URL:** `https://proxy-monetize.fluxapay.xyz/api/grok-api-call`
- **Description:** API for calling grok
- **Discovery:** `curl https://proxy-monetize.fluxapay.xyz/api/grok-api-call`

| Method | Path | Description | Price (USDC) |
|--------|------|-------------|-------------|
| POST | `/v1/responses` | request the xai api for search on X.com | 0.01 |

### Video Generation with VEO 3.1

- **Proxy URL:** `https://proxy-monetize.fluxapay.xyz/api/video-generation-with-veo-3-1`
- **Description:** Using Google's veo 3.1 to generate videos
- **Discovery:** `curl https://proxy-monetize.fluxapay.xyz/api/video-generation-with-veo-3-1`

| Method | Path | Description | Price (USDC) |
|--------|------|-------------|-------------|
| POST | `/generate-video` | Generate video with veo 3.1 | 0.5 |
| GET | `/get-video` | Get generated video | 0 |

### OpenAI API Endpoints

- **Proxy URL:** `https://proxy-monetize.fluxapay.xyz/api/openai-api-endpoints`
- **Description:** APIs for OpenAI models
- **Discovery:** `curl https://proxy-monetize.fluxapay.xyz/api/openai-api-endpoints`

| Method | Path | Description | Price (USDC) |
|--------|------|-------------|-------------|
| POST | `/audio` | Generates audio from the input text. | 0.1 |
| POST | `/web_search` | Use GPT models for web search | 0.02 |

### KLing I2V

- **Proxy URL:** `https://proxy-monetize.fluxapay.xyz/api/kling-i2v`
- **Description:** API for creating video from image
- **Discovery:** `curl https://proxy-monetize.fluxapay.xyz/api/kling-i2v`

| Method | Path | Description | Price (USDC) |
|--------|------|-------------|-------------|
| POST | `/v1/videos/image2video` | - | 0.01 |
| GET | `/v1/videos/image2video/` | Query task status | 0 |

## Your Tasks

1. **Read the payment docs** - Start with `./fluxa-wallet/SKILL.md` to understand how x402 payments work
2. **Explore each API** - Run the discovery curl command for each API above to see available endpoints
3. **Try calling endpoints** - Make test requests to understand what data each endpoint returns
4. **Propose skill ideas** - Come up with 3-5 creative skill ideas that combine these APIs
5. **Pick the best one** - Choose the most useful/interesting idea
6. **Implement it** - Update the `SKILL.md` file with your skill implementation

## Payment Reference

- Payment wallet docs: `./fluxa-wallet/SKILL.md`
- x402 protocol details: `./fluxa-wallet/X402-PAYMENT.md`
- Per-API integration docs: `./api-docs/` directory
- Payment links: `./fluxa-wallet/PAYMENT-LINK.md`
- Payouts: `./fluxa-wallet/PAYOUT.md`

## Important Notes

- All API calls go through the FluxA proxy and require x402 payment
- The agent needs a JWT from `~/.fluxa-ai-wallet-mcp/.agent-config.json`
- Create an intent mandate before making paid API calls
- See the per-API docs in `./api-docs/` for full integration instructions
