import * as THREE from
"https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js";

import { OrbitControls } from
"https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/controls/OrbitControls.js";

const container =
document.getElementById("robotCanvas");

const missionText =
document.getElementById("missionText");

const terminal =
document.getElementById("terminalOutput");

const startButton =
document.getElementById("startMission");

const aiButton =
document.getElementById("aiMode");

const resetButton =
document.getElementById("resetRobot");

const scene =
new THREE.Scene();

scene.background =
new THREE.Color(0x070b11);

const camera =
new THREE.PerspectiveCamera(
45,
container.clientWidth /
container.clientHeight,
0.1,
100
);

camera.position.set(
5,
3.2,
8
);

const renderer =
new THREE.WebGLRenderer({
antialias: true,
alpha: true
});

renderer.setPixelRatio(
Math.min(window.devicePixelRatio, 2)
);

renderer.setSize(
container.clientWidth,
container.clientHeight
);

renderer.shadowMap.enabled = true;

container.appendChild(
renderer.domElement
);

const controls =
new OrbitControls(
camera,
renderer.domElement
);

controls.enableDamping = true;

controls.enablePan = false;

controls.minDistance = 5;

controls.maxDistance = 12;

controls.target.set(
0,
1.5,
0
);

const ambientLight =
new THREE.HemisphereLight(
0x9edfff,
0x101010,
2
);

scene.add(
ambientLight
);

const keyLight =
new THREE.PointLight(
0x00e5ff,
25,
20
);

keyLight.position.set(
3,
5,
4
);

keyLight.castShadow = true;

scene.add(keyLight);

const fillLight =
new THREE.PointLight(
0x3355ff,
18,
20
);

fillLight.position.set(
-4,
3,
-3
);

scene.add(fillLight);

const floorGeometry =
new THREE.PlaneGeometry(
20,
20
);

const floorMaterial =
new THREE.MeshStandardMaterial({
color: 0x070b11,
metalness: .7,
roughness: .5
});

const floor =
new THREE.Mesh(
floorGeometry,
floorMaterial
);

floor.rotation.x =
-Math.PI / 2;

floor.receiveShadow = true;

scene.add(floor);

const grid =
new THREE.GridHelper(
20,
40,
0x00e5ff,
0x16313a
);

grid.position.y =
0.01;

scene.add(grid);

const robot =
new THREE.Group();

robot.position.y =
0;

scene.add(robot);

const robotMaterial =
new THREE.MeshStandardMaterial({
color: 0x9ca8b5,
metalness: .85,
roughness: .25
});

const darkMaterial =
new THREE.MeshStandardMaterial({
color: 0x151d27,
metalness: .9,
roughness: .2
});

const cyanMaterial =
new THREE.MeshStandardMaterial({
color: 0x00e5ff,
emissive: 0x00e5ff,
emissiveIntensity: 4,
metalness: .3,
roughness: .2
});

const head =
new THREE.Mesh(
new THREE.BoxGeometry(
1.15,
.85,
.9
),
robotMaterial
);

head.position.y =
2.8;

head.castShadow = true;

robot.add(head);

const face =
new THREE.Mesh(
new THREE.BoxGeometry(
.75,
.35,
.05
),
darkMaterial
);

face.position.set(
0,
2.8,
.46
);

robot.add(face);

function createEye(x) {

```
const eye =
    new THREE.Mesh(
        new THREE.SphereGeometry(
            .09,
            20,
            20
        ),
        cyanMaterial
    );

eye.position.set(
    x,
    2.82,
    .51
);

robot.add(eye);

return eye;
```

}

const leftEye =
createEye(-.2);

const rightEye =
createEye(.2);

const neck =
new THREE.Mesh(
new THREE.CylinderGeometry(
.18,
.18,
.25,
24
),
darkMaterial
);

neck.position.y =
2.25;

robot.add(neck);

const body =
new THREE.Mesh(
new THREE.BoxGeometry(
1.5,
1.55,
.95
),
robotMaterial
);

body.position.y =
1.45;

body.castShadow = true;

robot.add(body);

const chest =
new THREE.Mesh(
new THREE.BoxGeometry(
.75,
.5,
.06
),
darkMaterial
);

chest.position.set(
0,
1.5,
.5
);

robot.add(chest);

const core =
new THREE.Mesh(
new THREE.SphereGeometry(
.16,
24,
24
),
cyanMaterial
);

core.position.set(
0,
1.5,
.55
);

robot.add(core);

function createArm(x) {

```
const arm =
    new THREE.Group();


const upper =
    new THREE.Mesh(
        new THREE.CylinderGeometry(
            .16,
            .18,
            .9,
            16
        ),
        robotMaterial
    );


upper.position.y =
    -.45;


arm.add(upper);


const hand =
    new THREE.Mesh(
        new THREE.SphereGeometry(
            .2,
            16,
            16
        ),
        darkMaterial
    );


hand.position.y =
    -.95;


arm.add(hand);


arm.position.set(
    x,
    1.95,
    0
);


arm.rotation.z =
    x > 0 ? -.12 : .12;


robot.add(arm);

return arm;
```

}

const leftArm =
createArm(-.95);

const rightArm =
createArm(.95);

function createLeg(x) {

```
const leg =
    new THREE.Group();


const upper =
    new THREE.Mesh(
        new THREE.CylinderGeometry(
            .19,
            .21,
            1.05,
            16
        ),
        darkMaterial
    );


upper.position.y =
    -.52;


leg.add(upper);


const foot =
    new THREE.Mesh(
        new THREE.BoxGeometry(
            .4,
            .2,
            .65
        ),
        robotMaterial
    );


foot.position.set(
    0,
    -1.08,
    .15
);


leg.add(foot);


leg.position.set(
    x,
    .65,
    0
);


robot.add(leg);

return leg;
```

}

const leftLeg =
createLeg(-.4);

const rightLeg =
createLeg(.4);

const antenna =
new THREE.Mesh(
new THREE.CylinderGeometry(
.035,
.035,
.4,
12
),
darkMaterial
);

antenna.position.y =
3.42;

robot.add(antenna);

const antennaLight =
new THREE.Mesh(
new THREE.SphereGeometry(
.08,
16,
16
),
cyanMaterial
);

antennaLight.position.y =
3.65;

robot.add(antennaLight);

const idea =
new THREE.Group();

const cube =
new THREE.Mesh(
new THREE.BoxGeometry(
.55,
.55,
.55
),
cyanMaterial
);

idea.add(cube);

const ideaText =
document.createElement(
"canvas"
);

ideaText.width =
256;

ideaText.height =
128;

const ctx =
ideaText.getContext("2d");

ctx.fillStyle =
"#001014";

ctx.fillRect(
0,
0,
256,
128
);

ctx.fillStyle =
"#00e5ff";

ctx.font =
"bold 36px monospace";

ctx.textAlign =
"center";

ctx.fillText(
"IDEA",
128,
78
);

const textTexture =
new THREE.CanvasTexture(
ideaText
);

const label =
new THREE.Sprite(
new THREE.SpriteMaterial({
map: textTexture,
transparent: true
})
);

label.scale.set(
1.1,
.55,
1
);

label.position.z =
.3;

idea.add(label);

idea.position.set(
-2,
1.6,
0
);

scene.add(idea);

const workstation =
new THREE.Group();

const desk =
new THREE.Mesh(
new THREE.BoxGeometry(
2.8,
.3,
1.1
),
darkMaterial
);

desk.position.y =
1;

workstation.add(desk);

const monitor =
new THREE.Mesh(
new THREE.BoxGeometry(
1.8,
1.1,
.12
),
darkMaterial
);

monitor.position.set(
0,
2,
0
);

workstation.add(monitor);

const monitorGlow =
new THREE.Mesh(
new THREE.PlaneGeometry(
1.55,
.82
),
new THREE.MeshBasicMaterial({
color: 0x00e5ff
})
);

monitorGlow.position.set(
0,
2,
.07
);

workstation.add(
monitorGlow
);

workstation.position.x =
3.4;

scene.add(
workstation
);

let missionRunning =
false;

let aiMode =
false;

let missionProgress =
0;

function addTerminal(
message,
className = ""
) {

```
const line =
    document.createElement(
        "div"
    );

line.textContent =
    "> " + message;

if (className) {

    line.className =
        className;

}

terminal.appendChild(
    line
);


terminal.scrollTop =
    terminal.scrollHeight;
```

}

function startMission() {

```
if (missionRunning)
    return;


missionRunning =
    true;

missionProgress =
    0;


missionText.textContent =
    "Robot received an idea. Beginning delivery sequence.";


addTerminal(
    "MISSION STARTED"
);


addTerminal(
    "Idea package acquired."
);
```

}

function resetMission() {

```
missionRunning =
    false;

missionProgress =
    0;


robot.position.x =
    0;

idea.position.set(
    -2,
    1.6,
    0
);


idea.visible =
    true;


missionText.textContent =
    "Robot is waiting for an idea.";


addTerminal(
    "Mission reset."
);
```

}

function enableAI() {

```
aiMode =
    !aiMode;


if (aiMode) {

    addTerminal(
        "AI MODE ENABLED",
        "success"
    );


    addTerminal(
        "Python engine online."
    );


    addTerminal(
        "ML engine online."
    );


    addTerminal(
        "RAG pipeline ready."
    );


    missionText.textContent =
        "AI Mode active — neural systems are analyzing.";

}

else {

    addTerminal(
        "AI MODE DISABLED"
    );


    missionText.textContent =
        "Standard robot mode active.";

}
```

}

startButton.addEventListener(
"click",
startMission
);

resetButton.addEventListener(
"click",
resetMission
);

aiButton.addEventListener(
"click",
enableAI
);

const clock =
new THREE.Clock();

function animate() {

```
requestAnimationFrame(
    animate
);


const elapsed =
    clock.getElapsedTime();


controls.update();


head.rotation.y =
    Math.sin(
        elapsed * .8
    ) * .12;


antennaLight.scale.setScalar(
    1 +
    Math.sin(
        elapsed * 5
    ) * .15
);


core.scale.setScalar(
    1 +
    Math.sin(
        elapsed * 4
    ) * .12
);


idea.rotation.y =
    elapsed;


idea.position.y =
    1.6 +
    Math.sin(
        elapsed * 2
    ) * .12;


if (missionRunning) {

    missionProgress +=
        0.003;


    if (
        missionProgress < 0.5
    ) {

        const p =
            missionProgress /
            0.5;


        robot.position.x =
            p * 2.7 - 0.2;


        leftLeg.rotation.x =
            Math.sin(
                elapsed * 8
            ) * .45;


        rightLeg.rotation.x =
            -Math.sin(
                elapsed * 8
            ) * .45;


        leftArm.rotation.x =
            -Math.sin(
                elapsed * 8
            ) * .3;


        rightArm.rotation.x =
            Math.sin(
                elapsed * 8
            ) * .3;


        idea.position.x =
            robot.position.x -
            .9;

    }

    else if (
        missionProgress < 0.8
    ) {

        robot.position.x =
            2.5;


        idea.position.x =
            2.8;


        missionText.textContent =
            "Robot delivered the idea to the AI workstation.";


    }

    else {

        idea.visible =
            false;


        missionText.textContent =
            "🚀 Project generated successfully.";


        robot.position.x =
            2.5;


        missionRunning =
            false;


        addTerminal(
            "PROJECT GENERATED ✓",
            "success"
        );

    }

}


renderer.render(
    scene,
    camera
);
```

}

animate();

function resize() {

```
const width =
    container.clientWidth;

const height =
    container.clientHeight;


camera.aspect =
    width / height;


camera.updateProjectionMatrix();


renderer.setSize(
    width,
    height
);
```

}

window.addEventListener(
"resize",
resize
);

resize();
