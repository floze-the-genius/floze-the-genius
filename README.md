<!-- AUTO-GENERATED from README.template.md; edit the template, not this file. -->
<div align="center">
  <img src="./assets/header.svg" width="100%" alt="Floze - open-source systems engineering, coding agents, and production reliability" />

  <p>
    <a href="https://t.me/bastard11"><img src="https://img.shields.io/badge/Telegram-@bastard11-26A5E4?style=flat-square&logo=telegram&logoColor=white" alt="Telegram" /></a>
    <a href="https://github.com/floze-the-genius?tab=repositories"><img src="https://img.shields.io/badge/GitHub-projects-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub projects" /></a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/upstream%20merged-88-238636?style=flat-square&logo=git&logoColor=white" alt="88 merged upstream pull requests" />
    <img src="https://img.shields.io/badge/maintained%20tool%20stars-283-2f81f7?style=flat-square&logo=github&logoColor=white" alt="283 stars across maintained tools" />
    <img src="https://img.shields.io/badge/public%20contributions%20(12mo)-542-3fb950?style=flat-square&logo=githubactions&logoColor=white" alt="542 public contributions in the last 12 months" />
  </p>
</div>

I am an **open-source systems engineer** who turns ambiguous, cross-layer failures into shipped, reviewable fixes. I build developer tooling and coding-agent infrastructure, and I operate production systems where correctness, recovery, and observability are not optional.

My public work spans compiler/runtime behavior, Kubernetes policy validation, CLI execution safety, atomic storage, cloud integrations, package resolution, authentication, performance measurement, CI, and deployment reliability.

> I enter unfamiliar systems, find the real failure boundary, build the regression proof, and stay with the change until it is useful upstream.

## Products I maintain

<table>
  <tr>
    <td width="33%" valign="top">
      <h3><a href="https://github.com/floze-the-genius/opencode-multi-auth-codex">opencode-multi-auth-codex</a></h3>
      <p>A reliability layer for Codex OAuth in OpenCode: account routing, session controls, dashboard, and operational tooling.</p>
      <p>
        <img src="https://img.shields.io/github/stars/floze-the-genius/opencode-multi-auth-codex?style=flat-square&label=stars" alt="Stars" />
        <img src="https://img.shields.io/github/forks/floze-the-genius/opencode-multi-auth-codex?style=flat-square&label=forks" alt="Forks" />
      </p>
    </td>
    <td width="33%" valign="top">
      <h3><a href="https://github.com/floze-the-genius/opencode-tps-meter">opencode-tps-meter</a></h3>
      <p>Makes coding-agent throughput observable with live streaming and final output-token measurements in the OpenCode TUI.</p>
      <p>
        <img src="https://img.shields.io/github/stars/floze-the-genius/opencode-tps-meter?style=flat-square&label=stars" alt="Stars" />
        <img src="https://img.shields.io/github/forks/floze-the-genius/opencode-tps-meter?style=flat-square&label=forks" alt="Forks" />
      </p>
    </td>
    <td width="33%" valign="top">
      <h3><a href="https://github.com/floze-the-genius/opencode-status-signals">opencode-status-signals</a></h3>
      <p>Turns hidden agent state into immediate visual feedback through OpenCode's native theme system.</p>
      <p>
        <img src="https://img.shields.io/github/stars/floze-the-genius/opencode-status-signals?style=flat-square&label=stars" alt="Stars" />
        <img src="https://img.shields.io/github/forks/floze-the-genius/opencode-status-signals?style=flat-square&label=forks" alt="Forks" />
      </p>
    </td>
  </tr>
</table>

## Proof of work

<p align="center">
  <img src="./assets/engineering-signal.svg" width="100%" alt="Floze engineering signal: public upstream merges, maintained tool adoption, and public contributions" />
</p>

**What I bring to a difficult codebase**

- Deep debugging across runtime, API, storage, infrastructure, and deployment boundaries
- Regression tests and compatibility guards that make risky fixes maintainable
- Production ownership: observability, safe migrations, CI, recovery, and release discipline
- Maintainer-grade follow-through from unclear issue to reviewed, shipped result

## Selected upstream engineering

| Project | Merged contribution | Engineering area |
| --- | --- | --- |
| [Svelte](https://github.com/sveltejs/svelte) | [Preserve select selection with spread attributes](https://github.com/sveltejs/svelte/pull/18561) | Compiler/runtime DOM behavior |
| [Kong kongctl](https://github.com/Kong/kongctl) | [Enforce saved declarative-plan execution modes](https://github.com/Kong/kongctl/pull/1655) | CLI execution safety and test coverage |
| [NGINX Gateway Fabric](https://github.com/nginx/nginx-gateway-fabric) | [Detect conflicting route policies across overlapping hostnames](https://github.com/nginx/nginx-gateway-fabric/pull/5605) | Kubernetes Gateway API validation |
| [zarrs](https://github.com/zarrs/zarrs) | [Add an atomic write storage adapter](https://github.com/zarrs/zarrs/pull/421) | Rust storage concurrency and API design |
| [MapLibre Martin](https://github.com/maplibre/martin) | [Restore AWS profile support for PMTiles](https://github.com/maplibre/martin/pull/3029) | Cloud credentials and Rust integration |
| [yay](https://github.com/Jguer/yay) | [Prefer repository replacements over matching AUR upgrades](https://github.com/Jguer/yay/pull/2910) | Package resolution correctness |

## Recent upstream merges

Automatically refreshed from public GitHub data. Repositories are de-duplicated so one project cannot dominate the list.

- **[super-productivity/super-productivity#9173](https://github.com/super-productivity/super-productivity/pull/9173)** - fix(mobile): keep backlog add button round (2026-07-23)
- **[oclif/core#1628](https://github.com/oclif/core/pull/1628)** - feat: expose root help formatter (2026-07-23)
- **[Kong/kongctl#1655](https://github.com/Kong/kongctl/pull/1655)** - fix(declarative): enforce saved plan execution modes (2026-07-23)
- **[randovania/randovania#9412](https://github.com/randovania/randovania/pull/9412)** - Fix AM2R generation without nest pipes (2026-07-23)
- **[data-apis/array-api-extra#861](https://github.com/data-apis/array-api-extra/pull/861)** - ENH: add `nunique` delegation (2026-07-23)
- **[zarrs/zarrs#421](https://github.com/zarrs/zarrs/pull/421)** - feat(storage): add atomic write adapter (2026-07-23)

## Building now

- OpenCode and Codex interoperability that remains reliable under real account and session pressure
- MCP gateways, authentication, state visibility, and coding-agent performance instrumentation
- Production-grade APIs, data systems, CI, deployment pipelines, and failure recovery
- Technically substantive upstream fixes across compilers, runtimes, CLIs, storage, and infrastructure

## Stack

<p>
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white" alt="Node.js" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white" alt="Go" />
  <img src="https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white" alt="Rust" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions" />
  <img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black" alt="Linux" />
</p>

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/floze-the-genius/floze-the-genius/output/snake-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/floze-the-genius/floze-the-genius/output/snake.svg" />
    <img src="https://raw.githubusercontent.com/floze-the-genius/floze-the-genius/output/snake.svg" width="86%" alt="Contribution graph snake" />
  </picture>
</div>

<p align="center">
  <sub>Metrics are generated from authenticated public GitHub data. Engineering claims and selected work remain hand-reviewed.</sub>
</p>
