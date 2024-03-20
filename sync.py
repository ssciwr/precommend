import hashlib
import os
import shutil


# Check whether we need to copy the config file
if (
    not os.path.exists("precommend/.pre-commit-config.yaml")
    or hashlib.md5(open("precommend/.pre-commit-config.yaml", "rb").read()).hexdigest()
    != hashlib.md5(open(".pre-commit-config.yaml", "rb").read()).hexdigest()
):
    shutil.copy(".pre-commit-config.yaml", "precommend/.pre-commit-config.yaml")
    raise SystemExit(1)
