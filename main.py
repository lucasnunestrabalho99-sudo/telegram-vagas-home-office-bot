import os
import time
import sqlite3
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# --- 1. CONFIGURAÇÕES E CAMINHOS ---
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(DIRETORIO_ATUAL, '.env'))
CAMINHO_BANCO = os.path.join(DIRETORIO_ATUAL, 'vagas_querohome.db')

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID_GRUPO")

PALAVRAS_CHAVE = [
    "analista de dados", "business intelligence", "dados", "pricing", 
    "comercial", "vendas", "sdr", "bdr", "inside sales", "atendimento",
    "administrativo", "back office", "recepcionista", "suporte", "projetos"
] 

def vaga_nos_interessa(titulo):
    return True

# --- 2. BANCO DE DADOS ---
def iniciar_banco():
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vagas_enviadas (
            link TEXT PRIMARY KEY,
            data_publicacao TEXT,
            titulo TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

# --- 3. DISPARO PARA O TELEGRAM ---
def enviar_alerta_telegram(titulo, empresa, link, data, categoria):
    if not TOKEN or not CHAT_ID:
        print("❌ ERRO CRÍTICO: Token ou Chat ID não encontrados no .env!")
        return False

    mensagem = f"🏠 <b>NOVA VAGA HOME OFFICE!</b>\n\n" \
               f"💼 <b>Vaga:</b> {titulo}\n" \
               f"🏢 <b>Empresa:</b> {empresa}\n" \
               f"🏷️ <b>Categoria:</b> {categoria}\n" \
               f"📅 <b>Data:</b> {data}\n\n" \
               f"🔗 <a href='{link}'>Clique aqui para acessar</a>"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # parse_mode alterado para HTML
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML", "disable_web_page_preview": True}
    
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 429: 
            pausa = r.json().get('parameters', {}).get('retry_after', 30)
            print(f"⚠️ Rate Limit! Pausando por {pausa}s...")
            time.sleep(pausa)
            requests.post(url, json=payload, timeout=10)
            return True
        elif r.status_code == 200:
            print(f"✅ Telegram: {titulo[:40]}...")
            return True
        else:

            print(f"❌ Erro na API do Telegram: {r.status_code} - Detalhe: {r.text}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão com o Telegram: {e}")
        return False

# --- 4. MOTOR DE BUSCA PRINCIPAL ---
def buscar_vagas_home_office():
    print("🚀 Iniciando varredura no Quero Home...")
    conn, cursor = iniciar_banco()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    pagina_atual = 1
    vagas_velhas = 0
    LIMITE_VELHAS = 20
    LIMITE_PAGINAS = 200 
    
    while vagas_velhas < LIMITE_VELHAS and pagina_atual <= LIMITE_PAGINAS:
        print(f"Lendo Página {pagina_atual}...")
        url = f"https://www.querohome.com.br/arquivo?page={pagina_atual}"
        
        try:
            resposta = requests.get(url, headers=headers, timeout=15)
            
            if "Nenhuma vaga encontrada." in resposta.text:
                print("🛑 Fim da linha! O site não tem mais páginas com vagas.")
                break
                
            soup = BeautifulSoup(resposta.text, 'html.parser')
            artigos = soup.find_all('article', class_='post-card')
            
            if not artigos: break

            for artigo in artigos:
                h3 = artigo.find('h3', class_='card-title')
                if not h3 or not h3.find('a'): continue
                titulo = h3.find('a').text.strip()
                
                link_parcial = h3.find('a').get('href')
                link_completo = f"https://www.querohome.com.br{link_parcial}"
                
                empresa_tag = artigo.find('p', class_='card-company')
                empresa = empresa_tag.text.replace('🏢', '').strip() if empresa_tag else "Não informada"
                
                cat_tag = artigo.find('a', class_='card-badge')
                categoria = cat_tag.text.strip() if cat_tag else "Geral"
                
                time_tag = artigo.find('time')
                if not time_tag: continue
                data = time_tag.text.strip()

                cursor.execute('SELECT 1 FROM vagas_enviadas WHERE link = ?', (link_completo,))
                if cursor.fetchone():
                    vagas_velhas += 1
                    if vagas_velhas >= LIMITE_VELHAS: 
                        print(f"🛑 Limite de segurança atingido ({LIMITE_VELHAS} vagas antigas).")
                        break
                else:
                    vagas_velhas = 0 
                    cursor.execute('INSERT INTO vagas_enviadas VALUES (?, ?, ?)', (link_completo, data, titulo))
                    conn.commit()
                    
                    if vaga_nos_interessa(titulo):
                        enviar_alerta_telegram(titulo, empresa, link_completo, data, categoria)
                        time.sleep(2) # Pausa segura para envios sequenciais
                        
        except Exception as e:
            print(f"⚠️ Erro ao ler a página {pagina_atual}: {e}")
            
        pagina_atual += 1

    conn.close()
    print("✅ Varredura finalizada!")

if __name__ == '__main__':
    buscar_vagas_home_office()
