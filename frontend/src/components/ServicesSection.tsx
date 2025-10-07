import React, { useState } from "react";
import axios from "axios";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

export default function NumerologyReport() {
  const [dob, setDob] = useState("");
  const [gender, setGender] = useState("male"); // optional
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateReport = async () => {
    if (!dob) return alert("Please enter your date of birth");
    setLoading(true);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/profession-analysis-report/report",
        { date_of_birth: dob, include_kua: false, gender }
      );
      setReport(res.data);
    } catch (err) {
      console.error(err);
      alert("Error generating report");
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = () => {
    if (!report) return;
    const doc = new jsPDF("p", "mm", "a4");

    const pageWidth = 210;
    const pageHeight = 297;
    const margin = 20;
    const maxWidth = pageWidth - margin * 2;
    let yOffset = 20;

    // ---------- HEADER ----------
    const addHeaderFooter = () => {
      doc.setFontSize(14);
      doc.setFont("helvetica", "bold");
      doc.text("Radian Soul", pageWidth / 2, 10, { align: "center" });
      doc.setFontSize(10);
      doc.setFont("helvetica", "normal");
      doc.text("www.radiansoul.com", pageWidth / 2, pageHeight - 10, { align: "center" });
    };

    addHeaderFooter();

    // ---------- TITLE ----------
    doc.setFontSize(20);
    doc.text("Radian Soul Profession Analysis Report", pageWidth / 2, yOffset, { align: "center" });
    yOffset += 10;

    doc.setFontSize(12);
    doc.setFont("helvetica", "normal");
    doc.text(`Date of Birth: ${report.date_of_birth}`, margin, yOffset);
    yOffset += 6;

    doc.text(
      `PN (Personality Number / Mulank): ${report.profession_analysis.pn}, DN (Destiny Number / Bhagyank): ${report.profession_analysis.dn}, Anti Pair: ${report.profession_analysis.anti_pair}`,
      margin,
      yOffset
    );
    yOffset += 8;

    // ---------- LO SHU GRID ----------
    const gridSize = 30;
    const startX = (pageWidth - gridSize * 3) / 2;
    const startY = yOffset;

    report.visual_grid?.forEach((row, rowIdx) => {
      row.forEach((cell, colIdx) => {
        const x = startX + colIdx * gridSize;
        const y = startY + rowIdx * gridSize;

        let fillColor = "#E0E0E0"; // default
        if (report.missing_numbers?.includes(Number(cell))) fillColor = "#FFCDD2"; // missing
        if (report.repeated_numbers?.[cell]) fillColor = "#FFF59D"; // repeated
        if (
          Number(cell) === report.profession_analysis?.pn ||
          Number(cell) === report.profession_analysis?.dn
        )
          fillColor = "#B3E5FC"; // PN/DN

        doc.setFillColor(fillColor);
        doc.rect(x, y, gridSize, gridSize, "F");
        doc.setDrawColor(0);
        doc.rect(x, y, gridSize, gridSize);

        doc.setFontSize(14);
        doc.setFont("helvetica", "bold");
        doc.text(cell || "", x + gridSize / 2, y + gridSize / 2 + 3, { align: "center" });
      });
    });

    yOffset = startY + gridSize * 3 + 10;

    doc.setFontSize(12);
    doc.setFont("helvetica", "normal");
    doc.text(`Missing Numbers: ${report.missing_numbers?.join(", ") || "None"}`, margin, yOffset);
    yOffset += 6;
    doc.text(`Repeated Numbers: ${Object.keys(report.repeated_numbers || {}).join(", ") || "None"}`, margin, yOffset);
    yOffset += 8;

    // ---------- PROFESSIONS ----------
    doc.setFontSize(14);
    doc.setFont("helvetica", "bold");
    doc.text("Profession Choices", margin, yOffset);
    yOffset += 6;

    const pa = report.profession_analysis || {};

    const addWrappedText = (title, items, bgColor) => {
      if (!items || items.length === 0) return;
      doc.setFontSize(12);
      doc.setFont("helvetica", "bold");
      if (yOffset > pageHeight - 30) { doc.addPage(); yOffset = 20; addHeaderFooter(); }
      doc.text(`${title}:`, margin, yOffset);
      yOffset += 6;

      const text = items.join(", ");
      const lines = doc.splitTextToSize(text, maxWidth);

      lines.forEach((line) => {
        if (yOffset > pageHeight - 20) { doc.addPage(); yOffset = 20; addHeaderFooter(); }
        if (bgColor) {
          const textHeight = 6;
          const textWidth = doc.getTextWidth(line) + 2;
          doc.setFillColor(bgColor);
          doc.rect(margin - 1, yOffset - 4, textWidth, textHeight, "F");
        }
        doc.setFont("helvetica", "normal");
        doc.setTextColor(0, 0, 0);
        doc.text(line, margin, yOffset);
        yOffset += 6;
      });
      yOffset += 4;
    };

    addWrappedText("First Preference", pa.recommended_professions?.first_preference, "#B3E5FC");
    addWrappedText("Second Preference", pa.recommended_professions?.second_preference, "#C8E6C9");
    addWrappedText("Not Recommended", pa.not_recommended_professions, "#FFCDD2");

    doc.save(`Radian_Soul_Report_${report.date_of_birth}.pdf`);
  };

  return (
    <div>
      <h2>Radian Soul Profession Analysis Report</h2>
      <input
        type="date"
        value={dob}
        onChange={(e) => setDob(e.target.value)}
      />
      <select value={gender} onChange={(e) => setGender(e.target.value)}>
        <option value="male">Male</option>
        <option value="female">Female</option>
      </select>
      <button onClick={generateReport} disabled={loading}>
        {loading ? "Generating..." : "Generate Report"}
      </button>

      {report && report.visual_grid && (
        <div>
          <h3>Lo Shu Grid</h3>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(3, 50px)",
              gridTemplateRows: `repeat(${report.visual_grid.length}, 50px)`,
              gap: "5px",
              marginBottom: "20px",
            }}
          >
            {report.visual_grid.map((row, rowIdx) =>
              row.map((cell, colIdx) => (
                <div
                  key={`${rowIdx}-${colIdx}`}
                  style={{
                    border: "1px solid black",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    height: "50px",
                    fontWeight: "bold"
                  }}
                >
                  {cell || ""}
                </div>
              ))
            )}
          </div>

          <button onClick={downloadPDF}>Download PDF</button>
        </div>
      )}
    </div>
  );
}