import * as fs from "fs";

type Row = [number, number[]];

const input = fs
  .readFileSync(process.cwd() + "/07/input.txt", "utf-8")
  .split("\n");

const rows = [];

for (const line of input) {
  const split1 = line.split(": ");
  const splitVals = split1[1]
    .split(" ")
    .map((val, index) => (index === 0 ? [Number(val)] : Number(val)));
  rows.push([Number(split1[0]), splitVals] as Row);
}

function valCombos(arr: any[], concat: boolean = false): number[] {
  const combosIn = arr.shift();
  if (arr.length) {
    const newCombos = [];
    for (const val of combosIn) {
      const sum = Number(val) + arr[0];
      const product = Number(val) * arr[0];
      newCombos.push(sum, product);
      if (concat) {
        const catted = Number(`${val}${arr[0]}`);
        newCombos.push(catted);
      }
    }
    arr.shift();
    arr.unshift(newCombos);
    return valCombos(arr, concat);
  } else {
    return combosIn;
  }
}

function sumRows(rows: Row[], concat: boolean = false) {
  let sum = 0;
  for (const row of rows) {
    const result = row[0];
    const rowCombos = valCombos(row[1], concat);
    if (rowCombos.includes(result)) {
      sum += result;
    }
  }
  return sum;
}

console.log(sumRows(structuredClone(rows)));
console.log(sumRows(structuredClone(rows), true));
