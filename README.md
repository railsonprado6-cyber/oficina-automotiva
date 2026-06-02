# Sistema de Gestão para Oficina Automotiva

Sistema completo, profissional e robusto para gerenciamento de oficina automotiva com interface gráfica intuitiva, funcionalidade multi-terminal em rede local, estoque integrado e geração de ordens de serviço em PDF.

## 🎯 Características Principais

- ✅ **Busca Rápida por Placa** - Acesso instantâneo ao histórico completo do veículo
- ✅ **Gestão de Clientes e Veículos** - Cadastro completo com rastreamento
- ✅ **Ordens de Serviço** - Criar, editar, concluir e imprimir em PDF
- ✅ **Histórico de Serviços** - Registro detalhado com técnico, peças e valores
- ✅ **Estoque Integrado** - Controle de entrada/saída com baixa automática
- ✅ **Multi-Terminal em Rede** - Sincronização em tempo real entre computadores
- ✅ **Sistema de Usuários** - Permissões por nível (Admin, Atendente, Técnico, Estoque)
- ✅ **Relatórios Completos** - Faturamento, peças, histórico por cliente/período
- ✅ **Alertas Inteligentes** - Estoque baixo, OS vencidas, histórico de veículo
- ✅ **Backup Automático** - Proteção de dados com rotinas diárias

## 📊 Tecnologia

- **Backend**: FastAPI + SQLAlchemy (Python)
- **Frontend**: PyQt6 (Interface gráfica nativa Windows)
- **Banco de Dados**: PostgreSQL (com suporte local SQLite)
- **Relatórios**: ReportLab + FPDF2 (PDF profissional)
- **Instalador**: PyInstaller + NSIS (Windows Setup)

## 📁 Estrutura do Projeto

```
oficina-automotiva/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   └── services/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── main.py
│   ├── ui/
│   │   ├── windows/
│   │   ├── widgets/
│   │   └── styles/
│   ├── services/
│   └── requirements.txt
├── database/
│   ├── migrations/
│   └── seeds/
├── installer/
│   └── setup.nsi
├── docs/
│   ├── INSTALACAO.md
│   ├── MANUAL_USUARIO.md
│   └── API.md
└── requirements.txt
```

## 🚀 Instalação Rápida

### 1. Pré-requisitos
- Windows 10 ou superior
- Python 3.10+
- PostgreSQL 12+ (ou usar SQLite local)

### 2. Clonar Repositório
```bash
git clone https://github.com/railsonprado6-cyber/oficina-automotiva.git
cd oficina-automotiva
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Banco de Dados
```bash
cp .env.example .env
# Editar .env com suas configurações
python backend/setup_db.py
```

### 5. Iniciar Sistema
```bash
# Terminal 1 - Backend
python backend/run.py

# Terminal 2 - Frontend (esperar backend iniciar)
python frontend/main.py
```

## 📖 Documentação

- [Instalação Completa](docs/INSTALACAO.md)
- [Manual do Usuário](docs/MANUAL_USUARIO.md)
- [Documentação da API](docs/API.md)
- [Guia Multi-Terminal](docs/REDE.md)

## 👥 Permissões de Usuário

| Permissão | Admin | Atendente | Técnico | Estoque |
|-----------|-------|-----------|---------|---------|
| Clientes | ✅ | ✅ | ❌ | ❌ |
| Veículos | ✅ | ✅ | ✅ | ❌ |
| OS | ✅ | ✅ | ✅ | ❌ |
| Serviços | ✅ | ❌ | ✅ | ❌ |
| Estoque | ✅ | ❌ | ❌ | ✅ |
| Relatórios | ✅ | ✅ | ❌ | ❌ |
| Usuários | ✅ | ❌ | ❌ | ❌ |

## 📞 Suporte

Para dúvidas, abra uma [Issue](https://github.com/railsonprado6-cyber/oficina-automotiva/issues)

## 📄 Licença

MIT License - veja LICENSE para detalhes

---

**Desenvolvido com ❤️ para oficinas automotivas**
