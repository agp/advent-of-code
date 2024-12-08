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

const gridCopy = structuredClone(grid);
const antiNodes: Point[] = [];
// iterate each character points array lines
for (const [char, pointsArray] of combos) {
  for (const [a, b] of pointsArray) {
    // const slope = (b.y - a.y) / (b.x - a.x);
    // const length = Math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2);
    // console.log(slope);
    // console.log(length);
    const changeA = { x: a.x - b.x, y: a.y - b.y };
    const newPointA = { x: a.x + changeA.x, y: a.y + changeA.y };
    const changeB = { x: b.x - a.x, y: b.y - a.y };
    const newPointB = {x: b.x + changeB.x, y: b.y + changeB.y}
    for (const p of [newPointA, newPointB]) {
      if (checkBounds(grid, p)) {
        const exists = antiNodes.some((point) => p.x === point.x && p.y === point.y)
        if (!exists) {
          antiNodes.push(p)
        }
        const currGridChar = gridCopy[p.y][p.x]
        gridCopy[p.y][p.x] = currGridChar === "." ? "#" : currGridChar
      }
    }
  }
}
printGrid(gridCopy);
console.log(antiNodes.length);

