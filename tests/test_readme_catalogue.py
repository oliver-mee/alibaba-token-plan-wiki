"""Offline regression for mixed listed and unlisted video discovery."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("sync_readme", Path(__file__).parents[1] / "scripts" / "sync-readme.py")
assert spec is not None and spec.loader is not None
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class CatalogueTests(unittest.TestCase):
    def test_discovery_is_per_model_not_per_modality(self):
        def row(id, kind, **extra):
            return {"id": id, "kind": kind, "status": "active", "tiers": ["team"],
                    "regions": ["global"], **extra}
        rows = [row("chat", "chat"), row("listed-video", "video", discovery_listed=True),
                row("legacy-video", "video"), row("unlisted-chat", "chat", status="unlisted")]
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory) / "data.json"
            canon = Path(directory) / "canon.json"
            data.write_text(json.dumps({"updated": "2026-10-20", "models": rows}))
            canon.write_text(json.dumps({"models": rows}))
            with patch.object(sync, "DATA", data), patch.object(sync, "CANON", canon):
                body = " ".join(sync.build_body().split())
        self.assertIn("`/models` lists 2 ids per Team key: 1 chat + 1 video", body)
        self.assertIn("1 other active video models", body)
        self.assertIn("unlisted-chat", body)
        self.assertNotIn("never appear", body)


if __name__ == "__main__":
    unittest.main()
