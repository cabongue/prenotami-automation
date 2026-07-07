# Prenotami Automation 🇮🇹

Ferramenta Python para automatizar agendamento de **Primeiro Passaporte Italiano** no Prenot@mi.

> **⚠️ Importante:** Esta ferramenta é para uso pessoal exclusivo. O Prenot@mi combate automações indevidas. Use responsavelmente.

## Funcionalidades

✅ Login automático com credenciais  
✅ Preenchimento automático do formulário de passaporte  
✅ Upload de documentos (RG, comprovante de residência)  
✅ Seleção automática de data/hora disponível  
✅ Tenta múltiplas vezes se necessário  
✅ Burla detecção de bots com `undetected-chromedriver`  
✅ Logs em tempo real  

## Requisitos

- Python 3.8+
- Chrome/Chromium instalado
- Conexão estável com internet

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/cabongue/prenotami-automation.git
cd prenotami-automation
```

### 2. Crie ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale dependências

```bash
pip install -r requirements.txt
```

### 4. Configure os arquivos necessários

```bash
# Crie a pasta de arquivos
mkdir files

# Crie o arquivo .env com suas credenciais
cp .env.example .env
```

## Configuração

### 1. Credenciais (`.env`)

Edite o arquivo `.env`:
```
USERNAME=seu.email@exemplo.com
PASSWORD=sua.senha.aqui
```

### 2. Parâmetros Pessoais (`parameters.yaml`)

Edite o arquivo `parameters.yaml` com seus dados:

```yaml
request_type: "passport"  # ou "citizenship"

# Dados pessoais
full_name: "Seu Nome Completo"
full_address: "Rua Exemplo, 123, São Paulo, SP, Brasil"

# Perguntas do formulário
possess_expired_passport: "Sim"  # ou "Não"
total_children: "0"
marital_status: "Solteiro"  # Solteiro, Casado, Divorciado, Viúvo

# Consulado
consulate: "São Paulo"  # São Paulo, Rio de Janeiro, Brasília, etc.
```

### 3. Documentos Necessários

Crie a pasta `files/` e adicione:

- **identidade.pdf** - Cópia do RG ou documento de identidade
- **residencia.pdf** - Comprovante de residência recente (conta de água, luz, etc.)

```bash
files/
├── identidade.pdf
└── residencia.pdf
```

## Como Usar

### Execução simples

```bash
python main.py
```

O script irá:
1. Fazer login no Prenot@mi
2. Preencher automaticamente o formulário de passaporte
3. Upload de documentos
4. Selecionar primeira data/hora disponível
5. Confirmar agendamento
6. Deixar o navegador aberto para você confirmar

## Logs

Os logs são salvos em `/tmp/out.log` (Linux/Mac) ou no console.

Verifique:
```bash
tail -f /tmp/out.log  # Linux/Mac
```

## Troubleshooting

### Chrome não encontrado

```bash
# Linux
sudo apt-get install chromium-browser

# Mac
brew install chromium
```

### Arquivo de documentos não encontrado

Certifique-se que os PDFs estão em `files/`:
```bash
ls -la files/
# Deve mostrar identidade.pdf e residencia.pdf
```

### CAPTCHA bloqueando

O `undetected-chromedriver` tenta contornar, mas pode precisar de resolução manual.

## Limitações

- ⚠️ CAPTCHAs podem bloquear em algumas situações
- ⚠️ Prenot@mi muda constantemente, pode quebrar seletores
- ⚠️ Vagas são muito limitadas e esgotam rápido
- ⚠️ Sistema pode adicionar novas proteções anti-bot

## Suporte

Este projeto é baseado no trabalho de [handreassa/prenotami](https://github.com/handreassa/prenotami).

## Disclaimer

**USE POR SUA CONTA E RISCO**

Esta ferramenta é fornecida "como está". O autor não é responsável por:
- ❌ Bloqueio de conta
- ❌ Violação de termos de serviço
- ❌ Qualquer prejuízo decorrente do uso
- ❌ Multas ou problemas legais

**Use apenas para fins legítimos, pessoais e éticos.**

O Prenot@mi combate ativas automações não autorizadas. Respeite os termos de serviço.

## Licença

MIT License - Veja LICENSE para detalhes
