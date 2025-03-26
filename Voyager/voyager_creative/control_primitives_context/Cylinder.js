async function placeCylinder(bot, name, center, radius, height, isHollow) {
    const positions = await getCylinderVoxels(center, radius, height, isHollow);

    for (const pos of positions) {
        await placeItem(bot, name, pos);
    }
}