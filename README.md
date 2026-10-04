# Descrição de imagens com Azure AI Vision

App Python que envia uma imagem (URL ou arquivo local) ao serviço `visao-inova-rm94581`
(grupo `rg-vc-inova`, SKU Free) e exibe a descrição retornada.

## Uso
```
pip install -r requirements.txt
copy .env.example .env   # preencha VISION_KEY
python app.py https://exemplo.com/foto.jpg
python app.py minha_foto.jpg
```
