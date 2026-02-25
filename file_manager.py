from __future__ import annotations

import argparse
import csv
import logging
from pathlib import Path

from text_analysis import top_words, top_words_format

LOG_PATH = Path("logs") / "app.log"


def setup_logging() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.propagate = False
    #logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(fmt)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def read_text_file(file_path: str) -> str:
    try:
        logging.info("A ler ficheiro (utf-8): %s", file_path)
        return Path(file_path).read_text(encoding="utf-8")
        #with open(file_path, "r", encoding="utf-8") as file:
        #    return file.read()

    except FileNotFoundError:
        logging.error("Ficheiro não encontrado: %s", file_path)
        return ""

    except UnicodeDecodeError:
        logging.warning("Falhou utf-8, a tentar latin-1: %s", file_path)
        #with open(file_path, "r", encoding="latin-1") as file:
        #    return file.read()
        try:
            return Path(file_path).read_text(encoding="latin-1")
        except OSError as e:
            logging.error("Erro ao ler ficheiro: %s (%s)", file_path, e)
            return ""
    
    except OSError as e:
        logging.error("Erro ao abrir/ler ficheiro: %s (%s)", file_path, e)
        return ""


def save_report(report: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")
    logging.info("Relatório guardado em: %s", path)


def save_csv(items: list[tuple[str, int]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "word", "count"])
        for i, (word, count) in enumerate(items, 1):
            writer.writerow([i, word, count])
            
    logging.info("CSV guardado em: %s", path)


#def parse_args() -> argparse.Namespace:
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analisa texto e devolve as palavras mais comuns."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", help="Caminho para ficheiro de texto")
    group.add_argument("--text", help="Texto direto a analisar (entre aspas)")

    #parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--n", type=int, default=10, help="Top N palavras (default: 10)")
    parser.add_argument("--out", help="Caminho do report .txt a guardar")
    parser.add_argument("--csv", action="store_true", help="Guardar também CSV")

    return parser.parse_args(argv)
    #return parser.parse_args()

def ensure_txt_path(out_path: Path) -> Path:
    if out_path.suffix == "":
        # se for diretório existente OU terminar com separador "conceptual", mete report.txt
        if out_path.exists() and out_path.is_dir():
            return out_path / "report.txt"
        # senão, assume que quer um ficheiro e mete .txt
        return out_path.with_suffix(".txt")
    return out_path

""""
def ensure_txt_path(out_path: Path) -> Path:
    # Se vier um diretório, mete report.txt dentro
    if out_path.suffix == "":
        return out_path / "report.txt"
    # Se vier ficheiro sem .txt, não forçamos, mas podes forçar se quiseres
    return out_path
"""

#def main() -> int:
def main(argv: list[str] | None = None) -> int:
    setup_logging()
    args = parse_args(argv)
    
    if args.n <= 0:
        print("--n deve ser maior que 0")
        return 1

    # 1) obter texto
    if args.input:
        text = read_text_file(args.input)
    else:
        text = args.text or ""

    if not text.strip():
        print("Nenhum texto fornecido (ou ficheiro vazio/erro).")
        return 1

    # 2) analisar
    report = top_words_format(text, args.n)
    items = top_words(text, args.n)

    # 3) imprimir sempre
    print(report)

    # 4) guardar se pedido
    if args.out or args.csv:
        default_out = Path("output") / "report.txt"
        out_path = Path(args.out) if args.out else default_out
        out_path = ensure_txt_path(out_path)

        # guarda report se --out foi dado OU se --csv foi dado (opção: manter consistência)
        save_report(report, out_path)

        if args.csv:
            csv_path = out_path.with_suffix(".csv")
            save_csv(items, csv_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())