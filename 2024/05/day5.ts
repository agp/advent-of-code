import * as fs from "fs";

const input = fs
  .readFileSync(process.cwd() + "/05/input.txt", "utf-8")
  .split("\n");

const orderRules: number[][] = [];
const updates = [];

for (const line of input) {
  if (line.includes("|")) {
    const ruleSplit = line.split("|");
    orderRules.push(ruleSplit.map((rule) => Number(rule)));
  } else if (line.includes(",")) {
    const updatesSplit = line.split(",");
    updates.push(updatesSplit.map((page) => Number(page)));
  }
}
// console.log(orderRules);
// console.log(updates);

function checkPageOrder(update: number[]) {
  for (const page of update) {
    // console.log(`outer loop page: ${page}`);
    const pageIndex = update.indexOf(page);
    for (const nextPage of update.slice(pageIndex + 1)) {
      // console.log({ page });
      // console.log({ nextPage });
      for (const rule of orderRules) {
        const pageInRule = rule.includes(page);
        const nextPageInRule = rule.includes(nextPage);
        if (pageInRule && nextPageInRule) {
          // console.log(`found rule:${rule} with page:${page} and next page:${nextPage}`)
          const pageFollowsRule = rule.indexOf(page) === 0;
          if (pageFollowsRule) {
            continue;
          } else {
            return false;
          }
        }
      }
    }
  }
  return true;
}

// create a map with each page and a set of pages that it should come after
const ruleMap = new Map();
for (const [a, b] of orderRules) {
  if (!ruleMap.has(b)) {
    ruleMap.set(b, new Set());
  }
  ruleMap.get(b).add(a);
}
console.log(ruleMap);

// sort using ruleMap
function reorderUpdate(update: number[]) {
  const updateSorted = update.toSorted((a, b) => {
    // a should come before b
    if (ruleMap.get(a)?.has(b)) return 1;
    // b should come after a
    if (ruleMap.get(b)?.has(a)) return -1;
    // a and b don't have order
    return 0;
  });
  return updateSorted;
}

let middleSum = 0;
let reOrderSum = 0;
for (const update of updates) {
  const updateCorrect = checkPageOrder(update);
  if (updateCorrect) {
    // console.log(update);
    middleSum += update[Math.floor(update.length / 2)];
  } else {
    const newUpdate = reorderUpdate([...update]);
    reOrderSum += newUpdate[Math.floor(update.length / 2)];
  }
}

console.log(middleSum);
console.log(reOrderSum);
