from abc import ABC, abstractmethod


class TextProcessor(ABC):
    @abstractmethod
    def process_text(self, text: str) -> None: pass


class PDFConverter(ABC):
    @abstractmethod
    def convert_to_pdf(self) -> None: pass


class DocumentPrinter(ABC):
    @abstractmethod
    def print_document(self) -> None: pass


class TextDocument(TextProcessor, PDFConverter, DocumentPrinter):
    def process_text(self, text: str) -> None:
        print(f"Processing text: {text}")

    def convert_to_pdf(self) -> None:
        print("Converting TextDocument to PDF")

    def print_document(self) -> None:
        print("Printing TextDocument")


class PDFDocument(DocumentPrinter):
    def print_document(self) -> None:
        print("Printing PDFDocument")


class ReadOnlyDocument(PDFConverter):
    def convert_to_pdf(self) -> None:
        print("Converting ReadOnlyDocument to PDF")
