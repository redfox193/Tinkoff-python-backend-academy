from abc import ABC, abstractmethod


class DocumentProcessor(ABC):
    @abstractmethod
    def process_text(self, text: str) -> None: pass

    @abstractmethod
    def convert_to_pdf(self) -> None: pass

    @abstractmethod
    def print_document(self) -> None: pass


class TextDocument(DocumentProcessor):
    def process_text(self, text: str) -> None:
        print(f"Processing text: {text}")

    def convert_to_pdf(self) -> None:
        print("Converting TextDocument to PDF")

    def print_document(self) -> None:
        print("Printing TextDocument")


class PDFDocument(DocumentProcessor):
    def process_text(self, text: str) -> None:
        raise NotImplementedError("PDFDocument cannot process text")

    def convert_to_pdf(self) -> None:
        raise NotImplementedError("PDFDocument is already in PDF format")

    def print_document(self) -> None:
        print("Printing PDFDocument")


class ReadOnlyDocument(DocumentProcessor):
    def process_text(self, text: str) -> None:
        raise NotImplementedError("ReadOnlyDocument cannot process text")

    def convert_to_pdf(self) -> None:
        print("Converting ReadOnlyDocument to PDF")

    def print_document(self) -> None:
        raise NotImplementedError("ReadOnlyDocument cannot be printed")
