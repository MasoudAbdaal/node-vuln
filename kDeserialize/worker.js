// worker.js
const { parentPort } = require('node:worker_threads');

parentPort.on('message', (m) => {
  if (m && m.tag === 'stream') {
    const stream = m.s;
    console.log('[Worker] received stream object:', stream);

    // try to get a writer and write (this exercises the deserialized stream)
    const w = stream.getWriter();
    w.write('hello from worker').catch(e => console.error('[Worker] write error', e));
    w.close();

    // send back the list of visible symbols on the received object
    parentPort.postMessage({
      ok: true,
      protoSymbols: Object.getOwnPropertySymbols(Object.getPrototypeOf(stream)).map(s => s.toString()),
      ownSymbols: Object.getOwnPropertySymbols(stream).map(s => s.toString())
    });
  }
});
