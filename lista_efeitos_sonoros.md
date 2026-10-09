# Lista de efeitos sonoros — Proteja Equinópolis

Pasta: `game/audio/`. Formato: `.ogg` (ou `.mp3`/`.wav`/`.opus`). Nomes em minúsculas, sem espaços.
Duração sugerida: 0,1–0,5 s para cliques; até 2–3 s para fanfarras.
**Status:** ✅ já chamado no código (só falta o arquivo) · ➕ novo (eu ligo no código quando você mandar o som).
Dica: se faltar o arquivo, o jogo continua sem som.

## Interface
| Arquivo | Quando toca | Status |
|---|---|---|
| `sfx_hover.ogg` | passar o mouse num botão | ✅ |
| `sfx_click.ogg` | clicar num botão | ✅ |
| `sfx_locked.ogg` | clicar em node trancado / Continuar sem save | ➕ |
| `sfx_back.ogg` | botão Voltar / fechar janela | ➕ |
| `sfx_window_open.ogg` | abrir Opções, Conquistas, pausa | ➕ |
| `sfx_window_close.ogg` | fechar essas janelas | ➕ |
| `sfx_start.ogg` | confirmar Novo jogo | ➕ |

## Mapa e progresso
| Arquivo | Quando toca | Status |
|---|---|---|
| `sfx_node_unlock.ogg` | node novo desbloqueado | ➕ |
| `sfx_node_done.ogg` | minigame concluído (carimbo) | ➕ |
| `sfx_medal.ogg` | resultado perfeito (medalha) | ➕ |
| `sfx_achievement.ogg` | aviso de conquista (toast) | ➕ |
| `sfx_final.ogg` | conquista final "Salvou Equinópolis" | ➕ |

## Acerto, erro e resultado (todos os minigames)
| Arquivo | Quando toca | Status |
|---|---|---|
| `sfx_correct.ogg` | resposta/ação certa | ✅ |
| `sfx_wrong.ogg` | resposta/ação errada | ✅ |
| `sfx_win.ogg` | tela de resultado: vitória | ✅ |
| `sfx_lose.ogg` | tela de resultado: derrota (ex.: 4º erro no mg1) | ➕ |
| `sfx_score_tick.ogg` | pontuação contando na tela de resultado | ➕ |
| `sfx_pick.ogg` | pegar um item arrastável | ➕ |
| `sfx_drop.ogg` | soltar/encaixar item | ➕ |

## Cavalo
| Arquivo | Quando toca | Status |
|---|---|---|
| `sfx_horse_angry.ogg` | cavalo irritado/assustado | ✅ |
| `sfx_horse_calm.ogg` | relincho/bufar calmo (mg2, mg3) | ➕ |

## Por minigame
| Arquivo | Minigame | Quando toca | Status |
|---|---|---|---|
| `sfx_stethoscope.ogg` | 2 | usar estetoscópio/termômetro | ➕ |
| `sfx_tube.ogg` | 3 | escolher/encaixar o tubo (vidro) | ➕ |
| `sfx_paper.ogg` | 3 | preencher a ficha | ➕ |
| `sfx_cooler.ogg` | 3 | fechar a caixa isotérmica (gelo) | ➕ |
| `sfx_bubbles.ogg` | 4 | misturar reagentes | ➕ |
| `sfx_pipette.ogg` | 4 | pingar com a pipeta | ➕ |
| `sfx_spectro.ogg` | 4 | leitura do espectrofotômetro | ➕ |
| `sfx_gate.ogg` | 5 | porteira abrindo/fechando | ➕ |
| `sfx_fly_buzz.ogg` | 6 | mosca entrando (zumbido em loop curto) | ➕ |
| `sfx_fly_swat.ogg` | 6 | tapa na mosca hematófaga | ➕ |
| `sfx_fly_oops.ogg` | 6 | clicar na mosca inofensiva (penalidade) | ➕ |
| `sfx_needle_open.ogg` | 7 | abrir agulha nova (plástico) | ➕ |
| `sfx_needle_bin.ogg` | 7 | descartar no coletor de perfurocortantes | ➕ |

## Ambiente (loops baixinhos, tocam por baixo da música)
| Arquivo | Onde | Status |
|---|---|---|
| `amb_countryside.ogg` | menu e mapa (pássaros, vento) | ➕ |

**Prioridade para começar (5):** `sfx_click`, `sfx_hover`, `sfx_correct`, `sfx_wrong` e `sfx_win` (já ligados); depois `sfx_locked`, `sfx_medal`, `sfx_achievement` e `sfx_fly_buzz`.
