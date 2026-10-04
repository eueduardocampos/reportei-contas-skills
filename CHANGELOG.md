# Changelog

Mudanças relevantes deste projeto. O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e a numeração segue o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.1.1] - 2026-10-04

Muda a licença e a assinatura. As skills são as mesmas da 0.1.0.

### Alterado

- **Licença MIT**, em nome de Eduardo Campos. Uso livre e gratuito, inclusive comercial, com o aviso de licença mantido. A 0.1.0 saiu sob a "Licença de Uso Astronauta Martech 1.0"; a partir desta versão vale a MIT.
- **Autoria:** as skills passam a ser de Eduardo Campos, validadas ao vivo na Astronauta Martech.
- **Novo endereço do repositório:** github.com/eueduardocampos/reportei-contas-skills. O endereço antigo redireciona.
- A página do pacote no site da Astronauta saiu do ar; o README é a referência.

## [0.1.0] - 2026-10-01

Primeira versão, convertida para o formato de skills instaláveis e testada ao vivo com o conector oficial do Reportei.

### Adicionado

- **12 skills** em `skills/`: 5 criam, alteram ou apagam algo na conta, sempre com confirmação.
- **Base de conhecimento em `base/`**, copiada para dentro de cada skill: conector do Reportei, métricas e integrações, segurança de escrita, disciplina de evidência e formato de resposta.
- Manifesto do marketplace do Claude Code em `.claude-plugin/marketplace.json`, com o plugin `reportei-contas`.
- Script `scripts/sincronizar.py`.
