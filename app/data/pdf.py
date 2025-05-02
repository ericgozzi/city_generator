from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.enums import TA_JUSTIFY




class PDF:
    """
    A PDF generator.

    This class allows you to create a PDF document with customizable paragraphs.

    Attributes:
        file (str): The full name of the output PDF file, including the '.pdf' extension.    
        paragraphs (list): A list to hold the content (e.g., Paragraph objects) to be added to the PDF.
    """





    def __init__(self, file_name: str):
        """
        Initializes the PDF object with the specified file name.

        Args:
            file_name (str): The base name of the PDF file (with or without '.pdf' extension).
        """
        if not file_name.lower().endswith('.pdf'):
            file_name += '.pdf'

        self.file: str = file_name
        self.doc = SimpleDocTemplate(self.file, pagesize=A4)
        self.paragraphs = []

    




    def export(self) -> None:
        """
        Builds and exports the PDF to the current directory.

        This method compiles the list of added paragraphs and generates a PDF
        file using the ReportLab SimpleDocTemplate.

        Returns:
            None
        """
        self.doc.build(self.paragraphs)
        print(f'Aplausos! The PDF {self.file} has been exported!')





    def add_paragraph(self, text: str, **kwargs) -> None:
        """
        Adds a styled paragraph to the PDF.

        Args:
            text (str): The text content of the paragraph.
            **kwargs: Optional styling parameters for the paragraph. Includes:
                - font_name (str): Font of the text. Default is 'Helvetica'.
                - font_size (int): Size of the font. Default is 12.
                - space_after (int): Space after the paragraph. Default is 12.
                - space_before (int): Space before the paragraph. Default is 0.
                - text_alignment (int): Text alignment (0=left, 1=center, 2=right, 4=justify). Default is 4.

        Returns:
            None
        """
        # KWARGS
        font_name = kwargs.get("font_name", "Helvetica")
        font_size = kwargs.get("font_size", 12)
        space_after = kwargs.get("space_after", 12)
        space_before = kwargs.get("space_before", 0)
        text_alignment = kwargs.get("text_alignment", 4)

        # Export PDF
        styles = getSampleStyleSheet()
        style = ParagraphStyle(
            'CustomStyle',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=font_size,
            spaceAfter=space_after,  # Space after paragraphs
            spaceBefore=space_before,
            alignment= text_alignment,  # Align left (use 1 for center, 2 for right)
            wordWrap='None',  # Ensure word wrapping
        )
        paragraph = Paragraph(text, style)
        self.paragraphs.append(paragraph)