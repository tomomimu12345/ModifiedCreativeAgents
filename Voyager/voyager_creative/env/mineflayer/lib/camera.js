const { Viewer, WorldView, getBufferFromStream } = require('prismarine-viewer').viewer;
const { EventEmitter } = require('events');
const THREE = require('three');
const { createCanvas } = require('node-canvas-webgl/lib');
const { Vec3 } = require('vec3');
const fs = require('fs').promises;

class Camera extends EventEmitter {
    constructor(bot) {
        super();
        this.bot = bot;
        this.viewDistance = 4;
        this.width = 512;
        this.height = 512;
        this.canvas = createCanvas(this.width, this.height);
        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas });
        this.viewer = new Viewer(this.renderer);
    }

    async init() {
        const botPos = this.bot.entity.position;
        const center = new Vec3(botPos.x, botPos.y + 10, botPos.z);
        this.viewer.setVersion(this.bot.version);

        const worldView = new WorldView(this.bot.world, this.viewDistance, center);
        this.viewer.listen(worldView);
        this.viewer.camera.position.set(center.x, center.y, center.z);

        await worldView.init(center);
        console.log("Camera initialized.");
    }

    async takePicture(direction, name) {
        const cameraPos = new Vec3(this.viewer.camera.position.x, this.viewer.camera.position.y, this.viewer.camera.position.z);
        const point = cameraPos.add(direction);
        this.viewer.camera.lookAt(point.x, point.y, point.z);
        console.info('Waiting for world to load');
        await new Promise(resolve => setTimeout(resolve, 3000));
        this.renderer.render(this.viewer.scene, this.viewer.camera);

        const imageStream = this.canvas.createJPEGStream({
            bufsize: 4096,
            quality: 100,
            progressive: false
        });
        const buf = await getBufferFromStream(imageStream);
        let stats;
        try {
            stats = await fs.stat('./screenshots');
        } catch (e) {
            if (!stats?.isDirectory()) {
                await fs.mkdir('./screenshots');
            }
        }
        await fs.writeFile(`./screenshots/${name}.jpg`, buf);
        console.log(`Screenshot saved as ./screenshots/${name}.jpg`);
    }
}

module.exports = Camera;
