import * as fs from "fs";

const inputArray = [];

const input = fs
  .readFileSync(process.cwd() + "/02/input.txt", "utf-8")
  .split("\n");
for (const line of input) {
  const lineSplit = line.split(" ");
  const lineNumbers = lineSplit.map((s) => Number(s));
  inputArray.push(lineNumbers);
}
//   console.log(inputArray);

const safetyReport = inputArray.map((report) => {
  return testReport(report);
});

const safetyReportSpliced = inputArray.map((report) => {
  const reportIndexes = [...Array(report.length).keys()];
  const splicedReportsTest = reportIndexes.map((i) => {
    const reportSpliced = report.toSpliced(i, 1);
    return testReport(reportSpliced);
  });
  return splicedReportsTest.some(Boolean);
});

const safeReports = safetyReport.filter(Boolean);
const safeReportsSpliced = safetyReportSpliced.filter(Boolean);

console.log(safeReports.length);
console.log(safeReportsSpliced.length);

function testReport(report: number[]): boolean {
  let safeOrder = "";
  if (report[0] > report[1]) {
    safeOrder = "desc";
  } else {
    safeOrder = "asc";
  }
  let safe = true;

  for (let i = 1; i < report.length; i++) {
    if (safeOrder === "desc") {
      if (report[i - 1] < report[i]) {
        safe = false;
      }
    } else if (safeOrder === "asc") {
      if (report[i - 1] > report[i]) {
        safe = false;
      }
    }

    const absDiff = Math.abs(report[i - 1] - report[i]);
    if (absDiff < 1 || absDiff > 3) {
      safe = false;
    }
  }
  return safe;
}
