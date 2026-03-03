# Skill Development Agent Instructions

You are helping build a Claude Code skill that uses paid APIs from the FluxA platform.
Your goal is to explore these APIs, understand what they offer, and propose creative
ways to combine them into a useful skill.

## Available APIs

### Nano Banana

- **Proxy URL:** `https://proxy-monetize.fluxapay.xyz/api/nano-banana/7ded04c9`
- **Description:** API for Nano Banana
- **Discovery:** `curl https://proxy-monetize.fluxapay.xyz/api/nano-banana/7ded04c9`

| Method | Path | Description | Price (USDC) |
|--------|------|-------------|-------------|
| POST | `/gen-image` | generate image with nano banana 2.5 | 0.1 |
| POST | `/gen-image-pro` | generate image with nano banana 3 | 0.1 |

### Kling Video Generation

- **Proxy URL:** `https://proxy-monetize.fluxapay.xyz/api/kling-video-generation/7ded04c9`
- **Description:** Generate video with image using Kling v2.6
- **Discovery:** `curl https://proxy-monetize.fluxapay.xyz/api/kling-video-generation/7ded04c9`

| Method | Path | Description | Price (USDC) |
|--------|------|-------------|-------------|
| GET | `/get-video` | Get video generation task status and result | 0 |
| POST | `/image-to-video` | using image url to generate video with kling v2.6 | 0.2 |

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
- Register with `fluxa-wallet init --name "..." --client "..."` before making paid API calls
- Create an intent mandate before making paid API calls
- See the per-API docs in `./api-docs/` for full integration instructions
