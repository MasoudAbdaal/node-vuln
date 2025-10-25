// main.js
// node --expose-internals  .\main.js
const { Worker } = require('node:worker_threads');
const { WritableStream } = require('node:stream/web');

console.log('Node version:', process.version);

// -------------- try to require internal module ----------------
let transferable;
try {
  transferable = require('internal/worker/js_transferable');
  console.log('\n[internal/worker/js_transferable] loaded — keys:');
  console.log(Object.keys(transferable));
} catch (err) {
  console.error('\nCould not require internal/worker/js_transferable:', err.message);
}

// -------------- create a WritableStream ----------------
const writable = new WritableStream({
  write(chunk) { console.log('[Main] wrote chunk:', chunk); },
  close() { console.log('[Main] closed'); }
});
console.log('\n[Main] WritableStream created:', writable);

// -------------- inspect object's symbols ----------------
const protoSymbols = Object.getOwnPropertySymbols(Object.getPrototypeOf(writable));
const ownSymbols = Object.getOwnPropertySymbols(writable);
console.log('\n[Main] prototype symbols:', protoSymbols.map(s => s.toString()));
console.log('[Main] own symbols:', ownSymbols.map(s => s.toString()));

// -------------- if we loaded transferable, inspect exported symbols -----------
if (transferable) {
  // print exported symbol-desc or functions
  for (const k of Object.keys(transferable)) {
    console.log('[transferable exported key]', k, typeof transferable[k]);
  }

  // transferable may export actual Symbols (not as object keys),
  // try to print Symbol values if present (some exports are Symbols)
  // iterate over all exported props including symbols:
  const allPropNames = [
    ...Object.getOwnPropertyNames(transferable),
    ...Object.getOwnPropertySymbols(transferable).map(s => s.toString())
  ];
  console.log('\n[transferable all props]:', allPropNames);

  // If transferable exports the actual Symbol objects (e.g. transferable.kTransfer),
  // we can try to call writable[thatSymbol]() — but it may or may not exist.
  if (transferable.kTransfer) {
    console.log('\nFOUND transferable.kTransfer symbol (or value):', transferable.kTransfer.toString?.() || transferable.kTransfer);
    try {
      const tInfo = writable[transferable.kTransfer]?.();
      console.log('\nResult of writable[kTransfer]():', tInfo);
    } catch (e) {
      console.error('\nCalling writable[kTransfer]() threw:', e);
    }
  } else {
    console.log('\ntransferable.kTransfer not exported as property named kTransfer.');
    // try to find any Symbol within transferable values:
    const symProps = Object.getOwnPropertySymbols(transferable);
    console.log('transferable symbols:', symProps.map(s => s.toString()));
  }
} else {
  console.log('\n(no transferable module loaded — cannot introspect kTransfer/kDeserialize)');
}

// -------------- fallback: actually send the stream to a worker to observe runtime behavior -------------
console.log('\n-- now sending stream to a worker (standard postMessage) --');
const worker = new Worker('./worker.js');
worker.postMessage({ tag: 'stream', s: writable }, [writable]);

worker.on('message', (m) => {
  console.log('\n[Main] message from worker:', m);
});
worker.on('error', (err) => {
  console.error('[Main] worker error:', err);
});
