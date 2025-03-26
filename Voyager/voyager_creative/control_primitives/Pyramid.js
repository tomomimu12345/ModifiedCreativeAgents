async function getPyramidVoxels(center, baseSize, height, isHollow) {
    const positions = [];

    for (let y = 0; y < height; y++) {
        const layerSize = baseSize - 2 * y;
        if (layerSize <= 0) break;

        const minX = center.x - Math.floor(layerSize / 2);
        const maxX = center.x + Math.floor(layerSize / 2);
        const minZ = center.z - Math.floor(layerSize / 2);
        const maxZ = center.z + Math.floor(layerSize / 2);
        const yPos = center.y + y;

        for (let x = minX; x <= maxX; x++) {
        for (let z = minZ; z <= maxZ; z++) {
            if (isHollow) {
            if (x === minX || x === maxX || z === minZ || z === maxZ || y === height - 1) {
                positions.push(new Vec3(x, yPos, z));
            }
            } else {
            positions.push(new Vec3(x, yPos, z));
            }
        }
        }
    }

    return positions;
}
  

async function placePyramid(bot, name, center, baseSize, height, isHollow) {
    const positions = await getPyramidVoxels(center, baseSize, height, isHollow);

    for (const pos of positions) {
        await placeItem(bot, name, pos);
    }
}