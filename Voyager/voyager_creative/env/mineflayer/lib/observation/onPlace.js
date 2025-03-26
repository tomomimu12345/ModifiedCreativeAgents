const Observation = require("./base.js").Observation;

class onPlace extends Observation {
    constructor(bot) {
        super(bot);
        this.name = "onPlace";
        this.AABB = null;
        bot.on("blockPlace", (pos) => {
            if (!this.AABB) {
                this.AABB = {
                    min: { x: pos.x, y: pos.y, z: pos.z },
                    max: { x: pos.x + 1, y: pos.y + 1, z: pos.z + 1 },
                };
                return;
            }
    
            this.AABB.min.x = Math.min(this.AABB.min.x, pos.x);
            this.AABB.min.y = Math.min(this.AABB.min.y, pos.y);
            this.AABB.min.z = Math.min(this.AABB.min.z, pos.z);
            this.AABB.max.x = Math.max(this.AABB.max.x, pos.x + 1);
            this.AABB.max.y = Math.max(this.AABB.max.y, pos.y + 1);
            this.AABB.max.z = Math.max(this.AABB.max.z, pos.z + 1);
        });
    }

    observe() {
        const result = this.AABB;
        this.AABB = null;
        return result;
    }
}

module.exports = onPlace;
