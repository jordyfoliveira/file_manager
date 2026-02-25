from text_analysis import top_words, top_words_format
from pathlib import Path
import logging
import csv

LOG_PATH = Path("logs") / "app.log"

def read_text_file(file_path: str) -> str:
    try:
        logging.info("A ler ficheiro (utf-8): %s", file_path) #Regista uma mensagem de log indicando que o ficheiro está a ser lido usando encoding UTF-8, incluindo o caminho do ficheiro para facilitar a identificação do processo de leitura nos logs
        with open(file_path, "r", encoding="utf-8") as file: #Tenta abrir o ficheiro usando encoding UTF-8, que é o padrão para a maioria dos ficheiros de texto e suporta uma ampla gama de caracteres, incluindo acentos. Isso é necessário para garantir que o texto seja lido corretamente, especialmente se contiver caracteres acentuados comuns em português.
            return file.read() #Lê o conteúdo do ficheiro e retorna como uma string
            #logging.info("A ler ficheiro: %s", file_path) #Regista uma mensagem de log indicando que o ficheiro está a ser lido, incluindo o caminho do ficheiro para facilitar a identificação do processo de leitura nos logs

    except FileNotFoundError: #Trata o erro de ficheiro não encontrado
        logging.error("Ficheiro não encontrado: %s", file_path) #Regista uma mensagem de log indicando que o ficheiro não foi encontrado, incluindo o caminho do ficheiro para facilitar a identificação do problema nos logs
        #print(f"Erro: ficheiro não encontrado -> {file_path}") #Exibe uma mensagem de erro indicando que o ficheiro não foi encontrado
        return "" #Retorna uma string vazia em caso de erro de ficheiro não encontrado
    
    except UnicodeDecodeError: #Trata o erro de decodificação, que pode ocorrer se o ficheiro não estiver codificado em UTF-8
        logging.warning("Falhou utf-8, a tentar latin-1: %s", file_path) #Regista uma mensagem de log indicando que a tentativa de leitura do ficheiro usando encoding UTF-8 falhou e que será feita uma nova tentativa usando encoding "latin-1", incluindo o caminho do ficheiro para facilitar a identificação do processo de leitura nos logs
        with open(file_path, "r", encoding="latin-1") as file: #Tenta abrir o ficheiro novamente usando encoding "latin-1" para lidar com caracteres acentuados, garantindo que o texto seja lido corretamente mesmo que não esteja codificado em UTF-8.
            return file.read() #Lê o conteúdo do ficheiro e retorna como uma string, usando encoding "latin-1" para garantir que caracteres acentuados sejam lidos corretamente. Isso é necessário para evitar erros de decodificação ao lidar com ficheiros que podem conter caracteres acentuados, especialmente em português.
            #logging.info("A ler ficheiro (latin-1): %s", file_path) #Regista uma mensagem de log indicando que o ficheiro está a ser lido usando encoding "latin-1", incluindo o caminho do ficheiro para facilitar a identificação do processo de leitura nos logs
    
    #except UnicodeDecodeError: #Trata o erro de decodificação, que pode ocorrer se o ficheiro não estiver codificado em UTF-8
    #    print("Erro: encoding inválido. Tenta 'utf-8' ou 'latin-1'.") #Exibe uma mensagem de erro indicando que o encoding é inválido e sugere opções de encoding
    #    return "" #Retorna uma string vazia em caso de erro de decodificação
    
def save_report(report: str, path: Path) -> None:
    #path = input("Introduza o caminho do ficheiro de saída: ")
    #path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)  # cria a pasta output/ se não existir
    path.write_text(report, encoding="utf-8") #Escreve a string report no ficheiro especificado por path, usando encoding UTF-8. Se o ficheiro já existir, ele será sobrescrito; caso contrário, um novo ficheiro será criado.
    
def save_csv(items: list[tuple[str, int]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)  # cria a pasta output/ se não existir
    with path.open("w", newline="", encoding="utf-8") as file: #Abre o ficheiro em modo de escrita, garantindo que as linhas sejam separadas corretamente e usando encoding UTF-8
        #file.write("rank,word,count\n") #Escreve a linha de cabeçalho no ficheiro CSV
        writer = csv.writer(file) #Cria um objeto writer do módulo csv para facilitar a escrita de linhas no formato CSV
        writer.writerow(["rank", "word", "count"]) #Escreve a linha de cabeçalho no ficheiro CSV
        for i, (word, count) in enumerate(items, 1): #Itera sobre a lista de tuplas (palavra, contagem) e escreve cada par no ficheiro CSV, separando-os por vírgula
            #file.write(f"{i},{word},{count}\n") #Escreve cada palavra e sua contagem em uma linha do ficheiro CSV, formatando-os como "rank,palavra,contagem"
            writer.writerow([i, word, count]) #Escreve cada palavra e sua contagem em uma linha do ficheiro CSV usando o objeto writer, formatando-os como "rank,palavra,contagem"
            
def setup_logging() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True) #cria a pasta logs/ se não existir

    logger = logging.getLogger() #Obtém o logger raiz para configurar os handlers e o nível de logging. O logger raiz é usado para garantir que todas as mensagens de log sejam capturadas, independentemente do módulo ou parte do código onde são geradas.
    logger.setLevel(logging.INFO) #Define o nível de logging para INFO, o que significa que mensagens de nível INFO e superiores (WARNING, ERROR, CRITICAL) serão registradas. Isso é necessário para garantir que as mensagens de log relevantes sejam capturadas e registradas no ficheiro de log e na consola, facilitando a identificação de eventos importantes e problemas durante a execução do programa.

    # limpa handlers antigos (útil no VS Code)
    logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s") #Cria um objeto Formatter para definir o formato das mensagens de log, incluindo a data e hora, o nível de log e a mensagem. Isso é necessário para garantir que as mensagens de log sejam formatadas de maneira consistente e informativa, facilitando a leitura e a análise dos logs.

    # 1) Log para ficheiro (INFO e acima)
    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(fmt)

    # 2) Log para consola (WARNING e acima)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
                
#def menu() -> str:
def menu() -> tuple[str, str]:
    while True:
        print("1 - Inserir texto manualmente") #Exibe um menu para o user escolher entre inserir texto manualmente ou ler de um ficheiro, permitindo que ele escolha a forma de entrada do texto a ser processado. O loop while True garante que o menu seja exibido repetidamente até que o user escolha uma opção válida.
        print("2 - Ler de ficheiro") #Exibe um menu para o user escolher entre inserir texto manualmente ou ler de um ficheiro, permitindo que ele escolha a forma de entrada do texto a ser processado. O loop while True garante que o menu seja exibido repetidamente até que o user escolha uma opção válida.
        option = input("Escolha uma opção (1 ou 2): ").strip() #Lê a opção escolhida pelo user, removendo espaços em branco extras, para determinar se o texto será inserido manualmente ou lido de um ficheiro. A função strip() é usada para garantir que a entrada do user seja limpa de espaços em branco antes de ser processada.
    
        logging.info("Opção escolhida: %s", option) #Regista uma mensagem de log indicando a opção escolhida pelo user, para facilitar a identificação do processo de escolha nos logs
        if option == "1": #Verifica se o user escolheu a opção de inserir texto manualmente
            text = input("Introduza o texto: ") #Lê o texto inserido manualmente pelo user
            while not text.strip(): #Verifica se o texto inserido é vazio ou contém apenas espaços em branco, e solicita ao user que insira um texto válido até que isso seja feito 
                print("Texto inválido. Por favor, insira um texto não vazio.") #Exibe uma mensagem de erro indicando que o texto inserido é inválido e solicita ao user que insira um texto válido
                text = input("Introduza o texto: ") #Lê o texto inserido manualmente pelo user, removendo espaços em branco extras, para garantir que a entrada seja limpa antes de ser processada
            return option, text #Retorna a opção escolhida e o texto inserido pelo user para ser processado posteriormente
        
        elif option == "2": #Verifica se o user escolheu a opção de ler o texto de um ficheiro
            file_path = input("Introduza o caminho do ficheiro: ").strip() #Lê o caminho do ficheiro fornecido pelo user
            while not file_path: #Verifica se o caminho do ficheiro é vazio ou contém apenas espaços em branco, e solicita ao user que insira um caminho válido até que isso seja feito
                print("Caminho inválido. Por favor, insira um caminho não vazio.") #Exibe uma mensagem de erro indicando que o caminho do ficheiro é inválido e solicita ao user que insira um caminho válido
                file_path = input("Introduza o caminho do ficheiro: ").strip() #Lê o caminho do ficheiro fornecido pelo user, removendo espaços em branco extras, para garantir que a entrada seja limpa antes de ser processada
            
            text = read_text_file(file_path) #Chama a função read_text_file para ler o conteúdo do ficheiro e armazená-lo na variável text
                     
            if text.strip(): #Se o texto lido do ficheiro não estiver vazio, retorna o texto para ser processado posteriormente
                return option, text #Retorna a opção escolhida e o texto lido do ficheiro para ser processado posteriormente
            print("Erro ao ler o ficheiro. Verifique o caminho e o encoding.") #Exibe uma mensagem de erro indicando que houve um problema ao ler o ficheiro, sugerindo que o user verifique o caminho do ficheiro e o encoding
            continue #Continua o loop para permitir que o user escolha uma opção válida caso haja um problema ao ler o ficheiro
        
        print("Opção inválida. Por favor, escolha 1 ou 2.\n") #Exibe uma mensagem de erro indicando que a opção escolhida é inválida
        continue #Continua o loop para solicitar ao user que escolha uma opção válida

if __name__ == "__main__":
    try:
        setup_logging() #Chama a função setup_logging para configurar o logging, garantindo que as mensagens de log sejam registradas em um ficheiro de log específico
        logging.info("Aplicação iniciada.") #Regista uma mensagem de log a indicar que a aplicação foi iniciada
    
        default_output = Path("output") / "report.txt" #Define um caminho padrão para salvar o relatório, usando a classe Path do módulo pathlib para criar um caminho que combina a pasta "output" com o nome do ficheiro "report.txt". Isso permite que o relatório seja salvo em uma pasta específica, garantindo que a estrutura de diretórios seja criada se necessário.
        opt, txt = menu() #Chama a função menu para obter o texto a ser processado, seja inserido manualmente ou lido de um ficheiro, e armazena o resultado na variável text
    
        if not txt.strip(): #Verifica se o texto obtido do menu está vazio (após remover espaços em branco) e, se estiver, imprime uma mensagem indicando que nenhum texto foi fornecido e encerra o programa. Caso contrário, continua com o processamento do texto para obter as palavras mais comuns e salvar os resultados.
            print("Nenhum texto fornecido.") #Exibe uma mensagem indicando que nenhum texto foi fornecido
            raise SystemExit(0) #Encerra o programa com um código de saída 0, indicando que a execução foi bem-sucedida, mas sem processar nenhum texto devido à falta de entrada válida.
        report = top_words_format(txt, 10) #Chama a função top_words_format para obter as 10 palavras mais comuns e suas contagens a partir do texto obtido do menu, e armazena o resultado formatado na variável report
        print(report) #Imprime o relatório formatado contendo as 10 palavras mais comuns e suas contagens
    
        if opt == "1": #Verifica se a opção escolhida foi a de inserir texto manualmente
            user_path = input(f"Caminho para guardar (Enter = {default_output}): ").strip() #Lê o caminho onde o user deseja salvar o relatório, permitindo que ele pressione Enter para usar o caminho padrão definido por DEFAULT_OUTPUT. A função strip() é usada para garantir que a entrada do user seja limpa de espaços em branco antes de ser processada.
            output_path = Path(user_path) if user_path else default_output #Define o caminho de saída para salvar o relatório, usando o caminho fornecido pelo user se ele não for vazio, ou o caminho padrão DEFAULT_OUTPUT caso contrário. Isso permite que o user escolha onde deseja salvar o relatório, com a opção de usar um caminho padrão se preferir.

            if output_path.suffix == "": #Verifica se o caminho de saída não tem uma extensão de ficheiro (ou seja, se é um diretório) e, se for o caso, adiciona "report.txt" ao caminho para garantir que o relatório seja salvo como um ficheiro de texto dentro do diretório especificado. Isso é necessário para evitar erros ao tentar salvar o relatório em um diretório sem especificar um nome de ficheiro.
                output_path = output_path / "report.txt" #Adiciona "report.txt" ao caminho de saída se ele não tiver uma extensão de ficheiro, garantindo que o relatório seja salvo como um ficheiro de texto dentro do diretório especificado. Isso é necessário para evitar erros ao tentar salvar o relatório em um diretório sem especificar um nome de ficheiro.

            save_report(report, output_path) #Chama a função save_report para salvar o relatório formatado no ficheiro especificado por outputPath, garantindo que a pasta de destino exista e usando encoding UTF-8
            save_csv(top_words(txt, 10), output_path.with_suffix(".csv")) #Chama a função save_csv para salvar as 10 palavras mais comuns e suas contagens em um ficheiro CSV, usando o mesmo caminho de saída do relatório, mas com a extensão ".csv". Isso permite que os resultados sejam salvos em ambos os formatos, texto e CSV, para facilitar a análise e o compartilhamento dos dados.
            logging.info("Relatório guardado em: %s", output_path) #Regista uma mensagem de log indicando que o relatório foi salvo, incluindo o caminho do ficheiro para facilitar a identificação do processo de salvamento nos logs
            logging.info("CSV guardado em: %s", output_path.with_suffix('.csv')) #Regista uma mensagem de log indicando que o ficheiro CSV foi salvo, incluindo o caminho do ficheiro para facilitar a identificação do processo de salvamento nos logs
            print(f"Relatório guardado em: {output_path} e CSV em: {output_path.with_suffix('.csv')}") #Exibe uma mensagem indicando o caminho onde o relatório foi salvo, para informar ao user que o processo de salvamento foi concluído com sucesso
    
        else:
            logging.info("Modo leitura.") #Regista uma mensagem de log indicando que o modo de leitura foi selecionado, para facilitar a identificação do processo de escolha nos logs
            print("Modo leitura.")
    except Exception:
        logging.exception("Erro inesperado")
        raise
    
"""
    def setup_logging() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)  # cria a pasta logs/ se não existir
    logging.basicConfig(
        filename=str(LOG_PATH),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force = True
    ) #Configura o logging para registrar mensagens de informação e erros em um ficheiro de log, garantindo que a pasta de logs exista e usando um formato específico para as mensagens de log
    
    def menu():
    print("1 - Inserir texto manualmente")
    print("2 - Ler de ficheiro")
    option = input("Escolha uma opção (1 ou 2): ").strip() #Lê a opção escolhida pelo user, removendo espaços em branco extras, para determinar se o texto será inserido manualmente ou lido de um ficheiro. A função strip() é usada para garantir que a entrada do user seja limpa de espaços em branco antes de ser processada.
    
    if option == "1":        
        text = input("Introduza o texto: ") #Lê o texto inserido manualmente pelo user
        while not text.strip(): #Verifica se o texto inserido é vazio ou contém apenas espaços em branco, e solicita ao user que insira um texto válido até que isso seja feito 
            print("Texto inválido. Por favor, insira um texto não vazio.")
            text = input("Introduza o texto: ")
        return text #Retorna o texto inserido pelo user para ser processado posteriormente
    
    elif option == "2":
        file_path = input("Introduza o caminho do ficheiro: ") #Lê o caminho do ficheiro fornecido pelo user
        while not file_path.strip(): #Verifica se o caminho do ficheiro é vazio ou contém apenas espaços em branco, e solicita ao user que insira um caminho válido até que isso seja feito
            print("Caminho inválido. Por favor, insira um caminho de ficheiro não vazio.") #Exibe uma mensagem de erro indicando que o caminho do ficheiro é inválido e solicita ao user que insira um caminho válido
            file_path = input("Introduza o caminho do ficheiro: ")
        
        text = read_text_file(file_path) #Chama a função read_text_file para ler o conteúdo do ficheiro e armazená-lo na variável text
        #Verifica se o texto fornecido não está vazio (após remover espaços em branco) e, se não estiver, chama a função top_words_format para obter as 10 palavras mais comuns e suas contagens, imprimindo o resultado formatado. Caso contrário, imprime uma mensagem indicando que nenhum texto foi fornecido.
        if text.strip(): #Se o texto lido do ficheiro não estiver vazio, retorna o texto para ser processado posteriormente
            return text #Retorna o texto lido do ficheiro para ser processado posteriormente
        print("Erro ao ler o ficheiro. Verifique o caminho e o encoding.") #Exibe uma mensagem de erro indicando que houve um problema ao ler o ficheiro, sugerindo que o user verifique o caminho do ficheiro e o encoding
        return menu() #Chama recursivamente a função menu para permitir que o user escolha uma opção válida caso haja um problema ao ler o ficheiro
    
    else:
        print("Opção inválida. Por favor, escolha 1 ou 2.\n") #Exibe uma mensagem de erro indicando que a opção escolhida é inválida
        return menu() #Chama recursivamente a função menu para solicitar ao user que escolha uma opção válida
      
if __name__ == "__main__":
    #val = read_text_file("C:\\Users\\Utilizador\\Documents\\VSC\\teste.txt")
    #print(val)
    #OUTPUT_PATH = Path("output") / "C:\\Users\\Utilizador\\Documents\\VSC\\report.txt" #Define o caminho onde o relatório será salvo, usando a classe Path do módulo pathlib para criar um caminho que combina a pasta "output" com o nome do ficheiro "report.txt". Isso permite que o relatório seja salvo em uma pasta específica, garantindo que a estrutura de diretórios seja criada se necessário.
    default_output = Path("output") / "report.txt" #Define um caminho padrão para salvar o relatório, usando a classe Path do módulo pathlib para criar um caminho que combina a pasta "output" com o nome do ficheiro "report.txt". Isso permite que o relatório seja salvo em uma pasta específica, garantindo que a estrutura de diretórios seja criada se necessário.
    opt = menu() #Chama a função menu para obter o texto a ser processado, seja inserido manualmente ou lido de um ficheiro, e armazena o resultado na variável text
    if opt.strip(): #Verifica se o texto obtido do menu não está vazio (após remover espaços em branco) e, se não estiver, chama a função top_words para obter as 10 palavras mais comuns e suas contagens, imprimindo o resultado. Caso contrário, imprime uma mensagem indicando que nenhum texto foi fornecido.
        report = top_words_format(opt, 10) #Chama a função top_words_format para obter as 10 palavras mais comuns e suas contagens a partir do texto obtido do menu, e armazena o resultado formatado na variável report
        print(report) #Imprime o relatório formatado contendo as 10 palavras mais comuns e suas contagens
        
        user_path = input(f"Caminho para guardar (Enter = {default_output}): ").strip() #Lê o caminho onde o user deseja salvar o relatório, permitindo que ele pressione Enter para usar o caminho padrão definido por DEFAULT_OUTPUT. A função strip() é usada para garantir que a entrada do user seja limpa de espaços em branco antes de ser processada.
        output_path = Path(user_path) if user_path else default_output #Define o caminho de saída para salvar o relatório, usando o caminho fornecido pelo user se ele não for vazio, ou o caminho padrão DEFAULT_OUTPUT caso contrário. Isso permite que o user escolha onde deseja salvar o relatório, com a opção de usar um caminho padrão se preferir.
        
        #if outputPath.exists() and outputPath.is_dir(): #Verifica se o caminho de saída existe e é um diretório, e se for o caso, adiciona "report.txt" ao caminho para garantir que o relatório seja salvo como um ficheiro de texto dentro do diretório especificado. Isso é necessário para evitar erros ao tentar salvar o relatório em um diretório sem especificar um nome de ficheiro.
        #    outputPath = outputPath / "report.txt" #Adiciona "report.txt" ao caminho de saída se ele não tiver uma extensão de ficheiro, garantindo que o relatório seja salvo como um ficheiro de texto dentro do diretório especificado. Isso é necessário para evitar erros ao tentar salvar o relatório em um diretório sem especificar um nome de ficheiro.
        
        if output_path.suffix == "": #Verifica se o caminho de saída não tem uma extensão de ficheiro (ou seja, se é um diretório) e, se for o caso, adiciona "report.txt" ao caminho para garantir que o relatório seja salvo como um ficheiro de texto dentro do diretório especificado. Isso é necessário para evitar erros ao tentar salvar o relatório em um diretório sem especificar um nome de ficheiro.
            output_path = output_path / "report.txt" #Adiciona "report.txt" ao caminho de saída se ele não tiver uma extensão de ficheiro, garantindo que o relatório seja salvo como um ficheiro de texto dentro do diretório especificado. Isso é necessário para evitar erros ao tentar salvar o relatório em um diretório sem especificar um nome de ficheiro.
        save_report(report, output_path) #Chama a função save_report para salvar o relatório formatado no ficheiro especificado por outputPath, garantindo que a pasta de destino exista e usando encoding UTF-8
        #OUTPUT_PATH = Path("output") / opt #Define o caminho onde o relatório será salvo, usando a classe Path do módulo pathlib para criar um caminho que combina a pasta "output" com o nome do ficheiro "report.txt". Isso permite que o relatório seja salvo em uma pasta específica, garantindo que a estrutura de diretórios seja criada se necessário.
        #save_report(report, OUTPUT_PATH) #Chama a função save_report para salvar o relatório formatado no ficheiro especificado por OUTPUT_PATH, garantindo que a pasta de destino exista e usando encoding UTF-8
        print(f"Relatório guardado em: {output_path}") #Exibe uma mensagem indicando o caminho onde o relatório foi salvo, para informar ao user que o processo de salvamento foi concluído com sucesso
    else:
        print("Nenhum texto fornecido.")
    #print("Retorno: ", opt) #Exibe o texto retornado pela função menu, que pode ser o texto inserido manualmente ou o conteúdo do ficheiro lido, para verificar se a entrada foi processada corretamente
"""