# 🏠 Telegram Bot: Alertas de Vagas Home Office

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Telegram API](https://img.shields.io/badge/Telegram_API-Bot-0088cc?style=for-the-badge&logo=telegram&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-Web_Scraping-green?style=for-the-badge)

Um robô autônomo desenvolvido em Python que monitora diariamente a publicação de novas oportunidades de trabalho remoto, extrai os dados relevantes de forma inteligente e dispara alertas formatados diretamente em um grupo público do Telegram.

---

## 🎯 O Objetivo
Encontrar vagas 100% remotas de qualidade pode ser um desafio demorado. Este projeto nasceu para automatizar a curadoria dessas oportunidades, ajudando profissionais a receberem alertas em tempo real no celular, sem precisarem atualizar dezenas de sites de emprego todos os dias.

👉 **[Participe do Grupo Oficial no Telegram e receba os alertas ao vivo!](https://t.me/+n7fRlAV2BE5lYmYx)**

---

## 👀 Preview do Projeto

*(Substitua esta imagem por um print do seu grupo do Telegram recebendo as vagas)*
<div align="center">
  <img src="https://via.placeholder.com/800x400.png?text=Coloque+aqui+um+print+do+seu+grupo+recebendo+as+vagas" alt="Demonstração do Bot no Telegram">
</div>

---

## ✨ Principais Funcionalidades

- **Web Scraping Rápido:** Utiliza a biblioteca `requests` e `BeautifulSoup` para mapear dezenas de páginas em segundos, sem a necessidade de instanciar navegadores pesados.
- **Filtro Anti-Anúncios:** Lógica inteligente para identificar e ignorar anúncios nativos (Native Ads) disfarçados de vagas dentro do site.
- **Prevenção de Duplicidade:** Banco de dados integrado (`SQLite`) que memoriza o histórico de vagas e atua como "freio" de segurança, garantindo que os usuários não recebam a mesma vaga duas vezes.
- **Formatador HTML Seguro:** Integração com a API do Telegram utilizando formatação HTML para evitar quebra de mensagens por caracteres especiais nos títulos das vagas.
- **Proteção de Rate Limit:** Sistema de pausas estratégicas (throttling) que respeita as diretrizes de anti-spam da API do Telegram (Tratamento de Erro 429).
- **Execução Oculta (Background):** Script em `.bat` configurado para rodar de forma invisível via Agendador de Tarefas do Windows.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3** (Linguagem base)
* **BeautifulSoup4** (Parseamento do HTML)
* **Requests** (Requisições HTTP)
* **SQLite3** (Banco de dados nativo)
* **Python-dotenv** (Gestão de credenciais seguras)
* **Telegram Bot API** (Disparo de mensagens)

---

## 🚀 Como clonar e executar este projeto

Se você deseja rodar o robô na sua própria máquina ou adaptá-lo para outros sites, siga os passos abaixo:

### 1. Clone o repositório
```bash
git clone [https://github.com/lucasnunestrabalho99-sudo/nome-do-seu-repositorio.git](https://github.com/lucasnunestrabalho99-suudo/telegram-vagas-home-office.bot.git)
cd telegram-vagas-home-office.bot
```

### 2. Crie e ative um Ambiente Virtual
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto e adicione as suas credenciais do Telegram (nunca suba este arquivo para o GitHub):
```env
TELEGRAM_TOKEN=seu_token_gerado_no_botfather
CHAT_ID_GRUPO=-100_id_do_seu_supergrupo
```

### 5. Execute o robô
```bash
python main.py
```

---

## ⚙️ Automação no Windows (Agendador de Tarefas)
Para manter o robô rodando 24/7 sem interrupções, o projeto conta com um arquivo `rodar.bat` projetado para auto-minimizar a janela do terminal. Basta apontar o Agendador de Tarefas do Windows para este arquivo e configurar a repetição para o intervalo desejado (ex: a cada 30 minutos).

---
