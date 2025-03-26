async function getSphereVoxels(center, radius, isHollow) {
    const positions = [];
    const r2 = radius * radius;

    for (let x = -radius; x <= radius; x++) {
        for (let y = -radius; y <= radius; y++) {
        for (let z = -radius; z <= radius; z++) {
            const dist2 = x * x + y * y + z * z;
            if (dist2 <= r2) {
            if (isHollow) {
                if (dist2 >= (radius - 1) * (radius - 1)) {
                positions.push(new Vec3(center.x + x, center.y + y, center.z + z));
                }
            } else {
                positions.push(new Vec3(center.x + x, center.y + y, center.z + z));
            }
            }
        }
        }
    }
    return positions;
}
  
async function placeSphere(bot, name, center, radius, isHollow) {
    const positions = await getSphereVoxels(center, radius, isHollow);

    for (const pos of positions) {
        await placeItem(bot, name, pos);
    }
}