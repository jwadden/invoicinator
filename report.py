import sys

from optparse import OptionParser
from datetime import date
from isoweek import Week

from reportlab.lib import pagesizes, styles, enums, units, colors
from reportlab.pdfgen import canvas
from reportlab import platypus
from sqlalchemy import and_

import settings

from functions import get_hours

option_parser = OptionParser()
option_parser.add_option(
    "-d", "--date",
    dest="week_date",
    help="Date falling within the invoice week",
    metavar="YYYY-MM-DD"
)

option_parser.add_option(
    "-f", "--file",
    dest="filename",
    help="Output file",
    metavar="FILE"
)

(options, args) = option_parser.parse_args()

try:        
    date = date(*map(int, options.week_date.split('-')))
except ValueError:
    sys.exit('Invalid date format')
except AttributeError:
    date = date.today()

week = Week.withdate(date)
start_date = week.monday()
end_date = (week + 1).monday()

if options.filename is None:
    filename = 'invoice-%s.pdf' % week.sunday()
else:
    filename = options.filename

canvas = canvas.Canvas(filename, pagesize=pagesizes.letter)
page_width, page_height = pagesizes.letter

invoice = []

stylesheet = styles.getSampleStyleSheet()
stylesheet.add(
    styles.ParagraphStyle(name='Justify', alignment=enums.TA_JUSTIFY)
)

stylesheet.add(
    styles.ParagraphStyle(name='AlignRight', alignment=enums.TA_RIGHT)
)

stylesheet.add(
    styles.ParagraphStyle(
        name='AlignRightHeading',
        alignment=enums.TA_RIGHT,
        fontSize=16,
    )
)

address_frame = platypus.Frame(0, page_height - 4 * units.cm, 10 * units.cm, 4 * units.cm, id='address_frame')
address = [
    platypus.Paragraph('<strong>%s</strong>' % settings.name, stylesheet["Normal"]),
]
for part in settings.address_parts:
    ptext = part.strip()
    address.append(platypus.Paragraph(ptext, stylesheet["Normal"]))
    
address.append(platypus.Spacer(0, 0.5 * units.cm))
address.append(platypus.Paragraph(settings.phone, stylesheet["Normal"]))
address.append(platypus.Paragraph(settings.email, stylesheet["Normal"]))

address_frame.addFromList(address, canvas)

info_frame = platypus.Frame(page_width - 10 * units.cm, page_height - 4 * units.cm, 10 * units.cm, 4 * units.cm, id='info_frame')
info = [
    platypus.Paragraph('<strong>INVOICE</strong>', stylesheet["AlignRightHeading"]),
    platypus.Spacer(0, 0.5 * units.cm),
    platypus.Paragraph(week.sunday().strftime('%b %d, %Y'), stylesheet["AlignRight"]),
    platypus.Spacer(0, 0.5 * units.cm),
    platypus.Paragraph('Att: %s' % settings.recipient_name, stylesheet["AlignRight"]),
    platypus.Paragraph(settings.recipient_company, stylesheet["AlignRight"]),
]

info_frame.addFromList(info, canvas)

note_frame = platypus.Frame(3 * units.cm, page_height - 7.5 * units.cm, 15 * units.cm, 3 * units.cm, id='note_frame')
note = []
for note_line in settings.note.split('\n'):
    if len(note_line.strip()) > 0:
        note.append(platypus.Paragraph(note_line.strip(), stylesheet['Justify']))
        
note_frame.addFromList(note, canvas)

hours_dict = get_hours(start_date, end_date)

hours_header = (
    platypus.Paragraph('<strong>#</strong>', stylesheet['Normal']),
    platypus.Paragraph('<strong>Task</strong>', stylesheet['Normal']),
    platypus.Paragraph('<strong>Hours</strong>', stylesheet['Normal']),
    platypus.Paragraph('<strong>Rate</strong>', stylesheet['Normal']),
    platypus.Paragraph('<strong>Total</strong>', stylesheet['Normal']),
)

hours_data = [
    hours_header
]

invoice_total = 0.0
task_counter = 0

for task in sorted(hours_dict.keys()):
    hours_data.append((
        task_counter + 1,
        task,
        hours_dict[task],
        settings.rate,
        '$%.2f' % (hours_dict[task] * settings.rate),
    ))
    
    invoice_total += (hours_dict[task] * settings.rate)
    task_counter += 1

column_widths = (2 * units.cm, 10 * units.cm, 2 * units.cm, 2 * units.cm, 2 * units.cm)

hours_table = platypus.Table(hours_data, colWidths=column_widths)

hours_table.setStyle(
    platypus.TableStyle(
        [
            ('BACKGROUND',(0,0),(-1,0),colors.grey),
            ('TEXTCOLOR',(-1,1),(-1,-1),colors.green)
        ]
    )
)

table_width, table_height = hours_table.wrapOn(canvas, 0, 0)
hours_table.drawOn(canvas, 1.8 * units.cm, page_height - table_height - 8 * units.cm)

total_frame = platypus.Frame(
    1.8 * units.cm,
    page_height - table_height - 9 * units.cm,
    15 * units.cm, 1 * units.cm,
    id='total_frame'
)
total = [platypus.Paragraph('<strong>Total: $%.2f</strong>' % invoice_total, stylesheet['Normal'])]

total_frame.addFromList(total, canvas)

canvas.showPage()
canvas.save()
