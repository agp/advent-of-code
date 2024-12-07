import * as fs from "fs";

const input = fs.readFileSync(process.cwd() + "/03/input.txt", "utf-8");

const regex = /mul\((\d{1,3}),(\d{1,3})\)/gm;
const matches = input.matchAll(regex);
let sum = 0;
for (const match of matches) {
  const product = Number(match[1]) * Number(match[2]);
  sum += product;
}

let sumDo = 0;
const regexDo = /mul\((\d{1,3}),(\d{1,3})\)|do(?:n't)?/gm;
const matchesDo = input.matchAll(regexDo);
let enabled = true;
for (const match of matchesDo) {
  if (match[0] === "do") {
    enabled = true;
  } else if (match[0] === "don't") {
    enabled = false;
  } else {
    if (enabled) {
      const product = Number(match[1]) * Number(match[2]);
      sumDo += product;
    }
  }
}
console.log(sum);
console.log(sumDo);
