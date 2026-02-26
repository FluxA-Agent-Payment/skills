# Skill Development Agent Instructions

You are helping build a Claude Code skill that uses paid APIs from the FluxA platform.
Your goal is to explore these APIs, understand what they offer, and propose creative
ways to combine them into a useful skill.

## Available APIs

### asd

- **Proxy URL:** `https://proxy.fluxapay.xyz/api/asd-2`
- **Description:** asd
- **Discovery:** `curl https://proxy.fluxapay.xyz/api/asd-2`

| Method | Path | Description | Price (USDC) |
|--------|------|-------------|-------------|
| POST | `/mcp?apikey=YOUR_API_KEY` | - | 0.01 |

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
