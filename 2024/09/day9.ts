import * as fs from "fs";

const input = fs
  .readFileSync(process.cwd() + "/09/input.txt", "utf-8")
  .trim()
  .split("")
  .map((c) => Number(c));

// iterate input into pairs of disk values
const disk = input
  .reduce((acc: (string[] | number[])[][], _, index) => {
    if (index % 2 === 0) {
      const [size, free] = input.slice(index, index + 2);
      acc.push([
        new Array(size).fill(acc.length),
        // acc.length.toString().repeat(size),
        new Array(free).fill("."),
      ]);
    }
    return acc;
  }, [])
  .flat();

// recursively swap file blocks with empty space from end to start
function defrag(disk: (string[] | number[])[]) {
  const lastFileBlock = disk.findLastIndex((block) =>
    block.some((fileId) => typeof fileId === "number")
  );
  const lastFileBit = disk[lastFileBlock].findLastIndex(
    (bit) => typeof bit === "number"
  );
  const firstFreeBlock = disk.findIndex((block) =>
    block.some((bit) => bit === ".")
  );
  const firstFreeBit = disk[firstFreeBlock].findIndex((bit) => bit === ".");
  if (firstFreeBlock >= lastFileBlock && firstFreeBit > lastFileBit) {
    return disk;
  }
  disk[firstFreeBlock][firstFreeBit] = disk[lastFileBlock][lastFileBit];
  disk[lastFileBlock][lastFileBit] = ".";
  defrag(disk);
}

defrag(disk);
// reduce disk to checkSum by filtering on number and multiplying each fileId by the index
const checkSum = disk.flat().filter((bit)=> typeof bit === "number").reduce((sum: number, val: number, index) => {
    return (sum += val * index);
  }, 0);

console.log(checkSum);
