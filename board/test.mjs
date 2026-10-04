// Local test with an in-memory KV.
import W from './worker.js';
const kv=new Map();const env={BOARD:{get:async(k,t)=>kv.has(k)?JSON.parse(kv.get(k)):null,put:async(k,v)=>kv.set(k,v)}};
const words=JSON.parse((await import('fs')).readFileSync('words.json','utf8'));
const day=Math.floor((Date.now()-Date.UTC(2026,9,2))/864e5);
const ans=(ed)=>{const b=words[ed];return b[((day%b.length)+b.length)%b.length]};
const H={Origin:'https://tools.dnsc.ai','Content-Type':'application/json','CF-Connecting-IP':'1.2.3.4'};
async function post(body,hdr=H){const r=await W.fetch(new Request('https://x/submit',{method:'POST',headers:hdr,body:JSON.stringify(body)}),env);return [r.status,(await r.json())]}
const name=words.A[0]+' '+words.N[0];
console.log('ok   ',await post({ed:'regular',day,rows:['NOTES',ans('regular')],ms:42000,name,device:'device-one'}));
console.log('dupe ',await post({ed:'regular',day,rows:[ans('regular')],ms:1000,name:words.A[1]+' '+words.N[1],device:'device-one'}));
console.log('fake ',await post({ed:'regular',day,rows:['NOTES'],ms:1000,name:words.A[2]+' '+words.N[2],device:'device-two'}));
console.log('name ',await post({ed:'regular',day,rows:[ans('regular')],ms:1000,name:'Mean Words',device:'device-three'}));
console.log('adv  ',await post({ed:'advanced',day,rows:['ABCDEFG',ans('advanced')],ms:90000,name,device:'device-one'}));
console.log('len  ',await post({ed:'advanced',day,rows:['ABCDE',ans('advanced')],ms:1000,name:words.A[3]+' '+words.N[3],device:'device-four'}));
console.log('orig ',await post({ed:'regular',day,rows:[ans('regular')],ms:1,name:words.A[4]+' '+words.N[4],device:'device-five'},{...H,Origin:'https://evil.example'}));
const g=await W.fetch(new Request(`https://x/board?ed=regular&day=${day}`,{headers:{Origin:'https://tools.dnsc.ai'}}),env);console.log('board',g.status,JSON.stringify(await g.json()));
