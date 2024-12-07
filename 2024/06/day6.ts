import * as fs from "fs";

type Point = {
  y: number;
  x: number;
};

type Grid = string[][];

const input = fs
  .readFileSync(process.cwd() + "/06/input.txt", "utf-8")
  .split("\n");

const grid = input.map((line) => line.split(""));

const rows = grid.length;
const cols = grid[0].length;
// find starting position

function searchGridForGuard(gridToSearch: Grid): Point | undefined {
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      if (gridToSearch[i][j] === "^") {
        const pos = { y: i, x: j };
        return pos;
      } else {
        continue;
      }
    }
  }
}

function stepGuardInGrid(
  gridToWalk: Grid,
  guardPos: Point,
  newObstacle: Point | undefined = undefined
) {
  const genGuardDir = guardDirGenerator();
  let guardDir = genGuardDir.next().value
  if (newObstacle) {
    gridToWalk[newObstacle.y][newObstacle.x] = "O";
  }
  const knownPivots: Set<string> = new Set();
  while (true) {
    let nextY = guardPos.y + guardDir.y;
    let nextX = guardPos.x + guardDir.x;
    const inBounds = checkBounds(gridToWalk, { y: nextY, x: nextX });
    // if next step would be out of bounds, exit loop and assign final square to X
    if (!inBounds) {
      gridToWalk[guardPos.y][guardPos.x] = "X";
      break;
    }
    const nextStepContents = gridToWalk[nextY][nextX];
    //  if next step is an obstacle change guard direction
    if (nextStepContents === "#" || nextStepContents === "O") {
      guardDir = genGuardDir.next().value;
      const setPos = `y${guardPos.y}x${guardPos.x}yDir${guardDir.y}xDir${guardDir.x}`;
      if (knownPivots.has(setPos)) {
        // loop is positive
        return { grid: gridToWalk, looped: true };
      } else {
        knownPivots.add(setPos);
        continue;
      }
    }
    //   change current grid content to X and step the guard to next space
    gridToWalk[guardPos.y][guardPos.x] = "X";
    gridToWalk[nextY][nextX] = "^";
    guardPos.y = nextY;
    guardPos.x = nextX;
    // printGrid(gridToWalk);
  }
  return { grid: gridToWalk, looped: false };
}

function checkBounds(gridToCheck: Grid, coord: Point) {
  try {
    gridToCheck[coord.y][coord.x];
    if (coord.y >= 0 && coord.y < rows && coord.x >= 0 && coord.x < cols) {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    return false;
  }
}

function* guardDirGenerator(): Generator<Point> {
  while (true) {
    yield { y: -1, x: 0 };
    yield { y: 0, x: 1 };
    yield { y: 1, x: 0 };
    yield { y: 0, x: -1 };
  }
}

function printGrid(gridToPrint: Grid) {
  let output = "";
  gridToPrint.forEach((line) => {
    output += line.toString().replaceAll(",", "");
    output += "\n";
  });
  console.log(output);
}

let startGuardPos = searchGridForGuard(grid) as Point;

const t0 = performance.now();
const gridToWalk = structuredClone(grid);
const walkedGrid = stepGuardInGrid(
  gridToWalk,
  { ...startGuardPos }
);
const t1 = performance.now();
console.log(`Call to stepGuardInGrid took ${t1 - t0} milliseconds.`);

const sumX = walkedGrid.grid.flat().reduce((sum, currVal) => {
  if (currVal === "X") {
    return sum + 1;
  } else {
    return sum;
  }
}, 0);
console.log({sumX});

// part 2

// get all visited X squares
function getAllX(gridX: Grid) {
  const xSquares = [];
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      if (gridX[i][j] === "X") {
        const pos = { y: i, x: j };
        xSquares.push(pos);
      } else {
        continue;
      }
    }
  }
  return xSquares;
}

const xGridSquares = getAllX(walkedGrid.grid);

const t2 = performance.now()
// insert obstacle at every X and check for loop condition
let looped = 0;
for (const pos of xGridSquares) {
  if (pos !== startGuardPos) {
    const newGridToWalk = structuredClone(grid);
    const loopedGrid = stepGuardInGrid(
      newGridToWalk,
      { ...startGuardPos },
      pos
    );
    // printGrid(loopedGrid.grid);
    looped += loopedGrid.looped ? 1 : 0;
  }
}
const t3 = performance.now()
console.log(`obstacle iteration took ${t3 - t2} milliseconds.`);
console.log({looped});
