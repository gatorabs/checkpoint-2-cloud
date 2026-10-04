"""Descreve uma imagem (URL ou arquivo local) usando o Azure AI Vision."""
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("VISION_ENDPOINT", "").rstrip("/")
KEY = os.getenv("VISION_KEY", "")
API_URL = f"{ENDPOINT}/vision/v3.2/describe"


def descrever(origem: str, idioma: str = "pt") -> dict:
    params = {"maxCandidates": 3, "language": idioma}
    if origem.lower().startswith(("http://", "https://")):
        headers = {"Ocp-Apim-Subscription-Key": KEY, "Content-Type": "application/json"}
        resp = requests.post(API_URL, params=params, headers=headers, json={"url": origem})
    else:
        headers = {"Ocp-Apim-Subscription-Key": KEY, "Content-Type": "application/octet-stream"}
        with open(origem, "rb") as f:
            resp = requests.post(API_URL, params=params, headers=headers, data=f.read())
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if not ENDPOINT or not KEY:
        sys.exit("Defina VISION_ENDPOINT e VISION_KEY (veja .env.example).")
    if len(sys.argv) < 2:
        sys.exit("Uso: python app.py <URL-ou-caminho-da-imagem>")

    origem = sys.argv[1]
    print(f"Enviando imagem ao Serviço de Visão Computacional:\n  {origem}\n")
    resultado = descrever(origem)["description"]

    print("=== Descrição da imagem ===")
    for i, c in enumerate(resultado["captions"], 1):
        print(f"{i}. {c['text']}  (confiança: {c['confidence']:.1%})")
    print("\nTags:", ", ".join(resultado["tags"]))


if __name__ == "__main__":
    main()
