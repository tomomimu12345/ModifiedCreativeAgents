async function getCylinderVoxels(center, radius, height, isHollow) {
    const positions = [];
    const r2 = radius * radius;
    const startY = center.y;
    const endY = center.y + height - 1;

    for (let y = startY; y <= endY; y++) {
        for (let x = -radius; x <= radius; x++) {
        for (let z = -radius; z <= radius; z++) {
            const dist2 = x * x + z * z;
            if (dist2 <= r2) {
            if (isHollow) {
                if (dist2 >= (radius - 1) * (radius - 1) || y === startY || y === endY) {
                positions.push(new Vec3(center.x + x, y, center.z + z));
                }
            } else {
                positions.push(new Vec3(center.x + x, y, center.z + z));
            }
            }
        }
        }
    }
return positions;
}


async function placeCylinder(bot, name, center, radius, height, isHollow) {
    const positions = await getCylinderVoxels(center, radius, height, isHollow);

    for (const pos of positions) {
        await placeItem(bot, name, pos);
    }
}
  