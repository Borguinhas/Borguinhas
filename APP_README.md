
# Albion Market Master (Europe Server)

## Visão Geral
O **Albion Market Master** é uma aplicação desktop para Windows, desenvolvida em Python 3.11+, focada na arbitragem de mercado em tempo real para o servidor **Europeu** do Albion Online. A aplicação utiliza a API do [Albion Online Data Project](https://www.albion-online-data.com/) para identificar oportunidades de lucro entre cidades e o Black Market.

## Funcionalidades Principais
- **Foco no Servidor Europeu**: Todas as chamadas de API são restritas ao servidor Europe.
- **Arquitetura MVC**: Separação estrita entre lógica de negócio, dados e interface.
- **Cálculo Determinístico**: Considera taxas de premium, lixo (trash rate) do Black Market e impostos.
- **Interface Moderna**: Construída com `customtkinter` para uma experiência de utilizador fluida e responsiva.
- **Notificações em Tempo Real**: Alertas no Windows para oportunidades de arbitragem que superem o limite de ROI configurado.
- **Persistência de Dados**: Base de dados SQLite para armazenamento local de preços históricos.

## Arquitetura do Projeto
```text
/app
  main.py                # Ponto de entrada da aplicação
/config
  constants.py           # Configurações globais e limites
/data
  metadata_loader.py     # Gestão de itens e localizações (JSON)
  flip_loader.py         # Configuração de rotas de arbitragem
/database
  db_manager.py          # Gestão da base de dados SQLite
/models
  item.py                # Modelo de dados de itens (@dataclass)
  price.py               # Modelo de dados de preços (@dataclass)
  trade.py               # Modelo de dados de transações (@dataclass)
/services
  api_client.py          # Cliente API com suporte a retries e batching
  arbitrage_engine.py    # Motor de cálculo de lucro e ROI
  notification_service.py # Serviço de notificações desktop
/ui
  main_window.py         # Janela principal da aplicação
  table_view.py          # Visualização de dados em tabela
/utils
  fuzzy_match.py         # Utilitário de correspondência de nomes
  logger.py              # Sistema de logs centralizado
```

## Requisitos de Instalação
- Python 3.11 ou superior
- Sistema Operativo: Windows (recomendado para notificações nativas)

### Instalação de Dependências
```bash
pip install -r requirements.txt
```

## Como Executar
Navegue até à pasta raiz do projeto e execute:
```bash
python app/main.py
```

## Regras de Negócio Implementadas
- **ROI Mínimo**: 3%
- **Spread Mínimo**: 3%
- **Taxa de Lixo (BM)**: 10%
- **Imposto Premium**: 4%
- **Filtro de Itens**: Apenas armas, armaduras e equipamentos para o Black Market.

## Referências
- [Albion Online Data Project API](https://www.albion-online-data.com/api/v2/)
- [Albion Online Wiki - Marketplace](https://wiki.albiononline.com/wiki/Marketplace)

---
*Desenvolvido por Manus AI para Borguinhas.*
