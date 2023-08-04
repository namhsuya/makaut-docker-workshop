import argparse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import pandas as pd

# Function to read blast output files and extract the sseqid column
def read_blast_output(file_path):
    df = pd.read_csv(file_path, sep='\t', header=None, names=['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore'])
    return set(df['sseqid'])

# Function to create the Venn diagram and save it as an image
def create_venn_diagram(set1, set2, labels, title, output_path):
    plt.figure(figsize=(6, 6))
    vd = venn2([set1, set2], set_labels=labels)
    for text in vd.subset_labels:
        text.set_fontsize(16)
    for text in vd.set_labels:
        text.set_fontsize(16)
    lbl = vd.get_label_by_id("A")
    x, y = lbl.get_position()
    lbl.set_position((x - 0.3, y))
    lbl = vd.get_label_by_id("B")
    x, y = lbl.get_position()
    lbl.set_position((x + 0.3, y))
    plt.title(title)
    plt.grid()
    plt.savefig(output_path)
    plt.close()

# Function to compute Mean and SD values for pident, evalue and bitscore columns
def compute_mean_sd(file_path):
    # Read the blast output file
    df = pd.read_csv(file_path, sep='\t', header=None, names=['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore'])
    
    # Compute mean and SD for each column
    mean_pident = df['pident'].mean()
    sd_pident = df['pident'].std()
    
    mean_evalue = df['evalue'].mean()
    sd_evalue = df['evalue'].std()
    
    mean_bitscore = df['bitscore'].mean()
    sd_bitscore = df['bitscore'].std()
    
    data = {
        'Stat': ['Values'],
        'Mean_pident': [mean_pident],
        'SD_pident': [sd_pident],
        'Mean_evalue': [mean_evalue],
        'SD_evalue': [sd_evalue],
        'Mean_bitscore': [mean_bitscore], 
        'SD_bitscore': [sd_bitscore]
    } 
    return pd.DataFrame.from_dict(data).round(4)

# Function to create a table from DataFrame
def create_table_from_dataframe(dataframe):
    table_data = [dataframe.columns.tolist()] + dataframe.values.tolist()
    t = Table(table_data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    return t


def main():
    parser = argparse.ArgumentParser(description='Create a BLASTN Result Comparison Summary Report')
    parser.add_argument('file1', type=str, help='Path to the SAME-1 blastn report')
    parser.add_argument('file2', type=str, help='Path to the DIFFERENT blastn report')
    parser.add_argument('file3', type=str, help='Path to the SAME-2 blastn report')
    parser.add_argument('venn_output1', type=str, help='Path to save the Venn diagram between Same1 and Different')
    parser.add_argument('venn_output2', type=str, help='Path to save the Venn diagram between Same1 and Same2')
    parser.add_argument('pdf_output', type=str, help='Path to save the final PDF report')
    args = parser.parse_args()

    # Read blast output files and compute mean and standard deviation
    file1_sseqids = read_blast_output(args.file1)
    file2_sseqids = read_blast_output(args.file2)
    file3_sseqids = read_blast_output(args.file3)

    name1 = args.file1.split('/')[-1]
    name2 = args.file2.split('/')[-1]
    name3 = args.file3.split('/')[-1]
    
    df1 = compute_mean_sd(args.file1)
    df2 = compute_mean_sd(args.file2)
    df3 = compute_mean_sd(args.file3)

    # Create Venn diagrams
    create_venn_diagram(file1_sseqids, file2_sseqids, (name1, name2), 'Venn Diagram: '+name1+' vs '+name2, args.venn_output1)
    create_venn_diagram(file1_sseqids, file3_sseqids, (name1, name3), 'Venn Diagram: '+name1+' vs '+name3, args.venn_output2)

    # Create the PDF report
    doc = SimpleDocTemplate(args.pdf_output, pagesize=letter)
    styles = getSampleStyleSheet()

    # Add the title
    title = Paragraph("BLASTN Result Comparison Summary", styles['Title'])
    report_elements = [title, Spacer(1, 12)]

    # Add the Venn diagrams
    report_elements.append(Paragraph("Venn Diagram: "+name1+" vs "+name2, styles['Heading2']))
    report_elements.append(Spacer(1, 12))
    report_elements.append(Image(args.venn_output1, width=200, height=200))
    report_elements.append(Spacer(1, 12))
    report_elements.append(Paragraph("Venn Diagram: "+name1+" vs "+name3, styles['Heading2']))
    report_elements.append(Spacer(1, 12))
    report_elements.append(Image(args.venn_output2, width=200, height=200))
    report_elements.append(Spacer(1, 64))

    # Add the tables
    report_elements.append(Paragraph("Summary Tables:", styles['Heading2']))
    report_elements.append(Spacer(1, 12))
    report_elements.append(Paragraph(name2+" Summary Table:", styles['Normal']))
    report_elements.append(Spacer(1, 12))
    report_elements.append(create_table_from_dataframe(df1))
    report_elements.append(Spacer(1, 12))
    report_elements.append(Paragraph(name3+" Summary Table:", styles['Normal']))
    report_elements.append(Spacer(1, 12))
    report_elements.append(create_table_from_dataframe(df3))
    report_elements.append(Spacer(1, 12))
    report_elements.append(Paragraph(name2+" Summary Table:", styles['Normal']))
    report_elements.append(Spacer(1, 12))
    report_elements.append(create_table_from_dataframe(df2))
    report_elements.append(Spacer(1, 12))

    # Build the PDF
    doc.build(report_elements)


if __name__ == "__main__":
    # python summarize.py same1.txt different same2.txt venn_diagram1.png venn_diagram2.png blastn_summary_report.pdf
    main()