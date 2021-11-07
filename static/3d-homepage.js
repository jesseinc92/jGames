// 3D BACKGROUND FOR SITE INDEX
import * as THREE from 'https://cdn.skypack.dev/three@0.129.0/build/three.module.js';
import { GLTFLoader } from 'https://cdn.skypack.dev/three@0.129.0/examples/jsm/loaders/GLTFLoader.js';


const canvas = document.getElementById('3d-canvas');
const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
}

// HANDLE PAGE RESIZE

window.addEventListener('resize', () => {
    sizes.width = window.innerWidth;
    sizes.height = window.innerHeight;

    camera.aspect = sizes.width / sizes.height;

    camera.updateProjectionMatrix();
    renderer.setSize(sizes.width, sizes.height);
});


const loader = new GLTFLoader();
let XboxController1 = new THREE.Object3D();

loader.load('/static/assets/xbox-controller-black/scene.gltf', (gltf) => {
    XboxController1 = gltf.scene;
    scene.add(XboxController1);

    XboxController1.position.y = 0.5;
});

let XboxController2 = new THREE.Object3D();

loader.load('/static/assets/xbox-controller-white/scene.gltf', (gltf) => {
    XboxController2 = gltf.scene;
    scene.add(gltf.scene);

    XboxController2.rotation.y = Math.PI;
    XboxController2.position.y = 0.5;
});


const scene = new THREE.Scene();

const ambientLight = new THREE.AmbientLight(0xffffff);
const pointLight = new THREE.PointLight(0xffffff, 5);
pointLight.position.y = 4;

const camera = new THREE.PerspectiveCamera(75, sizes.width/sizes.height, 1, 100);
camera.position.y = 2;
camera.position.z = 2;
camera.lookAt(0, 0, 0);

scene.add(camera, ambientLight, pointLight);

const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    alpha: true,
    antialias: true,
});
renderer.setSize(sizes.width, sizes.height);
renderer.setClearColor(0x512DA8)


// RENDER THE SCENE
const animate = () => {

    renderer.render(scene, camera)

    XboxController1.rotation.y += 0.01;
    XboxController2.rotation.y += 0.01;

    requestAnimationFrame(animate)
}

animate();