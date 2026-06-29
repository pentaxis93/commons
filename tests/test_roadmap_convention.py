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


def _fleshed_register_targets():
    """Every conventions-register row marked fleshed, as (row, target) pairs.

    A fleshed row carries a ``[fleshed](<file>.md)`` link in its Status column;
    this finds each such target so the structural gate covers every fleshed
    convention by class, not one member by name.
    """
    text = REGISTER.read_text(encoding="utf-8")
    pairs = []
    for line in text.splitlines():
        if not line.startswith("| **"):
            continue
        m = re.search(r"\[fleshed\]\(([^)]+)\)", line)
        if m:
            pairs.append((line, m.group(1).strip()))
    return pairs


class FleshedConventionStratumTests(unittest.TestCase):
    """Class-level invariants every fleshed convention must satisfy.

    Generalizes the roadmap-specific checks above to the whole stratum: each
    fleshed register row points at a real member document that carries the
    fleshed-convention header, and that document's local links resolve.
    """

    def test_register_has_at_least_one_fleshed_convention(self):
        self.assertTrue(
            _fleshed_register_targets(),
            "expected at least one fleshed convention row in the register",
        )

    def test_every_fleshed_row_targets_a_stratum_member(self):
        for row, target in _fleshed_register_targets():
            with self.subTest(target=target):
                doc = (CONVENTIONS / target).resolve()
                self.assertTrue(
                    doc.exists(),
                    f"register row links to missing fleshed document {target}",
                )
                head = "\n".join(doc.read_text(encoding="utf-8").splitlines()[:5])
                self.assertIn(
                    "**Stratum:** Conventions",
                    head,
                    f"{target} does not declare its conventions stratum in its header",
                )
                self.assertIn(
                    "[Register](README.md)",
                    head,
                    f"{target} does not link back to the register in its header",
                )

    def test_every_fleshed_document_local_links_resolve(self):
        for _row, target in _fleshed_register_targets():
            doc = (CONVENTIONS / target).resolve()
            if not doc.exists():
                continue
            text = doc.read_text(encoding="utf-8")
            for link in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
                t = link.group(1).strip()
                if (
                    not t
                    or t.startswith("#")
                    or t.startswith("http://")
                    or t.startswith("https://")
                    or t.startswith("mailto:")
                ):
                    continue
                with self.subTest(document=target, link=t):
                    resolved = (doc.parent / t.split("#", 1)[0]).resolve()
                    self.assertTrue(
                        resolved.exists(),
                        f"{target} links to missing local target {t}",
                    )


if __name__ == "__main__":
    unittest.main()
