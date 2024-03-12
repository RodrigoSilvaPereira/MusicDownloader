from pytube import YouTube  # Importa a classe YouTube da biblioteca pytube
import os  # Importa o módulo os para operações relacionadas ao sistema operacional
import requests  # Importa o módulo requests para fazer requisições HTTP
import re  # Importa o módulo re para trabalhar com expressões regulares
import subprocess  # Importa o módulo subprocess para executar comandos no sistema operacional

def instalar_bibliotecas():
    """
    Instala as bibliotecas necessárias (pytube e requests) utilizando o pip.
    """
    try:
        subprocess.check_call(['pip', 'install', 'pytube', 'requests'])
        print("Bibliotecas instaladas com sucesso!")
    except subprocess.CalledProcessError:
        print("Erro ao instalar bibliotecas. Certifique-se de ter o pip instalado.")

def pesquisar_video(nome):
    """
    Pesquisa o vídeo no YouTube com base no nome da música fornecido.
    
    Args:
        nome (str): Nome da música a ser pesquisada.
    
    Returns:
        str: URL do vídeo encontrado no YouTube.
    """
    try:
        nome = nome.replace(' ', '+')
        pag = requests.get(f"https://www.youtube.com/results?search_query={nome}").text
        video_id = str(pag).split('{"videoId":"')[1].split('"')[0]
        link = f"https://www.youtube.com/watch?v={video_id}"
        return link
    except Exception as err:
        print(f'Ocorreu um erro: {err}')
        return None

def baixar_musica(link):
    """
    Baixa o áudio do vídeo do YouTube e salva como um arquivo MP3.
    
    Args:
        link (str): URL do vídeo do YouTube.
    """
    try:
        video = YouTube(link)
        titulo = video.title
        # Remover caracteres especiais do título
        titulo = re.sub(r'[\\/*?:"<>|]', '', titulo)
        print(f'[+] Baixando: {titulo}')

        if not os.path.exists('musicas'):
            os.makedirs('musicas')  # Criar a pasta "musicas" se não existir

        if os.path.exists(f"musicas/{titulo}.mp3"):
            os.remove(f"musicas/{titulo}.mp3")

        yt = video.streams.filter(only_audio=True).first().download(output_path='musicas')
        
        print('[+] Iniciando processo de conversão..')
        novo_nome = f"musicas/{titulo}.mp3"
        os.rename(yt, novo_nome)
        print('[+] Convertido!')

    except Exception as err:
        print(f'Ocorreu um erro: {err}')

def adicionar_musica(playlist_links):
    """
    Adiciona músicas à playlist.
    
    Args:
        playlist_links (list): Lista de URLs das músicas na playlist.
    """
    while True:
        nome_musica = input('Digite o nome da música ou "fim" para parar: ').strip()
        if nome_musica.lower() == 'fim':
            break
        link = pesquisar_video(nome_musica)
        if link:
            playlist_links.append(link)
            # Adicionar o link ao arquivo da playlist
            with open('playlist.txt', 'a') as file:
                file.write(link + '\n')
            print(f'Música "{nome_musica}" adicionada à playlist.')
        else:
            print('Não foi possível encontrar a música. Tente novamente.')

def excluir_musica(playlist_links):
    """
    Exclui músicas da playlist.
    
    Args:
        playlist_links (list): Lista de URLs das músicas na playlist.
    """
    if not playlist_links:
        print('A playlist está vazia.')
        return
    print('[+] Músicas na playlist:')
    for i, link in enumerate(playlist_links):
        print(f"{i+1} - {YouTube(link).title}")
    try:
        indice = int(input('Digite o número da música que deseja excluir: ')) - 1
        if 0 <= indice < len(playlist_links):
            del playlist_links[indice]
            print('Música excluída da playlist.')
        else:
            print('Número inválido.')
    except ValueError:
        print('Por favor, digite um número válido.')

def criar_playlist():
    """
    Cria uma playlist interativa.
    """
    playlist_links = []
    print('Bem-vindo ao Music Download - Criador de Playlist!')
    while True:
        print('\nEscolha uma opção:')
        print('1. Adicionar música à playlist')
        print('2. Excluir música da playlist')
        print('3. Iniciar o download das músicas')
        print('4. Sair')
        opcao = input('Digite o número da opção desejada: ').strip()
        if opcao == '1':
            adicionar_musica(playlist_links)
        elif opcao == '2':
            excluir_musica(playlist_links)
        elif opcao == '3':
            if playlist_links:
                # Se houver músicas na playlist, inicie o download
                print('[+] Playlist salva em playlist.txt')
                baixar_playlist('playlist.txt')
                os.remove('playlist.txt')  # Remover o arquivo da playlist após o download
                break
            else:
                print('A playlist está vazia. Adicione músicas antes de iniciar o download.')
        elif opcao == '4':
            print('Saindo...')
            break
        else:
            print('Opção inválida. Por favor, escolha uma opção válida.')

def baixar_playlist(nome_arquivo):
    """
    Baixa as músicas da playlist.
    
    Args:
        nome_arquivo (str): Nome do arquivo de playlist.
    """
    # Código para baixar a playlist
    if os.path.exists(nome_arquivo):
        try:
            with open(nome_arquivo, 'r') as file:
                for link in file:
                    baixar_musica(link.strip())
        except Exception as err:
            print(f'Ocorreu um erro: {err}')
    else:
        print(f'O arquivo da playlist "{nome_arquivo}" não foi encontrado.')

# Exemplo de uso:
criar_playlist()