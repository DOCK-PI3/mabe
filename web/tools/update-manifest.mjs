import {readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import vm from 'node:vm';
const base=new URL('../',import.meta.url), context={window:{}};
vm.runInNewContext(await readFile(new URL('dist/catalog.js',base),'utf8'),context);
const manifest=[],ids=new Set(),hashes=new Set();
for(const item of context.window.PORTFOLIO){
  const bytes=await readFile(new URL(`dist/${item.src}`,base));
  const hash=createHash('sha256').update(bytes).digest('hex');
  if(ids.has(item.id)||hashes.has(hash))throw new Error(`Archivo repetido: ${item.id}`);
  ids.add(item.id);hashes.add(hash);
  manifest.push({id:item.id,type:item.type,sourceSha256:item.sourceSha256||null,webSha256:hash,bytes:bytes.length});
}
await writeFile(new URL('media-manifest.json',base),JSON.stringify(manifest,null,2)+'\n');
console.log(`${manifest.length} archivos registrados, sin contenido repetido.`);
