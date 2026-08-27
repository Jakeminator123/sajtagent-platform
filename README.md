# Sajtagent Platform — legacy snapshot

This repository is a historical coordination and architecture snapshot. It is
not an active Sajtagent repository, product runtime, deployment target, or
source of truth.

## Canonical home

All current Sajtagent work belongs in
[`Jakeminator123/sajtagent-site`](https://github.com/Jakeminator123/sajtagent-site).

That single repository separates the product into clear surfaces:

| Surface | Canonical location |
| --- | --- |
| SiteAgent web product and Builder | `sajtagent-site/app`, `components`, and `lib/siteagent` |
| Privileged controller, OpenClaw, and Sprite runtime | `sajtagent-site/runtime` |
| Architecture and platform decisions | `sajtagent-site/docs` |
| Local maintenance and control utilities | `sajtagent-site/tools` when needed |

Accepted decisions from this repository are being consolidated into
`sajtagent-site/docs`. Do not add features, secrets, deployments, or new
architecture decisions here. The read-only control panel and older documents
remain reference material only and may be removed after the consolidation is
verified.

Legacy repositories `sajtagent-platform`, `sajtagent-sprites`, and
`builder-v2` must not be treated as parallel sources of truth.
