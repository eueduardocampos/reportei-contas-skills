#!/usr/bin/env python3
"""Copia os arquivos de base/ e o LICENSE para dentro de cada skill.

Cada skill precisa funcionar sozinha quando instalada, então leva uma cópia
dos arquivos de base que usa (em references/) e da licença. A fonte única
continua sendo base/ e o LICENSE da raiz; base/mapa.json diz o que vai
para onde.

Além das cópias, confere a estrutura: skill com SKILL.md fora do mapa.json
(ficaria sem LICENSE e sem referências), skill fora do marketplace.json e
arquivo sobrando em references/ (que não vem do mapa). Esses problemas não
são corrigidos sozinhos: o script lista e sai com erro.

Uso:
    python3 scripts/sincronizar.py            copia e confere a estrutura
    python3 scripts/sincronizar.py --check    só confere, sai com erro se
                                              alguma cópia estiver velha ou
                                              a estrutura tiver problema
"""

import json
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "base"
SKILLS = RAIZ / "skills"
MARKETPLACE = RAIZ / ".claude-plugin" / "marketplace.json"


def ler_mapa():
    return json.loads((BASE / "mapa.json").read_text(encoding="utf-8"))


def pares(mapa):
    """Gera (origem, destino) para tudo que deve existir dentro das skills."""
    for skill, arquivos in mapa.items():
        pasta = SKILLS / skill
        if not (pasta / "SKILL.md").exists():
            sys.exit(f"mapa.json cita {skill}, mas skills/{skill}/SKILL.md não existe")
        yield RAIZ / "LICENSE", pasta / "LICENSE"
        for nome in arquivos:
            yield BASE / nome, pasta / "references" / nome


def problemas_de_estrutura(mapa):
    """Lista o que as cópias não resolvem: skills fora do mapa ou do
    marketplace e arquivos sobrando em references/."""
    problemas = []
    listadas = None
    if MARKETPLACE.exists():
        mercado = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        listadas = {
            Path(caminho).name
            for plugin in mercado.get("plugins", [])
            for caminho in plugin.get("skills", [])
        }
    else:
        problemas.append(f"não encontrado: {MARKETPLACE.relative_to(RAIZ)}")
    for pasta in sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").exists()):
        if pasta.name not in mapa:
            problemas.append(f"fora do mapa.json: skills/{pasta.name}")
            continue
        if listadas is not None and pasta.name not in listadas:
            problemas.append(f"fora do marketplace.json: skills/{pasta.name}")
        refs = pasta / "references"
        if refs.is_dir():
            for arquivo in sorted(refs.iterdir()):
                if arquivo.name not in mapa[pasta.name]:
                    problemas.append(f"sobrando (não está no mapa.json): {arquivo.relative_to(RAIZ)}")
    return problemas


def main():
    so_conferir = "--check" in sys.argv
    mapa = ler_mapa()
    velhos = []
    for origem, destino in pares(mapa):
        if not origem.exists():
            sys.exit(f"origem não encontrada: {origem.relative_to(RAIZ)}")
        igual = destino.exists() and destino.read_bytes() == origem.read_bytes()
        if igual:
            continue
        if so_conferir:
            velhos.append(destino.relative_to(RAIZ))
        else:
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(origem, destino)
            print(f"atualizado: {destino.relative_to(RAIZ)}")
    problemas = problemas_de_estrutura(mapa)
    if velhos:
        print("cópias desatualizadas (rode sem --check):")
        for caminho in velhos:
            print(f"  {caminho}")
    if problemas:
        print("problemas de estrutura (corrija à mão e rode de novo):")
        for problema in problemas:
            print(f"  {problema}")
    if velhos or problemas:
        sys.exit(1)
    if so_conferir:
        print("tudo sincronizado")


if __name__ == "__main__":
    main()
