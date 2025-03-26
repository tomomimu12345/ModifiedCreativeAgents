async function getConeVoxels(center, baseRadius, topRadius, height, isHollow) {
    const positions = [];

    for (let y = 0; y <= height; y++) {
        const currentRadius = Math.round(
        baseRadius + (topRadius - baseRadius) * (y / height)
        );
        const r2 = currentRadius * currentRadius;

        for (let x = -currentRadius; x <= currentRadius; x++) {
        for (let z = -currentRadius; z <= currentRadius; z++) {
            const dist2 = x * x + z * z;
            if (dist2 <= r2) {
            if (isHollow) {
                if (dist2 >= (currentRadius - 1) * (currentRadius - 1) || y === 0 || y === height) {
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
  
async function placeCone(bot, name, center, baseRadius, topRadius, height, isHollow) {
    const positions = await getConeVoxels(center, baseRadius, topRadius, height, isHollow);

    for (const pos of positions) {
        await placeItem(bot, name, pos);
    }
}