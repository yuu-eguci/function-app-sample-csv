import inspect
import json
from pathlib import Path

from sample_csv_function import main

FUNCTION_DIR = Path(__file__).parents[1] / "sample_csv_function"


def test_function_json_matches_code_and_readme():
    config = json.loads((FUNCTION_DIR / "function.json").read_text(encoding="utf-8"))
    readme = (FUNCTION_DIR / "readme.md").read_text(encoding="utf-8")
    assert (FUNCTION_DIR / config["scriptFile"]).is_file()
    # binding の name と main の引数名がずれると、ホストが関数を読み込めない
    # ($return は戻り値の binding で、引数ではない)
    names = {b["name"] for b in config["bindings"] if b["name"] != "$return"}
    assert names == set(inspect.signature(main).parameters)
    # readme に書いたスケジュールが古くなっていないこと
    (timer,) = [b for b in config["bindings"] if b["type"] == "timerTrigger"]
    assert f"`{timer['schedule']}`" in readme
