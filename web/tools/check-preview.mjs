// Comprobación breve del servidor local; lo cierra al terminar.
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const port=4174;
const child=spawn(process.execPath,[fileURLToPath(new URL('./server.mjs',import.meta.url))],{env:{...process.env,PORT:String(port)},stdio:['ignore','pipe','pipe'],windowsHide:true});
try {
  await new Promise((resolve,reject)=>{child.stdout.once('data',resolve);child.once('error',reject);child.once('exit',code=>reject(new Error(`Servidor terminado: ${code}`)))});
  const base=`http://127.0.0.1:${port}`;
  for(const file of ['/','/cuaderno.html','/cine.html','/taller.html']){
    const response=await fetch(base+file);if(response.status!==200)throw new Error(`${file}: ${response.status}`);
  }
  const range=await fetch(base+'/assets/videos/VID20250819172959.mp4',{headers:{Range:'bytes=0-1023'}});
  if(range.status!==206||(await range.arrayBuffer()).byteLength!==1024)throw new Error('Lectura parcial de vídeo incorrecta');
  const missing=await fetch(base+'/archivo-inexistente');if(missing.status!==404)throw new Error('404 incorrecto');
  console.log('Vista previa verificada: cuatro páginas, vídeo con lectura parcial y archivo inexistente.');
} finally {child.kill()}
