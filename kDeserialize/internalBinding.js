const { WritableStream } = require('node:stream/web');

const ws = new WritableStream();
const symbols = Object.getOwnPropertySymbols(Object.getPrototypeOf(ws));

for (const s of symbols) {
  console.log(s.toString());
}
