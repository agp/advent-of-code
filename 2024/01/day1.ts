import * as fs from "fs";

const inputArrayOne: number[] = [];
const inputArrayTwo: number[] = [];

function sortArray(arr: number[]) {
  const sorted = arr.toSorted((a, b) => {
    return a - b;
  });
  return sorted;
}

const input = fs
  .readFileSync(process.cwd() + "/01/input.txt", "utf-8")
  .split("\n");
for (const line of input) {
  const lineSplit = line.split("   ");
  inputArrayOne.push(Number(lineSplit[0]));
  inputArrayTwo.push(Number(lineSplit[1]));
}

const sortedListOne = sortArray(inputArrayOne);
const sortedListTwo = sortArray(inputArrayTwo);
console.log(sortedListOne);
console.log(sortedListTwo);

let totalDistance = 0;
for (let i = 0; i < sortedListOne.length; i++) {
  const distanceForIndex = Math.abs(sortedListOne[i] - sortedListTwo[i]);
  // console.log(distanceForIndex);
  totalDistance += distanceForIndex;
}
// console.log(totalDistance);

let totalSimilarity = 0;
for (const locID of sortedListOne) {
  const listTwoOccurrences = sortedListTwo.reduce(
    (accumulator, currentValue) =>
      locID === currentValue ? ++accumulator : accumulator,
    0
  );
  totalSimilarity += locID * listTwoOccurrences;
}

console.log(totalDistance);
console.log(totalSimilarity);
