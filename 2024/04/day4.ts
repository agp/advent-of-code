import * as fs from "fs";

// yikes... went down some rabbit holes on this one.

const input = fs.readFileSync(process.cwd() + "/04/input.txt", "utf-8");
const letterMatrix = input.split("\n").map((row) => row.split(""));

const rows = letterMatrix.length;
const cols = letterMatrix[0].length;

// directions to move in matrix
const xDirs = [-1, 0, 1];
const yDirs = [-1, 0, 1];
// pair all direction values
const xyPairs = xDirs.flatMap((x) => yDirs.map((y) => [x, y]));
// remove 0,0 direction
xyPairs.splice(4, 1);
// console.log(xyPairs);

// I mistakenly thought this was going need a full depth first search so this was (poorly) written with that in mind at first
function searchMatrix(
  xyDirs: number[][],
  word: string[],
  matrix: string[][] = letterMatrix
): number {
  let foundWords = 0;
  const firstLetterCoords = [];
  for (let yIndex = 0; yIndex < rows; yIndex++) {
    for (let xIndex = 0; xIndex < cols; xIndex++) {
      if (letterMatrix[yIndex][xIndex] === word[0]) {
        // console.log(`${word[0]} is at ${xIndex}, ${yIndex}`);
        firstLetterCoords.push({ x: xIndex, y: yIndex });
        // iterate over all directions
        for (const pair of xyPairs) {
          let nextXCoord = xIndex + pair[0];
          let nextYCoord = yIndex + pair[1];
          // move in one step from direction pair for each letter
          for (const letter of word.slice(1)) {
            try {
              const letterAtCoord = letterMatrix[nextYCoord][nextXCoord];
              // console.log(letterAtCoord);
              if (letter === letterAtCoord) {
                // console.log({ letter: letter, x: nextXCoord, y: nextYCoord });
                if (letterAtCoord === word.at(-1)) {
                  // console.log("found a word");
                  foundWords += 1;
                  break;
                }
                nextXCoord = nextXCoord + pair[0];
                nextYCoord = nextYCoord + pair[1];
                // letter is correct but not S, continue with next letter using new coordinate.
                continue;
              } else {
                // letter is not correct
                break;
              }
            } catch (error) {
              // coordinate is out of bounds
              break;
            }
          }
        }
      }
    }
  }
  return foundWords;
}
const foundXmas = searchMatrix(xyPairs, Array.from("XMAS"));
console.log({ foundXmas });

// looks for the A and then checks the corners as sets.
function searchMatrixForMasCross(matrix: string[][] = letterMatrix): number {
  const word = Array.from("MAS");
  let foundMas = 0;
  for (let yIndex = 0; yIndex < rows; yIndex++) {
    for (let xIndex = 0; xIndex < cols; xIndex++) {
      if (letterMatrix[yIndex][xIndex] === word[1]) {
        // console.log(`${word[1]} is at ${xIndex}, ${yIndex}`);
        try {
          const topLeftLetter = letterMatrix[yIndex - 1][xIndex - 1];
          const bottomRightLetter = letterMatrix[yIndex + 1][xIndex + 1];
          const topRightLetter = letterMatrix[yIndex - 1][xIndex + 1];
          const bottomLeftLetter = letterMatrix[yIndex + 1][xIndex - 1];
          const firstSet = new Set([topLeftLetter, bottomRightLetter]);
          const secondSet = new Set([topRightLetter, bottomLeftLetter]);
          if (firstSet.has("M") && firstSet.has("S")) {
            if (secondSet.has("M") && secondSet.has("S")) {
              // console.log("have X-MAS")
              foundMas += 1;
            }
          }
        } catch (error) {
          break;
        }
      }
    }
  }
  return foundMas;
}
const foundXHyphenMas = searchMatrixForMasCross();
console.log({ foundXHyphenMas });
