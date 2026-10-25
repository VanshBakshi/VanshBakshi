import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const $ = (selector) => document.querySelector(selector);
const toast = $("#toast");
const logOutput = $("#logOutput");
const robotState = $("#robotState");
const viewportMode = $("#viewportMode");
let toastTimer;

function notify(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2400);
}

function addLog(message) {
  const now = new Date();
  const time = [now.getHours(), now.getMinutes(), now.getSeconds()]
    .map((n) => String(n).padStart(2, "0")).join(":");
  const row = document.createElement("p");
  const timeEl = document.createElement("time");
  const textEl = document.createElement("span");
  timeEl.textContent = time;
  textEl.textContent = message;
  row.append(timeEl, textEl);
  logOutput.prepend(row);
  while (logOutput.children.length > 4) logOutput.lastElementChild.remove();
}

const palettes = {
  forest: { bg: 0x06131b, fog: 0x06131b, floor: 0x09232a, accent: 0x63edff, accent2: 0x72ffc5, tree: 0x0a3a35, label: "FOREST" },
  cyber:  { bg: 0x08091e, fog: 0x08091e, floor: 0x15102d, accent: 0x8a7dff, accent2: 0xff5bd6, tree: 0x251b4b, label: "CYBER" },
  neural: { bg: 0x071421, fog: 0x071421, floor: 0x0a1d34, accent: 0x63edff, accent2: 0x5d8cff, tree: 0x102b49, label: "NEURAL" }
};

function createRobot(accentHex) {
  const root = new THREE.Group();
  root.name = "VNX-01";
  const accent = new THREE.Color(accentHex);
  const metal = new THREE.MeshStandardMaterial({ color: 0x9eb6c8, metalness: .86, roughness: .24 });
  const darkMetal = new THREE.MeshStandardMaterial({ color: 0x16283a, metalness: .8, roughness: .3 });
  const black = new THREE.MeshStandardMaterial({ color: 0x050b14, metalness: .45, roughness: .22 });
  const glow = new THREE.MeshStandardMaterial({ color: accent, emissive: accent, emissiveIntensity: 2.3, metalness: .35, roughness: .18 });
  const glowSoft = new THREE.MeshStandardMaterial({ color: accent, emissive: accent, emissiveIntensity: .7, metalness: .45, roughness: .3 });
  const white = new THREE.MeshStandardMaterial({ color: 0xe4f6ff, metalness: .65, roughness: .2 });
  const body = new THREE.Group();
  root.add(body);
  const mesh = (geo, mat, parent, x, y, z, sx=1, sy=1, sz=1) => {
    const m = new THREE.Mesh(geo, mat);
    m.position.set(x,y,z); m.scale.set(sx,sy,sz); m.castShadow = true; m.receiveShadow = true;
    parent.add(m); return m;
  };
  const box = (x,y,z,sx,sy,sz,mat,parent=body, bevel=.08) => {
    const geo = new THREE.BoxGeometry(sx,sy,sz);
    const m = mesh(geo, mat, parent, x,y,z);
    if (bevel > 0) {
      const edges = new THREE.EdgesGeometry(geo);
      const lines = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({color: accent, transparent:true, opacity:.28}));
      lines.position.copy(m.position); lines.scale.copy(m.scale); parent.add(lines);
    }
    return m;
  };
  const sphere = (x,y,z,sx,sy,sz,mat,parent=body) => mesh(new THREE.SphereGeometry(1,24,18),mat,parent,x,y,z,sx,sy,sz);
  const cylinder = (x,y,z,r1,r2,h,mat,parent=body,segments=20) => mesh(new THREE.CylinderGeometry(r1,r2,h,segments),mat,parent,x,y,z);

  // Legs and feet
  for (const side of [-1,1]) {
    const leg = new THREE.Group(); leg.position.set(side*.48,-.82,0); body.add(leg);
    cylinder(0,-.17,0,.19,.23,.18,darkMetal,leg);
    box(0,-.48,0,.27,.52,.3,metal,leg,.05);
    sphere(0,-.47,.165,.1,.22,.035,glowSoft,leg);
    cylinder(0,-.78,0,.17,.16,.14,darkMetal,leg);
    box(0,-1.02,.1,.39,.18,.57,black,leg,.045);
    box(0,-.97,.34,.25,.035,.04,glow,leg,.01);
    leg.userData.side = side; leg.userData.isLeg = true;
  }
  // Torso, core and armor
  box(0,.02,0,1.24,1.25,.62,darkMetal,body,.12);
  box(0,.04,.335,.91,.9,.1,metal,body,.07);
  box(0,.04,.397,.67,.62,.055,black,body,.035);
  const core = sphere(0,.1,.45,.19,.19,.09,glow);
  core.name = "core";
  const coreRing = mesh(new THREE.TorusGeometry(.28,.025,8,48),glowSoft,body,0,.1,.46);
  coreRing.name = "coreRing";
  const chestTop = box(0,.53,.37,.52,.11,.09,white,body,.025);
  for (let i=0;i<3;i++) box(-.18+i*.18,-.32,.4,.08,.035,.03,glowSoft,body,.01);
  // Shoulder joints and articulated arms
  const arms = [];
  for (const side of [-1,1]) {
    const arm = new THREE.Group(); arm.position.set(side*.77,.39,0); body.add(arm);
    sphere(0,0,0,.23,.24,.23,darkMetal,arm);
    box(side*.03,-.29,0,.31,.48,.34,metal,arm,.06);
    box(0,-.28,.185,.15,.25,.035,glowSoft,arm,.02);
    sphere(0,-.58,.02,.17,.17,.17,darkMetal,arm);
    box(0,-.78,.02,.27,.3,.28,metal,arm,.04);
    box(0,-.79,.18,.12,.16,.035,black,arm,.015);
    for (let k=0;k<3;k++) box(-.07+k*.07,-.96,.13,.025,.07,.04,glowSoft,arm,.01);
    arm.userData.side=side; arms.push(arm);
  }
  // Neck and head assembly
  cylinder(0,.75,0,.19,.23,.24,darkMetal,body);
  const head = new THREE.Group(); head.position.set(0,1.18,.02); body.add(head);
  box(0,0,0,.95,.72,.67,metal,head,.1);
  box(0,-.03,.35,.76,.38,.09,black,head,.045);
  // Visor and two glowing eyes
  box(0,-.01,.405,.66,.25,.045,darkMetal,head,.025);
  const eyes=[];
  for (const side of [-1,1]) {
    const eye = sphere(side*.19,.01,.445,.105,.052,.035,glow,head);
    eyes.push(eye);
    box(side*.36,-.02,.39,.055,.18,.06,glowSoft,head,.015);
    // Ear modules
    box(side*.52,-.02,0,.12,.3,.28,darkMetal,head,.035);
    box(side*.535,.015,.13,.05,.1,.04,glow,head,.01);
  }
  // Antenna and crown sensor
  cylinder(0,.43,0,.035,.045,.18,darkMetal,head);
  sphere(0,.55,0,.075,.075,.075,glow,head);
  const antennaLine = new THREE.Mesh(new THREE.CylinderGeometry(.012,.012,.25,8),glow);
  antennaLine.position.set(0,.45,0); head.add(antennaLine);
  // Small back pack
  box(0,.04,-.42,.63,.7,.22,darkMetal,body,.07);
  for (let i=0;i<3;i++) {
    const fin = box(-.19+i*.19,.05,-.56,.08,.45,.05,glowSoft,body,.015);
    fin.userData.finIndex=i;
  }
  // Floating micro particles orbiting around the robot
  const particleGroup = new THREE.Group(); root.add(particleGroup);
  const particleMat = new THREE.MeshBasicMaterial({color:accent, transparent:true, opacity:.75});
  for(let i=0;i<30;i++){
    const p = new THREE.Mesh(new THREE.SphereGeometry(.012+(i%3)*.006,8,8),particleMat);
    const a = i/30*Math.PI*2, r=1.2+(i%5)*.07;
    p.position.set(Math.cos(a)*r,((i%7)-3)*.19,Math.sin(a)*r);
    p.userData.phase=a; p.userData.radius=r; particleGroup.add(p);
  }
  root.userData = { body, head, arms, eyes, core, coreRing, particleGroup, accent, glow, glowSoft, metal, darkMetal, black, white };
  root.scale.setScalar(.82);
  root.position.y = .1;
  return root;
}

function createForest(scene, palette) {
  const group = new THREE.Group();
  const trunkMat = new THREE.MeshStandardMaterial({color:0x152e35, roughness:1});
  const leafMat = new THREE.MeshStandardMaterial({color:palette.tree, roughness:.9, metalness:.05});
  const leafMat2 = new THREE.MeshStandardMaterial({color:palette.accent2, roughness:.8, emissive:palette.accent2, emissiveIntensity:.15});
  for(let i=0;i<64;i++){
    const a = i*2.39996;
    const radius = 3.8 + (i%9)*.46;
    const x = Math.cos(a)*radius, z = Math.sin(a)*radius;
    const h = 1.7 + (i%5)*.32;
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(.045,.09,h,6),trunkMat);
    trunk.position.set(x,h/2-0.5,z); group.add(trunk);
    const cone = new THREE.Mesh(new THREE.ConeGeometry(.38+(i%3)*.1,1.25+(i%4)*.2,7),i%4===0?leafMat2:leafMat);
    cone.position.set(x,h*.68,z); cone.rotation.y=a; group.add(cone);
    if(i%3===0){
      const glow = new THREE.Mesh(new THREE.SphereGeometry(.035,8,8),new THREE.MeshBasicMaterial({color:palette.accent2}));
      glow.position.set(x,h*.8,z); group.add(glow);
    }
  }
  scene.add(group); return group;
}

function createStars(scene, count=500, spread=25, color=0x8eefff) {
  const positions = new Float32Array(count*3);
  for(let i=0;i<count;i++){
    positions[i*3]=(Math.random()-.5)*spread;
    positions[i*3+1]=(Math.random()-.25)*spread;
    positions[i*3+2]=(Math.random()-.5)*spread;
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position",new THREE.BufferAttribute(positions,3));
  const material = new THREE.PointsMaterial({color,size:.025,transparent:true,opacity:.8,sizeAttenuation:true});
  const points = new THREE.Points(geometry,material); scene.add(points); return points;
}

function createScene(container, large=false) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(palettes.forest.bg);
  scene.fog = new THREE.FogExp2(palettes.forest.fog, large ? .027 : .034);
  const camera = new THREE.PerspectiveCamera(large ? 42 : 39, 1, .1, 100);
  camera.position.set(large ? 0 : 0.2, large ? 2.0 : 1.45, large ? 7.2 : 6.5);
  const renderer = new THREE.WebGLRenderer({antialias:true,alpha:false,powerPreference:"high-performance"});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.8));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.18;
  renderer.domElement.setAttribute("aria-label","Interactive 3D robot. Drag to rotate and use the scroll wheel to zoom.");
  container.appendChild(renderer.domElement);

  const controls = new OrbitControls(camera,renderer.domElement);
  controls.enableDamping=true; controls.dampingFactor=.06; controls.enablePan=false;
  controls.minDistance=3.7; controls.maxDistance=10;
  controls.minPolarAngle=.55; controls.maxPolarAngle=2.25;
  controls.target.set(0,.25,0);
  if(!large){ controls.enableZoom=false; controls.enableRotate=false; controls.enablePan=false; }

  scene.add(new THREE.HemisphereLight(0x9edfff,0x10202b,2.0));
  const key = new THREE.DirectionalLight(0xc9f7ff,3.2); key.position.set(3,6,5); key.castShadow=true; scene.add(key);
  const rim = new THREE.PointLight(0x1bcfff,35,12); rim.position.set(-3,2,2); scene.add(rim);
  const fill = new THREE.PointLight(0x5c6cff,22,10); fill.position.set(3,1,-3); scene.add(fill);
  const floor = new THREE.Mesh(new THREE.CircleGeometry(10,80),new THREE.MeshStandardMaterial({color:palettes.forest.floor,roughness:.72,metalness:.18}));
  floor.rotation.x=-Math.PI/2; floor.position.y=-1.57; floor.receiveShadow=true; scene.add(floor);
  const grid = new THREE.GridHelper(18,36,0x1a8ba4,0x164054);
  grid.position.y=-1.55; grid.material.transparent=true; grid.material.opacity=.23; scene.add(grid);
  const forest=createForest(scene,palettes.forest);
  const stars=createStars(scene,large?700:380,large?30:24,palettes.forest.accent);
  const robot=createRobot(palettes.forest.accent); scene.add(robot);
  const scanRing = new THREE.Mesh(new THREE.TorusGeometry(1.65,.009,5,120),new THREE.MeshBasicMaterial({color:palettes.forest.accent,transparent:true,opacity:.55}));
  scanRing.rotation.x=Math.PI/2; scanRing.position.y=-1.48; scanRing.visible=false; scene.add(scanRing);
  const scanBeam = new THREE.Mesh(new THREE.PlaneGeometry(4.5,.025),new THREE.MeshBasicMaterial({color:palettes.forest.accent,transparent:true,opacity:.65,side:THREE.DoubleSide}));
  scanBeam.position.set(0,-.2,0); scanBeam.visible=false; scene.add(scanBeam);

  const state={container,scene,camera,renderer,controls,robot,forest,stars,floor,grid,scanRing,scanBeam,large,paused:false,mode:"forest",scanUntil:0,coreUntil:0,clock:new THREE.Clock(),raf:0,disposed:false};
  const resize=()=>{
    const width=Math.max(container.clientWidth,1), height=Math.max(container.clientHeight,1);
    camera.aspect=width/height; camera.updateProjectionMatrix(); renderer.setSize(width,height,false);
  };
  const observer=new ResizeObserver(resize); observer.observe(container); resize();
  state.resizeObserver=observer;

  function animate(){
    if(state.disposed) return;
    state.raf=requestAnimationFrame(animate);
    const t=state.clock.getElapsedTime();
    if(!state.paused){
      robot.position.y=.1+Math.sin(t*1.15)*.055;
      robot.rotation.y = large ? robot.rotation.y : Math.sin(t*.42)*.14;
      const data=robot.userData;
      data.head.rotation.y=Math.sin(t*.7)*.12;
      data.head.rotation.x=Math.sin(t*.55)*.035;
      data.arms.forEach((arm,i)=>{ arm.rotation.z=Math.sin(t*1.1+i*Math.PI)*.055; });
      data.eyes.forEach((eye,i)=>{ eye.scale.y=.052*(1+Math.sin(t*2+i)*.08); });
      data.core.material.emissiveIntensity=2.1+Math.sin(t*3.2)*.55+(performance.now()<state.coreUntil?2.8:0);
      data.coreRing.rotation.z=t*.7;
      data.particleGroup.rotation.y=t*.2;
      data.particleGroup.children.forEach((p,i)=>{p.position.y=Math.sin(t*1.3+p.userData.phase)*.28+((i%7)-3)*.19;});
      forest.rotation.y=Math.sin(t*.06)*.025;
      stars.rotation.y=t*.008;
    }
    if(performance.now()<state.scanUntil){
      const progress=1-(state.scanUntil-performance.now())/2200;
      scanRing.visible=true; scanRing.scale.setScalar(.5+progress*1.3);
      scanRing.material.opacity=Math.max(0,1-progress)*.8;
      scanBeam.visible=true; scanBeam.position.y=-1.25+progress*2.65;
      scanBeam.material.opacity=Math.max(0,1-progress)*.75;
    } else { scanRing.visible=false; scanBeam.visible=false; }
    controls.update();
    renderer.render(scene,camera);
  }
  animate();
  state.setMode=(mode)=>{
    const p=palettes[mode]||palettes.forest; state.mode=mode;
    scene.background.setHex(p.bg); scene.fog.color.setHex(p.fog);
    floor.material.color.setHex(p.floor); grid.material.color.setHex(p.accent);
    robot.userData.accent.setHex(p.accent);
    robot.userData.glow.color.setHex(p.accent); robot.userData.glow.emissive.setHex(p.accent);
    robot.userData.glowSoft.color.setHex(p.accent); robot.userData.glowSoft.emissive.setHex(p.accent);
    robot.userData.particleGroup.children.forEach((part)=>part.material.color.setHex(p.accent));
    stars.material.color.setHex(p.accent);
    scanRing.material.color.setHex(p.accent); scanBeam.material.color.setHex(p.accent);
    forest.children.forEach((obj)=>{
      if(obj.material && obj.material.color){
        if(obj.material.color.getHex()===palettes.forest.tree) obj.material.color.setHex(p.tree);
      }
    });
    rim.color.setHex(p.accent); fill.color.setHex(p.accent2);
    viewportMode.textContent=`MODE: ${p.label}`;
    state.renderer.render(scene,camera);
  };
  state.scan=()=>{state.scanUntil=performance.now()+2200;};
  state.pulse=()=>{state.coreUntil=performance.now()+1300;};
  state.reset=()=>{
    camera.position.set(large?0:.2,large?2:1.45,large?7.2:6.5);
    controls.target.set(0,.25,0); controls.update();
    robot.rotation.set(0,0,0);
  };
  state.destroy=()=>{state.disposed=true;cancelAnimationFrame(state.raf);observer.disconnect();controls.dispose();renderer.dispose();container.removeChild(renderer.domElement);};
  return state;
}

let heroScene, labScene;
try {
  heroScene = createScene($("#robot-stage"), false);
  labScene = createScene($("#lab-stage"), true);
  addLog("VNX-01 3D renderer connected.");
  addLog("Forest environment loaded.");
} catch (error) {
  console.error(error);
  const message = document.createElement("div");
  message.style.cssText="position:absolute;inset:15%;display:grid;place-items:center;text-align:center;color:#9bb3c8;font:12px Inter,sans-serif;line-height:1.8;";
  message.textContent="3D scene could not start. Please open this site in a modern browser with WebGL enabled and an internet connection.";
  $("#robot-stage")?.appendChild(message.cloneNode(true));
  $("#lab-stage")?.appendChild(message);
  addLog("Renderer error. Check WebGL/browser support.");
}

function setMode(mode) {
  heroScene?.setMode(mode);
  labScene?.setMode(mode);
  document.querySelectorAll(".mode-button").forEach((btn)=>btn.classList.toggle("selected",btn.dataset.mode===mode));
  addLog(`${mode.toUpperCase()} environment activated.`);
  notify(`${mode.toUpperCase()} MODE ACTIVATED`);
}
document.querySelectorAll(".mode-button").forEach((btn)=>btn.addEventListener("click",()=>setMode(btn.dataset.mode)));

$("#scanBtn").addEventListener("click",()=>{
  heroScene?.scan(); labScene?.scan();
  robotState.textContent="ROBOT STATUS: SCANNING";
  addLog("Diagnostic scan initiated.");
  notify("SYSTEM SCAN IN PROGRESS");
  setTimeout(()=>{robotState.textContent="ROBOT STATUS: ALL VISUAL SYSTEMS NOMINAL";addLog("Visual diagnostics complete.");},2200);
});
$("#coreBtn").addEventListener("click",()=>{
  heroScene?.pulse(); labScene?.pulse();
  addLog("AI core energy pulse triggered.");
  notify("AI CORE PULSE ACTIVATED");
});
let paused=false;
$("#motionBtn").addEventListener("click",()=>{
  paused=!paused;
  if(heroScene) heroScene.paused=paused;
  if(labScene) labScene.paused=paused;
  addLog(paused?"Idle animation paused.":"Idle animation resumed.");
  notify(paused?"ANIMATION PAUSED":"ANIMATION RESUMED");
});
$("#resetBtn").addEventListener("click",()=>{
  heroScene?.reset(); labScene?.reset();
  addLog("Camera and robot orientation reset.");
  notify("VIEWPORT RESET");
});

const menuToggle=$("#menuToggle"), nav=$(".main-nav");
menuToggle.addEventListener("click",()=>nav.classList.toggle("open"));
nav.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>nav.classList.remove("open")));

const navLinks=[...document.querySelectorAll(".main-nav a")];
const sectionObserver=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{
    if(entry.isIntersecting){
      navLinks.forEach(link=>link.classList.toggle("active",link.getAttribute("href")===`#${entry.target.id}`));
    }
  });
},{rootMargin:"-35% 0px -55% 0px"});
["home","lab","projects","about"].forEach(id=>{const el=document.getElementById(id);if(el)sectionObserver.observe(el);});

window.addEventListener("beforeunload",()=>{heroScene?.destroy();labScene?.destroy();});
