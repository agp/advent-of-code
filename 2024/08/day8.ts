import * as fs from "fs";
import { Grid } from "../lib/utils";
import { Point } from "../lib/utils";
import { printGrid } from "../lib/utils";
import { checkBounds } from "../lib/utils";

type GridChars = Map<string, Array<Point>>;

const input = fs
  .readFileSync(process.cwd() + "/08/input.txt", "utf-8")
  .split("\n");

const grid = input.map((line) => line.split(""));

const rows = grid.length;
const cols = grid[0].length;

// part 1

// iterate over grid and build character map with of char points
function searchGridForChars(gridToSearch: Grid): GridChars {
  const gridChars: GridChars = new Map();
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      const char = gridToSearch[i][j];
      if (char !== ".") {
        if (!gridChars.get(char)) {
          gridChars.set(char, []);
        }
        gridChars.get(char)?.push({ x: j, y: i });
      } else {
        continue;
      }
    }
  }
  return gridChars;
}

const gridChars = searchGridForChars(grid);

// iterate character points to to create all possible lines
function gridCharLineCombos(gridCharsInput: GridChars) {
  const combosOut = new Map();
  for (const [char, points] of gridChars) {
    combosOut.set(char, []);
    for (let i = 0; i < points.length; i++) {
      for (let j = i + 1; j < points.length; j++) {
        combosOut.get(char).push([points[i], points[j]]);
      }
    }
  }
  return combosOut;
}

const combos: Map<string, Array<Array<Point>>> = gridCharLineCombos(gridChars);

function nodeExists(antiNodeList: Point[], p: Point) {
  const exists = antiNodeList.some(
    (point) => p.x === point.x && p.y === point.y
  );
  return exists;
}
// iterate each character points array lines
function getAllAntiNodes(gridCopy: Grid, harmonics: boolean = false) {
  const antiNodes: Point[] = [];
  for (const [char, pointsArray] of combos) {
    for (const line of pointsArray) {
      if (harmonics) {
        for (const antenna of line) {
          if (!nodeExists(antiNodes, antenna)) {
            antiNodes.push({ x: antenna.x, y: antenna.y });
          }
        }
      }
      const newAntiNodes = getAntiNodesFromLine(line, harmonics);
      for (const p of newAntiNodes) {
        if (checkBounds(grid, p)) {
          if (!nodeExists(antiNodes, p)) {
            antiNodes.push(p);
          }
          const currGridChar = gridCopy[p.y][p.x];
          gridCopy[p.y][p.x] = currGridChar === "." ? "#" : currGridChar;
        }
      }
    }
  }
  return { grid: gridCopy, nodes: antiNodes };
}
const part1antiNodes = getAllAntiNodes(structuredClone(grid));
// printGrid(part1antiNodes.grid);
console.log(part1antiNodes.nodes.length);

// part 2

function getAntiNodesFromLine(segment: Point[], harmonics: boolean = false) {
  const newNodes: Point[] = [];
  const [a, b] = segment;
  const changeA = { x: a.x - b.x, y: a.y - b.y };
  const newPointA = { x: a.x + changeA.x, y: a.y + changeA.y };
  const changeB = { x: b.x - a.x, y: b.y - a.y };
  const newPointB = { x: b.x + changeB.x, y: b.y + changeB.y };
  newNodes.push(newPointA, newPointB);
  if (harmonics) {
    const newANodes = extendHarmonic(changeA, newPointA);
    newNodes.push(...newANodes);
    const newBNodes = extendHarmonic(changeB, newPointB);
    newNodes.push(...newBNodes);
  }
  return newNodes;
}

function extendHarmonic(change: Point, point: Point) {
  const nodes: Point[] = [];
  let inBounds = true;
  let currPoint = point;
  while (inBounds) {
    const nextPoint = { x: currPoint.x + change.x, y: currPoint.y + change.y };
    inBounds = checkBounds(grid, nextPoint);
    if (inBounds) {
      nodes.push(nextPoint);
      currPoint = nextPoint;
    }
  }
  return nodes;
}

const part2AntiNodes = getAllAntiNodes(structuredClone(grid), true);
console.log(part2AntiNodes.nodes.length);
// printGrid(part2AntiNodes.grid);
