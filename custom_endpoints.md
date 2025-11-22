# Endpoints

This document describes the three custom endpoints added to the Nephthys app.

## /project

**Method:** GET

**Description:** Sends a personalized DM to the specified Slack user notifying them that their project has been shipped on Construct. Includes the project URL in the message.

**Required Query Parameters:**
- `authorization`: Must match the `AUTH_KEY` from `.env`
- `slack-id`: The Slack user ID to send the DM to
- `project-url`: The URL of the shipped project

**Response:** JSON with success message and echoed parameters, or error if validation fails.

**Example:**
```bash
curl "https://axis.bbarni.hackclub.app/project?authorization=your_key&slack-id=U123&project-url=https://example.com/project"
```

## /shop

**Method:** GET

**Description:** Sends a personalized DM to the specified Slack user about the approval status of their item request on Construct.

**Required Query Parameters:**
- `authorization`: Must match the `AUTH_KEY` from `.env`
- `slack-id`: The Slack user ID to send the DM to
- `approved`: "true" for approved, "false" for not approved
- `item`: The name of the item requested

**Response:** JSON with success message and echoed parameters, or error if validation fails.

**Example:**
```bash
curl "https://axis.bbarni.hackclub.app/shop?authorization=your_key&slack-id=U123&approved=true&item=sticker"
```

## /review

**Method:** GET

**Description:** Sends a personalized DM to the specified Slack user about the review status of their project on Construct, including the reason.

**Required Query Parameters:**
- `authorization`: Must match the `AUTH_KEY` from `.env`
- `slack-id`: The Slack user ID to send the DM to
- `project-url`: The URL of the project under review
- `status`: "approved", "pending", "rejected", or "hour_deduction"
- `reason`: The reason for the status

**Response:** JSON with success message and echoed parameters, or error if validation fails.

**Example:**
```bash
curl "https://axis.bbarni.hackclub.app/review?authorization=your_key&slack-id=U123&project-url=https://example.com/project&status=approved&reason=Great work!"
```