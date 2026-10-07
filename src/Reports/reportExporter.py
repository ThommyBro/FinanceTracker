from pathlib import Path


class ReportWriter:
    """
    Simple Class for exporting reports.
    """
    def save(self, report: str, file_path: str | Path) -> None:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")