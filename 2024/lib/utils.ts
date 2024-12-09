export type Point = {
  x: number;
  y: number;
};

export type Grid = string[][];

export function printGrid(gridToPrint: Grid) {
  let output = "";
  gridToPrint.forEach((line) => {
    output += line.join("");
    output += "\n";
  });
  console.log(output);
}

export function checkBounds(grid: string[][]|number[][], point: Point) {
  if (point.y >= 0 && point.y < grid.length && point.x >= 0 && point.x < grid[0].length) {
    return true;
  } else {
    return false;
  }
}
