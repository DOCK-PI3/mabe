import {readFile,stat,readdir} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import vm from 'node:vm';
import {createHash} from 'node:crypto';
const root=fileURLToPath(new URL('../dist/',import.meta.url));
const context={window:{}};
vm.runInNewContext(await readFile(path.join(root,'catalog.js'),'utf8'),context);
const items=context.window.PORTFOLIO;
const excluded=['IMG20250825163127','IMG20250825163203','IMG20250825163219','IMG20250825163226','IMG20250928233359','20210416_224026'];
const ids=new Set();
const sourceHashes=new Set();
const webHashes=new Set();
const manifest=JSON.parse(await readFile(fileURLToPath(new URL('../media-manifest.json',import.meta.url)),'utf8'));
for(const item of items){
  if(ids.has(item.id))throw new Error(`ID repetido: ${item.id}`);
  ids.add(item.id);
  if(item.sourceSha256){
    if(sourceHashes.has(item.sourceSha256))throw new Error(`Contenido original repetido: ${item.id}`);
    sourceHashes.add(item.sourceSha256);
  }
  const record=manifest.find(x=>x.id===item.id);
  if(!record)throw new Error(`Archivo no registrado en el manifiesto: ${item.id}`);
  const actualHash=createHash('sha256').update(await readFile(path.join(root,item.src))).digest('hex');
  if(actualHash!==record.webSha256)throw new Error(`El contenido cambió respecto al manifiesto: ${item.id}`);
  if(webHashes.has(record.webSha256))throw new Error(`Contenido web repetido: ${item.id}`);
  webHashes.add(record.webSha256);
  for(const asset of new Set([item.src,item.poster])){
    const info=await stat(path.join(root,asset));
    if(info.size>=100*1024*1024)throw new Error(`Archivo demasiado grande para GitHub: ${asset}`);
  }
}
for(const id of excluded){if(ids.has(id))throw new Error(`Archivo excluido en catálogo: ${id}`)}
for(const html of ['index.html','cuaderno.html','cine.html','taller.html']){
  const text=await readFile(path.join(root,html),'utf8');
  for(const match of text.matchAll(/(?:src|href)="([^"#]+)"/g)){
    const ref=match[1];if(/^(data:|https?:|mailto:|tel:)/.test(ref)||ref.endsWith('/'))continue;
    await stat(path.join(root,ref.split(/[?#]/)[0]));
  }
}
for(const file of ['config.js','catalog.js','app.js'])new vm.Script(await readFile(path.join(root,file),'utf8'));
const actualImages=await readdir(path.join(root,'assets','images'));
for(const file of actualImages){if(excluded.some(id=>file.startsWith(id)))throw new Error(`Archivo excluido en carpeta pública: ${file}`)}
console.log(`Correcto: ${items.filter(x=>x.type==='image').length} fotos, ${items.filter(x=>x.type==='video').length} vídeos; sin IDs ni hashes repetidos; archivos y enlaces locales presentes.`);
