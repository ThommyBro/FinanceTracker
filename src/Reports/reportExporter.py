from pathlib import Path
from .reportGenerator import ReportGenerator


class ReportWriter:
    """
    Simple Class for exporting reports.
    """
    def save(self, report: str, file_path: str | Path, generator: ReportGenerator) -> None:
        path = Path(file_path)

        # generate correct file extension depending on the corresponding reporter
        if path.suffix.lower() != generator.file_extension:
            path = path.with_suffix(generator.file_extension)

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")