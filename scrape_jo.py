"""
Script para fazer scraping do livro de Jó - Bíblia NAA
Site: bible.com
Capítulos: 10 a 42 (1-9 já foram baixados manualmente)

Este script baixa os capítulos e formata o texto para que cada versículo
fique em uma única linha (sem quebras de linha no meio do versículo).
"""

import os
import time
import re
import ssl
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Desabilitar avisos de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['WDM_SSL_VERIFY'] = '0'

# Configurações
BASE_URL = "https://www.bible.com/pt/bible/1840/JOB.{chapter}.NAA"
OUTPUT_DIR = r"c:\RENE\PROJETOS\JO\TEXTO"
START_CHAPTER = 10  # Começar do capítulo 10 (1-9 já foram baixados)
END_CHAPTER = 42

def setup_driver():
    """Configura o driver do Chrome com opções otimizadas."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Tentando com webdriver-manager: {e}")
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

def format_text(text, chapter):
    """
    Formata o texto para que cada versículo fique em uma única linha.
    Mantém títulos de seção em linhas separadas.
    """
    lines = text.split('\n')
    result = []
    current_verse = []
    current_verse_num = None
    
    for line in lines:
        line = line.strip()
        if not line:
            # Linha vazia - finalizar versículo atual se houver
            if current_verse:
                result.append(' '.join(current_verse))
                current_verse = []
                current_verse_num = None
            result.append('')
            continue
        
        # Verificar se a linha começa com um número de versículo
        verse_match = re.match(r'^(\d+)\s*(.*)$', line)
        
        if verse_match:
            # Nova linha com número de versículo
            verse_num = verse_match.group(1)
            verse_text = verse_match.group(2)
            
            # Finalizar versículo anterior
            if current_verse:
                result.append(' '.join(current_verse))
            
            # Iniciar novo versículo
            current_verse = [f"{verse_num} {verse_text}"]
            current_verse_num = verse_num
        else:
            # Linha sem número de versículo
            # Verificar se é um título de seção (não começa com letra minúscula, aspas ou apóstrofo)
            # Verificar se é um título de seção
            starts_with_quote = line[0] in '"\'"\'"—-'
            is_title = (
                not current_verse_num and 
                not starts_with_quote and
                (line[0].isupper() or not line[0].isalpha())
            )
            
            if is_title and not current_verse:
                # É um título de seção - adicionar como está
                result.append(line)
            elif current_verse:
                # Continuação do versículo atual
                current_verse.append(line)
            else:
                # Linha avulsa (provavelmente título)
                result.append(line)
    
    # Finalizar último versículo se houver
    if current_verse:
        result.append(' '.join(current_verse))
    
    # Limpar linhas vazias duplicadas
    cleaned = []
    prev_empty = False
    for line in result:
        if line == '':
            if not prev_empty:
                cleaned.append(line)
            prev_empty = True
        else:
            cleaned.append(line)
            prev_empty = False
    
    # Garantir cabeçalho correto
    final_text = '\n'.join(cleaned).strip()
    if not final_text.startswith(f"Jó {chapter}"):
        final_text = f"Jó {chapter}\n\n" + final_text
    
    return final_text

def extract_chapter_text(driver, chapter):
    """Extrai o texto de um capítulo específico."""
    url = BASE_URL.format(chapter=chapter)
    print(f"Acessando capítulo {chapter}...")
    
    driver.get(url)
    
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='ChapterContent']"))
        )
    except:
        print(f"  Aviso: Timeout aguardando conteúdo do capítulo {chapter}")
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1.5)
    
    try:
        selectors = [
            ".ChapterContent_chapter__uvbXo",
            "[class*='ChapterContent_chapter']",
            "[class*='ChapterContent']",
            "main"
        ]
        
        text = None
        for selector in selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text
                if text and len(text) > 100:
                    break
            except:
                continue
        
        if not text:
            print(f"  Erro: Não foi possível extrair o texto do capítulo {chapter}")
            return None
        
        # Limpar navegação
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            if re.match(r'^JÓ \d+$', line.strip()):
                continue
            if line.strip() == 'JÓ':
                continue
            cleaned_lines.append(line)
        
        text = '\n'.join(cleaned_lines).strip()
        
        # Formatar o texto (consolidar versículos em linhas únicas)
        text = format_text(text, chapter)
        
        return text
        
    except Exception as e:
        print(f"  Erro ao extrair capítulo {chapter}: {e}")
        return None

def save_chapter(chapter, text):
    """Salva o texto do capítulo em um arquivo."""
    filename = os.path.join(OUTPUT_DIR, f"Jo_{chapter:02d}.txt")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"  Salvo: Jo_{chapter:02d}.txt")

def main():
    """Função principal."""
    print("=" * 50)
    print("Scraping do Livro de Jó - Bíblia NAA")
    print("=" * 50)
    print(f"Capítulos a baixar: {START_CHAPTER} a {END_CHAPTER}")
    print(f"Diretório de saída: {OUTPUT_DIR}")
    print()
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Iniciando navegador...")
    driver = setup_driver()
    print("Navegador iniciado com sucesso!")
    print()
    
    try:
        successful = 0
        failed = 0
        
        for chapter in range(START_CHAPTER, END_CHAPTER + 1):
            text = extract_chapter_text(driver, chapter)
            
            if text:
                save_chapter(chapter, text)
                successful += 1
            else:
                failed += 1
            
            time.sleep(0.5)
        
        print()
        print("=" * 50)
        print(f"Concluído!")
        print(f"Capítulos baixados com sucesso: {successful}")
        print(f"Capítulos com erro: {failed}")
        print("=" * 50)
        
    finally:
        driver.quit()
        print("Navegador fechado.")

if __name__ == "__main__":
    main()
