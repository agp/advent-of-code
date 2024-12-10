import * as fs from "fs";

const input = fs
  .readFileSync(process.cwd() + "/09/input.txt", "utf-8")
  .trim()
  .split("")
  .map((c) => Number(c));

// iterate input into pairs of disk values and push file id repeats and free space (.) into pairs
const disk = input
  .reduce((acc: any[][][], _, index) => {
    if (index % 2 === 0) {
      const [size, free] = input.slice(index, index + 2);
      acc.push([
        new Array(size).fill(acc.length),
        free ? new Array(free).fill(".") : [],
      ]);
    }
    return acc;
  }, [])
  .flat();

// recursively swap file block bits with empty space from end to start
function defrag(diskIn: any[][]) {
  const lastFileBlock = diskIn.findLastIndex((block) =>
    block.some((fileId) => typeof fileId === "number")
  );
  const lastFileBit = diskIn[lastFileBlock].findLastIndex(
    (bit) => typeof bit === "number"
  );
  const firstFreeBlock = diskIn.findIndex((block) =>
    block.some((bit) => bit === ".")
  );
  const firstFreeBit = diskIn[firstFreeBlock].findIndex((bit) => bit === ".");
  if (firstFreeBlock >= lastFileBlock && firstFreeBit > lastFileBit) {
    return diskIn;
  }
  diskIn[firstFreeBlock][firstFreeBit] = diskIn[lastFileBlock][lastFileBit];
  diskIn[lastFileBlock][lastFileBit] = ".";
  return defrag(diskIn);
}

// reduce disk to checkSum by filtering on number and multiplying each fileId by the index
function getCheckSum(diskToSum: any[][]) {
  return diskToSum.flat().reduce((sum: number, val: number, index) => {
    return typeof val === "number" ? (sum += val * index) : sum;
  }, 0);
}

// so slow... not sure what I was thinking here today
const t0 = performance.now();
const deFraggedDisk = defrag(structuredClone(disk));
const part1Sum = getCheckSum(deFraggedDisk);
console.log(part1Sum);
const t1 = performance.now();
console.log(`de-fragging bits and sum took ${t1 - t0} milliseconds.`);

// part 2

// recursively swap file blocks with empty blocks from end to start
function defragBlock(diskIn: any[][], lastIndex: number = diskIn.length - 1) {
  // find the next file block to eval for defrag
  const currFileBlockIndex = diskIn
    .slice(0, lastIndex)
    .findLastIndex((block) =>
      block.some((fileId) => typeof fileId === "number")
    );
  // find the first free block that contains free space and sufficient size for current file block
    const freeBlockIndex = diskIn.findIndex(
    (block) =>
      block.some((bit) => bit === ".") &&
      block.reduce((acc, val) => {
        return val === "." ? (acc += 1) : acc;
      }, 0) >= diskIn[currFileBlockIndex].length
  );
  // if free block is found and is lower index, copy the block onto free space
  if (freeBlockIndex != -1 && freeBlockIndex < currFileBlockIndex) {
    const firstFreeBit = diskIn[freeBlockIndex].findIndex((bit) => bit === ".");
    diskIn[freeBlockIndex].splice(
      firstFreeBit,
      diskIn[currFileBlockIndex].length,
      ...diskIn[currFileBlockIndex]
    );
    // . out the copied block
    diskIn[currFileBlockIndex].fill(".");
  }
  // recurse while positive working index
  if (currFileBlockIndex > 0) {
    return defragBlock(diskIn, currFileBlockIndex);
  }
  return diskIn;
}

const t2 = performance.now();
const part2Disk = defragBlock(structuredClone(disk));
const part2Sum = getCheckSum(part2Disk);
console.log(part2Sum);
const t3 = performance.now();
console.log(`de-fragging blocks and sum took ${t3 - t2} milliseconds.`);