---
name: skill-starter-kit--8-
description: A skill that uses Grok API call, Video Generation with VEO 3.1, OpenAI API Endpoints, KLing I2V
---

# My Skill

This skill uses the following paid APIs:
- **Grok API call**: API for calling grok
- **Video Generation with VEO 3.1**: Using Google's veo 3.1 to generate videos
- **OpenAI API Endpoints**: APIs for OpenAI models
- **KLing I2V**: API for creating video from image

## What This Skill Does

<!-- Describe what your skill does here -->

## Usage

<!-- Describe how to use this skill -->

## tools

* Grok API call

  * name: pay-per-use-based grok-api-call
  * access: agent-pay
  * usage:
    ```
    ** API Discovery ** First, discover available endpoints by making a GET request to the base URL:
    curl https://proxy-monetize.fluxapay.xyz/api/grok-api-call
    ```

* Video Generation with VEO 3.1

  * name: pay-per-use-based video-generation-with-veo-3-1
  * access: agent-pay
  * usage:
    ```
    ** API Discovery ** First, discover available endpoints by making a GET request to the base URL:
    curl https://proxy-monetize.fluxapay.xyz/api/video-generation-with-veo-3-1
    ```

* OpenAI API Endpoints

  * name: pay-per-use-based openai-api-endpoints
  * access: agent-pay
  * usage:
    ```
    ** API Discovery ** First, discover available endpoints by making a GET request to the base URL:
    curl https://proxy-monetize.fluxapay.xyz/api/openai-api-endpoints
    ```

* KLing I2V

  * name: pay-per-use-based kling-i2v
  * access: agent-pay
  * usage:
    ```
    ** API Discovery ** First, discover available endpoints by making a GET request to the base URL:
    curl https://proxy-monetize.fluxapay.xyz/api/kling-i2v
    ```

* Make X402 payment: see ./fluxa-wallet/X402-PAYMENT.md


# notes for tools use

* If the invoked tool's access is **agent-pay**, it means the tool is accessed by the agent on a **pay-per-use** basis.
  The agent needs to handle x402 payment flow to use these tools.
  See ./fluxa-wallet/SKILL.md for the complete payment wallet documentation.
* For x402 payment details, refer to ./fluxa-wallet/X402-PAYMENT.md
* For payout operations, refer to ./fluxa-wallet/PAYOUT.md
* For payment link operations, refer to ./fluxa-wallet/PAYMENT-LINK.md
