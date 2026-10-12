'use strict';
const $ = id => document.getElementById(id);
const NS = 'http://www.w3.org/2000/svg';
const GROUPS = [
  ['heat', 'Calor', ['tasmaxmax', 'tasmaxhwdmax']],
  ['dry', 'Sequía', ['prspellb1']],
  ['rain', 'Lluvia', ['prmax24']],
  ['fire', 'Incendios', ['fwi_days_gt30', 'fwi_mean', 'fire_context']],
  ['flood', 'Inundación', ['river_flood_10cm', 'river_flood', 'official', 'aqueduct_history', 'agreement']]
];
const A = 'https://escenarios.adaptecca.es/info';
const W = 'https://aqueduct.wridata.org/AqueductFloods20/index.html';
const H = 'https://doi.org/10.5281/zenodo.19792063';
const M = 'https://www.miteco.gob.es/es/cartografia-y-sig/ide/descargas/agua/zi-lamina.html';
const CONFIG = {
  tasmaxmax: {name:'Calor extremo',unit:'°C',source:'AdapteCCa',url:A,definition:'Máxima diaria anual, promediada en el periodo.',note:'Promedio de una celda, no récord de temperatura.'},
  tasmaxhwdmax: {name:'Duración de las olas de calor',unit:'días',source:'AdapteCCa',url:A,definition:'Duración de la ola de calor más larga del año.',note:'Se mide respecto al calor habitual de cada lugar.'},
  prspellb1: {name:'Duración de los periodos secos',unit:'días',source:'AdapteCCa',url:A,definition:'Periodo anual más largo con menos de 1 mm de lluvia al día.',note:'No mide la disponibilidad de agua.'},
  prmax24: {name:'Lluvia extrema',unit:'mm',source:'AdapteCCa',url:A,definition:'Máxima lluvia diaria anual, promediada en el periodo.',note:'No mide la profundidad de una inundación.',blue:true},
  fwi_days_gt30: {name:'Días con FWI >30',unit:'días/año',source:'Hetzer / FirEUrisk',url:H,definition:'Días al año con condiciones meteorológicas favorables al fuego, según el umbral FWI >30.',note:'Un modelo climático. No es la probabilidad de incendio.',fire:true},
  fwi_mean: {name:'Índice meteorológico de incendios',unit:'FWI',source:'Hetzer / FirEUrisk',url:H,definition:'Índice meteorológico de incendios, media anual.',note:'Un modelo climático. No incluye igniciones ni vegetación.',fire:true},
  fire_context: {name:'Verano · contexto regional',unit:'FWI',source:'FIRE-RES',url:'https://doi.org/10.5281/zenodo.11083641',definition:'Índice meteorológico de incendios, media de junio a agosto.',note:'Celdas de unos 40 × 55 km. Los escenarios pueden combinar modelos distintos.',coarse:true},
  river_flood_10cm: {name:'Ríos · profundidad >0,1 m',unit:'% de área modelada',source:'WRI Aqueduct',url:W,definition:'Superficie inundada en un evento fluvial de retorno de 100 años.',note:'Experimental: fuerte desacuerdo con los mapas oficiales.',river:true,blue:true},
  river_flood: {name:'Ríos · cualquier profundidad',unit:'% de área modelada',source:'WRI Aqueduct',url:W,definition:'Superficie con cualquier profundidad positiva en un evento de retorno de 100 años.',note:'Incluye profundidades de centímetros. Muy sensible al umbral.',river:true,blue:true},
  official: {name:'Mapa oficial · SNCZI',unit:'% de celda',source:'MITECO · SNCZI',url:M,definition:'Superficie incluida en los polígonos oficiales de inundación fluvial T100.',note:'Fuera de los polígonos, la cobertura de los estudios es desconocida.',comparison:true,blue:true},
  aqueduct_history: {name:'Comparar · Aqueduct histórico',unit:'% de área modelada',source:'WRI Aqueduct',url:W,definition:'Superficie inundada en el modelo histórico de Aqueduct, con el umbral elegido.',note:'Cambiar el umbral no corrige ni valida el modelo.',comparison:true,blue:true},
  agreement: {name:'Comparar · coincidencia con SNCZI',unit:'% de coincidencia',source:'SNCZI / Aqueduct',url:M,definition:'Parte del área oficial cubierta por Aqueduct que también aparece inundada en el modelo.',note:'Mayor coincidencia no significa mayor peligro. No es una medida de precisión global.',comparison:true,blue:true}
};
const S = {group:'heat',layer:'tasmaxmax',mode:'future',scenario:'ssp245',threshold:'0.1',fine:null,coarse:null,place:null};
const scenarioNames={ssp126:'SSP1-2.6',ssp245:'SSP2-4.5',ssp370:'SSP3-7.0',ssp585:'SSP5-8.5',rcp45:'RCP4.5'};
const modeNames={future:'2050',baseline:'Histórico',change:'Cambio',near:'2011–2040',spread:'Dispersión entre modelos',coverage:'Cobertura de datos'};
let renderedGrid=null, current=null;
const fmt=(v,d=1)=>v===null||!Number.isFinite(v)?'Sin datos':v.toLocaleString('es-ES',{minimumFractionDigits:d,maximumFractionDigits:d});
const signed=v=>v===null?'Sin datos':(v>0?'+':'')+fmt(v);
const dateFrom=s=>(s.match(/\d{4}[–-]\d{4}/)||[])[0]||s;
const exists=k=>k==='fire_context'?!!D.fire_context:CONFIG[k].comparison?!!D.flood_validation:!!D.values[k];
function option(select,value,label){select.add(new Option(label,value));}
function scenarios(){
 const c=CONFIG[S.layer];
 return c.comparison?['reference']:Object.keys(c.coarse?D.fire_context.values:D.values[S.layer]);
}
function modes(){
 const c=CONFIG[S.layer];
 return c.comparison?['baseline']:c.coarse?['future','baseline','change']:(D.metadata[S.layer].available_modes||['future','baseline','change','near','spread','coverage']);
}
function setupControls(){
 const c=CONFIG[S.layer],ss=scenarios(),mm=modes();
 if(!ss.includes(S.scenario))S.scenario=ss.includes('ssp245')?'ssp245':ss[0];
 if(!mm.includes(S.mode))S.mode=c.comparison?'baseline':'future';
 $('scenario').replaceChildren();ss.forEach(s=>option($('scenario'),s,scenarioNames[s]||'Referencia'));
 $('scenario').value=S.scenario;$('scenario').parentElement.hidden=c.comparison;
 $('threshold-field').hidden=!['aqueduct_history','agreement'].includes(S.layer);
 $('periods').replaceChildren();
 for(const k of ['future','baseline','change'].filter(k=>mm.includes(k))){
  const b=document.createElement('button');b.textContent=modeNames[k];b.type='button';b.dataset.mode=k;
  b.onclick=()=>{S.mode=k;render();};$('periods').appendChild(b);
 }
 $('periods').hidden=c.comparison;
 $('extra-view').replaceChildren();mm.forEach(k=>option($('extra-view'),k,modeNames[k]));
 $('extra-field').hidden=c.comparison||c.coarse;
 $('resolution').textContent=c.coarse?'Cuadrícula de ~0,5°':'Cuadrícula de 10 km';
}
function setGroup(group){
 S.group=group;const layers=GROUPS.find(g=>g[0]===group)[2].filter(exists);
 $('layer').replaceChildren();layers.forEach(k=>option($('layer'),k,CONFIG[k].name));
 if(!layers.includes(S.layer))S.layer=layers[0];
 $('layer').value=S.layer;
 for(const b of $('hazards').children)b.setAttribute('aria-pressed',String(b.dataset.group===group));
 setupControls();render();if(S.place)selectCity(S.place);
}
function modelNote(c){
 if(c.comparison)return 'T100 · fuentes distintas';
 if(c.coarse)return 'Media publicada';
 if(c.fire)return '1 modelo · MRI-ESM2-0';
 if(c.river)return '5 forzamientos · sin defensas';
 return '11 modelos · mediana';
}
function getData(){
 const c=CONFIG[S.layer];
 if(c.comparison){
  const f=D.flood_validation,arr=f.cells.map(cell=>{
   if(S.layer==='official')return cell.official_positive_km2>0?100*cell.official_positive_fraction_of_cell:null;
   if(S.layer==='aqueduct_history')return cell.aqueduct_valid_fraction_of_cell>=.8?100*cell.thresholds[S.threshold].aqueduct_positive_fraction_of_valid_area:null;
   const den=cell.official_positive_with_aqueduct_coverage_km2;
   return den>0?100*cell.thresholds[S.threshold].intersection_km2/den:null;
  });
  return {arr,domain:S.layer==='official'?arr:[0,100],baseline:'1960–1999',future:'Compilación SNCZI',period:S.layer==='official'?'SNCZI · estudios de distintas fechas':S.layer==='agreement'?'SNCZI ↔ Aqueduct · 1960–1999':'Aqueduct · 1960–1999',unit:c.unit};
 }
 const r=c.coarse?D.fire_context.values[S.scenario]:D.values[S.layer][S.scenario];
 const meta=c.coarse?{baseline_label:'1995–2014',future_label:'2041–2060'}:D.metadata[S.layer];
 const baseline=dateFrom(meta.baseline_label),future=dateFrom(meta.future_label);
 const all=Object.values(c.coarse?D.fire_context.values:D.values[S.layer]);
 let domain=all.flatMap(z=>(['future','baseline','near'].includes(S.mode)?['future','baseline',...(z.near?['near']:[])]:[S.mode]).flatMap(k=>z[k]||[]));
 let arr=r[S.mode];let unit=c.unit;
 if(S.mode==='coverage'){arr=arr.map(v=>v===null?null:100*v);domain=[0,100];unit='% de cobertura';}
 if(c.river&&['change','spread'].includes(S.mode))unit='puntos porcentuales';
 let period=S.mode==='baseline'?baseline:S.mode==='near'?'2011–2040':S.mode==='change'?`${baseline} → ${future}`:future;
 if(c.coarse)period+=' · junio–agosto';
 return {r,arr,domain,baseline,future,period,unit};
}
function ramp(t,blue){
 const stops=blue?[[234,243,242],[114,162,173],[36,79,115]]:[[250,242,213],[222,162,102],[177,65,40]];
 const n=t<=.5?0:1,u=t<=.5?t*2:(t-.5)*2;
 return `rgb(${stops[n].map((a,i)=>Math.round(a+(stops[n+1][i]-a)*u)).join(',')})`;
}
function color(v,lo,hi,c){
 if(v===null)return 'url(#missing)';
 let t=hi>lo?Math.min(1,Math.max(0,(v-lo)/(hi-lo))):.5;
 if(S.mode==='change'){
  const a=t<.5?[57,116,150]:[246,245,235],b=t<.5?[246,245,235]:[177,65,40],u=t<.5?t*2:(t-.5)*2;
  return `rgb(${a.map((x,i)=>Math.round(x+(b[i]-x)*u)).join(',')})`;
 }
 return ramp(t,c.blue||S.mode==='coverage');
}
function selected(){return CONFIG[S.layer].coarse?S.coarse:S.fine;}
function choose(i){if(CONFIG[S.layer].coarse)S.coarse=i;else S.fine=i;S.place=null;$('place').value='';render();}
function makeMap(){
 const c=CONFIG[S.layer],grid=c.coarse?'coarse':'fine';
 if(renderedGrid===grid)return;
 renderedGrid=grid;$('cells').replaceChildren();
 const paths=c.coarse?D.fire_context.paths:D.paths;
 paths.forEach((d,i)=>{
  const p=document.createElementNS(NS,'path');p.setAttribute('d',d);p.setAttribute('role','button');
  p.onclick=()=>choose(i);
  p.onkeydown=e=>{
   if(['Enter',' '].includes(e.key)){e.preventDefault();choose(i);}
   if(['ArrowRight','ArrowDown','ArrowLeft','ArrowUp'].includes(e.key)){
    e.preventDefault();
    const direction={ArrowRight:[1,0],ArrowLeft:[-1,0],ArrowDown:[0,1],ArrowUp:[0,-1]}[e.key];
    const origin=p.getBBox(),ox=origin.x+origin.width/2,oy=origin.y+origin.height/2;
    let j=i,best=Infinity;
    [...$('cells').children].forEach((candidate,k)=>{
     const b=candidate.getBBox(),dx=b.x+b.width/2-ox,dy=b.y+b.height/2-oy;
     const along=dx*direction[0]+dy*direction[1],across=Math.abs(dx*direction[1]-dy*direction[0]);
     const score=Math.hypot(dx,dy)+3*across;
     if(along>1&&score<best){j=k;best=score;}
    });
    choose(j);$('cells').children[j].focus();
   }
  };
  $('cells').appendChild(p);
 });
}
function row(label,value){return `<div class="value-row"><dt>${label}</dt><dd>${value}</dd></div>`;}
function selectCity(name){
 const city=D.cities.find(c=>c[0]===name);if(!city)return;
 const point=new DOMPoint(city[1],city[2]);
 const i=[...$('cells').children].findIndex(p=>p.isPointInFill(point));
 if(i>=0){if(CONFIG[S.layer].coarse)S.coarse=i;else S.fine=i;S.place=name;render();}
}
function renderDetails(c,x){
 const i=selected();$('clear-selection').hidden=i===null;
 if(i===null){
  $('selection').innerHTML='<div class="empty"><strong>Elige una zona.</strong><p>Haz clic en el mapa para comparar sus valores.</p></div>';
 }else{
  const cell=c.coarse?D.fire_context.cells[i]:D.cells[i];
  const name=S.place||'Zona seleccionada';
  const value=x.arr[i];let rows='',caption=S.mode==='change'?'Cambio respecto al periodo histórico':S.mode==='spread'?'Rango P90 − P10':x.period;
  if(c.comparison){
   const a=D.flood_validation.cells[i],r=a.thresholds[S.threshold];
   rows=row('SNCZI',fmt(a.official_positive_km2)+' km²')+row(`Aqueduct >${S.threshold.replace('.',',')} m`,fmt(r.aqueduct_positive_km2)+' km²')+row('Coincidencia',fmt(r.intersection_km2)+' km²');
  }else{
   rows=(S.mode==='baseline'?'':row(x.baseline,fmt(x.r.baseline[i])+' '+c.unit))+(S.mode==='future'?'':row(x.future,fmt(x.r.future[i])+' '+c.unit))+row(c.fire||c.coarse||c.river?'Cambio':'Cambio por modelo',signed(x.r.change[i])+' '+(c.river?'pp':c.unit));
  }
  $('selection').innerHTML=`<p class="eyebrow">${c.coarse?'Celda regional':fmt(cell.area_km2,0)+' km²'}</p><h2>${name}</h2><div class="big-value">${value===null?'—':fmt(value)}<small>${value===null?'':x.unit}</small></div><p class="value-caption">${value===null?(S.layer==='official'?'Sin polígono oficial':'Sin datos suficientes'):caption}</p><dl class="value-rows">${rows}</dl>`;
 }
 $('definition').textContent=c.definition;$('caveat').textContent=c.note;
 let method='';
 if(c.comparison){
  const f=D.flood_validation.metadata,t=f.thresholds[S.threshold];
  method=`<p>Comparación de superficies positivas. Los mapas difieren en fechas, cauces y métodos. No conocemos el dominio completo de los estudios oficiales.</p><div class="method-stat"><span>SNCZI · Galicia</span><span>${fmt(f.official_positive_km2)} km²</span></div><div class="method-stat"><span>Coincidencia · >${S.threshold.replace('.',',')} m</span><span>${fmt(100*t.official_positive_in_valid_captured_fraction)}%</span></div><p>La coincidencia usa el área oficial con cobertura de Aqueduct. Los umbrales son una prueba de sensibilidad.</p>`;
 }else if(c.coarse){
  method='<p>Media publicada por FIRE-RES, junio–agosto. Se conserva la cuadrícula original; no distingue zonas de 10 km. La composición del conjunto de modelos no está documentada en estos archivos.</p>';
 }else{
  method=`<p>${c.fire?'MRI-ESM2-0, SSP2-4.5. Se promedian 20 años por periodo; el umbral FWI >30 se aplica antes de agregar.':c.river?'Un modelo hidrológico, cinco forzamientos climáticos. Sin defensas; no cubre todos los cauces pequeños ni la inundación pluvial o costera.':'Mediana de 11 modelos. Primero se promedian los valores dentro de cada celda; después se resume el conjunto.'} Se exige al menos un 80% de cobertura.</p>`;
  if(!c.fire)method+=c.river?'<p>Los cambios usan una única referencia histórica WATCH. Los cinco forzamientos comparten el mismo modelo hidrológico.</p>':'<p>El cambio se calcula por modelo antes de resumirlo. Puede diferir de la resta de las medianas. La dispersión no es un intervalo de confianza.</p>';
  if(i!==null&&x.r.p10&&x.r.p10[i]!==null)method+=`<div class="method-stat"><span>Modelos · P10–P90</span><span>${fmt(x.r.p10[i])} – ${fmt(x.r.p90[i])} ${c.unit}</span></div>`;
  if(i!==null)method+=`<div class="method-stat"><span>Cobertura de la celda</span><span>${fmt(100*x.r.coverage[i])}%</span></div>`;
 }
 method+=`<a href="${c.url}" target="_blank" rel="noopener">${c.source} ↗</a>`;
 if(i!==null)method+=`<div class="method-stat"><span>Celda</span><span>${(c.coarse?D.fire_context.cells:D.cells)[i].id}</span></div>`;
 $('method-info').innerHTML=method;
 $('source-credit').textContent=c.source;$('source-credit').href=c.url;
}
function render(){
 const c=CONFIG[S.layer];makeMap();const x=getData();current=x;
 let domain=x.domain.filter(v=>v!==null&&Number.isFinite(v)),lo=domain.length?Math.min(...domain):0,hi=domain.length?Math.max(...domain):1;
 if(S.mode==='change'){hi=Math.max(Math.abs(lo),Math.abs(hi));lo=-hi;}
 const chosen=selected();
 [...$('cells').children].forEach((p,i)=>{
  p.style.fill=color(x.arr[i],lo,hi,c);p.classList.toggle('selected',i===chosen);p.setAttribute('aria-pressed',String(i===chosen));p.setAttribute('tabindex',i===(chosen??0)?'0':'-1');
  p.setAttribute('aria-label',`${c.name}: ${fmt(x.arr[i])} ${x.unit}`);
 });
 $('map-period').textContent=x.period;$('map-models').textContent=modelNote(c);
 $('low').textContent=fmt(lo);$('high').textContent=fmt(hi);$('unit').textContent=x.unit;
 $('gradient').style.background=S.mode==='change'?'linear-gradient(to right,#397496,#f6f5eb,#b14128)':`linear-gradient(to right,${ramp(0,c.blue||S.mode==='coverage')},${ramp(.5,c.blue||S.mode==='coverage')},${ramp(1,c.blue||S.mode==='coverage')})`;
 $('missing-note').textContent=S.layer==='official'?'Rayado: sin polígono oficial; no implica ausencia de inundación.':S.layer==='agreement'?'Rayado: sin área oficial comparable.':'Rayado: datos insuficientes.';
 for(const b of $('periods').children)b.setAttribute('aria-pressed',String(b.dataset.mode===S.mode));
 $('extra-view').value=S.mode;renderDetails(c,x);
}
for(const [group,name,keys] of GROUPS){
 if(!keys.some(exists))continue;const b=document.createElement('button');b.type='button';b.textContent=name;b.dataset.group=group;b.onclick=()=>setGroup(group);$('hazards').appendChild(b);
}
$('map').setAttribute('viewBox',`-15 -12 690 ${D.height+24}`);
for(const [name,x,y] of D.cities){
 const dot=document.createElementNS(NS,'circle');dot.setAttribute('cx',x);dot.setAttribute('cy',y);dot.setAttribute('r','2');$('cities').appendChild(dot);
 const t=document.createElementNS(NS,'text');t.setAttribute('x',x+5);t.setAttribute('y',y+3);t.textContent=name;$('cities').appendChild(t);option($('place'),name,name);
}
$('layer').onchange=()=>{S.layer=$('layer').value;setupControls();render();if(S.place)selectCity(S.place);};
$('scenario').onchange=()=>{S.scenario=$('scenario').value;render();};
$('threshold').onchange=()=>{S.threshold=$('threshold').value;render();};
$('extra-view').onchange=()=>{S.mode=$('extra-view').value;render();};
$('place').onchange=()=>selectCity($('place').value);
$('clear-selection').onclick=()=>{if(CONFIG[S.layer].coarse)S.coarse=null;else S.fine=null;S.place=null;$('place').value='';render();};
$('download').onclick=()=>{
 const c=CONFIG[S.layer],cells=c.coarse?D.fire_context.cells:D.cells;
 const esc=v=>'"'+String(v??'').replaceAll('"','""')+'"';
 const rows=[['celda','indicador','vista','periodo','escenario','umbral_m','valor','unidad','fuente'],...cells.map((cell,i)=>[cell.id,c.name,modeNames[S.mode],current.period,c.comparison?'':S.scenario,S.layer==='river_flood'?'0':S.layer==='river_flood_10cm'?'0.1':c.comparison&&S.layer!=='official'?S.threshold:'',current.arr[i],current.unit,c.url])];
 const blob=new Blob(['\ufeff'+rows.map(r=>r.map(esc).join(',')).join('\r\n')],{type:'text/csv;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`galicia-${S.layer}-${S.mode}.csv`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};
setGroup('heat');$('place').value='Santiago';selectCity('Santiago');
