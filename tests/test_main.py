from file_manager import main

def test_main_text_ok(capsys):
    code = main(["--text", "ola ola mundo", "--n", "2"])
    assert code == 0

    out = capsys.readouterr().out.lower()
    assert "ola" in out
    assert "mundo" in out

def test_main_invalid_n(capsys):
    code = main(["--text", "ola", "--n", "0"])
    assert code == 1

    out = capsys.readouterr().out.lower()
    assert "maior que 0" in out

def test_main_empty_text(capsys):
    code = main(["--text", "   "])
    assert code == 1

    out = capsys.readouterr().out.lower()
    assert "nenhum texto fornecido" in out