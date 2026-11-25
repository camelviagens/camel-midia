# Ferramentas de vídeo da Camel Viagens
Scripts usados pelas skills de vídeo (preços e conteúdo). Rodam no ambiente do Claude (Python + PIL + ffmpeg).
- sent.py: divide a narração em frases (silencedetect) para sincronizar.
- top_gen.py + ovlib.py + endcard.py + capa2.py: vídeo "Top N" de preços (config JSON; exemplo em exemplo_cfg_top_aereo.json).
- dicas_assets.py + dicas_build.py: vídeo de conteúdo "N dicas" de destino.
- cartao_assets.py + cartao_build.py: formato "cartão de embarque".
- painel_board.py + painel_build.py: formato "painel de partidas".
- tutorial/: telas do tutorial de cotação (tut1_0…tut3_2.png). end_cotacao.png: tela final.
- assets/logo_camel.png
Fontes: Poppins (google-fonts) e DejaVu Sans Mono. Os caminhos nos scripts apontam para /home/claude/... — ajuste ao clonar.
