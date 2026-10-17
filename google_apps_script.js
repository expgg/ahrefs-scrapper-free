/**
 * =========================================================================
 *     AHREFS AUTO SCRAPER - DEDICATED SHEET PER RESEARCH ENGINE
 *                     Engineered by Al Hossain Rifat
 * =========================================================================
 * Features:
 *   1. Auto-Creates a Brand New Standalone Google Sheet on Google Drive
 *      for every keyword research session.
 *   2. Row 1: Sleek Electric Cyan Title Banner (#050811 + #00E5FF).
 *   3. Row 2: 4 Live KPI Scorecards (Total Harvested, Avg Opp Score,
 *      Zero-Backlink Gems, Buyer Intent Ratio) with real working formulas!
 *   4. Row 3: Sticky Frozen Obsidian Header (#0B0F19) with explicit column
 *      widths so text NEVER squishes, truncates, or overlaps.
 *   5. Rows 4+: High-Contrast Data Badges with real-time live streaming &
 *      one-by-one KD badge illumination.
 * =========================================================================
 */

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const action = data.action || "sync";
    const topic = data.topic ? data.topic.trim() : "Keywords";
    let sheetId = data.sheet_id || null;
    let ss;

    // 1. Target or create the spreadsheet
    if (!sheetId) {
      let nowStr = "";
      try {
        nowStr = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || "GMT", "yyyy-MM-dd HH:mm");
      } catch (err) {
        nowStr = new Date().toISOString().substring(0, 16).replace("T", " ");
      }
      const title = topic.toUpperCase() + " - SEO Keyword Intelligence (" + nowStr + ")";
      ss = SpreadsheetApp.create(title);
      sheetId = ss.getId();
      const sheet = ss.getActiveSheet();
      setupSheetLayout(sheet, topic);
    } else {
      ss = SpreadsheetApp.openById(sheetId);
    }

    const sheet = ss.getActiveSheet();

    // 2. Real-time single-keyword update (Stage 2 Exact KD & Backlinks illumination)
    if (action === "update_keyword") {
      const targetKw = (data.keyword || "").toLowerCase().trim();
      const lastRow = sheet.getLastRow();
      if (lastRow >= 4) {
        const kwValues = sheet.getRange(4, 2, lastRow - 3, 1).getValues();
        for (let i = 0; i < kwValues.length; i++) {
          if (String(kwValues[i][0]).toLowerCase().trim() === targetKw) {
            const rowIdx = 4 + i;
            if (data.exact_kd !== undefined && data.exact_kd !== null) {
              sheet.getRange(rowIdx, 4).setValue(data.exact_kd);
            }
            if (data.backlinks !== undefined && data.backlinks !== null) {
              sheet.getRange(rowIdx, 8).setValue(data.backlinks);
            }
            if (data.opportunity_score !== undefined && data.opportunity_score !== null) {
              sheet.getRange(rowIdx, 3).setValue(data.opportunity_score);
            }
            break;
          }
        }
      }
      return ContentService.createTextOutput(JSON.stringify({
        status: "success",
        sheet_id: sheetId,
        sheet_url: ss.getUrl()
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // 3. Batch sync (Stage 1 Harvesting or Final Overwrite)
    const rows = data.rows || [];
    const mode = data.mode || "append";
    let startRow = 4;

    if (mode === "replace") {
      const lastRow = sheet.getLastRow();
      if (lastRow >= 4) {
        sheet.getRange(4, 1, lastRow - 3, 12).clearContent();
      }
      startRow = 4;
    } else {
      startRow = Math.max(4, sheet.getLastRow() + 1);
    }

    const newValues = [];
    for (let i = 0; i < rows.length; i++) {
      const r = rows[i];
      const rank = (startRow - 3) + i;
      newValues.push([
        rank,
        r.keyword || "",
        r.opportunity_score || "",
        r.exact_kd || "",
        r.kd_tier || "",
        r.search_volume || "",
        r.search_intent || "",
        r.backlinks_needed || "",
        r.keyword_tail || "",
        r.word_count || "",
        r.topic_cluster || "",
        r.match_type || ""
      ]);
    }

    if (newValues.length > 0) {
      const range = sheet.getRange(startRow, 1, newValues.length, 12);
      range.setValues(newValues);
      formatDataRange(sheet, startRow, newValues.length);
    }

    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      sheet_id: sheetId,
      sheet_url: ss.getUrl(),
      count: rows.length
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function setupSheetLayout(sheet, topic) {
  sheet.clear();
  sheet.clearConditionalFormatRules();
  
  sheet.setName(topic.substring(0, 30));
  sheet.setTabColor("#00E5FF");
  
  sheet.setRowHeight(1, 42); // Title Banner
  sheet.setRowHeight(2, 52); // KPI Scorecards
  sheet.setRowHeight(3, 34); // Sticky Column Headers
  
  // Row 1: Dedicated Title Banner
  sheet.getRange("A1:L1").merge()
    .setValue("⚡ " + topic.toUpperCase() + " — SEO KEYWORD INTELLIGENCE ENGINE")
    .setFontFamily("Inter").setFontSize(12).setFontWeight("bold")
    .setBackground("#050811").setFontColor("#00E5FF")
    .setHorizontalAlignment("center").setVerticalAlignment("middle");

  // Row 2: 4 Executive KPI Scorecard Blocks with LIVE calculating formulas
  sheet.getRange("A2:C2").merge()
    .setFormula('="TOTAL HARVESTED" & CHAR(10) & TEXT(COUNTA(A4:A), "#,##0") & " Keywords"')
    .setFontFamily("Inter").setFontSize(10).setFontWeight("bold")
    .setBackground("#0F172A").setFontColor("#38BDF8")
    .setHorizontalAlignment("center").setVerticalAlignment("middle").setWrap(true);
  
  sheet.getRange("D2:F2").merge()
    .setFormula('="AVG OPP SCORE" & CHAR(10) & IFERROR(TEXT(AVERAGE(C4:C), "0.0") & " / 100", "-")')
    .setFontFamily("Inter").setFontSize(10).setFontWeight("bold")
    .setBackground("#0F172A").setFontColor("#34D399")
    .setHorizontalAlignment("center").setVerticalAlignment("middle").setWrap(true);

  sheet.getRange("G2:I2").merge()
    .setFormula('="ZERO-BACKLINK GEMS" & CHAR(10) & COUNTIF(H4:H, "*~0*") & " Easy Wins"')
    .setFontFamily("Inter").setFontSize(10).setFontWeight("bold")
    .setBackground("#0F172A").setFontColor("#FBBF24")
    .setHorizontalAlignment("center").setVerticalAlignment("middle").setWrap(true);

  sheet.getRange("J2:L2").merge()
    .setFormula('="BUYER INTENT RATIO" & CHAR(10) & IFERROR(TEXT(COUNTIF(G4:G, "Commercial") / COUNTA(G4:G), "0.0%"), "0.0%")')
    .setFontFamily("Inter").setFontSize(10).setFontWeight("bold")
    .setBackground("#0F172A").setFontColor("#C084FC")
    .setHorizontalAlignment("center").setVerticalAlignment("middle").setWrap(true);

  // Row 3: Sticky Frozen Obsidian Header (#0B0F19 background with #00E5FF cyan text)
  const headers = [
    "#", "TARGET KEYWORD", "OPP SCORE", "EXACT KD", "KD TIER",
    "SEARCH VOLUME", "SEARCH INTENT", "BACKLINKS NEEDED",
    "KEYWORD TAIL", "WORD COUNT", "TOPIC CLUSTER", "MATCH TYPE"
  ];
  
  sheet.getRange(3, 1, 1, 12).setValues([headers])
    .setBackground("#0B0F19")
    .setFontColor("#00E5FF")
    .setFontFamily("Inter")
    .setFontSize(10)
    .setFontWeight("bold")
    .setHorizontalAlignment("center")
    .setVerticalAlignment("middle");

  sheet.getRange(3, 2).setHorizontalAlignment("left");
  sheet.getRange(3, 11).setHorizontalAlignment("left");
  sheet.setFrozenRows(3);

  // Generous column widths so text NEVER overlaps or truncates
  const colWidths = [50, 260, 100, 95, 115, 125, 135, 165, 115, 95, 175, 125];
  for (let c = 0; c < colWidths.length; c++) {
    sheet.setColumnWidth(c + 1, colWidths[c]);
  }
  
  setupConditionalFormatting(sheet);
}

function formatDataRange(sheet, startRow, rowCount) {
  const fullRange = sheet.getRange(startRow, 1, rowCount, 12);
  fullRange.setFontFamily("Inter").setFontSize(10).setVerticalAlignment("middle");
  
  // High contrast alternating rows
  for (let r = 0; r < rowCount; r++) {
    const currRow = startRow + r;
    sheet.setRowHeight(currRow, 28);
    const bg = (currRow % 2 === 0) ? "#FFFFFF" : "#F8FAFC";
    sheet.getRange(currRow, 1, 1, 12).setBackground(bg);
  }
  
  sheet.getRange(startRow, 1, rowCount, 1).setHorizontalAlignment("center").setFontWeight("bold").setFontColor("#64748B");
  sheet.getRange(startRow, 2, rowCount, 1).setHorizontalAlignment("left").setFontWeight("bold").setFontColor("#0F172A");
  sheet.getRange(startRow, 3, rowCount, 1).setHorizontalAlignment("center").setFontWeight("bold");
  sheet.getRange(startRow, 4, rowCount, 7).setHorizontalAlignment("center");
  sheet.getRange(startRow, 11, rowCount, 1).setHorizontalAlignment("left");
  sheet.getRange(startRow, 12, rowCount, 1).setHorizontalAlignment("center");
}

function setupConditionalFormatting(sheet) {
  const rules = [];
  
  // Column C: Opp Score
  const oppRange = sheet.getRange("C4:C500");
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenNumberGreaterThanOrEqualTo(80).setBackground("#DCFCE7").setFontColor("#15803D").setBold(true).setRanges([oppRange]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenNumberBetween(65, 79).setBackground("#E0F2FE").setFontColor("#0284C7").setBold(true).setRanges([oppRange]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenNumberBetween(50, 64).setBackground("#FEF3C7").setFontColor("#B45309").setRanges([oppRange]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenNumberLessThan(50).setBackground("#FFE4E6").setFontColor("#BE123C").setRanges([oppRange]).build());

  // Column D: Exact KD
  const kdRange = sheet.getRange("D4:D500");
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenNumberBetween(0, 15).setBackground("#DCFCE7").setFontColor("#15803D").setBold(true).setRanges([kdRange]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenNumberBetween(16, 35).setBackground("#ECFCCB").setFontColor("#3F6212").setRanges([kdRange]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenNumberBetween(36, 69).setBackground("#FEF3C7").setFontColor("#B45309").setRanges([kdRange]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenNumberGreaterThanOrEqualTo(70).setBackground("#FFE4E6").setFontColor("#BE123C").setBold(true).setRanges([kdRange]).build());

  // Column G: Search Intent
  const intentRange = sheet.getRange("G4:G500");
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo("Commercial").setBackground("#F3E8FF").setFontColor("#7C3AED").setBold(true).setRanges([intentRange]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo("Transactional").setBackground("#D1FAE5").setFontColor("#047857").setBold(true).setRanges([intentRange]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo("Informational").setBackground("#E0F2FE").setFontColor("#0284C7").setRanges([intentRange]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo("General").setBackground("#F1F5F9").setFontColor("#475569").setRanges([intentRange]).build());

  // Column H: Backlinks (~0 = Goldmine Easy Wins)
  const blRange = sheet.getRange("H4:H500");
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenTextContains("~0").setBackground("#D1FAE5").setFontColor("#065F46").setBold(true).setRanges([blRange]).build());

  // Column F: High Volume (>10k, >100k)
  const volRange = sheet.getRange("F4:F500");
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenTextContains(">10").setBackground("#FEF08A").setFontColor("#713F12").setBold(true).setRanges([volRange]).build());

  sheet.setConditionalFormatRules(rules);
}
