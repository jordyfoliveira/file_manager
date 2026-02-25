# Permite usar anotações de tipos como "list[str]" em versões antigas
# e adia a avaliação de tipos (útil para evitar import cycles).
from __future__ import annotations

# Biblioteca para criar programas com argumentos no terminal (CLI).
import argparse

# Biblioteca para escrever ficheiros CSV.
import csv

# Biblioteca para logs (registar info/warnings/erros).
import logging

# Biblioteca para escrever ficheiros JSON.
import json

# Path é uma forma moderna e segura de lidar com caminhos de ficheiros/pastas.
from pathlib import Path

# Importa as funções de análise de texto do teu módulo.
from text_analysis import top_words, top_words_format

# Define o caminho do ficheiro de logs.
LOG_PATH = Path("logs") / "app.log"


def setup_logging() -> None:
    # Garante que a pasta "logs/" existe (cria se não existir).
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Obtém o logger "raiz" (o logger principal do Python).
    logger = logging.getLogger()

    # Define o nível mínimo de logs que serão registados (INFO e acima).
    logger.setLevel(logging.INFO)

    # Impede que os logs sejam duplicados por propagação para loggers "pais"
    # (ajuda em alguns ambientes onde logs aparecem repetidos).
    logger.propagate = False

    # Se quisesses evitar duplicar handlers ao correr várias vezes,
    # podias limpar handlers antigos (por exemplo, no VSCode).
    # logger.handlers.clear()

    # Define o formato (data/hora + nível + mensagem).
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Cria um handler para escrever logs em ficheiro.
    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")

    # Define que este handler guarda INFO e acima.
    file_handler.setLevel(logging.INFO)

    # Aplica o formato definido às linhas do log do ficheiro.
    file_handler.setFormatter(fmt)

    # Cria um handler para mostrar logs na consola/terminal.
    console_handler = logging.StreamHandler()

    # Define que este handler só mostra WARNING e acima (menos "spam").
    console_handler.setLevel(logging.WARNING)

    # Aplica o formato também ao handler da consola.
    console_handler.setFormatter(fmt)

    # Adiciona o handler do ficheiro ao logger.
    logger.addHandler(file_handler)

    # Adiciona o handler da consola ao logger.
    logger.addHandler(console_handler)


def read_text_file(file_path: str) -> str:
    # Esta função tenta ler um ficheiro com fallback de encoding:
    # tenta utf-8 e se falhar tenta latin-1.
    try:
        # Regista nos logs que vai tentar ler como UTF-8.
        logging.info("A ler ficheiro (utf-8): %s", file_path)

        # Lê o conteúdo do ficheiro usando Path (mais simples que open()).
        return Path(file_path).read_text(encoding="utf-8")

        # Alternativa equivalente (comentada):
        # with open(file_path, "r", encoding="utf-8") as file:
        #     return file.read()

    except FileNotFoundError:
        # Se o ficheiro não existir, regista o erro.
        logging.error("Ficheiro não encontrado: %s", file_path)

        # Retorna string vazia para indicar falha.
        return ""

    except UnicodeDecodeError:
        # Se falhar UTF-8, avisa nos logs e tenta latin-1.
        logging.warning("Falhou utf-8, a tentar latin-1: %s", file_path)

        # Alternativa equivalente (comentada):
        # with open(file_path, "r", encoding="latin-1") as file:
        #     return file.read()

        try:
            # Tenta ler o ficheiro com encoding latin-1.
            return Path(file_path).read_text(encoding="latin-1")

        except OSError as e:
            # Se houver erro do sistema (permissões, path inválida, etc.)
            logging.error("Erro ao ler ficheiro: %s (%s)", file_path, e)

            # Retorna vazio para indicar falha.
            return ""
    
    except OSError as e:
        # Captura outros erros de sistema ao abrir/ler (ex.: sem permissões).
        logging.error("Erro ao abrir/ler ficheiro: %s (%s)", file_path, e)

        # Retorna vazio para indicar falha.
        return ""


def save_report(report: str, path: Path) -> None:
    # Garante que a pasta destino existe.
    path.parent.mkdir(parents=True, exist_ok=True)

    # Escreve o report no ficheiro (sobrescreve se já existir).
    path.write_text(report, encoding="utf-8")

    # Regista onde o report foi guardado.
    logging.info("Relatório guardado em: %s", path)


def save_csv(items: list[tuple[str, int]], path: Path) -> None:
    # Garante que a pasta destino existe.
    path.parent.mkdir(parents=True, exist_ok=True)

    # Abre o ficheiro CSV para escrita.
    with path.open("w", newline="", encoding="utf-8") as f:
        # Cria o writer CSV.
        writer = csv.writer(f)

        # Escreve a primeira linha (cabeçalho).
        writer.writerow(["rank", "word", "count"])

        # Enumera os items (rank começa em 1).
        for i, (word, count) in enumerate(items, 1):
            # Escreve cada linha do CSV.
            writer.writerow([i, word, count])
            
    # Regista onde o CSV foi guardado.
    logging.info("CSV guardado em: %s", path)
    

def save_json(items: list[tuple[str, int]], path: Path) -> None:
    # Garante que a pasta destino existe.
    path.parent.mkdir(parents=True, exist_ok=True)

    # Converte a lista de tuplas em lista de dicionários (mais "JSON-friendly").
    data = [
        {"rank": i, "word": word, "count": count}
        for i, (word, count) in enumerate(items, 1)
    ]

    # Abre o ficheiro JSON para escrita.
    with path.open("w", encoding="utf-8") as f:
        # Escreve JSON, mantendo acentos e formatando com indentação.
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Regista onde o JSON foi guardado.
    logging.info("JSON guardado em: %s", path)


# Função para "parsear" argumentos. Recebe argv opcional para facilitar testes.
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    # Cria parser com descrição.
    parser = argparse.ArgumentParser(
        description="Analisa texto e devolve as palavras mais comuns."
    )

    # Cria um grupo onde só podes escolher UMA das opções (--input OU --text).
    group = parser.add_mutually_exclusive_group(required=True)

    # Argumento para ler texto de um ficheiro.
    group.add_argument("--input", help="Caminho para ficheiro de texto")

    # Argumento para passar texto diretamente.
    group.add_argument("--text", help="Texto direto a analisar (entre aspas)")

    # Argumento opcional para escolher top N palavras.
    parser.add_argument("--n", type=int, default=10, help="Top N palavras (default: 10)")

    # Argumento opcional para indicar onde guardar o report .txt.
    parser.add_argument("--out", help="Caminho do report .txt a guardar")

    # Flag opcional para também guardar CSV.
    parser.add_argument("--csv", action="store_true", help="Guardar também CSV")

    # Flag opcional para também guardar JSON.
    parser.add_argument("--json", action="store_true", help="Guardar também JSON")

    # Faz parsing com argv (se None usa sys.argv automaticamente).
    return parser.parse_args(argv)


def ensure_txt_path(out_path: Path) -> Path:
    # Se não houver sufixo, pode ser diretório ou nome sem extensão.
    if out_path.suffix == "":
        # Se existe e é diretório, guarda "report.txt" dentro desse diretório.
        if out_path.exists() and out_path.is_dir():
            return out_path / "report.txt"

        # Se não é diretório, assume que é nome de ficheiro sem extensão → adiciona .txt
        return out_path.with_suffix(".txt")

    # Se já tem sufixo, devolve como está.
    return out_path


def main(argv: list[str] | None = None) -> int:
    # Configura logging logo no início.
    setup_logging()

    # Lê argumentos.
    args = parse_args(argv)
    
    # Validação simples: n tem de ser maior que 0.
    if args.n <= 0:
        print("--n deve ser maior que 0")
        return 1

    # 1) obter texto: ou do ficheiro, ou do argumento --text
    if args.input:
        text = read_text_file(args.input)
    else:
        text = args.text or ""

    # Se o texto estiver vazio, não faz sentido continuar.
    if not text.strip():
        print("Nenhum texto fornecido (ou ficheiro vazio/erro).")
        return 1

    # 2) analisar: gera report em string e items em lista de tuplas
    report = top_words_format(text, args.n)
    items = top_words(text, args.n)

    # 3) imprime sempre no terminal
    print(report)

    # 4) guardar se pedido (txt sempre que pedes out/csv/json)
    if args.out or args.csv or args.json:
        # caminho default se não for dado --out
        default_out = Path("output") / "report.txt"

        # se --out foi dado, usa-o; senão usa default
        out_path = Path(args.out) if args.out else default_out

        # normaliza para garantir que termina em .txt quando necessário
        out_path = ensure_txt_path(out_path)

        # guarda o report txt
        save_report(report, out_path)

        # se pediste CSV, guarda CSV com o mesmo nome mas .csv
        if args.csv:
            csv_path = out_path.with_suffix(".csv")
            save_csv(items, csv_path)
            
        # se pediste JSON, guarda JSON com o mesmo nome mas .json
        if args.json:
            json_path = out_path.with_suffix(".json")
            save_json(items, json_path)

    # retorna 0 = sucesso
    return 0


# Ponto de entrada do script: só executa se for "python app.py"
if __name__ == "__main__":
    # Termina o programa com o código devolvido por main()
    raise SystemExit(main())

""""
def ensure_txt_path(out_path: Path) -> Path:
    # Se vier um diretório, mete report.txt dentro
    if out_path.suffix == "":
        return out_path / "report.txt"
    # Se vier ficheiro sem .txt, não forçamos, mas podes forçar se quiseres
    return out_path
"""
