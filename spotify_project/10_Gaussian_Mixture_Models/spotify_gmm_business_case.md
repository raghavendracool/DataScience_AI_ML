# Spotify GMM Business Case

## Business Problem

Spotify users may not belong perfectly to one behavior persona.

Example:

```text
A user can be:
55% Power Streamer
41% Habitual Loyalist
4% Other
```

A hard-only segmentation hides this overlap.

## Objective

Use Gaussian Mixture Models to estimate:

- Most likely component
- Probability for every component
- Membership confidence
- Boundary-user status

## Technical Output

```text
user_id
gmm_component
component_0_probability
component_1_probability
component_2_probability
component_3_probability
membership_confidence
```

## Business Uses

- Flexible persona assignment
- Blended recommendation strategies
- Confidence-aware Premium campaigns
- Boundary-user analysis
- Segment transition monitoring
- Model-risk review

## Example

A high-engagement user with:

```text
Power Streamer probability = 0.58
Habitual Loyalist probability = 0.39
```

may receive:

- Premium conversion messaging
- Loyalty rewards
- Personalized high-frequency playlists

The business should not interpret the user as a perfectly certain persona.
