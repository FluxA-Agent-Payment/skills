---
name: my-skill
description: A skill that uses asd
---

# My Skill

This skill uses the following paid APIs:
- **asd**: asd

## What This Skill Does

<!-- Describe what your skill does here -->

## Usage

<!-- Describe how to use this skill -->

## tools

* asd

  * name: pay-per-use-based asd-2
  * access: agent-pay
  * usage:
    ```
    ** API Discovery ** First, discover available endpoints by making a GET request to the base URL:
    curl https://proxy.fluxapay.xyz/api/asd-2
    ```

* Make X402 payment: see ./fluxa-wallet/X402-PAYMENT.md


# notes for tools use

* If the invoked tool's access is **agent-pay**, it means the tool is accessed by the agent on a **pay-per-use** basis.
  The agent needs to handle x402 payment flow to use these tools.
  See ./fluxa-wallet/SKILL.md for the complete payment wallet documentation.
* For x402 payment details, refer to ./fluxa-wallet/X402-PAYMENT.md
* For payout operations, refer to ./fluxa-wallet/PAYOUT.md
* For payment link operations, refer to ./fluxa-wallet/PAYMENT-LINK.md
