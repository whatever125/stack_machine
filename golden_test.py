import base64
import contextlib
import io
import logging
import os
import tempfile

import main
import pytest
import translator


@pytest.mark.golden_test("golden/*.yml")
def test_translator_and_machine(golden, caplog, tick_limit=200000, debug_limit=100):
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmpdirname:
        source = os.path.join(tmpdirname, "source.asm")
        input_stream = os.path.join(tmpdirname, "input.txt")
        target = os.path.join(tmpdirname, "source.bin")
        commented_target = os.path.join(tmpdirname, "source_com.txt")

        with open(source, mode="w", encoding="utf-8") as f:
            f.write(golden["in_source"])
        with open(input_stream, mode="w", encoding="utf-8") as f:
            f.write(golden["in_stdin"])

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            translator.main(source, target)
            print("============================================================")
            first_line = golden["in_source"].splitlines()[0]
            char_output_test = ["; cat", "; hello_username", "; hello_world"]
            main.main(target, input_stream, tick_limit=tick_limit, debug_limit=debug_limit, char_output=(first_line in char_output_test), debug_logging=True)

        with open(target, mode="rb") as f:
            code = f.read()

        with open(commented_target, encoding="utf-8") as f:
            commented_code = f.read()

        assert code == golden.out["out_code"]
        assert commented_code == golden.out["out_commented_code"]
        assert stdout.getvalue() == golden.out["out_stdout"]
        assert caplog.text == golden.out["out_log"]
