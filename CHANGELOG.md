# Changelog

Mudanças relevantes deste projeto. O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e a numeração segue o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.1.0] - 2026-10-01

Primeira versão, convertida para o formato de skills instaláveis e testada ao vivo com o conector oficial do Reportei.

### Adicionado

- **12 skills** em `skills/`: 5 criam, alteram ou apagam algo na conta, sempre com confirmação.
- **Base de conhecimento em `base/`**, copiada para dentro de cada skill: conector do Reportei, métricas e integrações, segurança de escrita, disciplina de evidência e formato de resposta.
- Manifesto do marketplace do Claude Code em `.claude-plugin/marketplace.json`, com o plugin `reportei-contas`.
- Script `scripts/sincronizar.py`.
