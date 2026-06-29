from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONVENTIONS = ROOT / "conventions"
REGISTER = CONVENTIONS / "README.md"
CONVENTION = CONVENTIONS / "roadmap-graph.md"


class RoadmapConventionTests(unittest.TestCase):
    def test_roadmap_convention_document_is_stratum_member(self):
        self.assertTrue(CONVENTION.exists(), "expected a fleshed roadmap convention document")

        head = "\n".join(CONVENTION.read_text(encoding="utf-8").splitlines()[:5])
        self.assertIn("# Roadmap Graph", head)
        self.assertIn("**Stratum:** Conventions", head)
        self.assertIn("[Register](README.md)", head)

    def test_conventions_register_links_to_roadmap_convention(self):
        rows = [
            line
            for line in REGISTER.read_text(encoding="utf-8").splitlines()
            if line.startswith("| **Roadmap graph**")
        ]

        self.assertEqual(len(rows), 1, "expected exactly one roadmap convention register row")
        self.assertIn("[fleshed](roadmap-graph.md)", rows[0])
        self.assertTrue(CONVENTION.exists(), "expected register link target to exist")

    def test_local_markdown_links_resolve(self):
        for path in (REGISTER, CONVENTION):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.exists(), f"expected {path.relative_to(ROOT)} to exist")
                text = path.read_text(encoding="utf-8")
                for target in self._local_markdown_links(text):
                    target_path = self._resolve_link(path, target)
                    self.assertTrue(
                        target_path.exists(),
                        f"{path.relative_to(ROOT)} links to missing local target {target}",
                    )

    def _local_markdown_links(self, text):
        for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
            target = match.group(1).strip()
            if (
                not target
                or target.startswith("#")
                or target.startswith("http://")
                or target.startswith("https://")
                or target.startswith("mailto:")
            ):
                continue
            yield target

    def _resolve_link(self, source, target):
        path_part = target.split("#", 1)[0]
        return (source.parent / path_part).resolve()


if __name__ == "__main__":
    unittest.main()
